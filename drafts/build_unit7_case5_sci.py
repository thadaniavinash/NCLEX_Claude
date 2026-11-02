"""NURS 1017 Unit 7 Case Study 5: cervical spinal cord injury from a shallow-water dive.

Learning outcomes: spinal cord injury (definition, etiology, prevention); complications and sequelae: spinal shock, neurogenic shock,
respiratory compromise, autonomic dysreflexia.
Sources checked: OpenStax Medical-Surgical Nursing 17.9 (spinal cord injury); Lewis's Medical-Surgical Nursing in Canada (SCI,
neurogenic shock, autonomic dysreflexia); AANS/CNS acute cervical SCI guidelines (MAP 85-90 mm Hg for 7 days); Consortium for
Spinal Cord Medicine autonomic dysreflexia guideline (sit upright, loosen clothing, check bladder then bowel, SBP >= 150 mm Hg).
"""
from unit7_common import (NeuroChart, vs, lab, opts, dropdown, matrix_mc, matrix_mr, rationale, highlight_tab, screen, write_case)

INTRO = "The nurse in the emergency department is caring for a 22-year-old male client who dove into shallow water at a lake."
C = NeuroChart()

# ---------------------------------------------------------------- Screen 1: highlight (recognize)
S1 = [("Day 1 1430", "Dove headfirst off a dock into about 1 metre of water at 1340 and struck his head on the bottom. {Friends pulled "
       "him out of the water, keeping his head in line with his body}. Arrived by ambulance with a cervical collar and spinal motion "
       "restriction. {Alert and oriented × 4}. States, “I can't feel or move my legs.” Can shrug his shoulders and bend his elbows; "
       "cannot straighten his elbows or move his fingers. No sensation below the clavicles or in the arms and hands except the outer "
       "arms and thumbs. Legs flaccid with no reflexes; no anal sphincter tone. {Breathing is diaphragmatic: the abdomen rises while "
       "the chest barely moves|correct}; {speaks in short sentences|correct}; {weak cough|correct}. {Skin warm, dry and pink below the "
       "injury}. {3-cm abrasion on the forehead}.")]
S1_VS = [("Day 1 1430", "{T 36.4° C}, {P 48 beats/min|correct}, {RR 26 breaths/min, shallow|correct}, {BP 82/48 mm Hg|correct}, "
          "{SpO₂ 93% on room air|correct}.")]
C.notes("nn", "Nurses' Notes", *S1)
C.vitals("Day 1 1430", vs("36.4° C", "48 beats/min", "26 breaths/min, shallow", "82/48 mm Hg", "93% on room air"))
s1 = screen(1, INTRO, C, {
    "type": "highlight",
    "stem": "The nurse reviews the Nurses' Notes and the Vital Signs. <b>Highlight</b> the findings that require immediate follow-up.",
    "options": [],
    "highlightTabs": [highlight_tab("ht1", "Nurses' Notes", S1), highlight_tab("ht2", "Vital Signs", S1_VS)],
    "maxCorrectSelections": None,
    "explanation": rationale(
        "<b>Require immediate follow-up:</b>",
        "<b>Breathing (the first priority):</b> diaphragmatic breathing, short sentences, a weak cough, shallow breathing at 26 "
        "breaths/min and SpO₂ 93% show that the intercostal and abdominal muscles are paralyzed and the diaphragm is doing all the work. "
        "Fatigue and cord swelling can lead to respiratory failure.",
        "<b>BP 82/48 mm Hg with a heart rate of 48 beats/min:</b> hypotension with bradycardia after a cervical injury suggests "
        "<b>neurogenic shock</b>. Low BP reduces blood flow to the injured cord and worsens the secondary injury.",
        "<b>Expected or not urgent:</b> the motor and sensory loss is the injury itself and is documented as the baseline; warm, dry skin "
        "fits neurogenic shock (loss of sympathetic tone) rather than being a separate problem; the friends kept his head in line, which "
        "was correct; being alert and oriented is reassuring; the abrasion and temperature need no immediate action."),
})

# ---------------------------------------------------------------- Screen 2: matrix multiple response (analyze)
C.notes("dx", "Diagnostic Results",
    ("Day 1 1520", "<b>CT cervical spine:</b> fracture-dislocation of C5 on C6 with narrowing of the spinal canal."),
    ("Day 1 1545", "<b>MRI cervical spine:</b> compression and edema of the spinal cord from C5 to C7. Neurological level C6, complete "
     "injury (ASIA Impairment Scale A)."),
    ("Day 1 1550", "<b>FAST ultrasound and CT chest/abdomen:</b> no free fluid or internal bleeding."))
