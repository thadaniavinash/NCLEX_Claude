"""NURS 1017 Unit 6 Case Study 6: osteoarthritis of the knee and hands, analgesic safety and falls,
then nursing care after a total knee arthroplasty (outcome: osteoarthritis). Nursing focus, no
treatment decisions."""
from unit6_common import *

ID = "case_1782400000006"
INTRO = "The nurse in a primary care clinic is caring for a 68-year-old male client with right knee pain."
C = Chart()

# ---------------------------------------------------------------- Screen 1 (recognize cues): highlight
S1_NOTE = [("Day 1 1000",
    "Retired carpenter who knelt on job sites for 40 years. Reports 3 years of {right knee pain that worsens with walking and climbing "
    "stairs and eases with rest|correct}, worse by the end of the day. {Morning stiffness in the knee lasting about 15 minutes.|correct} "
    "{Grating (crepitus) felt and heard when the right knee bends.|correct} {Hard, bony enlargements on the end joints (DIP) of both index "
    "fingers.|correct} {Weight 102 kg, BMI 33.|correct} {MCP joints and wrists not swollen or warm.} {Temperature 36.7° C.} "
    "{Reports good appetite with no weight loss.} Right knee slightly enlarged and bony, with a small cool effusion; flexion limited to "
    "100°. {Takes ramipril 10 mg daily for hypertension.} Lives with his wife in a two-storey house.")]
C.notes("nn", "Nurses' Notes", *S1_NOTE)
C.vitals("Day 1 1000", vs("36.7° C", "78 beats/min", "16 breaths/min", "142/86 mm Hg", "97% on room air"))
s1 = screen(1, INTRO, C, {
    "type": "highlight",
    "stem": "The nurse reviews the Nurses' Notes. <b>Highlight</b> the findings that are consistent with osteoarthritis or increase the "
            "client's risk for it.",
    "options": [],
    "highlightTabs": [highlight_tab("ht1", "Nurses' Notes", S1_NOTE)],
    "maxCorrectSelections": None,
    "explanation": rationale(
        "<b>Consistent with osteoarthritis (OA):</b>",
        "<b>Pain with use that eases with rest</b> and worsens through the day: the damaged joint surfaces hurt under load. In late disease "
        "pain may also occur at rest and at night.",
        "<b>Short morning stiffness</b> (usually under 30 minutes) after rest, which loosens with movement.",
        "<b>Crepitus:</b> grating from roughened cartilage and bone surfaces moving against each other.",
        "<b>Heberden nodes:</b> bony enlargements (osteophytes) of the distal interphalangeal joints; Bouchard nodes affect the proximal "
        "interphalangeal joints.",
        "<b>Risk factors:</b> obesity (more load on weight-bearing joints, plus inflammatory substances from fat tissue) and years of "
        "repeated kneeling or joint stress. Age and previous joint injury are other major risk factors.",
        "<b>Not OA cues:</b> unswollen MCP joints and wrists, a normal temperature and no weight loss argue against an inflammatory, "
        "systemic arthritis such as rheumatoid arthritis. Ramipril treats his hypertension."),
})

# ---------------------------------------------------------------- Screen 2 (analyze cues): matrix
C.notes("dx", "Diagnostic Results", ("Day 1 1100",
    "<b>X-ray, right knee (standing):</b> narrowing of the medial joint space, osteophytes at the joint margins, subchondral sclerosis, "
    "and small subchondral cysts. Small effusion."))
