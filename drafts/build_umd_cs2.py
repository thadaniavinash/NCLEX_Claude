"""University of Maryland - CS2: Tuberculosis (medical-surgical faculty case study).

Converted from "Tuberculosis DOCX" (medical-surgical) in the Maryland Next Gen NCLEX Test Bank Project,
University of Maryland School of Nursing, https://www.nursing.umaryland.edu/mnwc/initiatives/nextgen-nclex/nextgen-nclex-library/
(Faculty case studies; author Elizabeth Mackessy-Lloyd, DNP, RN, CNE, Hood University; September 1, 2022).

Changes from the source (flag for clinician review):
- Laboratory values are shown in SI units (Canada); the author's reference ranges are converted, not
  replaced, so every question keys as written.
- Isoniazid order: the source lists 1000 mg PO daily, above the 300 mg maximum daily dose; shown as
  300 mg PO daily (the dose used in the 4-month rifapentine-moxifloxacin regimen).
- Answer keys and rationales are the author's (light punctuation only). The source's stand-alone trend
  question is the separate item drafts/build_umd_cs2_trend.py (University of Maryland - CS2 Trend).
- Option and matrix-row labels are plain text in the player (no HTML or entities): quotes are “ ” characters.

Usage: python3 drafts/build_umd_cs2.py  ->  drafts/case_1790769567553_University_of_Maryland_-_CS2.json
"""
import json
import os

CASE_ID = "case_1790769567553"
STAMP = "1790769567553"
TITLE = "University of Maryland - CS2"
SOURCE_URL = "https://www.nursing.umaryland.edu/mnwc/initiatives/nextgen-nclex/nextgen-nclex-library/"

FOOTNOTE = (
    "Taken from the Maryland Next Gen NCLEX Test Bank Project, University of Maryland School of Nursing: "
    "&ldquo;Tuberculosis&rdquo; medical-surgical faculty case study (Elizabeth Mackessy-Lloyd, DNP, RN, CNE, "
    f"Hood University, September 1, 2022). Available at {SOURCE_URL} (Faculty Case Studies). "
    "Laboratory values shown in SI units."
)

TH = 'border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;'
TD = 'border:1px solid #ccd8e0; padding:8px; min-width:80px; background:white; color:#1e293b;'


def note(time, text):
    return (f'<p class="nurse-note-row"><span class="nurse-note-time">{time}:</span>'
            f'<span class="nurse-note-text">{text}</span></p>')


def table(header, rows):
    head = "".join(f'<th style="{TH}">{h}</th>' for h in header)
    body = "".join("<tr>" + "".join(f'<td style="{TD}">{c}</td>' for c in r) + "</tr>" for r in rows)
    return (f'<table class="nclex-editor-table" style="width:100%; border-collapse:collapse; margin:12px 0;">'
            f"<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>")


# ---- Chart ----
NOTE_1000 = note("1000", (
    "Reports recent extended travel to Asia with a tour group. History of coughing, mild fatigue, and loss "
    "of appetite since return, 3 weeks ago. Complains of pain in chest of 4/10 on coughing. Reports taking an "
    "over-the-counter cough medication with limited results.<br>"
    "VS: BP 120/76 sitting, 118/72 standing, HR 78 beats per minute and regular, T 100&deg;F (37.8&deg;C) "
    "orally, RR 20, pulse oximetry reading 95% on room air. Lung sounds are diminished bilaterally with mild "
    "crackles noted in the bases. Weight 210 lb (95 kg), BMI 30."))
NOTE_1100 = note("1100", "Chest X-ray and bloodwork done.")

HOME_MEDS = ("<p>Hydrochlorothiazide 50 mg PO once daily for hypertension</p>"
             "<p>Atorvastatin 40 mg PO once daily for hyperlipidemia</p>"
             "<p>Almotriptan 12.5 mg PO as needed for migraine headache</p>")


def lab(name, rng):
    return f"<b>{name}</b><br>{rng}"


LABS = table(
    ["Laboratory Test and Reference Range", "1100"],
    [
        [lab("White blood cell (WBC) count", "5.0&ndash;10.0 &times; 10<sup>9</sup>/L"), "12.0 &times; 10<sup>9</sup>/L"],
        [lab("Platelet count", "150&ndash;400 &times; 10<sup>9</sup>/L"), "358 &times; 10<sup>9</sup>/L"],
        [lab("Hemoglobin (Hgb)", "115&ndash;155 g/L"), "108 g/L"],
        [lab("Hematocrit (Hct)", "0.36&ndash;0.48 L/L"), "0.35 L/L"],
        [lab("Hemoglobin A1c (HbA1c)", "&lt; 5.7%"), "6.0%"],
        [lab("Cholesterol, total", "&lt; 5.2 mmol/L"), "5.7 mmol/L"],
        [lab("Aspartate aminotransferase (AST)", "9&ndash;32 U/L"), "30 U/L"],
        [lab("Alanine aminotransferase (ALT)", "19&ndash;25 U/L"), "21 U/L"],
        [lab("Sputum culture", "Negative"), "Pending"],
    ]) + table(
    ["Diagnostic Study", "1100"],
    [["<b>Chest X-ray</b>", "Moderate bilateral pleural effusion"]])

