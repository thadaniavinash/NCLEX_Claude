"""NURS 1017 Unit 7 Case Study 9: a young adult with epilepsy admitted after a breakthrough seizure.

Nursing focus (OpenStax 17.5 nursing care of the patient with seizures): history and possible triggers, observing and describing
seizures (classification), seizure precautions, care during and after a seizure, documentation (onset, duration, aura, postictal
period), 5-minute emergency threshold, medication adherence and trigger teaching, safety, coping, and evaluation.
Different from Case Studies 3 and 4 (seizures as complications of meningitis and a brain tumour) and from Unit 7 Stand-alones.
"""
from unit7_common import (NeuroChart, vs, opts, dropdown, matrix_mc, rationale, highlight_tab, screen, write_case, bowtie)

INTRO = "The nurse on a medical unit is caring for a 20-year-old female university student with epilepsy."
C = NeuroChart()

# ---------------------------------------------------------------- Screen 1: highlight (recognize)
S1 = [("Day 1 1600", "Admitted for observation after a tonic-clonic seizure in the university library this morning; brought in by "
       "ambulance. Diagnosed with epilepsy at age 15; takes levetiracetam 750 mg PO twice daily. Says she {ran out of levetiracetam 3 "
       "days ago and has not had time to refill it|correct}. Has been {studying for final exams, sleeping about 4 hours a night for "
       "the past week|correct}. {Drank 5 beers at a friend's party last night|correct}. {Skipped breakfast and lunch today|correct}. "
       "{Had a coffee before going to the library}. The library has {ordinary overhead lighting}. {Exercises at the campus gym 3 times "
       "a week}. Before today, her last seizure was 14 months ago. Now alert and oriented; {sore tongue with a small bite on the "
       "right side}; muscles ache.")]
C.notes("nn", "Nurses' Notes", *S1)
C.vitals("Day 1 1600", vs("36.9° C", "84 beats/min", "16 breaths/min", "116/72 mm Hg", "99% on room air"))
s1 = screen(1, INTRO, C, {
    "type": "highlight",
    "stem": "The nurse reviews the Nurses' Notes. <b>Highlight</b> the findings that may have contributed to the client's seizure.",
    "options": [],
    "highlightTabs": [highlight_tab("ht1", "Nurses' Notes", S1)],
    "maxCorrectSelections": None,
    "explanation": rationale(
        "<b>Possible contributors (triggers):</b>",
        "<b>Missed antiseizure medication:</b> the most common cause of a breakthrough seizure. Levetiracetam levels fall within a day "
        "or two of stopping it.",
        "<b>Sleep deprivation:</b> one of the strongest seizure triggers; exam periods are a common time for breakthrough seizures in "
        "students.",
        "<b>Alcohol:</b> heavy drinking, and the withdrawal period the next day, lower the seizure threshold.",
        "<b>Skipped meals:</b> low blood glucose and missed routines can trigger seizures.",
        "<b>Not contributors here:</b> a usual amount of coffee, ordinary lighting (flashing or flickering lights affect only people "
        "with photosensitive epilepsy) and regular exercise. The tongue bite is a result of the seizure, not a cause.",
        "<b>What a seizure is:</b> a sudden, abnormal, excessive electrical discharge of a group of neurons that changes movement, "
        "sensation, awareness or behaviour. Epilepsy is a tendency to have recurrent unprovoked seizures."),
})

# ---------------------------------------------------------------- Screen 2: matrix (analyze)
s2 = screen(2, INTRO, C, {
    "type": "matrix_mc",
    "stem": "The client's roommate has witnessed several of her seizures and describes them to the nurse. For each description, click "
            "to specify the type of seizure it is most consistent with.",
    "matrix": matrix_mc("Description", ["Focal aware", "Focal impaired awareness", "Generalized tonic-clonic", "Absence"], [
        ("“She gets a rising feeling in her stomach and smells burning rubber, but she can still talk to me.”", 0),
        ("“She stiffens, falls, and her arms and legs jerk; afterwards she's confused and sleeps for an hour.”", 2),
        ("“She stares, smacks her lips, and fiddles with her sleeve; she doesn't answer me and doesn't remember it later.”", 1),
        ("“When she was a child, she would stare blankly for a few seconds many times a day, then carry on as if nothing happened.”", 3),
        ("“Her right hand twitches for about a minute, and she watches it happen and tells me about it.”", 0),
    ]),
    "explanation": rationale(
        "Accurate observation and description help the provider classify seizures and guide treatment and safety teaching. Seizures "
        "are <b>focal</b> (starting in one area of the brain) or <b>generalized</b> (involving both sides from the start).",
        "<b>Focal aware:</b> the person stays aware. It may be a sensation (a rising feeling in the stomach, an unusual smell) or "
        "movement of one part of the body. A focal aware seizure that comes before a larger seizure is often called an <b>aura</b>, and "
        "it is documented.",
        "<b>Focal impaired awareness:</b> the person is confused or unaware, often with staring and automatisms (lip smacking, "
        "fumbling), and does not remember it afterwards. A focal seizure can spread to both sides and become a tonic-clonic seizure.",
        "<b>Generalized tonic-clonic:</b> stiffening (tonic phase) and a fall, then rhythmic jerking (clonic phase), often with "
        "tongue biting and incontinence, followed by a <b>postictal</b> period of confusion, headache, sore muscles and sleepiness.",
        "<b>Absence:</b> brief (seconds) staring spells, often many times a day, with immediate recovery; most common in children.",
        "<b>Phases:</b> prodrome (warning signs hours before, such as irritability), ictal (the seizure itself) and postictal "
        "(recovery)."),
})

