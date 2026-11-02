"""NURS 1017 Unit 7 Case Study 2: traumatic brain injury (concussion picture -> epidural hematoma with a lucid interval).

Learning outcomes: TBI definition, etiology and prevention; primary injury (focal/coup, polar coup-contrecoup, diffuse);
concussion (pathophysiology, older grading), contusion, epidural/subdural/subarachnoid hemorrhage; secondary injury;
ICP (Monro-Kellie: brain tissue, blood, CSF), manifestations of increased ICP, CPP.
Sources checked: OpenStax Medical-Surgical Nursing 17.1 and 17.9; Lewis's Medical-Surgical Nursing in Canada (TBI, ICP);
Brain Trauma Foundation guidelines (4th ed.: SBP >= 110 mm Hg at 15-49 years, treat ICP > 22 mm Hg, CPP 60-70 mm Hg, no
prophylactic hyperventilation); Canadian CT Head Rule; Concussion in Sport Group consensus (2022, Amsterdam).
"""
from unit7_common import (NeuroChart, vs, opts, dropdown, matrix_mc, matrix_mr, rationale, highlight_tab, screen, write_case)

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

# ---------------------------------------------------------------- Screen 2: matrix multiple response (analyze)
C.notes("dx", "Diagnostic Results",
    ("1610", "<b>Non-contrast head CT:</b> nondisplaced linear fracture of the right temporal bone crossing the groove of the middle "
     "meningeal artery. Thin (6 mm) biconvex (lens-shaped) hyperdense collection between the skull and the dura over the right temporal "
     "lobe, consistent with a small acute epidural hematoma. Small contusion of the left frontal lobe. No midline shift."))
C.notes("nn", "Nurses' Notes",
    ("1615", "Neurosurgery consulted; plan is observation with neurological checks every 15 minutes and a repeat CT in 4 hours. Client "
     "states his headache is “a bit better” and asks to go home."))
