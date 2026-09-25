"""Builds NURS 1021 Unit 6 Case Study 2 (splenic laceration/hemothorax) from the NCSBN
NCLEX-RN Next Generation Exam Preview PDF (c 2022 NCSBN), third attachment (Test3.pdf,
items 32-37, screens 1-6). Same conventions as the other builders in this directory: every
screen carries question.footnote (NCSBN copyright, shown below Submit).

The source shows the revealed answer for the screen-3 dropdown ("respiratory status") and the
screen-6 highlight, but NOT for screens 1, 2, 4, or 5 -- those answer keys are this session's
own clinical judgment and need clinician review before publish, same as every other item in
this project so far.
"""
import json
import os

DRAFTS_DIR = os.path.dirname(os.path.abspath(__file__))

FOOTNOTE = (
    "&copy; NCSBN. Taken from https://www.nclex.com/prepare.page; "
    "click on &#39;Download Exam Preview&#39;."
)

INTRO = "The nurse in the emergency department (ED) is caring for a 17-year-old male client."

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


HP_TABLE = table(
    ["Body System", "Findings"],
    [
        ("Pulmonary", "denies shortness of breath; reports discomfort in the lower left side of chest when taking a deep breath"),
        ("Gastrointestinal", "reports feeling abdominal fullness and is occasionally nauseated"),
        ("Musculoskeletal", "sustained an injury to the left rib cage after being struck by a mechanically pitched baseball in a batting cage last week; reports intermittent pain in the left shoulder rated 6/10 on the Numerical Rating Scale; light-headed; significant bruising to the shoulder; history of an orthoscopic repair to the left shoulder for a torn rotator cuff last year"),
        ("Psychosocial", "client has not felt well enough to attend baseball practice since the injury"),
    ],
)

VITALS_TABLE = table(
    ["", "Emergency Department<br>Day 1<br>0900"],
    [
        ("T", "97.8&deg; F (36.6&deg; C)"),
        ("P", "116"),
        ("RR", "24"),
        ("BP", "90/50"),
        ("Pulse oximetry reading", "98% on room air"),
    ],
)

LABS_TABLE = table(
    ["Laboratory Test and Reference Range", "Emergency Department<br>Day 1<br>0900"],
    [
        ("white blood cell (WBC) count<br>Adult/child &gt; 2 years: 5,000&ndash;10,000/mm&sup3; (5&ndash;10 x 10&sup9;/L)", "19,000/mm&sup3; (19 x 10&sup9;/L)"),
        ("hemoglobin (Hgb)<br>Male: 14&ndash;18 g/dL (140&ndash;180 g/L)<br>Female: 12&ndash;16 g/dL (120&ndash;160 g/L)", "9 g/dL (90 g/L)"),
        ("hematocrit (HCT)<br>Male: 42%&ndash;52% (0.42&ndash;0.52)<br>Female: 37%&ndash;47% (0.37&ndash;0.47)", "27% (0.27)"),
    ],
)

NOTES_DAY1_0900 = (
    "Client appears pale and slightly diaphoretic. Large amount of bruising noted along the left "
    "torso and over the left upper quadrant (LUQ) of the abdomen. Tenderness, guarding, and "
    "dullness to percussion noted on abdominal assessment. Slightly diminished breath sounds in "
    "the left lung fields on auscultation; client has a productive cough. Electrocardiogram (ECG) "
    "shows normal sinus rhythm."
)
NOTES_TAB_S12 = "<p><b>Emergency Department</b></p><p><b>Day 1</b></p>" + note_row("0900", NOTES_DAY1_0900)
NOTES_TAB_S3 = NOTES_TAB_S12
NOTES_TAB_S4 = NOTES_TAB_S12 + note_row("1000", "Client diagnosed with a splenic laceration and a left-sided hemothorax per the physician.")
NOTES_TAB_S5 = NOTES_TAB_S4 + note_row("1030", "Client referred for immediate surgery.")

PROGRESS_NOTE_DAY3 = (
    "Client is postoperative day 3 after a splenectomy and is able to ambulate in the corridor 3 "
    "or 4 times daily with minimal assistance. Client has clear breath sounds bilaterally. Left-"
    "sided chest tube in place attached to a closed-chest drainage system. Tidaling of the water "
    "chamber noted on drainage system. {Client refuses to use the incentive spirometer, stating it "
    "causes left-sided chest pain. Client is using prescribed patient-controlled analgesia (PCA) "
    "device maximally every hour and continues to have intermittent nausea and vomiting.|correct} "
    "Adequate urine output. Abdominal surgical incision site with dressing clean, dry, and intact "
    "with no erythema, edema, or drainage."
)
PROGRESS_TAB = "<p><b>Progress Notes</b></p><p><b>Day 3</b></p>" + note_row("0800", PROGRESS_NOTE_DAY3)


