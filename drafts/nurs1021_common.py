"""Shared helpers for NURS 1021 case studies (build_1021_unit<u>_*.py), November 2026.

Builds on unit6_common (Chart: tabs only grow; seeded random answer order). Adds tabs whose table grows
by rows, select-all questions whose rationale numbers options after shuffling ("{A}" -> "(Option 3)"),
drop-downs, and write_case() for NURS 1021 ids (case_17860<unit>000000<n>).
"""
import json, os, re
from unit6_common import Chart, table, note_rows, shuffle, matrix_mc, matrix_mr, rationale, lab, highlight_tab, HERE

UNITS = {1: "Unit 1 (Blood Disorders)", 2: "Unit 2 (Cardiovascular Disorders)", 3: "Unit 3 (Respiratory Disorders)",
         4: "Unit 4 (Inflammation and Immune Disorders)", 5: "Unit 5 (Leukemias and Lymphomas)",
         6: "Unit 6 (Gastrointestinal Disorders)", 7: "Unit 7 (Urinary Disorders)",
         8: "Unit 8 (Fluid, Electrolytes, and Acid-Base Imbalances)", 9: "Unit 9 (Reproductive Disorders)"}
IMC = ["Indicated", "Non-Essential", "Contraindicated"]
SPO2 = "Pulse Oximetry Reading (SpO<sub>2</sub>)"


class Chart2(Chart):
    """unit6_common.Chart plus tabs whose table grows by rows (orders, care plans)."""

    def rows(self, tid, title, headers, rows):
        t = self._tab(tid, title, "rows", headers)
        t["entries"].extend(rows)

    def snapshot(self):
        out = super().snapshot()
        for tab in out:
            t = self.tabs[tab["id"]]
            if t["kind"] == "rows":
                tab["content"] = table(t["header"], t["entries"])
        return out


def vrow(label, expected=None):
    return f"<b>{label}</b>" + (f"<br>{expected}" if expected else "")


def _numbered(explanation, num):
    def refs(m):
        ns = sorted(num[k] for k in m.group(1).split(","))
        if len(ns) == 1:
            return f"(Option {ns[0]})"
        return "(Options " + ", ".join(map(str, ns[:-1])) + f" and {ns[-1]})"
    return re.sub(r"\{([A-Z](?:,[A-Z])*)\}", refs, explanation)


def options_q(qtype, seed, items, explanation, **q):
    """items: (key, text, correct). Shuffles; "{A}" / "{A,C}" in the rationale become option numbers."""
    order = shuffle([{"key": k, "text": t, "correct": c} for k, t, c in items], seed)
    num = {o["key"]: i + 1 for i, o in enumerate(order)}
    q.update({"type": qtype, "options": [{"text": o["text"], "correct": o["correct"]} for o in order],
              "explanation": _numbered(explanation, num)})
    return q


def select_all(seed, items, explanation, **q):
    return options_q("select_all", seed, items, explanation, **q)


def multiple_choice(seed, items, explanation, **q):
    return options_q("multiple_choice", seed, items, explanation, **q)


def dd(seed, correct, *wrong):
    return {"placeholder": "Select...", "options": shuffle([{"text": correct, "correct": True}] +
                                                           [{"text": w, "correct": False} for w in wrong], seed)}


def bowtie_list(seed, correct, wrong):
    return shuffle([{"text": t, "correct": True} for t in correct] + [{"text": t, "correct": False} for t in wrong], seed)


def screen(step, intro, chart, question):
    question.setdefault("preamble", "")
    return {"step": step, "leftContent": {"intro": intro, "tabs": chart.snapshot()}, "question": question}


def write_case(unit, n, description, screens, review):
    case_id = f"case_17860{unit}{n:07d}"
    title = f"NURS 1021 Unit {unit} Case Study {n}"
    case = {"id": case_id, "title": title, "course": "NURS 1021", "unit": UNITS[unit], "topic": UNITS[unit],
            "disorder": UNITS[unit], "description": description,
            "authorReview": {"note": review, "flaggedAt": "2026-11-24"}, "screens": screens}
    out = os.path.join(HERE, f"{case_id}_{title.replace(' ', '_')}.json")
    with open(out, "w") as f:
        json.dump(case, f, indent=2, ensure_ascii=False)
    print("wrote", out)
    return out
