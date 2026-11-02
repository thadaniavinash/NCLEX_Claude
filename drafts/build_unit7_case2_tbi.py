"""NURS 1017 Unit 7 Case Study 2: traumatic brain injury (concussion picture -> epidural hematoma with a lucid interval).

Learning outcomes: TBI definition, etiology and prevention; primary injury (focal/coup, polar coup-contrecoup, diffuse);
concussion (pathophysiology, older grading), contusion, epidural/subdural/subarachnoid hemorrhage; secondary injury;
ICP (Monro-Kellie: brain tissue, blood, CSF), manifestations of increased ICP, CPP.
Sources checked: OpenStax Medical-Surgical Nursing 17.1 and 17.9; Lewis's Medical-Surgical Nursing in Canada (TBI, ICP);
Brain Trauma Foundation guidelines (4th ed.: SBP >= 110 mm Hg at 15-49 years, treat ICP > 22 mm Hg, CPP 60-70 mm Hg, no
prophylactic hyperventilation); Canadian CT Head Rule; Concussion in Sport Group consensus (2022, Amsterdam).
"""
from unit7_common import (NeuroChart, vs, lab, opts, dropdown, matrix_mc, matrix_mr, rationale, highlight_tab, screen, write_case)

INTRO = "The nurse in the emergency department is caring for a 19-year-old male client who fell from a longboard and struck his head."
C = NeuroChart()

# ---------------------------------------------------------------- Screen 1: highlight (recognize)
S1 = [("1540", "Arrived by ambulance after falling from his longboard at about 1500 and striking the right side of his head on a curb. "
       "He was not wearing a helmet. His friend states he was {“knocked out for about a minute”|correct}, then woke up and was talking. "
       "Client is {alert}. {Oriented to person and place but not to time; repeatedly asks “What happened?” and cannot remember the "
       "fall|correct}. Reports a {headache rated 6/10 with nausea|correct}; {vomited once in the ambulance|correct}. {4-cm boggy swelling "
       "with an abrasion over the right temporal area|correct}. {No drainage from the nose or ears}. {Pupils equal, 3 mm, briskly "
       "reactive}. {Moves all extremities with equal strength}. Glasgow Coma Scale (GCS) {14 (E4 V4 M6)|correct}. Neck nontender with full "
       "range of motion; cervical collar removed by the ED physician. Plays recreational hockey; had a concussion last winter.")]
S1_VS = [("1540", "{T 36.8° C}, {P 88 beats/min}, {RR 16 breaths/min}, {BP 128/76 mm Hg}, {SpO₂ 98% on room air}.")]
C.notes("nn", "Nurses' Notes", *S1)
C.vitals("1540", vs("36.8° C", "88 beats/min", "16 breaths/min", "128/76 mm Hg", "98% on room air"))
s1 = screen(1, INTRO, C, {
    "type": "highlight",
    "stem": "The nurse reviews the Nurses' Notes and the Vital Signs. <b>Highlight</b> the findings that require follow-up.",
    "options": [],
    "highlightTabs": [highlight_tab("ht1", "Nurses' Notes", S1), highlight_tab("ht2", "Vital Signs", S1_VS)],
    "maxCorrectSelections": None,
    "explanation": rationale(
        "<b>Require follow-up:</b>",
        "<b>Loss of consciousness, amnesia for the event, disorientation to time, and a GCS of 14:</b> signs of a traumatic brain injury "
        "(TBI) at least as severe as a concussion. Even a brief loss of consciousness after a blow to the head needs a CT scan (Canadian CT "
        "Head Rule: GCS below 15, vomiting, a dangerous mechanism, or amnesia call for imaging).",
        "<b>Headache with nausea and vomiting:</b> may be part of a concussion, but they are also early signs of rising intracranial "
        "pressure (ICP) from a bleed, so they are trended closely.",
        "<b>Boggy swelling over the right temporal area:</b> the temporal bone is the thinnest part of the skull, and the middle meningeal "
        "artery runs just beneath it. A blow here can fracture the bone and tear the artery, causing an epidural hematoma.",
        "<b>Do not require follow-up now:</b> being alert, equal and brisk pupils, equal strength, no drainage from the nose or ears (no "
        "sign of a basal skull fracture or CSF leak), and normal vital signs. These are the baseline the nurse compares with on every "
        "neurological check."),
})

# ---------------------------------------------------------------- Screen 2: matrix (analyze)
C.notes("dx", "Diagnostic Results",
    ("1610", "<b>Non-contrast head CT:</b> nondisplaced linear fracture of the right temporal bone crossing the groove of the middle "
     "meningeal artery. Thin (6 mm) biconvex (lens-shaped) collection of blood between the skull and the dura over the right temporal "
     "lobe, consistent with a small acute epidural hematoma. Small contusion of the left frontal lobe. No midline shift."))
