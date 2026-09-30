"""Shared helpers for the University of Maryland faculty case study conversions (drafts/build_umd_cs*.py).

Source: Maryland Next Gen NCLEX Test Bank Project, University of Maryland School of Nursing,
https://www.nursing.umaryland.edu/mnwc/initiatives/nextgen-nclex/nextgen-nclex-library/ (Faculty case studies,
Medical-Surgical). Each generator builds one case study ("University of Maryland - CSn") and, when the Word file
has a stand-alone trend or bow-tie that is not a copy of a case screen, that stand-alone question too. Items are
written to drafts/ with draft: true (hidden from students until the author reviews them in the studio), and
each generator records its points for the author's review in drafts/umd_review/<CSn>.json, which
drafts/build_umd_review_pdf.js turns into the to-do PDF.

Conventions (see CLAUDE.md): option, matrix-row and drop-down labels are plain text (write “ ” ₂ × ⁹ ≥ as
characters, never HTML); rationales use <br>; lab values in SI units with the author's reference ranges
converted; each screen's question.footnote carries the acknowledgment.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE_URL = "https://www.nursing.umaryland.edu/mnwc/initiatives/nextgen-nclex/nextgen-nclex-library/"
TH = 'border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;'
TD = 'border:1px solid #ccd8e0; padding:8px; min-width:80px; background:white; color:#1e293b;'
STEPS = ["Recognize cues", "Analyze cues", "Prioritize hypotheses", "Generate solutions", "Take action",
         "Evaluate outcomes"]


def case_id(n):
    return f"case_17907768000{n:02d}"


def standalone_id(n, k=0):
    return f"standalone_1790776801{n:02d}{k}"


def footnote(topic, author, date="September 1, 2022", kind="medical-surgical faculty case study", si=True):
    return ("Taken from the Maryland Next Gen NCLEX Test Bank Project, University of Maryland School of Nursing: "
            f"&ldquo;{topic}&rdquo; {kind} ({author}, {date}). Available at {SOURCE_URL} (Faculty Case Studies)."
            + (" Laboratory values shown in SI units." if si else ""))


# ---- Chart content ----
def note(time, text):
    return (f'<p class="nurse-note-row"><span class="nurse-note-time">{time}:</span>'
            f'<span class="nurse-note-text">{text}</span></p>')


def title(text):
    """A bold title line above the entry or table that follows (the editor's T+)."""
    return f"<p><b>{text}</b></p>"


def paras(*lines):
    return "".join(f"<p>{x}</p>" for x in lines)


def table(header, rows):
    """header=None: no header row (e.g. History and Physical: system | findings)."""
    head = "".join(f'<th style="{TH}">{h}</th>' for h in header) if header else ""
    body = "".join("<tr>" + "".join(f'<td style="{TD}">{c}</td>' for c in r) + "</tr>" for r in rows)
    return (f'<table class="nclex-editor-table" style="width:100%; border-collapse:collapse; margin:12px 0;">'
            + (f"<thead><tr>{head}</tr></thead>" if head else "") + f"<tbody>{body}</tbody></table>")


def lab(name, rng):
    return f"<b>{name}</b><br>{rng}" if rng else f"<b>{name}</b>"


def vitals(times, rows):
    """Vital signs table: first header cell empty (user decision), one column per time."""
    return table([""] + list(times), [[f"<b>{r[0]}</b>"] + list(r[1:]) for r in rows])


G9 = " &times; 10<sup>9</sup>/L"
G12 = " &times; 10<sup>12</sup>/L"


# ---- Questions ----
def opts(*pairs):
    return [{"text": t, "correct": bool(c)} for t, c in pairs]


def matrix(first, columns, rows):
    return {"firstColumnHeader": first, "columns": columns,
            "rows": [{"text": t, "correctIndex": i, "correctIndices": [i]} for t, i in rows]}


def matrix_mr(first, columns, rows):
    return {"firstColumnHeader": first, "columns": columns,
            "rows": [{"text": t, "correctIndex": (ix[0] if ix else 0), "correctIndices": list(ix)} for t, ix in rows]}


def cloze(text, *dropdowns):
    return {"text": text, "dropdowns": [{"placeholder": "Select...", "options": opts(*d)} for d in dropdowns]}


def bowtie(actions, conditions, params):
    return {
        "bowtieActions": opts(*actions), "bowtieConditions": opts(*conditions), "bowtieParams": opts(*params),
        "bowtieCol1Header": "Actions to Take", "bowtieCol2Header": "Potential Conditions",
        "bowtieCol3Header": "Parameters to Monitor", "bowtieLeftPlaceholder": "Action to Take",
        "bowtieCenterPlaceholder": "Condition Most Likely Experiencing", "bowtieRightPlaceholder": "Parameter to Monitor",
    }


# ---- Items ----
def make_case(n, name, description, screens, fn):
    """screens: list of (intro, tabs, question); question gets the footnote. Returns the case dict."""
    out = []
    for i, (intro, tabs, q) in enumerate(screens, 1):
        q.setdefault("preamble", "")
        q["footnote"] = fn
        out.append({"step": i, "leftContent": {"intro": intro, "tabs": tabs}, "question": q})
    return {"id": case_id(n), "title": f"University of Maryland - CS{n}", "course": "Others", "unit": "Others",
            "topic": "Others", "disorder": "Others", "description": description, "availability": "all",
            # Hidden from students until the author has reviewed it (studio: Ready chip -> "Show to students").
            "draft": True, "screens": out}


def make_standalone(n, k, suffix, description, intro, tabs, q, fn):
    q.setdefault("preamble", "")
    q["footnote"] = fn
    return {"id": standalone_id(n, k), "title": f"University of Maryland - CS{n} {suffix}", "course": "Others",
            "unit": "Others", "topic": "Others", "disorder": "Others", "description": description,
            "isStandalone": True, "availability": "all", "draft": True,
            "screens": [{"step": 1, "leftContent": {"intro": intro, "tabs": tabs}, "question": q}]}


def write(items, n, topic, source_file, notes):
    """Writes each item to drafts/<id>_<title>.json and the review notes to drafts/umd_review/CS<n>.json."""
    files = []
    for it in items:
        name = f"{it['id']}_{it['title'].replace(' ', '_')}.json"
        with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
            json.dump(it, f, indent=2, ensure_ascii=False)
        files.append("drafts/" + name)
    os.makedirs(os.path.join(HERE, "umd_review"), exist_ok=True)
    with open(os.path.join(HERE, "umd_review", f"CS{n:02d}.json"), "w", encoding="utf-8") as f:
        json.dump({"cs": n, "topic": topic, "source": source_file, "items": [
            {"id": it["id"], "title": it["title"], "file": fl} for it, fl in zip(items, files)], "notes": notes},
            f, indent=2, ensure_ascii=False)
    for fl in files:
        print("wrote", fl)
    return files
