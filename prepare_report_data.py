#!/usr/bin/env python3
"""Prepare chart data for the p(doom) submissions report.

Reads the exported ``pdoom-submissions.json`` and emits the compact JSON blob
the report pages under ``reports/`` render from:

    {
      "rows":      [{"t", "m", "p10", "p90", "f", "fx": [pAI, pDB, pGC]}, ...],
      "months":    [{"month", "n", "median", "p25", "p75"}, ...],
      "titles":    [{"id", "label", "seen", "of"}, ...],
      "risks":     [{"id", "label", "seen", "of"}, ...],
      "flows":     [{"id", "label", "n"}, ...],
      "expertQ":   [{"id", "label", "kind", "opts", "median", "none"}, ...],
      "experts":   [{"names", "m"}, ...],
      "knowledge": {"terms", "real", "decoys", "takers", "pairs": [...], "taker": {...}},
      "sliders":   [{"m", "p10", "p90", "factors"}, ...],
      "dupes":     {"records", "unique", "byLevel": {level: {records, unique, median, medianDedup}}},
      "identity":  {"signed", "valid", "invalid", "unchecked", "unsigned", "visitors",
                    "repeat", "maxPerVisitor", "replays", "mismatched"},
      "gate":      {"attempted", "verified", "overrode", "accepted", "acceptedTo",
                    "medianScore", "scores"},
      "mediumQ":   [{"id", "label", "kind", "rho", "n"}, ...],
      "prompts":   [{"label", "n", "median", "values"}, ...],
      "mediumVuln":[{"known", "of", "m"}, ...],
      "vulnList":  [{"label", "known", "of", "ai"}, ...],
      "beginners": [{"films", "risks", "m", "p10", "p90", "spread", "g", "rg"}, ...]
    }

``rows`` is one entry per submission, sorted by timestamp; ``fx`` holds the
midpoints of the three chain factors. ``months`` aggregates the final p(doom)
midpoint per calendar month (UTC).

``titles`` and ``beginners`` back the film-exposure section, and need the quiz
option list, which is parsed out of ``index.html``. Each title's ``of`` is the
number of beginners who could actually have ticked it -- options added partway
through (see ``OPTION_ADDED``) get a smaller denominator than the full cohort.
``risks`` does the same for the catastrophe checklist. ``beginners`` buckets each
beginner respondent twice: ``g`` by how many titles they ticked, ``rg`` by how many
risks they recognised.

Usage:
    python3 prepare_report_data.py                      # blob to stdout
    python3 prepare_report_data.py -o data.json         # blob to file
    python3 prepare_report_data.py --inject reports/submissions-2026-08-18.html

A summary (group/era medians, factor correlations) is printed to stderr so the
headline numbers quoted in the report can be re-checked after a data refresh.

Report files are named ``reports/submissions-<YYYY-MM-DD>.html``, where the date is
the ``exported_at`` date of the submissions JSON the report was built from -- not the
day it was written -- so the filename says which data it covers.
"""

import argparse
import base64
import json
import math
import re
import statistics
import sys
from collections import Counter

# Signature verification needs `cryptography` (see requirements.txt). It is
# imported softly so the rest of the report still builds without it -- but the
# absence is reported loudly rather than passing off unchecked rows as fine.
try:
    from cryptography.exceptions import InvalidSignature
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
    HAVE_CRYPTO = True
except ImportError:  # pragma: no cover - depends on the local environment
    HAVE_CRYPTO = False

FACTOR_KEYS = ("powerfulAi", "dangerousBehavior", "globalCatastrophe")
QUIZ_LEVELS = ("beginner", "medium", "expert")

# Entertainment options added after the quiz launched. A respondent who submitted
# before an option existed never had the chance to tick it, so it is excluded from
# that option's denominator. Refresh after adding a title with:
#   git log --format=%ad --date=short -S'<option-id>' -- index.html | tail -1
OPTION_ADDED = {
    "entertainment-ironman": "2026-06-17",
    "entertainment-eagle-eye": "2026-08-18",
}

# Film-exposure groups: how many entertainment titles a respondent ticked.
GROUP_A_MIN = 12  # A: seen the most
GROUP_B_MIN = 7   # B: middle; C: everything below

# Risk-awareness groups: how many catastrophe types a respondent recognised (of 12).
RISK_A_MIN = 11
RISK_B_MIN = 9

# The quiz-level chooser went live with the level flows; submissions before this
# date predate the chooser entirely and are excluded from the flow breakdown.
QUIZ_LAUNCH = "2026-03-09"

