"""Fixes the existing 'NCSBN - Case Study 1' item (case_1781741217820), already published
in cases-data.js under course/unit "Others"/"Others", using the full 6-screen NCSBN NCLEX-RN
Next Generation Exam Preview PDF the user attached (Case_Study_1_exampreview.pdf).

This does NOT touch cases-data.js or the live database. It writes a corrected copy of the
item to drafts/ for review; the fix is applied to the live database only after the user
approves (via a careful download -> edit -> verify -> upload cycle, per CLAUDE.md's hard
rules on never overwriting the database without diffing first).

What changed vs. the existing published item:
1. Screen 1 highlight answer key corrected: the official PDF shows the ENTIRE vital-signs
   sentence highlighted as a single finding ("Vital signs: T 103.4F..., P 92, RR 22, BP
   130/86, pulse oximetry reading 98% on room air."), not just the temperature/pulse/RR/BP
   portion. The existing item had "pulse oximetry reading 98% on room air" marked as an
   incorrect distractor -- verified wrong by close inspection of the source PDF's highlighted
   screenshot (screens 7-8 in the PDF).
2. Typos fixed: "soadsuds enema" -> "soapsuds enema", "computed tomograph" -> "computed
   tomography" (screen 4).
3. Every screen gets question.footnote (NCSBN copyright), per the user's request that this
   apply to the case study too.
4. Moved from course/unit "Others"/"Others" into NURS 1021 / Unit 6 (Gastrointestinal
   Disorders) -- the first case study in that unit -- and title renamed to match the
   "NURS <course> Unit <n> Case Study <n>" convention used elsewhere in the bank.
5. Rationales merged/enriched: kept the substance of each existing explanation and expanded
   it to address every option/row/blank explicitly (screens 3 and 6 use the "(Option N)"
   convention; matrix/dropdown screens explain each row/blank by name).
6. Literal tab characters (stray copy-paste artifacts throughout the existing item's stems,
   preambles, and tab content) normalized to spaces.
"""
import json
import os

DRAFTS_DIR = os.path.dirname(os.path.abspath(__file__))

FOOTNOTE = (
    "&copy; NCSBN. Taken from https://www.nclex.com/prepare.page; "
    "click on &#39;Download Exam Preview&#39;."
)

COURSE = "NURS 1021"
UNIT = "Unit 6 (Gastrointestinal Disorders)"

NOTE_1100 = (
    "Client reports nausea, loss of appetite, vomiting, fever, and constipation for the past "
    "2 weeks and abdominal pain rated 7/10 on the Numerical Rating Scale for 1 week. Client "
    "states, “The abdominal pain started after my 7-year-old child accidentally kicked me "
    "in the stomach.” Client plays soccer with the child once a week. Vital signs: "
    "T 103.4° F (39.7° C), P 92, RR 22, BP 130/86, pulse oximetry reading 98% on room "
    "air. No significant past medical or surgical history. Body mass index (BMI) of 32. Drinks "
    "alcohol only during social occasions, usually 3 beverages. Smokes cigarettes during social "
    "occasions."
)

def note_row(time, text):
    return f'<div class="nurse-note-row"><span class="nurse-note-time">{time}:</span><span class="nurse-note-text">{text}</span></div>'

