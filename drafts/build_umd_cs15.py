"""University of Maryland - CS15: Type 2 diabetes and ketoacidosis, with its stand-alone bow-tie.
Source: "Ketoacidosis DOCX" (medical-surgical); DeNiece Bennett, DNP, MSN-Ed, University of Maryland School of
Nursing; September 1, 2022.
Corrections from the source (see NOTES): the arterial blood gas (HCO3 32 / PaCO2 45 is not DKA) now shows a metabolic
acidosis with respiratory compensation; the potassium additive is 20 mmol/L (source: 20 mEq/100 mL); pursed-lip
breathing is keyed contraindicated (it would blunt Kussmaul compensation).
Usage: python3 drafts/build_umd_cs15.py
"""
from umd_common import *  # noqa: F401,F403

N = 15
S = f"{N:02d}"
AUTH = "DeNiece Bennett, DNP, MSN-Ed, University of Maryland School of Nursing"
FN = footnote("Type II Diabetes &amp; Ketoacidosis", AUTH)
FN_B = footnote("Type II Diabetes &amp; Ketoacidosis", AUTH, kind="medical-surgical faculty case study, stand-alone bow-tie")

N1200 = note("1200", (
    "73-year-old male client with a history of type 2 diabetes brought to the emergency department by his spouse for "
    "changes in mental status from his baseline. His wife reports that he woke at 0600 to complete his morning routine. "
    "At approximately 1100 he became unaware of his surroundings and began sweating profusely and slurring his words. "
    "Breath sounds clear; fruity odor on the breath; deep, rapid respirations. Sinus tachycardia on the cardiac monitor. "
    "Awake and alert; pupils equal and reactive to light. Weight 93 kg (205 lb)."))
N1215 = note("1215", (
    "Voided 30 mL of dark amber urine, sent for urinalysis. Comprehensive metabolic panel, CBC, and ABG drawn. IV of "
    "normal saline started. Oxygen 2 L/min by nasal cannula started. Capillary glucose 24.4 mmol/L."))
N1230 = note("1230", "Transferred to ICU. IV fluid bolus given.")
N1300 = note("1300", "Maintenance IV fluids and insulin infusion started.")
N1330 = note("1330", (
    "Capillary glucose 24.2 mmol/L. Awake, alert, oriented to person and place, talking in full sentences. Denies pain. "
    "Breath sounds clear. Voided 300 mL of clear urine."))

VS_ROWS = [("T", "37.5&deg;C (99.5&deg;F)", "37.5&deg;C (99.5&deg;F)", "37.1&deg;C (98.9&deg;F)", "37.1&deg;C (98.9&deg;F)"),
           ("P", "118", "115", "105", "100"), ("RR", "32", "30", "30", "24"), ("BP", "97/66", "98/70", "100/70", "109/70"),
           ("Pulse oximetry reading", "89% on room air", "92% on 2 L/min NC", "94% on 2 L/min NC", "95% on 2 L/min NC")]


def vs(cols):
    return vitals(["1200", "1215", "1300", "1330"][:cols], [r[:cols + 1] for r in VS_ROWS])


MEDS = paras("Empagliflozin 10 mg PO daily", "Sitagliptin/metformin 50 mg/1000 mg PO daily", "Valsartan 160 mg PO daily")
LAB_ROWS = [
    [lab("Arterial pH", "7.35&ndash;7.45"), "7.20"],
    [lab("PaCO<sub>2</sub>", "35&ndash;45 mm Hg"), "25 mm Hg"],
    [lab("Bicarbonate (HCO<sub>3</sub><sup>&minus;</sup>)", "22&ndash;26 mmol/L"), "10 mmol/L"],
    [lab("Creatinine", "80&ndash;124 &micro;mol/L"), "168 &micro;mol/L"],
    [lab("Glucose, random", "3.9&ndash;7.8 mmol/L"), "24.2 mmol/L"],
    [lab("Ketones, urine", "Negative"), "Positive"],
    [lab("Potassium", "3.5&ndash;5.0 mmol/L"), "3.4 mmol/L"],
]
LABS = table(["Laboratory Test and Reference Range", "1215"], LAB_ROWS)
ORDERS = paras(
    "Admit to ICU with a diagnosis of ketoacidosis.", "Give 1000 mL 0.9% sodium chloride IV bolus over 30 minutes.",
    "Then start 0.9% sodium chloride with 20 mmol/L KCl at 125 mL/hr.",
    "Start regular insulin infusion at 0.1 units/kg/hr after the fluid bolus.",
    "Fingerstick blood glucose hourly; titrate insulin infusion per ICU protocol.", "Electrolytes every 2 hours.",
    "Continuous cardiac monitoring.")


