"""NURS 1017 Unit 6 Case Study 9: ankylosing spondylitis, compared with rheumatoid arthritis and SLE
(outcome: SLE and ankylosing spondylitis; also RA). Nursing focus, no treatment decisions."""
from unit6_common import *

ID = "case_1782400000009"
INTRO = "The nurse in a primary care clinic is caring for a 27-year-old male client with low back pain."
C = Chart()

# ---------------------------------------------------------------- Screen 1 (recognize cues): select all
C.notes("nn", "Nurses' Notes", ("Day 1 0900",
    "Reports 8 months of low back pain that came on gradually. His back is stiff for about an hour each morning and loosens up after a "
    "hot shower and moving around; it is worse after sitting for a long time and better with exercise. Wakes in the early morning hours "
    "with back pain and has to get up and walk around. Has aching deep in the buttocks, sometimes on the right and sometimes on the left. "
    "Pain and tenderness at the back of both heels where the Achilles tendons attach. Last year had a painful, red right eye with "
    "sensitivity to light that an eye doctor treated. Works in a warehouse; denies a back injury. No numbness or weakness in the legs; "
    "bladder and bowel function normal. Smokes 10 cigarettes a day. His father has had “a stiff back” for years. Reduced forward "
    "bending of the lower back; increase on the Schober test 2.5 cm (expected 5 cm or more). Chest expansion 4 cm."))
C.vitals("Day 1 0900", vs("36.8° C", "72 beats/min", "14 breaths/min", "124/78 mm Hg", "99% on room air"))
s1 = screen(1, INTRO, C, {
    "type": "select_all",
    "stem": "Which findings suggest an inflammatory cause of the client's back pain rather than a mechanical (strain) cause? "
            "<b>Select all that apply.</b>",
    "options": opts(
        ("Morning stiffness lasting about an hour that loosens with a hot shower and movement", True),
        ("Back pain that improves with exercise and worsens with rest", True),
        ("Wakes in the early morning hours with back pain and gets up to walk around", True),
        ("Aching deep in the buttocks that alternates between sides", True),
        ("Pain where the Achilles tendons attach to both heels", True),
        ("Painful, red eye with light sensitivity last year", True),
        ("Works in a warehouse", False),
        ("No numbness or weakness in the legs", False),
        ("Blood pressure 124/78 mm Hg", False),
        seed="c9s1"),
    "explanation": rationale(
        "<b>Inflammatory back pain</b> typically starts before age 40, comes on gradually, lasts more than 3 months, causes morning "
        "stiffness of 30 minutes or more, improves with exercise but not with rest, and wakes the person in the second half of the night. "
        "Mechanical back pain is the opposite: it worsens with activity and improves with rest.",
        "<b>Alternating buttock pain</b> points to inflammation of the sacroiliac joints (sacroiliitis), the hallmark of ankylosing "
        "spondylitis (AS).",
        "<b>Heel pain at the Achilles insertion</b> is enthesitis, inflammation where tendons and ligaments attach to bone, a key feature of "
        "the spondyloarthritis family.",
        "<b>Acute anterior uveitis</b> (painful red eye with light sensitivity) is the most common extra-articular feature of AS.",
        "<b>Not cues:</b> warehouse work could suggest a mechanical cause, and normal leg strength and sensation with normal bladder and bowel "
        "function show no nerve compression; neither points to inflammation. His blood pressure is normal."),
})

# ---------------------------------------------------------------- Screen 2 (analyze cues): matrix
C.labs("Day 1 0930", [
    (lab("Erythrocyte sedimentation rate (ESR)", "Male: 0–10 mm/h"), "32 mm/h"),
    (lab("C-reactive protein (CRP)", "≤ 10 mg/L"), "24 mg/L"),
    (lab("HLA-B27", "Negative"), "Positive"),
    (lab("Rheumatoid factor (RF)", "≤ 20 kIU/L"), "&lt; 10 kIU/L"),
    (lab("Antinuclear antibodies (ANA)", "Negative"), "Negative"),
])
C.notes("dx", "Diagnostic Results",
    ("Day 1 1000", "<b>X-ray, pelvis:</b> erosions and sclerosis of both sacroiliac joints (bilateral sacroiliitis)."),
    ("Day 5 1400", "<b>MRI, sacroiliac joints:</b> bone marrow edema on both sides of both sacroiliac joints, consistent with active "
     "sacroiliitis."))
