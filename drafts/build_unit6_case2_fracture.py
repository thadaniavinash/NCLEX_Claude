"""NURS 1017 Unit 6 Case Study 2: femur fracture and shoulder dislocation, fat embolism syndrome,
stages of bone healing and delayed union (outcomes: 5 stages of bone healing, types of fractures,
complications in bone healing and soft tissue, dislocation and subluxation). Nursing focus, no
treatment decisions."""
from unit6_common import *

ID = "case_1782400000002"
INTRO = ("The nurse is caring for a 22-year-old male client brought to the emergency department after a motorcycle collision.")
C = Chart()

# ---------------------------------------------------------------- Screen 1 (recognize cues): highlight
S1_NOTE = [("Day 1 1540",
    "Arrived by ambulance 30 minutes after a motorcycle collision; was wearing a helmet and did not lose consciousness. "
    "Alert and oriented × 4. {Right thigh swollen and deformed, with the right leg shortened and externally rotated.|correct} "
    "{Skin over the right thigh intact.} {Right foot warm and pink; pedal pulses 2+; capillary refill 2 seconds.} "
    "{Left shoulder has a squared-off contour; holds the left arm slightly away from his body and cannot move it.|correct} "
    "{Reports numbness over the outer aspect of the left upper arm.|correct} {Left radial pulse 2+.} "
    "{Abrasions on the left forearm and left knee.} {Skin pale, cool, and diaphoretic.|correct} "
    "Vital signs: {T 36.6° C}, {P 116 beats/min|correct}, {RR 22 breaths/min}, {BP 100/62 mm Hg|correct}, "
    "{SpO₂ 97% on room air}.")]
C.notes("nn", "Nurses' Notes", *S1_NOTE)
C.vitals("Day 1 1540", vs("36.6° C", "116 beats/min", "22 breaths/min", "100/62 mm Hg", "97% on room air"))
s1 = screen(1, INTRO, C, {
    "type": "highlight",
    "stem": "The nurse reviews the Nurses' Notes. <b>Highlight</b> the findings that require immediate follow-up.",
    "options": [],
    "highlightTabs": [highlight_tab("ht1", "Nurses' Notes", S1_NOTE)],
    "maxCorrectSelections": None,
    "explanation": rationale(
        "<b>Require immediate follow-up:</b>",
        "<b>Shortened, externally rotated, deformed right leg:</b> the classic picture of a displaced femoral shaft fracture. The limb "
        "must be immobilized (splinted or in traction) before any movement, and neurovascular status is checked often.",
        "<b>Tachycardia (116 beats/min), BP 100/62 mm Hg, and pale, cool, diaphoretic skin:</b> a closed femoral shaft fracture can "
        "hide 1 to 1.5 L of blood in the thigh. These are early signs of hypovolemic shock and must be reported now.",
        "<b>Squared-off shoulder that he cannot move:</b> the humeral head has left the joint (anterior dislocation is the most common "
        "type). A dislocation is reduced as soon as possible to protect the nerves, blood vessels and joint cartilage.",
        "<b>Numbness over the outer upper arm:</b> the axillary nerve wraps around the neck of the humerus and is the nerve most often "
        "injured by an anterior shoulder dislocation. Sensation is documented before and after reduction.",
        "<b>Do not need immediate follow-up:</b> intact skin over the fracture (a closed fracture), a warm, pink foot with strong pulses "
        "and brisk capillary refill, a strong left radial pulse, a temperature of 36.6° C, SpO₂ 97% and an RR of 22 breaths/min (expected "
        "with pain). The abrasions need cleaning but are not urgent."),
})

# ---------------------------------------------------------------- Screen 2 (analyze cues): matrix
C.notes("nn", "Nurses' Notes", ("Day 1 1620",
    "Right leg immobilized in a traction splint; right foot remains warm with pedal pulses 2+. The client tells the nurse that his left "
    "shoulder “popped partly out” twice while playing hockey last year and both times “slid back in on its own.”"))
