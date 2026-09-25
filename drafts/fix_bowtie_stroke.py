"""Fixes the existing 'Bowtie-Stroke' item (case_1789577787012), already published in
cases-data.js under course/unit "Others"/"Others" and one of the 4 items check.js has always
flagged as known-incomplete ("answer key scores 3/5").

This item is, verbatim, the NCSBN NCLEX-RN Next Generation Exam Preview's own bowtie *example*
(fifth attachment, item 112, labeled "Bow-Tie Example Screen 1"): a 79-year-old client with
right-sided ptosis, facial drooping, hemiparesis, and expressive aphasia, plus an irregular
apical pulse of 126 bpm.

NOTE: an earlier version of this script incorrectly concluded the condition was hypoglycemia
(misreading the client's glucose value against the wrong reference range, and mistaking the
source PDF's template cell shading for a revealed answer key -- the source publishes no answer
key at all). That was wrong and has been corrected here per clinician review. The correct
read: this is a classic acute ischemic stroke presentation (right-sided ptosis/facial
drooping/hemiparesis/expressive aphasia, consistent with a left-hemisphere event), and the
irregular, tachycardic apical pulse (126 bpm) points to atrial fibrillation, a major risk
factor for embolic ischemic stroke.

The existing (published) item already had the condition right (ischemic stroke marked
correct) but was still incomplete: bowtieActions had only 1 of 2 correct actions marked, and
bowtieParams was missing 3 of its 5 options outright (blank placeholders), which is the source
of the "3/5" incomplete score check.js has tolerated all session.

This does NOT touch cases-data.js or the live database. It writes a corrected copy to drafts/
for review, exactly like the earlier case-study fix.
"""
import json
import os

DRAFTS_DIR = os.path.dirname(os.path.abspath(__file__))

FOOTNOTE = (
    "&copy; NCSBN. Taken from https://www.nclex.com/prepare.page; "
    "click on &#39;Download Exam Preview&#39;."
)

COURSE = "NURS 1017"
UNIT = "Unit 7 (Neurological Disorders)"

NOTES_TAB = (
    '<p class="nurse-note-row"><span class="nurse-note-time">1215:</span>'
    '<span class="nurse-note-text">Client presents with right-sided ptosis and facial drooping, '
    'right-sided hemiparesis, and expressive aphasia. Client’s adult child reports that the '
    'client recently had influenza. On assessment, skin is warm and dry. Lung sounds are clear; '
    'apical pulse is irregular. Bowel sounds are active in all quadrants. Client is incontinent of '
    'urine 2 times in the ED; adult child reports that the client is typically continent of urine. '
    'Capillary refill of 3 seconds. Peripheral pulses palpable, 2+. Vital signs: T 97.5° F '
    '(36.4° C), P 126, RR 18, BP 188/90, pulse oximetry reading 90% on room '
    'air.</span></p>'
)
HP_TAB = (
    '<table class="nclex-editor-table" style="width:100%; border-collapse:collapse; margin:12px 0;">'
    '<thead><tr><th style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;">Body System</th>'
    '<th style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;">Findings</th></tr></thead><tbody>'
    '<tr><td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;"><b>Neurological</b></td><td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">history of a stroke 2 years ago</td></tr>'
    '<tr><td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;"><b>Cardiovascular</b></td><td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">history of hypertension; atrial fibrillation; hyperlipidemia</td></tr>'
    '<tr><td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;"><b>Gastrointestinal</b></td><td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">history of gastrointestinal bleeding 2 months ago</td></tr>'
    '<tr><td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;"><b>Endocrine</b></td><td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">history of diabetes mellitus (type 2) for 30 years</td></tr>'
    '<tr><td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;"><b>Immunological</b></td><td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">influenza 3 weeks ago</td></tr>'
    '</tbody></table>'
)
LABS_TAB = (
    '<table class="nclex-editor-table" style="width:100%; border-collapse:collapse; margin:12px 0;">'
    '<thead><tr><th style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;">Laboratory Test and Reference Range</th>'
    '<th style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;">1215</th></tr></thead><tbody>'
    '<tr><td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;"><b>random serum glucose</b><br>Elderly 60-90 years: 4.6-6.4 mmol/L</td>'
    '<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">4.2 mmol/L</td></tr>'
    '</tbody></table>'
)


def opt(text, correct):
    return {"text": text, "correct": correct}


