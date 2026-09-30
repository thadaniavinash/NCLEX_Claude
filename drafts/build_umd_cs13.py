"""University of Maryland - CS13: Heart failure (clinic exacerbation, medication-order error), with its bow-tie.
Source: "Heart Failure DOCX" (medical-surgical); Lisa Seldomridge, PhD, RN, CNE; Jennifer Hart, DNP, FNP-BC; Molly
Dale, DNP, FNP-BC; Salisbury University; January 25, 2023.
Usage: python3 drafts/build_umd_cs13.py
"""
from umd_common import *  # noqa: F401,F403

N = 13
S = f"{N:02d}"
AUTH = "Lisa Seldomridge, PhD, RN, CNE; Jennifer Hart, DNP, FNP-BC; Molly Dale, DNP, FNP-BC; Salisbury University"
FN = footnote("Heart Failure", AUTH, "January 25, 2023")
FN_B = footnote("Heart Failure", AUTH, "January 25, 2023", "medical-surgical faculty case study, stand-alone bow-tie",
                si=False)

D1_1000 = note("Day 1 1000", (
    "68-year-old male client presents for a routine clinic appointment. Reports &ldquo;tiring easily when out shopping "
    "or for walks&rdquo;; has been staying home reading and watching television. Reports difficulty sleeping and wakes "
    "with shortness of breath in the middle of the night. Reports an 8-lb (3.6-kg) weight gain over the past 2 weeks "
    "since the last appointment. States normal appetite. Denies chest pain and back pain. States he is "
    "&ldquo;anxious&rdquo; about his condition. No known allergies. Current medications: enalapril 20 mg PO twice a day, "
    "hydrochlorothiazide 25 mg PO twice a day, digoxin 0.125 mg PO once a day.<br><b>Assessment:</b> alert and oriented "
    "&times; 4, appears slightly anxious; HR regular at 102; 4+ pitting pedal and pretibial edema; respirations "
    "unlabored, crackles in bases bilaterally; abdomen soft, nontender, bowel sounds active; skin warm, dry, and intact; "
    "frequent urination of small amounts of clear yellow urine."))
D1_1030 = note("Day 1 1030", (
    "Order to discontinue digoxin and begin sacubitril/valsartan 49/51 mg PO daily, with a nutrition/dietitian "
    "consult. Begin low-sodium diet and fluid restriction to 1500 mL/24 hours; instructed to weigh himself daily and "
    "record. Return to clinic in 3 weeks for follow-up."))
D14_0830 = note("Day 14 0830", (
    "Client called the clinic to report a nagging cough, pink-tinged sputum, and difficulty &ldquo;catching&rdquo; his "
    "breath. States he is sleeping in a recliner because he cannot breathe when lying down in bed. His wife checked his "
    "pulse and it is 90. Reports lack of appetite, thirst, and getting up twice a night to urinate. States he is "
    "&ldquo;worried&rdquo; about his health. Advised client that worsening symptoms need immediate attention. Spoke with "
    "client&rsquo;s wife, who agreed to take him to the emergency department."))

VS = vitals(["Day 1 1000"], [("T", "37&deg;C (98.6&deg;F)"), ("P", "102"), ("RR", "22"), ("BP", "170/100"),
                             ("Pulse oximetry reading", "93% on room air"), ("Weight", "97.7 kg (215 lb)")])
LABS = table(["Laboratory Test and Reference Range", "Day 1"], [
    [lab("Cholesterol, total", "Normal &lt; 5.2 mmol/L; borderline 5.2&ndash;6.2 mmol/L; high &ge; 6.2 mmol/L"),
     "6.4 mmol/L"],
    [lab("Urea (BUN)", "3.6&ndash;7.1 mmol/L"), "3.6 mmol/L"],
    [lab("Creatinine", "80&ndash;124 &micro;mol/L"), "133 &micro;mol/L"],
    [lab("Hematocrit (Hct)", "Male: 0.42&ndash;0.52 L/L; Female: 0.35&ndash;0.47 L/L"), "0.346 L/L"],
    [lab("Hemoglobin (Hgb)", "Male: 130&ndash;180 g/L; Female: 120&ndash;160 g/L"), "135 g/L"],
    [lab("Potassium", "3.5&ndash;5.0 mmol/L"), "2.8 mmol/L"],
    [lab("Sodium", "135&ndash;145 mmol/L"), "135 mmol/L"],
    [lab("Chloride", "96&ndash;106 mmol/L"), "95 mmol/L"],
])