C.labs("1550", [
    (lab("Hemoglobin (Hgb)", "Male: 125–170 g/L"), "148 g/L"),
    (lab("Platelet count", "130–380 × 10<sup>9</sup>/L"), "232 × 10<sup>9</sup>/L"),
    (lab("International normalized ratio (INR)", "0.9–1.2"), "1.0"),
    (lab("Glucose, random", "4.0–11.0 mmol/L"), "6.1 mmol/L"),
    (lab("Ethanol", "Not detected"), "Not detected"),
])
C.notes("nn", "Nurses' Notes",
    ("1615", "Neurosurgery consulted; plan is observation in the ED with neurological checks every 15 minutes and a repeat CT in 4 hours. "
     "Client states his headache is “a bit better” and asks to go home."))
s2 = screen(2, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Diagnostic Results, the Laboratory Results and the Nurses' Notes from 1615.",
    "stem": "The nurse is performing neurological checks every 15 minutes. For each finding, click to specify whether it would be an "
            "<b>early sign</b> of increased intracranial pressure (ICP), a <b>late sign</b> of increased ICP, or <b>not a sign</b> of "
            "increased ICP.",
    "matrix": matrix_mc("Finding", ["Early sign", "Late sign", "Not a sign"], [
        ("New restlessness, irritability, or confusion", 0),
        ("One pupil dilated and not reacting to light", 1),
        ("Headache that is getting worse, with vomiting", 0),
        ("Abrasion over the right temple", 2),
        ("Rising systolic BP with a widening pulse pressure, a slowing pulse, and irregular breathing", 1),
        ("Takes longer to answer, or needs a louder voice or a touch to stay awake", 0),
        ("Abnormal flexion or extension of the arms in response to a painful stimulus", 1),
        ("Pupils equal, round, and briskly reactive", 2),
    ]),
    "explanation": rationale(
        "<b>Why this client is watched so closely:</b> his CT shows a small <b>epidural hematoma</b>: arterial bleeding from the middle "
        "meningeal artery, under a temporal bone fracture, between the skull and the dura. A typical course is a brief loss of "
        "consciousness, then a <b>lucid interval</b> in which the client seems well (as he does now, asking to go home), then rapid "
        "deterioration as the arterial clot grows. The skull cannot expand: according to the <b>Monro-Kellie doctrine</b>, its contents "
        "(brain tissue about 80%, blood about 10%, CSF about 10%) keep ICP normal only while CSF and venous blood can be pushed out to "
        "make room. Once that reserve is used up, ICP rises quickly.",
        "<b>Early signs</b> (report promptly): a change in level of consciousness is the earliest and most sensitive sign: "
        "restlessness, irritability, new confusion, slower responses, needing more stimulation to stay awake. Worsening headache and "
        "vomiting also occur early.",
        "<b>Late signs</b> (an emergency): a dilated, nonreactive pupil (pressure on cranial nerve III), abnormal posturing "
        "(decorticate flexion or decerebrate extension), and <b>Cushing's triad</b> (rising systolic BP with a widening pulse "
        "pressure, bradycardia, irregular respirations), which means the brainstem is being compressed.",
        "<b>Not signs of increased ICP:</b> the abrasion and equal, brisk pupils (the baseline the nurse compares with).",
        "<b>Other injury types:</b> a <b>concussion</b> is a temporary disturbance of brain function from acceleration-deceleration "
        "forces (stretched axons, ion shifts, an energy crisis) with a normal CT; older systems graded it (grade 1: confusion without "
        "loss of consciousness, clearing within 15 minutes; grade 2: longer than 15 minutes; grade 3: any loss of consciousness), "
        "but current guidance manages each concussion by its symptoms. A <b>contusion</b> is bruised brain tissue; his left frontal "
        "contusion, opposite the blow, is a <b>coup-contrecoup</b> injury. A <b>subdural hematoma</b> is venous bleeding from torn "
        "bridging veins (crescent-shaped, may develop slowly in older adults or people on anticoagulants), and a <b>subarachnoid "
        "hemorrhage</b> is blood in the CSF space (sudden severe headache, neck stiffness). His normal platelets and INR mean no "
        "bleeding disorder is adding to the risk."),
})

