"""NURS 1017 Unit 6 Case Study 3: osteomyelitis from a diabetic foot ulcer (outcome: osteomyelitis;
also complications in bone healing). Nursing focus, no treatment decisions."""
from unit6_common import *

ID = "case_1782400000003"
INTRO = "The home care nurse is visiting a 61-year-old female client with type 2 diabetes for care of a foot ulcer."
C = Chart()

# ---------------------------------------------------------------- Screen 1 (recognize cues): select all
C.notes("nn", "Nurses' Notes", ("Day 1 0930",
    "Home visit for wound care of a plantar ulcer under the right great toe, present for 7 weeks. Type 2 diabetes for 18 years "
    "(metformin 1,000 mg twice daily) with peripheral neuropathy. The ulcer measures 2.0 × 1.5 cm and is deeper than at the last visit; "
    "bone is visible at its base. Purulent, foul-smelling drainage on the dressing. Redness and swelling of the great toe extend 2 cm "
    "onto the forefoot. Client says, “It doesn't hurt at all, so I didn't think it was getting worse.” Her capillary blood glucose "
    "readings have been 14 to 18 mmol/L for the past week (usually 6 to 9 mmol/L). She has been walking barefoot around the house "
    "“to let the foot breathe.” Husband helps with the daily dressing changes. Left foot skin intact, no calluses. Right dorsalis pedis "
    "pulse 1+, left 2+."))
C.vitals("Day 1 0930", vs("38.1° C", "92 beats/min", "18 breaths/min", "136/82 mm Hg", "97% on room air"))
s1 = screen(1, INTRO, C, {
    "type": "select_all",
    "stem": "Which findings require follow-up by the nurse? <b>Select all that apply.</b>",
    "options": opts(
        ("Bone visible at the base of the ulcer", True),
        ("Purulent, foul-smelling drainage", True),
        ("Redness and swelling extending 2 cm onto the forefoot", True),
        ("Temperature 38.1° C", True),
        ("Capillary blood glucose readings of 14 to 18 mmol/L for the past week", True),
        ("Walks barefoot around the house", True),
        ("Blood pressure 136/82 mm Hg", False),
        ("Husband helps with the daily dressing changes", False),
        ("Takes metformin 1,000 mg twice daily", False),
        ("Left foot skin intact with no calluses", False),
        seed="c3s1"),
    "explanation": rationale(
        "<b>Require follow-up:</b>",
        "<b>Bone visible (or felt with a probe) at the base of a foot ulcer</b> strongly suggests that the infection has reached the bone "
        "(osteomyelitis).",
        "<b>Purulent, foul-smelling drainage and spreading redness and swelling</b> show active infection of the soft tissue around the "
        "ulcer. A swollen, red, “sausage-shaped” toe is typical when the bone underneath is infected.",
        "<b>Fever</b> shows a systemic response to the infection.",
        "<b>High blood glucose:</b> infection raises stress hormones (cortisol, catecholamines), which raise blood glucose. Persistent "
        "hyperglycemia in turn impairs neutrophil function and wound healing, so the two worsen each other.",
        "<b>Walking barefoot</b> on an insensate foot puts pressure and trauma on the ulcer. The client's lack of pain is not reassuring: "
        "peripheral neuropathy removes the warning sign, so infection can advance unnoticed.",
        "<b>Do not need follow-up:</b> her blood pressure is acceptable, the husband's help is a strength, metformin is her usual "
        "medication, and the left foot is intact. The weaker right dorsalis pedis pulse is worth noting as a sign of reduced blood flow."),
})

# ---------------------------------------------------------------- Screen 2 (analyze cues): matrix
C.notes("nn", "Nurses' Notes", ("Day 1 1500",
    "Admitted to the medical unit from the clinic. Right great toe red, swollen, and warm; ulcer dressed. Blood cultures drawn. Bone "
    "biopsy of the proximal phalanx scheduled."))
