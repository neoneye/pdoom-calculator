#!/usr/bin/env python3
"""Validate _data/exhibits.yml.

`limits` is required on every exhibit: an exhibit that does not say what it fails
to establish is an anecdote, not evidence. Run before committing content.
"""
import re
import sys

REQUIRED = ("id", "link", "title", "date", "what", "source", "limits")
LINKS = {"powerfulAi", "dangerousBehavior", "globalCatastrophe"}
# Optional. Marks an exhibit that still teaches something but no longer describes
# the current frontier, so it renders under a "historical context" subheading.
ERAS = {"historical"}


def parse(path):
    """Minimal reader for the flat list-of-maps shape this file uses, so the
    check has no dependency beyond the standard library. Folded scalars (`>`)
    continue until the next key at the same indent."""
    entries, cur, key, folding = [], None, None, False
    for raw in open(path):
        line = raw.rstrip("\n")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("- "):
            if cur:
                entries.append(cur)
            cur, key, folding = {}, None, False
            line = "  " + line[2:]
        m = re.match(r"^  (\w+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if val in (">", "|", ">-", "|-"):
                cur[key], folding = "", True
            else:
                cur[key] = val if val else {}
                folding = False
            continue
        m = re.match(r"^    (\w+):\s*(.*)$", line)
        if m and isinstance(cur.get(key), dict):
            cur[key][m.group(1)] = m.group(2).strip()
            continue
        if folding and key and line.startswith("    "):
            cur[key] = (cur[key] + " " + line.strip()).strip()
    if cur:
        entries.append(cur)
    return entries


def main():
    entries = parse("_data/exhibits.yml")
    errors = []
    seen = set()
    for i, e in enumerate(entries):
        where = e.get("id") or f"entry {i + 1}"
        for field in REQUIRED:
            if not e.get(field):
                errors.append(f"{where}: missing {field}")
        if e.get("link") and e["link"] not in LINKS:
            errors.append(f"{where}: link '{e['link']}' is not one of {sorted(LINKS)}")
        if e.get("id") in seen:
            errors.append(f"{where}: duplicate id")
        seen.add(e.get("id"))
        if e.get("era") and e["era"] not in ERAS:
            errors.append(f"{where}: era '{e['era']}' is not one of {sorted(ERAS)}")
        for field in ("source", "source2", "source3"):
            src = e.get(field)
            if src is None or src == "":
                continue
            if isinstance(src, dict):
                if not str(src.get("url", "")).startswith("http"):
                    errors.append(f"{where}: {field}.url must be an absolute URL")
                if not src.get("label"):
                    errors.append(f"{where}: {field}.label missing")
            else:
                errors.append(f"{where}: {field} must have label and url")

    print(f"{len(entries)} exhibits, {len(errors)} problems")
    for err in errors:
        print("  " + err)
    by_link = {l: sum(1 for e in entries if e.get("link") == l) for l in sorted(LINKS)}
    print("by link:", by_link)
    print("historical:", sum(1 for e in entries if e.get("era") == "historical"))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