# ---------------------------------------------------------------- Screen 3: drop-down cloze (prioritize)
s3 = screen(3, INTRO, C, {
    "type": "dropdown_cloze",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {
        "text": "While the client is in hospital, the nurse's priority problem is [[drop0]] because [[drop1]]. Before discharge, the "
                "nurse's teaching will focus first on [[drop2]].",
        "dropdowns": [
            dropdown(("disturbed sleep pattern", False), ("risk for injury and aspiration", True), ("anxiety", False),
                     ("imbalanced nutrition", False), seed="u7c9-d0"),
            dropdown(("her levetiracetam levels are low, so another seizure may occur", True),
                     ("she exercises at the gym", False), ("her vital signs are abnormal", False),
                     ("she has a sore tongue", False), seed="u7c9-d1"),
            dropdown(("taking her antiseizure medication every day without running out", True),
                     ("avoiding all caffeine", False), ("avoiding bright overhead lights", False),
                     ("stopping exercise", False), seed="u7c9-d2"),
        ],
    },
    "explanation": rationale(
        "<b>Risk for injury and aspiration:</b> until her medication level is restored, she may have another seizure. During a "
        "tonic-clonic seizure she could fall, strike her head or limbs, or aspirate saliva or vomit, so safety is the first priority.",
        "<b>Teaching priority:</b> running out of medication was the main trigger; daily adherence, refills before the supply ends, and "
        "a plan for missed doses prevent most breakthrough seizures. Sleep, alcohol and meals are taught next. Caffeine in moderation, "
        "ordinary lighting and exercise are not problems for her."),
})

# ---------------------------------------------------------------- Screen 4: select all (generate solutions)
C.notes("ord", "Provider Orders",
    ("Day 1 1630", "Levetiracetam 750 mg PO twice daily (first dose now).<br>"
     "Seizure precautions.<br>"
     "Saline lock IV.<br>"
     "Lorazepam 2 mg IV for a seizure lasting 5 minutes or longer; notify provider of any seizure.<br>"
     "Neurological checks and vital signs every 4 hours."))
s4 = screen(4, INTRO, C, {
    "type": "select_all",
    "preamble": "The nurse has reviewed the Provider Orders.",
    "stem": "Which interventions should the nurse include when setting up seizure precautions for the client? <b>Select all that "
            "apply.</b>",
    "options": opts(
        ("Keep the bed in the lowest position with the side rails up and padded", True),
        ("Keep oxygen and suction equipment ready at the bedside", True),
        ("Tape a padded tongue blade to the head of the bed", False),
        ("Keep the saline lock patent", True),
        ("Take her temperature with an oral glass thermometer", False),
        ("Have her shower with the bathroom door unlocked and a nurse nearby, rather than take a tub bath", True),
        ("Apply wrist restraints while she sleeps", False),
        ("Remove nearby objects that could injure her, such as the bedside table", True),
        seed="u7c9-s4"),
    "explanation": rationale(
        "<b>Include:</b> a low bed with padded rails prevents falls and injury. Oxygen and suction support the airway after a seizure. "
        "A patent IV lets the nurse give lorazepam quickly if a seizure lasts 5 minutes or more. Showers with someone nearby are safer "
        "than tub baths (drowning risk). Hazards near the bed are moved away.",
        "<b>Do not include:</b> nothing is placed in the mouth during a seizure; a tongue blade can break teeth, cause airway "
        "obstruction or injure the nurse. Oral temperatures are avoided, especially with glass or breakable thermometers, because "
        "she could bite down during a seizure; tympanic, temporal or axillary routes are used. Restraints cause injury and are not "
        "used."),
})

# ---------------------------------------------------------------- Screen 5: bowtie (take action)
C.notes("nn", "Nurses' Notes",
    ("Day 2 0610", "Called to the room by the roommate in the next bed at 0607: client lying in bed, unresponsive, with her whole body "
     "stiff, then rhythmic jerking of both arms and legs. Saliva frothing at the mouth. Before the jerking began, she called out "
     "“I smell burning rubber.”"))