# ---------------------------------------------------------------- Screen 3: drop-down cloze (prioritize)
C.notes("nn", "Nurses' Notes",
    ("1720", "Client difficult to rouse: opens eyes only to a painful stimulus, speaks in confused, inappropriate words, and localizes "
     "pain (GCS 10, E2 V3 M5). Vomited twice since 1700. Right pupil 6 mm and sluggish; left pupil 3 mm and brisk. Left arm and leg "
     "weaker than the right (3/5). Respirations irregular."))
C.vitals("1720", vs("37.0° C", "56 beats/min", "12 breaths/min, irregular", "174/70 mm Hg", "94% on room air"))
s3 = screen(3, INTRO, C, {
    "type": "dropdown_cloze",
    "preamble": "The nurse has reviewed the Nurses' Notes from 1720 and the Vital Signs from 1720.",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {
        "text": "The client's findings indicate [[drop0]], as shown by [[drop1]]. The nurse's first action is to [[drop2]].",
        "dropdowns": [
            dropdown(("a second concussion", False), ("rapidly rising ICP from the expanding epidural hematoma", True),
                     ("a postictal state after an unwitnessed seizure", False), ("dehydration from vomiting", False), seed="u7c2-d0"),
            dropdown(("the abrasion over his right temple", False),
                     ("a falling GCS, a dilated right pupil, left-sided weakness, and Cushing's triad", True),
                     ("a temperature of 37.0° C", False), ("an SpO₂ of 94%", False), seed="u7c2-d1"),
            dropdown(("notify the provider immediately and prepare him for emergency surgery", True),
                     ("recheck his neurological status in 15 minutes", False),
                     ("give him an antiemetic and let him sleep", False),
                     ("lower the head of the bed flat", False), seed="u7c2-d2"),
        ],
    },
    "explanation": rationale(
        "<b>Rapidly rising ICP from the expanding hematoma:</b> after the lucid interval, his level of consciousness has fallen "
        "(GCS 14 to 10), and he now has late signs: a dilated, sluggish pupil on the <b>same side</b> as the bleed (the swelling "
        "temporal lobe pushes on cranial nerve III), weakness on the <b>opposite side</b> (the motor tracts cross in the brainstem), "
        "and Cushing's triad (BP 174/70 mm Hg with a widened pulse pressure, pulse 56 beats/min, irregular respirations). These mean "
        "the brain is about to herniate.",
        "<b>First action:</b> this is a neurosurgical emergency; the provider is notified at once and the client is prepared for "
        "emergency evacuation of the clot (the nurse also protects the airway, raises the head of the bed to 30 degrees with the head "
        "midline, and stays with him). Waiting 15 minutes, sedating him, or lying him flat would delay treatment or raise ICP further.",
        "<b>Why not the others:</b> a concussion, a postictal state or dehydration would not cause a one-sided dilated pupil or "
        "Cushing's triad."),
})

# ---------------------------------------------------------------- Screen 4: matrix indicated / contraindicated (generate solutions)
C.notes("nn", "Nurses' Notes",
    ("2130", "Returned from the operating room after emergency right temporal craniotomy and evacuation of the epidural hematoma. "
     "Admitted to the neurological ICU. Intubated and mechanically ventilated; sedated with propofol and fentanyl infusions. ICP "
     "monitor in place: ICP 12 mm Hg. Pupils 3 mm, equal and reactive. Moves all limbs to painful stimuli; left side weaker."))
C.notes("ord", "Provider Orders",
    ("2130", "Head of bed 30 degrees; head and neck midline.<br>"
     "ICP and CPP monitoring; notify for ICP above 22 mm Hg or CPP below 60 mm Hg.<br>"
     "Notify for SBP below 110 mm Hg, SpO₂ below 94%, or temperature above 38° C.<br>"
     "0.9% sodium chloride IV at 80 mL/h.<br>"
     "Propofol and fentanyl infusions titrated to the sedation scale; fentanyl 25 mcg IV PRN for coughing or agitation.<br>"
     "3% sodium chloride 250 mL IV over 30 minutes PRN for ICP above 22 mm Hg for more than 5 minutes; serum sodium every 6 hours.<br>"
     "Acetaminophen 650 mg per NG tube every 6 hours PRN for temperature above 38° C.<br>"
     "Levetiracetam 500 mg IV every 12 hours for 7 days (seizure prevention)."))
