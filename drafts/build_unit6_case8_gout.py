"""NURS 1017 Unit 6 Case Study 8: acute gouty arthritis and long-term urate control (outcome: gout).
Nursing focus, no treatment decisions."""
from unit6_common import *

ID = "case_1782400000008"
INTRO = "The nurse in an urgent care clinic is caring for a 58-year-old male client with sudden, severe pain in his right foot."
C = Chart()

# ---------------------------------------------------------------- Screen 1 (recognize cues): select all
C.notes("nn", "Nurses' Notes", ("Day 1 0730",
    "Woke at 0300 with severe pain in his right big toe; says even the bedsheet touching it was unbearable. Pain 9/10. The joint at the "
    "base of the right great toe is red, hot, swollen, and shiny; he cannot bear weight on the foot. Attended a wedding yesterday, where "
    "he drank 6 beers and ate shrimp and other seafood. Had two similar attacks in the left big toe in the past year that went away on "
    "their own in about a week. Firm, chalky, nontender nodule on the rim of the left ear. Medical history: hypertension "
    "(hydrochlorothiazide 25 mg daily), obesity (weight 112 kg, BMI 35), chronic kidney disease. Drinks 2 cans of regular cola most days. "
    "Hands: no joint swelling; no morning stiffness."))
C.vitals("Day 1 0730", vs("37.9° C", "96 beats/min", "18 breaths/min", "152/94 mm Hg", "97% on room air"))
s1 = screen(1, INTRO, C, {
    "type": "select_all",
    "stem": "The nurse reviews the client's history and assessment. Which of the following findings would be consistent with <b>acute gouty arthritis</b>? <b>Select all that apply.</b>",
    "options": opts(
        ("Sudden, severe pain that woke him at 0300", True),
        ("Red, hot, swollen, shiny joint at the base of the right great toe", True),
        ("Cannot tolerate the bedsheet touching the toe", True),
        ("Attack began after drinking beer and eating seafood", True),
        ("Previous attacks that went away on their own in about a week", True),
        ("Firm, chalky nodule on the rim of the left ear", True),
        ("No joint swelling or morning stiffness in the hands", False),
        ("Respiratory rate 18 breaths/min", False),
        ("SpO₂ 97% on room air", False),
        seed="c8s1"),
    "explanation": rationale(
        "<b>Typical of acute gout:</b> attacks start suddenly, often at night, and reach maximal pain within 12 to 24 hours. The first "
        "metatarsophalangeal joint of the big toe is the classic site (<b>podagra</b>). The joint is red, hot, swollen and shiny and so "
        "tender that even a bedsheet hurts. Untreated attacks usually settle in 1 to 2 weeks, and the client is symptom-free between "
        "attacks.",
        "<b>Triggers:</b> alcohol (especially beer, which is rich in purines) and purine-rich foods such as shellfish and organ meats raise "
        "uric acid; dehydration, fasting and surgery can also trigger attacks.",
        "<b>Tophi:</b> firm, chalky deposits of urate crystals under the skin (ear rim, elbows, fingers) show long-standing high urate "
        "levels (chronic tophaceous gout). A low-grade fever can accompany an acute attack.",
        "<b>Not consistent:</b> the absence of hand involvement and morning stiffness, and his normal breathing and oxygen saturation, do not point "
        "toward gout."),
})

# ---------------------------------------------------------------- Screen 2 (analyze cues): matrix multiple response
C.labs("Day 1 0800", [
    (lab("White blood cell (WBC) count", "3.5–10.5 × 10<sup>9</sup>/L"), "11.4 × 10<sup>9</sup>/L"),
    (lab("C-reactive protein (CRP)", "≤ 10 mg/L"), "64 mg/L"),
    (lab("Uric acid", "Male: 208–400 µmol/L"), "528 µmol/L"),
    (lab("Creatinine", "Male: 49–93 µmol/L"), "118 µmol/L"),
])
C.notes("dx", "Diagnostic Results",
    ("Day 1 0845", "<b>Joint fluid, right first metatarsophalangeal joint (aspiration):</b> cloudy, yellow; WBC 24 × 10<sup>9</sup>/L, "
     "mostly neutrophils; <b>needle-shaped, negatively birefringent monosodium urate crystals</b> seen under polarized light. Gram stain: "
     "no organisms seen. Culture pending."))