def screen(step, question, tabs, intro=INTRO):
    q = dict(question)
    q.setdefault("footnote", FOOTNOTE)
    return {
        "step": step,
        "question": q,
        "leftContent": {
            "tabs": [
                {"id": "hp_case2", "title": "History and Physical", "content": HP_TABLE},
                {"id": "nn_case2", "title": "Nurses' Notes", "content": tabs.get("notes", "")},
                {"id": "vs_case2", "title": "Vital Signs", "content": VITALS_TABLE},
                {"id": "lab_case2", "title": "Laboratory Results", "content": LABS_TABLE},
            ],
            "intro": intro,
        },
    }


screens = []

# Screen 1 -- recognize cues (select_all, 7 options)
screens.append(screen(1, {
    "stem": "Which of the following assessment findings require <b>immediate</b> follow-up? <b>Select all that apply.</b>",
    "type": "select_all",
    "preamble": "",
    "options": opts(
        ("lung sounds", True),
        ("shoulder pain", True),
        ("laboratory results", True),
        ("productive cough", False),
        ("abdominal assessment findings", True),
        ("pulse, respirations, and blood pressure", True),
        ("temperature and pulse oximetry reading", False),
    ),
    "explanation": (
        "Diminished breath sounds in the left lung fields (Option 1) require follow-up, since "
        "combined with the trauma history they raise concern for a hemothorax. Left shoulder pain "
        "(Option 2) requires follow-up because it can represent Kehr's sign, referred pain from "
        "diaphragmatic irritation caused by bleeding from a splenic injury, not just the client's "
        "old rotator cuff history. The laboratory results (Option 3) require follow-up: the "
        "hemoglobin of 9 g/dL and hematocrit of 27% are well below normal, consistent with ongoing "
        "blood loss, and the WBC of 19,000/mm&sup3; reflects an acute inflammatory/traumatic "
        "response. The abdominal assessment findings (Option 5) require follow-up: LUQ bruising, "
        "tenderness, guarding, and dullness to percussion over the spleen's location are classic "
        "signs of splenic injury with possible intra-abdominal bleeding. The pulse, respirations, "
        "and blood pressure (Option 6) require follow-up because tachycardia (116), tachypnea "
        "(24), and hypotension (90/50) together are early signs of hypovolemic shock from blood "
        "loss. A productive cough (Option 4) is a nonspecific finding already reflected in the "
        "more specific lung sounds finding above, and the temperature and pulse oximetry reading "
        "(Option 7) are within normal limits and do not require follow-up."
    ),
}, {"notes": NOTES_TAB_S12}))

# Screen 2 -- analyze cues (select_all, 6 options -> at risk of developing)
screens.append(screen(2, {
    "stem": "Which of the following issues is the client at risk of developing? <b>Select all that apply.</b>",
    "type": "select_all",
    "preamble": "",
    "options": opts(
        ("stroke", False),
        ("hemothorax", True),
        ("bowel perforation", True),
        ("splenic laceration", True),
        ("pulmonary embolism", False),
        ("abdominal aortic aneurysm", False),
    ),
    "explanation": (
        "Given blunt trauma to the left flank/rib cage with LUQ bruising, tenderness, diminished "
        "left breath sounds, tachycardia, and hypotension, the client is at risk for a splenic "
        "laceration (Option 4, the organ most often injured by blunt left-flank/rib trauma), a "
        "hemothorax (Option 2, given the diminished left lung sounds and chest discomfort with deep "
        "breathing), and bowel perforation (Option 3, a recognized complication of blunt abdominal "
        "trauma). A stroke (Option 1) is not a typical consequence of blunt torso trauma. A "
        "pulmonary embolism (Option 5) is not an immediate risk from this acute injury itself. An "
        "abdominal aortic aneurysm (Option 6) is a degenerative vascular condition that develops "
        "over time, not something caused by an acute traumatic injury."
    ),
}, {"notes": NOTES_TAB_S12}))

# Screen 3 -- prioritize hypotheses (dropdown_cloze, 1 blank)
screens.append(screen(3, {
    "stem": "Complete the following sentence by choosing from the list of options.",
    "type": "dropdown_cloze",
    "cloze": {
        "text": "The nurse should first address the client's [[drop0]].",
        "dropdowns": [
            {"placeholder": "Select...", "options": opts(("abdominal pain", False), ("respiratory status", True), ("laboratory results", False))},
        ],
    },
    "options": blank_options(3),
    "preamble": "",
    "explanation": (
        "The client's respiratory status is the priority using the airway-breathing-circulation "
        "framework: diminished left breath sounds, chest discomfort with deep inspiration, "
        "tachypnea (RR 24), and borderline pulse oximetry all point to a possible hemothorax "
        "compromising oxygenation, which is more immediately life-threatening than addressing "
        "abdominal pain or reviewing laboratory results, both of which are important but secondary "
        "once the airway and breathing are confirmed to be adequately supported."
    ),
}, {"notes": NOTES_TAB_S3}))

