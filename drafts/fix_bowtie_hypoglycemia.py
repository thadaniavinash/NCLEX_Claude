"""Fixes the existing 'Bowtie-Stroke' item (case_1789577787012), already published in
cases-data.js under course/unit "Others"/"Others" and one of the 4 items check.js has always
flagged as known-incomplete ("answer key scores 3/5").

This item is, verbatim, the NCSBN NCLEX-RN Next Generation Exam Preview's own bowtie *example*
(fifth attachment, item 112, labeled "Bow-Tie Example Screen 1"): a 79-year-old client with
right-sided ptosis, facial drooping, hemiparesis, and expressive aphasia -- symptoms that look
like stroke, but the client's random serum glucose (4.2 mmol/L) is BELOW the elderly reference
range (4.6-6.4 mmol/L). This is the classic "hypoglycemia mimics stroke" teaching scenario.

The existing item has 2 real bugs, not just incompleteness:
1. bowtieConditions marks "ischemic stroke" correct; it should be "hypoglycemia".
2. bowtieActions marks "Administer oxygen..." correct (as one of only 2); the condition-specific
   pair is "Insert a peripheral VAD" + "Request an order for 50% dextrose in water IV" (the
   direct treatment for symptomatic hypoglycemia).
3. bowtieParams is missing 3 of its 5 options outright (blank placeholders) -- this is the source
   of the "3/5" incomplete score. The missing 2 correct parameters are "neurologic status" (to
   confirm the deficits resolve once glucose is corrected) and "serum glucose level"; the 5th,
   non-correct option is "electrocardiogram (ECG) rhythm", matching the source's full list of 5.

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
UNIT = "Unit 11 (Endocrine Disorders)"

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
    "title": "NURS 1017 Unit 11 Bowtie 1: Hypoglycemia Mimicking Stroke",
    "unit": UNIT,
    "course": COURSE,
    "topic": UNIT,
    "disorder": UNIT,
    "description": "NCSBN NCLEX-RN Next Generation Exam Preview's own bowtie item-type example: an older adult presents with stroke-like symptoms, but the cause is hypoglycemia.",
    "screens": [{
        "step": 1,
        "question": {
            "stem": "Complete the diagram by dragging from the choices below to specify what condition the client is most likely experiencing, 2 actions the nurse should take to address that condition, and 2 parameters the nurse should monitor to assess the client’s progress.",
            "type": "bowtie",
            "options": [opt("", False) for _ in range(5)],
            "preamble": "The nurse is reviewing the client’s assessment data to prepare the client’s plan of care.",
            "footnote": FOOTNOTE,
            "explanation": (
                "The client's neurologic deficits (facial drooping, hemiparesis, expressive "
                "aphasia) look like an acute stroke, but the random serum glucose of 4.2 mmol/L is "
                "below the elderly reference range of 4.6-6.4 mmol/L -- the client is hypoglycemic, "
                "and severe hypoglycemia is a well-known stroke mimic. The nurse should insert a "
                "peripheral VAD and request an order for IV 50% dextrose, the direct treatment for "
                "symptomatic hypoglycemia; administering oxygen and obtaining a urine specimen (for "
                "a possible UTI) or an oral corticosteroid (for Bell's palsy) do not address the "
                "actual cause. Neurologic status should be monitored, since resolution of the "
                "deficits as glucose is corrected confirms hypoglycemia was the cause rather than a "
                "stroke; serum glucose level should be monitored directly to confirm response to "
                "treatment. Urine output, temperature, and ECG rhythm are reasonable general "
                "parameters but are not the 2 most specific to this condition."
            ),
            "bowtieParams": [
                opt("urine output", False),
                opt("temperature", False),
                opt("neurologic status", True),
                opt("serum glucose level", True),
                opt("electrocardiogram (ECG) rhythm", False),
            ],
            "bowtieActions": [
                opt("Administer oxygen at 2 L/min via nasal cannula.", False),
                opt("Request a prescription for an oral corticosteroid.", False),
                opt("Insert a peripheral venous access device (VAD).", True),
                opt("Obtain a urine specimen for urinalysis and culture and sensitivity (C & S).", False),
                opt("Request an order for 50% dextrose in water to be administered intravenously.", True),
            ],
            "bowtieCol1Header": "Actions to Take",
            "bowtieCol2Header": "Potential Conditions",
            "bowtieCol3Header": "Parameters to Monitor",
            "bowtieConditions": [
                opt("Bell's palsy", False),
                opt("hypoglycemia", True),
                opt("ischemic stroke", False),
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
    out_path = os.path.join(DRAFTS_DIR, "case_1789577787012_FIXED_NURS_1017_Unit_11_Bowtie_1.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(item, f, indent=2, ensure_ascii=False)
    print("wrote", out_path)
