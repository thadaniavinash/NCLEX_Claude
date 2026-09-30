"""University of Maryland - CS16: Liver failure (cirrhosis with ascites and hepatic encephalopathy), with its bow-tie.
Source: "Liver Failure DOCX" (medical-surgical); Mary DiBartolo, PhD, RN-BC, CNE, FGSA, FAAN, Salisbury University;
September 1, 2022, revised April 17, 2023. Screen 5's key comes from the source's highlighted Key.
Usage: python3 drafts/build_umd_cs16.py
"""
from umd_common import *  # noqa: F401,F403

N = 16
S = f"{N:02d}"
AUTH = "Mary DiBartolo, PhD, RN-BC, CNE, FGSA, FAAN, Salisbury University"
DATE = "September 1, 2022; revised April 17, 2023"
FN = footnote("Liver Failure", AUTH, DATE)
FN_B = footnote("Liver Failure", AUTH, DATE, "medical-surgical faculty case study, stand-alone bow-tie")

D1_1000 = note("Day 1 1000", (
    "Admitted with ascites and confusion; oriented to person only. 25-year history of alcohol use disorder, mild "
    "hypertension, and gastroesophageal reflux disease. Drowsy and dozing off and on, mildly dyspneic, appears thin and "
    "malnourished; somewhat agitated when answering questions. States he has not had a drink in a few weeks; his sister, "
    "who accompanied him, reports a recent drinking binge a week ago. Placed on oxygen 2 L/min by nasal cannula. Bulging "
    "flanks and peripheral edema noted. Bloodwork sent to the lab. Admission weight 64.5 kg (142 lb)."))
D1_1400 = note("Day 1 1400", (
    "Remains alert at times but confused, mumbling off and on; mild hand flap (asterixis) noted. Moderately dyspneic on 2 "
    "L/min oxygen by nasal cannula, RR 26. Bulging flanks and prominent veins around the umbilicus noted; provider "
    "notified."))
D1_1700 = note("Day 1 1700", (
    "Pulse oximetry reading 93% on 4 L/min oxygen. Second dose of lactulose given; 2 large, loose brown stools since the "
    "first dose. Alert, coherent, and cooperative with assessment. Urine output 400 mL since 1400."))
D2_0900 = note("Day 2 0900", (
    "Pulse oximetry reading 95% on room air; no dyspnea. Alert and oriented &times; 3 with no signs of agitation. Urine "
    "clear yellow at 30&ndash;40 mL/hr since 0600. Weight 62.7 kg (138 lb); abdominal girth recorded. Morning medications "
    "(metoprolol and spironolactone) given. Ammonia level now 42 &micro;mol/L."))

VS_ROWS = [("T", "36.9&deg;C (98.4&deg;F)", "37&deg;C (98.6&deg;F)", "36.5&deg;C (97.8&deg;F)", "37&deg;C (98.6&deg;F)"),
           ("P", "85", "86", "88", "85"), ("RR", "22", "26", "18", "16"), ("BP", "142/72", "145/78", "139/72", "132/64"),
           ("Pulse oximetry reading", "92% on 2 L/min NC", "89% on 2 L/min NC", "93% on 4 L/min NC", "95% on room air"),
           ("Glasgow Coma Scale (3&ndash;15)", "12", "12", "14", "14"),
           ("Abdominal girth", "95 cm (37.5 in)", "", "", "88 cm (34.5 in)")]


def vs(cols):
    return vitals(["Day 1 1000", "Day 1 1400", "Day 1 1800", "Day 2 0800"][:cols], [r[:cols + 1] for r in VS_ROWS])


MEDS = table(["Medication", "Dose, Route, Frequency", "Time"], [["Metoprolol XL", "50 mg PO daily", "1000"]])


def labs(day2):
    rows = [[lab("Urea (BUN)", "3.6&ndash;7.1 mmol/L"), "7.9 mmol/L", ""],
            [lab("Glucose, fasting", "&lt; 5.5 mmol/L"), "3.9 mmol/L", ""],
            [lab("Ammonia", "6&ndash;47 &micro;mol/L"), "55 &micro;mol/L", "42 &micro;mol/L"],
            [lab("Albumin", "34&ndash;54 g/L"), "32 g/L", ""]]
    return table(["Laboratory Test and Reference Range", "Day 1"] + (["Day 2"] if day2 else []),
                 [r if day2 else r[:2] for r in rows])


