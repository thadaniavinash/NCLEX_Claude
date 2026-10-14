"""NURS 1017 Unit 6 Case Study 4: osteoporosis with a vertebral compression fracture (outcomes:
osteoporosis; types of fractures; complications). Nursing focus, no treatment decisions."""
from unit6_common import *

ID = "case_1782400000004"
INTRO = "The nurse in the emergency department is caring for a 72-year-old female client with sudden mid-back pain."
C = Chart()

# ---------------------------------------------------------------- Screen 1 (recognize cues): highlight
S1_NOTE = [("Day 1 1030",
    "Reports sudden, severe mid-back pain that began 2 days ago when she lifted a bag of potting soil. Pain 8/10, worse when sitting or "
    "standing and eased by lying down. History: {menopause at age 44|correct}; {takes prednisone 10 mg daily for the past 2 years for "
    "polymyalgia rheumatica|correct}; {takes amlodipine for hypertension}. {Weight 48 kg, height 158 cm (BMI 19.2).|correct} "
    "{Smokes 10 cigarettes per day.|correct} {Drinks 1 glass of wine on weekends.} {Avoids milk and cheese because “dairy upsets my "
    "stomach.”|correct} {Walks her dog for 30 minutes every day.} {Her mother fractured her hip at age 75.|correct} Tender over the "
    "lower thoracic spine; increased thoracic curvature. Strength 5/5 in both legs; sensation intact; voided without difficulty.")]
C.notes("nn", "Nurses' Notes", *S1_NOTE)
C.vitals("Day 1 1030", vs("36.8° C", "88 beats/min", "18 breaths/min", "148/86 mm Hg", "96% on room air"))
s1 = screen(1, INTRO, C, {
    "type": "highlight",
    "stem": "The nurse reviews the Nurses' Notes. <b>Highlight</b> the findings that are risk factors for osteoporosis.",
    "options": [],
    "highlightTabs": [highlight_tab("ht1", "Nurses' Notes", S1_NOTE)],
    "maxCorrectSelections": None,
    "explanation": rationale(
        "<b>Risk factors for osteoporosis:</b>",
        "<b>Early menopause (before 45):</b> estrogen restrains osteoclasts. When estrogen falls, bone resorption speeds up, and an early "
        "menopause means more years of rapid loss.",
        "<b>Long-term glucocorticoids</b> (7.5 mg/day or more of prednisone for 3 months or longer is the usual threshold): they suppress "
        "osteoblasts, increase resorption and reduce calcium absorption. This is the most common cause of secondary osteoporosis.",
        "<b>Low body weight</b> (small frame, BMI under about 20): less mechanical load on the bones and less estrogen produced by fat "
        "tissue.",
        "<b>Smoking:</b> toxic to osteoblasts and lowers estrogen levels.",
        "<b>Low calcium intake:</b> avoiding dairy without other calcium sources means the body takes calcium from bone to keep blood "
        "levels normal.",
        "<b>Parental hip fracture:</b> a strong family risk factor, reflecting inherited peak bone mass.",
        "<b>Not risk factors:</b> one glass of wine on weekends (risk rises with 3 or more drinks a day), daily walking (weight-bearing "
        "exercise protects bone) and amlodipine."),
})

# ---------------------------------------------------------------- Screen 2 (analyze cues): cloze
C.notes("dx", "Diagnostic Results",
    ("Day 1 1115", "<b>X-ray, thoracic and lumbar spine:</b> anterior wedge compression fracture of T12 with about 30% loss of vertebral "
     "height; older wedge deformity of T8. Diffuse osteopenia. No retropulsed fragments."),
    ("Day 1 1400", "<b>Bone mineral density (DEXA):</b> lumbar spine T-score −3.1; left femoral neck T-score −2.7."))