def tabs(step):
    t = [{"id": f"cn_umd{S}", "title": "Clinic Notes",
          "content": D1_1000 + (D1_1030 if step >= 5 else "") + (D14_0830 if step >= 6 else "")},
         {"id": f"vs_umd{S}", "title": "Vital Signs", "content": VS}]
    if step >= 3:
        t.append({"id": f"labs_umd{S}", "title": "Laboratory Results", "content": LABS})
    return t


INTRO = "The nurse cares for a 68-year-old male client who presents for a routine clinic appointment."

screens = [
    (INTRO, tabs(1), {
        "type": "select_n", "limit": 4,
        "stem": "Select the <b>4</b> findings that are <b>most</b> concerning.",
        "options": opts(("States he is anxious", 0), ("4+ pitting pedal and pretibial edema", 1),
                        ("Crackles in bilateral lung bases", 1), ("Frequent urination", 0), ("Appetite", 0),
                        ("Awakening at night with shortness of breath", 1), ("Weight gain", 1), ("Heart rate", 0)),
        "explanation": (
            "The client is showing signs of worsening heart failure (HF). Crackles in the lung bases, waking at night "
            "short of breath, and weight gain are associated with left-sided HF; lower-extremity edema is associated with "
            "right-sided HF but is still a concern.<br>Anxiety, appetite (reported as normal), and frequent urination are "
            "not priority concerns compared with the signs of worsening HF, and the heart rate is only slightly elevated."),
    }),
    (INTRO, tabs(2), {
        "type": "select_n", "limit": 2,
        "stem": "Select the <b>2</b> problems the client is at <b>most</b> risk for developing.",
        "options": opts(("Anemia", 0), ("Electrolyte imbalance", 1), ("Dehydration", 0), ("Heart attack", 0),
                        ("Fluid volume overload", 1), ("Diabetes mellitus", 0), ("Hyperkalemia", 0),
                        ("Thrombophlebitis", 0)),
        "explanation": (
            "The client has worsening heart failure and is at risk for fluid volume overload and for electrolyte "
            "imbalances from hemodilution. He also takes hydrochlorothiazide and may become hypokalemic if his diet does "
            "not include enough potassium.<br>He is at no or low risk for hyperkalemia, dehydration, anemia, heart "
            "attack, diabetes mellitus, and thrombophlebitis."),
    }),
    (INTRO, tabs(3), {
        "type": "multiple_choice",
        "preamble": "The nurse has reviewed the Laboratory Results.",
        "stem": "Which abnormal laboratory finding should the nurse address <b>first</b>?",
        "options": opts(("Cholesterol", 0), ("Potassium", 1), ("Hematocrit", 0), ("Creatinine", 0)),
        "explanation": (
            "The serum potassium must be addressed first: it is dangerously low and can precipitate digoxin "
            "toxicity.<br>The cholesterol is high but is not an urgent issue, and the hematocrit is slightly low, partly "
            "from hemodilution. The creatinine is slightly elevated, which bears watching but is not an urgent concern "
            "compared with the potassium level."),
    }),
    (INTRO, tabs(4), {
        "type": "select_all",
        "stem": "What should the nurse include in the teaching plan for this client? <b>Select all that apply.</b>",
        "options": opts(("Increase intake of oral fluids to stay hydrated.", 0),
                        ("Weigh yourself every day at the same time and in the same clothes.", 1),
                        ("Limit sodium in the diet to no more than 2 grams per day.", 1),
                        ("Immediately report a 1-lb (0.5-kg) weight gain in 1 day or 3 lb (1.4 kg) in 1 week.", 0),
                        ("Limit exercise and physical activity.", 0),
                        ("Take prescribed medication every day, even if feeling better.", 1),
                        ("Eat foods high in potassium.", 1)),
        "explanation": (
            "The client is having an exacerbation of heart failure and must be taught self-care: daily weights at the "
            "same time in the same clothes, limiting dietary sodium, adding potassium-rich foods, and taking medication "
            "as prescribed.<br>Increasing fluids would worsen the fluid overload. The usual teaching is to report a gain "
            "of 2&ndash;3 lb (1&ndash;1.5 kg) in a day or 5 lb (2.3 kg) in a week. Regular, tolerated activity is "
            "encouraged rather than limited."),
    }),
    (INTRO, tabs(5), {
        "type": "select_all",
        "preamble": "The nurse has reviewed the Clinic Notes from Day 1 1030.",
        "stem": ("Which actions should the nurse take in response to the change in the medical orders? <b>Select all that "
                 "apply.</b>"),
        "options": opts(("Instruct client to start the new medication today", 0), ("Question the new medication order", 1),
                        ("Educate client about stopping digoxin", 1),
                        ("Tell client to take an additional dose of diuretic today", 0),
                        ("Request that the provider order a potassium supplement", 1),
                        ("Ask the dietitian to meet with the client", 1), ("Determine if the client owns a scale", 1)),
        "explanation": (
            "The new order for sacubitril/valsartan should be questioned because the client is already taking enalapril: "
            "an ACE inhibitor must be stopped at least 36 hours before sacubitril/valsartan is started, because the "
            "combination can cause angioedema. The client needs education about stopping digoxin, a potassium supplement "
            "for the low potassium, a dietitian consultation about the fluid restriction and potassium-rich foods, and a "
            "scale for daily weights.<br>The client should not start the new medication until the order is clarified, "
            "and an extra diuretic dose is not ordered and would worsen the hypokalemia."),
    }),
    (INTRO, tabs(6), {
        "type": "matrix_mc",
        "preamble": ("The nurse has reviewed the Clinic Notes from Day 14 0830. On day 14, the nurse follows up with the "
                     "client."),
        "stem": ("For each finding, click to specify if the finding indicates that the client&rsquo;s status has "
                 "improved, worsened, or is unchanged from his condition at the clinic visit 2 weeks earlier."),
        "matrix": matrix("Finding", ["Improved", "Worsened", "Unchanged"], [
            ("Sleeping in recliner", 1), ("Nagging cough", 1), ("Pink-tinged sputum", 1), ("Difficulty catching breath", 1),
            ("Pulse", 0), ("Lack of appetite", 1), ("Getting up at night to urinate", 1), ("Thirst", 2)]),
        "explanation": (
            "A nagging cough, difficulty catching his breath, sleeping in a recliner (orthopnea), and pink-tinged sputum "
            "are signs of worsening left-sided HF that require immediate intervention. Lack of appetite and getting up at "
            "night to urinate also show that the heart failure is worsening.<br>The pulse is slightly improved (102 to 90) "
            "and within normal limits. Thirst is not related to the heart failure and is keyed as unchanged."),
    }),
]

