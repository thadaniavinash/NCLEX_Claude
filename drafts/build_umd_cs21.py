"""University of Maryland - CS21: Thyroid Storm, with its stand-alone bow-tie.
Source: "Thyroid Storm DOC" (medical-surgical); Suzana Jarquin, MSN, RN, CNEcl, Frederick Community College;
September 1, 2022, updated April 23, 2023. The .doc was read as plain text, which loses highlighting: the key of screen 5
(the 2 orders to implement first) is taken from its rationale (oxygen and the 12-lead ECG).
Usage: python3 drafts/build_umd_cs21.py
"""
from umd_common import *  # noqa: F401,F403

N = 21
S = f"{N:02d}"
AUTH = "Suzana Jarquin, MSN, RN, CNEcl, Frederick Community College"
DATE = "September 1, 2022; updated April 23, 2023"
FN = footnote("Thyroid Storm", AUTH, DATE)
FN_B = footnote("Thyroid Storm", AUTH, DATE, "medical-surgical faculty case study, stand-alone bow-tie")

N0900 = note("0900", (
    "Accompanied by spouse; reports being short of breath and having palpitations. Placed in an ED treatment room directly "
    "from triage. Alert and oriented &times; 4; appears restless, anxious, and fatigued. Skin flushed and hot to touch. "
    "Bilateral eye protrusion noted; client states this is not their baseline and that their eyes feel &ldquo;very "
    "dry.&rdquo; Lung sounds clear to auscultation; no cough, but intermittent and worsening dyspnea. Normal S1 and S2; "
    "bilateral pulses 2&ndash;3+. Hyperactive bowel sounds in all 4 quadrants. Reports no pain. Reports excessive hunger "
    "and thirst over the past week, unrelieved by oral intake, and an unexpected weight loss of about 4 kg (8 lb) over the "
    "past week."))
N0910 = note("0910", ("Assessed by the provider. IV line established; ordered blood work collected and sent to the "
                      "laboratory. Vital signs reassessed; fever is increasing."))
N0930 = note("0930", "Oxygen at 2 L/min applied. ECG obtained. Fluid bolus started. Acetaminophen given. Cooling blanket applied.")
N1000 = note("1000", "Thyroid studies returned with critically elevated serum T3 and T4. Order received for oral methimazole.")
N1100 = note("1100", (
    "Reassessed after cooling measures and administration of oral methimazole and acetaminophen as ordered. Sitting up on "
    "the stretcher; remains alert and cooperative but still very anxious."))

TIMES = ["0900", "0910", "1000", "1100"]
VS_ROWS = [
    ("T", "39.6&deg;C (103.2&deg;F)", "39.7&deg;C (103.5&deg;F)", "39.4&deg;C (103.0&deg;F)", "38.9&deg;C (102.0&deg;F)"),
    ("P", "137", "140", "136", "127"),
    ("RR", "28", "27", "26", "24"),
    ("BP", "152/98", "148/89", "146/89", "137/82"),
    ("Pulse Oximetry Reading (SpO<sub>2</sub>)", "97% on room air", "97% on room air", "97% on 2 L/min oxygen",
     "97% on 2 L/min oxygen"),
    ("Pain", "0/10", "0/10", "0/10", "0/10")]


def vs(cols):
    return vitals(TIMES[:cols], [r[:cols + 1] for r in VS_ROWS])


ORDER_TEXT = ["Admit to the hospital", "Apply cooling blanket and ice packs",
              "Acetaminophen 1 g PO &times; 1 dose now", "Artificial tears (drops) to both eyes",
              "Humidified oxygen at 2 L/min via nasal cannula", "12-lead ECG",
              "0.9% sodium chloride 1000 mL IV bolus"]
FIRST = {4, 5}
METHIMAZOLE = "Methimazole 20 mg PO every 8 hours"
ORDERS = paras(*[f"{i + 1}. {t}" for i, t in enumerate(ORDER_TEXT)])
ORDERS_6 = paras(*[f"{i + 1}. {t}" for i, t in enumerate(ORDER_TEXT + [METHIMAZOLE])])
ORDERS_MARKED = paras(*[f"{i + 1}. " + ("{%s|correct}" % t if i in FIRST else "{%s}" % t)
                        for i, t in enumerate(ORDER_TEXT)])