ORDERS = ("<p>Rifapentine 1200 mg PO daily</p>"
          "<p>Moxifloxacin 400 mg PO daily</p>"
          "<p>Isoniazid 300 mg PO daily</p>"
          "<p>Pyrazinamide 2000 mg PO daily</p>")

PROGRESS = ("<p>Client returns for a follow-up appointment 4 weeks after being diagnosed with a tuberculosis "
            "infection. Reports missing several doses of medication. Continues to have a productive cough and is "
            "tired most days. Lung sounds clear with few scattered crackles. Rates pain with the cough at 3/10. "
            "VS: T 98.8&deg;F (37.1&deg;C), P 80, RR 22, BP 144/88, pulse oximetry reading 95% on room air. "
            "Repeat WBC 9.0 &times; 10<sup>9</sup>/L. Chest X-ray shows mild pleural effusion in the right base.</p>")


def tabs(screen):
    t = [{"id": f"nn_{STAMP}", "title": "Nurses' Notes", "content": NOTE_1000 + (NOTE_1100 if screen >= 3 else "")},
         {"id": f"meds_{STAMP}", "title": "Home Medications", "content": HOME_MEDS}]
    if screen >= 3:
        t.append({"id": f"labs_{STAMP}", "title": "Laboratory and Diagnostic Results", "content": LABS})
    if screen >= 4:
        t.append({"id": f"orders_{STAMP}", "title": "Orders", "content": ORDERS})
    if screen >= 6:
        t.append({"id": f"progress_{STAMP}", "title": "Progress Notes", "content": PROGRESS})
    return t


INTRO_CLINIC = ("A 48-year-old female client presents to the outpatient clinic in response to contact tracing for "
                "possible tuberculosis exposure.")
INTRO_5 = ("A 48-year-old female client presented to the outpatient clinic in response to contact tracing for "
           "possible tuberculosis exposure and was found to be symptomatic.")
INTRO_6 = "A 48-year-old female client with tuberculosis is seen in the clinic at a 4-week follow-up appointment."


def opts(*pairs):
    return [{"text": t, "correct": c} for t, c in pairs]


def matrix(first, columns, rows):
    return {"firstColumnHeader": first, "columns": columns,
            "rows": [{"text": t, "correctIndex": i, "correctIndices": [i]} for t, i in rows]}


def screen(step, intro, question):
    question.setdefault("preamble", "")
    question["footnote"] = FOOTNOTE
    return {"step": step, "leftContent": {"intro": intro, "tabs": tabs(step)}, "question": question}


