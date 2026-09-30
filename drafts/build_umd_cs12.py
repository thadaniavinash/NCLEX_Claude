"""University of Maryland - CS12: Gastroesophageal reflux disease, with its stand-alone bow-tie.
Source: "Gastroesphageal Reflux DOCX" (medical-surgical); Tara Sohrabi, Nursing Professor, Montgomery College;
September 1, 2022. Screen 1's key comes from the source's highlighted Key passage.
Usage: python3 drafts/build_umd_cs12.py
"""
from umd_common import *  # noqa: F401,F403

N = 12
S = f"{N:02d}"
AUTH = "Tara Sohrabi, Nursing Professor, Montgomery College"
FN = footnote("Gastroesophageal Reflux Disease", AUTH)
FN_B = footnote("Gastroesophageal Reflux Disease", AUTH, kind="medical-surgical faculty case study, stand-alone bow-tie",
                si=False)

T0345 = ("The client is admitted to the emergency department with {E}, {N}. Client reports pain 6/10 that started "
         "2 hours after eating last night and has vomited 3 times before coming to the emergency department. Reports "
         "increased episodes of epigastric pain, {C}, and {K} over the last several months. The pain is keeping him "
         "awake at night. Client denies diarrhea, current chest pain, or shortness of breath. {V}, pulse oximetry "
         "reading 97% on room air.")
PLAIN = dict(E="epigastric pain", N="nausea and vomiting", C="intermittent chest pain", K="chronic cough",
             V="VS: T 37.1&deg;C (98.9&deg;F), P 90, RR 18, BP 130/86")
MARKED = dict(E="{epigastric pain|correct}", N="{nausea and vomiting|correct}", C="{intermittent chest pain}",
              K="{chronic cough}", V="{VS: T 37.1&deg;C (98.9&deg;F), P 90, RR 18, BP 130/86}")
N0345 = note("0345", T0345.format(**PLAIN))
N0415 = note("0415", ("IV line placed; 0.9% sodium chloride started at 100 mL/hr. Morphine 2 mg and ondansetron 4 mg "
                      "given IV. Labs drawn."))
N0445 = note("0445", ("Client reports pain 1/10. No nausea or vomiting. Taught client about diet, positioning after "
                      "eating, and weight management."))
PROGRESS = paras("Working diagnosis: probable gastroesophageal reflux disease.")
ORDERS = paras("1. Start 0.9% sodium chloride at 100 mL/hr.", "2. Administer morphine 2 mg IV STAT.",
               "3. Administer ondansetron 4 mg IV STAT.", "4. Blood panel for sodium and potassium.",
               "5. Educate client about lifestyle modifications.", "6. Schedule follow-up with gastroenterologist.")
LABS = table(["Laboratory Test and Reference Range", "0415"], [
    [lab("Potassium", "3.5&ndash;5.0 mmol/L"), "3.0 mmol/L"], [lab("Sodium", "135&ndash;145 mmol/L"), "133 mmol/L"]])


def tabs(step):
    t = [{"id": f"nn_umd{S}", "title": "Nurses' Notes",
          "content": N0345 + (N0415 if step >= 5 else "") + (N0445 if step >= 6 else "")}]
    if step >= 4:
        t.append({"id": f"pn_umd{S}", "title": "Progress Notes", "content": PROGRESS})
    if step >= 5:
        t += [{"id": f"ord_umd{S}", "title": "Orders", "content": ORDERS},
              {"id": f"labs_umd{S}", "title": "Laboratory Results", "content": LABS}]
    return t


INTRO = "The nurse cares for a 47-year-old client with nausea and vomiting in the emergency department."