C.labs("Day 1 1440", [
    (lab("Hemoglobin (Hgb)", "Male: 125–170 g/L"), "148 g/L"),
    (lab("Lactate", "0.5–2.5 mmol/L"), "1.6 mmol/L"),
])
s2 = screen(2, INTRO, C, {
    "type": "matrix_mr",
    "preamble": "The nurse has reviewed the Diagnostic Results and the Laboratory Results.",
    "stem": "For each finding, click to specify whether it is consistent with <b>spinal shock</b>, <b>neurogenic shock</b>, or "
            "<b>hypovolemic shock</b>. Each finding may support more than one condition.",
    "matrix": matrix_mr("Finding", ["Spinal shock", "Neurogenic shock", "Hypovolemic shock"], [
        ("Flaccid paralysis and absent reflexes below the level of injury", [0]),
        ("Hypotension", [1, 2]),
        ("Bradycardia", [1]),
        ("Cool, clammy skin", [2]),
        ("Loss of sympathetic nervous system outflow from an injury at T6 or above", [1]),
        ("Warm, dry skin below the injury", [1]),
        ("Tachycardia", [2]),
        ("Loss of bladder and bowel reflexes, including anal sphincter tone", [0]),
    ]),
    "explanation": rationale(
        "A <b>spinal cord injury</b> is damage to the cord from trauma (in Canada, mostly falls and motor vehicle crashes, then sports "
        "and recreation, such as diving into shallow water) or from disease. The primary injury (compression, contusion, laceration) is "
        "followed by a secondary injury (ischemia, edema, inflammation) that can extend the damage over hours to days.",
        "<b>Spinal shock</b> is a <b>neurological</b> state: a temporary loss of all reflex activity below the injury (flaccid "
        "paralysis, no reflexes, no anal tone, bladder and bowel retention). It lasts days to weeks; its end is marked by the return of "
        "reflexes (for example, the bulbocavernosus reflex), followed by spasticity.",
        "<b>Neurogenic shock</b> is a <b>hemodynamic</b> state, a type of distributive shock: an injury at <b>T6 or above</b> cuts the "
        "sympathetic outflow (which leaves the cord from T1 to L2), leaving the vagus nerve unopposed. Vessels dilate (hypotension, "
        "warm, dry skin, poor temperature control) and the heart slows (bradycardia).",
        "<b>Hypovolemic shock</b> from bleeding causes hypotension with <b>tachycardia</b> and cool, clammy skin, because the "
        "sympathetic response is intact. This client's normal hemoglobin and lactate and the scans without bleeding make hypovolemia "
        "unlikely, but bleeding is always ruled out in trauma, because a cervical injury can hide abdominal pain."),
})

# ---------------------------------------------------------------- Screen 3: drop-down cloze (prioritize)
C.notes("nn", "Nurses' Notes",
    ("Day 1 1630", "Vital capacity 1.1 L (predicted 4.8 L). Using neck muscles to breathe; says he feels “tired of breathing.” Oxygen "
     "4 L/min by nasal cannula applied."))
C.vitals("Day 1 1630", vs("36.1° C", "52 beats/min", "28 breaths/min, shallow", "88/52 mm Hg", "95% on 4 L/min nasal cannula"))
s3 = screen(3, INTRO, C, {
    "type": "dropdown_cloze",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 1 1630 and the Vital Signs from Day 1 1630.",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {
        "text": "The client's priority problem is [[drop0]]. His injury spares [[drop1]] but paralyzes [[drop2]]. His breathing may get "
                "worse over the next few days because [[drop3]].",
        "dropdowns": [
            dropdown(("autonomic dysreflexia", False), ("risk for respiratory failure", True), ("impaired skin integrity", False),
                     ("hypothermia", False), seed="u7c5-d0"),
            dropdown(("the vagus nerve", False), ("the T1 nerve roots", False), ("the phrenic nerve (C3–C5), which controls the "
                     "diaphragm", True), ("the spinal accessory nerve", False), seed="u7c5-d1"),
            dropdown(("the diaphragm", False), ("the intercostal and abdominal muscles", True),
                     ("the sternocleidomastoid and trapezius muscles", False), ("the muscles of the face", False), seed="u7c5-d2"),
            dropdown(("edema of the spinal cord can extend upward toward C3–C5", True), ("spinal shock will end", False),
                     ("his heart rate will rise", False), ("autonomic dysreflexia will begin", False), seed="u7c5-d3"),
        ],
    },
    "explanation": rationale(
        "<b>Risk for respiratory failure</b> is the priority: airway and breathing come first. A vital capacity of 1.1 L (about 23% of "
        "predicted), use of accessory neck muscles, fatigue and rising respiratory rate signal that he may need intubation and "
        "ventilation (a vital capacity below about 15 mL/kg, or one that keeps falling, is reported).",
        "<b>Why:</b> “C3, 4 and 5 keep the diaphragm alive”: the <b>phrenic nerve</b> is spared in a C6 injury, so the diaphragm "
        "still works, but the <b>intercostal and abdominal muscles</b> (thoracic nerves) are paralyzed. He cannot expand the chest fully "
        "or cough effectively, so secretions collect (atelectasis, pneumonia). Cord edema peaks in the first days and can climb to C3–C5, "
        "weakening the diaphragm as well.",
        "<b>Why not the others:</b> autonomic dysreflexia begins after spinal shock resolves (usually weeks later). The sternocleidomastoid "
        "and trapezius (spinal accessory nerve, cranial nerve XI) and the face (cranial nerves) are not affected; he is using his neck "
        "muscles to help him breathe."),
})

