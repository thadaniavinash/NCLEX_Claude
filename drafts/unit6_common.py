"""Shared helpers for the NURS 1017 Unit 6 case studies (build_unit6_case*.py), October 2026.

Chart: tabs that unfold over the six screens and are never subtracted (CLAUDE.md chart carry-forward):
notes tabs gain timed entries, tables gain columns. snapshot() returns the tabs as they stand.
Answer order: shuffle() puts options in a seeded random order (user decision 14 Oct 2026: random, no
pattern; correct answers may come first, but not all of them bunched at the top).
"""
import json, os, random, re

UNIT = "Unit 6 (Musculoskeletal Disorders)"
TH = 'style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;"'
TD = 'style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;"'
HERE = os.path.dirname(os.path.abspath(__file__))


def table(headers, rows):
    head = "".join(f"<th {TH}>{h}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td {TD}>{c}</td>" for c in r) + "</tr>" for r in rows)
    return (f'<table class="nclex-editor-table" style="width:100%; border-collapse:collapse; margin:12px 0;">'
            f"<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>")


def note_rows(entries):
    return "".join(f'<p class="nurse-note-row"><span class="nurse-note-time">{t}:</span>'
                   f'<span class="nurse-note-text">{x}</span></p>' for t, x in entries)


BRACE = re.compile(r"\{([^{|}]+)(?:\|correct)?\}")


def strip_marks(text):
    """Highlight markup {phrase|correct} / {phrase} -> plain phrase (for the chart copy)."""
    return BRACE.sub(r"\1", text)


class Chart:
    def __init__(self):
        self.order, self.tabs = [], {}

    def _tab(self, tid, title, kind, header=None):
        if tid not in self.tabs:
            self.order.append(tid)
            self.tabs[tid] = {"title": title, "kind": kind, "entries": [], "header": header, "cols": [], "rows": {}}
        return self.tabs[tid]

    def notes(self, tid, title, *entries):
        t = self._tab(tid, title, "notes")
        t["entries"].extend((label, strip_marks(text)) for label, text in entries)

    def column(self, tid, title, header, col, values):
        """Adds a reading column; values is a list of (row label, value)."""
        t = self._tab(tid, title, "table", header)
        t["cols"].append(col)
        for label, value in values:
            t["rows"].setdefault(label, {})[col] = value

    def vitals(self, col, values, tid="vs", title="Vital Signs"):
        self.column(tid, title, "", col, values)

    def labs(self, col, values, tid="labs", title="Laboratory Results"):
        self.column(tid, title, "Laboratory Test and Reference Range", col, values)

    def snapshot(self):
        out = []
        for tid in self.order:
            t = self.tabs[tid]
            if t["kind"] == "notes":
                content = note_rows(t["entries"])
            else:
                rows = [[label] + [vals.get(c, "") for c in t["cols"]] for label, vals in t["rows"].items()]
                content = table([t["header"]] + t["cols"], rows)
            out.append({"id": tid, "title": t["title"], "content": content})
        return out


VS = {"T": "<b>T</b>", "P": "<b>P</b>", "RR": "<b>RR</b>", "BP": "<b>BP</b>",
      "SpO2": "<b>Pulse Oximetry Reading (SpO<sub>2</sub>)</b>"}


def vs(t, p, rr, bp, spo2):
    return [(VS["T"], t), (VS["P"], p), (VS["RR"], rr), (VS["BP"], bp), (VS["SpO2"], spo2)]


def lab(name, rng):
    return f"<b>{name}</b><br>{rng}"


def shuffle(items, seed, correct=lambda o: o["correct"]):
    """Seeded random order; reshuffles while several correct items all sit at the top (or nothing moved)."""
    rng = random.Random(seed)
    items = list(items)
    n = sum(1 for o in items if correct(o))
    for _ in range(50):
        out = items[:]
        rng.shuffle(out)
        top = all(correct(o) for o in out[:n]) if 1 < n < len(out) else False  # one correct answer may come first
        if not top and out != items:
            return out
    return out


def opts(*pairs, seed):
    return shuffle([{"text": t, "correct": c} for t, c in pairs], seed)


def dropdown(*pairs, seed):
    return {"placeholder": "Select...", "options": opts(*pairs, seed=seed)}


def matrix_mc(header, columns, rows):
    return {"firstColumnHeader": header, "columns": columns,
            "rows": [{"text": t, "correctIndex": i, "correctIndices": [i]} for t, i in rows]}


def matrix_mr(header, columns, rows):
    return {"firstColumnHeader": header, "columns": columns,
            "rows": [{"text": t, "correctIndex": ix[0], "correctIndices": list(ix)} for t, ix in rows]}


def rationale(*items):
    return "<br><br>".join(items)


def highlight_tab(tid, title, entries):
    return {"id": tid, "title": title, "content": note_rows(entries)}


def screen(step, intro, chart, question):
    question.setdefault("preamble", "")
    return {"step": step, "leftContent": {"intro": intro, "tabs": chart.snapshot()}, "question": question}


def write_case(case_id, n, description, screens, review_lines):
    case = {
        "id": case_id,
        "title": f"NURS 1017 Unit 6 Case Study {n}",
        "course": "NURS 1017",
        "unit": UNIT,
        "topic": UNIT,
        "disorder": UNIT,
        "description": description,
        "authorReview": {
            "note": "New case written by Claude on 14 Oct 2026 to fill a Unit 6 gap; please review before using it with students:\n"
                    + "\n".join(review_lines),
            "flaggedAt": "2026-10-14",
        },
        "screens": screens,
    }
    out = os.path.join(HERE, f"{case_id}_NURS_1017_Unit_6_Case_Study_{n}.json")
    with open(out, "w") as f:
        json.dump(case, f, indent=2, ensure_ascii=False)
    print("wrote", out)