s2 = screen(2, INTRO, C, {
    "type": "matrix_mr",
    "preamble": "The nurse has reviewed the Diagnostic Results and the Nurses' Notes from 1615.",
    "stem": "The client asks how his injury differs from a concussion. For each finding, click to specify whether it is consistent with "
            "a <b>concussion</b>, an <b>epidural hematoma</b>, a <b>subdural hematoma</b>, or a <b>subarachnoid hemorrhage</b>. Each "
            "finding may support more than one condition.",
    "matrix": matrix_mr("Finding", ["Concussion", "Epidural hematoma", "Subdural hematoma", "Subarachnoid hemorrhage"], [
        ("Bleeding from a torn middle meningeal artery, often with a temporal bone fracture", [1]),
        ("Brief loss of consciousness with amnesia for the event and a normal CT scan", [0]),
        ("Crescent-shaped collection from torn bridging veins that can spread across suture lines", [2]),
        ("Headache, nausea, and vomiting", [0, 1, 2, 3]),
        ("Loss of consciousness, then a lucid interval, then rapid deterioration", [1]),
        ("Sudden, severe (“worst ever”) headache with neck stiffness from blood in the space around the brain", [3]),
        ("Symptoms that may develop slowly over weeks in older adults and clients taking anticoagulants", [2]),
        ("Biconvex (lens-shaped) collection that stops at the suture lines", [1]),
    ]),
    "explanation": rationale(
        "<b>Concussion</b> is a mild diffuse TBI. Rapid acceleration and deceleration stretch axons; this causes ion shifts (potassium "
        "out of and calcium into neurons), a surge of glutamate, and an energy crisis in which the brain needs more glucose while its "
        "blood flow falls. The result is a temporary loss of function (confusion, amnesia, headache, nausea, sometimes loss of "
        "consciousness) without a structural lesion, so <b>CT and MRI are normal</b>. Older systems graded concussions (for example, "
        "grade 1: confusion without loss of consciousness, clearing within 15 minutes; grade 2: symptoms longer than 15 minutes; grade 3: "
        "any loss of consciousness). Current Canadian and international guidance has dropped the grades and manages each concussion by "
        "its symptoms, with a gradual return to activity.",
        "<b>Epidural hematoma</b>: arterial bleeding (usually the middle meningeal artery under a temporal bone fracture) between the skull "
        "and the dura. The dura is attached at the sutures, so the clot is <b>biconvex and stops at the suture lines</b>. Classic course: "
        "brief loss of consciousness, a <b>lucid interval</b> (minutes to hours), then rapid deterioration as the arterial clot expands. "
        "It is a neurosurgical emergency.",
        "<b>Subdural hematoma</b>: venous bleeding from <b>torn bridging veins</b> between the dura and the arachnoid; it is "
        "<b>crescent-shaped</b> and can cross suture lines. Acute subdurals follow severe injury; chronic subdurals develop over weeks in "
        "older adults (brain atrophy stretches the veins), people who misuse alcohol, and those taking anticoagulants.",
        "<b>Subarachnoid hemorrhage</b>: blood in the subarachnoid space (CSF space), from trauma or a ruptured aneurysm, causing a "
        "sudden severe headache and meningeal irritation (neck stiffness, photophobia).",
        "<b>All four</b> can cause headache, nausea and vomiting. This client also has a <b>contusion</b> (bruised brain tissue) of the "
        "left frontal lobe, on the opposite side from the blow: a <b>coup-contrecoup</b> (polar) injury, where the brain strikes the skull "
        "at the impact site (coup) and then rebounds against the opposite side (contrecoup)."),
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
        "text": "The client's deterioration is most likely caused by [[drop0]]. Because the skull cannot expand, the added [[drop1]] volume "
                "was at first offset by moving [[drop2]] out of the skull. That compensation has now failed, and the rising ICP is causing "
                "[[drop3]].",
        "dropdowns": [
            dropdown(("a second concussion", False), ("expansion of the epidural hematoma", True), ("a postictal state", False),
                     ("dehydration from vomiting", False), seed="u7c2-d0"),
            dropdown(("brain tissue", False), ("cerebrospinal fluid", False), ("blood", True), seed="u7c2-d1"),
            dropdown(("cerebrospinal fluid and venous blood", True), ("arterial blood and brain tissue", False),
                     ("brain tissue only", False), ("interstitial fluid into the lungs", False), seed="u7c2-d2"),
            dropdown(("herniation of the left frontal lobe under the falx", False),
                     ("herniation of the right temporal lobe (uncus) that compresses cranial nerve III and the brainstem", True),
                     ("compression of the spinal cord at C1", False), ("bleeding into the left frontal contusion", False),
                     seed="u7c2-d3"),
        ],
    },
    "explanation": rationale(
        "<b>Expanding epidural hematoma:</b> the client had a brief loss of consciousness, a lucid interval (talking, “a bit better”), and "
        "now rapid deterioration, the classic course of an arterial epidural bleed.",
        "<b>Monro-Kellie doctrine:</b> the adult skull is a rigid box holding about 80% brain tissue, 10% blood and 10% CSF. If one volume "
        "increases (here, <b>blood</b> from the hematoma), ICP stays normal only if another decreases: CSF is pushed into the spinal "
        "subarachnoid space and absorbed faster, and venous blood is squeezed out. Once these small reserves are used up, a little more "
        "volume causes a steep rise in ICP (normal ICP is 5 to 15 mm Hg).",
        "<b>Uncal (transtentorial) herniation:</b> the expanding right temporal clot pushes the medial temporal lobe (uncus) through the "
        "tentorial notch. It compresses <b>cranial nerve III on the same side</b> (right pupil dilated and sluggish) and the brainstem "
        "motor tracts, which cross below, causing <b>weakness on the opposite side</b> (left). Falling GCS and <b>Cushing's triad</b> "
        "(BP 174/70 mm Hg with a widened pulse pressure, bradycardia of 56 beats/min, irregular respirations) are late signs that the "
        "brainstem is being compressed. This needs emergency surgical evacuation of the clot.",
        "<b>Why not the others:</b> a second concussion would not cause a unilateral dilated pupil or Cushing's triad; there was no seizure; "
        "two episodes of vomiting do not explain focal signs."),
})

# ---------------------------------------------------------------- Screen 4: matrix indicated / contraindicated (generate solutions)
C.notes("nn", "Nurses' Notes",
    ("2130", "Returned from the operating room after emergency right temporal craniotomy and evacuation of the epidural hematoma (bleeding "
     "middle meningeal artery coagulated). Admitted to the neurological ICU. Intubated and mechanically ventilated; sedated with propofol. "
     "Intraparenchymal ICP monitor in place: ICP 12 mm Hg. Pupils 3 mm, equal and reactive."))
C.notes("ord", "Provider Orders",
    ("2130", "Head of bed 30 degrees; head and neck midline.<br>"
     "ICP and CPP monitoring: notify for ICP above 22 mm Hg or CPP below 60 mm Hg.<br>"
     "Keep SBP at or above 110 mm Hg; SpO₂ at or above 94%; PaCO₂ 35–45 mm Hg; temperature below 38° C; blood glucose 6–10 mmol/L.<br>"
     "0.9% sodium chloride IV at 80 mL/h.<br>"
     "Propofol infusion and fentanyl infusion, titrate to the sedation scale; fentanyl 25 mcg IV PRN for coughing or agitation.<br>"
     "3% sodium chloride 250 mL IV over 30 minutes PRN for ICP above 22 mm Hg for more than 5 minutes.<br>"
     "Acetaminophen 650 mg per NG tube every 6 hours PRN for temperature above 38° C.<br>"
     "Levetiracetam 500 mg IV every 12 hours for 7 days (seizure prophylaxis)."))