s2 = screen(2, INTRO, C, {
    "type": "matrix_mr",
    "preamble": "The nurse has reviewed the Laboratory Results and the Diagnostic Results.",
    "stem": "A hot, swollen joint can be gout or a joint infection. For each finding, click to specify whether it is consistent with "
            "<b>gout</b>, <b>septic arthritis</b>, or both. Each finding may support more than one condition.",
    "matrix": matrix_mr("Finding", ["Gout", "Septic arthritis"], [
        ("Needle-shaped, negatively birefringent crystals in the joint fluid", [0]),
        ("Red, hot, swollen, very painful single joint", [0, 1]),
        ("Bacteria seen on Gram stain of the joint fluid", [1]),
        ("Temperature 37.9° C and WBC 11.4 × 10⁹/L", [0, 1]),
        ("Chalky nodules (tophi) on the ear", [0]),
        ("Earlier attacks that settled on their own within about a week", [0]),
        ("Joint fluid culture growing Staphylococcus aureus", [1]),
    ]),
    "explanation": rationale(
        "<b>Both:</b> gout and septic arthritis can both produce a single red, hot, swollen, very painful joint with fever, a raised WBC count "
        "and raised CRP. Because an infected joint can be destroyed within days, joint fluid is aspirated to tell them apart; the two can "
        "also occur together.",
        "<b>Gout:</b> the diagnostic finding is <b>monosodium urate crystals</b>, needle-shaped and negatively birefringent under polarized "
        "light, inside neutrophils in the joint fluid. Tophi and earlier attacks that resolved on their own support gout. This client's joint "
        "fluid showed urate crystals and no organisms on Gram stain; the culture is pending.",
        "<b>Septic arthritis:</b> bacteria on Gram stain or a positive culture (most often <i>Staphylococcus aureus</i>) confirm infection. "
        "Septic arthritis does not settle on its own and needs urgent treatment.",
        "<b>Note on uric acid:</b> his serum uric acid is high (528 µmol/L), but it can be normal during an acute attack, so a normal level "
        "does not rule out gout; the crystals do."),
})

# ---------------------------------------------------------------- Screen 3 (prioritize hypotheses): cloze
s3 = screen(3, INTRO, C, {
    "type": "dropdown_cloze",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {
        "text": "Uric acid is the end product of the breakdown of [[drop0]]. Gout develops when [[drop1]]. The client's hydrochlorothiazide "
                "and chronic kidney disease raise his uric acid because they [[drop2]]. The nurse's priority at this time is the client's "
                "[[drop3]].",
        "dropdowns": [
            dropdown(("purines", True), ("amino acids", False), ("fatty acids", False), ("glucose", False), seed="c8s3a"),
            dropdown(("urate in body fluids exceeds its solubility and forms crystals in and around joints", True),
                     ("antibodies attack the joint cartilage", False),
                     ("calcium deposits replace the synovium", False), seed="c8s3b"),
            dropdown(("reduce the excretion of uric acid by the kidneys", True), ("increase the production of purines", False),
                     ("increase the absorption of purines from food", False), seed="c8s3c"),
            dropdown(("acute pain", True), ("risk for infection", False), ("impaired skin integrity", False),
                     ("chronic kidney disease", False), seed="c8s3d"),
        ],
    },
    "explanation": rationale(
        "<b>Where uric acid comes from:</b> purines (from the body's own cell turnover and from foods such as organ meats, shellfish, some "
        "fish and beer) are broken down to uric acid, which is excreted mainly by the kidneys. About 90% of people with gout are "
        "<b>underexcreters</b> rather than overproducers.",
        "<b>Crystal formation:</b> when urate rises above its solubility (about 400 µmol/L), monosodium urate crystals form, more easily in "
        "cooler, peripheral joints such as the big toe and in acidic conditions. Shed crystals are engulfed by neutrophils and activate the "
        "inflammasome, releasing interleukin-1 and producing intense acute inflammation.",
        "<b>Contributing factors:</b> thiazide diuretics and kidney disease reduce uric acid excretion; obesity, alcohol and fructose (as in "
        "regular cola) increase uric acid.",
        "<b>Priority:</b> the attack causes severe pain (9/10) that prevents him from walking. Joint infection was made unlikely by the joint "
        "fluid (urate crystals, no organisms), his skin is intact, and his kidney disease is a long-term issue to follow up, not the immediate problem."),
})