DIAG = paras("<b>12-lead ECG (0930):</b> sinus tachycardia.")
LABS = table(["Laboratory Test and Reference Range", "0910"], [
    [lab("White blood cells (WBC)", "4.5&ndash;10.5" + G9), "13" + G9],
    [lab("Potassium", "3.5&ndash;5.0 mmol/L"), "5.0 mmol/L"],
    [lab("Sodium", "135&ndash;145 mmol/L"), "142 mmol/L"],
    [lab("Thyroid-stimulating hormone (TSH)", "0.45&ndash;4.5 mU/L"), "0.27 mU/L"],
    [lab("Triiodothyronine (T3), total", "1.2&ndash;3.1 nmol/L"), "6.1 nmol/L"],
    [lab("Thyroxine (T4), total", "57&ndash;148 nmol/L"), "270 nmol/L"]])


def tabs(step):
    cols = 4 if step >= 6 else 2 if step >= 5 else 1
    notes = N0900 + (N0910 if step >= 5 else "") + (N0930 + N1000 + N1100 if step >= 6 else "")
    t = [{"id": f"nn_umd{S}", "title": "Nurses' Notes", "content": notes},
         {"id": f"vs_umd{S}", "title": "Vital Signs", "content": vs(cols)}]
    if step >= 5:
        t.append({"id": f"ord_umd{S}", "title": "Orders", "content": ORDERS_6 if step >= 6 else ORDERS})
    if step >= 6:
        t += [{"id": f"dx_umd{S}", "title": "Diagnostic Results", "content": DIAG},
              {"id": f"labs_umd{S}", "title": "Laboratory Results", "content": LABS}]
    return t


INTRO = ("A 32-year-old woman with a history of hyperthyroidism is brought to the emergency department by their "
         "spouse.")