s4 = screen(4, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from 2130 and the Provider Orders.",
    "stem": "The nurse plans care to prevent secondary brain injury. For each intervention, click to specify whether it is "
            "<b>indicated</b> or <b>contraindicated</b>.",
    "matrix": matrix_mc("Intervention", ["Indicated", "Contraindicated"], [
        ("Keep the head and neck in midline alignment and avoid tight endotracheal tube ties around the neck", 0),
        ("Hyperventilate the client routinely to keep the PaCO₂ near 25 mm Hg", 1),
        ("Report a systolic BP below 110 mm Hg promptly", 0),
        ("Position the client with the hips flexed more than 90 degrees", 1),
        ("Change the maintenance IV fluid to 5% dextrose in water", 1),
        ("Give the prescribed acetaminophen and use cooling measures for a temperature above 38° C", 0),
        ("Hyperoxygenate before suctioning and limit each suction pass to 10 seconds or less", 0),
        ("Group the bath, linen change, suctioning, and repositioning into one long session", 1),
    ]),
    "explanation": rationale(
        "<b>Secondary brain injury</b> is the damage that develops in the hours and days after the primary injury (the impact, fracture "
        "and bleed). Ischemia triggers an injury cascade: glutamate release, calcium entry into cells, free radicals and inflammation. "
        "Failing cell membrane pumps let sodium and water into cells (<b>cytotoxic edema</b>), and damage to the blood-brain barrier lets "
        "plasma leak into the brain (<b>vasogenic edema</b>), both raising ICP. Hypoxia, hypotension, hypercapnia or excessive "
        "hypocapnia, fever, seizures, and high or low glucose all worsen it, so nursing care aims to prevent each one.",
        "<b>Indicated:</b> a midline head and neck and loose tube ties keep the jugular veins open for venous drainage. Low BP lowers "
        "cerebral perfusion pressure (CPP = MAP − ICP); guidelines keep SBP at or above 110 mm Hg in adults aged 15 to 49. Fever raises "
        "brain metabolism and blood flow, so it is treated promptly. Suctioning raises ICP, so it is kept brief and preceded by "
        "hyperoxygenation.",
        "<b>Contraindicated:</b> routine hyperventilation lowers PaCO₂ and constricts cerebral vessels, reducing ICP briefly but causing "
        "ischemia; it is not used to prevent ICP rises (only briefly, on order, for signs of herniation). Hip flexion above 90 degrees "
        "raises intra-abdominal and intrathoracic pressure and impedes venous return from the head. D5W becomes free water once the "
        "glucose is used and worsens cerebral edema; isotonic 0.9% sodium chloride is used. Long clusters of care cause sustained ICP "
        "rises; activities are spaced with rest periods."),
})

# ---------------------------------------------------------------- Screen 5: select all (take action)
C.notes("nn", "Nurses' Notes",
    ("Day 2 0400", "Client coughing and pushing against the ventilator during repositioning; sedation scale shows light sedation. ICP "
     "26 mm Hg for the last 10 minutes; MAP 78 mm Hg. Head turned to the right on the pillow. Skin warm and flushed."))
C.vitals("Day 2 0400", vs("38.6° C", "96 beats/min", "16 breaths/min (ventilator)", "112/61 mm Hg", "97% (ventilator, FiO₂ 0.40)"))
s5 = screen(5, INTRO, C, {
    "type": "select_all",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 2 0400 and the Vital Signs from Day 2 0400.",
    "stem": "Which actions should the nurse take? <b>Select all that apply.</b>",
    "options": opts(
        ("Reposition the head to midline and confirm the head of the bed is at 30 degrees", True),
        ("Lower the head of the bed flat to increase blood flow to the brain", False),
        ("Administer the prescribed PRN fentanyl", True),
        ("Administer the prescribed 3% sodium chloride", True),
        ("Give the prescribed acetaminophen and apply cooling measures", True),
        ("Suction the endotracheal tube every 15 minutes to prevent coughing", False),
        ("Notify the provider of the ICP and the CPP", True),
        ("Complete the morning bed bath now while the client is awake", False),
        seed="u7c2-s5"),
    "explanation": rationale(
        "<b>CPP = MAP − ICP = 78 − 26 = 52 mm Hg</b>, below the target of 60 to 70 mm Hg, and the ICP has been above 22 mm Hg for more "
        "than 5 minutes. Coughing against the ventilator, a head turned to one side (kinked jugular veins) and fever (38.6° C) are all "
        "raising it.",
        "<b>Correct:</b> straighten the head and keep the head of the bed at 30 degrees to improve venous drainage. Give the PRN fentanyl "
        "for coughing and agitation. Give the 3% sodium chloride as ordered: hypertonic saline draws water out of brain tissue into the "
        "blood. Treat the fever (acetaminophen, cooling) to lower brain metabolism. Notify the provider, because the ICP and CPP are "
        "outside the ordered limits.",
        "<b>Incorrect:</b> lying flat reduces venous drainage and raises ICP. Frequent routine suctioning triggers coughing and raises ICP; "
        "suction only when needed. Nonurgent care (a bed bath) is postponed while ICP is high."),
})

