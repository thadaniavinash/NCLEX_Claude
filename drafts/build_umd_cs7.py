"""University of Maryland - CS7: Compartment syndrome (after ORIF of a tibia-fibula fracture), with its trend.
Source: "Compartment Syndrome DOCX" (medical-surgical); Dawn Leukhardt, MSN, RN, College of Southern Maryland,
La Plata, Maryland; September 1, 2022.
Usage: python3 drafts/build_umd_cs7.py
"""
from umd_common import *  # noqa: F401,F403

N = 7
S = f"{N:02d}"
AUTH = "Dawn Leukhardt, MSN, RN, College of Southern Maryland, La Plata, Maryland"
FN = footnote("Compartment Syndrome", AUTH, si=False)
FN_T = footnote("Compartment Syndrome", AUTH, kind="medical-surgical faculty case study, stand-alone trend", si=False)

N0830 = note("0830", (
    "Admitted from the post-anesthesia care unit following surgery to repair an open fracture with internal fixation, "
    "with application of a fiberglass cast. R lower extremity elevated. IV infusing as ordered. Client medicated for "
    "pain before transport. VS: BP 110/72, HR 90, RR 29, T 99&deg;F (37.2&deg;C). Unable to assess pedal pulse on R "
    "lower extremity because of the cast. Motion of toes limited by pain and cast. Will monitor for signs of acute "
    "complications."))
N0930 = note("0930", "Client resting at this time. Will continue to monitor.")
N1100 = note("1100", "Client reports pain 10/10 in R lower extremity. Neurovascular checks updated.")
N1115 = note("1115", "VS: BP 82/44, HR 112, RR 22, T 99&deg;F (37.2&deg;C). Provider notified of client changes.")
N1145 = note("1145", "Cast removed at bedside; see updated flow sheet.")
N1245 = note("1245", "VS: BP 116/70, HR 88, RR 16, T 98.8&deg;F (37.1&deg;C), pain 3/10.")

NV_HEAD = ["Time", "Pain (0&ndash;10)", "Motion", "Sensation", "Capillary Refill", "Color", "Warmth", "Pulse"]
NV_LEGEND = paras(
    "<b>Key:</b> Motion and Sensation: F = full, L = limited (motion) / P = partial (sensation), N = none. Capillary "
    "refill: B = brisk (&lt; 3 seconds), S = sluggish (&gt; 3 seconds). Color: N = normal, P = pale, D = dusky, C = "
    "cyanotic. Warmth: H = hot, W = warm, T = tepid, C = cold. Pulse: 4+ bounding, 3+ increased, 2+ normal, 1+ weak, "
    "0 absent, UTA = unable to assess.")
NV = {"0830": "3/10 L F B N W UTA", "0930": "3/10 L F B N W UTA", "1030": "4/10 L F B N W UTA",
      "1100": "10/10 N N S P T UTA", "1115": "10/10 N N S P T UTA", "1130": "10/10 N N S D T UTA",
      "1145": "10/10 L N S P T 1+", "1245": "3/10 L N S N C 0"}


def flow(times, data=NV, heading="Neurovascular assessment, right lower extremity"):
    return (title(heading) + table(NV_HEAD, [[f"<b>{t}</b>"] + data[t].split() for t in times]) + NV_LEGEND)


ADMIT = note("0830", (
    "<b>Admission orders</b><br>Bedrest with right leg elevated on 2 pillows.<br>May use bedside commode with assistance; "
    "no weight bearing on R lower extremity.<br>Advance to regular diet as tolerated.<br>VS and neurovascular checks every "
    "hour for 4 hours, then every 4 hours."))
STAT = note("1130", (
    "<b>STAT orders</b><br>Strict bedrest; maintain R leg at the level of the heart.<br>Assist client to use bedpan; "
    "monitor intake and output.<br>Keep client NPO until cleared.<br>Document height and weight.<br>Order cast-cutting tray "
    "and compartment pressure measuring device to bedside.<br>Check neurovascular status and vital signs every 15 minutes "
    "for 2 hours.<br>IV fluid bolus of 500 mL normal saline over 30 minutes for systolic BP &lt; 100 mm Hg.<br>Complete "
    "preoperative checklist; notify the operating room to prepare for possible fasciotomy."))

