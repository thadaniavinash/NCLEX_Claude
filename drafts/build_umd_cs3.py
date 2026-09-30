"""University of Maryland - CS3: Acute respiratory failure (medical-surgical faculty case study).

Converted from "Acute Respiratory Distress DOCX" (medical-surgical) in the Maryland Next Gen NCLEX Test Bank
Project, University of Maryland School of Nursing,
https://www.nursing.umaryland.edu/mnwc/initiatives/nextgen-nclex/nextgen-nclex-library/
(Faculty case studies; author Kadriyya Clark, DNP, RN, CNE, Community College of Baltimore County;
September 1, 2022). The document's stand-alone "Trend Template" is the same question as screen 6, so it is
not added separately.

Changes from the source (flag for clinician review):
- Laboratory values in SI units with the author's reference ranges converted (mEq/L -> mmol/L; magnesium
  1.5 mEq/L -> 0.75 mmol/L; cell counts x 10^9/L); blood gases stay in mm Hg (as MCC prints them).
- PEEP 5 "mmHg" -> 5 cm H2O. Screen 1 option "PCO2 50 mm Hg" -> 51 mm Hg (the value in the chart).
- Screen 5 answer key taken from the source's highlighted "Key" table (IV of 0.9% sodium chloride,
  midazolam, chest X-ray).
- Not changed but flagged: amoxicillin IVPB (no IV amoxicillin in Canada/US, and a narrow choice for
  gram-negative bacteremia); "gram-negative cocci" in the blood culture; SaO2 96% on the 0900 labs with
  PaO2 75 mm Hg; lactate 4.5 mmol/L is also an urgent (sepsis) finding but is not keyed on screen 1.

Usage: python3 drafts/build_umd_cs3.py
"""
import json
import os