screens = [
    (INTRO, tabs(1), {
        "type": "select_n",
        "limit": 4,
        "stem": "Which <b>4</b> client findings are <b>most urgent</b>?",
        "options": opts(("2–3+ pulse grade", 0), ("Dyspnea", 1), ("Tachycardia", 1), ("Hunger", 0),
                        ("Palpitations", 1), ("Thirst", 0), ("Fever", 1), ("Anxiety", 0),
                        ("Hyperactive bowel sounds", 0), ("Bilateral eye protrusion", 0)),
        "explanation": (
            "All of the findings are concerning, but the physiological findings of dyspnea, tachycardia, palpitations, "
            "and fever take precedence over the less acute findings of hunger, thirst, eye protrusion, and hyperactive "
            "bowel sounds. Anxiety is acute but not physiological.<br>The pulse strength is within normal limits. "
            "Hyperactive bowel sounds are not a normal finding but do not take priority over the most urgent findings."),
    }),
    (INTRO, tabs(2), {
        "type": "matrix_mc",
        "stem": ("For each assessment finding, click to specify whether the finding is helpful or not helpful in "
                 "determining if the client is experiencing a thyroid problem."),
        "matrix": matrix("Assessment Finding", ["Helpful", "Not Helpful"], [
            ("Fever", 0), ("Bilateral eye protrusion", 0), ("Lung sounds", 1), ("Anxiety level", 0),
            ("Palpitations", 0), ("Dyspnea", 0)]),
        "explanation": (
            "Fever, eye protrusion, palpitations, dyspnea, and increased anxiety are abnormal findings that help determine "
            "whether the client is experiencing a thyroid problem.<br>The lung sounds are clear, so this finding is "
            "unremarkable and does not help identify this endocrine disorder."),
    }),
    (INTRO, tabs(3), {
        "type": "drag_drop_cloze",
        "stem": "Drag the most appropriate choice from the list of options to fill in the blank of the following sentence.",
        "cloze": cloze("The nurse recognizes that the condition the client is most likely experiencing is [[drop0]].",
                       [("hypothyroidism", 0), ("thyroid storm", 1), ("adrenal insufficiency", 0),
                        ("Cushing’s syndrome", 0), ("myxedema", 0)]),
        "explanation": (
            "The client&rsquo;s clinical manifestations indicate a hypermetabolic state. With a history of "
            "hyperthyroidism and increasing anxiety, restlessness, fatigue, tachycardia, dyspnea, and hyperpyrexia, the "
            "client is most likely experiencing a thyroid storm."),
    }),
    (INTRO, tabs(4), {
        "type": "select_all",
        "preamble": "The client receives a working diagnosis of thyroid storm.",
        "stem": "Which of the following prescriptions should the nurse anticipate? <b>Select all that apply.</b>",
        "options": opts(("Oral acetylsalicylic acid", 0), ("Humidified oxygen via nasal cannula at 2 L/min", 1),
                        ("12-lead ECG", 1), ("Oral levothyroxine", 0), ("Oral acetaminophen", 1),
                        ("Cooling blanket", 1), ("Oral methimazole", 1)),
        "explanation": (
            "Humidified oxygen is given to treat the client&rsquo;s dyspnea. The hyperthermia must be treated: the nurse "
            "anticipates acetaminophen and a cooling blanket to lower the body temperature more rapidly. The client has "
            "palpitations and tachycardia, so a 12-lead ECG is needed to assess the cardiac rate and rhythm. An "
            "antithyroid medication such as methimazole is an expected therapy for thyroid storm.<br>Acetylsalicylic acid "
            "displaces thyroid hormones from their binding proteins and can worsen the hypermetabolic state. "
            "Levothyroxine would increase thyroid hormone levels."),
    }),
    (INTRO, tabs(5), {
        "type": "highlight_2",
        "preamble": "The nurse has reviewed the Nurses&rsquo; Notes from 0910, the Vital Signs, and the Orders.",
        "stem": "Click to highlight the <b>2</b> orders the nurse should implement <b>first</b>.",
        "maxCorrectSelections": 2,
        "highlightTabs": [{"id": f"ht_umd{S}", "title": "Orders", "content": ORDERS_MARKED}],
        "explanation": (
            "The client&rsquo;s airway, breathing, and circulation require priority intervention. Because the client is "
            "tachypneic and short of breath with palpitations, oxygen is started to support oxygenation of the heart while "
            "cardiac events are ruled out, and a 12-lead ECG is obtained to detect any life-threatening abnormality in "
            "cardiac conduction, rate, or rhythm.<br>The cooling blanket and fluid bolus can be started after the ECG. The "
            "acetaminophen can be given after the cooling blanket is applied because it takes longer to work. Artificial "
            "tears are a comfort measure given after the other interventions."),
    }),
    (INTRO, tabs(6), {
        "type": "matrix_mc",
        "preamble": ("The nurse has reviewed the Nurses&rsquo; Notes from 0930, 1000, and 1100, the Vital Signs from 1000 "
                     "and 1100, the Orders, the Diagnostic Results, and the Laboratory Results. The nurse administered "
                     "the oral acetaminophen and methimazole, placed the client on oxygen, and instituted cooling "
                     "measures, and now reassesses the client."),
        "stem": ("For each finding, click to specify if the finding indicates that the client&rsquo;s status has improved "
                 "or remains unchanged."),
        "matrix": matrix("Finding", ["Improved", "Unchanged"], [
            ("Temperature", 0), ("Anxiety level", 1), ("Respiratory rate", 0), ("Heart rate", 0), ("Oxygenation", 1),
            ("Pain level", 1)]),
        "explanation": (
            "The temperature, heart rate, and respiratory rate have all improved with humidified oxygen, acetaminophen, "
            "and cooling measures.<br>The client remains anxious because of the hypermetabolic state, and oxygenation is "
            "stable (unchanged) with an SpO<sub>2</sub> of 97%. The client has reported no pain."),
    }),
]

case = make_case(N, "", "", screens, FN)
case["description"] = ("Maryland Next Gen NCLEX Test Bank Project, September 1, 2022 (updated April 23, 2023); Author: "
                       "Suzana Jarquin, Frederick Community College. Thyroid storm: a 32-year-old client with "
                       "hyperthyroidism, fever, and tachycardia; recognizing thyroid storm, priority orders, and "
                       "evaluating the response to treatment.")