# Screen 4 -- generate solutions (matrix_mc, indicated/not indicated)
screens.append(screen(4, {
    "stem": "For each potential order, click to specify whether the potential order is indicated or not indicated for the client.",
    "type": "matrix_mc",
    "matrix": {
        "rows": [
            {"text": "intravenous fluids", "correctIndex": 0},
            {"text": "serum type and screen", "correctIndex": 0},
            {"text": "chest percussion therapy", "correctIndex": 1},
            {"text": "insertion of a nasogastric (NG) tube", "correctIndex": 0},
            {"text": "administration of prescribed pain medication", "correctIndex": 0},
        ],
        "columns": ["Indicated", "Not Indicated"],
        "firstColumnHeader": "Potential Orders",
    },
    "options": blank_options(5),
    "preamble": "The nurse has reviewed the Nurses' Notes from 1000.",
    "explanation": (
        "Intravenous fluids are indicated to begin resuscitating a client with signs of hypovolemic "
        "shock from a splenic laceration. A serum type and screen is indicated to prepare for a "
        "likely blood transfusion and anticipated surgery. Chest percussion therapy is not "
        "indicated: it is contraindicated with a hemothorax and recent rib trauma, since it can "
        "worsen bleeding and cause significant pain. Insertion of an NG tube is indicated given the "
        "client's abdominal fullness and nausea and the likelihood of surgery, to decompress the "
        "stomach and reduce aspiration risk. Administration of prescribed pain medication is "
        "indicated to treat the client's reported 6/10 pain."
    ),
}, {"notes": NOTES_TAB_S4}))

# Screen 5 -- take action (select_all, 8 options, pre-op)
screens.append(screen(5, {
    "stem": "Which of the following actions should the nurse take? <b>Select all that apply.</b>",
    "type": "select_all",
    "preamble": "The nurse has reviewed the Nurses' Notes from 1030.",
    "options": opts(
        ("Mark the surgical site.", True),
        ("Provide the client with ice chips.", False),
        ("Perform a medication reconciliation.", True),
        ("Obtain consent for surgery from the client.", False),
        ("Insert a peripheral venous access device (VAD).", True),
        ("Inform the client about the risks and benefits of the surgery.", False),
        ("Assess the client's previous experience with surgery and anesthesia.", True),
        ("Ask the client's parents to wait in the waiting room while the plan of care is discussed with the client.", False),
    ),
    "explanation": (
        "Marking the surgical site, performing a medication reconciliation, inserting a peripheral "
        "VAD, and assessing the client's previous experience with surgery and anesthesia are all "
        "standard nursing pre-operative preparation tasks. Providing ice chips is inappropriate "
        "because the client needs to be NPO before surgery. Obtaining consent and informing the "
        "client about the risks and benefits of the surgery are the surgeon's/prescriber's "
        "responsibility, not the nurse's, and legally a minor client's parent or guardian must give "
        "consent, not the 17-year-old client. Asking the client's parents to leave while the plan of "
        "care is discussed is inappropriate for a minor client; parents/guardians should be included "
        "in care planning discussions, not excluded."
    ),
}, {"notes": NOTES_TAB_S5}))

# Screen 6 -- evaluate outcomes (highlight)
screens.append(screen(6, {
    "stem": "Click to highlight the findings below that indicate a worsening of the client's status.",
    "type": "highlight",
    "preamble": "The nurse has reviewed the Progress Notes from 0800.",
    "options": blank_options(5),
    "highlightTabs": [{"id": "ht_case2_s6", "title": "Progress Notes", "content": PROGRESS_NOTE_DAY3}],
    "maxCorrectSelections": None,
    "explanation": (
        "Refusing to use the incentive spirometer because of left-sided chest pain, combined with "
        "maximal PCA use every hour and continued nausea and vomiting, indicates worsening status: "
        "poorly controlled pain that prevents deep breathing raises the risk of atelectasis and "
        "pneumonia, and ongoing nausea/vomiting despite heavy analgesic use is not the expected "
        "postoperative trajectory by day 3. Ambulating with minimal assistance, clear bilateral "
        "breath sounds, an appropriately functioning (tidaling) chest tube drainage system, adequate "
        "urine output, and a clean, dry, intact incision without erythema, edema, or drainage are "
        "all reassuring, expected findings that do not indicate worsening."
    ),
}, {"notes": NOTES_TAB_S5, }))
# Screen 6 uses the same accumulated Nurses' Notes tab as screen 5, plus its own Progress Notes tab.
screens[-1]["leftContent"]["tabs"].insert(2, {"id": "pn_case2_s6", "title": "Progress Notes", "content": PROGRESS_TAB})

item = {
    "id": "case_1786060000002",
    "unit": "Unit 6 (Gastrointestinal Disorders)",
    "title": "NURS 1021 Unit 6 Case Study 2",
    "topic": "Unit 6 (Gastrointestinal Disorders)",
    "course": "NURS 1021",
    "screens": screens,
    "disorder": "Unit 6 (Gastrointestinal Disorders)",
    "description": "NCSBN NCLEX-RN Next Generation Exam Preview Case Study: a 17-year-old male client with a splenic laceration and left-sided hemothorax from blunt trauma, from recognize cues through evaluate outcomes.",
    "availability": "all",
}

if __name__ == "__main__":
    out_path = os.path.join(DRAFTS_DIR, "case_1786060000002_NURS_1021_Unit_6_Case_Study_2.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(item, f, indent=2, ensure_ascii=False)
    print("wrote", out_path)
