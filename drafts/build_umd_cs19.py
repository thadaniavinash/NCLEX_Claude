"""University of Maryland - CS19: Stroke (acute ischemic stroke treated with alteplase), with its stand-alone bow-tie.
Source: "Stroke DOCX" (medical-surgical); DeNiece Bennett, DNP, MSN-Ed, RN, University of Maryland School of Nursing;
September 1, 2022, revised April 17, 2023. Screen 1's key comes from the source's highlighted Key passage.
Usage: python3 drafts/build_umd_cs19.py
"""
from umd_common import *  # noqa: F401,F403

N = 19
S = f"{N:02d}"
AUTH = "DeNiece Bennett, DNP, MSN-Ed, RN, University of Maryland School of Nursing"
DATE = "September 1, 2022; revised April 17, 2023"
FN = footnote("Stroke", AUTH, DATE)
FN_B = footnote("Stroke", AUTH, DATE, "medical-surgical faculty case study, stand-alone bow-tie")

T1100 = ("A {AGE} of Latin descent presents to the emergency department with {L}, {W}, and a {H} after completing a "
         "2.5-mile sprint. Reports some nausea but no vomiting. Thinking she was dehydrated from her exercise, she drank "
         "about a liter of water and {A}, with no improvement. She reports the symptoms began at approximately 0900. No "
         "significant previous medical or surgical history. Takes an oral combined hormonal contraceptive. Occasionally "
         "{D}, and {V}.<br>Continuous cardiac monitoring initiated per protocol. {HR}, {BP}. Awake and alert and able to "
         "make her needs known. Voiding clear yellow urine; abdomen soft with bowel sounds in all quadrants. Reports "
         "increasing numbness of the left side and the left upper and lower extremities.")
PLAIN = dict(AGE="26-year-old female", L="lightheadedness", W="generalized weakness of the left lower and upper extremities",
             H="sudden headache", A="self-administered 500 mg of acetaminophen for pain",
             D="drinks 3&ndash;4 glasses of wine a week", V="vapes with e-cigarettes daily", HR="Heart rate 99",
             BP="blood pressure 160/100")
MARKED = dict(AGE="{26-year-old female}", L="{lightheadedness|correct}",
              W="{generalized weakness of the left lower and upper extremities|correct}", H="{sudden headache|correct}",
              A="{self-administered 500 mg of acetaminophen for pain}", D="{drinks 3&ndash;4 glasses of wine a week}",
              V="{vapes with e-cigarettes daily}", HR="{Heart rate 99|correct}", BP="{blood pressure 160/100|correct}")
N1100 = note("1100", T1100.format(**PLAIN))
N1130 = note("1130", "20-gauge IV catheters placed in the right and left antecubital veins per protocol. Blood work "
                     "drawn; results returned.")
N1200 = note("1200", ("Weight 75 kg. Alteplase 67.5 mg infused over 60 minutes; 7 mg of the total dose given as a bolus "
                      "per protocol."))
N1230 = note("1230", "Transferred to the critical care unit.")
DIAG = paras("<b>Head CT:</b> findings consistent with acute ischemic stroke; no intracranial hemorrhage.")
LABS = table(["Laboratory Test and Reference Range", "1130"], [
    [lab("Glucose, fasting", "&lt; 5.5 mmol/L"), "10.3 mmol/L"],
    [lab("Hematocrit (Hct)", "Male: 0.42&ndash;0.52 L/L; Female: 0.35&ndash;0.47 L/L"), "0.55 L/L"],
    [lab("Hemoglobin (Hgb)", "Male: 130&ndash;180 g/L; Female: 120&ndash;160 g/L"), "130 g/L"],
    [lab("Platelet count", "140&ndash;450" + G9), "500" + G9],
    [lab("Prothrombin time (PT)", "9.5&ndash;12 seconds"), "13.5 seconds"]])
ORDERS = paras(
    "Alteplase 0.9 mg/kg (maximum dose 90 mg) IV over 60 minutes, STAT; give 10% of the dose as a bolus.",
    "Labetalol 20 mg IV bolus over 2 minutes, then 10 mg IV to maintain systolic BP above 140 but below 185 mm Hg and "
    "diastolic BP above 80 but below 110 mm Hg.")
