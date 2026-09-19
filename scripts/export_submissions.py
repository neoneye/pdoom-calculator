#!/usr/bin/env python3
"""Export the submissions table to pdoom-submissions.json from the command line.

Produces the same file the stats page's "Export" button downloads: the same
columns, the same summary block, the same row shape (optional columns written
only when set). The Supabase URL and anon key are read from _data/supabase.yml,
the same source the stats page uses. Usage:

    python3 scripts/export_submissions.py            # writes pdoom-submissions.json
    python3 scripts/export_submissions.py -o out.json
"""
import argparse
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_ROWS = 500  # same cap as the stats page
SELECT = ("submitted_at,summary,factors,quiz_flow_id,quiz_answers,"
          "gate_score,gate_recommended_level,expert_verified,gate_answers,"
          "visitor_key,submit_count,signed_payload,signature,page_version,calibration")
# Written only when set, in this order, so old rows stay as compact as they were
# and a missing key means "never recorded", not "recorded null".
OPTIONAL = ["quiz_flow_id", "quiz_answers", "gate_score", "gate_recommended_level",
            "expert_verified", "gate_answers", "visitor_key", "submit_count",
            "signed_payload", "signature", "page_version", "calibration"]


def read_config():
    text = (ROOT / "_data" / "supabase.yml").read_text()
    url = re.search(r'^url:\s*"([^"]+)"', text, re.M)
    key = re.search(r'^anon_key:\s*"([^"]+)"', text, re.M)
    if not url or not key:
        sys.exit("error: _data/supabase.yml must hold url and anon_key")
    return url.group(1), key.group(1)


def fetch(url, key):
    req = urllib.request.Request(
        f"{url}/rest/v1/submissions?select={SELECT}&order=submitted_at.asc&limit={MAX_ROWS}",
        headers={"apikey": key, "Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def average(values):
    return sum(values) / len(values) if values else None


def summary(rows):
    midpoints = [r["summary"]["midpoint"] for r in rows
                 if isinstance(r.get("summary"), dict) and isinstance(r["summary"].get("midpoint"), (int, float))]
    factors = {}
    for r in rows:
        for f in (r.get("factors") or []):
            b = factors.setdefault(f["key"], {"label": f.get("label") or f["key"], "lower": [], "upper": [], "midpoint": []})
            for k in ("lower", "upper", "midpoint"):
                if isinstance(f.get(k), (int, float)):
                    b[k].append(f[k])
    return {
        "total_submissions": len(rows),
        "average_pdoom": average(midpoints),
        "factors": [{"label": b["label"], "average_lower": average(b["lower"]),
                     "average_midpoint": average(b["midpoint"]), "average_upper": average(b["upper"])}
                    for b in factors.values()],
    }


def main():
    ap = argparse.ArgumentParser(description="Export the submissions table to pdoom-submissions.json.")
    ap.add_argument("-o", "--output", default=str(ROOT / "pdoom-submissions.json"))
    args = ap.parse_args()
    url, key = read_config()
    rows = fetch(url, key)
    rows.sort(key=lambda r: r.get("submitted_at") or "~")
    if len(rows) >= MAX_ROWS:
        print(f"warning: hit the {MAX_ROWS}-row cap; raise MAX_ROWS here and on the stats page", file=sys.stderr)
    out = {
        "source": "https://github.com/neoneye/pdoom-calculator",
        "exported_at": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
        "summary": summary(rows),
        "submissions": [
            {"submitted_at": r["submitted_at"], "summary": r["summary"], "factors": r["factors"],
             **{k: r[k] for k in OPTIONAL if r.get(k) is not None}}
            for r in rows],
    }
    Path(args.output).write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    with_cal = sum(1 for r in rows if isinstance(r.get("calibration"), dict))
    print(f"wrote {len(rows)} submissions to {args.output} ({with_cal} carry a calibration)", file=sys.stderr)


if __name__ == "__main__":
    main()
