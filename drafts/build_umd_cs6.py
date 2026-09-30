"""University of Maryland - CS6: Chest pain (ST-elevation myocardial infarction), with its stand-alone bow-tie.
Source: "Chest Pain (MI) DOCX" (medical-surgical); Kadriyya Clark, DNP, RN, CNE, Community College of Baltimore
County; September 1, 2022.
Usage: python3 drafts/build_umd_cs6.py
"""
from umd_common import *  # noqa: F401,F403

N = 6
S = f"{N:02d}"
AUTH = "Kadriyya Clark, DNP, RN, CNE, Community College of Baltimore County"
FN = footnote("Chest Pain (MI)", AUTH)
FN_B = footnote("Chest Pain (MI)", AUTH, kind="medical-surgical faculty case study, stand-alone bow-tie", si=False)

N1000_TEXT = (
    "60-year-old male client admitted to the emergency department with crushing sternal pain radiating down the left "
    "arm that is worse with walking. Pain began 2 hours ago while walking outside. Client also reports shortness of "
    "breath with activity. Reports taking a regular aspirin on the way to the hospital. VS: T 99&deg;F (37.2&deg;C); "
    "HR 110; RR 22; BP 160/90; pulse oximetry reading 93% on room air; chest pain 8/10. Weight reported as 280 lb "
    "(127 kg), BMI 35.")
N1000 = note("1000", N1000_TEXT + (
    " Started on unit chest pain protocol. Oxygen applied and nitroglycerin given. A peripheral IV line has been placed "
    "in the client&rsquo;s left arm. Morphine given. Labs drawn."))
N1025 = note("1025", "Orders received. Tenecteplase given.")
N1030 = note("1030", ("VS: T 99&deg;F (37.2&deg;C); HR 120; RR 22; BP 150/85; pulse oximetry reading 95% on 2 L/min "
                      "via nasal cannula; pain 6/10."))

DIAG = paras("<b>ECG:</b> sinus tachycardia, rate 110. ST-segment elevation in leads V3 and V4 (anterior leads).")
LABS = table(["Laboratory Test and Reference Range", "1000"], [
    [lab("Cholesterol, total", "Normal &lt; 5.2 mmol/L; borderline 5.2&ndash;6.2 mmol/L; high &ge; 6.2 mmol/L"),
     "6.5 mmol/L"],
    [lab("White blood cell (WBC) count", "4.5&ndash;10.5" + G9), "10.0" + G9],
    [lab("Platelet count", "140&ndash;450" + G9), "400" + G9],
    [lab("Potassium", "3.5&ndash;5.0 mmol/L"), "3.9 mmol/L"],
    [lab("Sodium", "135&ndash;145 mmol/L"), "140 mmol/L"],
    [lab("Magnesium", "0.75&ndash;1.05 mmol/L"), "0.75 mmol/L"],
    [lab("Troponin T", "0&ndash;40 ng/L"), "500 ng/L"],
    [lab("Creatine kinase MB (CK-MB)", "5&ndash;25 U/L"), "170 U/L"],
])
ORDERS = table(["Category", "Orders"], [[
    "<b>Medications</b>",
    "Enoxaparin 100 mg SC<br>Metoprolol 25 mg PO<br>Tenecteplase 50 mg IV<br>"
    "Morphine sulfate 2 mg IV every 15 minutes as needed for pain"]])


def tabs(step):
    t = [{"id": f"nn_umd{S}", "title": "Nurses' Notes", "content": N1000 + (N1025 + N1030 if step >= 6 else "")},
         {"id": f"dx_umd{S}", "title": "Diagnostic Results", "content": DIAG},
         {"id": f"labs_umd{S}", "title": "Laboratory Results", "content": LABS}]
    if step >= 5:
        t.append({"id": f"ord_umd{S}", "title": "Orders", "content": ORDERS})
    return t


INTRO = "The nurse cares for a 60-year-old male client admitted to the emergency department with chest pain."