# ---------------------------------------------------------------- Screen 4 (generate solutions): select all
C.notes("nn", "Nurses' Notes", ("Day 1 1000",
    "Diagnosis of acute gout discussed with the client. The provider has prescribed an anti-inflammatory medication for the attack. "
    "Client asks what he can do at home to ease the pain."))
s4 = screen(4, INTRO, C, {
    "type": "select_all",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 1 1000.",
    "stem": "Which actions should the nurse include in the plan of care during the acute attack? <b>Select all that apply.</b>",
    "options": opts(
        ("Rest and elevate the right foot", True),
        ("Apply a cold pack wrapped in a cloth to the toe for 15 to 20 minutes at a time", True),
        ("Use a bed cradle or footboard to keep the bedsheet off the toe", True),
        ("Give the prescribed anti-inflammatory medication and reassess the pain", True),
        ("Encourage 2 to 3 litres of fluid a day, unless the provider sets a limit", True),
        ("Apply a heating pad to the toe", False),
        ("Massage the joint to disperse the crystals", False),
        ("Offer aspirin for the pain", False),
        ("Wrap the toe snugly in an elastic bandage", False),
        seed="c8s4"),
    "explanation": rationale(
        "<b>Correct:</b> rest and elevation reduce swelling and pain. Cold reduces inflammation and pain in an acute gout attack (wrapped, "
        "for limited periods to protect the skin). A bed cradle keeps the weight of the sheets off the exquisitely tender joint. Taking the "
        "prescribed medication early in the attack shortens it; the nurse reassesses pain afterward. Fluids help the kidneys excrete uric "
        "acid and reduce the risk of urate kidney stones; because he has chronic kidney disease, the nurse checks whether the provider has "
        "set a fluid limit.",
        "<b>Incorrect:</b> heat increases the inflammation of an acute attack. Massage or pressure on the joint is extremely painful and "
        "does not remove crystals. Aspirin (salicylate) can raise uric acid levels by competing with its excretion in the kidney, so it is "
        "avoided for gout pain. A snug bandage puts pressure on the swollen, tender joint."),
})

# ---------------------------------------------------------------- Screen 5 (take action): matrix
C.notes("nn", "Nurses' Notes", ("Day 28 1000",
    "Follow-up visit. The attack resolved in 5 days. The provider has started allopurinol 100 mg PO daily, to be increased gradually to "
    "lower his uric acid, and has replaced hydrochlorothiazide with another antihypertensive. The nurse begins teaching about preventing "
    "future attacks."))
C.notes("dx", "Diagnostic Results", ("Day 3 0900", "<b>Joint fluid culture:</b> no growth."))
C.vitals("Day 28 1000", vs("36.7° C", "80 beats/min", "16 breaths/min", "138/86 mm Hg", "98% on room air"))
s5 = screen(5, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 28 1000, the Diagnostic Results from Day 3, and the Vital Signs from "
                "Day 28.",
    "stem": "For each instruction, click to specify whether it is <b>appropriate</b> or <b>not appropriate</b> to include in the "
            "client's teaching.",
    "matrix": matrix_mc("Instruction", ["Appropriate", "Not appropriate"], [
        ("Take allopurinol every day, even when you have no pain", 0),
        ("Fast for a few days to lose weight quickly", 1),
        ("Limit beer and spirits, and avoid binge drinking", 0),
        ("Stop the allopurinol if your toe starts to hurt again", 1),
        ("Limit organ meats, shellfish, and sardines", 0),
        ("Replace regular cola and other sugar-sweetened drinks with water", 0),
        ("Stop taking allopurinol and call your provider right away if you develop a skin rash", 0),
        ("Avoid all milk products, because they contain purines", 1),
    ]),
    "explanation": rationale(
        "<b>Appropriate:</b> allopurinol lowers uric acid production and must be taken every day to prevent attacks and dissolve tophi; it "
        "does not relieve an attack. Beer and spirits raise uric acid; organ meats, shellfish and some oily fish are high in purines; "
        "fructose in sugar-sweetened drinks increases uric acid production. A rash on allopurinol can be the first sign of a rare but "
        "life-threatening hypersensitivity reaction (including Stevens-Johnson syndrome), so the drug is stopped and the rash reported at "
        "once.",
        "<b>Not appropriate:</b> fasting and crash diets raise uric acid (ketones compete with its excretion) and can trigger attacks; weight "
        "loss should be gradual. Attacks can still happen in the first months of urate-lowering therapy as crystals dissolve; stopping "
        "allopurinol during an attack makes urate levels swing and prolongs the problem, so the client calls the provider instead. Low-fat "
        "dairy products are low in purines and are associated with lower uric acid levels, so they are encouraged."),
})