C.labs("Day 1 1430", [
    (lab("White blood cell (WBC) count", "3.5–10.5 × 10<sup>9</sup>/L"), "13.8 × 10<sup>9</sup>/L"),
    (lab("Erythrocyte sedimentation rate (ESR)", "Female: 0–20 mm/h"), "92 mm/h"),
    (lab("C-reactive protein (CRP)", "≤ 10 mg/L"), "118 mg/L"),
    (lab("Glucose, random", "4.0–11.0 mmol/L"), "16.2 mmol/L"),
    (lab("Hemoglobin A1c (HbA1c)", "4.8%–6.0%"), "9.4%"),
    (lab("Creatinine", "Female: 22–75 µmol/L"), "70 µmol/L"),
])
C.notes("dx", "Diagnostic Results",
    ("Day 1 1400", "<b>X-ray, right foot:</b> erosion of the cortex of the proximal phalanx of the great toe with periosteal reaction; "
     "soft-tissue swelling."),
    ("Day 1 1530", "<b>Monofilament test:</b> no sensation at 8 of 10 sites on both feet (loss of protective sensation)."),
    ("Day 1 1700", "<b>MRI, right foot:</b> bone marrow edema of the proximal phalanx of the great toe, continuous with the plantar ulcer. "
     "Consistent with osteomyelitis."))
s2 = screen(2, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 1 1500, the Laboratory Results and the Diagnostic Results.",
    "stem": "For each finding, click to specify whether it is a <b>risk factor</b> for the client's osteomyelitis, a <b>local sign</b> of "
            "bone and soft-tissue infection, or a <b>systemic sign</b> of infection.",
    "matrix": matrix_mc("Finding", ["Risk factor", "Local sign", "Systemic sign"], [
        ("HbA1c 9.4%", 0),
        ("Bone marrow edema on MRI", 1),
        ("WBC 13.8 × 10⁹/L", 2),
        ("Loss of protective sensation on monofilament testing", 0),
        ("Cortical erosion and periosteal reaction on X-ray", 1),
        ("Temperature 38.1° C", 2),
        ("Right dorsalis pedis pulse 1+", 0),
        ("Purulent drainage from the ulcer", 1),
    ]),
    "explanation": rationale(
        "<b>Risk factors:</b> poorly controlled diabetes (HbA1c 9.4%) impairs white blood cell function and healing. Neuropathy (loss of "
        "protective sensation) lets ulcers form and worsen unnoticed. Reduced arterial blood flow (weak pedal pulse) delivers less oxygen, "
        "white blood cells and antibiotic to the tissue.",
        "<b>Local signs:</b> purulent drainage shows infection at the site. The MRI shows marrow edema early, while plain X-rays show bone "
        "destruction (cortical erosion) and new bone laid down by the periosteum only after 10 to 14 days of infection.",
        "<b>Systemic signs:</b> fever and a raised WBC count reflect the body's response to infection. ESR and CRP are also raised (ESR "
        "92 mm/h, CRP 118 mg/L); a very high ESR in a diabetic foot ulcer suggests osteomyelitis, and both are followed to judge the "
        "response to treatment."),
})

# ---------------------------------------------------------------- Screen 3 (prioritize hypotheses): cloze
s3 = screen(3, INTRO, C, {
    "type": "dropdown_cloze",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {
        "text": "Bacteria reached the client's bone by [[drop0]]. Inside the rigid bone, the inflammatory exudate [[drop1]]. Areas of dead "
                "bone, called [[drop2]], are hard for white blood cells and antibiotics to reach. The nurse's priority at this time is to "
                "monitor for [[drop3]].",
        "dropdowns": [
            dropdown(("direct spread from the adjacent soft-tissue infection", True),
                     ("the bloodstream from a distant site", False),
                     ("direct inoculation during surgery", False), seed="c3s3a"),
            dropdown(("raises pressure, compresses blood vessels, and causes bone ischemia and necrosis", True),
                     ("dissolves the bone completely within a few hours", False),
                     ("is absorbed quickly because bone has a rich lymphatic supply", False), seed="c3s3b"),
            dropdown(("sequestra", True), ("involucra", False), ("osteophytes", False), ("tophi", False), seed="c3s3c"),
            dropdown(("sepsis", True), ("fat embolism syndrome", False), ("compartment syndrome", False), ("osteoporosis", False),
                     seed="c3s3d"),
        ],
    },
    "explanation": rationale(
        "<b>Routes of infection:</b> bacteria reach bone in three ways. (a) <b>Contiguous spread</b> from nearby infected tissue, as here "
        "from a diabetic foot ulcer or a pressure injury. (b) <b>Hematogenous spread</b> through the bloodstream, most common in children "
        "(metaphysis of long bones) and in the vertebrae of older adults. (c) <b>Direct inoculation</b> through an open fracture, "
        "surgery or a penetrating wound. <i>Staphylococcus aureus</i> is the most common organism.",
        "<b>Why bone infection is hard to cure:</b> bone cannot swell. Pus and edema inside the rigid bone raise pressure, compress the "
        "small blood vessels and cut off the blood supply, so bone dies (ischemic necrosis). Pus can lift the periosteum, stripping more "
        "blood supply.",
        "<b>Sequestrum and involucrum:</b> a <b>sequestrum</b> is a piece of dead, avascular bone that harbours bacteria out of reach of "
        "white blood cells and antibiotics. The body walls it off with new bone, the <b>involucrum</b>. This is why osteomyelitis can "
        "become chronic and why long courses of antibiotics, and sometimes removal of dead bone, are needed. Osteophytes are bone spurs of "
        "osteoarthritis; tophi are urate deposits of gout.",
        "<b>Priority:</b> the client has fever, a raised WBC count, and blood cultures pending. Spread of the infection into the bloodstream "
        "(<b>sepsis</b>) is the most immediate threat to her life. Fat embolism and compartment syndrome are complications of fractures, "
        "and osteoporosis is not an acute problem."),
})