screens = [
    (INTRO, tabs(1), {
        "type": "select_n", "limit": 2,
        "preamble": "The nurse reviews the diagnostic and laboratory findings.",
        "stem": "Select the <b>2</b> findings that are <b>most</b> significant.",
        "options": opts(("Cholesterol", 0), ("ECG", 1), ("Platelets", 0), ("White blood cell count", 0),
                        ("Troponin T", 1), ("Creatine kinase MB", 0)),
        "explanation": (
            "Sinus tachycardia with ST-segment elevation on the ECG indicates damage to the cardiac muscle and must be "
            "addressed immediately. An elevated troponin T is specific for myocardial injury.<br>Creatine kinase MB can "
            "be used as a test for myocardial cell death but is also found in other tissues, so it is not specific to "
            "the myocardium. The cholesterol is elevated but is not diagnostic of a myocardial infarction. The platelet "
            "and white blood cell counts are normal."),
    }),
    (INTRO, tabs(2), {
        "type": "matrix_mr",
        "stem": ("For each client finding, click to specify whether the finding is consistent with ST-elevation "
                 "myocardial infarction (STEMI), non-ST-elevation myocardial infarction (NSTEMI), or unstable angina. "
                 "Each finding may be consistent with more than one condition."),
        "matrix": matrix_mr("Client Finding", ["STEMI", "NSTEMI", "Unstable Angina"], [
            ("Elevated creatine kinase MB", [0, 1]), ("Crushing chest pain", [0, 1, 2]),
            ("ST elevation in leads V3 and V4", [0]), ("Elevated cholesterol", [0, 1, 2]), ("Obesity", [0, 1, 2]),
            ("Elevated troponin T", [0, 1])]),
        "explanation": (
            "Obesity, elevated cholesterol, and crushing chest pain are associated with all three acute coronary "
            "syndromes. Cardiac biomarkers (troponin, CK-MB) are elevated with myocardial infarction (STEMI and NSTEMI) "
            "but not with unstable angina.<br>ST elevation indicates significant cardiac damage and is the finding that "
            "defines an ST-elevation myocardial infarction (STEMI)."),
    }),
    (INTRO, tabs(3), {
        "type": "dyad",
        "stem": "Complete the following sentence by choosing from the lists of options.",
        "cloze": cloze("The nurse should recognize that the client is most likely experiencing a/an [[drop0]] caused by "
                       "coronary artery [[drop1]].",
                       [("non-ST-elevation myocardial infarction", 0), ("ST-elevation myocardial infarction", 1),
                        ("unstable angina", 0)],
                       [("blockage", 1), ("rupture", 0), ("spasm", 0)]),
        "explanation": (
            "The client&rsquo;s laboratory results and symptoms are congruent with a STEMI. A STEMI occurs when an "
            "unstable plaque in the wall of a coronary artery suddenly ruptures and a clot builds up over it. The clot "
            "totally blocks the artery, and the blood supply to that part of the heart is lost."),
    }),
    (INTRO, tabs(4), {
        "type": "matrix_mc",
        "preamble": "The client receives a diagnosis of ST-elevation myocardial infarction.",
        "stem": ("For each potential medication order, click to specify whether the medication is indicated or not "
                 "indicated to include in the plan of care."),
        "matrix": matrix("Potential Medication", ["Indicated", "Not Indicated"], [
            ("Analgesics", 0), ("Antibiotics", 1), ("Anticoagulants", 0), ("Beta blockers", 0), ("Fluid bolus", 1),
            ("Fibrinolytics", 0)]),
        "explanation": (
            "Acute care for a STEMI includes pain management, restoring perfusion, and limiting ischemic damage. "
            "Analgesics, typically morphine, are given for pain. Ischemia is limited by decreasing myocardial oxygen "
            "demand: beta blockers lower the heart rate and blood pressure. Reperfusion therapy can be medical or "
            "mechanical; medical therapy is a fibrinolytic to dissolve the clot blocking the artery, and anticoagulants "
            "prevent the obstruction from worsening.<br>A fluid bolus would increase the cardiac workload, and there is "
            "no evidence of infection requiring antibiotics."),
    }),
    (INTRO, tabs(5), {
        "type": "dyad",
        "preamble": "The nurse has reviewed the Orders.",
        "stem": "Complete the following sentence by choosing from the lists of options.",
        "cloze": cloze("The nurse should next give the [[drop0]], which should be given [[drop1]].",
                       [("enoxaparin 100 mg SC", 0), ("metoprolol 25 mg PO", 0), ("tenecteplase 50 mg IV", 1)],
                       [("immediately upon admission", 0), ("within 30 minutes of admission", 1),
                        ("within 90 minutes of admission", 0)]),
        "explanation": (
            "Tenecteplase is a tissue plasminogen activator that dissolves the clot blocking the coronary artery. When "
            "fibrinolysis is the reperfusion strategy for a STEMI, the standard of care is to give it within 30 minutes "
            "of arrival (door-to-needle time)."),
    }),
    (INTRO, tabs(6), {
        "type": "matrix_mc",
        "preamble": ("The nurse has reviewed the Nurses&rsquo; Notes from 1025 and 1030. The nurse reassesses the client "
                     "after initiating the chest pain protocol and giving tenecteplase."),
        "stem": ("For each finding, click to specify if the finding indicates that the client&rsquo;s status has "
                 "improved, declined, or is unchanged."),
        "matrix": matrix("Finding", ["Improved", "Declined", "Unchanged"], [
            ("Pulse", 1), ("Blood pressure", 0), ("Pulse oximetry reading", 0), ("Respiratory rate", 2), ("Pain", 0)]),
        "explanation": (
            "The blood pressure, pulse oximetry reading, and pain level have all improved after oxygen by nasal cannula, "
            "nitroglycerin, morphine, and tenecteplase.<br>The heart rate has increased (110 to 120), which could "
            "indicate the heart muscle attempting to pump more oxygenated blood to the tissues. The respiratory rate is "
            "unchanged."),
    }),
]

