"""University of Maryland - CS9: COPD II (COPD exacerbation with pneumonia; discharge teaching), with its bow-tie.
Source: "COPD II DOCX" (medical-surgical); Mary DiBartolo, PhD, RN-BC, CNE, FGSA, FAAN, Salisbury University;
January 25, 2023.
Usage: python3 drafts/build_umd_cs9.py
"""
from umd_common import *  # noqa: F401,F403

N = 9
S = f"{N:02d}"
AUTH = "Mary DiBartolo, PhD, RN-BC, CNE, FGSA, FAAN, Salisbury University"
FN = footnote("COPD II", AUTH, "January 25, 2023")
FN_B = footnote("COPD II", AUTH, "January 25, 2023", "medical-surgical faculty case study, stand-alone bow-tie")

INFO = table(None, [["<b>Name</b>", "Roy Blue", "<b>Gender</b>", "Male"],
                    ["<b>Age</b>", "63", "<b>Weight</b>", "144 lb (65 kg)"],
                    ["<b>Allergies</b>", "Penicillin, aspirin, milk products", "", ""]])

D1_1300 = note("Day 1 1300", (
    "Admitted to the medical-surgical unit from the ED with moderate shortness of breath (SOB) and a productive cough "
    "of purulent, rust-colored sputum. History of emphysema and chronic bronchitis since age 42; former 2-pack-per-day "
    "smoker for 25 years (50 pack-years) who started smoking again approximately 6 months ago. Takes salmeterol/"
    "fluticasone 25/250 dry powder inhaler 1 inhalation every 12 hours and ipratropium metered-dose inhaler 2 puffs 4 "
    "times a day, as well as a &ldquo;pill for my high blood pressure, cholesterol, and reflux.&rdquo; States that until "
    "recently he has minimized the effects of his disease with his inhalers and proper rest and exercise. About a week "
    "ago he &ldquo;caught a cold,&rdquo; which worsened in the past 3 days; he started coughing up rust-colored sputum and "
    "running a low-grade fever. Appears weak and cachectic, with poor appetite, feeling too tired to eat. Mild clubbing "
    "noted in fingers. Has been unable to work at his job at a chemical factory for the past few months and is confined "
    "to home. Wants to start the pneumococcal vaccine series but has not felt up to leaving the house to get it.<br>"
    "VS: T 101.4&deg;F (38.5&deg;C), P 98, RR 28, BP 140/72, pulse oximetry reading 85% on 2 L/min oxygen. Labs obtained. "
    "Chest X-ray and sputum cultures pending."))
D1_1315_A = ("Chest X-ray results back. Provider notified of client status. Oxygen increased to 35% via Venturi mask.")
D1_1315 = note("Day 1 1315", D1_1315_A)
D1_1315_B = note("Day 1 1315", D1_1315_A + " Sputum cultures obtained.")
D1_1400 = note("Day 1 1400", "RR 21; pulse oximetry reading now 87%; reports mild SOB with exertion; resting "
                             "comfortably in bed.")
D2_0900 = note("Day 2 0900", (
    "T 98.8&deg;F (37.1&deg;C) after a dose of acetaminophen, two doses of IV antibiotic, and IV methylprednisolone. RR 18; "
    "pulse oximetry reading 92% on 2 L/min oxygen via nasal cannula. ABGs checked this morning. No reports of SOB; up in "
    "chair for breakfast. Ate 75% of breakfast. Orders to discharge this afternoon."))


def labs(day2):
    rows = [
        [lab("Potassium", "3.5&ndash;5.0 mmol/L"), "4.2 mmol/L", ""],
        [lab("Sodium", "135&ndash;145 mmol/L"), "144 mmol/L", ""],
        [lab("Glucose, fasting", "&lt; 5.5 mmol/L"), "4.3 mmol/L", ""],
        [lab("White blood cell (WBC) count", "4.5&ndash;10.5" + G9), "14.2" + G9, ""],
        [lab("Arterial pH", "7.35&ndash;7.45"), "7.31", "7.32"],
        [lab("PaO<sub>2</sub>", "75&ndash;100 mm Hg"), "72 mm Hg", "88 mm Hg"],
        [lab("PaCO<sub>2</sub>", "35&ndash;45 mm Hg"), "51 mm Hg", "50 mm Hg"],
        [lab("Bicarbonate (HCO<sub>3</sub><sup>&minus;</sup>)", "22&ndash;26 mmol/L"), "28 mmol/L", "26 mmol/L"],
    ]
    head = ["Laboratory Test and Reference Range", "Admission"] + (["Day 2"] if day2 else [])
    return table(head, [r if day2 else r[:2] for r in rows])