C.labs("Day 1 1030", [
    (lab("Erythrocyte sedimentation rate (ESR)", "Male: 0–10 mm/h"), "8 mm/h"),
    (lab("C-reactive protein (CRP)", "≤ 10 mg/L"), "3 mg/L"),
    (lab("Rheumatoid factor (RF)", "≤ 20 kIU/L"), "&lt; 10 kIU/L"),
    (lab("Uric acid", "Male: 208–400 µmol/L"), "352 µmol/L"),
])
s2 = screen(2, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Diagnostic Results and the Laboratory Results.",
    "stem": "The nurse is explaining the client's X-ray to him. For each finding, click to specify whether it is mainly the result of "
            "<b>loss of articular cartilage</b>, <b>bone remodeling</b>, or <b>secondary synovial inflammation</b>.",
    "matrix": matrix_mc("Finding", ["Loss of articular cartilage", "Bone remodeling", "Secondary synovial inflammation"], [
        ("Osteophytes at the joint margins", 1),
        ("Narrowing of the medial joint space", 0),
        ("Small, cool effusion that increases after a long walk", 2),
        ("Subchondral sclerosis and cysts", 1),
        ("Heberden nodes", 1),
    ]),
    "explanation": rationale(
        "<b>Loss of articular cartilage</b> is the central change in OA. Chondrocytes fail to keep up with the breakdown of the cartilage "
        "matrix (driven by mechanical load and enzymes), so the cartilage softens, fissures and wears away. The joint space on X-ray is the "
        "cartilage, so its narrowing (here on the medial side, which carries the most load) shows cartilage loss.",
        "<b>Bone remodeling:</b> as cartilage is lost, the bone underneath takes the load. It thickens and becomes dense (subchondral "
        "sclerosis), and joint fluid forced into cracks forms cysts. At the joint margins, new bone grows as spurs (osteophytes), which "
        "limit motion and, in the fingers, form Heberden and Bouchard nodes.",
        "<b>Secondary synovial inflammation:</b> fragments of cartilage irritate the synovium, which produces a mild, cool effusion after "
        "activity. This inflammation is local and mild, so the ESR and CRP are normal and the RF is negative, unlike in rheumatoid "
        "arthritis. The normal uric acid argues against gout."),
})

# ---------------------------------------------------------------- Screen 3 (prioritize hypotheses): cloze
C.notes("nn", "Nurses' Notes",
    ("Day 60 1000", "Follow-up visit. Client reports the knee “gave way” on the stairs last week and he caught the railing; he does not "
     "use a cane. He takes two 500-mg acetaminophen tablets every 4 hours while awake (six times a day) “because the label dose doesn't "
     "touch the pain,” plus a night-time cold and flu tablet that contains acetaminophen 650 mg. Drinks 3 beers most evenings. Denies "
     "abdominal pain or dark stools."))
C.vitals("Day 60 1000", vs("36.6° C", "80 beats/min", "16 breaths/min", "144/88 mm Hg", "97% on room air"))
C.labs("Day 60 1030", [
    (lab("Alanine aminotransferase (ALT)", "17–63 IU/L"), "112 IU/L"),
])
s3 = screen(3, INTRO, C, {
    "type": "dropdown_cloze",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 60 1000, the Vital Signs from Day 60, and the Laboratory Results from "
                "Day 60.",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {
        "text": "The nurse's priority concern is the client's risk for [[drop0]], because [[drop1]]. The nurse also identifies a risk for "
                "[[drop2]] related to [[drop3]].",
        "dropdowns": [
            dropdown(("liver injury", True), ("gastrointestinal bleeding", False), ("kidney stones", False), seed="c6s3a"),
            dropdown(("he takes about 6.6 g of acetaminophen a day, drinks alcohol daily, and his ALT is elevated", True),
                     ("his blood pressure is 144/88 mm Hg", False),
                     ("his morning stiffness lasts 15 minutes", False), seed="c6s3b"),
            dropdown(("falls", True), ("infection", False), ("pressure injury", False), seed="c6s3c"),
            dropdown(("knee instability and pain without a walking aid", True), ("his age alone", False),
                     ("the night-time cold and flu tablet", False), seed="c6s3d"),
        ],
    },
    "explanation": rationale(
        "<b>Liver injury:</b> 2 × 500 mg six times a day (6 g) plus 650 mg at night is about 6.6 g of acetaminophen a day, well above the "
        "usual maximum of 4 g a day (lower, often 3 g or less, for older adults and people who drink alcohol regularly). Alcohol depletes "
        "glutathione, which the liver needs to detoxify an acetaminophen metabolite, so the risk of liver injury rises. His raised ALT is "
        "already a warning. Hidden acetaminophen in combination cold and flu products is a common cause of accidental overdose. The nurse "
        "reports this to the provider at once.",
        "<b>Not the priority:</b> he is not taking NSAIDs and denies dark stools, so GI bleeding is not suggested; blood pressure and "
        "stiffness need follow-up but are not urgent.",
        "<b>Falls:</b> a knee that “gives way” (from pain, quadriceps weakness and joint instability) on the stairs, without a walking aid, "
        "puts him at high risk of a fall and fracture. Age adds to the risk but is not the cause here. The cold and flu tablet may cause "
        "drowsiness, but the knee instability is the main factor."),
})

