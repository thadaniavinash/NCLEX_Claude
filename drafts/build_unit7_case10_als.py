"""NURS 1017 Unit 7 Case Study 10: amyotrophic lateral sclerosis (ALS) cared for at home.

Nursing focus (OpenStax 17.4 nursing care of the patient with ALS: assess speech, eating, hand use, breathing; prioritize life-
sustaining functions such as breathing and eating; sustain life and independence; breathing support; speech, physical and
occupational therapy; mental health support; palliative care and end-of-life planning). Pathophysiology (degeneration of upper and
lower motor neurons; sensation and usually cognition spared) is kept to the rationales.
"""
from unit7_common import (NeuroChart, vs, opts, dropdown, matrix_mc, matrix_mr, rationale, screen, write_case)

INTRO = "The home care nurse is visiting a 58-year-old male client who was diagnosed with amyotrophic lateral sclerosis (ALS) 14 months ago."
C = NeuroChart()

# ---------------------------------------------------------------- Screen 1: select all (recognize)
C.notes("nn", "Nurses' Notes",
    ("Week 1 1000", "Home visit. Lives with his wife in a bungalow; retired electrician. Uses a power wheelchair; hands weak, needs help "
     "with buttons and cutting food. Wife reports he coughs and clears his throat during most meals, and meals now take about an "
     "hour; he often stops eating because he is tired. Voice sounds wet and gurgly after drinking water. Weight 64 kg (68 kg two months "
     "ago). Sleeps in his recliner because he is short of breath lying flat; wakes with headaches and dozes during the day. Weak cough. "
     "Twitching visible in both forearms and the tongue. Speech slow and slurred but understandable; alert, does the crossword daily. "
     "Sensation intact. Wife says, “I haven't slept a full night in weeks; I'm afraid he'll choke when I'm asleep.”"))
C.vitals("Week 1 1000", vs("36.7° C", "88 beats/min", "22 breaths/min, shallow", "124/76 mm Hg", "93% on room air"))
s1 = screen(1, INTRO, C, {
    "type": "select_all",
    "stem": "The nurse reviews the assessment. Which findings require follow-up? <b>Select all that apply.</b>",
    "options": opts(
        ("Coughing during most meals and a wet, gurgly voice after drinking", True),
        ("Weight loss of 4 kg in 2 months", True),
        ("Twitching of the forearm muscles", False),
        ("Sleeps in a recliner because he is short of breath lying flat", True),
        ("Morning headaches and daytime sleepiness", True),
        ("Sensation intact", False),
        ("Wife has not slept a full night in weeks", True),
        ("Does the crossword daily", False),
        ("SpO₂ 93% with shallow breathing at 22 breaths/min", True),
        seed="u7c10-s1"),
    "explanation": rationale(
        "<b>Require follow-up:</b> coughing during meals and a wet voice are signs of <b>dysphagia</b> with aspiration. Losing 4 kg "
        "in 2 months shows he is not meeting his nutritional needs (long, tiring meals). Shortness of breath lying flat (orthopnea), "
        "morning headaches, daytime sleepiness, shallow breathing and a low SpO₂ suggest <b>weakening breathing muscles</b>, with "
        "carbon dioxide building up during sleep. His wife's exhaustion and fear signal <b>caregiver strain</b>, which affects them "
        "both.",
        "<b>Expected:</b> twitching muscles (fasciculations) are typical of ALS. Sensation and thinking are usually preserved, as here.",
        "<b>Why:</b> ALS is a progressive disease that destroys <b>upper and lower motor neurons</b> in the brain and spinal cord. "
        "Without nerve input, muscles weaken, waste and twitch; weakness spreads to the muscles of speech, swallowing and breathing. "
        "Most people live 2 to 5 years after diagnosis, and respiratory failure is the usual cause of death."),
})

# ---------------------------------------------------------------- Screen 2: matrix multiple response (analyze)
s2 = screen(2, INTRO, C, {
    "type": "matrix_mr",
    "stem": "For each finding, click to specify the nursing problem or problems it relates to: <b>risk for aspiration</b>, "
            "<b>ineffective breathing pattern</b>, or <b>imbalanced nutrition: less than body requirements</b>. Each finding may "
            "relate to more than one problem.",
    "matrix": matrix_mr("Finding", ["Risk for aspiration", "Ineffective breathing pattern", "Imbalanced nutrition"], [
        ("Wet, gurgly voice after drinking", [0]),
        ("Weight loss of 4 kg in 2 months", [2]),
        ("Weak cough", [0, 1]),
        ("Short of breath lying flat", [1]),
        ("Meals take an hour, and he stops eating because he is tired", [0, 2]),
        ("Morning headaches and daytime sleepiness", [1]),
    ]),
    "explanation": rationale(
        "<b>Risk for aspiration:</b> weak tongue, throat and swallowing muscles let food and fluid enter the airway (wet voice, coughing "
        "during meals). A weak cough cannot clear what is aspirated, and fatigue late in a long meal makes swallowing less safe.",
        "<b>Ineffective breathing pattern:</b> weak diaphragm and chest muscles cause shallow breathing and shortness of breath lying "
        "flat (the abdominal contents push up on a weak diaphragm). Breathing becomes shallower during sleep, CO₂ rises, and he wakes "
        "with headaches and is sleepy during the day. A weak cough also reflects weak breathing muscles.",
        "<b>Imbalanced nutrition:</b> long, tiring meals and fear of choking reduce intake; weight loss also comes from muscle wasting "
        "and the extra work of breathing."),
})