TIMES = {1: ["0830", "0930", "1030", "1100"], 3: ["0830", "0930", "1030", "1100", "1115"],
         5: ["0830", "0930", "1030", "1100", "1115", "1130"],
         6: ["0830", "0930", "1030", "1100", "1115", "1130", "1145", "1245"]}


def tabs(step):
    notes = N0830 + N0930 + N1100 + (N1115 if step >= 4 else "") + (N1145 + N1245 if step >= 6 else "")
    times = TIMES[6 if step >= 6 else 5 if step >= 5 else 3 if step >= 3 else 1]
    return [{"id": f"nn_umd{S}", "title": "Nurses' Notes", "content": notes},
            {"id": f"nv_umd{S}", "title": "Neurovascular Flow Sheet", "content": flow(times)},
            {"id": f"ord_umd{S}", "title": "Orders", "content": ADMIT + (STAT if step >= 5 else "")}]


INTRO = ("The nurse is caring for a 23-year-old female client admitted to the medical-surgical unit following surgery "
         "for a compound fracture of the right tibia and fibula.")

screens = [
    (INTRO, tabs(1), {
        "type": "select_all",
        "preamble": "The nurse is performing a neurovascular assessment of the right lower extremity.",
        "stem": "Which findings require <b>immediate</b> follow-up? <b>Select all that apply.</b>",
        "options": opts(("Unable to palpate pedal pulses on the right leg", 0),
                        ("Toes on the affected extremity are cool to the touch", 1),
                        ("Right toes have noticeable pallor compared with the left", 1),
                        ("Client describes absent sensation of the right lower leg", 1),
                        ("Capillary refill greater than 3 seconds in the right toes", 1),
                        ("Client reports pain of 10/10 in the R lower extremity", 1)),
        "explanation": (
            "Primary signs of compartment syndrome include the &ldquo;5 P&rsquo;s&rdquo;: pain (out of proportion or not "
            "relieved by pain medication), pallor, pulses (diminished or absent), paresthesia, and paralysis. Fullness, "
            "a cool or cold extremity, and weakness may also occur. Any of these indicates neurovascular compromise, "
            "which can result in tissue death and loss of the limb if untreated.<br>The pedal pulse cannot be assessed "
            "because of the cast, so being unable to palpate it is expected."),
    }),
    (INTRO, tabs(2), {
        "type": "matrix_mc",
        "preamble": "The nurse documented, &ldquo;Will monitor for signs of acute complications.&rdquo;",
        "stem": ("For each potential complication of a fracture, click to indicate if the complication is an acute "
                 "complication or a chronic complication associated with fractures."),
        "matrix": matrix("Complication", ["Acute Complication", "Chronic Complication"], [
            ("Venous thromboembolism", 0), ("Complex regional pain syndrome", 1), ("Avascular necrosis", 1),
            ("Osteomyelitis", 1), ("Delayed union", 1), ("Compartment syndrome", 0)]),
        "explanation": (
            "Acute complications of a fracture include deep vein thrombosis or pulmonary embolism (venous "
            "thromboembolism), fat embolism, and compartment syndrome.<br>Late, or chronic, complications include "
            "complex regional pain syndrome, avascular necrosis, osteomyelitis, and delayed union."),
    }),
    (INTRO, tabs(3), {
        "type": "dyad",
        "preamble": "The nurse has reviewed the Neurovascular Flow Sheet from 1115.",
        "stem": "Complete the following sentence by choosing from the lists of options.",
        "cloze": cloze("Based on the assessment findings, the client is most likely experiencing [[drop0]], as most "
                       "evidenced by the [[drop1]].",
                       [("complex regional pain syndrome", 0), ("compartment syndrome", 1), ("delayed union", 0),
                        ("avascular necrosis", 0), ("osteomyelitis", 0)],
                       [("pain rating of 10/10", 0), ("neurovascular assessment", 1), ("decreased mobility", 0),
                        ("presence of the fiberglass cast", 0), ("neurological assessment", 0)]),
        "explanation": (
            "Compartment syndrome is suspected based on the abnormal findings in the neurovascular assessment: severe "
            "pain, no motion or sensation, sluggish capillary refill, pallor, and a tepid extremity.<br>Pain alone, "
            "decreased mobility, or the presence of a cast does not establish the diagnosis, and a neurological "
            "assessment evaluates the brain and nerves rather than perfusion of the limb."),
    }),
    (INTRO, tabs(4), {
        "type": "select_all",
        "preamble": ("The nurse has reviewed the Nurses&rsquo; Notes from 1115. The nurse suspects the client is "
                     "developing compartment syndrome and prepares for the provider to reassess the client."),
        "stem": ("Based on the assessment findings and recent vital signs, which orders does the nurse anticipate being "
                 "included in the plan of care? <b>Select all that apply.</b>"),
        "options": opts(("Nursing: Place client in Trendelenburg position", 0),
                        ("Nursing: Change diet to nothing by mouth", 1),
                        ("Nursing: Cast removal saw to bedside STAT", 1),
                        ("Nursing: Order compartment pressure measurement device to bedside", 1),
                        ("Medication: Administer ibuprofen 400 mg by mouth STAT", 0),
                        ("Medication: Administer morphine 4 mg IV push for pain", 1),
                        ("Medication: Administer aspirin 325 mg by mouth every 12 hours", 0),
                        ("Medication: Administer IV normal saline bolus of 500 mL over 30 minutes", 1),
                        ("Collaborative: Physical therapy to instruct on crutch walking", 0),
                        ("Collaborative: Initiate respiratory therapy protocol", 0),
                        ("Collaborative: Case management to plan for long-term care placement", 0),
                        ("Collaborative: Consult surgery team for possible fasciotomy", 1)),
        "explanation": (
            "The nurse prioritizes interventions that relieve pressure within the compartment, monitor for an improving "
            "or declining condition, and treat potential life- or limb-threatening conditions: frequent neurovascular "
            "assessments and preparing to remove the cast as soon as possible (cast removal saw at the bedside). The "
            "provider is likely to measure compartment pressures. The client is kept NPO in case surgery is required, "
            "and the surgical team is consulted for a possible fasciotomy. Morphine is indicated for the pain, and "
            "because of the hypotension an IV fluid bolus is indicated.<br>Ibuprofen is not effective for pain of "
            "10/10, and aspirin is contraindicated because of its antiplatelet effect if the client needs surgery. The "
            "Trendelenburg position is not indicated. Crutch walking waits until the compartment syndrome is resolved, "
            "and respiratory therapy and case management for long-term care are not indicated at this time."),
    }),
    (INTRO, tabs(5), {
        "type": "select_all",
        "preamble": ("The nurse has reviewed the Orders from 1130 and the Neurovascular Flow Sheet from 1130. The nurse "
                     "has reviewed the updated orders placed by the provider."),
        "stem": ("Which tasks can the nurse delegate to the unlicensed assistive personnel (UAP)? <b>Select all that "
                 "apply.</b>"),
        "options": opts(("Check neurovascular status every 15 minutes for 2 hours", 0),
                        ("Obtain vital signs every hour for 4 hours", 1), ("Assist client to use bedpan to void", 1),
                        ("Complete preoperative checklist", 0),
                        ("Assist client to maintain right leg at the level of the heart", 1),
                        ("Measure intake and output", 1), ("Document client’s height and weight", 1)),
        "explanation": (
            "To accomplish all the tasks needed for this client, the nurse may delegate some tasks to the UAP. Measuring "
            "and documenting vital signs, intake and output, and height and weight may be done by the UAP, and the UAP "
            "may help the client keep the extremity in the proper position as instructed by the nurse.<br>The UAP "
            "cannot perform assessments or monitor neurovascular status. It is the nurse&rsquo;s responsibility to "
            "ensure the client is ready for surgery; the preoperative checklist is used to ensure all preoperative "
            "criteria are met."),
    }),
    (INTRO, tabs(6), {
        "type": "matrix_mc",
        "preamble": ("The nurse has reviewed the Nurses&rsquo; Notes from 1145 and 1245 and the Neurovascular Flow Sheet "
                     "from 1145 and 1245. The nurse follows up on tasks delegated to the UAP, reviews the vital signs, "
                     "and updates the neurovascular flow sheet with the most recent assessment."),
        "stem": ("For each finding, click to specify if the finding indicates that the client&rsquo;s status has "
                 "improved, declined, or is unchanged since the onset of symptoms."),
        "matrix": matrix("Finding", ["Improved", "Declined", "Unchanged"], [
            ("Pain", 0), ("Motion", 0), ("Sensation", 2), ("Capillary refill", 2), ("Color", 0), ("Warmth", 1),
            ("Pulse", 1)]),
        "explanation": (
            "Since the onset of symptoms (1100), the pain rating, motion, and color have improved, as shown in the "
            "neurovascular assessment.<br>The warmth and the pulse have declined (the extremity is now cold with an "
            "absent pulse), and the sensation and capillary refill are unchanged."),
    }),
]