case = make_case(N, "", "", screens, FN)
case["description"] = ("Maryland Next Gen NCLEX Test Bank Project, January 25, 2023; Authors: Lisa Seldomridge, Jennifer "
                       "Hart, Molly Dale, Salisbury University. Heart failure: a 68-year-old client in the clinic with "
                       "worsening HF and hypokalemia; a medication-order error (ACE inhibitor + ARNI), teaching, and "
                       "worsening symptoms 2 weeks later.")

B_NOTE = note("Day 1 1100", (
    "Client reports that his primary care provider sent him to the hospital after his follow-up appointment today "
    "because of a nagging cough, pink-tinged sputum, and difficulty &ldquo;catching&rdquo; his breath. States he is "
    "sleeping in a recliner because of difficulty breathing when lying down in bed. Reports lack of appetite, thirst, "
    "and getting up twice a night to urinate. States feeling &ldquo;worried&rdquo; about his health. No known drug "
    "allergies."))
B_HP = table(None, [["<b>Cardiac</b>", "Regular rhythm, tachycardia; 4+ pitting pedal and pretibial edema"],
                    ["<b>Respiratory</b>", "Unlabored; crackles in bases bilaterally"],
                    ["<b>Neurologic</b>", "Oriented to time, place, person, and situation; anxious"],
                    ["<b>Gastrointestinal</b>", "Abdomen soft, nontender; bowel sounds active"],
                    ["<b>Skin</b>", "Warm, dry, intact"],
                    ["<b>Genitourinary</b>", "Frequent urination, small amounts, clear yellow, no foul odor"]])
