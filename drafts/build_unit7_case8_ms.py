"""NURS 1017 Unit 7 Case Study 8: multiple sclerosis relapse on a medical unit.

Nursing focus: focused neurological assessment, linking findings to nursing problems (falls, urinary retention and infection,
fatigue), priorities, an individualized plan with PT/OT and mental health support, monitoring during corticosteroid therapy, and
teaching for independence (OpenStax 17.3 nursing care of the patient with MS: assess motor function, coordination, sensation,
fatigue, mood; corticosteroids for exacerbations with monitoring of BP, insomnia and mood; PT; teach active self-management).
Pathophysiology (autoimmune demyelination of the CNS, relapses and remissions, heat sensitivity) is kept to the rationales.
Does not repeat Unit 7 Stand-alones 2 and 3 (MS teaching evaluation, ataxia care planning).
"""
from unit7_common import (NeuroChart, vs, lab, opts, dropdown, matrix_mc, matrix_mr, rationale, screen, write_case)

INTRO = "The nurse on a medical unit is caring for a 34-year-old female client with relapsing-remitting multiple sclerosis (MS)."
C = NeuroChart()

# ---------------------------------------------------------------- Screen 1: select all (recognize)
C.notes("nn", "Nurses' Notes",
    ("Day 1 1400", "Admitted with a relapse of MS. For 5 days her legs have felt weak and stiff, and she has double vision when "
     "looking to the left. Walks with a wide, unsteady gait and holds on to furniture; needed help to the bathroom. Says the weakness "
     "is much worse after a hot shower. Has had urinary urgency with leaking and gets up to void 4 times a night; limits her drinking "
     "to about 800 mL a day “so I don't have accidents.” Bladder scan after voiding: 350 mL. Numbness of the fingertips of both hands, "
     "unchanged for 2 years. Fatigue: needs to rest after dressing. Tearful; says, “I've stopped seeing my friends. I feel like "
     "a burden to my husband.” Works as a dental hygienist; has a 4-year-old son. Wears glasses for reading."))
C.vitals("Day 1 1400", vs("36.9° C", "78 beats/min", "16 breaths/min", "118/74 mm Hg", "98% on room air"))
s1 = screen(1, INTRO, C, {
    "type": "select_all",
    "stem": "The nurse reviews the client's history and assessment. Which findings require follow-up? <b>Select all that apply.</b>",
    "options": opts(
        ("Needs help to walk to the bathroom because of weak, stiff legs and an unsteady gait", True),
        ("Double vision when looking to the left", True),
        ("Bladder scan of 350 mL after voiding", True),
        ("Numbness of the fingertips, unchanged for 2 years", False),
        ("Limits her fluid intake to about 800 mL a day", True),
        ("Temperature 36.9° C", False),
        ("States she has stopped seeing friends and feels like a burden", True),
        ("Wears glasses for reading", False),
        ("Weakness is much worse after a hot shower", True),
        seed="u7c8-s1"),
    "explanation": rationale(
        "<b>Require follow-up:</b> new leg weakness, stiffness (spasticity), an unsteady gait and double vision put her at high risk of "
        "falling. A post-void residual of 350 mL means her bladder is not emptying (urinary retention), and limiting fluids to avoid "
        "accidents concentrates the urine; both raise the risk of a urinary tract infection. Withdrawing from friends and feeling like a "
        "burden can signal depression, which is common in MS and needs screening and support. Worsening weakness after a hot shower "
        "(heat sensitivity) is important for safety and teaching.",
        "<b>Do not require follow-up now:</b> fingertip numbness that has not changed in 2 years is her baseline (the nurse documents it "
        "to compare with later). A normal temperature is expected (and reassuring, because infection and fever can worsen MS symptoms). "
        "Reading glasses are unrelated.",
        "<b>Why MS causes these findings:</b> MS is an autoimmune disease in which immune cells attack the myelin of the brain, optic "
        "nerves and spinal cord. Inflamed, demyelinated areas (plaques) slow or block nerve conduction, so symptoms depend on where the "
        "plaques are: motor weakness and spasticity, double vision, bladder dysfunction, sensory changes and fatigue. In a relapse, new "
        "inflammation causes new or worse symptoms over days; they often improve as inflammation settles (remission)."),
})