FLOW_LABELS = [
    ("decide", "Decide the right level for me"),
    ("beginner", "Beginner quiz"),
    ("medium", "Medium quiz"),
    ("expert", "Expert quiz"),
    ("none", "No quiz (sliders)"),
]

# The expert quiz mixes questions answerable by reasoning with questions that only
# someone following the field can answer. Splitting them is the point of the section.
# Every knowledge-check decoy is a keyword collision with a real AI term -- that is
# the mechanism the check tests. The pairing is editorial; the flags come from the page.
DECOY_COLLISIONS = {
    "all-you-need-is-love": "Attention Is All You Need",
    "the-real-slim-shady": "Attention Is All You Need",
    "adhd": "Attention Is All You Need",
    "operation-paperclip": "Paperclip maximizer",
    "agent-orange": "Agent",
    "james-bond": "Agent",
    "standard-model": "Model",
    "wireframe-model": "Model",
    "personal-trainer": "Training data",
    "clinical-supervisor": "Unsupervised learning",
    "reinforced-concrete": "Reinforcement learning",
}

# The medium quiz mixes questions about what the visitor knows or has experienced with
# questions asking what they believe. An opinion about risk correlating with an estimate
# of risk is close to tautological, so the two kinds are reported apart.
MEDIUM_QUESTIONS = [
    ("medium-vulnerabilities", "Vulnerabilities recognised", "knowledge"),
    ("medium-system-prompts", "System-prompt familiarity", "knowledge"),
    ("medium-off-the-rails", "Seen AI go off the rails", "knowledge"),
    ("medium-speed", "Can humans react in time?", "opinion"),
    ("medium-governance", "Can governance keep AI safe?", "opinion"),
    ("medium-competition", "Competition lowers barriers", "opinion"),
]

# Which entries on the vulnerability checklist are AI-native rather than general
# infosec. Editorial, like the expert-question split; the labels come from the page.
AI_NATIVE_VULNS = {
    "medium-vulnerabilities-prompt-injection",
    "medium-vulnerabilities-data-poisoning",
    "medium-vulnerabilities-sleeper-agent",
    "medium-vulnerabilities-adversarial",
    "medium-vulnerabilities-model-stealing",
}

EXPERT_QUESTIONS = [
    ("expert-continuous-learning", "Ways AI keeps learning", "concept"),
    ("expert-self-improvement", "Ways AI self-improves", "concept"),
    ("expert-self-replication", "Ways AI self-replicates", "concept"),
    ("expert-campaign-organisations", "Campaign organisations", "names"),
    ("expert-research-organisations", "Research organisations", "names"),
    ("expert-commentators", "Commentators", "names"),
    ("expert-content-creators", "Content creators", "names"),
]


def load_rows(submissions):
    rows = []
    for s in submissions:
        summary = s["summary"]
        factors = {f["key"]: round(f["midpoint"], 4) for f in s["factors"]}
        rows.append({
            "t": s["submitted_at"][:16],  # minute resolution is enough for the charts
            "m": round(summary["midpoint"], 4),
            "p10": round(summary["p10"], 4),
            "p90": round(summary["p90"], 4),
            "f": s.get("quiz_flow_id") or "untagged",
            "fx": [factors[k] for k in FACTOR_KEYS],
        })
    rows.sort(key=lambda r: r["t"])
    return rows


def monthly_aggregates(rows):
    by_month = {}
    for r in rows:
        by_month.setdefault(r["t"][:7], []).append(r["m"])
    months = []
    for month in sorted(by_month):
        vals = sorted(by_month[month])
        n = len(vals)
        if n >= 2:
            q = statistics.quantiles(vals, n=4)
            p25, p75 = q[0], q[2]
        else:
            p25 = p75 = vals[0]
        months.append({
            "month": month,
            "n": n,
            "median": round(statistics.median(vals), 4),
            "p25": round(p25, 4),
            "p75": round(p75, 4),
        })
    return months


def parse_options(index_html, question_id, next_question_id):
    """Pull one question's options (id, label) out of index.html, in display order."""
    with open(index_html) as f:
        html = f.read()
    try:
        start = html.index(f"id: '{question_id}'")
        end = html.index(f"id: '{next_question_id}'", start)
    except ValueError:
        sys.exit(f"error: could not locate the {question_id} options in {index_html}")
    found = re.findall(r"\{\s*id:\s*'([^']+)',\s*label:\s*'((?:[^'\\]|\\.)*)'", html[start:end])
    return [(oid, label.replace("\\'", "'")) for oid, label in found]