ORDER_TEXT = ["VS, pulse oximetry, and neuro assessment every 4 hours and as needed", "Low-sodium diet",
              "Record weight and abdominal girth daily",
              "Oxygen per nasal cannula to maintain pulse oximetry reading at 95% or greater",
              "IV normal saline at 30 mL/hr", "Lactulose 30 mL PO every 4 hours &times; 3 doses", "Furosemide 20 mg IV",
              "Spironolactone 100 mg PO daily"]
FIRST = {3, 5, 6}
ORDERS = paras(*[f"{i + 1}. {t}" for i, t in enumerate(ORDER_TEXT)])
ORDERS_MARKED = paras(*[f"{i + 1}. " + ("{%s|correct}" % t if i in FIRST else "{%s}" % t) for i, t in enumerate(ORDER_TEXT)])


def tabs(step):
    notes = D1_1000 + (D1_1400 if step >= 4 else "") + (D1_1700 + D2_0900 if step >= 6 else "")
    t = [{"id": f"nn_umd{S}", "title": "Nurses' Notes", "content": notes},
         {"id": f"vs_umd{S}", "title": "Vital Signs", "content": vs(4 if step >= 6 else 2 if step >= 4 else 1)},
         {"id": f"meds_umd{S}", "title": "Medications", "content": MEDS},
         {"id": f"labs_umd{S}", "title": "Laboratory Results", "content": labs(step >= 6)}]
    if step >= 6:
        t.append({"id": f"ord_umd{S}", "title": "Orders", "content": ORDERS})
    return t


INTRO = ("The nurse is caring for a 67-year-old male client with a history of alcohol use disorder and cirrhosis "
         "admitted to the medical-surgical unit.")