# ---------------------------------------------------------------- Screen 4 (generate solutions): select all
s4 = screen(4, INTRO, C, {
    "type": "select_all",
    "stem": "The nurse is planning teaching for the client. Which instructions should the nurse include? <b>Select all that apply.</b>",
    "options": opts(
        ("Read the labels of all over-the-counter products for acetaminophen and keep the total within the daily limit your provider "
         "sets", True),
        ("Use a cane in your left hand", True),
        ("Apply warmth before activity to ease stiffness, and a cold pack after activity if the knee swells", True),
        ("Do low-impact exercise such as swimming or cycling, and quadriceps-strengthening exercises", True),
        ("Losing even a small amount of weight reduces the load on your knees", True),
        ("Use a cane in your right hand", False),
        ("Rest the knee completely until the pain goes away", False),
        ("Strengthen the knee with deep squats and kneeling exercises", False),
        ("Sleep with a pillow under the right knee", False),
        seed="c6s4"),
    "explanation": rationale(
        "<b>Correct:</b> checking labels prevents hidden acetaminophen overdose. A cane is held in the hand opposite the affected knee and "
        "moved forward with it, which shifts weight off the painful knee and widens the base of support. Heat relaxes muscles and eases "
        "stiffness before activity; cold reduces swelling and pain after activity. Low-impact aerobic exercise and quadriceps strengthening "
        "stabilize the knee and reduce pain without overloading it. Every kilogram of weight lost removes about 4 kg of load from the knee "
        "with each step.",
        "<b>Incorrect:</b> a cane on the same side as the bad knee does not unload it. Complete rest causes stiffness, muscle weakness and "
        "further loss of function. Deep squats and kneeling load the damaged cartilage heavily. A pillow under the knee is comfortable but "
        "encourages a flexion contracture."),
})

# ---------------------------------------------------------------- Screen 5 (take action): matrix
C.notes("nn", "Nurses' Notes", ("Day 400 0800",
    "One year later, after conservative care no longer controlled his pain, the client had a right total knee arthroplasty yesterday. "
    "Postoperative day 1. Right knee dressing dry and intact; right foot warm, pedal pulses 2+, sensation and movement intact. Pain 4/10 "
    "with movement after IV analgesia. Sequential compression devices on both legs. Physiotherapy to walk him with a walker this morning."))