case = make_case(N, "", "", screens, FN)
case["description"] = ("Maryland Next Gen NCLEX Test Bank Project, September 1, 2022; Author: Dawn Leukhardt, College of "
                       "Southern Maryland. Compartment syndrome: after ORIF of a tibia-fibula fracture, a 23-year-old "
                       "client develops neurovascular compromise; the nurse recognizes it, anticipates orders, "
                       "delegates, and evaluates after cast removal.")

T_NV = {"1115": "10/10 N N S P T UTA", "1130": "10/10 N N S D T UTA", "1145": "10/10 L N S P T 1+",
        "1200": "6/10 L N S P T 1+", "1215": "5/10 L N S P T 1+", "1230": "5/10 L N S P C 1+",
        "1245": "3/10 L N S P C 0"}
trend = make_standalone(N, 1, "Trend", (
    "Stand-alone trend for University of Maryland - CS7 (compartment syndrome): neurovascular checks every 15 minutes "
    "after cast removal."),
    ("The nurse is caring for a 23-year-old female client on the medical-surgical unit who developed compartment "
     "syndrome following surgery for a compound fracture of the right tibia and fibula."),
    [{"id": f"nn_umd{S}t", "title": "Nurses' Notes", "content": note("1115", (
        "Neurovascular assessment completed. VS: BP 82/44, HR 112, RR 22, T 99&deg;F (37.2&deg;C); pain increased to "
        "10/10 in R lower extremity. Provider notified.")) + N1145 + N1245},
     {"id": f"nv_umd{S}t", "title": "Neurovascular Flow Sheet", "content": flow(list(T_NV), T_NV)}],
    {"type": "dyad",
     "preamble": "The nurse reassesses the client every 15 minutes for 1 hour after cast removal.",
     "stem": "Complete the following sentences by choosing from the lists of options.",
     "cloze": cloze("Based on the data, the nurse determines the client&rsquo;s status is [[drop0]]. The nurse should now "
                    "[[drop1]].",
                    [("improving", 0), ("deteriorating", 1), ("unchanged", 0)],
                    [("notify the physician", 1), ("continue to monitor", 0), ("administer pain medication", 0)]),
     "explanation": (
         "Although the pain has decreased and some assessments are unchanged, the extremity has become increasingly "
         "cool to the touch and the pulse is now absent. There is evidence that neurovascular compromise is still "
         "present, so the physician should be notified immediately in case the client needs a surgical fasciotomy to "
         "restore adequate perfusion to the extremity.")}, FN_T)

