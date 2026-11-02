"""Shared helpers for the NURS 1017 Unit 7 (neurological) case studies 2-6 (build_unit7_case<n>_*.py), November 2026.

Reuses drafts/unit6_common.py (Chart: tabs only grow; seeded random answer order; table/notes markup) and adds
free-text tabs (History and Physical) plus a writer for Unit 7 items.
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unit6_common import (Chart, vs, lab, opts, dropdown, matrix_mc, matrix_mr, rationale, highlight_tab,  # noqa: F401,E402
                          screen, strip_marks, note_rows, HERE)

UNIT = "Unit 7 (Neurological Disorders)"


class NeuroChart(Chart):
    """Chart with optional fixed free-text tabs (kind "html")."""

    def html(self, tid, title, content):
        t = self._tab(tid, title, "html")
        t["content"] = content

    def snapshot(self):
        html = {t: self.tabs[t] for t in self.order if self.tabs[t]["kind"] == "html"}
        for t in html:
            self.tabs[t] = dict(html[t], kind="notes", entries=[])
        try:
            out = super().snapshot()
        finally:
            for t, tab in html.items():
                self.tabs[t] = tab
        for o in out:
            if o["id"] in html:
                o["content"] = html[o["id"]]["content"]
        return out


def kv_html(entries, marked=False):
    """History and Physical paragraphs: [(label, text)]; marked=True keeps {highlight} markup."""
    return "".join(f"<p><b>{k}:</b> {v if marked else strip_marks(v)}</p>" for k, v in entries)


def ordered(*steps):
    return list(steps)


def write_case(n, description, screens, review_lines, slug):
    case_id = f"case_178241000000{n}"
    case = {
        "id": case_id,
        "title": f"NURS 1017 Unit 7 Case Study {n}",
        "course": "NURS 1017",
        "unit": UNIT,
        "topic": UNIT,
        "disorder": UNIT,
        "description": description,
        "authorReview": {
            "note": "New case written by Claude on 2 Nov 2026 for the Unit 7 learning outcomes; please review before using it with "
                    "students:\n" + "\n".join(review_lines),
            "flaggedAt": "2026-11-02",
        },
        "screens": screens,
    }
    out = os.path.join(HERE, f"{case_id}_NURS_1017_Unit_7_Case_Study_{n}_{slug}.json")
    with open(out, "w") as f:
        json.dump(case, f, indent=2, ensure_ascii=False)
    print("wrote", out)
    return case