C.notes("nn", "Nurses' Notes", ("Day 10 1000",
    "Returns for results. The provider diagnoses ankylosing spondylitis. Client says his cousin has lupus and a friend has rheumatoid "
    "arthritis, and asks, “Is this the same kind of arthritis?”"))
s2 = screen(2, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Laboratory Results, the Diagnostic Results, and the Nurses' Notes from Day 10 1000.",
    "stem": "For each finding, click to specify whether it is most characteristic of <b>ankylosing spondylitis</b>, <b>rheumatoid "
            "arthritis</b>, or <b>systemic lupus erythematosus</b>.",
    "matrix": matrix_mc("Finding", ["Ankylosing spondylitis", "Rheumatoid arthritis", "Systemic lupus erythematosus"], [
        ("HLA-B27 positive with a negative rheumatoid factor", 0),
        ("Antibodies to double-stranded DNA", 2),
        ("Symmetric swelling of the small joints of both hands with anti-CCP antibodies", 1),
        ("Sacroiliitis on X-ray or MRI", 0),
        ("Butterfly rash on the cheeks that worsens in the sun", 2),
        ("Vertebrae joined by bony bridges (“bamboo spine”)", 0),
        ("Firm nodules over the elbows with joint erosions of the hands", 1),
        ("Protein in the urine from immune complexes in the kidneys", 2),
    ]),
    "explanation": rationale(
        "<b>Ankylosing spondylitis (AS)</b> is a <b>seronegative spondyloarthritis</b>: rheumatoid factor and ANA are negative, and about "
        "90% of clients carry the <b>HLA-B27</b> gene (which is also found in about 8% of healthy people, so it supports but does not prove "
        "the diagnosis). Inflammation affects the sacroiliac joints and spine; over years, new bone bridges the vertebrae (syndesmophytes), "
        "giving the “bamboo spine” on X-ray. It usually begins in young men.",
        "<b>Rheumatoid arthritis (RA)</b> is a symmetric inflammatory polyarthritis of small joints (hands, wrists, feet) with rheumatoid "
        "factor and anti-CCP antibodies, erosions, and rheumatoid nodules.",
        "<b>Systemic lupus erythematosus (SLE)</b> is a multisystem autoimmune disease, most common in young women, with ANA and "
        "anti-double-stranded DNA antibodies. Immune complexes deposit in skin (malar rash, photosensitivity), joints (non-erosive "
        "arthritis), kidneys (lupus nephritis, proteinuria), blood cells and serous membranes.",
        "So all three are inflammatory arthritides, but they differ in the joints involved, the antibodies, and the organs affected."),
})

# ---------------------------------------------------------------- Screen 3 (prioritize hypotheses): cloze
s3 = screen(3, INTRO, C, {
    "type": "dropdown_cloze",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {
        "text": "In ankylosing spondylitis, inflammation begins at the [[drop0]]. Repeated inflammation is followed by [[drop1]]. Without "
                "regular exercise and good posture, the client is at greatest risk for [[drop2]]. Involvement of the joints of the ribs can "
                "also lead to [[drop3]].",
        "dropdowns": [
            dropdown(("entheses, where ligaments and tendons attach to bone", True), ("synovium of the small joints of the hands", False),
                     ("cartilage of weight-bearing joints from wear and tear", False), seed="c9s3a"),
            dropdown(("new bone formation that can fuse the vertebrae", True), ("loss of bone that makes the spine more flexible", False),
                     ("complete healing with no lasting change", False), seed="c9s3b"),
            dropdown(("a fused spine fixed in a stooped, forward-flexed posture", True), ("osteoarthritis of the hands", False),
                     ("gout of the big toe", False), seed="c9s3c"),
            dropdown(("reduced chest expansion and restricted breathing", True), ("muscle weakness from loss of acetylcholine receptors",
                     False), ("fat embolism", False), seed="c9s3d"),
        ],
    },
    "explanation": rationale(
        "<b>Enthesitis:</b> AS is driven by inflammation at the entheses of the spine, sacroiliac joints and heels (cytokines such as TNF-α "
        "and IL-17 are central). This differs from RA, which begins in the synovium, and from osteoarthritis, which is degenerative.",
        "<b>Ankylosis:</b> after inflammation, the body lays down new bone. Bony bridges (syndesmophytes) gradually join the vertebrae and "
        "the sacroiliac joints fuse. The spine loses movement, and if it fuses while the client is stooped, the posture becomes fixed in "
        "flexion (kyphosis), which also limits the field of vision.",
        "<b>Chest wall:</b> inflammation and fusion of the costovertebral and costosternal joints reduce chest expansion (his is 4 cm; under "
        "about 2.5 cm is clearly reduced), which restricts breathing. Daily deep breathing and not smoking protect lung function.",
        "<b>Also:</b> a fused, osteoporotic spine breaks easily, even after a minor fall, so new neck or back pain after trauma needs urgent "
        "assessment."),
})