NOTES_TAB_BASE = '<p><b>Emergency Department</b></p>' + note_row("1100", NOTE_1100)
NOTES_TAB_S4 = NOTES_TAB_BASE + note_row("1130", "Notified primary health care provider about client status. Awaiting orders.")
NOTES_TAB_S5 = (
    NOTES_TAB_S4
    + note_row("1230", "Client transported to radiology department for abdominal computed tomography (CT) scan.")
    + note_row("1245", "20-gauge peripheral venous access device (VAD) inserted into the left hand. VAD site patent without signs of infiltration. 0.9% sodium chloride (normal saline) infusing at 75 mL/hr.")
    + note_row("1400", "Client reports sudden relief of abdominal pain. Vital signs: T 102.5° F (39.2° C), P 110, RR 20, BP 125/86.")
    + note_row("1415", "Primary health care provider notified about client status. Order received for an additional abdominal CT scan. Client transported to radiology department.")
)
NOTES_TAB_S6 = (
    NOTES_TAB_S5
    + note_row("1800", "Client transported to the operating room for an open appendectomy.")
    + '<div><b>Medical-Surgical Unit</b></div>'
    + note_row("2030", "Client transported back to the medical-surgical unit.")
    + note_row("2230", "Client performing coughing and deep-breathing exercises every hour while awake with the incentive spirometer. Performing postoperative leg exercises every hour while awake. Nasogastric (NG) tube removed. Drinking clear liquids. Abdomen boardlike with diminished bowel sounds in all quadrants. Rebound tenderness present.")
)

DIAGNOSTIC_TAB = (
    '<p class="nurse-note-row"><span class="nurse-note-time">1100:</span>'
    '<span class="nurse-note-text">Acute gangrenous appendix with calcified appendicolith.</span></p>'
    '<div class="nurse-note-row"><span class="nurse-note-time">1130: '
    '<span style="font-weight: normal;">Free intraperitoneal fluid noted consistent with a ruptured appendix.</span></span>'
    '<span class="nurse-note-text"><br></span></div>'
)

INTRO = "The nurse in the emergency department (ED) is caring for a 41-year-old male client."


def opts(*pairs):
    return [{"text": t, "correct": c} for t, c in pairs]


def blank_options(n):
    return [{"text": "", "correct": False} for _ in range(n)]


screens = []

# Screen 1: highlight (recognize cues)
highlight_content = (
    "Client reports {nausea,} {loss of appetite,|correct} "
    "{vomiting, fever, and constipation for the past 2 weeks} and "
    "{abdominal pain rated 7/10 on the Numerical Rating Scale for 1 week. Client states, "
    "“The abdominal pain started after my 7-year-old child accidentally kicked me in the "
    "stomach.”|correct} "
    "{Client plays soccer with the child once a week.} "
    "{Vital signs: T 103.4° F (39.7° C), P 92, RR 22, BP 130/86, pulse oximetry reading "
    "98% on room air.|correct} "
    "{No significant past medical or surgical history.} {Body mass index (BMI) of 32.} "
    "{Drinks alcohol only during social occasions, usually 3 beverages.} "
    "{Smokes cigarettes during social occasions.}"
)
screens.append({
    "step": 1,
    "question": {
        "stem": "Click to highlight the findings below that would require follow-up.",
        "type": "highlight",
        "options": blank_options(5),
        "preamble": INTRO,
        "footnote": FOOTNOTE,
        "explanation": (
            "Loss of appetite is highlighted because it is a classic early symptom of appendicitis "
            "and other acute intra-abdominal inflammatory processes. The abdominal pain description "
            "is highlighted because pain rated 7/10, present for a full week, and attributed by the "
            "client to a single kick 9 days earlier is disproportionate to a single minor blunt-trauma "
            "event and instead suggests an evolving intra-abdominal process such as appendicitis, "
            "bowel obstruction, or an unrecognized traumatic injury (for example, to the spleen). The "
            "full vital sign set — T 103.4°F (39.7°C), P 92, RR 22, BP 130/86, and pulse "
            "oximetry 98% — is highlighted as one finding because the fever signals an infectious "
            "or inflammatory process, and together with the mildly elevated pulse and respiratory rate "
            "it reflects an early systemic response to that process, even though the pulse, respiratory "
            "rate, and oxygen saturation are each close to normal in isolation. Nausea, the narrative "
            "mention of vomiting/fever/constipation, and the client playing soccer with the child once "
            "a week restate or add context to the more specific findings above without independently "
            "requiring follow-up. No significant past medical or surgical history, the BMI of 32, and "
            "the client's social alcohol and cigarette use are baseline/lifestyle information, not acute "
            "findings, and do not require follow-up."
        ),
        "highlightTabs": [{"id": "ht_1781743042143", "title": "Nurses' Notes", "content": highlight_content}],
        "maxCorrectSelections": None,
    },
    "leftContent": {"tabs": [{"id": "nn_1781741217820", "title": "Nurses' Notes", "content": ""}], "intro": ""},
})