item = {
    "id": "case_1789577787012",
    "title": "NURS 1017 Unit 7 Bowtie 1: Ischemic Stroke with Atrial Fibrillation",
    "unit": UNIT,
    "course": COURSE,
    "topic": UNIT,
    "disorder": UNIT,
    "description": "NCSBN NCLEX-RN Next Generation Exam Preview's own bowtie item-type example: an older adult presents with classic ischemic stroke findings and a history of atrial fibrillation.",
    "screens": [{
        "step": 1,
        "question": {
            "stem": "Complete the diagram by dragging from the choices below to specify what condition the client is most likely experiencing, 2 actions the nurse should take to address that condition, and 2 parameters the nurse should monitor to assess the client’s progress.",
            "type": "bowtie",
            "options": [opt("", False) for _ in range(5)],
            "preamble": "The nurse is reviewing the client’s assessment data to prepare the client’s plan of care.",
            "footnote": FOOTNOTE,
            "explanation": (
                "<b>Condition Most Likely Experiencing</b><br>"
                "Ischemic stroke: The client exhibits classic signs of a stroke (likely in the left "
                "hemisphere), including right-sided ptosis, facial drooping, right-sided hemiparesis, "
                "and expressive aphasia. The irregular apical pulse of 126 bpm strongly suggests "
                "atrial fibrillation, which is a major risk factor for embolic ischemic strokes."
                "<br><br><b>Actions to Take</b><br>"
                "Administer oxygen at 2 L/min via nasal cannula: The client's pulse oximetry reading "
                "is 90% on room air, indicating mild hypoxia that needs to be corrected to prevent "
                "further brain tissue ischemia.<br>"
                "Insert a peripheral venous access device (VAD): Establishing IV access is a critical "
                "immediate step for suspected stroke patients to facilitate emergency lab draws, CT "
                "contrast administration, and potential thrombolytic therapy (e.g., tPA) or other "
                "medications."
                "<br><br><b>Parameters to Monitor</b><br>"
                "Neurologic status: Continuous neuro assessments (such as the NIH Stroke Scale) are "
                "vital to track the progression or resolution of the client's deficits and to monitor "
                "for potential complications like increased intracranial pressure.<br>"
                "Electrocardiogram (ECG) rhythm: Because the client presented with an irregular, "
                "tachycardic apical pulse (126 bpm), continuous ECG monitoring is necessary to "
                "evaluate the rhythm (likely atrial fibrillation) and guide rate/rhythm control "
                "interventions."
            ),
            "bowtieParams": [
                opt("urine output", False),
                opt("temperature", False),
                opt("neurologic status", True),
                opt("serum glucose level", False),
                opt("electrocardiogram (ECG) rhythm", True),
            ],
            "bowtieActions": [
                opt("Administer oxygen at 2 L/min via nasal cannula.", True),
                opt("Request a prescription for an oral corticosteroid.", False),
                opt("Insert a peripheral venous access device (VAD).", True),
                opt("Obtain a urine specimen for urinalysis and culture and sensitivity (C & S).", False),
                opt("Request an order for 50% dextrose in water to be administered intravenously.", False),
            ],
            "bowtieCol1Header": "Actions to Take",
            "bowtieCol2Header": "Potential Conditions",
            "bowtieCol3Header": "Parameters to Monitor",
            "bowtieConditions": [
                opt("Bell's palsy", False),
                opt("hypoglycemia", False),
                opt("ischemic stroke", True),
                opt("urinary tract infection (UTI)", False),
            ],
            "bowtieLeftPlaceholder": "",
            "bowtieRightPlaceholder": "",
            "bowtieCenterPlaceholder": "",
        },
        "leftContent": {
            "tabs": [
                {"id": "nn_1789577787012", "title": "Nurses' Notes", "content": NOTES_TAB},
                {"id": "tab_1789577946502", "title": "History and Physical", "content": HP_TAB},
                {"id": "tab_1789578518012", "title": "Laboratory Results", "content": LABS_TAB},
            ],
            "intro": "The nurse in the emergency department (ED) is caring for a 79-year-old female client.",
        },
    }],
    "availability": "all",
}

if __name__ == "__main__":
    out_path = os.path.join(DRAFTS_DIR, "case_1789577787012_FIXED_NURS_1017_Unit_7_Bowtie_1.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(item, f, indent=2, ensure_ascii=False)
    print("wrote", out_path)