C.notes("dx", "Diagnostic Results",
    ("Day 1 1600", "<b>X-ray, right femur:</b> closed, comminuted fracture of the midshaft of the femur, with displaced and overriding "
     "fragments."),
    ("Day 1 1605", "<b>X-ray, left shoulder:</b> anterior dislocation of the glenohumeral joint; the humeral head lies completely outside "
     "the glenoid cavity. No fracture."))
s2 = screen(2, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 1 1620 and the Diagnostic Results.",
    "stem": "For each finding, click to specify whether it is consistent with a <b>fracture</b>, a <b>dislocation</b>, or a "
            "<b>subluxation</b>.",
    "matrix": matrix_mc("Finding", ["Fracture", "Dislocation", "Subluxation"], [
        ("Humeral head lying completely outside the glenoid cavity on X-ray", 1),
        ("Shortening and external rotation of the leg", 0),
        ("Shoulder that “popped partly out” and slid back in on its own", 2),
        ("Bone broken into several fragments on X-ray", 0),
        ("Partial loss of contact between the joint surfaces, which remain partly aligned", 2),
        ("Squared-off shoulder contour with loss of normal movement", 1),
    ]),
    "explanation": rationale(
        "<b>Fracture:</b> a break in the continuity of a bone. This client's femur fracture is <b>closed</b> (skin intact) and "
        "<b>comminuted</b> (more than two fragments). Other types: <b>open</b> (bone ends break through the skin), <b>transverse</b> "
        "(straight across), <b>oblique</b> (at an angle), <b>spiral</b> (twisting around the shaft from a rotational force), "
        "<b>greenstick</b> (incomplete, on one side of a bendable child's bone), <b>compression</b> (bone crushed, as in vertebrae), "
        "<b>impacted</b> (one fragment driven into another), <b>avulsion</b> (a fragment pulled off by a tendon or ligament) and "
        "<b>pathologic</b> (through bone weakened by disease). Muscle spasm pulls the overriding femur fragments together, shortening "
        "and rotating the leg.",
        "<b>Dislocation:</b> the joint surfaces lose contact <b>completely</b>, as the X-ray shows for the left shoulder. The joint "
        "looks deformed (the shoulder is squared off because the humeral head no longer fills out the deltoid) and cannot move normally.",
        "<b>Subluxation:</b> a <b>partial</b> dislocation; the joint surfaces still touch in part. It often reduces on its own, as in his "
        "hockey injuries. Repeated subluxations stretch the capsule and ligaments, which made this full dislocation more likely."),
})

# ---------------------------------------------------------------- Screen 3 (prioritize hypotheses): cloze
C.notes("nn", "Nurses' Notes",
    ("Day 1 2100", "Returned to the orthopedic unit after intramedullary nailing of the right femur. The left shoulder was reduced in the "
     "emergency department at 1700; left arm in a sling. Sensation over the outer left upper arm is decreased but improving."),
    ("Day 3 0300", "Client is restless and confused, oriented to person only, and says, “I can't catch my breath.” Breathing is rapid "
     "and shallow; fine crackles in both lung bases. Pinpoint red-purple spots (petechiae) on the anterior chest, both axillae, and the "
     "conjunctivae. Right foot warm, pedal pulses 2+, right thigh dressing dry. Pain 4/10."))