# ---------------------------------------------------------------- Screen 4 (generate solutions): select all
C.notes("nn", "Nurses' Notes", ("Day 10 1030",
    "The provider has prescribed an anti-inflammatory medication and referred the client to physiotherapy. The nurse plans teaching for "
    "self-management. Client says, “When my back hurts I just want to curl up in bed.”"))
s4 = screen(4, INTRO, C, {
    "type": "select_all",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 10 1030.",
    "stem": "Which instructions should the nurse include in the client's teaching? <b>Select all that apply.</b>",
    "options": opts(
        ("Do stretching and back-extension exercises every day, including on days with pain", True),
        ("Sleep on a firm mattress, on your back or stomach, with a thin pillow or none", True),
        ("Do deep-breathing exercises several times a day", True),
        ("Stop smoking", True),
        ("Take a warm shower in the morning before exercising to ease stiffness", True),
        ("Seek care right away for new neck or back pain after even a minor fall", True),
        ("Rest in bed curled on your side with pillows under your head and knees when your back hurts", False),
        ("Avoid exercise during flares until the pain is gone", False),
        ("Sit in a soft, low armchair to take the strain off your back", False),
        seed="c9s4"),
    "explanation": rationale(
        "<b>Correct:</b> daily exercise, especially stretching and extension exercises and activities such as swimming, is the cornerstone of "
        "AS care: it maintains spinal mobility and helps the spine stay upright if it fuses. Sleeping flat on a firm surface with little or no "
        "pillow (lying prone for periods each day) prevents flexion deformity. Deep breathing maintains chest expansion. Smoking worsens AS "
        "progression and lung function. Heat eases morning stiffness before activity. A fused spine fractures easily, so new pain after a fall "
        "must be assessed urgently.",
        "<b>Incorrect:</b> curling up with pillows under the head and knees and sitting in soft, low chairs encourage a flexed posture, and "
        "rest worsens inflammatory stiffness. In AS, activity relieves the pain, so exercise continues during flares at a gentler level."),
})

# ---------------------------------------------------------------- Screen 5 (take action): matrix
C.notes("nn", "Nurses' Notes", ("Day 220 1100",
    "Client calls the clinic and then comes in. Since this morning his left eye has been red and painful, with blurred vision and pain "
    "in bright light. Visual acuity: right eye 20/20, left eye 20/50. Left pupil smaller than the right. No discharge. Says, “It's just like "
    "last year. I thought I'd wait and see if it clears up.”"))
C.vitals("Day 220 1100", vs("36.8° C", "78 beats/min", "16 breaths/min", "126/78 mm Hg", "99% on room air"))
s5 = screen(5, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 220 1100 and the Vital Signs from Day 220.",
    "stem": "For each nursing action, click to specify whether it is <b>indicated</b>, <b>contraindicated</b>, or <b>nonessential</b> for "
            "the client at this time.",
    "matrix": matrix_mc("Nursing Action", ["Indicated", "Contraindicated", "Nonessential"], [
        ("Arrange an urgent, same-day assessment by an eye specialist", 0),
        ("Advise him to wait a week to see whether the redness clears", 1),
        ("Report the reduced visual acuity in the left eye to the provider", 0),
        ("Suggest wearing sunglasses for comfort until he is seen", 0),
        ("Measure his chest expansion today", 2),
        ("Tell him that the eye problem is unrelated to his back condition", 1),
        ("Teach him that this eye problem can recur and to seek care promptly each time", 0),
    ]),
    "explanation": rationale(
        "These are signs of <b>acute anterior uveitis</b> (iritis): a painful red eye, light sensitivity, blurred vision and a small pupil. It "
        "affects up to about a third of people with AS and is often recurrent and on one side.",
        "<b>Indicated:</b> uveitis needs urgent assessment and treatment by an eye specialist to prevent complications such as adhesions of "
        "the iris, glaucoma and vision loss; the drop in visual acuity is reported. Sunglasses ease light sensitivity while he waits. "
        "Because attacks recur, he is taught to seek care promptly each time.",
        "<b>Contraindicated:</b> waiting risks permanent damage to the eye. Saying the eye problem is unrelated is incorrect: uveitis is a "
        "recognized extra-articular feature of AS and shares the HLA-B27 link.",
        "<b>Nonessential:</b> chest expansion is part of routine follow-up, not of this urgent visit."),
})