# ---------------------------------------------------------------- Screen 4 (generate solutions): select all
C.notes("nn", "Nurses' Notes", ("Day 3 1000",
    "Bone biopsy grew methicillin-sensitive <i>Staphylococcus aureus</i>. Blood cultures negative. Peripherally inserted central catheter "
    "(PICC) placed in the left arm for 6 weeks of IV antibiotic therapy at home. Client and husband will learn to give the infusions. "
    "Non-weight-bearing on the right foot with an offloading boot and a walker, as prescribed."))
C.vitals("Day 3 1000", vs("37.4° C", "84 beats/min", "16 breaths/min", "132/78 mm Hg", "98% on room air"))
s4 = screen(4, INTRO, C, {
    "type": "select_all",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 3 1000 and the Vital Signs from Day 3 1000.",
    "stem": "The nurse is planning care for the client. Which interventions should the nurse include in the plan of care? "
            "<b>Select all that apply.</b>",
    "options": opts(
        ("Check capillary blood glucose before meals and at bedtime", True),
        ("Reinforce non-weight-bearing on the right foot with the offloading boot and walker", True),
        ("Assess the PICC insertion site every shift and use aseptic technique when accessing the line", True),
        ("Teach the client to inspect both feet every day, including between the toes, using a mirror", True),
        ("Encourage meals and snacks rich in protein", True),
        ("Soak the right foot in warm water twice a day to soften the wound", False),
        ("Apply a heating pad to the right foot to increase blood flow", False),
        ("Teach the client that the antibiotic can be stopped once the fever is gone", False),
        ("Massage lotion between the toes to prevent dry skin", False),
        seed="c3s4"),
    "explanation": rationale(
        "<b>Correct:</b> infection and hyperglycemia feed each other, so glucose is checked regularly and abnormal readings reported. "
        "Pressure on the ulcer prevents healing, so offloading (no weight on the foot) is essential. A PICC is a central line with a risk "
        "of bloodstream infection and thrombosis, so the site is assessed and accessed aseptically. Daily foot inspection is vital when "
        "sensation is lost, because the client cannot feel new injuries. Protein supports tissue repair and the immune response.",
        "<b>Incorrect:</b> soaking macerates the skin and the wound and increases the risk of infection. Heating pads can burn a foot that "
        "cannot feel heat. Antibiotic courses for osteomyelitis are long (often 6 weeks) because bone is poorly perfused; stopping when the "
        "fever goes leaves bacteria in the bone and leads to chronic infection. Moisture between the toes promotes fungal infection and skin "
        "breakdown; lotion is applied to the tops and soles, not between the toes."),
})