s4 = screen(4, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from 2130 and the Provider Orders.",
    "stem": "The nurse plans care to prevent secondary brain injury. For each intervention, click to specify whether it is "
            "<b>indicated</b> or <b>contraindicated</b>.",
    "matrix": matrix_mc("Intervention", ["Indicated", "Contraindicated"], [
        ("Keep the head and neck in midline alignment and avoid tight endotracheal tube ties around the neck", 0),
        ("Position the client with the hips flexed more than 90 degrees", 1),
        ("Compare each neurological check with the previous one and report any decline", 0),
        ("Change the maintenance IV fluid to 5% dextrose in water", 1),
        ("Monitor the BP, respirations and sedation level closely while the propofol and fentanyl infusions run", 0),
        ("Hyperoxygenate before suctioning and limit each suction pass to 10 seconds or less", 0),
        ("Group the bath, linen change, suctioning, and repositioning into one long session", 1),
        ("Turn the client every 2 hours, keeping the head in line with the body", 0),
    ]),
    "explanation": rationale(
        "<b>Secondary brain injury</b> is damage that develops in the hours and days after the primary injury. Low oxygen and low "
        "blood flow trigger a chain of events (glutamate release, calcium entry into cells, inflammation) that causes two kinds of "
        "swelling: <b>cytotoxic edema</b> (cells swell when their membrane pumps fail) and <b>vasogenic edema</b> (a leaky "
        "blood-brain barrier lets fluid into the tissue). Hypoxia, hypotension, fever, seizures and high or low glucose all make it "
        "worse; nursing care aims to prevent each one.",
        "<b>Indicated:</b> a midline head and loose tube ties keep the jugular veins open so blood drains from the brain. Comparing "
        "each neurological check with the last one detects decline early. Propofol and opioids can lower BP and depress breathing "
        "(adverse effects that reduce blood flow to the brain), so BP and sedation are monitored. Suctioning raises ICP, so it is "
        "brief and preceded by extra oxygen. Regular turning with the head aligned prevents pressure injuries and pneumonia without "
        "raising ICP.",
        "<b>Contraindicated:</b> hip flexion above 90 degrees raises abdominal and chest pressure and slows venous drainage from the "
        "head. D5W acts as free water once the glucose is used, and worsens brain swelling; isotonic fluids are used. Long clusters of "
        "care cause sustained rises in ICP; activities are spaced with rest periods."),
})

# ---------------------------------------------------------------- Screen 5: select all (take action)
C.notes("nn", "Nurses' Notes",
    ("Day 2 0400", "Client coughing and pushing against the ventilator during repositioning; sedation scale shows light sedation. ICP "
     "26 mm Hg for the last 10 minutes; MAP 78 mm Hg. Head turned to the right on the pillow. Skin warm and flushed. Has received two "
     "doses of 3% sodium chloride overnight."))
C.vitals("Day 2 0400", vs("38.6° C", "96 beats/min", "16 breaths/min (ventilator)", "112/61 mm Hg", "97% (ventilator, FiO₂ 0.40)"))
C.labs("Day 2 0200", [
    (lab("Hemoglobin (Hgb)", "Male: 125–170 g/L"), "131 g/L"),
    (lab("Platelet count", "130–380 × 10<sup>9</sup>/L"), "198 × 10<sup>9</sup>/L"),
    (lab("International normalized ratio (INR)", "0.9–1.2"), "1.1"),
    (lab("Glucose, random", "4.0–11.0 mmol/L"), "7.4 mmol/L"),
    (lab("Sodium (Na)", "136–146 mmol/L"), "149 mmol/L"),
])
s5 = screen(5, INTRO, C, {
    "type": "select_all",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 2 0400, the Vital Signs from Day 2 0400 and the Laboratory Results "
                "from Day 2 0200.",
    "stem": "Which actions should the nurse take? <b>Select all that apply.</b>",
    "options": opts(
        ("Reposition the head to midline and confirm the head of the bed is at 30 degrees", True),
        ("Lower the head of the bed flat to increase blood flow to the brain", False),
        ("Administer the prescribed PRN fentanyl", True),
        ("Give the prescribed acetaminophen and apply cooling measures", True),
        ("Suction the endotracheal tube every 15 minutes to prevent coughing", False),
        ("Notify the provider of the ICP and CPP and the latest sodium result", True),
        ("Complete the morning bed bath now while the client is awake", False),
        ("Check the IV site of the hypertonic saline for redness, swelling or pain", True),
        seed="u7c2-s5"),
    "explanation": rationale(
        "<b>CPP = MAP − ICP = 78 − 26 = 52 mm Hg</b>, below the ordered limit of 60 mm Hg, and the ICP has been above the ordered limit "
        "for 10 minutes. Coughing against the ventilator, a head turned to one side (kinked jugular veins) and fever are raising it.",
        "<b>Correct:</b> straighten the head and keep the head of the bed at 30 degrees to improve venous drainage. Give the PRN "
        "fentanyl for coughing and agitation, as ordered. Treat the fever, which raises brain metabolism and blood flow. Notify the "
        "provider: the ICP and CPP are outside the ordered limits, and the sodium has risen to 149 mmol/L after two doses of "
        "hypertonic saline (it draws water out of the brain into the blood, so sodium is monitored; a high sodium is an expected "
        "effect, but the provider decides whether another dose is safe). Hypertonic solutions irritate veins and damage tissue if "
        "they leak, so the IV site is checked.",
        "<b>Incorrect:</b> lying flat reduces venous drainage and raises ICP. Frequent routine suctioning triggers coughing and raises "
        "ICP; suction only when needed. Nonurgent care (a bed bath) is postponed while ICP is high."),
})

