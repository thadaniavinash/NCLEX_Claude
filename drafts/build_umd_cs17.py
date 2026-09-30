"""University of Maryland - CS17: Prostate cancer with prostatectomy (postoperative hemorrhagic shock), with its bow-tie.
Source: "Prostate Cancer DOCX" (medical-surgical); Tara Sohrabi, Nursing Professor, Montgomery College; September 1,
2022. Screen 5's key comes from the source's highlighted Key; screen 3 has no key in the source (see NOTES).
Usage: python3 drafts/build_umd_cs17.py
"""
from umd_common import *  # noqa: F401,F403

N = 17
S = f"{N:02d}"
AUTH = "Tara Sohrabi, Nursing Professor, Montgomery College"
FN = footnote("Prostate Cancer with Prostatectomy", AUTH)
FN_B = footnote("Prostate Cancer with Prostatectomy", AUTH, kind="medical-surgical faculty case study, stand-alone bow-tie")

N1315 = note("1315", (
    "Client transferred from the postanesthesia care unit to the surgical unit after a robotic-assisted laparoscopic "
    "prostatectomy for early-stage prostate cancer. Alert and oriented &times; 4. Vital signs normal. Six small abdominal "
    "incisions with 4 &times; 4 dressings covered by clear dressings, dry and intact. Indwelling urinary catheter with "
    "continuous bladder irrigation draining clear, red-colored urine."))
N1330 = note("1330", "Dressings dry and intact; urinary catheter draining red urine. Irrigation rate increased.")
N1345 = note("1345", "Dressings dry and intact. Ketorolac 30 mg IV push given. Urine slightly red.")
N1415 = note("1415", "Pain decreased, but client is slightly confused. Urine bright red.")
N1420 = note("1420", "Provider notified of change in client status.")
N1445 = note("1445", "Provider retaped catheter to client&rsquo;s leg. Oxygen and fluid bolus given. Urine light pink.")

VS_ROWS = [("T", "37.4&deg;C (99.4&deg;F)", "37.4&deg;C (99.4&deg;F)", "37.3&deg;C (99.2&deg;F)", "37.3&deg;C (99.2&deg;F)",
            "36.7&deg;C (98.2&deg;F)"),
           ("P", "85", "88", "102", "124", "100"), ("RR", "16", "16", "20", "20", "16"),
           ("BP", "145/73", "130/73", "110/70", "95/53", "110/55"),
           ("Pulse oximetry reading", "96% on room air", "96% on room air", "94% on room air", "90% on room air",
            "96% on 2 L/min"),
           ("Pain", "3/10", "3/10", "6/10", "2/10", "2/10")]


def vs(cols):
    return vitals(["1315", "1330", "1345", "1415", "1445"][:cols], [r[:cols + 1] for r in VS_ROWS])


ORDER_TEXT = ["Maintain traction on catheter", "Continuous bladder irrigation: titrate to keep urine pink to clear",
              "Administer 500 mL 0.9% sodium chloride IV bolus", "Administer oxygen to keep oxygen saturation above 94%",
              "Obtain blood for hemoglobin and hematocrit", "Notify primary care provider promptly with laboratory results",
              "Administer blood component if hemoglobin is below 70 g/L"]
ORDERS = paras(*ORDER_TEXT)
ORDERS_MARKED = paras(*([ORDER_TEXT[0]] + [("{%s|correct}" if i in (2, 3) else "{%s}") % t
                                           for i, t in enumerate(ORDER_TEXT) if i > 0]))
LABS = table(["Laboratory Test and Reference Range", "1445"], [
    [lab("Hematocrit (Hct)", "Male: 0.42&ndash;0.52 L/L; Female: 0.35&ndash;0.47 L/L"), "0.32 L/L"],
    [lab("Hemoglobin (Hgb)", "Male: 130&ndash;180 g/L; Female: 120&ndash;160 g/L"), "100 g/L"]])


def tabs(step):
    notes = N1315 + N1330 + N1345 + N1415 + (N1420 if step >= 4 else "") + (N1445 if step >= 6 else "")
    t = [{"id": f"nn_umd{S}", "title": "Nurses' Notes", "content": notes},
         {"id": f"vs_umd{S}", "title": "Vital Signs", "content": vs(5 if step >= 6 else 4)}]
    if step >= 6:
        t += [{"id": f"ord_umd{S}", "title": "Orders", "content": ORDERS},
              {"id": f"labs_umd{S}", "title": "Laboratory Results", "content": LABS}]
    return t


INTRO = ("A 55-year-old client is admitted to the surgical unit after a robotic-assisted laparoscopic radical "
         "prostatectomy for early-stage prostate cancer.")