C.vitals("Day 3 0300", vs("38.4° C", "128 beats/min", "32 breaths/min", "118/70 mm Hg", "86% on room air"))
C.labs("Day 1 1600", [
    (lab("Hemoglobin (Hgb)", "Male: 125–170 g/L"), "138 g/L"),
    (lab("Platelet count", "130–380 × 10<sup>9</sup>/L"), "236 × 10<sup>9</sup>/L"),
])
C.labs("Day 3 0310", [
    (lab("Hemoglobin (Hgb)", "Male: 125–170 g/L"), "104 g/L"),
    (lab("Platelet count", "130–380 × 10<sup>9</sup>/L"), "96 × 10<sup>9</sup>/L"),
    (lab("pH, arterial blood", "7.38–7.46"), "7.49"),
    (lab("PCO₂, arterial blood", "32–45 mm Hg"), "30 mm Hg"),
    (lab("PO₂, arterial blood", "83–116 mm Hg"), "54 mm Hg"),
    (lab("Bicarbonate (HCO₃), arterial blood", "22–27 mmol/L"), "23 mmol/L"),
])
s3 = screen(3, INTRO, C, {
    "type": "dropdown_cloze",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 1 2100 and Day 3 0300, the Vital Signs from Day 3 0300, and the "
                "Laboratory Results.",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {
        "text": "The client is most likely experiencing [[drop0]] as evidenced by [[drop1]]. The nurse's priority is the client's "
                "[[drop2]].",
        "dropdowns": [
            dropdown(("fat embolism syndrome", True), ("compartment syndrome", False), ("hypovolemic shock", False),
                     ("alcohol withdrawal", False), seed="c2s3a"),
            dropdown(("new confusion, hypoxemia, and petechiae 36 hours after a long-bone fracture", True),
                     ("a temperature of 38.4° C", False), ("a hemoglobin of 104 g/L after surgery", False),
                     ("pain rated 4/10", False), seed="c2s3b"),
            dropdown(("impaired gas exchange", True), ("acute pain", False), ("risk for infection", False),
                     ("impaired physical mobility", False), seed="c2s3c"),
        ],
    },
    "explanation": rationale(
        "<b>Fat embolism syndrome (FES)</b> occurs most often 24 to 72 hours after a fracture of a long bone (especially the femur) or the "
        "pelvis, or after surgery on the marrow canal. Fat globules from the marrow enter torn veins and lodge in the lungs, brain and "
        "skin. Free fatty acids released from the fat damage the capillaries, causing inflammation and leaky lung capillaries.",
        "<b>The classic triad:</b> respiratory distress with hypoxemia (SpO₂ 86%, PO₂ 54 mm Hg, with a low PCO₂ from rapid breathing), "
        "neurologic changes (restlessness, confusion) and <b>petechiae</b> on the chest, axillae and conjunctivae, which usually appear "
        "last. Fever, tachycardia, a falling platelet count and anemia support the diagnosis.",
        "<b>Why not the others:</b> compartment syndrome causes severe pain and neurovascular changes in the limb, but his foot is warm "
        "with strong pulses and his pain is 4/10. His blood pressure is stable, so this is not hypovolemic shock; some fall in hemoglobin "
        "after surgery is expected. Alcohol withdrawal can cause confusion but not hypoxemia and petechiae. Fever and the hemoglobin value "
        "alone do not point to a cause.",
        "<b>Priority:</b> airway and breathing come first. The client's oxygenation is failing (impaired gas exchange), which also "
        "explains his confusion. Pain, infection risk and mobility matter but are not life-threatening now."),
})

# ---------------------------------------------------------------- Screen 4 (generate solutions): select all
s4 = screen(4, INTRO, C, {
    "type": "select_all",
    "stem": "Which actions should the nurse take at this time? <b>Select all that apply.</b>",
    "options": opts(
        ("Stay with the client and call the rapid response team", True),
        ("Raise the head of the bed", True),
        ("Apply oxygen according to the unit's protocol and monitor SpO₂ continuously", True),
        ("Reassess level of consciousness and breathing frequently", True),
        ("Handle the right leg as little as possible and keep it supported in alignment", True),
        ("Massage the right calf to improve circulation", False),
        ("Lower the head of the bed and raise the legs", False),
        ("Help the client walk to the bathroom to expand his lungs", False),
        ("Offer cold oral fluids to bring down the fever", False),
        ("Recheck the vital signs at the next scheduled time, 0400", False),
        seed="c2s4"),
    "explanation": rationale(
        "<b>Correct:</b> the client's oxygenation and level of consciousness are deteriorating, so the nurse stays with him and calls the "
        "rapid response team. Raising the head of the bed improves lung expansion and oxygenation. Oxygen is started under the unit's "
        "protocol, with continuous pulse oximetry. Frequent reassessment shows whether he is improving or needs airway support. Moving the "
        "fractured limb as little as possible limits further release of fat from the marrow.",
        "<b>Incorrect:</b> massaging the calf could dislodge a clot if a deep vein thrombosis is present and does nothing for the lungs. "
        "Lowering the head of the bed worsens breathing. A confused, hypoxemic client with a newly repaired femur must not walk. Oral fluids "
        "risk aspiration in a confused, breathless client. Waiting for the next scheduled check delays care while he deteriorates."),
})