def beginner_answers(submissions, question_id):
    """(submitted_at, set of ticked option ids, submission) per beginner respondent."""
    out = []
    for s in submissions:
        if s.get("quiz_flow_id") != "beginner":
            continue
        for a in s.get("quiz_answers") or []:
            if a["question_id"] == question_id:
                out.append((s["submitted_at"][:10], set(a.get("values") or []), s))
    return out


def option_counts(submissions, options, question_id):
    """Tick-counts per option, with denominators adjusted for options added late."""
    answers = beginner_answers(submissions, question_id)
    titles = []
    for oid, label in options:
        added = OPTION_ADDED.get(oid)
        # same-day submissions are ambiguous (the edit may have landed after them),
        # so an option only counts for respondents who submitted strictly later
        eligible = [a for a in answers if added is None or a[0] > added]
        titles.append({
            "id": oid,
            "label": label,
            "seen": sum(1 for _, ticked, _ in eligible if oid in ticked),
            "of": len(eligible),
        })
    titles.sort(key=lambda t: (-(t["seen"] / t["of"] if t["of"] else 0), -t["seen"], t["label"]))
    return titles


def beginner_groups(submissions):
    """One record per beginner respondent, bucketed by films seen and by risks known."""
    risk_answers = {id(s): len(ticked) for _, ticked, s in beginner_answers(submissions, "beginner-catastrophes")}
    out = []
    for _, ticked, s in beginner_answers(submissions, "beginner-entertainment"):
        n = len(ticked)
        k = risk_answers.get(id(s), 0)
        summary = s["summary"]
        out.append({
            "films": n,
            "risks": k,
            "m": round(summary["midpoint"], 4),
            "p10": round(summary["p10"], 4),
            "p90": round(summary["p90"], 4),
            "spread": round(statistics.mean(f["spread"] for f in s["factors"]), 4),
            "g": "A" if n >= GROUP_A_MIN else ("B" if n >= GROUP_B_MIN else "C"),
            "rg": "A" if k >= RISK_A_MIN else ("B" if k >= RISK_B_MIN else "C"),
        })
    out.sort(key=lambda r: -r["films"])
    return out


def payload_key(s):
    """Everything a submission says, minus when it was said."""
    return json.dumps({"summary": s["summary"], "factors": s["factors"],
                       "quiz_flow_id": s.get("quiz_flow_id"),
                       "quiz_answers": s.get("quiz_answers")}, sort_keys=True)


def duplicate_audit(submissions):
    """The export has no visitor id, so identical payloads cannot be shown to be
    distinct people. Counting them lets the report state n honestly."""
    by_level = {}
    for lvl in QUIZ_LEVELS:
        rows = [s for s in submissions if s.get("quiz_flow_id") == lvl]
        seen, uniq = set(), []
        for s in rows:
            k = payload_key(s)
            if k not in seen:
                seen.add(k)
                uniq.append(s)
        by_level[lvl] = {
            "records": len(rows),
            "unique": len(uniq),
            # A duplicate sitting at the median position can move it, so both are published.
            "median": round(statistics.median([s["summary"]["midpoint"] for s in rows]), 4),
            "medianDedup": round(statistics.median([s["summary"]["midpoint"] for s in uniq]), 4),
        }
    return {"records": len(submissions),
            "unique": len({payload_key(s) for s in submissions}),
            "byLevel": by_level}


def _public_key_from_visitor_key(visitor_key):
    """Rebuild the P-256 public key from "p256:" + base64url(x || y)."""
    if not isinstance(visitor_key, str) or not visitor_key.startswith("p256:"):
        return None
    body = visitor_key[5:]
    try:
        raw = base64.urlsafe_b64decode(body + "=" * (-len(body) % 4))
    except (ValueError, TypeError):
        return None
    if len(raw) != 64:
        return None
    numbers = ec.EllipticCurvePublicNumbers(
        int.from_bytes(raw[:32], "big"), int.from_bytes(raw[32:], "big"), ec.SECP256R1())
    try:
        return numbers.public_key()
    except ValueError:
        return None  # not a point on the curve


def _signed_fields(signed_payload):
    """Parse the canonical string into its key=value fields."""
    parts = signed_payload.split("|")
    if not parts or parts[0] != "pdoom/1":
        return None
    fields = {}
    for part in parts[1:]:
        key, _, value = part.partition("=")
        fields[key] = value
    return fields