screens = [
    (INTRO, tabs(1), {
        "type": "select_all",
        "stem": "Which findings require <b>immediate</b> follow-up? <b>Select all that apply.</b>",
        "options": opts(("Temperature", 0), ("Mental status", 1), ("Heart rate", 1), ("Blood pressure", 1),
                        ("Respiratory rate", 0), ("Pain", 0), ("Pulse oximetry reading", 1), ("Urine", 1)),
        "explanation": (
            "The trends in the heart rate, blood pressure, and pulse oximetry reading are consistent with hypovolemia, and "
            "the confusion may be a symptom of poor cerebral perfusion. The urine was only slightly red but is now bright "
            "red again, suggesting the bleeding is getting worse.<br>The temperature and respiratory rate are stable, and "
            "the pain has decreased."),
    }),
    (INTRO, tabs(2), {
        "type": "matrix_mr",
        "stem": ("For each finding, click to specify if the finding is consistent with the complication of hemorrhagic "
                 "shock, fluid overload, or pulmonary embolism. Each finding may support more than one complication."),
        "matrix": matrix_mr("Finding", ["Hemorrhagic Shock", "Fluid Overload", "Pulmonary Embolism"], [
            ("Confusion", [0, 2]), ("Rapid heart rate", [0, 2]), ("Low blood pressure", [0, 2]),
            ("Low pulse oximetry reading", [0, 1, 2]), ("Bright red urine", [0])]),
        "explanation": (
            "All three postoperative complications can cause low oxygenation. Hemorrhagic shock and pulmonary embolism "
            "both manifest as mental status changes, tachycardia, and hypotension.<br>The bright red urine indicates active "
            "bleeding and is associated with hemorrhagic shock."),
    }),
    (INTRO, tabs(3), {
        "type": "dyad",
        "stem": "Complete the following sentence by choosing from the lists of options.",
        "cloze": cloze("The client is most likely experiencing [[drop0]], as evidenced by the [[drop1]].",
                       [("fluid overload", 0), ("hemorrhagic shock", 1), ("pulmonary embolism", 0)],
                       [("cardiovascular assessment", 1), ("respiratory assessment", 0), ("neurologic assessment", 0)]),
        "explanation": (
            "The client is experiencing hemorrhagic shock, as most evidenced by the cardiovascular assessment: low blood "
            "pressure and tachycardia, with active bleeding in the urine."),
    }),
    (INTRO, tabs(4), {
        "type": "matrix_mc",
        "preamble": ("The nurse has reviewed the Nurses&rsquo; Notes from 1420. The nurse suspects the client is "
                     "experiencing hemorrhagic shock and notifies the provider."),
        "stem": ("For each potential intervention, click to specify whether the intervention is appropriate or not "
                 "appropriate to include in the plan of care for a client experiencing hemorrhagic shock after "
                 "prostatectomy."),
        "matrix": matrix("Potential Intervention", ["Appropriate", "Not Appropriate"], [
            ("Obtaining a hemoglobin and hematocrit", 0), ("Removing the urinary catheter", 1),
            ("Administering a fluid bolus", 0), ("Obtaining a urine culture", 1), ("Administering an enema", 1),
            ("Assessing urine output hourly", 0), ("Applying oxygen", 0)]),
        "explanation": (
            "The nurse restores perfusion by applying oxygen and giving a fluid bolus. Hemoglobin and hematocrit levels "
            "show whether blood is needed. Urine output is monitored closely to ensure the catheter is patent and renal "
            "perfusion is adequate.<br>The catheter stays in place; the provider may apply traction to put pressure on "
            "bleeding sites. A urine culture is unlikely to help, because infection is not suspected and the urine is "
            "bloody. Enemas are contraindicated because they may injure the prostatic fossa."),
    }),
    (INTRO, tabs(5), {
        "type": "highlight_2",
        "preamble": "The physician assesses the client, applies traction to the catheter, and writes orders.",
        "stem": ("Click to highlight <b>2</b> additional orders the nurse should implement <b>immediately</b> to manage "
                 "hemorrhagic shock."),
        "maxCorrectSelections": 2,
        "highlightTabs": [{"id": f"ht_umd{S}", "title": "Orders", "content": ORDERS_MARKED}],
        "explanation": (
            "The nurse immediately gives the IV fluid bolus to treat the hypovolemia and applies oxygen to improve "
            "oxygenation and perfusion.<br>The other orders (irrigation titration, blood work, reporting results, and a "
            "possible transfusion) follow."),
    }),
    (INTRO, tabs(6), {
        "type": "dyad",
        "preamble": ("The nurse has reviewed the Nurses&rsquo; Notes and Vital Signs from 1445, the Orders, and the "
                     "Laboratory Results. At 1445, the nurse reassesses the client&rsquo;s vital signs and reviews the "
                     "laboratory results."),
        "stem": "Complete the following sentences by choosing from the lists of options.",
        "cloze": cloze("The nurse determines the client&rsquo;s status is [[drop0]]. The nurse should now [[drop1]].",
                       [("improving", 1), ("deteriorating", 0), ("unchanged", 0)],
                       [("modify the plan of care", 0), ("continue monitoring the client’s vital signs", 1),
                        ("prepare the client for discharge", 0)]),
        "explanation": (
            "The client&rsquo;s vital signs are improving, and the nurse should continue monitoring them. The current plan "
            "of care is meeting the outcome, so it does not need to be modified.<br>It is too soon to prepare for "
            "discharge: discharge planning begins at admission, but the client&rsquo;s condition deteriorated and needs to "
            "be monitored for longer."),
    }),
]