# ---------------------------------------------------------------- Screen 6: matrix (evaluate)
C.notes("nn", "Nurses' Notes",
    ("Day 9 1000", "Extubated on Day 4; transferred to the neurosurgical unit on Day 5. GCS 15. Mild headache (2/10), tires easily, and "
     "says bright screens bother him. Walks independently; incision healing. Discharge home with his parents today; "
     "neurosurgery has continued levetiracetam by mouth until the follow-up visit in 2 weeks. The nurse reviews the "
     "discharge teaching with the client."))
C.vitals("Day 9 1000", vs("36.8° C", "76 beats/min", "16 breaths/min", "124/74 mm Hg", "98% on room air"))
s6 = screen(6, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 9 1000 and the Vital Signs from Day 9 1000.",
    "stem": "For each statement the client makes, click to specify whether it indicates an <b>understanding</b> of the discharge teaching "
            "or a <b>need for further teaching</b>.",
    "matrix": matrix_mc("Client Statement", ["Understanding", "Needs further teaching"], [
        ("“I'll wear a certified helmet every time I ride my longboard or bike.”", 0),
        ("“I can go back to playing hockey as soon as my headache is gone.”", 1),
        ("“If I feel unusually irritable, down, or very sleepy on the levetiracetam, I'll tell my doctor.”", 0),
        ("“A few beers at the party this weekend won't affect how my brain heals.”", 1),
        ("“I'll drive myself to my follow-up appointment next week.”", 1),
        ("“If my headache gets much worse, I keep vomiting, or I get very sleepy or confused, I'll go to emergency.”", 0),
        ("“I'll start with short periods of light activity and limit screen time, then increase slowly if my symptoms don't get "
         "worse.”", 0),
    ]),
    "explanation": rationale(
        "<b>Understanding:</b> most traumatic brain injuries are preventable (falls, motor vehicle and bicycle crashes, sports and "
        "assaults are the main causes); a certified helmet, seat belts, fall prevention and not riding or driving impaired reduce the "
        "risk. Levetiracetam commonly causes drowsiness and can cause irritability, mood changes and, rarely, depression or suicidal "
        "thoughts, which he reports. Worsening headache, repeated vomiting, drowsiness or confusion can mean bleeding or rising "
        "pressure and need emergency care. After a brain injury, a short period of relative rest is followed by a <b>gradual</b> "
        "return to light activity and screen use, increased only if symptoms do not worsen.",
        "<b>Needs further teaching:</b> return to contact sport follows a stepwise plan and needs clearance by the neurosurgeon; "
        "another injury before recovery causes greater damage. Alcohol slows recovery, impairs judgment (raising the risk of another "
        "injury), adds to the drowsiness from levetiracetam and lowers the seizure threshold. Driving is not allowed until the provider "
        "clears him."),
})

write_case(2,
    "19-year-old male client who fell from a longboard without a helmet: recognizing a head injury, early and late signs of "
    "increased ICP during neurological checks (epidural hematoma with a lucid interval), the nurse's response to deterioration, "
    "nursing care to prevent secondary brain injury after craniotomy (positioning, suctioning, fever, sedation and hypertonic saline "
    "monitoring), and discharge teaching on medication effects, graded return to activity and TBI prevention.",
    [s1, s2, s3, s4, s5, s6],
    ["- Revised 2 Nov 2026 to the nursing-focused rules (safety, function, quality of life; hallmark manifestations; labs and "
     "medication adverse effects included; no emphasis on doses or treatment criteria).",
     "- Screen 2 is now early vs late signs of increased ICP; concussion, contusion, coup-contrecoup and the hematoma types are in "
     "its rationale.",
     "- Clinician review: provider orders (doses), the sodium result after hypertonic saline, the return-to-sport statement."],
    "TBI",
    intro_note="Case written by Claude on 2 Nov 2026 for the Unit 7 learning outcomes and revised the same day to be more "
               "nursing-focused; please review before using it with students:")