screens = [
    (INTRO, tabs(1), {
        "type": "select_n", "limit": 2,
        "preamble": "The nurse assesses the client on admission to the unit.",
        "stem": "Select the <b>2</b> findings that are <b>most</b> concerning.",
        "options": opts(("Blood pressure", 0), ("Urea (BUN)", 0), ("Neurologic assessment", 1), ("Peripheral edema", 0),
                        ("Dyspnea", 1), ("Albumin level", 0), ("Glucose", 0)),
        "explanation": (
            "The most concerning findings are the dyspnea, from ascites pressing on the diaphragm and limiting lung "
            "expansion, and the decline in neurologic function (drowsy and dozing off and on, oriented to person only, "
            "agitated).<br>The BUN is slightly elevated, likely from dehydration. A low serum albumin is expected with "
            "cirrhosis and the malnutrition of alcohol use disorder. The blood pressure is only mildly elevated."),
    }),
    (INTRO, tabs(2), {
        "type": "matrix_mc",
        "stem": "For each finding, click to specify if the finding is most consistent with ascites or an elevated ammonia level.",
        "matrix": matrix("Assessment Finding", ["Ascites", "Elevated Ammonia"], [
            ("Abdominal girth", 0), ("Agitation", 1), ("Bulging flanks", 0), ("Dozing off and on", 1), ("Dyspnea", 0),
            ("Peripheral edema", 0), ("Pulse oximetry reading", 0), ("Serum albumin", 0)]),
        "explanation": (
            "Ascites, a complication of portal hypertension and the low albumin of cirrhosis, increases the abdominal "
            "girth, causes bulging flanks and peripheral edema, and can compromise breathing (dyspnea, a low pulse "
            "oximetry reading).<br>The deterioration in neurologic status (drowsiness and agitation) results from the "
            "increased ammonia level causing hepatic encephalopathy."),
    }),
    (INTRO, tabs(3), {
        "type": "dyad",
        "stem": "Complete the following sentence by choosing from the lists of options.",
        "cloze": cloze("The client is most likely experiencing [[drop0]], as evidenced by the [[drop1]].",
                       [("esophageal varices", 0), ("hepatorenal failure", 0), ("hepatic encephalopathy", 1),
                        ("acute cholecystitis", 0)],
                       [("vital signs", 0), ("neurologic assessment", 1), ("respiratory assessment", 0),
                        ("glucose level", 0)]),
        "explanation": (
            "Hepatic encephalopathy is a common complication of cirrhosis caused by the liver&rsquo;s inability to "
            "detoxify protein by-products. The resulting increase in ammonia is toxic to the central nervous system. "
            "Abnormal neurologic findings such as confusion, lethargy, dozing off and on, restlessness, and agitation are "
            "common indicators."),
    }),
    (INTRO, tabs(4), {
        "type": "matrix_mc",
        "preamble": ("The nurse has reviewed the Nurses&rsquo; Notes and Vital Signs from Day 1 1400. The client receives "
                     "the diagnosis of hepatic encephalopathy."),
        "stem": ("For each potential intervention, click to specify whether the intervention is indicated, not indicated, "
                 "or contraindicated in the plan of care."),
        "matrix": matrix("Potential Intervention", ["Indicated", "Not Indicated", "Contraindicated"], [
            ("Neuro assessment every 4 hours", 0), ("Record abdominal girth daily", 0),
            ("Administer acetaminophen 650 mg as needed for temperature above 101°F (38.3°C)", 2),
            ("Monitor pulse oximetry every 4 hours", 0), ("Administer sedative as needed for agitation", 2),
            ("Daily weights", 0), ("Supine position when in bed", 2), ("Low-sodium diet", 0),
            ("Point-of-care glucose every 6 hours", 1), ("Lactulose 30 mL every 4 hours × 3 doses", 0)]),
        "explanation": (
            "Interventions focus on treating both the ascites and the hepatic encephalopathy: neuro assessments, pulse "
            "oximetry, daily weights and abdominal girth, a low-sodium diet, and lactulose to lower the ammonia level."
            "<br>Acetaminophen (metabolized by the liver) and sedatives are contraindicated, as is placing the client "
            "flat in bed when he is dyspneic from ascites. Glucose monitoring would not harm the client but is not "
            "necessary."),
    }),
    (INTRO, tabs(5), {
        "type": "highlight_2",
        "preamble": "At 1430, the provider assesses the client, reviews the chart, and writes orders.",
        "stem": "Click to highlight the <b>3</b> orders that the nurse should implement <b>immediately</b>.",
        "maxCorrectSelections": 3,
        "highlightTabs": [{"id": f"ht_umd{S}", "title": "Orders", "content": ORDERS_MARKED}],
        "explanation": (
            "The priorities are to reduce the ammonia level with the first dose of lactulose, to promote prompt diuresis "
            "of the excess fluid with IV furosemide, and to improve oxygenation by increasing the oxygen to keep the pulse "
            "oximetry reading at 95% or greater.<br>The other orders (routine assessments, diet, daily weight and girth, "
            "the IV, and the daily spironolactone) are carried out as scheduled."),
    }),
    (INTRO, tabs(6), {
        "type": "dyad",
        "preamble": ("The nurse has reviewed the Nurses&rsquo; Notes from Day 1 1700 and Day 2 0900, the Vital Signs from "
                     "Day 1 1800 and Day 2 0800, the Day 2 Laboratory Results, and the Orders. On the second day, the "
                     "nurse reviews the morning vital signs, urine output, and updated ammonia level."),
        "stem": "Complete the following sentences by choosing from the lists of options.",
        "cloze": cloze("The nurse determines the client&rsquo;s status is [[drop0]]. The nurse should now [[drop1]].",
                       [("improving", 1), ("deteriorating", 0), ("unchanged", 0)],
                       [("request an order for more lactulose", 0), ("apply restraints", 0),
                        ("explore readiness to stop drinking", 1)]),
        "explanation": (
            "The client&rsquo;s overall condition has improved. IV furosemide and sodium restriction reduced the ascites "
            "(weight and abdominal girth down, no dyspnea, pulse oximetry reading 95% on room air), and the ammonia level "
            "and neurologic status improved after the lactulose.<br>Now that the client is alert and oriented, the nurse "
            "can explore his readiness to stop drinking. More lactulose is not needed, and restraints are not indicated."),
    }),
]