case = make_case(N, "", "", screens, FN)
case["description"] = ("Maryland Next Gen NCLEX Test Bank Project, September 1, 2022; Author: Kadriyya Clark, Community "
                       "College of Baltimore County. Chest pain (MI): a 60-year-old client with an anterior STEMI; the "
                       "nurse interprets the ECG and biomarkers, gives fibrinolytic therapy, and evaluates the response.")

bow = make_standalone(N, 1, "Bowtie", (
    "Stand-alone bow-tie for University of Maryland - CS6 (chest pain, myocardial infarction)."),
    "A 60-year-old male client is admitted to the emergency department with chest pain.",
    [{"id": f"nn_umd{S}b", "title": "Nurses' Notes", "content": note("1000", N1000_TEXT)}],
    dict({"type": "bowtie",
          "stem": ("Complete the diagram by dragging from the choices below to specify what condition the client is most "
                   "likely experiencing, 2 actions the nurse should take to address that condition, and 2 parameters "
                   "the nurse should monitor to assess the client&rsquo;s progress."),
          "explanation": (
              "The actions and monitoring for a client with acute coronary syndrome help determine the next steps in "
              "treatment. Oxygen and nitroglycerin improve oxygenation and dilate the vessels to improve blood flow to "
              "the heart muscle, and improving ischemic pain indicates improved perfusion. The pulse oximetry reading "
              "shows whether oxygenation is adequate.<br>Low-dose aspirin is not the dose used for a suspected "
              "myocardial infarction (a higher, chewable dose is given). Tenecteplase may be given for a STEMI, but "
              "only after the diagnosis is confirmed by ECG. A fluid bolus would increase the cardiac workload.")},
         **bowtie([("Administer sublingual nitroglycerin", 1), ("Administer low-dose aspirin", 0),
                   ("Administer a normal saline fluid bolus", 0), ("Administer oxygen", 1),
                   ("Administer tenecteplase", 0)],
                  [("Atrial fibrillation", 0), ("Cardiogenic shock", 0), ("Ischemic stroke", 0),
                   ("Myocardial infarction", 1)],
                  [("Pain", 1), ("Neuro checks", 0), ("Urinary output", 0), ("Pulse oximetry reading", 1),
                   ("Peripheral pulses", 0)])), FN_B)

NOTES = [
    "Screen 3 has NO answer key in the source. It was keyed as ST-elevation myocardial infarction + coronary artery "
    "\"blockage\" (the rationale ends with the clot causing total blockage of the artery), but the rationale also "
    "describes plaque \"rupture\". Please confirm blockage vs rupture.",
    "Oxygen: the case applies oxygen at SpO2 93% on room air, and the bow-tie keys \"Administer oxygen\" as a correct "
    "action (source rationale: SpO2 should be ≥ 95%). Current ACS guidelines (AHA/CCS) recommend oxygen only when "
    "SpO2 is < 90%. Consider revising the bow-tie key or the SpO2 value; the sentence about ≥ 95% was removed from "
    "the rationale.",
    "Bow-tie: \"Administer low-dose aspirin\" is keyed incorrect (source: aspirin should be given in higher doses). "
    "Chewable aspirin 160-325 mg is standard; the option wording may confuse students. Please review.",
    "Orders: enoxaparin 100 mg SC (client 127 kg; with fibrinolysis the usual regimen is 30 mg IV bolus + 1 mg/kg SC, "
    "max 100 mg for the first doses), tenecteplase 50 mg IV (weight ≥ 90 kg, correct), metoprolol 25 mg PO, morphine "
    "2 mg IV every 15 min PRN. Please review the enoxaparin order.",
    "Screen 5: \"within 30 minutes\" is the door-to-needle target for fibrinolysis; for an anterior STEMI, primary PCI "
    "within 90 minutes (door-to-balloon) is preferred when available. The question works as written; consider adding "
    "that the facility has no PCI capability.",
    "Screen 2: the row \"ECG changes\" now reads \"ST elevation in leads V3 and V4\" (NSTEMI and unstable angina can "
    "also show ECG changes, e.g. ST depression). CK-MB and troponin rows now say \"Elevated\".",
    "Labs in SI with the author's ranges: cholesterol 250 mg/dL → 6.5 mmol/L; magnesium 1.5 mEq/L → 0.75 mmol/L; "
    "troponin T 0.5 ng/mL → 500 ng/L (0-40); WBC/platelets × 10⁹/L; K+/Na+ mmol/L. CK-MB kept in U/L as in the "
    "source.",
    "Screen 1 options were reordered so a correct answer is not listed first.",
]

write([case, bow], N, "Chest Pain (MI)", "Chest-Pain-(MI).docx", NOTES)