screens = [
    # 1. Recognize cues
    screen(1, INTRO_CLINIC, {
        "type": "select_n",
        "limit": 3,
        "stem": "Select the <b>3</b> assessment findings that are <b>most</b> concerning at this time.",
        "options": opts(("Blood pressure", False), ("Lung sounds", True), ("Temperature", True), ("Heart rate", False),
                        ("Pain in chest", True), ("Respirations", False), ("Pulse oximetry reading", False)),
        "explanation": ("Lung sounds (diminished bilaterally with crackles in the bases), the elevated temperature, and "
                        "the complaint of chest pain with coughing are all indicative of respiratory alterations "
                        "consistent with tuberculosis."),
    }),
    # 2. Analyze cues
    screen(2, INTRO_CLINIC, {
        "type": "matrix_mc",
        "stem": ("For each assessment finding, click to specify if the finding is a risk factor or is not a risk "
                 "factor for tuberculosis infection."),
        "matrix": matrix("Assessment Finding", ["Risk Factor", "Not a Risk Factor"], [
            ("Client is overweight", 1), ("Medication list", 1), ("Recent travel to Asia", 0),
            ("Extended travel with a group", 0), ("Temperature", 0), ("Blood pressure", 1),
            ("Cough", 0), ("Pain characteristics", 0)]),
        "explanation": ("Asia is a high-risk area for tuberculosis, and living in close quarters with others (extended "
                        "travel with a tour group) is a risk factor, as are the elevated temperature, cough, and "
                        "complaints of chest pain.<br>Being overweight, the home medication list, and the blood "
                        "pressure are not risk factors for tuberculosis infection."),
    }),
    # 3. Prioritize hypotheses
    screen(3, INTRO_CLINIC, {
        "type": "drag_drop_cloze",
        "preamble": ("The nurse has reviewed the Nurses' Notes from 1100 and the Laboratory and Diagnostic "
                     "Results."),
        "stem": ("Drag the most appropriate word choice from the list of options to complete the following "
                 "sentence."),
        "cloze": {
            "text": "The nurse should recognize that the client's priority problem to address at this time is [[drop0]].",
            "dropdowns": [{"placeholder": "Select...", "options": opts(
                ("Ineffective airway clearance", False), ("Impaired gas exchange", False),
                ("Alteration in tissue perfusion", False), ("Risk for spreading infection", True),
                ("Pain secondary to coughing", False))}],
        },
        "explanation": ("In prioritizing the client's needs, airway clearance is not the issue, and there is no "
                        "evidence of decreased tissue perfusion. There is evidence of mildly altered gas exchange "
                        "(the borderline low pulse oximetry reading and the auscultated lung congestion), but the "
                        "risk of spreading the infection to others is the priority concern at this time."),
    }),
    # 4. Generate solutions
    screen(4, INTRO_CLINIC, {
        "type": "matrix_mc",
        "preamble": ("The client is diagnosed with a tuberculosis infection, and orders for new medications are "
                     "received. The nurse has reviewed the Orders."),
        "stem": ("For each potential nursing intervention, click to specify whether the intervention is appropriate "
                 "or not appropriate to include in the plan of care."),
        "matrix": matrix("Potential Nursing Intervention", ["Appropriate", "Not Appropriate"], [
            ("Implement a fluid restriction while taking tuberculosis medication", 1),
            ("Initiate a 24-hour urine collection", 1),
            ("Instruct the client to wear a mask when around others for the next 3 weeks", 0),
            ("Teach coughing and deep breathing techniques", 0),
            ("Alert the client's family that she has tuberculosis", 1),
            ("Encourage a high-carbohydrate diet", 1),
            ("Withhold opioid pain medication", 1),
            ("Apply an N95 face mask", 0)]),
        "explanation": ("An N95 respirator protects the nurse from airborne transmission of tuberculosis. Coughing "
                        "and deep breathing is an important nursing intervention for this client, and the client "
                        "should be encouraged to wear a face mask around others for at least the first 3 weeks of "
                        "treatment.<br>While contact tracing would be done for close contacts, the nurse would not "
                        "reveal the client's identity. The other interventions are not appropriate for this client."),
    }),
    # 5. Take action
    screen(5, INTRO_5, {
        "type": "matrix_mc",
        "stem": ("For each client teaching point, click to specify whether the information needs to be provided "
                 "immediately, at the time of client follow-up, or is not indicated for this client."),
        "matrix": matrix("Client Teaching Point", ["Immediately", "On Return Visit", "Not Indicated"], [
            ("“Your cholesterol is high, and we need to discuss your diet.”", 1),
            ("“You will need to take the medications every day for at least 4 months.”", 0),
            ("“If you continue to cough at home, please save all of your sputum.”", 2),
            ("“You will need to have regular labs to check the effects of this medication on your liver.”", 0),
            ("“Try to pace your activities to preserve your energy.”", 0),
            ("“Tuberculosis is not spread by germs on dishes or linens.”", 0),
            ("“Your A1C is high, and you may have diabetes.”", 1)]),
        "explanation": ("Teaching about the medication schedule and length of treatment, liver monitoring, energy "
                        "conservation, and how tuberculosis is (and is not) spread is needed immediately.<br>"
                        "The cholesterol is high and the A1C is elevated but in the prediabetes range. These should "
                        "be addressed at the follow-up visit, when the client may be more able to receive "
                        "information unrelated to the presenting problem.<br>There is no need to collect sputum "
                        "at home since the antibiotics have already been started."),
    }),
    # 6. Evaluate outcomes
    screen(6, INTRO_6, {
        "type": "dyad",
        "preamble": "The nurse has reviewed the Progress Notes.",
        "stem": "Complete the following sentence by choosing from the lists of options.",
        "cloze": {
            "text": "The nurse determines the client's status is [[drop0]]. The nurse should now [[drop1]].",
            "dropdowns": [
                {"placeholder": "Select...", "options": opts(("deteriorating", False), ("improving", True), ("unchanged", False))},
                {"placeholder": "Select...", "options": opts(("discharge the client home", False),
                                                             ("review medication teaching", True),
                                                             ("admit the client for observation", False))},
            ],
        },
        "explanation": ("The client's symptoms are improving: the chest X-ray has improved, the lung sounds have "
                        "improved, the temperature is normal, and the WBC count is within normal limits. However, the "
                        "client is not adhering strictly to the medication schedule and needs medication teaching "
                        "before being sent home."),
    }),
]

case = {
    "id": CASE_ID,
    "title": TITLE,
    "course": "Others",
    "unit": "Others",
    "topic": "Others",
    "disorder": "Others",
    "description": ("Maryland Next Gen NCLEX Test Bank Project September 1, 2022; Author: Elizabeth Mackessy-Lloyd, "
                    "DNP, RN, CNE, Hood University. Tuberculosis (medical-surgical): contact tracing, diagnosis, "
                    "infection control, medication teaching, and 4-week follow-up."),
    "availability": "all",
    # Added hidden from students until the author has reviewed it (studio: Ready chip -> "Show to students").
    "draft": True,
    "screens": screens,
}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{CASE_ID}_University_of_Maryland_-_CS2.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(case, f, indent=2, ensure_ascii=False)
print("wrote", os.path.relpath(out, os.path.dirname(os.path.dirname(out))))