# ---------------------------------------------------------------- Screen 6 (evaluate outcomes): matrix
C.notes("nn", "Nurses' Notes",
    ("Day 120 1000", "Follow-up visit, 4 months after the first attack. No further attacks. Weight 107 kg (was 112 kg). Drinks about 2.5 L "
     "of water a day. Tophus on the left ear slightly smaller. Has had an itchy red rash on both forearms for 2 days and is still taking "
     "allopurinol."),
    ("Day 120 1015", "Client states: “I take my allopurinol every morning.” “I still have 6 or 7 beers on Saturday nights with my "
     "friends.” “I switched from cola to water and low-fat milk.”"))
C.vitals("Day 120 1000", vs("36.6° C", "76 beats/min", "16 breaths/min", "132/82 mm Hg", "98% on room air"))
C.labs("Day 120 0900", [
    (lab("Uric acid", "Male: 208–400 µmol/L"), "352 µmol/L"),
    (lab("Creatinine", "Male: 49–93 µmol/L"), "112 µmol/L"),
])
s6 = screen(6, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 120 1000 and 1015, the Vital Signs from Day 120, and the Laboratory "
                "Results from Day 120.",
    "stem": "For each finding, click to specify whether it indicates that the plan of care has been <b>effective</b> or <b>not "
            "effective</b>.",
    "matrix": matrix_mc("Finding", ["Effective", "Not effective"], [
        ("Uric acid 352 µmol/L", 0),
        ("“I still have 6 or 7 beers on Saturday nights.”", 1),
        ("No further attacks in 3 months", 0),
        ("Tophus on the left ear slightly smaller", 0),
        ("Weight 107 kg, down from 112 kg", 0),
        ("“I switched from cola to water and low-fat milk.”", 0),
        ("“I take my allopurinol every morning.”", 0),
        ("Itchy red rash on both forearms for 2 days", 1),
    ]),
    "explanation": rationale(
        "<b>Effective:</b> a uric acid below 360 µmol/L is the usual treatment target, low enough for crystals to dissolve; the shrinking "
        "tophus shows this is happening. He has had no further attacks, is losing weight gradually, takes allopurinol daily, and has "
        "replaced sugary drinks.",
        "<b>Not effective:</b> binge drinking of beer raises uric acid and dehydrates him, and is a common trigger of attacks. The nurse "
        "reinforces limiting alcohol and explores support for cutting down. A new rash while taking allopurinol must not be ignored: as "
        "taught, the drug is held and the provider is notified the same day, because a rash can be the first sign of a serious "
        "hypersensitivity reaction. His kidney function remains reduced and continues to be monitored."),
})

write_case(ID, 8,
    "58-year-old male client with hypertension on a thiazide, obesity and chronic kidney disease who has an acute gout attack of the right "
    "great toe after beer and seafood; gout vs septic arthritis (joint fluid crystals), purine metabolism and urate crystal formation, "
    "nursing care during the attack, prevention teaching for allopurinol and diet, and evaluation at 4 months.",
    [s1, s2, s3, s4, s5, s6],
    ["The acute-attack medication is left generic (“an anti-inflammatory medication”) so no question depends on the provider's choice.",
     "Screen 4: fluids of 2 to 3 L/day are qualified by “unless the provider sets a limit” because of his kidney disease.",
     "Screen 6: the uric acid target (< 360 µmol/L) follows common guidelines."])