def _agrees_with_row(fields, s, tol=1e-6):
    """The signature covers the canonical string, not the jsonb. Check the two
    tell the same story, so a row edited after signing is caught."""
    def close(a, b):
        try:
            return abs(float(a) - float(b)) <= tol
        except (TypeError, ValueError):
            return False

    summary = s.get("summary") or {}
    for field, key in (("m", "midpoint"), ("lo", "lower"), ("hi", "upper"),
                       ("p10", "p10"), ("p90", "p90")):
        if not close(fields.get(field), summary.get(key)):
            return False
    factors = s.get("factors") or []
    pairs = [p for p in (fields.get("f") or "").split(",") if p]
    if len(pairs) != len(factors):
        return False
    for pair, factor in zip(pairs, factors):
        mid, _, spread = pair.partition(":")
        if not close(mid, factor.get("midpoint")) or not close(spread, factor.get("spread")):
            return False
    return (fields.get("k") == (s.get("visitor_key") or "")
            and fields.get("n") == str(s.get("submit_count")))


def verify_submissions(submissions):
    """Check every signature against the public key the row itself carries.

    A visitor's browser holds a non-extractable P-256 private key and signs the
    canonical string stored in ``signed_payload``. Anyone with the export can
    repeat this check, which is the point: the "these rows are one person"
    grouping is verifiable rather than asserted.

    What it cannot show is that distinct keys mean distinct people -- keys are
    free to generate. Rows are annotated in place with ``_identity`` and invalid
    ones are flagged, never dropped; silently discarding data would be a worse
    failure than reporting a bad signature."""
    counts = Counter()
    mismatched = 0
    seen_pairs = Counter()
    per_visitor = Counter()
    for s in submissions:
        key, sig, payload = s.get("visitor_key"), s.get("signature"), s.get("signed_payload")
        if not (key and sig and payload):
            s["_identity"] = "unsigned"
            counts["unsigned"] += 1
            continue
        counts["signed"] += 1
        per_visitor[key] += 1
        seen_pairs[(key, s.get("submit_count"))] += 1
        if not HAVE_CRYPTO:
            s["_identity"] = "unchecked"
            counts["unchecked"] += 1
            continue
        verdict = "signed-invalid"
        public_key = _public_key_from_visitor_key(key)
        if public_key is not None:
            try:
                raw_sig = base64.urlsafe_b64decode(sig + "=" * (-len(sig) % 4))
            except (ValueError, TypeError):
                raw_sig = b""
            if len(raw_sig) == 64:
                der = encode_dss_signature(int.from_bytes(raw_sig[:32], "big"),
                                           int.from_bytes(raw_sig[32:], "big"))
                try:
                    public_key.verify(der, payload.encode("utf-8"), ec.ECDSA(hashes.SHA256()))
                    verdict = "signed-valid"
                except InvalidSignature:
                    verdict = "signed-invalid"
        if verdict == "signed-valid":
            fields = _signed_fields(payload)
            if fields is None or not _agrees_with_row(fields, s):
                mismatched += 1
        s["_identity"] = verdict
        counts[verdict] += 1
    return {
        "signed": counts["signed"],
        "valid": counts["signed-valid"],
        "invalid": counts["signed-invalid"],
        "unchecked": counts["unchecked"],
        "unsigned": counts["unsigned"],
        "visitors": len(per_visitor),
        "repeat": sum(1 for n in per_visitor.values() if n > 1),
        "maxPerVisitor": max(per_visitor.values(), default=0),
        # A visitor's counter is monotonic, so a repeated (key, count) pair means
        # the same submission reached the table twice.
        "replays": sum(n - 1 for n in seen_pairs.values() if n > 1),
        "mismatched": mismatched,
    }


def flow_counts(submissions):
    """How post-launch visitors answered the level chooser."""
    post = [s for s in submissions if s["submitted_at"][:10] >= QUIZ_LAUNCH]
    seen = Counter(s.get("quiz_flow_id") or "none" for s in post)
    return [{"id": fid, "label": label, "n": seen.get(fid, 0)} for fid, label in FLOW_LABELS]


def parse_question_options(index_html, question_id):
    """Options for one question, matched by walking its own options array."""
    with open(index_html) as f:
        html = f.read()
    start = html.index(f"id: '{question_id}'")
    open_at = html.index("options: [", start)
    depth, i = 0, open_at + len("options: [") - 1
    while True:
        if html[i] == "[":
            depth += 1
        elif html[i] == "]":
            depth -= 1
            if depth == 0:
                break
        i += 1
    found = re.findall(r"\{\s*id:\s*'([^']+)',\s*label:\s*'((?:[^'\\]|\\.)*)'", html[open_at:i])
    return [(oid, label.replace("\\'", "'")) for oid, label in found]