# Screen 2: matrix_mr (analyze cues)
screens.append({
    "step": 2,
    "question": {
        "stem": "For each assessment finding below, click to specify if the finding is consistent with the disease process of bowel obstruction, appendicitis, or ruptured spleen. Each finding may support more than 1 disease process.",
        "type": "matrix_mr",
        "matrix": {
            "rows": [
                {"text": "appetite", "correctIndices": [0, 1]},
                {"text": "pain level", "correctIndices": [0, 1, 2]},
                {"text": "bowel pattern", "correctIndices": [0, 1]},
                {"text": "gastrointestinal symptoms", "correctIndices": [0, 1]},
            ],
            "columns": ["Bowel Obstruction", "Appendicitis", "Ruptured Spleen"],
            "firstColumnHeader": "Assessment Finding",
        },
        "options": blank_options(5),
        "preamble": "",
        "footnote": FOOTNOTE,
        "explanation": (
            "Decreased appetite is consistent with bowel obstruction and appendicitis (both cause "
            "visceral inflammation or distension that suppresses appetite) but is not a typical "
            "finding of an isolated ruptured spleen, so appetite is checked under Bowel Obstruction "
            "and Appendicitis only. Pain level is checked under all 3 disease processes because bowel "
            "obstruction, appendicitis, and a ruptured spleen can each cause significant abdominal "
            "pain — obstruction from bowel wall distension, appendicitis from localized peritoneal "
            "irritation, and splenic rupture from hemoperitoneum and capsular stretch. Bowel pattern "
            "(constipation) is checked under Bowel Obstruction and Appendicitis, since mechanical "
            "obstruction directly halts stool passage and appendicitis commonly causes an associated "
            "ileus with constipation, while an isolated splenic injury does not typically alter bowel "
            "pattern. Gastrointestinal symptoms such as nausea and vomiting are checked under Bowel "
            "Obstruction and Appendicitis, both of which commonly trigger vomiting through bowel "
            "distension or peritoneal irritation, whereas an isolated splenic rupture (a vascular/"
            "hemorrhagic injury) does not typically produce prominent nausea and vomiting on its own."
        ),
    },
    "leftContent": {"tabs": [{"id": "nn_1781741217820", "title": "Nurses' Notes", "content": NOTES_TAB_BASE}], "intro": INTRO},
})

# Screen 3: select_n (prioritize hypotheses)
screens.append({
    "step": 3,
    "question": {
        "stem": "Select the 3 complications the client is at risk for developing.",
        "type": "select_n",
        "limit": 3,
        "options": opts(
            ("anemia", False),
            ("peritonitis", True),
            ("septic shock", True),
            ("hypovolemia", True),
            ("dysrhythmias", False),
            ("cardiac arrest", False),
        ),
        "preamble": "",
        "footnote": FOOTNOTE,
        "explanation": (
            "The client's presentation and CT findings (revealed later in the case) are consistent "
            "with a gangrenous, ruptured appendix. A ruptured appendix spills infected intestinal "
            "contents into the peritoneal cavity, so peritonitis (Option 2) — inflammation of the "
            "peritoneum — is a direct and expected complication. Untreated peritonitis can progress "
            "to septic shock (Option 3) as bacteria and inflammatory mediators enter the bloodstream. "
            "Vomiting, fever, and fluid shifting into the inflamed peritoneal space (third spacing) "
            "place the client at risk for hypovolemia (Option 4) from both fluid loss and reduced oral "
            "intake. Anemia (Option 1) is not an expected complication of appendiceal rupture, since "
            "this process does not typically cause significant blood loss. Dysrhythmias (Option 5) and "
            "cardiac arrest (Option 6) are late, severe complications that could theoretically follow "
            "untreated septic shock, but they are not among the 3 most directly expected complications "
            "of a ruptured appendix."
        ),
    },
    "leftContent": {"tabs": [{"id": "nn_1781741217820", "title": "Nurses' Notes", "content": NOTES_TAB_BASE}], "intro": INTRO},
})