def tabs(step):
    notes = N1200 + (N1215 if step >= 2 else "") + (N1230 + N1300 + N1330 if step >= 6 else "")
    t = [{"id": f"nn_umd{S}", "title": "Nurses' Notes", "content": notes},
         {"id": f"vs_umd{S}", "title": "Vital Signs", "content": vs(4 if step >= 6 else 2 if step >= 2 else 1)},
         {"id": f"meds_umd{S}", "title": "Medications", "content": MEDS}]
    if step >= 2:
        t.append({"id": f"labs_umd{S}", "title": "Laboratory Results", "content": LABS})
    if step >= 5:
        t.append({"id": f"ord_umd{S}", "title": "Orders", "content": ORDERS})
    return t


INTRO = ("A 73-year-old male client with a history of type 2 diabetes presents to the emergency department with a change "
         "in mental status.")

screens = [
    (INTRO, tabs(1), {
        "type": "select_n", "limit": 4,
        "stem": "Select the <b>4</b> findings that are <b>most</b> significant.",
        "options": opts(("Lung sounds", 0), ("History of type 2 diabetes", 1), ("Respiratory status", 1),
                        ("Circulation", 1), ("Pupils", 0), ("Temperature", 0), ("Mental status", 1), ("Medications", 0)),
        "explanation": (
            "Because the client has type 2 diabetes, the nurse follows up on signs that the diabetes may be out of "
            "control: the deep, rapid respirations and fruity breath odor, and the change in mental status. The low blood "
            "pressure and tachycardia (circulation) can indicate severe hypovolemia.<br>The lung sounds are clear, the "
            "pupils are equal and reactive, and the temperature is only slightly elevated."),
    }),
    (INTRO, tabs(2), {
        "type": "matrix_mr",
        "preamble": ("The nurse has reviewed the Nurses&rsquo; Notes and Vital Signs from 1215 and the Laboratory Results. "
                     "The nurse starts an IV and reviews the laboratory results."),
        "stem": ("For each finding, click to specify if it is consistent with ketoacidosis or hyperglycemic hyperosmolar "
                 "syndrome. Each finding may support more than one condition."),
        "matrix": matrix_mr("Laboratory Finding", ["Ketoacidosis", "Hyperglycemic Hyperosmolar Syndrome"], [
            ("pH 7.20", [0]), ("Blood glucose 24.2 mmol/L", [0]), ("Serum creatinine 168 µmol/L", [0, 1]),
            ("Urine ketones positive", [0])]),
        "explanation": (
            "Blood glucose in diabetic ketoacidosis ranges widely (about 14&ndash;44 mmol/L), whereas in HHS it is "
            "typically above 33 mmol/L. A low pH and ketones in the urine are seen with DKA and are typically absent in "
            "HHS.<br>Both conditions cause dehydration, which elevates the creatinine."),
    }),
    (INTRO, tabs(3), {
        "type": "dropdown_cloze",
        "stem": "Complete the following sentence by choosing from the list of options.",
        "cloze": cloze("The problem the nurse should address first is [[drop0]].",
                       [("correcting pH", 0), ("restoring volume", 1), ("lowering glucose", 0)]),
        "explanation": (
            "The priority is to restore volume so the client has adequate perfusion. Once the volume is improved, insulin "
            "therapy begins and brings the glucose down slowly.<br>The acidosis is monitored to see whether it is "
            "worsening; sodium bicarbonate is not given unless the pH is below 6.9."),
    }),
    (INTRO, tabs(4), {
        "type": "matrix_mc",
        "preamble": "The client is diagnosed with ketoacidosis, and the nurse begins to plan care.",
        "stem": ("For each nursing intervention, click to specify whether the intervention is indicated, contraindicated, "
                 "or nonessential."),
        "matrix": matrix("Nursing Intervention", ["Indicated", "Contraindicated", "Nonessential"], [
            ("Obtain glycosylated hemoglobin (A1C)", 2), ("Teach the client pursed-lip breathing", 1),
            ("Administer insulin glargine subcutaneously", 1), ("Insert indwelling urinary catheter", 1),
            ("Administer IV potassium", 0), ("Monitor ECG", 0)]),
        "explanation": (
            "IV potassium is indicated: the potassium is already low, and insulin therapy moves potassium into the cells. "
            "ECG monitoring is indicated because acidosis and potassium shifts cause dysrhythmias.<br>The deep, rapid "
            "(Kussmaul) respirations are the body&rsquo;s compensation for the metabolic acidosis, so pursed-lip breathing "
            "to slow the breathing is contraindicated. DKA is treated with IV regular insulin, which can be titrated, not "
            "subcutaneous insulin glargine. Urine output can be measured with a urinal; an indwelling catheter adds "
            "infection risk in a client with diabetes.<br>The A1C reflects glucose control over months and does not guide "
            "acute treatment, so it is nonessential now."),
    }),
    (INTRO, tabs(5), {
        "type": "select_all",
        "preamble": "The nurse has reviewed the Orders.",
        "stem": "What actions should the nurse take while implementing the treatment plan? <b>Select all that apply.</b>",
        "options": opts(("Begin insulin after the bolus at 0.9 units/hr", 0),
                        ("Anticipate holding insulin for low potassium levels", 1),
                        ("Request IV fluids with dextrose when glucose levels start to normalize", 1),
                        ("Allow the client to eat when status stabilizes", 1), ("Monitor for symptoms of fluid overload", 1)),
        "explanation": (
            "Insulin therapy can cause hypokalemia; insulin is typically held if the potassium falls below 3.3 mmol/L. "
            "Dextrose is added to the IV fluids as glucose levels fall to prevent hypoglycemia while the ketosis resolves. "
            "The client can eat once the respiratory status is stable and he feels like eating. During the initial fluid "
            "resuscitation, the nurse monitors for fluid overload.<br>The client weighs 93 kg, so the ordered starting "
            "rate (0.1 units/kg/hr) is 9.3 units/hr, not 0.9 units/hr."),
    }),
    (INTRO, tabs(6), {
        "type": "select_all",
        "preamble": ("The nurse has reviewed the Nurses&rsquo; Notes from 1230, 1300, and 1330 and the Vital Signs from 1300 "
                     "and 1330. The nurse reassesses the client after the fluid bolus and the start of the insulin "
                     "infusion."),
        "stem": "Which findings indicate the treatment plan has been effective? <b>Select all that apply.</b>",
        "options": opts(("Breath sounds", 0), ("Blood pressure", 1), ("Mental status", 1), ("Pulse 100", 1),
                        ("Capillary glucose", 0), ("Pain level", 0)),
        "explanation": (
            "Treatment of DKA corrects the dehydration, the glucose, the electrolyte imbalances, and the acidosis. As the "
            "fluid volume is restored, the blood pressure rises and the heart rate falls, and as the cells are rehydrated "
            "and glucose moves into them, the neurological status improves.<br>Pain was not a problem, and the breath "
            "sounds were clear from the start. The blood glucose has not yet begun to decrease."),
    }),
]

