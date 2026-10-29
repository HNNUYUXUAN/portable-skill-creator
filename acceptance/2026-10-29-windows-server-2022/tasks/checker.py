"""Acceptor-side checker: compares recipient Markdown output with the raw input."""
import json
import re
import sys
from pathlib import Path

GROUPS = ["TODO", "DONE", "BLOCKED", "UNMARKED"]
MARKERS = {"TODO:": "TODO", "DONE:": "DONE", "BLOCKED:": "BLOCKED"}


def expected(lines):
    exp = {g: [] for g in GROUPS}
    for raw in lines:
        line = raw.rstrip("\r\n")
        if not line.strip():
            continue
        group = "UNMARKED"
        for marker, name in MARKERS.items():
            if line.startswith(marker):
                group = name
                break
        exp[group].append(line)
    return exp


def parse(md):
    got, order, counts = {g: [] for g in GROUPS}, [], {}
    current = None
    for line in md.splitlines():
        m = re.match(r"^##\s+(TODO|DONE|BLOCKED|UNMARKED)\s*\((\d+)\)\s*$", line.strip())
        if m:
            current = m.group(1)
            counts[current] = int(m.group(2))
            if current in order:
                raise ValueError("duplicate heading " + current)
            order.append(current)
            continue
        if line.startswith("## "):
            raise ValueError("unexpected heading: " + line)
        if current and line.strip().startswith("- "):
            body = line.strip()[2:]
            if body.strip() not in ("（无条目）", "(none)"):
                got[current].append(body)
    return got, order, counts


def check(input_path, result_path):
    lines = Path(input_path).read_text(encoding="utf-8").splitlines(True)
    exp = expected(lines)
    md = Path(result_path).read_text(encoding="utf-8")
    got, order, counts = parse(md)
    report = {"result": str(result_path), "checks": {}, "ok": True}

    report["checks"]["heading_order"] = order == GROUPS
    if order != GROUPS:
        report["ok"] = False

    for g in GROUPS:
        same = got[g] == exp[g]
        cnt_ok = counts.get(g) == len(got[g])
        report["checks"]["group_" + g] = {
            "order_and_text_match": same,
            "declared_count": counts.get(g),
            "actual_items": len(got[g]),
            "count_ok": cnt_ok,
            "diff": [] if same else {"expected": exp[g], "actual": got[g]},
        }
        if not same or not cnt_ok:
            report["ok"] = False

    total_items = sum(len(v) for v in got.values())
    nonempty = sum(1 for l in lines if l.strip())
    report["checks"]["total_items_equals_nonempty_lines"] = {
        "items": total_items,
        "nonempty_lines": nonempty,
        "ok": total_items == nonempty,
    }
    if total_items != nonempty:
        report["ok"] = False
    return report


if __name__ == "__main__":
    out = check(sys.argv[1], sys.argv[2])
    print(json.dumps(out, ensure_ascii=False, indent=2))
    sys.exit(0 if out["ok"] else 1)