CASE_ID = "case_1790776800002"
STAMP = "1790776800002"
TITLE = "University of Maryland - CS3"
SOURCE_URL = "https://www.nursing.umaryland.edu/mnwc/initiatives/nextgen-nclex/nextgen-nclex-library/"
FOOTNOTE = (
    "Taken from the Maryland Next Gen NCLEX Test Bank Project, University of Maryland School of Nursing: "
    "&ldquo;Acute Respiratory Distress&rdquo; medical-surgical faculty case study (Kadriyya Clark, DNP, RN, CNE, "
    f"Community College of Baltimore County, September 1, 2022). Available at {SOURCE_URL} (Faculty Case Studies). "
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


def lab(name, rng):
    return f"<b>{name}</b><br>{rng}"


# ---- Chart ----
N0900 = note("0900", (
    "Client was admitted to the ICU in respiratory distress after minimal response to high-flow oxygen for a pulse "
    "oximetry reading of 83% on room air. Crackles heard bilaterally in lower lobes with diminished breath sounds "
    "in right middle lobe; S1 S2 auscultated; bowel sounds positive in all 4 quadrants; skin warm, dry, and intact. "
    "VS: T 99.8&deg;F (37.7&deg;C); HR 110; RR 30; BP 168/90; pulse oximetry reading 87% on 100% non-rebreather "
    "mask; pain 0/10."))
N0930 = note("0930", (
    "Client was intubated with a #6 endotracheal tube and placed on assist-control mechanical ventilation, rate 14, "
    "PEEP 5 cm H<sub>2</sub>O, FiO<sub>2</sub> 60%. VS: T 99.8&deg;F (37.7&deg;C); HR 110; RR 14; BP 180/90; pulse "
    "oximetry reading 96% on FiO<sub>2</sub> 60%. Client is restless."))
N1000 = note("1000", (
    "Chest X-ray obtained. IV placed and midazolam given. ECG shows sinus tachycardia. VS: T 99.8&deg;F "
    "(37.7&deg;C); HR 100; RR 14; BP 150/70; pulse oximetry reading 93% on FiO<sub>2</sub> 60%; drowsy, &minus;1 "
    "on sedation scale."))


def labs(with_sao2):
    rows = [
        [lab("Arterial pH", "7.35&ndash;7.45"), "7.20"],
        [lab("PaO<sub>2</sub>", "75&ndash;100 mm Hg"), "75 mm Hg"],
        [lab("PaCO<sub>2</sub>", "35&ndash;45 mm Hg"), "51 mm Hg"],
    ]
    if with_sao2:
        rows.append([lab("SaO<sub>2</sub>", "95&ndash;100%"), "96%"])
    rows += [
        [lab("Bicarbonate (HCO<sub>3</sub><sup>&minus;</sup>)", "22&ndash;26 mmol/L"), "28 mmol/L"],
        [lab("White blood cell (WBC) count", "4.5&ndash;10.5 &times; 10<sup>9</sup>/L"), "35.0 &times; 10<sup>9</sup>/L"],
        [lab("Platelet count", "140&ndash;450 &times; 10<sup>9</sup>/L"), "250 &times; 10<sup>9</sup>/L"],
        [lab("Potassium", "3.5&ndash;5.0 mmol/L"), "4.0 mmol/L"],
        [lab("Sodium", "135&ndash;145 mmol/L"), "140 mmol/L"],
        [lab("Magnesium", "0.75&ndash;1.05 mmol/L"), "0.75 mmol/L"],
        [lab("Lactate", "0.5&ndash;2.2 mmol/L"), "4.5 mmol/L"],
        [lab("Blood culture", "Negative"), "Gram-negative cocci"],
        [lab("Urine culture", "Negative"), "Pending"],
        [lab("Sputum culture", "Negative"), "Pending"],
    ]
    return table(["Laboratory Test and Reference Range", "0900"], rows)


ORDER_ROWS = [
    ("Nursing", ["Insert urinary catheter", "Suction endotracheal tube as needed",
                 "Titrate oxygen to keep pulse oximetry reading at or above 95%"]),
    ("Medications", ["Start IV of 0.9% sodium chloride at 75 mL/hr", "Amoxicillin 500 mg IVPB every 12 hours",
                     "Midazolam 2&ndash;4 mg IV push every 1 hour as needed for agitation",
                     "Acetaminophen 650 mg per rectum every 8 hours as needed for T &gt; 100.8&deg;F (38.2&deg;C)"]),
    ("Monitoring", ["Perform 12-lead ECG", "Call for chest X-ray", "Blood gas in 30 minutes"]),
]
FIRST = {"Start IV of 0.9% sodium chloride at 75 mL/hr",
         "Midazolam 2&ndash;4 mg IV push every 1 hour as needed for agitation", "Call for chest X-ray"}


def orders_table(marked):
    rows = []
    for cat, items in ORDER_ROWS:
        cells = [(("{%s|correct}" % o) if o in FIRST else "{%s}" % o) if marked else o for o in items]
        rows.append([f"<b>{cat}</b>", "<br>".join(cells)])
    return table(["Category", "Orders"], rows)


def tabs(step):
    notes = N0900 + (N0930 if step >= 4 else "") + (N1000 if step >= 6 else "")
    t = [{"id": f"nn_{STAMP}", "title": "Nurses' Notes", "content": notes},
         {"id": f"labs_{STAMP}", "title": "Laboratory Results", "content": labs(step >= 5)}]
    if step >= 6:
        t.append({"id": f"orders_{STAMP}", "title": "Orders", "content": orders_table(False)})
    return t


INTRO = ("The nurse cares for a 78-year-old female client admitted to the medical intensive care unit in "
         "respiratory distress.")


def opts(*pairs):
    return [{"text": t, "correct": c} for t, c in pairs]


def screen(step, question):
    question.setdefault("preamble", "")
    question["footnote"] = FOOTNOTE
    return {"step": step, "leftContent": {"intro": INTRO, "tabs": tabs(step)}, "question": question}


screens = [
    # 1. Recognize cues
    screen(1, {
        "type": "select_n",
        "limit": 4,
        "stem": "Select the <b>4</b> findings that are <b>most</b> urgent.",
        "options": opts(("BP 168/90", False), ("WBC 35.0 × 10⁹/L", False), ("Lactate 4.5 mmol/L", False),
                        ("pH 7.20", True), ("PaCO₂ 51 mm Hg", True), ("PaO₂ 75 mm Hg", False),
                        ("Respiratory rate 30", True), ("Blood culture: gram-negative cocci", False),
                        ("Pulse oximetry reading 87%", True)),
        "explanation": ("The client has signs and symptoms of infection and respiratory failure. The most urgent "
                        "findings are related to respiratory failure: a pH of 7.20 indicating an acidic state, a "
                        "PaCO<sub>2</sub> above 50 mm Hg, tachypnea (RR 30), and a pulse oximetry reading of 87% on "
                        "high-flow oxygen. The blood pressure is elevated but is not yet critical."),
    }),
    # 2. Analyze cues
    screen(2, {
        "type": "matrix_mr",
        "stem": ("For each finding, click to specify if the finding is consistent with acute respiratory failure or "
                 "pneumonia. Each finding may support more than one condition."),
        "matrix": {"firstColumnHeader": "Finding", "columns": ["Acute Respiratory Failure", "Pneumonia"], "rows": [
            {"text": "Crackles in bilateral lower lobes", "correctIndex": 0, "correctIndices": [0, 1]},
            {"text": "Pulse oximetry reading 87% on 100% oxygen", "correctIndex": 0, "correctIndices": [0, 1]},
            {"text": "PaCO₂ 51 mm Hg", "correctIndex": 0, "correctIndices": [0]},
            {"text": "pH 7.20", "correctIndex": 0, "correctIndices": [0]},
        ]},
        "explanation": ("Bilateral crackles can be associated with both conditions and are common in respiratory "
                        "illnesses. A pulse oximetry reading of 87% indicates a low level of oxygen in the blood, which "
                        "can be caused by either condition.<br>A PaCO<sub>2</sub> of 51 mm Hg and a pH of 7.20 indicate "
                        "respiratory acidosis and are consistent with acute respiratory failure."),
    }),
    # 3. Prioritize hypotheses
    screen(3, {
        "type": "multiple_choice",
        "stem": "What does the nurse determine is the priority for this client's care?",
        "options": opts(("Administering corticosteroids to reduce inflammation", False),
                        ("Intubating for mechanical ventilation support", True),
                        ("Opening airways with aerosol treatments", False),
                        ("Treating infection with antibiotics", False)),
        "explanation": ("Acute respiratory failure is characterized by the lungs' inability to oxygenate properly. The "
                        "client has had a poor response to maximum supplemental oxygen and now needs mechanical "
                        "ventilation.<br>The respiratory failure was most likely caused by pneumonia; treating the "
                        "pneumonia should take place next. Aerosols and corticosteroids may be incorporated into the "
                        "treatment plan but are not as critical as intubation."),
    }),
    # 4. Generate solutions
    screen(4, {
        "type": "matrix_mc",
        "preamble": ("The nurse has reviewed the Nurses' Notes from 0930. The nurse plans care for the client after "
                     "beginning mechanical ventilation."),
        "stem": ("For each potential intervention, click to specify whether the intervention is indicated or not "
                 "indicated to include in the plan of care."),
        "matrix": {"firstColumnHeader": "Potential Intervention", "columns": ["Indicated", "Not Indicated"],
                   "rows": [{"text": t, "correctIndex": i, "correctIndices": [i]} for t, i in [
                       ("Administer sedatives", 0), ("Repeat chest X-ray", 0), ("Schedule suctioning every 2 hours", 1),
                       ("Administer amiodarone", 1), ("Administer IV antibiotics", 0),
                       ("Position supine with head midline", 1), ("Obtain an electrocardiogram (ECG)", 0)]]},
        "explanation": ("Most intubated clients require sedation to prevent them from fighting the ventilator. A chest "
                        "X-ray should be done after intubation to confirm endotracheal tube placement. Antibiotics are "
                        "indicated to fight infection. The client has tachycardia and an elevated blood pressure, which "
                        "makes obtaining an ECG important.<br>Suctioning can damage tracheal tissue and should be done "
                        "as needed, not on a schedule. Amiodarone, an antiarrhythmic, is not indicated because no "
                        "arrhythmia has been identified. Positioning the client supine is not indicated; semi-Fowler's "
                        "or prone positioning is best to help with postural drainage."),
    }),
    # 5. Take action
    screen(5, {
        "type": "highlight_2",
        "preamble": "The nurse has reviewed the Laboratory Results and receives orders.",
        "stem": "Click to highlight the <b>3</b> orders the nurse should implement <b>first</b>.",
        "maxCorrectSelections": 3,
        "highlightTabs": [{"id": f"ht_{STAMP}", "title": "Orders", "content": orders_table(True)}],
        "explanation": ("A chest X-ray is needed after intubation to confirm optimal endotracheal tube placement. The "
                        "client does not yet have venous access; this should be established immediately so medications "
                        "can be given. The BP and heart rate are significantly elevated, and the client is agitated; "
                        "sedation (midazolam) should be given to decrease agitation and the risk of self-extubation."
                        "<br>Next, an ECG can be done and antibiotics can be given. The oxygen level is above 95%, so "
                        "adjustments are not needed, and there is no indication that suctioning is needed. The blood "
                        "gas is not due yet. The urinary catheter can be placed after other treatments."),
    }),
    # 6. Evaluate outcomes
    screen(6, {
        "type": "matrix_mc",
        "preamble": ("The nurse has reviewed the Nurses' Notes from 1000 and the Orders. The nurse reassesses the "
                     "client at 1000 and compares the findings to 0930."),
        "stem": ("For each finding, click to specify if the finding indicates that the client's status has improved, "
                 "declined, or is unchanged."),
        "matrix": {"firstColumnHeader": "Finding", "columns": ["Improved", "Declined", "Unchanged"],
                   "rows": [{"text": t, "correctIndex": i, "correctIndices": [i]} for t, i in [
                       ("Heart rate", 0), ("Temperature", 2), ("Respiratory rate", 2), ("Blood pressure", 0),
                       ("Pulse oximetry reading", 1), ("Agitation", 0)]]},
        "explanation": ("The heart rate decreased from 110 to 100 and the blood pressure dropped from 180/90 to 150/70; "
                        "both indicate improvement. The client is drowsy, showing that the agitation has decreased."
                        "<br>The temperature and respiratory rate remain unchanged. The pulse oximetry reading has "
                        "declined slightly (96% to 93%); the nurse should assess the lung sounds to determine if "
                        "suctioning or ventilator changes are needed."),
    }),
]

case = {
    "id": CASE_ID,
    "title": TITLE,
    "course": "Others",
    "unit": "Others",
    "topic": "Others",
    "disorder": "Others",
    "description": ("Maryland Next Gen NCLEX Test Bank Project September 1, 2022; Author: Kadriyya Clark, DNP, RN, CNE, "
                    "Community College of Baltimore County. Acute respiratory failure (medical-surgical): a 78-year-old "
                    "client in the ICU with pneumonia progresses to intubation and mechanical ventilation."),
    "availability": "all",
    # Added hidden from students until the author has reviewed it (studio: Ready chip -> "Show to students").
    "draft": True,
    "screens": screens,
}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{CASE_ID}_University_of_Maryland_-_CS3.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(case, f, indent=2, ensure_ascii=False)
print("wrote", os.path.basename(out))