C.labs("Day 1 1100", [
    (lab("Calcium, total", "2.12–2.52 mmol/L"), "2.30 mmol/L"),
    (lab("Phosphate (PO₄)", "0.81–1.58 mmol/L"), "1.10 mmol/L"),
    (lab("Alkaline phosphatase", "50–136 IU/L"), "98 IU/L"),
    (lab("Vitamin D (25-hydroxyvitamin D)", "75–250 nmol/L"), "42 nmol/L"),
    (lab("Creatinine", "Female: 22–75 µmol/L"), "68 µmol/L"),
])
s2 = screen(2, INTRO, C, {
    "type": "dropdown_cloze",
    "preamble": "The nurse has reviewed the Diagnostic Results and the Laboratory Results.",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {
        "text": "The client's lumbar spine T-score of −3.1 indicates [[drop0]]. Osteoporosis develops when [[drop1]]. Her normal serum "
                "calcium [[drop2]]. Her low vitamin D level contributes to bone loss because vitamin D is needed to [[drop3]].",
        "dropdowns": [
            dropdown(("osteoporosis", True), ("osteopenia", False), ("normal bone density for her age", False), seed="c4s2a"),
            dropdown(("bone resorption by osteoclasts exceeds bone formation by osteoblasts", True),
                     ("bone matrix is formed normally but is not mineralized", False),
                     ("bacteria destroy the bone matrix", False), seed="c4s2b"),
            dropdown(("does not rule out osteoporosis, because the body keeps blood calcium normal by taking calcium from bone", True),
                     ("shows that her bones are healthy", False),
                     ("means she does not need calcium in her diet", False), seed="c4s2c"),
            dropdown(("absorb calcium from the intestine", True), ("excrete calcium in the urine", False),
                     ("produce estrogen", False), seed="c4s2d"),
        ],
    },
    "explanation": rationale(
        "<b>T-score:</b> the number of standard deviations the client's bone density differs from that of a healthy young adult. "
        "−1.0 or higher is normal; between −1.0 and −2.5 is <b>osteopenia</b> (low bone mass); <b>−2.5 or lower is osteoporosis</b>. "
        "A fragility fracture (a fracture from a force that would not break a healthy bone, such as lifting a bag of soil) also indicates "
        "osteoporosis.",
        "<b>Pathophysiology:</b> bone is remodeled throughout life. In osteoporosis, resorption by osteoclasts outpaces formation by "
        "osteoblasts, so bone mass falls and the trabeculae thin and break, making the bone porous and fragile. The bone that is formed is "
        "normally mineralized; failure of mineralization is osteomalacia.",
        "<b>Serum calcium</b> is tightly controlled by parathyroid hormone, which releases calcium from bone when intake is low. A normal "
        "blood calcium therefore says nothing about bone density.",
        "<b>Vitamin D</b> increases the absorption of calcium (and phosphate) from the intestine. When it is low, less calcium is absorbed, "
        "parathyroid hormone rises and more calcium is taken from bone."),
})

# ---------------------------------------------------------------- Screen 3 (prioritize hypotheses): matrix
s3 = screen(3, INTRO, C, {
    "type": "matrix_mc",
    "stem": "The nurse is monitoring the client after the vertebral compression fracture. For each finding, click to specify whether it is "
            "<b>expected</b> with a stable vertebral compression fracture or <b>requires immediate follow-up</b>.",
    "matrix": matrix_mc("Finding", ["Expected", "Requires immediate follow-up"], [
        ("Back pain that is worse when sitting or standing and eased by lying down", 0),
        ("New weakness of both legs", 1),
        ("Tenderness over the T12 spinous process", 0),
        ("Numbness of the buttocks and inner thighs (saddle area)", 1),
        ("Pain that wraps around the trunk in a band at the level of the fracture", 0),
        ("Unable to void for 8 hours, with a distended bladder", 1),
        ("Increased forward curvature of the thoracic spine", 0),
    ]),
    "explanation": rationale(
        "<b>Expected:</b> a compression fracture causes sudden, localized back pain over the fractured vertebra that worsens with upright "
        "posture (load on the spine) and eases when lying down. Irritation of the nerve roots at that level can cause pain that wraps "
        "around the trunk in a band. Repeated wedge fractures of the front of the thoracic vertebrae increase the forward curve (kyphosis, "
        "the “dowager's hump”) and cause loss of height.",
        "<b>Require immediate follow-up:</b> new leg weakness, numbness in the saddle area, and urinary retention (or new incontinence) "
        "suggest that bone fragments or collapse are compressing the spinal cord or the cauda equina. These are emergencies; the nurse "
        "keeps the client flat, reports at once, and continues neurologic checks."),
})

