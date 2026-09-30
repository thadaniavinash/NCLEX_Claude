"""Builds drafts/restore_1021_u3c1_notes_patch.json: puts back the Nurses' Notes of NURS 1021 Unit 3
Case Study 1 (case_1786030000001) as they were in the backup of 29 Sep 2026 (commit a2c5868), before the
1000 entry and the "Emergency Department" line were deleted in the studio on 30 Sep (the deletion on
screen 1 was carried to every later screen). Only tab contents that differ are listed; everything else
in the case stays as it is now. Apply with the Supabase workflow's `patch` action.

Usage: python3 drafts/build_restore_1021_u3c1_notes.py
"""
import json
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import bank  # noqa: E402

CASE_ID = "case_1786030000001"
SOURCE = "a2c5868"


def main():
    old = json.loads(subprocess.check_output(
        ["git", "show", f"{SOURCE}:backup/items/cases/{CASE_ID}.json"], cwd=REPO))
    cases, _ = bank.load()
    now = next(c for c in cases if c["id"] == CASE_ID)
    entries = []
    for si, (s_old, s_now) in enumerate(zip(old["screens"], now["screens"])):
        tabs_old = {t["id"]: t for t in s_old["leftContent"]["tabs"]}
        for ti, tab in enumerate(s_now["leftContent"]["tabs"]):
            before = tabs_old.get(tab["id"])
            if before and before["content"] != tab["content"]:
                entries.append({"row": "cases", "id": CASE_ID,
                                "path": ["screens", si, "leftContent", "tabs", ti, "content"],
                                "before": tab["content"], "after": before["content"]})
                print(f"screen {si + 1} {tab['title']}: {len(tab['content'])} -> {len(before['content'])} characters")
    out = os.path.join(REPO, "drafts", "restore_1021_u3c1_notes_patch.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=1, ensure_ascii=False)
    print(f"{len(entries)} tab contents -> drafts/restore_1021_u3c1_notes_patch.json")


if __name__ == "__main__":
    main()