# ---------------------------------------------------------------- Screen 5 (take action): ordered response
C.notes("nn", "Nurses' Notes", ("Day 6 1000",
    "Fat embolism syndrome resolved with supportive care; transferred back from the intensive care unit on Day 5. SpO₂ 97% on room air, "
    "alert and oriented. Walking with crutches, partial weight bearing on the right leg as prescribed. Discharge planned for tomorrow. "
    "Client asks, “How long until my leg is back to normal? What is actually happening in the bone?”"))
C.vitals("Day 6 1000", vs("36.8° C", "84 beats/min", "16 breaths/min", "124/76 mm Hg", "97% on room air"))
s5 = screen(5, INTRO, C, {
    "type": "ordered_response",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 6 1000 and the Vital Signs from Day 6 1000.",
    "stem": "The nurse uses the client's question to teach him how a fracture heals. Place the stages of bone healing in order, "
            "from the first stage to the last.",
    "options": [],
    "orderedOptions": [
        "Hematoma formation: bleeding at the fracture forms a clot between the bone ends, and inflammation begins",
        "Cellular proliferation: new capillaries, fibroblasts and bone-forming cells grow into the clot, forming granulation tissue",
        "Callus formation: cartilage and immature (woven) bone form a soft callus that bridges the fracture",
        "Ossification: the callus is mineralized into hard bone, uniting the fragments",
        "Remodeling: osteoclasts remove excess callus and the bone regains its shape and strength",
    ],
    "explanation": rationale(
        "<b>1. Hematoma formation (first days):</b> torn blood vessels bleed into the fracture site and a clot forms. Inflammatory cells "
        "clear debris, and the clot becomes the framework for repair.",
        "<b>2. Cellular proliferation (about days 3 to 14):</b> capillaries, fibroblasts and osteoblasts invade the clot, turning it into "
        "granulation tissue.",
        "<b>3. Callus formation (weeks 2 to 6):</b> cartilage and woven bone form a callus around and between the bone ends. The fracture "
        "is held together but is not yet strong, which is why weight bearing is limited.",
        "<b>4. Ossification (weeks 3 to 12 or more):</b> minerals are laid down and the callus becomes hard bone. On X-ray, bridging bone "
        "crosses the fracture line.",
        "<b>5. Remodeling (months to a year or more):</b> osteoclasts remove the excess callus and the bone is reshaped along the lines "
        "of stress, restoring near-normal strength.",
        "Healing times vary with the bone, the age of the client, the blood supply and other factors. A large weight-bearing bone such as "
        "the femur typically takes several months to unite. Smoking, poor nutrition, low vitamin D, infection, diabetes, corticosteroids "
        "and movement at the fracture site all slow healing."),
})

# ---------------------------------------------------------------- Screen 6 (evaluate outcomes): matrix
C.notes("nn", "Nurses' Notes", ("Day 180 1000",
    "Orthopedic clinic follow-up, 6 months after injury. Left shoulder has full range of motion with no further dislocations. Sensation "
    "over the outer left upper arm is normal. Reports aching at the fracture site whenever he puts full weight on the right leg; takes "
    "ibuprofen 400 mg three times a day most days. Started smoking 10 cigarettes a day while recovering “because I was bored.” Right "
    "foot warm, pedal pulses 2+, no calf swelling or tenderness. Walking with crutches as instructed."))