PROGRESS = note("Day 2 0800", (
    "Awake, alert, and oriented to person, place, and time. Heart rate 98, sinus rhythm; blood pressure 128/86; afebrile. "
    "Bleeding and fall precautions continued. Instructed to use the call bell for assistance with ambulation. Stroke "
    "education provided and expected outcomes after a stroke reviewed. Health risk factors, signs and symptoms, early "
    "interventions, follow-up care, and apixaban at discharge discussed. Advised of a speech and swallow test to evaluate "
    "oropharyngeal motor function. Educated on the adverse effects of alteplase and the increased risk of bleeding."))


def tabs(step):
    notes = N1100 + (N1130 if step >= 4 else "") + (N1200 if step >= 5 else "") + (N1230 if step >= 6 else "")
    t = [{"id": f"nn_umd{S}", "title": "Nurses' Notes", "content": notes}]
    if step >= 3:
        t.append({"id": f"dx_umd{S}", "title": "Diagnostic Results", "content": DIAG})
    if step >= 4:
        t += [{"id": f"labs_umd{S}", "title": "Laboratory Results", "content": LABS},
              {"id": f"ord_umd{S}", "title": "Orders", "content": ORDERS}]
    if step >= 6:
        t.append({"id": f"pn_umd{S}", "title": "Progress Notes", "content": PROGRESS})
    return t


INTRO = ("A 26-year-old woman presents to the emergency department with a sudden onset of lightheadedness and generalized "
         "weakness of the left lower and upper extremities.")