bow = make_standalone(N, 1, "Bowtie", "Stand-alone bow-tie for University of Maryland - CS21 (thyroid storm).", INTRO,
                      [{"id": f"nn_umd{S}b", "title": "Nurses' Notes", "content": N0900},
                       {"id": f"vs_umd{S}b", "title": "Vital Signs", "content": vs(1)},
                       {"id": f"labs_umd{S}b", "title": "Laboratory Results", "content": LABS}],
                      dict({"type": "bowtie",
                            "preamble": "The nurse reviews the client&rsquo;s laboratory results.",
                            "stem": ("Complete the diagram by dragging from the choices below to specify what condition "
                                     "the client is most likely experiencing, 2 actions the nurse should take to address "
                                     "that condition, and 2 parameters the nurse should monitor to assess the "
                                     "client&rsquo;s progress."),
                            "explanation": (
                                "The client is experiencing a thyroid storm, which requires an antithyroid medication such "
                                "as methimazole. To decrease the client&rsquo;s metabolic demands, the nurse promotes a "
                                "calm, restful environment; cooling measures and IV fluids are also needed. Body "
                                "temperature and serum thyroid levels are important parameters to monitor.<br>A warming "
                                "blanket, levothyroxine, and fluid restriction would worsen the client&rsquo;s condition. "
                                "Daily weights, the amount of sleep, and the WBC count are not effective ways to assess "
                                "this client&rsquo;s progress.")},
                           **bowtie([("Provide a warming blanket", 0), ("Administer methimazole", 1),
                                     ("Promote a calm, restful environment", 1), ("Administer levothyroxine sodium", 0),
                                     ("Initiate oral fluid restriction", 0)],
                                    [("Adrenal insufficiency", 0), ("Hypothyroidism", 0), ("Thyroid storm", 1),
                                     ("Myxedema crisis", 0)],
                                    [("White blood cells", 0), ("Body temperature", 1), ("Daily weights", 0),
                                     ("Thyroid levels", 1), ("Amount of sleep", 0)])), FN_B)

NOTES = [
    "Screen 5 answer key: the source .doc's highlighting could not be read, so the 2 orders to implement first were taken "
    "from the rationale (humidified oxygen and the 12-lead ECG). Please confirm.",
    "Oxygen is keyed as anticipated (screen 4) and as a first priority (screen 5) although SpO2 is 97% on room air; "
    "oxygen is not routinely indicated at that saturation. Consider lowering the SpO2 or re-keying.",
    "Treatment gaps: a beta-blocker (propranolol) is a cornerstone of thyroid storm treatment for the tachycardia and is not "
    "in the orders or options; propylthiouracil is often preferred to methimazole in thyroid storm (blocks T4-to-T3 "
    "conversion), and iodine and glucocorticoids are also usual. Consider adding propranolol to the orders/options.",
    "Screen 5 rationale said \"Now medication orders should be implemented within 60-90 minutes\"; removed (a STAT/now "
    "order is given promptly). The order \"Admission\" was written as \"Admit to the hospital\".",
    "Screen 6 asks about the laboratory report, which the source shows only in the bow-tie; the Laboratory Results (drawn at "
    "0910) and the ECG report were added to screen 6's chart.",
    "Labs in SI with the author's ranges: WBC 13 × 10⁹/L (4.5-10.5); K 5.0 mmol/L; Na 142 mmol/L; TSH 0.27 mU/L "
    "(0.45-4.5); total T3 400 ng/dL -> 6.1 nmol/L (80-200 ng/dL -> 1.2-3.1 nmol/L); T4 270 nmol/L (57-148). In thyroid "
    "storm TSH is usually suppressed (< 0.01 mU/L); 0.27 is only mildly low. Consider changing it.",
    "Screen 1 (\"What 4 client findings are most urgent?\") is a select-4 question; anxiety is keyed not urgent. Screen 1 "
    "and screen 4 options were reordered so a correct answer is not listed first.",
    "The source uses they/them for the client in the notes and \"female\" in the intro; kept as in the source.",
]

write([case, bow], N, "Thyroid Storm", "Thyroid-Storm.doc", NOTES)