DIAG = paras("<b>Chest X-ray (Day 1):</b> left lower lobe pneumonia.")
DC = title("Discharge orders") + paras("Discharge this afternoon on home oxygen 2 L/min.", "Levofloxacin 500 mg PO daily.",
                                       "Prednisone 40 mg PO daily for 5 days.", "Roflumilast 500 mcg PO daily.")


def tabs(step):
    notes = D1_1300 + ((D1_1315 if step == 3 else D1_1315_B) if step >= 3 else "") + (D1_1400 + D2_0900 if step >= 5 else "")
    t = [{"id": f"info_umd{S}", "title": "Client Information", "content": INFO},
         {"id": f"nn_umd{S}", "title": "Nurses' Notes", "content": notes},
         {"id": f"labs_umd{S}", "title": "Laboratory Results", "content": labs(step >= 5)}]
    if step >= 3:
        t.append({"id": f"dx_umd{S}", "title": "Diagnostic Results", "content": DIAG})
    if step >= 5:
        t.append({"id": f"dc_umd{S}", "title": "Discharge Orders", "content": DC})
    return t


INTRO = ("A 63-year-old male client with a history of chronic obstructive pulmonary disease (COPD) is admitted to the "
         "medical-surgical unit with respiratory distress.")

screens = [
    (INTRO, tabs(1), {
        "type": "select_n", "limit": 3,
        "stem": "Select the <b>3</b> assessment findings that are <b>most</b> significant.",
        "options": opts(("Pulse 98", 0), ("Temperature 101.4°F (38.5°C)", 1), ("BP 140/72", 0),
                        ("Pulse oximetry reading 85%", 1), ("Poor appetite", 0), ("PaCO₂ 51 mm Hg", 0),
                        ("Productive cough of purulent sputum", 1), ("HCO₃⁻ 28 mmol/L", 0)),
        "explanation": (
            "Oxygenation is compromised by the COPD exacerbation, as shown by the pulse oximetry reading of 85%. A "
            "productive cough of purulent, rust-colored sputum with a fever indicates bacterial pneumonia, which "
            "interferes with gas exchange.<br>The BP and pulse are within normal limits. The PaCO<sub>2</sub> is expected "
            "to be slightly elevated with the chronic respiratory acidosis of COPD, with a slightly elevated "
            "HCO<sub>3</sub><sup>&minus;</sup> as the compensatory response. Poor appetite is not urgent and will likely "
            "improve once the infection resolves."),
    }),
    (INTRO, tabs(2), {
        "type": "matrix_mc",
        "stem": "For each finding, click to specify if the finding is associated or not associated with COPD.",
        "matrix": matrix("Assessment Finding", ["Associated with COPD", "Not Associated with COPD"], [
            ("Occupation", 0), ("Hypertension", 1), ("Pulse oximetry reading 85%", 0),
            ("50 pack-year smoking history", 0), ("Productive cough", 0), ("Clubbing in fingers", 0),
            ("PaCO₂ 51 mm Hg", 0), ("Vaccine status", 1)]),
        "explanation": (
            "His job at a chemical factory (inhaled irritants affecting lung function) and his smoking history are risk "
            "factors for COPD. The productive cough and low pulse oximetry reading are symptoms of his pneumonia and "
            "COPD exacerbation. Clubbing of the fingers is a sign of long-term hypoxia, and the PaCO<sub>2</sub> is "
            "elevated because of the chronic respiratory acidosis associated with COPD.<br>Vaccine status relates to his "
            "pneumonia risk, and hypertension is not a risk factor for COPD."),
    }),
    (INTRO, tabs(3), {
        "type": "drag_drop_cloze",
        "preamble": ("The nurse has reviewed the Nurses&rsquo; Notes from Day 1 1315 and the Diagnostic Results. The "
                     "chest X-ray results return, and the provider is notified of the client&rsquo;s status."),
        "stem": "Drag the most appropriate word choice from the list of options to fill in the blank of the following "
                "sentence.",
        "cloze": cloze("The top priority for this client is to [[drop0]].",
                       [("reduce temperature", 0), ("improve PaCO₂", 0), ("evaluate nutritional status and food intake", 0),
                        ("treat the pneumonia", 1), ("assess readiness to stop smoking", 0),
                        ("address vaccination status", 0)]),
        "explanation": (
            "The priority is to treat the pneumonia, the source of infection, which will in turn resolve the fever and "
            "improve the breathing status and pulse oximetry reading.<br>Nutrition, smoking, and vaccination status can "
            "be addressed later, once the client is stable. Although elevated, the temperature is not life-threatening."),
    }),
    (INTRO, tabs(4), {
        "type": "matrix_mc",
        "stem": ("For each potential nursing or collaborative intervention, click to specify whether the intervention is "
                 "appropriate or not appropriate to include in the plan of care."),
        "matrix": matrix("Potential Intervention", ["Appropriate", "Not Appropriate"], [
            ("Administer IV methylprednisolone", 0), ("Administer PO acetaminophen as needed for fever", 0),
            ("Administer oxygen to achieve pulse oximetry readings of at least 95%", 1),
            ("Encourage flutter valve or Acapella use every 2 hours", 0), ("Administer PO cough suppressant", 1),
            ("Administer IV ampicillin/sulbactam", 1), ("Restrict PO fluids", 1), ("Encourage pursed-lip breathing", 0),
            ("Monitor WBC count", 0), ("Encourage milk, ice cream, and cheese as sources of protein", 1)]),
        "explanation": (
            "IV corticosteroids reduce inflammation, and acetaminophen reduces the fever from the pneumonia. Pursed-lip "
            "breathing and the flutter valve or Acapella increase positive expiratory pressure and help mobilize "
            "secretions with vibration. Monitoring the WBC count shows whether the antibiotic treatment is effective.<br>"
            "The usual target pulse oximetry range for a client with COPD is 88&ndash;92%. Ampicillin/sulbactam contains a "
            "penicillin and is contraindicated by his allergy. A cough suppressant is contraindicated because the goal is "
            "to cough up purulent secretions, and restricting fluids would thicken them. Milk products are contraindicated "
            "by his allergy."),
    }),
    (INTRO, tabs(5), {
        "type": "select_all",
        "preamble": ("The nurse has reviewed the Nurses&rsquo; Notes from Day 1 1400 and Day 2 0900, the Day 2 Laboratory "
                     "Results, and the Discharge Orders. The nurse prepares the client for possible discharge."),
        "stem": ("What should the nurse teach the client about the treatment plan before discharge? <b>Select all that "
                 "apply.</b>"),
        "options": opts(("If feeling better (no SOB or fever), you can stop taking the prednisone.", 0),
                        ("Continue to increase fluid intake.", 1),
                        ("Continue the flutter valve or Acapella at least 3–4 times daily.", 1),
                        ("Increase oxygen to 5–6 L/minute whenever short of breath.", 0),
                        ("Obtain pneumococcal and influenza vaccines at the next provider visit.", 1),
                        ("Eat smaller, more frequent high-calorie, high-protein meals.", 1),
                        ("Avoid all exercise for at least 3 months.", 0), ("Consider strategies to stop smoking.", 1)),
        "explanation": (
            "Increased fluids reduce the viscosity and retention of secretions. The flutter valve or Acapella continues to "
            "optimize lung expansion and gas exchange and mobilize secretions. Pneumococcal and influenza vaccines prevent "
            "future infections and exacerbations. Smaller, more frequent meals optimize nutrition. Smoking cessation is "
            "essential.<br>The client should take the entire course of prednisone as prescribed. Oxygen is kept at the "
            "lowest flow that maintains a pulse oximetry reading of 88&ndash;92%. Some mild exercise as tolerated is "
            "important."),
    }),
    (INTRO, tabs(6), {
        "type": "matrix_mc",
        "preamble": "The nurse completes the discharge teaching.",
        "stem": ("For each client statement, click to specify whether the statement indicates an understanding or no "
                 "understanding of the discharge teaching provided."),
        "matrix": matrix("Client Statement", ["Understanding", "No Understanding"], [
            ("“I should take the prednisone in the morning with food.”", 0),
            ("“I can get back to my previous level of activity as I recover.”", 0),
            ("“I can stop taking the antibiotic now that I am feeling better.”", 1),
            ("“I should use a spacer with my metered-dose inhalers.”", 0),
            ("“I can continue to smoke, as the damage is already done.”", 1),
            ("“I should do pursed-lip breathing several times daily.”", 0),
            ("“I should avoid crowds during cold and flu season.”", 0)]),
        "explanation": (
            "Glucocorticoids are best taken in the morning to mimic the diurnal pattern, and with food to decrease GI "
            "upset. The client should resume activity as tolerated, use a spacer with metered-dose inhalers to optimize "
            "the dose received, continue pursed-lip breathing to prolong expiration and eliminate CO<sub>2</sub>, and "
            "avoid crowds during cold and flu season.<br>The client should take every dose of the antibiotic to clear the "
            "infection and prevent multidrug-resistant organisms, and should still attempt smoking cessation: it is never "
            "too late to quit and benefit."),
    }),
]

