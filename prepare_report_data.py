#!/usr/bin/env python3
"""Prepare chart data for the p(doom) submissions report.

Reads the exported ``pdoom-submissions.json`` and emits the compact JSON blob
the report page (``pdoom-submissions-viz.html``) renders from:

    {
      "rows":   [{"t", "m", "p10", "p90", "f", "fx": [pAI, pDB, pGC]}, ...],
      "months": [{"month", "n", "median", "p25", "p75"}, ...]
    }

``rows`` is one entry per submission, sorted by timestamp; ``fx`` holds the
midpoints of the three chain factors. ``months`` aggregates the final p(doom)
midpoint per calendar month (UTC).

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

FACTOR_KEYS = ("powerfulAi", "dangerousBehavior", "globalCatastrophe")
QUIZ_LEVELS = ("beginner", "medium", "expert")


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
    ap.add_argument("-q", "--quiet", action="store_true", help="skip the stderr summary")
    args = ap.parse_args()

    with open(args.input) as f:
        rows = load_rows(json.load(f)["submissions"])
    data = {"rows": rows, "months": monthly_aggregates(rows)}
    blob = json.dumps(data, separators=(",", ":"))

    if not args.quiet:
        print_summary(rows)
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