screens = [
    (INTRO, tabs(1), {
        "type": "highlight",
        "stem": "Click to highlight the findings that require <b>immediate</b> follow-up.",
        "highlightTabs": [{"id": f"ht_umd{S}", "title": "Nurses' Notes", "content": note("1100", T1100.format(**MARKED))}],
        "explanation": (
            "A disruption of the blood supply to areas of the brain causes a sudden loss of motor function. Like a "
            "myocardial infarction, a disruption of blood flow to the brain is a medical emergency that requires "
            "immediate intervention. Lightheadedness, weakness of the left lower and upper extremities, a sudden headache, "
            "and the heart rate and elevated blood pressure indicate poor cerebral perfusion and require immediate "
            "follow-up.<br>The client&rsquo;s age, the acetaminophen, the alcohol intake, and the vaping are not findings "
            "that need immediate follow-up."),
    }),
    (INTRO, tabs(2), {
        "type": "matrix_mc",
        "stem": "For each finding, click to specify if the finding is a risk factor or not a risk factor for ischemic stroke.",
        "matrix": matrix("Assessment Finding", ["Risk Factor", "Not a Risk Factor"], [
            ("Combined hormonal contraceptive", 0), ("Drinks 3–4 glasses of alcohol a week", 1),
            ("Vapes e-cigarettes daily", 0), ("Completed a 2.5-mile sprint on the treadmill", 1), ("Latin descent", 0)]),
        "explanation": (
            "Combined hormonal contraceptives contain estrogen, which affects the coagulation system and increases the "
            "risk of blood clots, stroke, and heart attack. Vaping delivers nicotine, which further increases the risk of "
            "clots, stroke, and heart attack in a person using estrogen. Age, race, and sex are nonmodifiable risk "
            "factors; some Hispanic/Latino populations have a higher incidence of stroke and stroke mortality.<br>Physical "
            "activity and moderate alcohol consumption are part of a healthy lifestyle that reduces the risk of stroke."),
    }),
    (INTRO, tabs(3), {
        "type": "drag_drop_cloze",
        "preamble": "The nurse has reviewed the Diagnostic Results. The client is diagnosed with an ischemic stroke.",
        "stem": "Drag the most appropriate choice from the list of options to fill in the blank of the following sentence.",
        "cloze": cloze("The top priority for this client is [[drop0]].",
                       [("improving fluid and electrolytes", 0), ("restoring cerebral perfusion", 1),
                        ("supporting proper body alignment", 0), ("promoting nutrition and dietary needs", 0)]),
        "explanation": (
            "An interruption of blood flow to the brain from a thrombotic or embolic event causes an ischemic stroke. The "
            "main priority is to restore cerebral perfusion to prevent further neurologic deficits, an altered level of "
            "consciousness, or death of brain cells."),
    }),
    (INTRO, tabs(4), {
        "type": "select_all",
        "preamble": ("The nurse has reviewed the Nurses&rsquo; Notes from 1130, the Laboratory Results, and the Orders. The "
                     "nurse reviews the orders and plans to administer alteplase."),
        "stem": ("What additional assessment data should the nurse obtain before administering alteplase? <b>Select all "
                 "that apply.</b>"),
        "options": opts(("Recent international travel", 0), ("No current pregnancy", 1),
                        ("Blood glucose greater than 2.8 mmol/L", 1), ("No major surgical procedures within 14 days", 1),
                        ("Serum pH greater than 7.35", 0), ("Confirm onset and time frame of symptoms", 1),
                        ("Serum potassium greater than 3.5 mmol/L", 0), ("Can safely ambulate to the bathroom", 0),
                        ("Client weight", 1)),
        "explanation": (
            "Alteplase (recombinant tissue plasminogen activator) dissolves the clot once an ischemic stroke is confirmed, "
            "and the dose is weight-based. Starting thrombolytic therapy within the treatment window lessens the "
            "stroke&rsquo;s severity and improves outcomes. Contraindications include symptom onset outside the treatment "
            "window, a major surgical procedure within the last 14 days, current pregnancy, a blood glucose below 2.8 "
            "mmol/L, and heparin within the past 48 hours.<br>Travel history, the serum pH and potassium, and the ability "
            "to ambulate are not part of the alteplase screening."),
    }),
    (INTRO, tabs(5), {
        "type": "matrix_mc",
        "preamble": "The nurse has reviewed the Nurses&rsquo; Notes from 1200.",
        "stem": "For each possible action, click to specify if it is indicated or not indicated after administering alteplase.",
        "matrix": matrix("Action", ["Indicated", "Not Indicated"], [
            ("Ensure oral anticoagulants are withheld for the next 24 hours", 0),
            ("Arrange for an inpatient admission to the medical-surgical unit", 1),
            ("Assess and monitor vital signs for intracerebral hemorrhage", 0),
            ("Insert an indwelling catheter to record urine output accurately", 1),
            ("Consult with a hematologist to increase the client’s PT and INR levels", 1),
            ("Keep the client NPO until a speech and swallow evaluation is completed", 0),
            ("Monitor serum glucose level to prevent complications of a stroke", 0)]),
        "explanation": (
            "Clients who receive thrombolytic therapy are admitted to an intensive care unit for continuous cardiac "
            "monitoring and close observation for bleeding, and oral anticoagulants are withheld for the next 24 hours. "
            "Vital signs are checked every 15 minutes for 2 hours, every 30 minutes for the next 6 hours, and then hourly "
            "until 24 hours after treatment to detect intracerebral hemorrhage. The client stays NPO until a swallow "
            "evaluation is done. The blood glucose is kept at about 7.8&ndash;10 mmol/L while avoiding hypoglycemia; "
            "hyperglycemia is associated with poor neurologic outcomes.<br>Insertion of nasogastric tubes, urinary "
            "catheters, and arterial lines is delayed for 24 hours. Increasing the PT and INR would raise the risk of "
            "bleeding."),
    }),
    (INTRO, tabs(6), {
        "type": "matrix_mc",
        "preamble": ("The nurse has reviewed the Nurses&rsquo; Notes from 1230 and the Progress Notes. The client&rsquo;s "
                     "condition has improved the next day, and the nurse evaluates the client&rsquo;s understanding of the "
                     "instructions provided."),
        "stem": ("For each client statement, click to specify whether the statement indicates an understanding or no "
                 "understanding of the teaching provided."),
        "matrix": matrix("Client Statement", ["Understanding", "No Understanding"], [
            ("“I will use the call bell and wait for someone to help me get out of bed.”", 0),
            ("“A speech and swallow test will determine if I can drink normally again.”", 0),
            ("“I will switch to an electric razor instead of a straight razor to shave.”", 0),
            ("“The physical therapist will determine my functional ability.”", 1),
            ("“At discharge, I should plan to self-administer insulin for hyperglycemia.”", 1),
            ("“I will follow up with my gynecologist to determine a better contraceptive plan.”", 0)]),
        "explanation": (
            "To prevent a fall, the client calls for help to get out of bed. An ischemic stroke can cause dysphagia, so a "
            "speech and swallow evaluation determines whether she needs thickened liquids or pureed foods to prevent "
            "aspiration. Because of the bleeding risk, she uses an electric razor and a soft-bristled toothbrush. "
            "Combined hormonal contraception increases the risk of stroke, so she should explore alternatives.<br>The "
            "baseline assessment of the client&rsquo;s functional ability (motor, social, and cognitive) is completed by "
            "the nurse. The client has no diagnosis of diabetes and is not prescribed insulin; she will take apixaban, an "
            "oral anticoagulant."),
    }),
]

