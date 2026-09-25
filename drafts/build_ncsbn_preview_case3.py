"""Builds NURS 1021 Unit 3 Case Study 2 (pneumonia vs. UTI vs. influenza, with atrial
fibrillation history) from the NCSBN NCLEX-RN Next Generation Exam Preview PDF (c 2022
NCSBN), fourth attachment (Test4.pdf, items 65-70, screens 1-6).

The source reveals the answer for 2 of the 6 screens (screen 3's dropdown, "dysrhythmias",
and screen 5's highlight, the sepsis-bundle orders); both are confirmed against the source
and built exactly as shown. The other 4 screens (1, 2, 4, 6) are this session's own clinical
judgment and need clinician review before publish, same as every other item in this project.
"""
import json
import os

DRAFTS_DIR = os.path.dirname(os.path.abspath(__file__))

FOOTNOTE = (
    "&copy; NCSBN. Taken from https://www.nclex.com/prepare.page; "
    "click on &#39;Download Exam Preview&#39;."
)

INTRO = "The nurse in the emergency department (ED) is caring for a 78-year-old female client."

TH = 'style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;"'
TD = 'style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;"'


def table(headers, rows):
    head = "".join(f"<th {TH}>{h}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td {TD}>{c}</td>" for c in r) + "</tr>" for r in rows)
    return (f'<table class="nclex-editor-table" style="width:100%; border-collapse:collapse; margin:12px 0;">'
            f"<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>")


def note_row(time, text):
    return f'<div class="nurse-note-row"><span class="nurse-note-time">{time}:</span><span class="nurse-note-text">{text}</span></div>'


def opts(*pairs):
    return [{"text": t, "correct": c} for t, c in pairs]


def blank_options(n):
    return [{"text": "", "correct": False} for _ in range(n)]


NOTE_1000 = (
    "Client was brought to the ED by the client's adult child due to increased shortness of "
    "breath this morning. The adult child reports that the client has been running a fever for "
    "the past few days and has started to cough up greenish mucus and to complain of soreness "
    "throughout the body. Client was hospitalized for issues with atrial fibrillation 6 days ago. "
    "History of hypertension. Vital signs: T 101.1&deg; F (38.4&deg; C), P 92, RR 22, BP 152/86, "
    "pulse oximetry reading 94% on oxygen at 2 L/min via nasal cannula. On assessment, the "
    "client's breathing appears slightly labored, and coarse crackles (rales) are noted in the "
    "bilateral lung bases. Skin slightly cool to touch and pale pink in tone; pulses 3+ and "
    "irregular. Capillary refill is 3 seconds. Client is alert and oriented to person, place, and "
    "time. The adult child states, “Sometimes it seems like my parent is confused.” "
    "Peripheral venous access device (VAD) placed in right forearm."
)
NOTE_1200 = (
    "Called to bedside by the adult child who states that the client “isn't acting right.” "
    "On assessment, client is difficult to arouse, pale, and diaphoretic. Vital signs: P 112, RR 32, "
    "BP 90/62, pulse oximetry reading 91% on 2 L/min via nasal cannula."
)
NOTES_TAB_S13 = "<p><b>Emergency Department</b></p>" + note_row("1000", NOTE_1000)
NOTES_TAB_S46 = NOTES_TAB_S13 + note_row("1200", NOTE_1200)

ORDERS_1215 = (
    "<p><b>Orders</b></p><p><b>1215:</b></p><ul>"
    "<li>{insert an indwelling urethral catheter}</li>"
    "<li>{vancomycin 1 g, IV, every 12 hours|correct}</li>"
    "<li>{computed tomography (CT) scan of the chest}</li>"
    "<li>{0.9% sodium chloride (normal saline) 500 mL, IV, once|correct}</li>"
    "<li>{laboratory tests: blood culture and sensitivity (C &amp; S), complete blood count (CBC), arterial blood gas (ABG)|correct}</li>"
    "</ul>"
)
ORDERS_TAB_PLAIN = (
    "<p><b>Orders</b></p><p><b>1215:</b></p><ul>"
    "<li>insert an indwelling urethral catheter</li>"
    "<li>vancomycin 1 g, IV, every 12 hours</li>"
    "<li>computed tomography (CT) scan of the chest</li>"
    "<li>0.9% sodium chloride (normal saline) 500 mL, IV, once</li>"
    "<li>laboratory tests: blood culture and sensitivity (C &amp; S), complete blood count (CBC), arterial blood gas (ABG)</li>"
    "</ul>"
)


def screen(step, question, tabs, intro=INTRO):
    q = dict(question)
    q.setdefault("footnote", FOOTNOTE)
    return {"step": step, "question": q, "leftContent": {"tabs": tabs, "intro": intro}}


screens = []

