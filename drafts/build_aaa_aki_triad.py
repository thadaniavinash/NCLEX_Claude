"""Converts a triad (3-blank dropdown cloze) item the user originally wrote in an earlier
version of this app into this app's data format: a 54-year-old client, 24 hours after an
abdominal aortic aneurysm (AAA) repair, developing acute kidney injury.

The user supplied the stem/preamble, the full Vital Signs table (0400/0800/1200), the Intake &
Output table, the Laboratory Results, the full 3-list answer-choice pool, and a complete
written rationale via screenshots. Per the user's instruction, no Nurses' Notes tab is included
(the source has none). This is the user's own original content, not sourced from the NCSBN
exam preview, so no NCSBN copyright footnote is added.
"""
import json
import os

DRAFTS_DIR = os.path.dirname(os.path.abspath(__file__))


def opt(text, correct):
    return {"text": text, "correct": correct}


def dropdown(*pairs):
    return {"placeholder": "Select...", "options": [opt(t, c) for t, c in pairs]}


VITALS_TAB = (
    '<table class="nclex-editor-table" style="width:100%; border-collapse:collapse; margin:12px 0;">'
    '<thead><tr><th style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;"></th>'
    '<th style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;">0400</th>'
    '<th style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;">0800</th>'
    '<th style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;">1200</th></tr></thead><tbody>'
    '<tr><td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;"><b>T</b></td>'
    '<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">37.6° C (99.8° F)</td>'
    '<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">37.5° C (99.6° F)</td>'
    '<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">37.3° C (99.2° F)</td></tr>'
    '<tr><td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;"><b>HR</b></td>'
    '<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">72 BPM</td>'
    '<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">80 BPM</td>'
    '<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">88 BPM</td></tr>'
    '<tr><td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;"><b>RR</b></td>'
    '<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">14 bpm</td>'
    '<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">16 bpm</td>'
    '<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">18 bpm</td></tr>'
    '<tr><td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;"><b>BP</b></td>'
    '<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">106/58 mm Hg</td>'
    '<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">126/78 mm Hg</td>'
    '<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">140/80 mm Hg</td></tr>'
    '<tr><td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;"><b>SpO<sub>2</sub> (RA)</b></td>'
    '<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">95%</td>'
    '<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">93%</td>'
    '<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">92%</td></tr>'
    '</tbody></table>'
)

IO_TAB = (
    '<table class="nclex-editor-table" style="width:100%; border-collapse:collapse; margin:12px 0;">'
    '<thead><tr><th style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;"></th>'
    '<th style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;">0400</th>'
    '<th style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;">0800</th>'
    '<th style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;">1200</th></tr></thead><tbody>'
    '<tr><td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;"><b>Intake oral</b></td>'
    '<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">120 mL</td>'
    '<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">150 mL</td>'
    '<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">90 mL</td></tr>'
    '<tr><td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;"><b>Intake IV</b></td>'
    '<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">300 mL</td>'
    '<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">300 mL</td>'
    '<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">300 mL</td></tr>'
    '<tr><td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;"><b>Output</b></td>'
    '<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">90 mL</td>'
    '<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">50 mL</td>'
    '<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">26 mL</td></tr>'
    '</tbody></table>'
)

LABS_TAB = (
    '<table class="nclex-editor-table" style="width:100%; border-collapse:collapse; margin:12px 0;">'
    '<thead><tr><th style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;"></th>'
    '<th style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;">Result</th>'
    '<th style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;">Reference Range</th></tr></thead><tbody>'
    '<tr><td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;"><b>Blood urea nitrogen (BUN)</b></td>'
    '<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">12.6 mmol/L (35 mg/dL) <span style="color:#c0392b; font-weight:600;">H</span></td>'
    '<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">3.6–7.1 mmol/L (10–20 mg/dL)</td></tr>'
    '<tr><td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;"><b>Creatinine (Cr)</b></td>'
    '<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">198 mcmol/L (1.8 mg/dL) <span style="color:#c0392b; font-weight:600;">H</span></td>'
    '<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">44–106 mcmol/L (0.4–1.2 mg/dL)</td></tr>'
    '</tbody></table>'
)