# ---------------------------------------------------------------- Screen 5 (take action): matrix
s5 = screen(5, INTRO, C, {
    "type": "matrix_mc",
    "stem": "The nurse is preparing the client and her husband for discharge with home IV therapy. For each instruction, click to specify "
            "whether it is <b>appropriate</b> or <b>not appropriate</b> to include in the teaching.",
    "matrix": matrix_mc("Instruction", ["Appropriate", "Not appropriate"], [
        ("Scrub the PICC hub with an alcohol pad for at least 15 seconds and let it dry before each connection", 0),
        ("Have your blood pressure taken on the left arm, where the PICC is", 1),
        ("Cover the PICC dressing with a waterproof cover when showering", 0),
        ("Report fever, chills, or redness, swelling, or pain at the PICC site or in the left arm", 0),
        ("Wear the offloading boot whenever you are up, and never walk barefoot", 0),
        ("Soak the foot in Epsom salts each evening", 1),
        ("Skip the infusion on days when the foot looks better", 1),
        ("Keep checking your blood glucose and write down the readings for your appointments", 0),
    ]),
    "explanation": rationale(
        "<b>Appropriate:</b> scrubbing the hub (“scrub the hub”) removes bacteria before each access and prevents central line infection. "
        "Keeping the dressing dry protects the site. Fever, chills, or redness, swelling or pain at the site or in the arm can mean line "
        "infection or a clot and are reported at once. Offloading and protective footwear protect the healing foot. Glucose records help "
        "the team adjust diabetes management, because good control supports healing.",
        "<b>Not appropriate:</b> blood pressure cuffs, tourniquets and blood draws are avoided on the arm with the PICC (they can damage the "
        "catheter or the vein). Soaking macerates the wound. Missing doses lowers the drug level in bone and allows the infection to persist "
        "or become chronic."),
})

# ---------------------------------------------------------------- Screen 6 (evaluate outcomes): matrix
C.notes("nn", "Nurses' Notes", ("Day 42 1000",
    "Home visit, end of 6 weeks of IV antibiotics. Ulcer 0.8 × 0.6 cm with pink granulation tissue and no drainage. Redness and swelling of "
    "the toe resolved. Fasting glucose readings 6 to 8 mmol/L. Husband demonstrates scrubbing the hub for 15 seconds before connecting the "
    "infusion. Client reports she “walks to the mailbox in socks so the foot can breathe.” Left upper arm along the PICC is red, swollen, "
    "and tender; left upper arm circumference 3 cm larger than the right."))
C.vitals("Day 42 1000", vs("36.8° C", "80 beats/min", "16 breaths/min", "128/76 mm Hg", "98% on room air"))
C.labs("Day 42 0900", [
    (lab("White blood cell (WBC) count", "3.5–10.5 × 10<sup>9</sup>/L"), "7.1 × 10<sup>9</sup>/L"),
    (lab("Erythrocyte sedimentation rate (ESR)", "Female: 0–20 mm/h"), "40 mm/h"),
    (lab("C-reactive protein (CRP)", "≤ 10 mg/L"), "12 mg/L"),
])
s6 = screen(6, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 42 1000, the Vital Signs from Day 42, and the Laboratory Results from "
                "Day 42.",
    "stem": "For each finding, click to specify whether it indicates that the plan of care has been <b>effective</b> or <b>not "
            "effective</b>.",
    "matrix": matrix_mc("Finding", ["Effective", "Not effective"], [
        ("Temperature 36.8° C and WBC 7.1 × 10⁹/L", 0),
        ("Walks to the mailbox in socks", 1),
        ("CRP 12 mg/L and ESR 40 mm/h, down from 118 mg/L and 92 mm/h", 0),
        ("Red, swollen, tender left upper arm, 3 cm larger than the right", 1),
        ("Ulcer 0.8 × 0.6 cm with pink granulation tissue and no drainage", 0),
        ("Husband scrubs the hub for 15 seconds before connecting the infusion", 0),
        ("Fasting glucose readings of 6 to 8 mmol/L", 0),
    ]),
    "explanation": rationale(
        "<b>Effective:</b> no fever and a normal WBC count; CRP and ESR falling steadily (ESR falls more slowly than CRP); a smaller, clean "
        "ulcer with healthy granulation tissue; improved glucose control; and correct line care by the husband.",
        "<b>Not effective:</b> walking in socks puts pressure on the ulcer and exposes the insensate foot to injury; the nurse reinforces "
        "wearing the offloading boot. A red, swollen, tender arm with a larger circumference on the PICC side suggests a catheter-related "
        "deep vein thrombosis or phlebitis; the nurse does not use the line until it is assessed and reports the finding to the provider "
        "promptly."),
})

write_case(ID, 3,
    "61-year-old female client with type 2 diabetes and peripheral neuropathy whose plantar ulcer spreads to the bone of the great toe "
    "(contiguous osteomyelitis); risk factors and local/systemic signs, sequestrum and involucrum, sepsis risk, home IV therapy via a PICC "
    "and evaluation after 6 weeks.",
    [s1, s2, s3, s4, s5, s6],
    ["Screen 5: “scrub the hub” time (15 seconds) follows common practice; your agency's policy may differ.",
     "Screen 6: the arm finding is keyed as a possible PICC-related thrombosis/phlebitis to report."])