screens = [
    (INTRO, tabs(1), {
        "type": "highlight",
        "stem": "Click to highlight the <b>2</b> findings that require <b>immediate</b> follow-up.",
        "maxCorrectSelections": 2,
        "highlightTabs": [{"id": f"ht_umd{S}", "title": "Nurses' Notes", "content": note("0345", T0345.format(**MARKED))}],
        "explanation": (
            "The client&rsquo;s epigastric pain and nausea and vomiting are acute and should be followed up "
            "immediately.<br>The client has no chest pain or shortness of breath now to indicate an immediate cardiac "
            "problem, and the vital signs are normal. The cough is chronic, whereas the vomiting and epigastric pain are "
            "acute."),
    }),
    (INTRO, tabs(2), {
        "type": "matrix_mr",
        "stem": ("For each finding, click to specify if the finding is most consistent with gastroesophageal reflux "
                 "disease, peptic ulcer, or cholecystitis. Each finding may support more than one condition."),
        "matrix": matrix_mr("Assessment Finding", ["Gastroesophageal Reflux Disease", "Peptic Ulcer", "Cholecystitis"], [
            ("Epigastric pain", [0, 1, 2]), ("Intermittent chest pain", [0, 2]), ("Vomiting", [0, 1, 2]),
            ("Cough", [0])]),
        "explanation": (
            "Epigastric pain and vomiting can be seen with all three problems. GERD and cholecystitis can cause chest pain "
            "that may mimic a heart attack.<br>GERD may cause a chronic cough after meals or when lying down at night."),
    }),
    (INTRO, tabs(3), {
        "type": "dropdown_cloze",
        "stem": "Complete the following sentence by choosing from the list of options.",
        "cloze": cloze("The nurse should recognize that the client is most likely experiencing [[drop0]].",
                       [("cholecystitis", 0), ("gastroesophageal reflux disease", 1), ("peptic ulcer", 0)]),
        "explanation": (
            "The client shows clinical manifestations of gastroesophageal reflux disease: epigastric pain and nausea and "
            "vomiting after eating, a chronic cough, pain that keeps him awake at night, and a history of intermittent "
            "chest pain."),
    }),
    (INTRO, tabs(4), {
        "type": "select_all",
        "preamble": ("The nurse has reviewed the Progress Notes. The provider makes a diagnosis of probable "
                     "gastroesophageal reflux disease."),
        "stem": "Which interventions should the nurse include in the plan of care? <b>Select all that apply.</b>",
        "options": opts(("Obtain stool culture", 0), ("Order CBC", 0),
                        ("Check lab report for sodium and potassium levels", 1), ("Administer antiemetics", 1),
                        ("Obtain abdominal CT scan", 0), ("Teach the client about health maintenance", 1),
                        ("Administer analgesics", 1)),
        "explanation": (
            "The client&rsquo;s pain, nausea, and vomiting should be treated, and the sodium and potassium levels "
            "monitored because vomiting can cause electrolyte imbalances. The client should be taught lifestyle changes, "
            "including weight management, eating the evening meal early, and not eating before going to bed.<br>The "
            "client has no diarrhea, so a stool culture is not needed, and a CBC and abdominal CT scan are not needed to "
            "manage probable GERD."),
    }),
    (INTRO, tabs(5), {
        "type": "select_all",
        "preamble": ("The nurse has reviewed the Nurses&rsquo; Notes from 0415, the Orders, and the Laboratory Results. "
                     "The nurse receives orders."),
        "stem": "Which modifications should the nurse include in the teaching plan? <b>Select all that apply.</b>",
        "options": opts(("Take aspirin for intermittent pain", 0), ("Avoid eating large meals", 1),
                        ("Avoid eating late at night", 1), ("Eat a low-fat diet", 1), ("Limit caffeinated beverages", 1),
                        ("Drink carbonated beverages for nausea", 0), ("Sleep on your right side", 0),
                        ("Maintain a healthy weight", 1)),
        "explanation": (
            "The client should avoid foods and drinks that trigger reflux, typically fatty foods and caffeinated and "
            "carbonated beverages. Small meals decrease pressure on the lower esophageal sphincter, and eating close to "
            "bedtime should be avoided. Maintaining a healthy weight and sleeping with the head of the bed elevated are "
            "recommended.<br>Aspirin is contraindicated because it irritates the lining of the esophagus and stomach. "
            "Sleeping on the right side tends to worsen reflux (the left side is preferred)."),
    }),
    (INTRO, tabs(6), {
        "type": "multiple_choice",
        "preamble": ("The nurse has reviewed the Nurses&rsquo; Notes from 0445. The nurse educates the client about "
                     "lifestyle management."),
        "stem": "The nurse determines that the dietary teaching was successful if the client chooses which food?",
        "options": opts(("Chocolate", 0), ("Coffee", 0), ("Nonfat milk", 1), ("Mint tea", 0)),
        "explanation": (
            "The client should avoid foods and drinks that trigger reflux. Common triggers include fatty or fried foods, "
            "tomato sauce, alcohol, chocolate, mint, garlic, onion, and caffeine. Nonfat milk is not a trigger."),
    }),
]