def expert_breakdown(submissions, index_html):
    """Per-question tick rates for expert-quiz takers, plus each taker's name recall."""
    experts = [s for s in submissions if s.get("quiz_flow_id") == "expert"]
    questions, name_ids = [], []
    for qid, label, kind in EXPERT_QUESTIONS:
        options = parse_question_options(index_html, qid)
        if kind == "names":
            name_ids.append(qid)
        ticked = [len(a.get("values") or [])
                  for s in experts for a in s.get("quiz_answers") or []
                  if a["question_id"] == qid]
        if not ticked:
            continue
        questions.append({
            "id": qid,
            "label": label,
            "kind": kind,
            "opts": len(options),
            "median": statistics.median(ticked),
            "none": sum(1 for t in ticked if t == 0),
        })
    name_total = sum(q["opts"] for q in questions if q["kind"] == "names")
    people = []
    for s in experts:
        recalled = sum(len(a.get("values") or [])
                       for a in s.get("quiz_answers") or []
                       if a["question_id"] in name_ids)
        people.append({"names": recalled, "of": name_total,
                       "m": round(s["summary"]["midpoint"], 4)})
    people.sort(key=lambda r: -r["names"])
    return questions, people


def gate_picks(s):
    """Term ids ticked on the expert check, or None if this visitor never took it.

    Two shapes exist. Current rows carry ``gate_answers``, a flat list, and are
    produced by anyone who clicked the expert quiz. Rows from before 19 Aug 2026
    carry the selections inside ``quiz_answers`` under the retired ``decide`` flow.
    An empty set means "took the check and ticked nothing", which is not the same
    as never taking it -- hence None rather than an empty set for the latter."""
    if s.get("gate_answers") is not None:
        return set(s["gate_answers"])
    if s.get("quiz_flow_id") == "decide":
        return {v for a in s.get("quiz_answers") or [] for v in (a.get("values") or [])}
    return None


def gate_journeys(submissions):
    """What became of everyone who asked for the expert quiz.

    ``gate_score`` is non-null exactly when the visitor clicked Expert quiz, because
    the check cannot be reached any other way. What this cannot show is anyone who
    took the check and left without submitting -- they leave no row at all."""
    counts = Counter()
    rerouted_to = Counter()
    scores = []
    for s in submissions:
        if s.get("gate_score") is None:
            continue
        scores.append(s["gate_score"])
        taken = s.get("quiz_flow_id")
        if s.get("expert_verified"):
            counts["verified"] += 1
        elif taken == "expert":
            counts["overrode"] += 1
        else:
            counts["accepted"] += 1
            rerouted_to[taken or "none"] += 1
    attempted = sum(counts.values())
    return {
        "attempted": attempted,
        "verified": counts["verified"],
        "overrode": counts["overrode"],
        "accepted": counts["accepted"],
        "acceptedTo": dict(rerouted_to),
        "medianScore": round(statistics.median(scores), 1) if scores else None,
        "scores": sorted(scores),
    }


def knowledge_check(submissions, index_html):
    """The decoy instrument, and how the visitors who took it fared against it."""
    with open(index_html) as f:
        html = f.read()
    start = html.index("const knowledgeCheckQuestions")
    open_at = html.index("options: [", start)
    depth, i = 0, open_at + len("options: [") - 1
    while True:
        if html[i] == "[":
            depth += 1
        elif html[i] == "]":
            depth -= 1
            if depth == 0:
                break
        i += 1
    terms = []
    for chunk in re.split(r"\n\s{10}\{", html[open_at:i]):
        oid = re.search(r"id: '([^']+)'", chunk)
        text = re.search(r"""text: (?:'((?:[^'\\]|\\.)*)'|"((?:[^"\\]|\\.)*)")""", chunk)
        flag = re.search(r"aiRelated: (true|false)", chunk)
        if oid and flag:
            terms.append({
                "id": oid.group(1),
                "label": (((text.group(1) or text.group(2)).replace("\\'", "'"))
                          if text else oid.group(1)),
                "ai": flag.group(1) == "true",
            })
    real_ids = {t["id"] for t in terms if t["ai"]}
    decoys = [t for t in terms if not t["ai"]]
    pairs = [{"decoy": t["label"], "collides": DECOY_COLLISIONS.get(t["id"])} for t in decoys]
    pairs.sort(key=lambda p: (p["collides"] is None, p["collides"] or "", p["decoy"]))

    takers = []
    for s in submissions:
        picked = gate_picks(s)
        if picked is None:
            continue
        hits = len(picked & real_ids)
        tripped = len(picked - real_ids)
        avoided = len(decoys) - tripped
        correct = hits + avoided
        takers.append({
            "hits": hits, "tripped": tripped, "avoided": avoided,
            "correct": correct, "of": len(terms),
            "routed": ("beginner" if correct <= 20 else "medium" if correct <= 25 else "expert"),
            "calibrated": max(0, hits - tripped),
            "m": round(s["summary"]["midpoint"], 4),
            "p10": round(s["summary"]["p10"], 4),
            "p90": round(s["summary"]["p90"], 4),
        })
    # How each individual term fared, which the score alone cannot show.
    seen = Counter()
    for s in submissions:
        picked = gate_picks(s)
        if picked is None:
            continue
        for tid in picked:
            seen[tid] += 1
    per_term = [{
        "id": t["id"],
        "label": t["label"],
        "ai": t["ai"],
        # For a real term this is how many spotted it; for a decoy, how many fell for it.
        "picked": seen.get(t["id"], 0),
        "of": len(takers),
    } for t in terms]
    per_term.sort(key=lambda t: (t["ai"], -t["picked"]))

    return {
        "terms": len(terms),
        "real": len(real_ids),
        "decoys": len(decoys),
        "takers": takers,
        "pairs": pairs,
        "perTerm": per_term,
    }