case = make_case(N, "", "", screens, FN)
case["description"] = ("Maryland Next Gen NCLEX Test Bank Project, September 1, 2022 (revised April 17, 2023); Author: Mary "
                       "DiBartolo, Salisbury University. Liver failure: a 67-year-old client with alcohol use disorder, "
                       "cirrhosis, ascites, and hepatic encephalopathy; priorities, orders, and response to lactulose and "
                       "diuretics.")

bow = make_standalone(N, 1, "Bowtie", "Stand-alone bow-tie for University of Maryland - CS16 (liver failure).", INTRO,
                      [{"id": f"nn_umd{S}b", "title": "Nurses' Notes", "content": D1_1000},
                       {"id": f"vs_umd{S}b", "title": "Vital Signs", "content": vs(1)},
                       {"id": f"meds_umd{S}b", "title": "Medications", "content": MEDS},
                       {"id": f"labs_umd{S}b", "title": "Laboratory Results", "content": labs(False)}],
                      dict({"type": "bowtie",
                            "stem": ("Complete the diagram by dragging from the choices below to specify what condition "
                                     "the client is most likely experiencing, 2 actions the nurse should take to address "
                                     "that condition, and 2 parameters the nurse should monitor to assess the "
                                     "client&rsquo;s progress."),
                            "explanation": (
                                "Based on the neurologic status (confusion and agitation) and the elevated ammonia level, "
                                "the client is experiencing hepatic encephalopathy. Interventions include lactulose to "
                                "lower the ammonia level and safety precautions to prevent injury until the confusion and "
                                "agitation subside; the neurologic status and serum ammonia show the response.<br>"
                                "Furosemide may be ordered, but its purpose is to reduce the ascites. Sedatives are "
                                "contraindicated in liver failure. Education about alcohol cessation waits until the "
                                "client is more stable and readiness can be assessed.")},
                           **bowtie([("Administer lactulose", 1), ("Request order for sedative", 0),
                                     ("Institute safety precautions", 1), ("Administer IV furosemide", 0),
                                     ("Educate client about alcohol cessation", 0)],
                                    [("Esophageal varices", 0), ("Hepatic encephalopathy", 1), ("Acute cholecystitis", 0),
                                     ("Acute alcohol intoxication", 0)],
                                    [("Serum glucose", 0), ("Neurologic status", 1), ("Serum ammonia", 1),
                                     ("Serum creatinine", 0), ("Blood pressure", 0)])), FN_B)

NOTES = [
    "Screen 4 keys \"acetaminophen 650 mg PRN for fever\" as CONTRAINDICATED. Current guidance (e.g. AASLD) considers "
    "acetaminophen up to about 2 g/day the preferred analgesic/antipyretic in cirrhosis (NSAIDs are the drugs to avoid). "
    "Consider changing the key to Indicated, or the option to an NSAID (e.g. ibuprofen).",
    "Screen 4: point-of-care glucose is keyed Not indicated, but this malnourished client with alcohol use disorder has a "
    "fasting glucose of 70 mg/dL (3.9 mmol/L) and is at risk of hypoglycemia. Please confirm.",
    "Screen 1 rationale said dyspnea indicates \"hepatopulmonary syndrome from worsening ascites\" and that the "
    "creatinine is normal (no creatinine is charted). Rewritten: dyspnea from ascites limiting diaphragm movement; the "
    "creatinine sentence was removed. Consider adding a creatinine value to the lab report.",
    "Screen 5 is a highlight question (question on the right, the order list as the passage; chart on the left). Its key "
    "(oxygen, lactulose, IV furosemide) is from the source's highlighted Key; students may select 3.",
    "Screen 6 rationale now explains the second blank (explore readiness to stop drinking) and why the other choices are "
    "wrong.",
    "Medication list: metoprolol XL 50 mg daily (a selective beta-blocker; nonselective beta-blockers are used for portal "
    "hypertension). Not tested; consider whether intended.",
    "Labs in SI with the author's ranges: BUN 22 mg/dL → urea 7.9 mmol/L; glucose 70 mg/dL → 3.9 mmol/L; ammonia 94 "
    "mcg/dL → 55 µmol/L (6-47) and Day 2 72 mcg/dL → 42 µmol/L (also added to the lab table on screen 6); albumin 3.2 "
    "g/dL → 32 g/L.",
]

write([case, bow], N, "Liver Failure", "Liver-Failure.docx", NOTES)