B_VS = vitals(["1100"], [("T", "37&deg;C (98.6&deg;F)"), ("P", "110"), ("RR", "22"), ("BP", "170/110"),
                         ("Pulse oximetry reading", "93% on room air"), ("Weight", "97.7 kg (215 lb)")])
bow = make_standalone(N, 1, "Bowtie", "Stand-alone bow-tie for University of Maryland - CS13 (heart failure).",
                      ("The nurse is caring for a 68-year-old client who is admitted to the medical unit from an outpatient "
                       "clinic."),
                      [{"id": f"cn_umd{S}b", "title": "Admission Notes", "content": B_NOTE},
                       {"id": f"hp_umd{S}b", "title": "History and Physical", "content": B_HP},
                       {"id": f"vs_umd{S}b", "title": "Vital Signs", "content": B_VS}],
                      dict({"type": "bowtie",
                            "stem": ("Complete the diagram by dragging from the choices below to specify what condition "
                                     "the client is most likely experiencing, 2 actions the nurse should take to address "
                                     "that condition, and 2 parameters the nurse should monitor to assess the "
                                     "client&rsquo;s progress."),
                            "explanation": (
                                "A nagging cough, pink-tinged sputum, and orthopnea are symptoms of worsening heart "
                                "failure. Appropriate actions are an IV diuretic and a fluid restriction, and weight and "
                                "lung sounds show whether the interventions are effective.<br>There is no indication of "
                                "infection, so IV antibiotics and WBC monitoring are not appropriate. Normal saline is "
                                "contraindicated because of the fluid overload. A Foley catheter is not indicated because "
                                "the client is voiding. The pulse oximetry reading and heart sounds are stable.")},
                           **bowtie([("Administer IV diuretic", 1), ("Place Foley catheter", 0),
                                     ("Administer IV antibiotic", 0), ("Place client on fluid restriction", 1),
                                     ("Administer normal saline at 100 mL/hr", 0)],
                                    [("COPD exacerbation", 0), ("Pneumonia", 0), ("Urinary tract infection", 0),
                                     ("Heart failure", 1)],
                                    [("WBC count", 0), ("Weight", 1), ("Pulse oximetry reading", 0), ("Heart sounds", 0),
                                     ("Lung sounds", 1)])), FN_B)

NOTES = [
    "Home medications: hydrochlorothiazide 25 mg PO TWICE a day (usually once daily; a loop diuretic is more typical "
    "for HF with this degree of fluid overload). Please review.",
    "Screen 5 key: questioning sacubitril/valsartan with enalapril is correct (ARNI + ACE inhibitor contraindicated; "
    "36-hour washout). The rationale now states the reason (angioedema risk) and why an extra diuretic dose and "
    "starting today are wrong.",
    "Screen 3 rationale said the creatinine was \"within normal limits\"; it is above the range (1.5 mg/dL = 133 µmol/L "
    "vs 80-124). Rationale corrected to \"slightly elevated\".",
    "Labs: Hct 34.6% with Hgb 13.5 g/dL is physiologically inconsistent (Hgb normal, Hct low). Consider Hgb ~11.5 g/dL "
    "(115 g/L) or Hct ~40%.",
    "Screen 2 was a two-blank drag-and-drop where either order is correct; the app scores blanks by position, so it is "
    "a Select 2 question here (same options and key).",
    "Screen 4: weight units shown in lb and kg; a sentence was added giving the usual reporting threshold (2-3 lb/day "
    "or 5 lb/week) to explain why the 1-lb option is keyed incorrect.",
    "Screen 6: thirst is keyed Unchanged although the Day 1 note does not mention thirst; consider rewording the row.",
    "Labs in SI with the author's ranges: cholesterol 248 mg/dL → 6.4 mmol/L; BUN 10 mg/dL → urea 3.6 mmol/L; "
    "creatinine 1.5 mg/dL → 133 µmol/L; Hct 0.346 L/L; Hgb 135 g/L; K+/Na+/Cl- mmol/L.",
    "Screen 3, 4 and 5 options were reordered so a correct answer is not listed first.",
]

write([case, bow], N, "Heart Failure", "Heart-Failure.docx", NOTES)