# ---------------------------------------------------------------- Screen 6: matrix (evaluate)
C.notes("nn", "Nurses' Notes",
    ("Day 9 1000", "Extubated on Day 4; transferred to the neurosurgical unit on Day 5. GCS 15. Mild headache (2/10), tires easily, and "
     "says bright screens bother him. Incision healing. Discharge home with his parents today; follow-up with neurosurgery in 2 weeks. "
     "The nurse reviews the discharge teaching with the client."))
C.vitals("Day 9 1000", vs("36.8° C", "76 beats/min", "16 breaths/min", "124/74 mm Hg", "98% on room air"))
s6 = screen(6, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 9 1000 and the Vital Signs from Day 9 1000.",
    "stem": "For each statement the client makes, click to specify whether it indicates an <b>understanding</b> of the discharge teaching "
            "or a <b>need for further teaching</b>.",
    "matrix": matrix_mc("Client Statement", ["Understanding", "Needs further teaching"], [
        ("“I'll wear a certified helmet every time I ride my longboard or bike.”", 0),
        ("“I can go back to playing hockey as soon as my headache is gone.”", 1),
        ("“A few beers at the party this weekend won't affect how my brain heals.”", 1),
        ("“I'll drive myself to my follow-up appointment next week.”", 1),
        ("“If my headache gets much worse, I keep vomiting, or I get very sleepy or confused, I'll go to emergency.”", 0),
        ("“I'll start with short periods of light activity and limit screen time, then increase slowly if my symptoms don't get "
         "worse.”", 0),
    ]),
    "explanation": rationale(
        "<b>Understanding:</b> most TBIs are preventable (falls, motor vehicle and bicycle crashes, sports and assaults are the main "
        "causes in Canada); a certified helmet, seat belts, fall prevention and not riding or driving impaired reduce the risk. Worsening "
        "headache, repeated vomiting, drowsiness or confusion can mean a new bleed or rising ICP and need emergency care. After a brain "
        "injury, a short period of relative rest is followed by a <b>gradual</b> return to light activity and screen use, increased only "
        "if symptoms do not worsen.",
        "<b>Needs further teaching:</b> return to contact sport needs a stepwise plan and clearance by the neurosurgeon (after a "
        "craniotomy and a second brain injury, this may take months or not be advised); a further injury before recovery causes greater "
        "damage. Alcohol slows recovery, impairs judgment (raising the risk of another injury) and lowers the seizure threshold. Driving "
        "is not allowed until the provider clears him (attention, reaction time and seizure risk after a brain injury)."),
})

write_case(2,
    "19-year-old male client who fell from a longboard without a helmet: concussion picture, then a right temporal epidural hematoma "
    "with a lucid interval and uncal herniation (Monro-Kellie doctrine, Cushing's triad), care after craniotomy to prevent secondary "
    "brain injury (ICP, CPP), and discharge teaching on TBI prevention and graded return to activity.",
    [s1, s2, s3, s4, s5, s6],
    ["- Learning outcomes: TBI definition/etiology/prevention, coup-contrecoup and contusion, concussion (pathophysiology, older grades), "
     "epidural vs subdural vs subarachnoid bleeding, secondary injury, Monro-Kellie, ICP manifestations, CPP.",
     "- Targets follow the Brain Trauma Foundation 4th edition (SBP ≥ 110 mm Hg, ICP > 22 mm Hg, CPP 60–70 mm Hg); your course text may "
     "give other numbers (for example, ICP 20 mm Hg).",
     "- Clinician review: orders in the Provider Orders tab (doses) and the return-to-sport statement."],
    "TBI")