C.notes("dx", "Diagnostic Results", ("Day 180 0930",
    "<b>X-ray, right femur:</b> intramedullary nail in place. Callus present, but the fracture line is still clearly visible and the "
    "callus does not bridge the fracture. Consistent with delayed union."))
C.vitals("Day 180 1000", vs("36.7° C", "78 beats/min", "16 breaths/min", "122/74 mm Hg", "98% on room air"))
C.labs("Day 180 0930", [
    (lab("Hemoglobin (Hgb)", "Male: 125–170 g/L"), "146 g/L"),
    (lab("Vitamin D (25-hydroxyvitamin D)", "75–250 nmol/L"), "38 nmol/L"),
])
s6 = screen(6, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 180 1000, the Diagnostic Results from Day 180, the Vital Signs from "
                "Day 180, and the Laboratory Results from Day 180.",
    "stem": "For each finding at the 6-month visit, click to specify whether it shows that an <b>expected outcome has been met</b> or that "
            "it <b>requires follow-up</b>.",
    "matrix": matrix_mc("Finding", ["Expected outcome met", "Requires follow-up"], [
        ("Fracture line still visible, with callus that does not bridge the fracture", 1),
        ("Full range of motion of the left shoulder with no further dislocations", 0),
        ("Smokes 10 cigarettes per day", 1),
        ("Normal sensation over the outer left upper arm", 0),
        ("Aching at the fracture site with full weight bearing, managed with ibuprofen most days", 1),
        ("Right foot warm with pedal pulses 2+ and no calf swelling", 0),
        ("Vitamin D 38 nmol/L", 1),
        ("Hemoglobin 146 g/L", 0),
    ]),
    "explanation": rationale(
        "<b>Expected outcomes met:</b> the shoulder has healed without recurrence and the axillary nerve has recovered. Circulation to the "
        "right leg is normal with no signs of deep vein thrombosis. The hemoglobin has returned to normal after the blood loss.",
        "<b>Requires follow-up: delayed union.</b> By 6 months a femur would be expected to show bridging bone. A fracture that heals more "
        "slowly than expected is a <b>delayed union</b>; if healing stops altogether it becomes a <b>nonunion</b>; a fracture that heals "
        "in a poor position is a <b>malunion</b>. Pain at the fracture site with weight bearing is a sign that the bone has not united.",
        "<b>Factors slowing his healing, which the nurse reports and addresses:</b> <b>smoking</b> (nicotine constricts blood vessels and "
        "reduces oxygen delivery to the healing bone); <b>low vitamin D</b> (needed to absorb calcium for mineralizing the callus); and "
        "regular <b>NSAID</b> use (evidence suggests NSAIDs may interfere with the inflammatory phase of bone healing). The nurse reports "
        "these findings to the provider, offers smoking cessation support, and reinforces nutrition with enough protein, calcium and "
        "vitamin D."),
})

write_case(ID, 2,
    "22-year-old male client after a motorcycle collision with a closed comminuted femur fracture and an anterior shoulder dislocation "
    "(after earlier subluxations); fracture types, dislocation vs subluxation, fat embolism syndrome on Day 3, the five stages of bone "
    "healing, and delayed union at 6 months.",
    [s1, s2, s3, s4, s5, s6],
    ["Screen 5: the five stages of bone healing are worded hematoma, cellular proliferation, callus, ossification, remodeling; match your "
     "textbook's names.",
     "Screen 6: the NSAID effect on bone healing is described as possible (the evidence is mixed); timing of delayed union for the femur "
     "(no bridging at 6 months) should suit your teaching.",
     "Screen 3: timing of fat embolism (about 36 hours after injury) and the ABG values are illustrative."])