case = make_case(N, "", "", screens, FN)
case["description"] = ("Maryland Next Gen NCLEX Test Bank Project, January 25, 2023; Author: Mary DiBartolo, Salisbury "
                       "University. COPD II: a 63-year-old client with a COPD exacerbation and left lower lobe pneumonia; "
                       "risk factors, priorities, interventions, and discharge teaching.")

bow = make_standalone(N, 1, "Bowtie", "Stand-alone bow-tie for University of Maryland - CS9 (COPD II).",
                      "A 63-year-old male client is admitted to the medical-surgical unit with respiratory distress.",
                      [{"id": f"info_umd{S}b", "title": "Client Information", "content": INFO},
                       {"id": f"nn_umd{S}b", "title": "Nurses' Notes", "content": D1_1300},
                       {"id": f"labs_umd{S}b", "title": "Laboratory Results", "content": labs(False)}],
                      dict({"type": "bowtie",
                            "stem": ("Complete the diagram by dragging from the choices below to specify what condition "
                                     "the client is most likely experiencing, 2 actions the nurse should take to address "
                                     "that condition, and 2 parameters the nurse should monitor to assess the "
                                     "client&rsquo;s progress."),
                            "explanation": (
                                "The client is experiencing a COPD exacerbation caused by pneumonia, as shown by the "
                                "shortness of breath, productive cough of rust-colored sputum, fever, and elevated WBC "
                                "count. Treatment includes an IV glucocorticoid to reduce airway inflammation and an IV "
                                "antibiotic; the arterial blood gases and WBC count show the response.<br>The head of the "
                                "bed is not lowered for a client who is short of breath, and a cough suppressant is "
                                "contraindicated because secretions need to be expelled. There is no evidence of "
                                "pneumothorax, so a chest tube is not indicated.")},
                           **bowtie([("Administer cough suppressant", 0), ("Administer IV glucocorticoid", 1),
                                     ("Maintain client in supine position", 0), ("Administer IV antibiotic", 1),
                                     ("Assist with chest tube placement", 0)],
                                    [("Pulmonary edema", 0), ("Tension pneumothorax", 0), ("Exacerbation of COPD", 1),
                                     ("Pulmonary embolism", 0)],
                                    [("Blood pressure", 0), ("Arterial blood gases", 1), ("WBC count", 1),
                                     ("Hematocrit", 0), ("Daily chest X-rays", 0)])), FN_B)