# ---------------------------------------------------------------- Screen 4 (generate solutions): select all
C.notes("nn", "Nurses' Notes", ("Day 2 0900",
    "Admitted to the medical unit for pain control and mobilization. Pain 5/10 with movement after analgesia. Strength 5/5 and sensation "
    "intact in both legs; voiding without difficulty. Physiotherapy to begin today. Client says, “I'm afraid to move. What if I break "
    "something else?”"))
C.vitals("Day 2 0900", vs("36.7° C", "80 beats/min", "16 breaths/min", "138/80 mm Hg", "97% on room air"))
s4 = screen(4, INTRO, C, {
    "type": "select_all",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 2 0900 and the Vital Signs from Day 2 0900.",
    "stem": "Which interventions should the nurse include in the client's plan of care? <b>Select all that apply.</b>",
    "options": opts(
        ("Give the prescribed analgesic about 30 minutes before physiotherapy and walking", True),
        ("Teach the client to get out of bed by rolling onto her side and pushing up with her arms", True),
        ("Check leg strength, sensation, and bladder function every shift", True),
        ("Keep the bed low, the call bell in reach, and nonslip footwear on when walking", True),
        ("Encourage calcium-rich foods she tolerates, such as fortified soy beverage, canned salmon with bones, and almonds", True),
        ("Keep the client on bed rest until the pain is gone", False),
        ("Teach her to bend at the waist with straight knees when picking up objects", False),
        ("Teach sit-ups and toe-touching exercises to strengthen her back", False),
        ("Use a soft, deep chair that she sinks into for comfort", False),
        seed="c4s4"),
    "explanation": rationale(
        "<b>Correct:</b> pain relief before activity allows early, safe mobilization. Rolling to the side and pushing up keeps the spine "
        "straight (no twisting or flexion). Regular neurologic and bladder checks detect cord compression early. Falls are the main cause "
        "of new fractures, so fall precautions are essential. Calcium intake matters, and lactose-free or non-dairy sources suit a client "
        "who avoids milk.",
        "<b>Incorrect:</b> bed rest speeds up bone loss and causes deconditioning, pneumonia and blood clots; walking is encouraged as soon "
        "as pain allows. Bending at the waist and flexion exercises (sit-ups, toe touches) load the front of the vertebrae and can cause "
        "new compression fractures; lifting is done with bent knees and a straight back. A deep, soft chair forces the spine into flexion "
        "and makes standing up hard; a firm chair with arms is safer."),
})

# ---------------------------------------------------------------- Screen 5 (take action): matrix
C.notes("nn", "Nurses' Notes", ("Day 4 1000",
    "Walking in the hallway with a walker; pain 3/10. Discharge planned for tomorrow. Alendronate 70 mg PO once weekly, calcium carbonate "
    "500 mg PO twice daily, and vitamin D₃ 2,000 IU PO daily have been prescribed. The nurse begins discharge teaching."))
s5 = screen(5, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 4 1000.",
    "stem": "For each instruction, click to specify whether it is <b>appropriate</b> or <b>not appropriate</b> to include in the "
            "client's discharge teaching.",
    "matrix": matrix_mc("Instruction", ["Appropriate", "Not appropriate"], [
        ("Take alendronate first thing in the morning with a full glass of plain water, before any food, drink, or other medicine", 0),
        ("Lie down for a few minutes after taking alendronate if you feel dizzy", 1),
        ("Take the alendronate tablet with breakfast and your calcium tablet", 1),
        ("Stay sitting or standing upright for at least 30 minutes after taking alendronate", 0),
        ("Report heartburn, pain or difficulty swallowing, or chest pain", 0),
        ("Tell your dentist that you take alendronate before any dental surgery", 0),
        ("Take calcium carbonate with meals", 0),
        ("Remove loose rugs and use night lights between the bedroom and bathroom", 0),
    ]),
    "explanation": rationale(
        "<b>Alendronate</b> (a bisphosphonate) slows bone resorption by osteoclasts. It is poorly absorbed and irritates the esophagus, so "
        "it is taken on an empty stomach with a full glass of plain water, at least 30 minutes before food, drinks (including coffee) or "
        "other medicines, and the client stays upright for at least 30 minutes. Lying down lets the tablet reflux and cause esophagitis or "
        "ulcers; taking it with food or calcium blocks its absorption. Heartburn, painful swallowing or chest pain can signal esophageal "
        "injury. Osteonecrosis of the jaw is a rare risk, so dentists should know before invasive dental work.",
        "<b>Calcium carbonate</b> needs stomach acid to be absorbed, so it is taken with meals, and at a different time from alendronate.",
        "<b>Fall prevention</b> at home (no loose rugs, night lights, grab bars, good lighting) prevents the falls that cause most "
        "osteoporotic fractures."),
})