item = {
    "id": "standalone_1784070000007",
    "title": "Unit 7 Stand-alone 7: Triad - Acute Kidney Injury After AAA Repair",
    "unit": "Unit 7 (Urinary Disorders)",
    "course": "NURS 1021",
    "topic": "Unit 7 (Urinary Disorders)",
    "disorder": "Unit 7 (Urinary Disorders)",
    "isStandalone": True,
    "description": "A postoperative abdominal aortic aneurysm repair client develops acute kidney injury.",
    "screens": [{
        "step": 1,
        "question": {
            "stem": "Complete the following sentence by selecting from the 3 lists of options below. Based on the assessment data in the medical record, click to specify the <b>most likely</b> condition the client is experiencing and 2 assessment findings that <b>most</b> support that condition.",
            "type": "triad",
            "preamble": (
                "1300: The nurse reviews the medical record and morning laboratory results of a "
                "54-year-old client who had an abdominal aneurysm repair 24 hours ago. The "
                "client has an IV infusion at a rate of 75 mL/hr, unchanged for the last 12 "
                "hours."
            ),
            "cloze": {
                "text": "The client is most likely experiencing [[drop0]] as evidenced by [[drop1]] and [[drop2]].",
                "dropdowns": [
                    dropdown(
                        ("Hypoxia", False),
                        ("Bleeding", False),
                        ("Wound infection", False),
                        ("Acute kidney injury", True),
                    ),
                    dropdown(
                        ("Heart rate", False),
                        ("Urine output", True),
                        ("Temperature", False),
                        ("Respiratory rate", False),
                    ),
                    dropdown(
                        ("SpO2", False),
                        ("IV intake", False),
                        ("BUN and Cr", True),
                        ("Blood pressure", False),
                    ),
                ],
            },
            "explanation": (
                "All 4 conditions listed are complications the nurse would monitor for after "
                "this surgery, but the client's data most specifically point to acute kidney "
                "injury (AKI). Following abdominal aortic aneurysm repair, the kidneys are at "
                "risk from intraoperative blood loss and, depending on the aneurysm's location, "
                "temporary hypoperfusion of the renal arteries. The client's urine output has "
                "declined steadily across the shift (90 mL, then 50 mL, then only 26 mL) despite "
                "a steady IV infusion rate and ongoing oral intake, and the BUN (12.6 mmol/L / 35 "
                "mg/dL) and creatinine (198 mcmol/L / 1.8 mg/dL) are both elevated above their "
                "reference ranges. These findings support AKI, and the surgeon should be "
                "notified immediately. Hypoxia would be expected to present with restlessness, "
                "dyspnea, diaphoresis, tachycardia, hypertension, cyanosis, and a low pulse "
                "oximetry reading; although the blood pressure has risen and the pulse oximetry "
                "has dropped slightly (92% at 1200), neither change is marked enough, and no "
                "other finding supports hypoxia as the primary concern this far out from "
                "anesthesia (24 hours postoperative). Bleeding would be expected to present with "
                "restlessness, a weak and rapid pulse, hypotension, tachypnea, and cool, clammy "
                "skin; the client's pulse and blood pressure are trending up, not down, and only "
                "the declining urine output could be argued to fit, which is far better explained "
                "by AKI. Wound infection would be expected to present with fever, chills, and a "
                "warm, tender, painful, inflamed incision; the client's temperature has "
                "trended downward across the shift, and there is no documentation of chills or "
                "incisional findings."
            ),
        },
        "leftContent": {
            "tabs": [
                {"id": "vs_1784070000007", "title": "Vital Signs", "content": VITALS_TAB},
                {"id": "io_1784070000007", "title": "Intake & Output", "content": IO_TAB},
                {"id": "lab_1784070000007", "title": "Laboratory Results", "content": LABS_TAB},
            ],
            "intro": "The nurse is caring for a 54-year-old postoperative client.",
        },
    }],
    "availability": "all",
}

if __name__ == "__main__":
    path = os.path.join(DRAFTS_DIR, f"{item['id']}_Triad_AKI_After_AAA_Repair.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(item, f, indent=2, ensure_ascii=False)
    print("wrote", path)