# ---------------------------------------------------------------- Screen 6 (evaluate outcomes): matrix
C.notes("nn", "Nurses' Notes",
    ("Day 365 1000", "One-year follow-up. Uveitis resolved; vision 20/20 in both eyes. Morning stiffness about 15 minutes. Increase on the "
     "Schober test 3 cm (was 2.5 cm); chest expansion 4 cm (unchanged). Swims twice a week and does his stretching programme most days. "
     "Still smokes 10 cigarettes a day."),
    ("Day 365 1015", "Client states: “I sleep with two thick pillows because it's more comfortable.” “When my eye got red again last "
     "month, I went to the eye clinic the same day.”"))
C.vitals("Day 365 1000", vs("36.7° C", "70 beats/min", "14 breaths/min", "122/76 mm Hg", "99% on room air"))
C.labs("Day 365 0930", [
    (lab("Erythrocyte sedimentation rate (ESR)", "Male: 0–10 mm/h"), "9 mm/h"),
    (lab("C-reactive protein (CRP)", "≤ 10 mg/L"), "5 mg/L"),
])
s6 = screen(6, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 365 1000 and 1015, the Vital Signs from Day 365, and the Laboratory "
                "Results from Day 365.",
    "stem": "For each finding, click to specify whether it indicates that the plan of care has been <b>effective</b> or <b>not "
            "effective</b>.",
    "matrix": matrix_mc("Finding", ["Effective", "Not effective"], [
        ("Morning stiffness about 15 minutes", 0),
        ("“I sleep with two thick pillows.”", 1),
        ("Schober test increase 3 cm, up from 2.5 cm", 0),
        ("Still smokes 10 cigarettes a day", 1),
        ("CRP 5 mg/L and ESR 9 mm/h", 0),
        ("Swims twice a week and stretches most days", 0),
        ("“When my eye got red again, I went to the eye clinic the same day.”", 0),
        ("Chest expansion 4 cm, unchanged", 0),
    ]),
    "explanation": rationale(
        "<b>Effective:</b> shorter morning stiffness and normal inflammatory markers show that inflammation is controlled; spinal mobility "
        "has improved slightly and chest expansion has not declined; he exercises regularly; and he recognized a recurrence of uveitis and "
        "sought care the same day, as taught.",
        "<b>Not effective:</b> thick pillows hold the neck in flexion and promote a fixed, stooped posture; the nurse reteaches sleeping flat "
        "with a thin pillow. Continued smoking speeds spinal fusion and harms lung function in a client whose chest expansion is already "
        "limited; the nurse offers cessation support."),
})

write_case(ID, 9,
    "27-year-old male client with 8 months of inflammatory back pain, alternating buttock pain, Achilles enthesitis and a past episode of "
    "uveitis, diagnosed with HLA-B27-positive ankylosing spondylitis; AS vs rheumatoid arthritis vs SLE, enthesitis and spinal fusion, "
    "exercise and posture teaching, a recurrence of acute anterior uveitis, and evaluation at 1 year.",
    [s1, s2, s3, s4, s5, s6],
    ["Screen 1: Schober test normal (increase of 5 cm or more) and chest expansion values are commonly cited; check your textbook.",
     "Screen 2: HLA-B27 prevalence (about 90% in AS, about 8% in the general population) varies by population.",
     "Screen 5: the uveitis prevalence (up to about a third of clients with AS) is an approximate figure."])