# Screen 1 -- recognize cues (select_n, limit 4)
screens.append(screen(1, {
    "stem": "Select the 4 client findings that require <b>immediate</b> follow-up.",
    "type": "select_n",
    "limit": 4,
    "preamble": "",
    "options": opts(
        ("vital signs", True),
        ("lung sounds", True),
        ("capillary refill", False),
        ("client orientation", False),
        ("radial pulse characteristics", True),
        ("characteristics of the cough", True),
    ),
    "explanation": (
        "The vital signs require follow-up: a fever of 101.1&deg;F and a pulse oximetry reading of "
        "94% despite supplemental oxygen both signal an active, worsening process. The lung sounds "
        "require follow-up: coarse bilateral crackles are consistent with pneumonia. The radial "
        "pulse characteristics require follow-up: an irregular pulse could reflect the client's "
        "known atrial fibrillation becoming unstable under physiologic stress. The characteristics "
        "of the cough require follow-up: greenish (purulent) sputum points to a bacterial "
        "respiratory infection. Capillary refill of 3 seconds is only borderline/minimally delayed "
        "and does not clearly require immediate follow-up. Client orientation is documented as "
        "intact (alert and oriented to person, place, and time) on this assessment, even though the "
        "adult child reports occasional confusion historically; the current objective finding is "
        "normal."
    ),
}, [{"id": "nn_case3", "title": "Nurses' Notes", "content": NOTES_TAB_S13}]))

# Screen 2 -- analyze cues (matrix_mr)
screens.append(screen(2, {
    "stem": "For each client finding below, click to specify if the finding is consistent with the disease process of pneumonia, a urinary tract infection (UTI), or influenza. Each finding may support more than 1 disease process.",
    "type": "matrix_mr",
    "matrix": {
        "rows": [
            {"text": "fever", "correctIndices": [0, 1, 2]},
            {"text": "confusion", "correctIndices": [0, 1]},
            {"text": "body soreness", "correctIndices": [2]},
            {"text": "cough and sputum", "correctIndices": [0]},
            {"text": "shortness of breath", "correctIndices": [0, 2]},
        ],
        "columns": ["Pneumonia", "Urinary Tract Infection", "Influenza"],
        "firstColumnHeader": "Client Findings",
    },
    "options": blank_options(5),
    "preamble": "",
    "explanation": (
        "Fever is a nonspecific sign of infection consistent with all 3 processes. Confusion in an "
        "older adult is a classic atypical presentation of a UTI and can also occur with pneumonia "
        "through hypoxia or a systemic inflammatory response, but is not a hallmark influenza "
        "finding. Body soreness (myalgia) is a hallmark influenza symptom and is not characteristic "
        "of pneumonia or a UTI. Cough with purulent (greenish) sputum is characteristic of bacterial "
        "pneumonia; influenza classically causes a dry cough, and a UTI does not cause cough. "
        "Shortness of breath is consistent with pneumonia (the primary respiratory process) and can "
        "occur with influenza (especially with complications), but is not a UTI finding."
    ),
}, [{"id": "nn_case3", "title": "Nurses' Notes", "content": NOTES_TAB_S13}]))

# Screen 3 -- prioritize hypotheses (dropdown_cloze, revealed)
screens.append(screen(3, {
    "stem": "Complete the following sentence by choosing from the list of options.",
    "type": "dropdown_cloze",
    "cloze": {
        "text": "The client is at highest risk for developing [[drop0]].",
        "dropdowns": [
            {"placeholder": "Select...", "options": opts(("stroke", False), ("hypoxia", False), ("dysrhythmias", True), ("a pulmonary embolism", False))},
        ],
    },
    "options": blank_options(4),
    "preamble": "",
    "explanation": (
        "The client has a recent history of atrial fibrillation, and the physiologic stress of an "
        "acute infection (fever, hypoxia, tachycardia) commonly destabilizes an existing arrhythmia "
        "or provokes a new one, making dysrhythmias the highest risk. Hypoxia, stroke, and pulmonary "
        "embolism are all plausible general risks for an acutely ill older adult, but none is as "
        "directly tied to this client's specific known cardiac history as a dysrhythmia is."
    ),
}, [{"id": "nn_case3", "title": "Nurses' Notes", "content": NOTES_TAB_S13}]))