s5 = screen(5, INTRO, C, {
    "type": "bowtie",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 2 0610.",
    "stem": "Complete the diagram by dragging from the choices below to specify what condition the client is most likely experiencing, "
            "2 actions the nurse should take to address that condition, and 2 parameters the nurse should monitor to assess the "
            "client's progress.",
    "options": [],
    **bowtie(
        [("A tonic-clonic seizure that began as a focal aware seizure (aura)", True), ("An absence seizure", False),
         ("Fainting (syncope)", False), ("A panic attack", False)],
        [("Turn her onto her side and protect her head", True), ("Note the time the seizure started and how long it lasts", True),
         ("Insert an oral airway between her teeth", False), ("Hold her arms and legs still", False),
         ("Give her sips of water", False)],
        [("Airway and breathing (respiratory pattern and oxygen saturation)", True),
         ("Level of consciousness and orientation during recovery", True), ("Bowel sounds", False),
         ("Capillary refill in the toes", False), ("Urine specific gravity", False)],
        seed="u7c9-bt"),
    "explanation": rationale(
        "<b>Condition:</b> the smell of burning rubber (an aura, a focal aware seizure) followed by loss of consciousness, stiffening "
        "and rhythmic jerking of all limbs is a focal seizure that spread to a bilateral tonic-clonic seizure.",
        "<b>Actions:</b> turning her onto her side lets saliva drain and keeps the tongue from blocking the airway; a pillow or "
        "padding protects her head. Timing the seizure is essential: a seizure lasting 5 minutes or more is an emergency, and the "
        "prescribed lorazepam is given. Nothing is put in the mouth, and her movements are not restrained (injury risk). Nothing is "
        "given by mouth until she is fully awake and can swallow.",
        "<b>Parameters:</b> airway and breathing (respiratory pattern, oxygen saturation; suction and oxygen as needed) and level of "
        "consciousness and orientation through the postictal period (asking her name and location). The nurse documents the aura, "
        "time of onset, the movements, duration, incontinence or injury, and the length of the postictal period, and notifies the "
        "provider."),
})

# ---------------------------------------------------------------- Screen 6: matrix (evaluate)
C.notes("nn", "Nurses' Notes",
    ("Day 2 0614", "Seizure stopped at 0609 (2 minutes). Turned to her left side; oral suction for saliva; oxygen 2 L/min by nasal "
     "cannula; SpO₂ 96%. Postictal: drowsy, oriented to person only at 0630, oriented × 4 at 0715. Provider notified."),
    ("Day 3 1000", "No further seizures. Pharmacist arranged a 3-month supply and automatic refills. Discharge today. The nurse reviews "
     "the teaching with the client; her roommate is present."))
s6 = screen(6, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 2 0614 and Day 3 1000.",
    "stem": "For each statement, click to specify whether it indicates an <b>understanding</b> of the teaching or a <b>need for "
            "further teaching</b>.",
    "matrix": matrix_mc("Statement", ["Understanding", "Needs further teaching"], [
        ("Client: “I'll set alarms on my phone for my levetiracetam and refill it a week before I run out.”", 0),
        ("Client: “If I miss a dose, I'll just take two at the next dose.”", 1),
        ("Client: “I won't drive until my neurologist tells me it's safe under the provincial rules.”", 0),
        ("Client: “I can stay up all night studying as long as I take my pills.”", 1),
        ("Roommate: “If she has a seizure, I'll turn her on her side, time it, and call 9-1-1 if it lasts 5 minutes.”", 0),
        ("Client: “I'll swim only with a friend who knows about my epilepsy.”", 0),
        ("Client: “I'll wear my medical alert bracelet.”", 0),
    ]),
    "explanation": rationale(
        "<b>Understanding:</b> reminders and early refills support adherence, the most important way to prevent seizures. In Canada, "
        "provincial licensing rules restrict driving after a seizure; the neurologist advises when she may drive. Friends who know "
        "seizure first aid (side-lying, timing, call 9-1-1 at 5 minutes, or if she is injured or does not wake up) keep her safe. "
        "Swimming with a knowledgeable companion and wearing a medical alert bracelet are standard safety measures.",
        "<b>Needs further teaching:</b> doubling a missed dose can cause side effects (drowsiness, dizziness); she follows the "
        "pharmacist's instructions, usually taking the missed dose when she remembers unless the next one is due soon. Sleep "
        "deprivation is a trigger even when medications are taken; regular sleep is part of seizure control. The nurse also offers "
        "support for coping with stigma and with exam stress (campus health services, Epilepsy Canada resources)."),
})

write_case(9,
    "20-year-old university student with epilepsy admitted after a breakthrough tonic-clonic seizure: seizure triggers (missed "
    "medication, sleep loss, alcohol, missed meals), describing and classifying seizures from witness accounts, seizure precautions, "
    "care during and after a seizure (bow-tie), documentation, and self-management teaching.",
    [s1, s2, s3, s4, s5, s6],
    ["- Nursing-focused case following OpenStax 17.5 (nursing care of the patient with seizures).",
     "- Screen 5 is a bow-tie (condition, 2 actions, 2 parameters).",
     "- Clinician review: lorazepam order, missed-dose advice for levetiracetam, wording on provincial driving rules."],
    "Epilepsy")