NOTES = [
    "Screen 4: the source is a grouped multiple-response question (Nursing / Medication / Collaborative, \"each "
    "category may have more than one order\"). The app has no grouped type, so it is a Select All with the category "
    "at the start of each option (same key, +/- scoring).",
    "Screen 5 (delegation): \"Obtain vital signs every hour for 4 hours\" is keyed as delegable, but the 1130 STAT "
    "order is vital signs every 15 minutes, and the client is hypotensive (BP 82/44). Consider rewording the option to "
    "match the order, and whether VS for an unstable client should be delegated.",
    "Chart timing: the source's screen 5 flow sheet already shows the 1145 and 1245 readings (after cast removal); "
    "in the app they appear on screen 6, with the 1145/1245 notes.",
    "Flow sheet 1245 color: the case shows N (normal) but the trend shows P (pale) for the same time. Screen 6 keys "
    "color as Improved (based on N). Please confirm.",
    "Screen 6 key: Pain/Motion/Color improved while the limb is now cold and pulseless; the trend then asks students "
    "to call this \"deteriorating\". Consider whether screen 6 should say so in its rationale.",
    "0830 note: RR 29 (tachypnea on admission) is not addressed anywhere; possibly a typo for 20.",
    "Screen 3 rationale referred to abnormal vital signs and tachycardia that are not yet charted at 1115 (only in the "
    "1115 note shown from screen 4); it was rewritten around the neurovascular findings.",
    "Screen 1 options were reordered so a correct answer is not listed first.",
    "No laboratory values in this case.",
]

write([case, trend], N, "Compartment Syndrome", "Compartment-Syndrome.docx", NOTES)