case = make_case(N, "", "", screens, FN)
case["description"] = ("Maryland Next Gen NCLEX Test Bank Project, September 1, 2022; Author: Tara Sohrabi, Montgomery "
                       "College. Prostate cancer with prostatectomy: a 55-year-old client develops hemorrhagic shock after "
                       "a robotic-assisted laparoscopic prostatectomy; recognition, actions, and evaluation.")

B_VS = vitals(["1315", "1330", "1345", "1415"], [r[:5] for r in VS_ROWS[:2]] + [("RR", "16", "16", "20", "24")]
              + [r[:5] for r in VS_ROWS[3:]])
bow = make_standalone(N, 1, "Bowtie", "Stand-alone bow-tie for University of Maryland - CS17 (prostatectomy).", INTRO,
                      [{"id": f"nn_umd{S}b", "title": "Nurses' Notes", "content": N1315 + N1330 + N1345 + N1415},
                       {"id": f"vs_umd{S}b", "title": "Vital Signs", "content": B_VS},
                       {"id": f"labs_umd{S}b", "title": "Laboratory Results", "content": LABS}],
                      dict({"type": "bowtie",
                            "stem": ("Complete the diagram by dragging from the choices below to specify what condition "
                                     "the client is most likely experiencing, 2 actions the nurse should take to address "
                                     "that condition, and 2 parameters the nurse should monitor to assess the "
                                     "client&rsquo;s progress."),
                            "explanation": (
                                "The trends in the heart rate, blood pressure, and pulse oximetry reading are consistent "
                                "with shock, and the confusion may be a symptom of poor cerebral perfusion. The urine was "
                                "only slightly red but is now bright red again, suggesting the bleeding is getting worse. "
                                "The client needs oxygen and a fluid bolus to improve perfusion, and the urine and blood "
                                "pressure are monitored for resolution of the bleeding and hypotension.")},
                           **bowtie([("Administer oxygen", 1), ("Administer antibiotics", 0),
                                     ("Encourage incentive spirometry", 0), ("Administer IV fluid bolus", 1),
                                     ("Obtain a chest X-ray", 0)],
                                    [("Sepsis", 0), ("Atelectasis", 0), ("Hemorrhagic shock", 1), ("Pulmonary embolism", 0)],
                                    [("Blood pressure", 1), ("Urine", 1), ("WBC count", 0), ("Breath sounds", 0),
                                     ("Temperature", 0)])), FN_B)

NOTES = [
    "Screen 3 has NO answer key in the source. Keyed as hemorrhagic shock + \"cardiovascular assessment\" (the rationale "
    "cites low BP, tachycardia, and bleeding). Please confirm the second blank.",
    "Ketorolac 30 mg IV is given at 1345 to a client who is bleeding after surgery (NSAIDs increase bleeding risk). "
    "Not tested; consider replacing it with an opioid or using it as a cue in a rationale.",
    "Continuous bladder irrigation with catheter traction is standard after TURP, but uncommon after a robotic-assisted "
    "RADICAL prostatectomy (which has a urethrovesical anastomosis). Consider changing the procedure to TURP, or "
    "removing CBI/traction.",
    "Screen 6 vital signs in the source show RR 14 at 1345 and 1415, while screens 1-5 show 20; the earlier values "
    "(20, 20) are used throughout so the chart does not change.",
    "Screen 5 is a highlight question (question on the right, the order list as the passage; chart on the left); its "
    "key (fluid bolus, oxygen) is from the source's highlighted Key. \"Maintain traction on catheter\" is not selectable "
    "(already done by the physician).",
    "Screen 4 stem typo fixed (\"appropriate or not appropriate\").",
    "Labs in SI with the author's ranges: Hct 32% → 0.32 L/L; Hgb 10 g/dL → 100 g/L; transfusion threshold Hgb < 7 g/dL "
    "→ < 70 g/L.",
    "Screen 1 options were reordered so a correct answer is not listed first.",
]

write([case, bow], N, "Prostate Cancer with Prostatectomy", "Prostate-Cancer.docx", NOTES)