# Screen 4 -- generate solutions (matrix_mc)
screens.append(screen(4, {
    "stem": "For each potential nursing intervention, click to specify whether the intervention is indicated or not indicated for the care of the client.",
    "type": "matrix_mc",
    "matrix": {
        "rows": [
            {"text": "Prepare the client for defibrillation.", "correctIndex": 1},
            {"text": "Place client in a semi-Fowler's position.", "correctIndex": 0},
            {"text": "Request an order to increase the oxygen flow rate.", "correctIndex": 0},
            {"text": "Request an order to insert an additional peripheral VAD.", "correctIndex": 0},
            {"text": "Request an order to administer an intravenous fluid bolus.", "correctIndex": 0},
        ],
        "columns": ["Indicated", "Not Indicated"],
        "firstColumnHeader": "Potential Nursing Interventions",
    },
    "options": blank_options(5),
    "preamble": "The nurse has reviewed the Nurses' Notes from 1200.",
    "explanation": (
        "Defibrillation is not indicated: it treats pulseless ventricular fibrillation/tachycardia, "
        "and this client has a pulse and is not in cardiac arrest. A semi-Fowler's position is "
        "indicated to ease the client's work of breathing. Increasing the oxygen flow rate is "
        "indicated given the client's hypoxia (91% despite 2 L/min). An additional VAD is indicated "
        "to support anticipated fluids and IV medications. An intravenous fluid bolus is indicated "
        "given the client's new hypotension (90/62), tachycardia, and signs suggestive of early "
        "septic shock."
    ),
}, [{"id": "nn_case3", "title": "Nurses' Notes", "content": NOTES_TAB_S46}]))

# Screen 5 -- take action (highlight, revealed)
screens.append(screen(5, {
    "stem": "Click to highlight the orders that the nurse should consider a priority.",
    "type": "highlight",
    "preamble": "The nurse has reviewed the Orders from 1215.",
    "options": blank_options(5),
    "highlightTabs": [{"id": "ht_case3_s5", "title": "Orders", "content": ORDERS_1215}],
    "maxCorrectSelections": None,
    "explanation": (
        "The vancomycin, the normal saline bolus, and the blood culture/CBC/ABG labs form the core "
        "of a sepsis-bundle response to a client with a likely serious infection and new signs of "
        "shock: cultures should be drawn before (or essentially alongside) starting antibiotics, "
        "antibiotics should be given promptly, and fluids address the hypotension. The indwelling "
        "urethral catheter and the chest CT are reasonable orders but are not as time-critical as "
        "the sepsis-bundle interventions."
    ),
}, [{"id": "nn_case3", "title": "Nurses' Notes", "content": NOTES_TAB_S46}, {"id": "ord_case3", "title": "Orders", "content": ORDERS_TAB_PLAIN}]))

# Screen 6 -- evaluate outcomes (matrix_mc, improved/not changed/worsened)
screens.append(screen(6, {
    "stem": "For each assessment finding, click to specify if the finding indicates that the client's condition has improved, not changed, or worsened.",
    "type": "matrix_mc",
    "matrix": {
        "rows": [
            {"text": "pale skin tone", "correctIndex": 1},
            {"text": "respirations, 36", "correctIndex": 2},
            {"text": "blood pressure, 118/68", "correctIndex": 0},
            {"text": "pulse oximetry reading 91%", "correctIndex": 1},
            {"text": "client interacting with adult child at bedside", "correctIndex": 0},
        ],
        "columns": ["Improved", "Not Changed", "Worsened"],
        "firstColumnHeader": "Assessment Findings",
    },
    "options": blank_options(5),
    "preamble": "",
    "explanation": (
        "Compared to the 1200 assessment (P 112, RR 32, BP 90/62, pulse oximetry 91%, difficult to "
        "arouse, pale, diaphoretic), the blood pressure of 118/68 is improved (no longer "
        "hypotensive), and the client interacting with the adult child at the bedside is improved "
        "(previously difficult to arouse). Pale skin tone is not changed (still pale, as before). "
        "The pulse oximetry reading of 91% is not changed (identical to the 1200 value). "
        "Respirations of 36 are worsened (up from 32), showing the client's respiratory status "
        "remains a concern even as circulation and mental status are trending in the right "
        "direction."
    ),
}, [{"id": "nn_case3", "title": "Nurses' Notes", "content": NOTES_TAB_S46}, {"id": "ord_case3", "title": "Orders", "content": ORDERS_TAB_PLAIN}]))

item = {
    "id": "case_1786030000001",
    "unit": "Unit 3 (Respiratory Disorders)",
    "title": "NURS 1021 Unit 3 Case Study 1",
    "topic": "Unit 3 (Respiratory Disorders)",
    "course": "NURS 1021",
    "screens": screens,
    "disorder": "Unit 3 (Respiratory Disorders)",
    "description": "NCSBN NCLEX-RN Next Generation Exam Preview Case Study: a 78-year-old female client with pneumonia and a history of atrial fibrillation, presenting with fever, cough, and confusion, progressing toward septic shock, from recognize cues through evaluate outcomes.",
    "availability": "all",
}

if __name__ == "__main__":
    out_path = os.path.join(DRAFTS_DIR, "case_1786030000001_NURS_1021_Unit_3_Case_Study_1.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(item, f, indent=2, ensure_ascii=False)
    print("wrote", out_path)