# ---------------------------------------------------------------- Screen 4: matrix indicated / contraindicated (generate solutions)
C.notes("nn", "Nurses' Notes",
    ("Day 2 0800", "Underwent anterior cervical decompression and fusion of C5–C6 overnight; in a hard cervical collar. Remains on 4 L/min "
     "oxygen; vital capacity 1.3 L. Admitted to the ICU."))
C.notes("ord", "Provider Orders",
    ("Day 2 0800", "Keep MAP 85–90 mm Hg for 7 days: 0.9% sodium chloride, then norepinephrine infusion titrated to MAP.<br>"
     "Atropine 0.5 mg IV PRN for heart rate below 40 beats/min with hypotension.<br>"
     "Vital capacity and cough strength every 4 hours; notify for vital capacity below 1 L.<br>"
     "Hard cervical collar at all times; logroll with 2 staff.<br>"
     "Indwelling urinary catheter; nasogastric tube to low suction.<br>"
     "Enoxaparin 30 mg subcut every 12 hours starting Day 3; sequential compression devices."))
s4 = screen(4, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 2 0800 and the Provider Orders.",
    "stem": "For each intervention, click to specify whether it is <b>indicated</b> or <b>contraindicated</b> for the client.",
    "matrix": matrix_mc("Intervention", ["Indicated", "Contraindicated"], [
        ("Logroll the client with a second nurse holding the head in line with the body", 0),
        ("Suction the airway for longer than 15 seconds to clear thick secretions", 1),
        ("Measure the vital capacity and assess cough strength as ordered", 0),
        ("Raise the head of the bed quickly to 90 degrees to ease his breathing", 1),
        ("Titrate the norepinephrine to keep the MAP at 85–90 mm Hg", 0),
        ("Remove the cervical collar to wash his neck while he lies alone", 1),
        ("Turn him at least every 2 hours and inspect the skin over bony prominences", 0),
        ("Monitor urine output through the indwelling catheter", 0),
    ]),
    "explanation": rationale(
        "<b>Indicated:</b> logrolling with a person at the head keeps the spine aligned after fusion. Vital capacity and cough strength "
        "show early respiratory decline. Keeping the MAP at 85–90 mm Hg improves blood flow to the injured cord and limits secondary "
        "injury. He cannot feel pressure or move, so turning and skin checks prevent pressure injuries. In spinal shock the bladder does "
        "not empty (urinary retention), so the catheter drains it and urine output shows perfusion.",
        "<b>Contraindicated:</b> long suctioning causes hypoxia and stimulates the vagus nerve, which, with no sympathetic opposition, "
        "can cause severe bradycardia or asystole; suctioning is brief, with hyperoxygenation, and atropine is at hand. A quick move to "
        "sitting causes severe orthostatic hypotension (no sympathetic vasoconstriction); the head is raised gradually with the spine "
        "protected. The collar stays on; neck care is done with a second person holding the head."),
})

# ---------------------------------------------------------------- Screen 5: ordered response (take action)
C.notes("nn", "Nurses' Notes",
    ("Week 5 1400", "Rehabilitation unit. Spinal shock resolved in Week 3; reflexes and spasticity in the legs have returned. Client lying "
     "in bed, reports a sudden pounding headache and blurred vision. Face and neck flushed and sweating; skin below the clavicles pale and "
     "cool with goosebumps. Nasal stuffiness. Wearing an abdominal binder and leg straps for the urine drainage bag. Indwelling catheter "
     "bag has had no new urine for 3 hours."))