def slider_submissions(submissions):
    """Post-launch submissions that bypassed the quiz entirely."""
    out = []
    for s in submissions:
        if s["submitted_at"][:10] < QUIZ_LAUNCH or s.get("quiz_flow_id"):
            continue
        out.append({
            "date": s["submitted_at"][:10],
            "m": round(s["summary"]["midpoint"], 4),
            "p10": round(s["summary"]["p10"], 4),
            "p90": round(s["summary"]["p90"], 4),
            "factors": [{"lower": f["lower"], "mid": f["midpoint"], "upper": f["upper"]}
                        for f in s["factors"]],
        })
    return out


def ranks(values):
    """Average ranks, so tied answers do not fabricate an ordering."""
    order = sorted(range(len(values)), key=lambda i: values[i])
    out = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        for k in range(i, j + 1):
            out[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return out


def spearman(xs, ys):
    return pearson(ranks(xs), ranks(ys))


def medium_breakdown(submissions, index_html):
    """Each medium question's rank correlation with p(doom), plus two questions in full."""
    meds = [s for s in submissions if s.get("quiz_flow_id") == "medium"]
    questions, prompts, vulns, vuln_list = [], [], [], []
    for qid, label, kind in MEDIUM_QUESTIONS:
        options = [oid for oid, _ in parse_question_options(index_html, qid)]
        xs, ys = [], []
        for s in meds:
            for a in s.get("quiz_answers") or []:
                if a["question_id"] != qid:
                    continue
                if a["type"] == "multi-select":
                    xs.append(len(a.get("values") or []))
                elif a.get("value") in options:
                    xs.append(options.index(a["value"]))  # display order is the ordinal scale
                else:
                    continue
                ys.append(s["summary"]["midpoint"])
        if len(xs) < 3:
            continue
        questions.append({"id": qid, "label": label, "kind": kind,
                          "rho": round(spearman(xs, ys), 3), "n": len(xs)})
        if qid == "medium-system-prompts":
            labels = [lab for _, lab in parse_question_options(index_html, qid)]
            for level, lab in enumerate(labels):
                vals = sorted(round(y, 4) for x, y in zip(xs, ys) if x == level)
                prompts.append({"label": lab, "n": len(vals),
                                "median": round(statistics.median(vals), 4) if vals else None,
                                "values": vals})
        if qid == "medium-vulnerabilities":
            of = len(options)
            vulns = [{"known": x, "of": of, "m": round(y, 4)} for x, y in zip(xs, ys)]
            picked = Counter(v for s in meds for a in s.get("quiz_answers") or []
                             if a["question_id"] == qid for v in (a.get("values") or []))
            for oid, lab in parse_question_options(index_html, qid):
                vuln_list.append({"label": lab, "known": picked.get(oid, 0),
                                  "of": len(meds), "ai": oid in AI_NATIVE_VULNS})
            vuln_list.sort(key=lambda v: (-v["known"], v["label"]))
    questions.sort(key=lambda q: -q["rho"])
    return questions, prompts, vulns, vuln_list


def pearson(xs, ys):
    mx, my = statistics.mean(xs), statistics.mean(ys)
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
    return cov / den if den else float("nan")


def print_summary(rows, out=sys.stderr):
    med = statistics.median
    group = lambda r: r["f"] if r["f"] in QUIZ_LEVELS else "untagged"

    print(f"submissions: {len(rows)}  ({rows[0]['t'][:10]} .. {rows[-1]['t'][:10]})", file=out)
    early = [r["m"] for r in rows if r["t"] < "2026-01"]
    late = [r["m"] for r in rows if r["t"] >= "2026-06"]
    print(f"median p(doom): first 3 months {med(early):.3f} (n={len(early)}), "
          f"last 3 months {med(late):.3f} (n={len(late)})", file=out)
    for g in QUIZ_LEVELS + ("untagged",):
        vals = [r["m"] for r in rows if group(r) == g]
        if vals:
            print(f"  {g:9s} n={len(vals):3d}  median={med(vals):.3f}", file=out)
    for i, key in enumerate(FACTOR_KEYS):
        r = pearson([r["fx"][i] for r in rows], [r["m"] for r in rows])
        print(f"  r({key} vs final) = {r:.2f}", file=out)


def print_film_summary(titles, beginners, out=sys.stderr):
    med = statistics.median
    if not beginners:
        return
    print(f"film exposure: {len(beginners)} beginner respondents, "
          f"median {med([b['films'] for b in beginners]):.0f} of {len(titles)} titles ticked", file=out)
    never = [t["label"] for t in titles if t["seen"] == 0 and t["of"] > 0]
    if never:
        print(f"  never ticked: {', '.join(never)}", file=out)
    for g in ("A", "B", "C"):
        vals = [b for b in beginners if b["g"] == g]
        if vals:
            print(f"  group {g}: n={len(vals):2d}  films {min(b['films'] for b in vals)}-{max(b['films'] for b in vals)}"
                  f"  median p(doom)={med([b['m'] for b in vals]):.2f}"
                  f"  median range-width={med([b['spread'] for b in vals]):.2f}", file=out)
    r = pearson([b["films"] for b in beginners], [b["m"] for b in beginners])
    print(f"  r(films seen vs p(doom)) = {r:+.2f}", file=out)


def print_risk_summary(beginners, out=sys.stderr):
    med = statistics.median
    if not beginners:
        return
    print(f"risk awareness: median {med([b['risks'] for b in beginners]):.0f} of 12 recognised", file=out)
    for g in ("A", "B", "C"):
        vals = [b for b in beginners if b["rg"] == g]
        if vals:
            print(f"  group {g}: n={len(vals):2d}  risks {min(b['risks'] for b in vals)}-{max(b['risks'] for b in vals)}"
                  f"  median p(doom)={med([b['m'] for b in vals]):.2f}"
                  f"  median range-width={med([b['spread'] for b in vals]):.2f}"
                  f"  min p(doom)={min(b['m'] for b in vals):.2f}", file=out)
    ks = [b["risks"] for b in beginners]
    print(f"  r(risks known vs p(doom))      = {pearson(ks, [b['m'] for b in beginners]):+.2f}", file=out)
    print(f"  r(risks known vs range-width)  = {pearson(ks, [b['spread'] for b in beginners]):+.2f}", file=out)


def print_flow_summary(flows, expert_q, experts, out=sys.stderr):
    total = sum(f["n"] for f in flows)
    if not total:
        return
    print(f"level chooser ({QUIZ_LAUNCH} onward, {total} submissions):", file=out)
    for f in flows:
        print(f"  {f['label']:32s} {f['n']:>3}  {100 * f['n'] / total:>4.0f}%", file=out)
    if not experts:
        return
    med = statistics.median
    for kind, title in (("concept", "reasoning questions"), ("names", "name-recognition questions")):
        qs = [q for q in expert_q if q["kind"] == kind]
        if qs:
            share = med([q["median"] / q["opts"] for q in qs])
            print(f"  expert quiz, {title}: median {100 * share:.0f}% of options ticked", file=out)
    recalled = [e["names"] for e in experts]
    of = experts[0]["of"]
    print(f"  expert name recall: median {med(recalled):.0f} of {of}"
          f"; {sum(1 for r in recalled if r <= 2)} of {len(experts)} recalled 2 or fewer", file=out)


def print_medium_summary(medium_q, prompts, out=sys.stderr):
    if not medium_q:
        return
    print(f"medium quiz (n={medium_q[0]['n']}), rank correlation with p(doom):", file=out)
    for q in medium_q:
        print(f"  {q['rho']:+.2f}  {q['label']:30s} [{q['kind']}]", file=out)
    for p in prompts:
        shown = f"{p['median']:.2f}" if p["median"] is not None else "--"
        print(f"    system prompts: {p['label'][:38]:40s} n={p['n']:>2}  median={shown}", file=out)


def print_gate_summary(gate, out=sys.stderr):
    print("\n-- expert check --", file=out)
    if not gate["attempted"]:
        print("nobody has taken the check yet", file=out)
        return
    print(f"asked for the expert quiz {gate['attempted']}, "
          f"cleared the bar {gate['verified']}, "
          f"fell short and took expert anyway {gate['overrode']}, "
          f"fell short and accepted a lower level {gate['accepted']} {gate['acceptedTo']}", file=out)
    print(f"median score {gate['medianScore']} of 30", file=out)


def print_identity_summary(identity, out=sys.stderr):
    print("\n-- visitor identity --", file=out)
    if identity["signed"] and not HAVE_CRYPTO:
        print(f"WARNING: {identity['signed']} signed rows NOT verified -- "
              f"`cryptography` is not installed (see requirements.txt)", file=out)
    print(f"signed {identity['signed']} (valid {identity['valid']}, "
          f"invalid {identity['invalid']}, unchecked {identity['unchecked']}), "
          f"unsigned {identity['unsigned']}", file=out)
    print(f"distinct visitors {identity['visitors']}, "
          f"submitted more than once {identity['repeat']}, "
          f"most from one visitor {identity['maxPerVisitor']}", file=out)
    if identity["replays"]:
        print(f"replayed (key, count) pairs: {identity['replays']}", file=out)
    if identity["mismatched"]:
        print(f"signed rows whose numbers disagree with the signed string: "
              f"{identity['mismatched']}", file=out)


def inject(report_path, blob):
    with open(report_path) as f:
        html = f.read()
    new_html, count = re.subn(
        r"const DATA = \{.*?\};\n",
        lambda _: f"const DATA = {blob};\n",
        html, count=1, flags=re.S,
    )
    if count != 1:
        sys.exit(f"error: no `const DATA = {{...}};` statement found in {report_path}")
    with open(report_path, "w") as f:
        f.write(new_html)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("input", nargs="?", default="pdoom-submissions.json",
                    help="exported submissions JSON (default: %(default)s)")
    ap.add_argument("-o", "--output", help="write the data blob to this file instead of stdout")
    ap.add_argument("--inject", metavar="REPORT_HTML",
                    help="rewrite the `const DATA = ...;` statement inside the report page")
    ap.add_argument("--quiz-source", default="index.html", metavar="INDEX_HTML",
                    help="page holding the quiz option labels (default: %(default)s)")
    ap.add_argument("-q", "--quiet", action="store_true", help="skip the stderr summary")
    args = ap.parse_args()

    with open(args.input) as f:
        submissions = json.load(f)["submissions"]
    rows = load_rows(submissions)
    titles = option_counts(
        submissions,
        parse_options(args.quiz_source, "beginner-entertainment", "beginner-catastrophes"),
        "beginner-entertainment")
    risks = option_counts(
        submissions,
        parse_options(args.quiz_source, "beginner-catastrophes", "beginner-capability"),
        "beginner-catastrophes")
    beginners = beginner_groups(submissions)
    expert_q, experts = expert_breakdown(submissions, args.quiz_source)
    medium_q, prompts, vulns, vuln_list = medium_breakdown(submissions, args.quiz_source)
    identity = verify_submissions(submissions)
    gate = gate_journeys(submissions)
    data = {
        "rows": rows,
        "months": monthly_aggregates(rows),
        "titles": titles,
        "risks": risks,
        "beginners": beginners,
        "flows": flow_counts(submissions),
        "knowledge": knowledge_check(submissions, args.quiz_source),
        "mediumQ": medium_q,
        "prompts": prompts,
        "mediumVuln": vulns,
        "vulnList": vuln_list,
        "sliders": slider_submissions(submissions),
        "dupes": duplicate_audit(submissions),
        "identity": identity,
        "gate": gate,
        "expertQ": expert_q,
        "experts": experts,
    }
    blob = json.dumps(data, separators=(",", ":"))

    if not args.quiet:
        print_summary(rows)
        print_film_summary(titles, beginners)
        print_risk_summary(beginners)
        print_flow_summary(data["flows"], expert_q, experts)
        print_medium_summary(medium_q, prompts)
        print_gate_summary(gate)
        print_identity_summary(identity)
    if args.inject:
        inject(args.inject, blob)
        print(f"injected {len(blob) // 1024} KB into {args.inject}", file=sys.stderr)
    elif args.output:
        with open(args.output, "w") as f:
            f.write(blob)
    else:
        print(blob)


if __name__ == "__main__":
    main()