case = make_case(N, "", "", screens, FN)
case["description"] = ("Maryland Next Gen NCLEX Test Bank Project, September 1, 2022; Author: DeNiece Bennett, University of "
                       "Maryland School of Nursing. Type 2 diabetes and ketoacidosis: a 73-year-old client on an SGLT2 "
                       "inhibitor with DKA; DKA vs HHS, priorities, insulin and potassium management, and response.")

B_LABS = table(["Laboratory Test and Reference Range", "1215"], [
    LAB_ROWS[0], [lab("PaO<sub>2</sub>", "75&ndash;100 mm Hg"), "60 mm Hg"], LAB_ROWS[1], LAB_ROWS[2],
    [lab("Urea (BUN)", "3.6&ndash;7.1 mmol/L"), "12.1 mmol/L"], LAB_ROWS[3],
    [lab("Hematocrit (Hct)", "Male: 0.42&ndash;0.52 L/L; Female: 0.35&ndash;0.47 L/L"), "0.37 L/L"],
    [lab("Hemoglobin (Hgb)", "Male: 130&ndash;180 g/L; Female: 120&ndash;160 g/L"), "140 g/L"],
    [lab("White blood cell (WBC) count", "4.5&ndash;10.5" + G9), "4.7" + G9],
    [lab("Platelet count", "140&ndash;450" + G9), "140" + G9],
    LAB_ROWS[6], [lab("Sodium", "135&ndash;145 mmol/L"), "140 mmol/L"], LAB_ROWS[5]])