case = make_case(N, "", "", screens, FN)
case["description"] = ("Maryland Next Gen NCLEX Test Bank Project, September 1, 2022; Author: Tara Sohrabi, Montgomery "
                       "College. Gastroesophageal reflux disease: a 47-year-old client in the emergency department with "
                       "epigastric pain and vomiting; focused assessment, treatment, and lifestyle teaching.")

bow = make_standalone(N, 1, "Bowtie", "Stand-alone bow-tie for University of Maryland - CS12 (GERD).",
                      "The nurse cares for a 47-year-old client with epigastric pain and vomiting in the emergency department.",
                      [{"id": f"nn_umd{S}b", "title": "Nurses' Notes", "content": N0345}],
                      dict({"type": "bowtie",
                            "stem": ("Complete the diagram by dragging from the choices below to specify what condition "
                                     "the client is most likely experiencing, 2 actions the nurse should take to address "
                                     "that condition, and 2 parameters the nurse should monitor to assess the "
                                     "client&rsquo;s progress."),
                            "explanation": (
                                "The signs of GERD are epigastric pain and nausea and vomiting after eating, along with a "
                                "history of intermittent chest pain and chronic cough. The nurse administers an analgesic "
                                "to relieve the pain and an antiemetic to treat the nausea and vomiting, monitors the "
                                "nausea and vomiting to evaluate the medications, and monitors the electrolytes to find out "
                                "whether the vomiting has caused an imbalance.")},
                           **bowtie([("Administer analgesics", 1), ("Assess stomach pH", 0),
                                     ("Encourage lying on the right side", 0), ("Administer antiemetic", 1),
                                     ("Encourage intake of low-sodium diet", 0)],
                                    [("Peptic ulcer", 0), ("Gastroesophageal reflux disease", 1), ("Cholecystitis", 0),
                                     ("Esophageal cancer", 0)],
                                    [("Nausea and vomiting", 1), ("Blood pressure", 0), ("Stool for occult blood", 0),
                                     ("Electrolyte levels", 1), ("Hemoglobin level", 0)])), FN_B)

NOTES = [
    "Chest pain: a 47-year-old with intermittent chest pain and epigastric pain would normally have an ECG and troponin "
    "to rule out acute coronary syndrome before GERD is diagnosed. Screen 1 keys chest pain as not needing immediate "
    "follow-up. Consider adding \"ECG normal sinus rhythm; troponin negative\" to the chart so the reasoning holds.",
    "Orders: no acid suppression (PPI/H2 blocker or antacid) is ordered for probable GERD, morphine is the analgesic "
    "(opioids are not typical for GERD pain), and potassium 3.0 mmol/L has no replacement order. Please review the "
    "order set.",
    "Screen 3 rationale mentioned \"difficulty swallowing\", which is not in the chart; replaced with the charted "
    "findings.",
    "Screen 5: \"Sleep on your right side\" keyed incorrect; a sentence was added explaining that the left side is "
    "preferred (the source only mentioned elevating the head of the bed).",
    "Laboratory report: the source's sodium reference range reads \"145 mEq/L\"; shown as 135-145 mmol/L.",
    "Screen 1 is a highlight question (chart passage and question in the left panel); the key (epigastric pain; nausea "
    "and vomiting) comes from the source's highlighted Key passage. Students may select 2.",
    "Screen 5 options were reordered so a correct answer is not listed first.",
]

write([case, bow], N, "Gastroesophageal Reflux Disease", "Gastroesphageal-Reflux.docx", NOTES)