# ---------------------------------------------------------------- Screen 6 (evaluate outcomes): matrix
C.notes("nn", "Nurses' Notes",
    ("Day 90 1000", "Clinic follow-up, 3 months after discharge. Pain 2/10; walks 20 minutes most days. Strength and sensation normal in "
     "both legs; voiding without difficulty. Reports heartburn and pain when swallowing for the past week. Has cut down to 5 cigarettes "
     "per day."),
    ("Day 90 1015", "Client states: “I take my alendronate with my morning coffee to save time.” “I took out the hallway rugs and put in "
     "night lights.” “I have a fortified soy drink or canned salmon most days.” “I bend over from the waist to fill my dog's dish; it's "
     "quicker.”"))
C.labs("Day 90 0900", [
    (lab("Calcium, total", "2.12–2.52 mmol/L"), "2.34 mmol/L"),
    (lab("Vitamin D (25-hydroxyvitamin D)", "75–250 nmol/L"), "84 nmol/L"),
])
s6 = screen(6, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 90 1000 and 1015 and the Laboratory Results from Day 90.",
    "stem": "For each finding, click to specify whether it indicates that the plan of care has been <b>effective</b> or <b>not "
            "effective</b>.",
    "matrix": matrix_mc("Finding", ["Effective", "Not effective"], [
        ("Pain 2/10 and walking 20 minutes most days", 0),
        ("“I take my alendronate with my morning coffee to save time.”", 1),
        ("Vitamin D 84 nmol/L", 0),
        ("Heartburn and pain when swallowing for the past week", 1),
        ("“I took out the hallway rugs and put in night lights.”", 0),
        ("“I bend over from the waist to fill my dog's dish.”", 1),
        ("“I have a fortified soy drink or canned salmon most days.”", 0),
        ("Normal strength and sensation in both legs; voiding without difficulty", 0),
    ]),
    "explanation": rationale(
        "<b>Effective:</b> pain is controlled and she is walking regularly (weight-bearing exercise helps maintain bone). Her vitamin D is "
        "now in the normal range. She has made her home safer and includes calcium-rich foods she tolerates. No neurologic signs of cord "
        "compression.",
        "<b>Not effective:</b> taking alendronate with coffee blocks its absorption and suggests she may not stay upright or wait before "
        "eating; together with her new heartburn and painful swallowing this points to esophageal irritation, which the nurse reports to "
        "the provider. Bending from the waist loads the front of the vertebrae and risks another compression fracture; the nurse reteaches "
        "bending at the knees with a straight back. Her reduced smoking is progress, and continued cessation support is offered."),
})

write_case(ID, 4,
    "72-year-old female client with a T12 vertebral compression fracture after lifting a bag of soil; osteoporosis risk factors "
    "(early menopause, long-term prednisone, low weight, smoking, low calcium intake, parental hip fracture), T-scores and "
    "pathophysiology, red flags for cord compression, safe mobilization and fall prevention, alendronate and calcium teaching, and "
    "evaluation at 3 months.",
    [s1, s2, s3, s4, s5, s6],
    ["Screen 1: the risk factors follow Osteoporosis Canada / FRAX-style criteria (glucocorticoids ≥ 7.5 mg/day for ≥ 3 months, "
     "BMI under about 20, current smoking, parental hip fracture); check that they match your textbook.",
     "Screen 5: alendronate instructions follow the Canadian product monograph (upright at least 30 minutes)."])