# ---------------------------------------------------------------- Screen 2: matrix multiple response (analyze)
s2 = screen(2, INTRO, C, {
    "type": "matrix_mr",
    "stem": "For each finding, click to specify the nursing problem or problems it contributes to: <b>risk for falls</b>, <b>risk for "
            "urinary tract infection</b>, or <b>fatigue</b>. Each finding may contribute to more than one problem.",
    "matrix": matrix_mr("Finding", ["Risk for falls", "Risk for urinary tract infection", "Fatigue"], [
        ("Weak, stiff legs with an unsteady gait", [0]),
        ("Post-void residual of 350 mL", [1]),
        ("Gets up to void 4 times a night", [0, 2]),
        ("Double vision", [0]),
        ("Drinks only about 800 mL a day", [1]),
        ("Weakness worse after a hot shower", [0, 2]),
        ("Needs to rest after dressing", [2]),
    ]),
    "explanation": rationale(
        "<b>Risk for falls:</b> weakness, spasticity and poor balance, double vision (impaired depth perception), hurried trips to the "
        "bathroom at night in the dark, and the temporary weakness that follows heat exposure.",
        "<b>Risk for urinary tract infection:</b> urine left in the bladder (retention) lets bacteria multiply, and a low fluid intake "
        "reduces flushing of the urinary tract. A urinary tract infection, or any fever, can temporarily worsen MS symptoms "
        "(a pseudo-relapse), so prevention matters.",
        "<b>Fatigue:</b> the most common MS symptom; demyelinated nerves need more energy to conduct impulses. Broken sleep from "
        "nocturia and heat make it worse. Heat slows conduction in demyelinated nerves even more, so symptoms worsen temporarily after a "
        "hot shower, exercise in the heat, or a fever (and improve with cooling)."),
})

# ---------------------------------------------------------------- Screen 3: drop-down cloze (prioritize)
s3 = screen(3, INTRO, C, {
    "type": "dropdown_cloze",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {
        "text": "The nurse's priority problem for the client is [[drop0]] because of [[drop1]]. The nurse also addresses her [[drop2]], "
                "which increases her risk of [[drop3]].",
        "dropdowns": [
            dropdown(("fatigue", False), ("risk for falls", True), ("disturbed body image", False), ("chronic sensory loss", False),
                     seed="u7c8-d0"),
            dropdown(("her leg weakness, unsteady gait, double vision, and nighttime trips to the bathroom", True),
                     ("the numbness of her fingertips", False), ("her job as a dental hygienist", False),
                     ("her normal vital signs", False), seed="u7c8-d1"),
            dropdown(("urinary retention and low fluid intake", True), ("reading glasses", False), ("normal temperature", False),
                     ("blood pressure", False), seed="u7c8-d2"),
            dropdown(("a urinary tract infection that can worsen her MS symptoms", True), ("kidney stones from too much fluid", False),
                     ("hypertension", False), ("a pressure injury on her heels", False), seed="u7c8-d3"),
        ],
    },
    "explanation": rationale(
        "<b>Risk for falls is the priority:</b> it is an immediate safety threat. A fall could cause a fracture or head injury and set "
        "back her recovery and independence. Her weakness, gait, double vision and nocturia together make a fall likely, especially at "
        "night.",
        "<b>Urinary retention and low fluid intake</b> come next: they raise the risk of a urinary tract infection, which can worsen MS "
        "symptoms and, if untreated, damage the kidneys. Fatigue and mood are also addressed in the plan, but they are not as urgent as "
        "her physical safety."),
})