NOTES = [
    "Discharge orders: levofloxacin 500 mg PO daily (community-acquired pneumonia is usually treated with 750 mg daily, "
    "or 500 mg in older regimens) and roflumilast 500 mcg PO daily (often started at 250 mcg for 4 weeks). Please review "
    "the antibiotic dose and duration (none given).",
    "Screen 2: the source row \"Pulse oximeter 87%\" was changed to 85% (the admission value in the chart; 87% appears "
    "only at 1400 on screen 5). Its rationale also listed \"dyslipidemia\" as a COPD risk factor, which is not a row and "
    "is not a recognized risk factor; that phrase was removed.",
    "Screen 2 keys clubbing as associated with COPD (as in CS8, clubbing is not typical of COPD alone). Please review.",
    "Home inhaler: the source says salmeterol/fluticasone \"250/25\"; the product is labelled fluticasone/salmeterol "
    "250/50 (Diskus) or salmeterol/fluticasone 25/250 (MDI). Written here as 25/250; please confirm.",
    "Client Information shows the name \"Roy Blue\" as in the source (fictional).",
    "Labs in SI with the author's ranges: glucose 78 mg/dL → 4.3 mmol/L (< 5.5); WBC 14.2 × 10⁹/L; HCO₃⁻, K+, Na+ in "
    "mmol/L; blood gases in mm Hg.",
    "Screen 1 and screen 5 options were reordered so a correct answer is not listed first.",
]

write([case, bow], N, "COPD II", "COPD-II.docx", NOTES)