C.vitals("Week 5 1400", vs("36.8° C", "50 beats/min", "18 breaths/min", "198/108 mm Hg (usual 98/60 mm Hg)", "97% on room air"))
s5 = screen(5, INTRO, C, {
    "type": "ordered_response",
    "preamble": "The nurse has reviewed the Nurses' Notes from Week 5 1400 and the Vital Signs from Week 5 1400.",
    "stem": "Place the nurse's actions in the order in which they should be performed. Arrange from first to last.",
    "options": [],
    "orderedOptions": [
        "Sit the client upright and lower his legs",
        "Loosen the abdominal binder and the leg straps",
        "Check the catheter tubing for kinks or blockage",
        "If urine does not drain, replace the catheter using lidocaine jelly",
        "If the BP stays high after the bladder is emptied, notify the provider",
    ],
    "explanation": rationale(
        "This is <b>autonomic dysreflexia</b>, a life-threatening emergency in clients with an injury at <b>T6 or above</b> once spinal "
        "shock has resolved. A stimulus below the injury (most often a <b>full bladder</b>, then constipation or impaction, pressure "
        "injuries, tight clothing or ingrown toenails) triggers a massive sympathetic reflex below the injury: vasoconstriction causes "
        "severe hypertension (a rise of 20 to 40 mm Hg or more above the client's usual BP), pale cool skin and goosebumps below the "
        "injury. The brain detects the high BP through the baroreceptors, but its inhibitory signals cannot pass the injury, so only the "
        "body above the injury responds: vagal bradycardia, flushing, sweating, nasal stuffiness and a pounding headache. It can cause "
        "seizures, stroke and death.",
        "<b>Order:</b> (1) Sit him up and lower his legs, so blood pools in the legs and the BP falls. (2) Loosen anything tight. "
        "(3) Look for the most common cause, the bladder: check the tubing for kinks. (4) If urine still does not drain, replace the "
        "catheter, using lidocaine jelly to reduce further stimulation. (5) The BP is checked every 2 to 5 minutes; if it stays high "
        "(systolic 150 mm Hg or more) after the bladder is emptied, the provider is notified for a fast-acting antihypertensive and the "
        "bowel is checked next for stool."),
})

# ---------------------------------------------------------------- Screen 6: matrix (evaluate)
C.notes("nn", "Nurses' Notes",
    ("Week 5 1420", "Tubing kinked under his thigh; straightened, 900 mL of urine drained. BP 128/76 mm Hg at 1415, 104/64 mm Hg at 1425. "
     "Headache resolving."),
    ("Week 10 1000", "Discharge planning. The nurse reviews teaching with the client and his brother, who will help with his care at home."))
s6 = screen(6, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Week 5 1420 and Week 10 1000.",
    "stem": "For each statement, click to specify whether it indicates an <b>understanding</b> of the teaching or a <b>need for further "
            "teaching</b>.",
    "matrix": matrix_mc("Statement", ["Understanding", "Needs further teaching"], [
        ("Client: “If I get a pounding headache and my face flushes, I'll sit up right away and check my catheter.”", 0),
        ("Brother: “When his blood pressure goes up, he should lie down flat.”", 1),
        ("Client: “Autonomic dysreflexia only happens in the first few months after an injury.”", 1),
        ("Client: “I'll carry my autonomic dysreflexia wallet card and show it to staff if I go to emergency.”", 0),
        ("Client: “I'll do my bowel program at the same time every day.”", 0),
        ("Brother: “Since he can't feel his legs, we don't need to check his skin.”", 1),
        ("Brother: “Next summer, everyone will check the water depth and go in feet first the first time.”", 0),
    ]),
    "explanation": rationale(
        "<b>Understanding:</b> sitting up and finding the trigger (bladder first) are the first steps. A wallet card helps emergency staff "
        "who may not recognize autonomic dysreflexia. A regular bowel program prevents constipation and impaction, a common trigger. "
        "Most spinal cord injuries are preventable: checking water depth and entering feet first, seat belts, not driving impaired, fall "
        "prevention and safe sport (for example, no checking from behind in hockey).",
        "<b>Needs further teaching:</b> lying flat raises the BP further; the client sits up. Autonomic dysreflexia is a <b>lifelong</b> "
        "risk for injuries at T6 or above. Loss of sensation means he cannot feel pressure or injury, so the skin must be inspected at "
        "least daily (a pressure injury can also trigger autonomic dysreflexia)."),
})

write_case(5,
    "22-year-old male client with a complete C6 spinal cord injury after diving into shallow water: neurogenic vs spinal vs hypovolemic "
    "shock, respiratory risk (phrenic nerve, vital capacity), acute care after fusion, autonomic dysreflexia in rehabilitation, and "
    "teaching on prevention and lifelong self-care.",
    [s1, s2, s3, s4, s5, s6],
    ["- Learning outcomes: SCI definition, etiology and prevention; spinal shock, neurogenic shock, respiratory compromise, autonomic "
     "dysreflexia.",
     "- Screen 5 is an ordered response (sit up, loosen, check tubing, recatheterize, notify); please confirm the order matches your "
     "course text.",
     "- Clinician review: MAP target (85–90 mm Hg for 7 days), atropine and enoxaparin orders, sensory level description."],
    "Spinal_Cord_Injury")