# ---------------------------------------------------------------- Screen 4: select all (generate solutions)
C.notes("ord", "Provider Orders",
    ("Day 1 1500", "Methylprednisolone 1 g IV daily for 5 days (first dose 0900 Day 2).<br>"
     "Capillary blood glucose twice daily during methylprednisolone.<br>"
     "Bladder scan after each void; intermittent catheterization if post-void residual is more than 300 mL; teach clean intermittent "
     "self-catheterization.<br>"
     "Physiotherapy and occupational therapy referrals.<br>"
     "Social work referral; screen for depression."))
s4 = screen(4, INTRO, C, {
    "type": "select_all",
    "preamble": "The nurse has reviewed the Provider Orders.",
    "stem": "Which interventions should the nurse include in the client's plan of care? <b>Select all that apply.</b>",
    "options": opts(
        ("Keep the bed in the lowest position with the call bell and a urinal or commode within reach at night", True),
        ("Encourage her to stay in bed until the relapse resolves", False),
        ("Plan care and activities with rest periods in between", True),
        ("Apply a heating pad to her stiff legs", False),
        ("Encourage a fluid intake of about 2 L a day, spread over the day and reduced in the evening", True),
        ("Offer lukewarm, not hot, showers with a shower chair", True),
        ("Ask open-ended questions about her mood and coping, and involve her husband if she wishes", True),
        ("Insert an indwelling urinary catheter to keep her bladder empty", False),
        seed="u7c8-s4"),
    "explanation": rationale(
        "<b>Include:</b> a low bed, the call bell and a commode or urinal close by reduce night-time falls. Pacing activities with rest "
        "conserves energy. A fluid intake of about 2 L a day prevents urinary tract infections; reducing fluids in the evening lessens "
        "nocturia. Lukewarm water and a shower chair avoid heat-related weakness and falls. Talking openly about mood, coping and "
        "family roles, with the social worker's help, supports her mental health. Physiotherapy (strength, stretching for spasticity, "
        "balance, a walking aid) and occupational therapy (energy conservation, home and work adaptations) are part of the team plan.",
        "<b>Do not include:</b> bed rest causes deconditioning and contractures; she stays as active as she safely can. A heating pad "
        "can worsen symptoms and can burn skin with reduced sensation. An indwelling catheter greatly raises infection risk; intermittent "
        "catheterization (done by the nurse, then by the client) empties the bladder with less risk and supports independence."),
})

# ---------------------------------------------------------------- Screen 5: select all (take action)
C.notes("nn", "Nurses' Notes",
    ("Day 3 0200", "Client awake, sitting on the edge of the bed, crying. Says she has not slept since starting the steroid and feels "
     "“wired.” States, “What's the point? I'm going to end up in a wheelchair and my son will grow up with a useless mother.”"))
C.vitals("Day 3 0200", vs("36.8° C", "92 beats/min", "18 breaths/min", "146/90 mm Hg", "98% on room air"))
C.labs("Day 3 0200", [(lab("Glucose, random (capillary)", "4.0–11.0 mmol/L"), "13.6 mmol/L")])
s5 = screen(5, INTRO, C, {
    "type": "select_all",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 3 0200, the Vital Signs from Day 3 0200 and the Laboratory Results.",
    "stem": "Which actions should the nurse take? <b>Select all that apply.</b>",
    "options": opts(
        ("Ask her directly whether she is having thoughts of harming herself or ending her life", True),
        ("Tell her that steroids always cause these feelings, so she should try to ignore them", False),
        ("Stay with her and listen to her concerns", True),
        ("Hold the next methylprednisolone dose until the provider sees her in the morning", False),
        ("Report the glucose, BP, insomnia and mood changes to the provider", True),
        ("Help her back to bed and offer measures that promote sleep, such as dimming the lights and limiting interruptions", True),
        ("Encourage her to walk the hallway alone until she feels tired", False),
        seed="u7c8-s5"),
    "explanation": rationale(
        "<b>Correct:</b> a statement of hopelessness is followed by a direct question about suicidal thoughts; asking does not put the "
        "idea in the person's mind, and it guides immediate safety measures (in Canada, the 9-8-8 Suicide Crisis Helpline is also "
        "available). Staying with her and listening shows respect and lets her express her fears. High-dose corticosteroids commonly "
        "cause insomnia, mood changes, hyperglycemia and raised BP; these are reported so the provider can treat them (for example, "
        "insulin for glucose, a sleep aid, giving the dose early in the day). Sleep-promoting measures help.",
        "<b>Incorrect:</b> dismissing her feelings blocks communication and may miss depression or suicide risk. The nurse does not hold "
        "a prescribed dose without consulting the provider. Walking alone at night with weak legs and double vision risks a fall."),
})