bow = make_standalone(N, 1, "Bowtie", "Stand-alone bow-tie for University of Maryland - CS15 (type 2 diabetes and "
                      "ketoacidosis).", INTRO,
                      [{"id": f"nn_umd{S}b", "title": "Nurses' Notes", "content": N1200 + N1215},
                       {"id": f"vs_umd{S}b", "title": "Vital Signs", "content": vs(2)},
                       {"id": f"meds_umd{S}b", "title": "Medications", "content": MEDS},
                       {"id": f"labs_umd{S}b", "title": "Laboratory Results", "content": B_LABS}],
                      dict({"type": "bowtie",
                            "stem": ("Complete the diagram by dragging from the choices below to specify what condition "
                                     "the client is most likely experiencing, 2 actions the nurse should take to address "
                                     "that condition, and 2 parameters the nurse should monitor to assess the "
                                     "client&rsquo;s progress."),
                            "explanation": (
                                "The laboratory results show diabetic ketoacidosis, an acute complication of diabetes: "
                                "hyperglycemia, metabolic acidosis, and ketones. Treatment corrects the dehydration "
                                "(normal saline bolus) and the glucose and acidosis (IV insulin infusion). The nurse "
                                "closely monitors the capillary glucose to adjust the insulin, and the level of "
                                "consciousness, which should improve as the cells are rehydrated and glucose moves into "
                                "them.")},
                           **bowtie([("Administer IV insulin", 1), ("Give nitroglycerin", 0), ("Assist with intubation", 0),
                                     ("Administer antibiotics", 0), ("Infuse normal saline fluid bolus", 1)],
                                    [("Cardiogenic shock", 0), ("Diabetic ketoacidosis", 1),
                                     ("Hyperglycemic hyperosmolar syndrome", 0), ("Urinary tract infection with delirium", 0)],
                                    [("Capillary glucose", 1), ("Serial electrocardiograms", 0), ("Arterial blood gases", 0),
                                     ("Urinalysis", 0), ("Level of consciousness", 1)])), FN_B)

NOTES = [
    "CORRECTED blood gas: the source's ABG (pH 7.20, PaCO2 45, HCO3 32) is not DKA (a high bicarbonate means metabolic "
    "alkalosis/compensated respiratory acidosis). Changed to PaCO2 25 mm Hg and HCO3- 10 mmol/L (metabolic acidosis with "
    "respiratory compensation; still pH 7.20). Same change in the bow-tie. Please confirm.",
    "CORRECTED potassium order: \"0.9 NS with 20 mEq KCl/100 mL\" (= 200 mmol/L, dangerous) is now \"0.9% sodium "
    "chloride with 20 mmol/L KCl\" (20 mmol per litre). Please confirm the intended concentration.",
    "CHANGED KEY (screen 4): \"Teach the client pursed-lip breathing\" was keyed Indicated; it is now Contraindicated, "
    "because the Kussmaul respirations compensate for the metabolic acidosis. Please confirm, or replace the row.",
    "Screen 4 also keys insulin glargine SC and an indwelling catheter as Contraindicated; some DKA protocols give early "
    "basal insulin, and ICU care may use a catheter for hourly output. Consider \"Not indicated at this time\".",
    "Vital signs: the source's last two columns are both labelled 1330; they are 1300 and 1330 here (matching the notes).",
    "The 1215 note on screen 2 includes \"2 L O2 started per NC\" but screens 3-6 omit it; it is kept on every screen from "
    "screen 2 so the chart does not lose it.",
    "SpO2 89% on room air with clear lungs and a PaO2 of 60 (bow-tie) is unusual for DKA alone; consider whether it is "
    "intended.",
    "Home medication: sitagliptin/metformin 50/1000 mg once daily (usually twice daily). Empagliflozin (an SGLT2 "
    "inhibitor) is a useful cue for DKA in type 2 diabetes; consider mentioning it in a rationale.",
    "Labs in SI with the author's ranges: glucose 435-440 mg/dL → 24.2-24.4 mmol/L (3.9-7.8); creatinine 1.9 mg/dL → "
    "168 µmol/L; BUN 34 mg/dL → urea 12.1 mmol/L; K+/Na+ mmol/L; Hct 0.37; Hgb 140 g/L. The screen 2 rationale's glucose "
    "ranges were converted (300-800 mg/dL ≈ 14-44 mmol/L; > 600 mg/dL ≈ > 33 mmol/L).",
    "Screen 6 options were reordered so a correct answer is not listed first.",
]

write([case, bow], N, "Type II Diabetes and Ketoacidosis", "Ketoacidosis.docx", NOTES)
