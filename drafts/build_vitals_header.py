"""Builds drafts/vitals_header_patch.json: empties the first header cell of every table in chart tabs
whose title starts with "Vital Signs" (the tab name already says what the rows are; the user asked for
the cell to stay empty, as in the ready-made Vital signs table). Only that cell's text changes; its
markup and styles are kept. Apply with the Supabase workflow's `patch` action.

Usage: python3 drafts/build_vitals_header.py
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools"))
import bank  # noqa: E402

TITLE = re.compile(r"\s*vital signs", re.I)
TABLE = re.compile(r"<table[\s\S]*?</table>")
FIRST_CELL = re.compile(r"(<tr[^>]*>\s*<th[^>]*>)([\s\S]*?)(</th>)")


def clear_first_headers(html):
    def fix_table(m):
        table = m.group(0)
        cell = FIRST_CELL.search(table)
        if not cell or not re.sub(r"<[^>]+>|&nbsp;|\s", "", cell.group(2)) or "{" in cell.group(2):
            return table
        return table[:cell.start(2)] + table[cell.end(2):]
    return TABLE.sub(fix_table, html)


def main():
    cases, standalone = bank.load()
    entries, cleared = [], {}
    for row, items in (("cases", cases), ("standalone", standalone)):
        for item in items:
            for si, screen in enumerate(item.get("screens", [])):
                for ti, tab in enumerate(screen.get("leftContent", {}).get("tabs", []) or []):
                    if not TITLE.match(tab.get("title", "")):
                        continue
                    new = clear_first_headers(tab["content"])
                    if new != tab["content"]:
                        for label in FIRST_CELL.findall(tab["content"]):
                            text = re.sub(r"<[^>]+>", "", label[1]).strip()
                            if text:
                                cleared[text] = cleared.get(text, 0) + 1
                        entries.append({"row": row, "id": item["id"],
                                        "path": ["screens", si, "leftContent", "tabs", ti, "content"],
                                        "before": tab["content"], "after": new})
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vitals_header_patch.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=1, ensure_ascii=False)
    items = len({e["id"] for e in entries})
    print(f"{len(entries)} tab contents in {items} items -> drafts/vitals_header_patch.json")
    print("Header labels removed:", cleared)


if __name__ == "__main__":
    main()