# Screen 4: matrix_mc (generate solutions)
screens.append({
    "step": 4,
    "question": {
        "stem": "For each potential intervention, click to specify whether the intervention is indicated or not indicated for the client.",
        "type": "matrix_mc",
        "matrix": {
            "rows": [
                {"text": "clear liquid diet", "correctIndex": 1},
                {"text": "soapsuds enema", "correctIndex": 1},
                {"text": "heating pad to abdomen", "correctIndex": 1},
                {"text": "abdominal girth measurements", "correctIndex": 1},
                {"text": "abdominal computed tomography (CT) scan", "correctIndex": 0},
            ],
            "columns": ["Indicated", "Not Indicated"],
            "firstColumnHeader": "Potential Intervention",
        },
        "options": blank_options(5),
        "preamble": "The nurse has reviewed the Nurses' Notes from 1130.",
        "footnote": FOOTNOTE,
        "explanation": (
            "A clear liquid diet is not indicated because the client should remain NPO (nothing by "
            "mouth) while an acute surgical abdomen is being evaluated and urgent surgery is "
            "anticipated; oral intake increases aspiration risk with anesthesia and can worsen nausea/"
            "vomiting. A soapsuds enema is not indicated because increasing intraluminal pressure and "
            "peristalsis in an inflamed or possibly obstructed/perforated bowel raises the risk of "
            "worsening perforation. A heating pad to the abdomen is not indicated because heat "
            "increases local blood flow and metabolic activity in inflamed tissue, which can accelerate "
            "an inflammatory process, and is contraindicated whenever appendicitis is suspected (it can "
            "increase the risk of rupture). Abdominal girth measurements are not indicated as a "
            "priority action here; they help trend progressive distension in conditions such as bowel "
            "obstruction or ascites, but they do not provide diagnostic information about the "
            "underlying disease process. An abdominal CT scan is indicated because it is the key "
            "diagnostic study needed to identify the cause of the client's pain — appendicitis, "
            "bowel obstruction, or a traumatic injury such as splenic rupture — and to guide the "
            "surgical plan."
        ),
    },
    "leftContent": {"tabs": [{"id": "nn_1781741217820", "title": "Nurses' Notes", "content": NOTES_TAB_S4}], "intro": INTRO},
})

# Screen 5: dropdown_cloze (take action)
screens.append({
    "step": 5,
    "question": {
        "stem": "Complete the following sentence by choosing from the lists of options.",
        "type": "dropdown_cloze",
        "cloze": {
            "text": "The nurse should insert [[drop0]]. It would be a priority for the nurse to request a prescription for an [[drop1]]. The nurse should prepare the client for surgery within [[drop2]].",
            "dropdowns": [
                {"placeholder": "Select...", "options": opts(("rectal tube", False), ("a nasogastric (NG) tube", True), ("an indwelling urethral catheter", False))},
                {"placeholder": "Select...", "options": opts(("analgesic medication", False), ("antipyretic medication", False), ("anti-infective medication", True))},
                {"placeholder": "Select...", "options": opts(("6 hours", True), ("8 hours", False), ("24 hours", False))},
            ],
        },
        "options": blank_options(5),
        "preamble": "The nurse has reviewed the Nurses' Notes from 1230, 1245, 1400, and 1415 and the Diagnostic Results from 1230 and 1445.",
        "footnote": FOOTNOTE,
        "explanation": (
            "The CT scan confirms acute gangrenous appendicitis with a calcified appendicolith, and "
            "the follow-up scan — ordered after the client's sudden pain relief, which can signal "
            "that the appendix has ruptured and relieved pressure-related pain — confirms free "
            "intraperitoneal fluid consistent with a ruptured appendix. The nurse should insert a "
            "nasogastric (NG) tube, not a rectal tube or indwelling urethral catheter, to decompress "
            "the stomach, reduce nausea/vomiting, and reduce aspiration risk before surgery. An "
            "anti-infective (antibiotic) medication is the priority prescription to request, over an "
            "analgesic or antipyretic, because a ruptured appendix has caused peritoneal contamination "
            "and the client is at immediate risk for progression to sepsis/septic shock; treating the "
            "underlying infection takes priority, though analgesics and antipyretics may also "
            "ultimately be given for comfort. The client should be prepared for surgery within 6 hours, "
            "not 8 or 24 hours, because a ruptured appendix with free peritoneal fluid is a surgical "
            "emergency — delaying surgery further increases the risk of worsening sepsis and "
            "peritoneal contamination."
        ),
    },
    "leftContent": {
        "tabs": [
            {"id": "nn_1781741217820", "title": "Nurses' Notes", "content": NOTES_TAB_S5},
            {"id": "tab_1781749126110", "title": "Diagnostic Results", "content": DIAGNOSTIC_TAB},
        ],
        "intro": INTRO,
    },
})