case = make_case(N, "", "", screens, FN)
case["description"] = ("Maryland Next Gen NCLEX Test Bank Project, September 1, 2022 (revised April 17, 2023); Author: "
                       "DeNiece Bennett, University of Maryland School of Nursing. Stroke: a 26-year-old client on a combined "
                       "hormonal contraceptive with an acute ischemic stroke; risk factors, alteplase screening and "
                       "post-thrombolysis care, and teaching.")

bow = make_standalone(N, 1, "Bowtie", "Stand-alone bow-tie for University of Maryland - CS19 (stroke).", INTRO,
                      [{"id": f"nn_umd{S}b", "title": "Nurses' Notes", "content": N1100 + N1130},
                       {"id": f"labs_umd{S}b", "title": "Laboratory Results", "content": LABS}],
                      dict({"type": "bowtie",
                            "preamble": "The nurse reviews the assessment data to determine the appropriate plan of care.",
                            "stem": ("Complete the diagram by dragging from the choices below to specify what condition "
                                     "the client is most likely experiencing, 2 actions the nurse should take to address "
                                     "that condition, and 2 parameters the nurse should monitor to assess the "
                                     "client&rsquo;s progress."),
                            "explanation": (
                                "The client is showing signs of an ischemic stroke; a combined hormonal contraceptive is a "
                                "major risk factor for stroke in young adults. The nurse initiates a code stroke, which "
                                "coordinates a rapid team response: an immediate CT scan to determine the type of stroke, "
                                "blood work within a set time frame, and a neurology consultation, to minimize neurologic "
                                "deficits. Supplemental oxygen helps prevent cell death from the lack of blood flow.<br>"
                                "Airway management is a priority because the client is at risk of dysphagia, so the nurse "
                                "monitors airway patency, and reassesses the level of consciousness: a decrease indicates "
                                "increased intracranial pressure or poor cerebral perfusion.")},
                           **bowtie([("Administer morphine", 0), ("Bolus intravenous fluids", 0),
                                     ("Give supplemental oxygen", 1), ("Initiate code stroke", 1),
                                     ("Initiate seizure precautions", 0)],
                                    [("Hypoperfusion syndrome", 0), ("Hypovolemic shock", 0), ("Ischemic stroke", 1),
                                     ("Meningitis", 0)],
                                    [("Blood pressure", 0), ("Level of consciousness", 1), ("Patency of airway", 1),
                                     ("Serum glucose", 0), ("Range of motion", 0)])), FN_B)

NOTES = [
    "Screen 1 keys \"heart rate 99\" as needing immediate follow-up (rationale: elevated heart rate), but 99 is within "
    "normal limits. Consider changing the value (e.g. 112) or removing it from the key.",
    "Head CT: the source says the CT \"shows ischemic stroke\". Early CT is usually normal in ischemic stroke and is done to "
    "exclude hemorrhage; the report now reads \"findings consistent with acute ischemic stroke; no intracranial "
    "hemorrhage\". Please confirm.",
    "Timing: symptoms began at 0900 and alteplase is started at 1200 (3 hours). The source rationale says \"within 3 hours\"; "
    "current guidelines allow up to 4.5 hours for eligible clients. The rationale now says \"within the treatment window\".",
    "Discharge on apixaban (an anticoagulant) after an ischemic stroke without atrial fibrillation is unusual (antiplatelet "
    "therapy is standard). Please review the discharge medication.",
    "Screen 6 keys \"The physical therapist will determine my functional ability\" as no understanding (source: the nurse "
    "completes the baseline functional assessment). PT/OT also assess function after stroke; consider rewording.",
    "Bow-tie keys supplemental oxygen as a correct action, but no SpO2 is charted; guidelines give oxygen only if SpO2 < "
    "94%. Consider adding a low SpO2 to the chart.",
    "Labs: PT 13.5 s (prolonged) with no anticoagulant, Hct 55% (high for a woman) and platelets 500 × 10⁹/L are not "
    "explained; consider whether intended (e.g. dehydration/polycythemia).",
    "Labs in SI with the author's ranges: glucose 186 mg/dL → 10.3 mmol/L; alteplase glucose cut-off 50 mg/dL → 2.8 mmol/L; "
    "post-stroke glucose target 140-180 mg/dL → 7.8-10 mmol/L; Hct 0.55 L/L; Hgb 130 g/L; platelets 500 × 10⁹/L.",
    "Screen 1 is a highlight question (passage and question in the left panel); its key is from the source's highlighted "
    "Key passage (5 findings). \"Students may select\" has no limit, as in the source.",
    "Screen 4 options were reordered so a correct answer is not listed first.",
]

write([case, bow], N, "Stroke", "Stroke.docx", NOTES)