# ---------------------------------------------------------------- Screen 3: drop-down cloze (prioritize)
s3 = screen(3, INTRO, C, {
    "type": "dropdown_cloze",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {
        "text": "The nurse's highest priority is the client's [[drop0]], followed by his [[drop1]]. Because his [[drop2]] are usually "
                "preserved in ALS, the nurse involves him directly in decisions about his care.",
        "dropdowns": [
            dropdown(("weakening breathing", True), ("muscle twitching", False), ("weak hands", False), ("slurred speech", False),
                     seed="u7c10-d0"),
            dropdown(("risk for aspiration during meals", True), ("hobby of doing crosswords", False),
                     ("use of a power wheelchair", False), ("normal blood pressure", False), seed="u7c10-d1"),
            dropdown(("thinking and sensation", True), ("swallowing and breathing", False), ("walking and hand strength", False),
                     ("speech and voice", False), seed="u7c10-d2"),
        ],
    },
    "explanation": rationale(
        "<b>Breathing first, then swallowing:</b> in ALS, problems with life-sustaining functions (breathing and eating) take "
        "priority. Signs of nighttime hypoventilation and a low SpO₂ come first, because respiratory failure is the main threat to life. "
        "Aspiration is next, because it can cause pneumonia and choking.",
        "<b>Involving him in decisions:</b> ALS usually spares thinking, sensation, bladder and bowel control and eye movements. He can "
        "make his own decisions about breathing support, a feeding tube and end-of-life care, and these conversations should happen "
        "early, while he can still speak."),
})

# ---------------------------------------------------------------- Screen 4: select all (generate solutions)
s4 = screen(4, INTRO, C, {
    "type": "select_all",
    "stem": "The nurse plans care with the client, his wife and the ALS clinic team. Which interventions should the nurse include? "
            "<b>Select all that apply.</b>",
    "options": opts(
        ("Sit him fully upright for meals and for 30 minutes afterwards", True),
        ("Have him drink thin liquids through a straw so they go down faster", False),
        ("Request a speech-language pathology swallowing assessment", True),
        ("Offer small, frequent, high-calorie meals and a dietitian referral", True),
        ("Discuss with the team a trial of noninvasive ventilation (BiPAP) at night", True),
        ("Introduce a communication device now, while his speech is still understandable", True),
        ("Encourage vigorous strength training to rebuild his muscles", False),
        ("Arrange respite care and connect his wife with the ALS Society support program", True),
        ("Avoid talking about future care so he does not become upset", False),
        seed="u7c10-s4"),
    "explanation": rationale(
        "<b>Include:</b> an upright position (with a chin-tuck if the speech-language pathologist recommends it) protects the airway. "
        "The speech-language pathologist recommends safe food textures (often thickened liquids) and techniques; the dietitian plans "
        "calorie-dense meals and, if weight loss continues, a discussion of a feeding tube (gastrostomy). Noninvasive ventilation at "
        "night relieves hypoventilation, morning headaches and fatigue. Communication devices (including voice banking and eye-gaze "
        "devices) are easier to learn before speech is lost. Respite and support (ALS Canada and provincial ALS societies) reduce "
        "caregiver strain.",
        "<b>Do not include:</b> straws deliver liquid quickly to the back of the throat and raise aspiration risk. Vigorous exercise "
        "causes fatigue; gentle range-of-motion and stretching are used to keep joints mobile. Avoiding conversations about future care "
        "takes away his chance to plan; advance care planning is started early and revisited."),
})

# ---------------------------------------------------------------- Screen 5: select all (take action)
C.notes("nn", "Nurses' Notes",
    ("Week 10 1400", "Uses BiPAP at night; gastrostomy tube placed in Week 6. Advance directive completed: he wants noninvasive "
     "ventilation and comfort care, and does not want intubation or CPR. Today the wife calls the nurse to the bedroom: client sitting "
     "slumped in his recliner, breathing fast and shallow, using his neck muscles, saliva pooling in his mouth, says in a whisper “can't "
     "breathe.” Anxious. Lungs: coarse crackles on the right."))