# Screen 6: select_all (evaluate outcomes)
screens.append({
    "step": 6,
    "question": {
        "stem": "Which of the following findings would indicate the client is progressing as expected? <b>Select all that apply.</b>",
        "type": "select_all",
        "options": opts(
            ("clear, liquid diet", False),
            ("board-like abdomen", False),
            ("rebound tenderness", False),
            ("incentive spirometry use", True),
            ("diminished bowel sounds", False),
            ("performance of leg exercises", True),
        ),
        "preamble": "The nurse has reviewed the Nurses' Notes from 1800, 2030, and 2230.",
        "footnote": FOOTNOTE,
        "explanation": (
            "Incentive spirometry use (Option 4) and performance of leg exercises (Option 6) are "
            "expected, appropriate postoperative behaviors that indicate the client is progressing as "
            "expected: incentive spirometry and coughing/deep breathing reduce the risk of atelectasis "
            "and pneumonia, and leg exercises reduce the risk of venous thromboembolism during a period "
            "of reduced mobility after surgery. A clear liquid diet (Option 1) alone is not evidence of "
            "expected progress; how oral intake is advanced depends on the client's bowel and abdominal "
            "assessment findings, which in this case remain abnormal. A boardlike (rigid) abdomen "
            "(Option 2), rebound tenderness (Option 3), and diminished bowel sounds (Option 5) are "
            "concerning findings, not expected ones, after surgery for a ruptured appendix; a boardlike "
            "abdomen and rebound tenderness suggest ongoing peritoneal irritation or a new complication "
            "such as an abscess, and diminished bowel sounds can indicate a postoperative ileus. All 3 "
            "require follow-up rather than indicating expected progress."
        ),
    },
    "leftContent": {
        "tabs": [
            {"id": "nn_1781741217820", "title": "Nurses' Notes", "content": NOTES_TAB_S6},
            {"id": "tab_1781749126110", "title": "Diagnostic Results", "content": DIAGNOSTIC_TAB},
        ],
        "intro": INTRO,
    },
})

item = {
    "id": "case_1781741217820",
    "unit": UNIT,
    "title": "NURS 1021 Unit 6 Case Study 1",
    "topic": UNIT,
    "course": COURSE,
    "screens": screens,
    "disorder": UNIT,
    "description": "NCSBN NCLEX-RN Next Generation Exam Preview Case Study 1: a 41-year-old male client with a ruptured appendix, from recognize cues through evaluate outcomes.",
    "availability": "all",
}

if __name__ == "__main__":
    out_path = os.path.join(DRAFTS_DIR, "case_1781741217820_FIXED_NURS_1021_Unit_6_Case_Study_1.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(item, f, indent=2, ensure_ascii=False)
    print("wrote", out_path)