C.vitals("Day 400 0800", vs("37.4° C", "84 beats/min", "16 breaths/min", "136/78 mm Hg", "96% on room air"))
s5 = screen(5, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 400 0800 and the Vital Signs from Day 400.",
    "stem": "For each nursing action, click to specify whether it is <b>indicated</b>, <b>contraindicated</b>, or <b>nonessential</b> "
            "for the client on postoperative day 1.",
    "matrix": matrix_mc("Nursing Action", ["Indicated", "Contraindicated", "Nonessential"], [
        ("Place a pillow under the right knee to relieve pain", 1),
        ("Assess circulation, movement, and sensation of the right foot regularly", 0),
        ("Encourage ankle pumps every hour while awake and keep the sequential compression devices on in bed", 0),
        ("Keep the client on bed rest for the first 3 days", 1),
        ("Give the prescribed analgesic before physiotherapy", 0),
        ("Arrange X-rays of both hands", 2),
        ("Apply the prescribed cold therapy to the right knee", 0),
    ]),
    "explanation": rationale(
        "<b>Indicated:</b> neurovascular checks detect nerve or vascular injury and compartment problems early. Ankle pumps and sequential "
        "compression devices promote venous return and help prevent deep vein thrombosis, a major risk after knee replacement. Pain relief "
        "before physiotherapy lets him take part in early walking and range-of-motion exercise. Cold therapy reduces swelling and pain.",
        "<b>Contraindicated:</b> a pillow under the knee holds it flexed and can cause a flexion contracture; the knee is kept straight when "
        "resting (a pillow may go under the calf and heel if the leg is elevated). Bed rest increases the risk of blood clots, pneumonia and "
        "stiffness; walking usually starts on the day of surgery or the day after.",
        "<b>Nonessential:</b> hand X-rays do not change his postoperative care."),
})

# ---------------------------------------------------------------- Screen 6 (evaluate outcomes): matrix
C.notes("nn", "Nurses' Notes",
    ("Day 442 1000", "Clinic follow-up, 6 weeks after surgery. Right knee flexion 105° with full extension. Incision healed with no "
     "redness or drainage. Walks with a cane in his left hand; no falls. Weight 96 kg (was 102 kg). Right calf warm, swollen, and tender; "
     "right calf circumference 3 cm larger than the left. Reports the calf started aching 2 days ago."),
    ("Day 442 1015", "Client states: “I check labels and keep track of my acetaminophen.” “I still sleep with a pillow under my right "
     "knee; it feels better.”"))
C.vitals("Day 442 1000", vs("36.8° C", "92 beats/min", "18 breaths/min", "134/80 mm Hg", "97% on room air"))
s6 = screen(6, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 442 1000 and 1015 and the Vital Signs from Day 442.",
    "stem": "For each finding, click to specify whether it indicates that the plan of care has been <b>effective</b> or <b>not "
            "effective</b>.",
    "matrix": matrix_mc("Finding", ["Effective", "Not effective"], [
        ("Right knee flexion 105° with full extension", 0),
        ("Warm, swollen, tender right calf, 3 cm larger than the left", 1),
        ("Walks with a cane in his left hand, with no falls", 0),
        ("“I still sleep with a pillow under my right knee.”", 1),
        ("Weight 96 kg, down from 102 kg", 0),
        ("Incision healed, with no redness or drainage", 0),
        ("“I check labels and keep track of my acetaminophen.”", 0),
    ]),
    "explanation": rationale(
        "<b>Effective:</b> good range of motion (about 90° to 110° of flexion is a usual goal at this stage), a healed incision, safe use of "
        "the cane on the correct side with no falls, weight loss, and safe use of acetaminophen.",
        "<b>Not effective:</b> a warm, swollen, tender calf that is larger than the other suggests a deep vein thrombosis, which can lead to "
        "a pulmonary embolism. The nurse does not massage the calf, has the client rest, and reports the finding to the provider "
        "immediately. Sleeping with a pillow under the knee risks a flexion contracture and loss of the extension gained in therapy; the "
        "nurse reteaches keeping the knee straight."),
})

write_case(ID, 6,
    "68-year-old male client, a retired carpenter with obesity, with osteoarthritis of the right knee and Heberden nodes; cartilage loss, "
    "bone remodeling and secondary synovitis, acetaminophen overuse and fall risk, self-management teaching, and nursing care and "
    "evaluation after a total knee arthroplasty.",
    [s1, s2, s3, s4, s5, s6],
    ["Screen 3: acetaminophen maximum stated as 4 g/day, lower (often 3 g or less) for older adults and regular alcohol use; adjust to "
     "your course's reference.",
     "Screen 4: the “1 kg lost = about 4 kg less load on the knee” figure comes from Messier et al. (2005).",
     "Screen 6: knee flexion goal at 6 weeks (about 90°–110°) varies by surgeon."])