C.vitals("Week 10 1400", vs("38.1° C", "112 beats/min", "30 breaths/min, shallow", "132/80 mm Hg", "86% on room air"))
s5 = screen(5, INTRO, C, {
    "type": "select_all",
    "preamble": "The nurse has reviewed the Nurses' Notes from Week 10 1400 and the Vital Signs from Week 10 1400.",
    "stem": "Which actions should the nurse take? <b>Select all that apply.</b>",
    "options": opts(
        ("Reposition him upright with his head supported", True),
        ("Suction the saliva from his mouth with the oral suction device", True),
        ("Apply his BiPAP mask", True),
        ("Have his wife call 9-1-1 and ask for intubation", False),
        ("Lay him flat to rest", False),
        ("Contact the provider and the palliative care team about the change", True),
        ("Give him a glass of water to loosen the secretions", False),
        ("Stay with him and explain each action in a calm voice", True),
        seed="u7c10-s5"),
    "explanation": rationale(
        "He is in respiratory distress, likely from aspiration pneumonia (fever, crackles on the right, SpO₂ 86%), on top of weak "
        "breathing muscles.",
        "<b>Correct:</b> sitting upright with the head supported eases breathing and protects the airway. Clearing pooled saliva "
        "reduces further aspiration. His BiPAP supports ventilation and is within his stated wishes. The provider and palliative care "
        "team decide on treatment that matches his goals (for example, antibiotics, oxygen, medications that ease breathlessness and "
        "secretions). Staying with him and explaining what is happening reduces fear, which worsens breathlessness.",
        "<b>Incorrect:</b> intubation is against his advance directive; the nurse respects his documented wishes (emergency services "
        "can be called for transport only if that fits his goals). Lying flat worsens breathing and aspiration. He cannot swallow "
        "safely, so oral fluids would cause more aspiration."),
})

# ---------------------------------------------------------------- Screen 6: matrix (evaluate)
C.notes("nn", "Nurses' Notes",
    ("Week 12 1000", "Treated at home with antibiotics through the gastrostomy tube; fever resolved. Home visit: sleeps 6 hours with "
     "BiPAP and no longer wakes with headaches. Weight 64 kg, stable for 4 weeks on gastrostomy feeds. Uses an eye-gaze communication "
     "device to choose activities and talk with his grandchildren. A respite worker comes 2 afternoons a week. Wife gives the tube "
     "feeding with him lying flat “so he can nap.” Red area over the sacrum that does not blanch."))
C.vitals("Week 12 1000", vs("36.8° C", "84 beats/min", "20 breaths/min", "122/74 mm Hg", "94% on room air"))
s6 = screen(6, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Week 12 1000 and the Vital Signs from Week 12 1000.",
    "stem": "For each finding, click to specify whether it shows that an <b>expected outcome has been met</b> or that it <b>requires "
            "follow-up</b>.",
    "matrix": matrix_mc("Finding", ["Expected outcome met", "Requires follow-up"], [
        ("Sleeps 6 hours with BiPAP without morning headaches", 0),
        ("Wife gives tube feedings while he lies flat", 1),
        ("Weight stable for 4 weeks", 0),
        ("Red area over the sacrum that does not blanch", 1),
        ("Uses an eye-gaze device to make choices and talk with family", 0),
        ("Respite worker visits 2 afternoons a week", 0),
    ]),
    "explanation": rationale(
        "<b>Outcomes met:</b> nighttime ventilation is working (restful sleep, no CO₂ headaches); his weight is stable; he communicates "
        "and takes part in decisions and family life; his wife has regular respite. These match the OpenStax goals for ALS: symptoms "
        "controlled, quality of life and as much independence as possible.",
        "<b>Require follow-up:</b> tube feedings are given with the head of the bed (or recliner) raised at least 30 to 45 degrees and "
        "kept up for 30 to 60 minutes afterwards, to prevent reflux and aspiration; the nurse reteaches his wife. Non-blanching redness "
        "is a stage 1 pressure injury: he needs a pressure-redistributing cushion and mattress, regular repositioning and skin checks."),
})

write_case(10,
    "58-year-old male client with ALS cared for at home: recognizing dysphagia, nighttime hypoventilation, weight loss and caregiver "
    "strain; linking findings to nursing problems; prioritizing breathing and swallowing; an interprofessional plan (SLP, dietitian, "
    "BiPAP, communication device, respite, advance care planning); respiratory distress managed within his advance directive; and "
    "evaluation of outcomes.",
    [s1, s2, s3, s4, s5, s6],
    ["- Nursing-focused case following OpenStax 17.4 (nursing care of the patient with ALS), including palliative care and advance "
     "care planning.",
     "- Screen 5 tests respecting an advance directive (no intubation); please confirm this suits your course.",
     "- Clinician review: wording about BiPAP, tube-feeding position and the respiratory distress scenario."],
    "ALS")