# ---------------------------------------------------------------- Screen 6: matrix (evaluate)
C.notes("nn", "Nurses' Notes",
    ("Day 7 1000", "Leg strength improving; walks on the unit with a 4-wheeled walker and stand-by assistance. Double vision resolved. "
     "Performs clean intermittent self-catheterization every 6 hours; residuals 150–250 mL. Drinks about 2 L a day. Has started "
     "counselling through the MS clinic; depression screen shows mild symptoms. Discharge home tomorrow. The nurse reviews the "
     "discharge teaching with the client and her husband."))
s6 = screen(6, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 7 1000.",
    "stem": "For each statement, click to specify whether it indicates an <b>understanding</b> of the discharge teaching or a "
            "<b>need for further teaching</b>.",
    "matrix": matrix_mc("Statement", ["Understanding", "Needs further teaching"], [
            ("Client: “I'll wash my hands and the catheter, and catheterize every 6 hours, even when I'm busy at work.”", 0),
            ("Husband: “She should stop the disease-modifying injections once she feels back to normal.”", 1),
            ("Client: “If my urine burns, smells bad, or I get a fever, I'll call the MS clinic.”", 0),
            ("Client: “I'll use my walker at home until physiotherapy says I can stop.”", 0),
            ("Client: “I'll save my errands for the hottest part of the afternoon, when I've had time to rest.”", 1),
            ("Husband: “We'll ask the occupational therapist about setting up the kitchen so she can sit while she works.”", 0),
            ("Client: “I'll keep my counselling appointments, even if I'm feeling better.”", 0),
    ]),
    "explanation": rationale(
        "<b>Understanding:</b> clean technique and a regular schedule for self-catheterization prevent infection and overdistension. "
        "Signs of a urinary tract infection are reported early, because infection can worsen MS symptoms. Using the walker until "
        "physiotherapy advises otherwise prevents falls. Sitting to work and arranging the kitchen are energy-conservation strategies. "
        "Continuing counselling supports her coping over the long term.",
        "<b>Needs further teaching:</b> disease-modifying therapies reduce relapses and slow disability; they are continued between "
        "relapses, when she feels well, and are changed only with the neurologist. Heat worsens MS symptoms, so errands are planned for "
        "the cooler parts of the day, with cooling strategies (air conditioning, cooling vest, cool drinks)."),
})

write_case(8,
    "34-year-old female client with a relapse of multiple sclerosis: focused neurological assessment, falls, urinary retention and "
    "infection risk, fatigue and heat sensitivity, nursing priorities and an interprofessional plan, mood and safety during high-dose "
    "corticosteroids, and discharge teaching for self-catheterization, energy conservation and ongoing therapy.",
    [s1, s2, s3, s4, s5, s6],
    ["- Nursing-focused case following OpenStax 17.3 (nursing care of the patient with MS); pathophysiology kept to the rationales.",
     "- Different from Unit 7 Stand-alones 2 and 3 (MS teaching evaluation, ataxia care planning): heat and energy conservation "
     "appear again but in new situations.",
     "- Clinician review: methylprednisolone order, post-void residual threshold (300 mL) and self-catheterization interval."],
    "Multiple_Sclerosis")
