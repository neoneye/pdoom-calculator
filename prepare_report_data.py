#!/usr/bin/env python3
"""Prepare chart data for the p(doom) submissions report.

Reads the exported ``pdoom-submissions.json`` and emits the compact JSON blob
the report page (``pdoom-submissions-viz.html``) renders from:

    {
      "rows":      [{"t", "m", "p10", "p90", "f", "fx": [pAI, pDB, pGC]}, ...],
      "months":    [{"month", "n", "median", "p25", "p75"}, ...],
      "titles":    [{"id", "label", "seen", "of"}, ...],
      "risks":     [{"id", "label", "seen", "of"}, ...],
      "flows":     [{"id", "label", "n"}, ...],
      "expertQ":   [{"id", "label", "kind", "opts", "median", "none"}, ...],
      "experts":   [{"names", "m"}, ...],
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
    python3 prepare_report_data.py --inject report.html # rewrite `const DATA = ...;`

A summary (group/era medians, factor correlations) is printed to stderr so the
headline numbers quoted in the report can be re-checked after a data refresh.
"""

import argparse
import json
import math
import re
import statistics
import sys
from collections import Counter

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
    data = {
        "rows": rows,
        "months": monthly_aggregates(rows),
        "titles": titles,
        "risks": risks,
        "beginners": beginners,
        "flows": flow_counts(submissions),
        "expertQ": expert_q,
        "experts": experts,
    }
    blob = json.dumps(data, separators=(",", ":"))

    if not args.quiet:
        print_summary(rows)
        print_film_summary(titles, beginners)
        print_risk_summary(beginners)
        print_flow_summary(data["flows"], expert_q, experts)
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
