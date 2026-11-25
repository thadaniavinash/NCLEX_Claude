"""NURS 1021 Unit 1 Case Study 2: severe hemophilia A with an acute knee hemarthrosis, then a minor head injury.
Outcomes: assessments and diagnostic tests of hemostasis and coagulation (PT/INR, aPTT, platelets, fibrinogen,
mixing study, factor assays); hemophilia A and B and their impact on homeostasis; clinical manifestations.
Facts checked against the Merck Manual Professional Edition, "Hemophilia" (full review Jul 2025): factor VIII
(A, about 80%) vs IX (B), X-linked; severity <1% severe, 1-5% moderate, 5-49% mild; prolonged PTT with normal PT
and platelets; mixing study; FVIII targets 50-80% for severe joint bleeds, 100% for intracranial bleeding;
desmopressin only for mild hemophilia A (>=5%) with proven response; avoid aspirin/NSAIDs and IM injections;
treat suspected intracranial bleeding before CT."""
from nurs1021_common import *

INTRO = ("The nurse in the emergency department is caring for a 22-year-old male client with severe hemophilia A who "
         "arrived with right knee pain.")
C = Chart2()
C.notes("nn", "Nurses' Notes", ("Day 1 1830",
    "The client arrived at the emergency department with a roommate, reporting right knee pain that began after a "
    "collision during a basketball game 6 hours ago. The client states that the knee “felt tingly and warm” before it "
    "became painful and stiff. The health history and physical assessment were completed."))
S1_HX = [
    sec("Reason for visit", "Right knee pain and swelling after a collision during a basketball game 6 hours ago."),
    sec("Medical history", "Severe hemophilia A (factor VIII activity less than 1%), diagnosed in infancy. "
        "{This is the third bleed into the right knee this year.|correct}"),
    sec("Medications", "Recombinant factor VIII IV three times a week, self-infused at home as prophylaxis. "
        "{The client has missed the last two prophylactic factor VIII infusions during university examinations.|correct} "
        "{The client took ibuprofen 400 mg PO twice at home today for the pain.|correct}"),
    sec("Weight", "70 kg.")]
S1_PA = [
    sec("Neurological", "{The client is alert and oriented × 4.}"),
    sec("Musculoskeletal", "{The right knee is swollen, warm and tense.|correct} {The client holds the right knee flexed "
        "at about 30° and cannot extend it fully.|correct} {The right knee circumference is 42 cm; the left knee "
        "circumference is 37 cm.|correct}"),
    sec("Neurovascular, right foot", "{Pedal pulses are 2+.} {Capillary refill is less than 2 seconds.} {Sensation is "
        "intact.}"),
    sec("Pain", "{The client rates the right knee pain at 8/10.|correct}")]
C.doc("hx", "Health History", *S1_HX)
C.doc("pa", "Physical Assessment", *S1_PA)
VS = [vrow("T"), vrow("P"), vrow("RR"), vrow("BP"), vrow(SPO2), vrow("Pain (0–10)")]


def vitals(col, *v):
    C.column("vs", "Vital Signs", "", col, list(zip(VS, v)))


vitals("Day 1 1830", "37.4° C", "102 beats/min", "18 breaths/min", "132/78 mm Hg", "98% on room air", "8")
s1 = screen(1, INTRO, C, {
    "type": "highlight",
    "stem": "The nurse reviews the Health History and the Physical Assessment. <b>Highlight</b> the findings that require "
            "follow-up.",
    "options": [],
    "highlightTabs": [highlight_doc("ht1", "Health History", S1_HX), highlight_doc("ht2", "Physical Assessment", S1_PA)],
    "maxCorrectSelections": None,
    "explanation": rationale(
        "<b>Require follow-up:</b> a swollen, warm, tense knee held in flexion, with severe pain and a 5 cm difference in "
        "circumference, is an acute <b>hemarthrosis</b> (bleeding into the joint), the most common bleed in severe hemophilia. "
        "Blood in the joint space raises pressure and the client holds the knee bent because that is the position of greatest "
        "joint volume. A tingling or warm feeling often comes before swelling, so pain is an early sign.",
        "Missing two prophylactic factor VIII infusions left the client with almost no factor VIII, so a minor collision caused a "
        "major bleed. Ibuprofen inhibits platelet function and adds to the bleeding; clients with hemophilia avoid aspirin and "
        "NSAIDs. A third bleed into the same joint this year makes the right knee a <b>target joint</b>: repeated bleeds "
        "inflame the synovium (synovitis), which bleeds more easily and leads to hemophilic arthropathy.",
        "<b>Do not require follow-up:</b> strong pedal pulses, brisk capillary refill and normal sensation show that blood "
        "flow and nerves below the knee are intact. The client is alert and oriented."),
})

# Screen 2
C.notes("nn", "Nurses' Notes", ("Day 1 1915",
    "The hematology service was paged. The right knee was splinted and elevated on pillows. The client asked how "
    "hemophilia A differs from the hemophilia B that a cousin has, and why the desmopressin nasal spray that an uncle with "
    "mild hemophilia uses cannot be used."))
LAB = [lab("Hemoglobin (Hgb)", "Male: 125–170 g/L"), lab("Platelet count", "130–380 × 10<sup>9</sup>/L"),
       lab("Prothrombin time (PT)", "10–14 s"), lab("International normalized ratio (INR)", "0.9–1.2"),
       lab("Activated partial thromboplastin time (aPTT)", "22–30 s"), lab("Fibrinogen", "2.0–4.0 g/L"),
       lab("aPTT mixing study (1:1 with normal plasma)", "Corrects to the reference range"),
       lab("Factor VIII activity", "50%–150%"), lab("Factor IX activity", "50%–150%")]
C.column("labs", "Laboratory Results", "Laboratory Test and Reference Range", "Day 1 1850", list(zip(LAB, [
    "138 g/L", "245 × 10<sup>9</sup>/L", "12 s", "1.0", "68 s", "3.1 g/L", "Corrects to 29 s", "less than 1%", "94%"])))
s2 = screen(2, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 1 1915 and the Laboratory Results.",
    "stem": "The nurse answers the client's questions. For each statement, click to specify whether it applies to "
            "<b>hemophilia A</b>, <b>hemophilia B</b>, or <b>both</b>.",
    "matrix": matrix_mc("Statement", ["Hemophilia A", "Hemophilia B", "Both"], [
        ("Caused by a deficiency of factor IX (also called Christmas disease)", 1),
        ("Inherited as an X-linked recessive disorder, so it occurs mainly in males", 2),
        ("Caused by a deficiency of factor VIII and accounts for about 80% of cases", 0),
        ("Prolonged aPTT with a normal PT and platelet count", 2),
        ("Mild forms may be treated with desmopressin, which releases stored factor", 0),
        ("Repeated bleeding into a joint can lead to chronic synovitis and arthropathy", 2)]),
    "explanation": rationale(
        "<b>Hemophilia A</b> is a deficiency of factor VIII and makes up about 80% of cases. Desmopressin (DDAVP) releases "
        "factor VIII and von Willebrand factor stored in endothelial cells, so it can raise the level about two- to threefold "
        "in <b>mild</b> hemophilia A (factor VIII 5% or higher) in clients who have been shown to respond. It cannot help when "
        "there is no factor VIII to release, as in this client's severe disease (less than 1%), or in hemophilia B.",
        "<b>Hemophilia B</b> (Christmas disease) is a deficiency of factor IX.",
        "<b>Both</b> are X-linked recessive, so males are mainly affected and the daughters of an affected male are carriers. "
        "Factors VIII and IX both belong to the intrinsic pathway, so both prolong the aPTT while the PT (extrinsic pathway) "
        "and platelet count stay normal; only factor assays tell them apart. Both cause the same bleeding: hemarthroses, "
        "muscle hematomas and, after even minor head trauma, intracranial hemorrhage. Severity depends on the factor level: "
        "below 1% severe (spontaneous bleeding), 1% to 5% moderate (bleeding after minor trauma), 5% to 49% mild (bleeding "
        "after surgery or dental extraction)."),
})

# Screen 3
C.notes("nn", "Nurses' Notes", ("Day 1 1940",
    "The client rates the right knee pain at 8/10. The right knee circumference is now 43 cm. The right foot is warm, "
    "with 2+ pedal pulses. The hematologist reviewed the laboratory results by telephone and will enter orders."))
vitals("Day 1 1940", "37.4° C", "104 beats/min", "18 breaths/min", "134/80 mm Hg", "98% on room air", "8")
s3 = screen(3, INTRO, C, {
    "type": "dropdown_cloze",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 1 1940 and the Vital Signs.",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {"text": "A prolonged aPTT with a normal PT, INR and platelet count points to a defect in the [[drop0]]. "
                      "Because the aPTT corrects when the client's plasma is mixed with normal plasma, the cause is [[drop1]]. "
                      "The nurse's priority is [[drop2]].",
              "dropdowns": [
                  dd(231, "intrinsic pathway of coagulation", "extrinsic pathway of coagulation",
                     "formation of the platelet plug", "breakdown of clots by fibrinolysis"),
                  dd(232, "a missing clotting factor", "an antibody that inhibits factor VIII",
                     "a lack of vitamin K", "consumption of clotting factors"),
                  dd(233, "stopping the bleeding into the knee", "preventing infection in the knee",
                     "restoring knee range of motion", "teaching about the inheritance of hemophilia")]},
    "explanation": rationale(
        "<b>Reading the tests:</b> the aPTT measures the intrinsic and common pathways (factors XII, XI, IX, VIII, then X, V, "
        "II and fibrinogen); the PT and INR measure the extrinsic and common pathways (factor VII, then X, V, II, fibrinogen). "
        "A normal platelet count and fibrinogen with a prolonged aPTT and normal PT localize the problem to the intrinsic "
        "factors, which include VIII and IX.",
        "<b>Mixing study:</b> normal plasma supplies the missing factor, so a factor <b>deficiency</b> corrects. An "
        "<b>inhibitor</b> (an antibody against factor VIII, which develops in about 30% of clients with severe hemophilia A "
        "treated with factor) would also block the factor in the normal plasma, so the aPTT would stay prolonged. Vitamin K "
        "deficiency and consumption of factors (as in DIC) prolong the PT as well.",
        "<b>Priority:</b> the knee is still bleeding (circumference 42 to 43 cm, pain 8/10, rising heart rate). Ongoing "
        "bleeding threatens the joint now and increases blood loss; it is stopped by replacing factor VIII. Range of motion, "
        "infection risk and genetics teaching come after the bleeding is controlled."),
})

# Screen 4
C.notes("nn", "Nurses' Notes", ("Day 1 2000", "Hematology orders were received. A peripheral IV catheter was inserted in the left forearm."))
C.rows("orders", "Orders", ["Category", "Order"], [
    ["<b>Factor replacement</b>", "Recombinant factor VIII 3,500 units (50 units/kg) IV now, then 1,750 units IV every "
                                  "12 hours. Factor VIII activity 30 minutes after the first dose."],
    ["<b>Pain</b>", "Acetaminophen 1 g PO every 6 hours as needed (maximum 4 g/day). Hydromorphone 1 mg IV every 3 hours as "
                    "needed for severe pain."],
    ["<b>Activity</b>", "Bed rest with the right knee splinted and elevated. Ice pack, wrapped in a towel, 15 to 20 minutes "
                        "every 2 hours while awake."],
    ["<b>Precautions</b>", "Bleeding precautions. No aspirin or NSAIDs. No intramuscular injections."]])
s4 = screen(4, INTRO, C, select_all(241, [
    ("A", "Give the factor VIII infusion as soon as possible", True),
    ("B", "Keep the right knee at rest in the splint and elevated", True),
    ("C", "Apply the wrapped ice pack to the knee for 15 to 20 minutes at a time", True),
    ("D", "Give hydromorphone IV or acetaminophen PO for pain as prescribed", True),
    ("E", "Measure the knee circumference and check pulses and sensation in the foot regularly", True),
    ("F", "Give ibuprofen PO, since it eases both pain and joint inflammation", False),
    ("G", "Start active range-of-motion exercises of the knee tonight to prevent stiffness", False),
    ("H", "Apply a warm compress to the knee to relax the surrounding muscles", False)],
    rationale(
        "<b>Include:</b> factor VIII replacement is the treatment that stops the bleeding, and it is given as early as "
        "possible; a dose of 50 units/kg raises factor VIII to about 100%, since each unit/kg raises it about 2% {A}. Rest, "
        "splinting and elevation limit further bleeding and pain {B}. Cold causes local vasoconstriction and eases pain "
        "{C}. Acetaminophen and opioids relieve pain without affecting platelets; hydromorphone is given IV, never IM {D}. "
        "Circumference, pain and neurovascular checks show whether the bleeding is controlled and detect compression of "
        "nerves or vessels {E}.",
        "<b>Do not include:</b> NSAIDs and aspirin inhibit platelet function and increase bleeding {F}. Active exercise "
        "while the joint is still bleeding causes more bleeding; physiotherapy starts once pain and swelling settle {G}. "
        "Heat dilates blood vessels and increases bleeding {H}."),
    preamble="The nurse has reviewed the Nurses' Notes from Day 1 2000 and the Orders.",
    stem="Which interventions should the nurse include in the client's plan of care? Select all that apply."))

# Screen 5
C.notes("nn", "Nurses' Notes",
    ("Day 1 2045", "The factor VIII infusion was completed without reaction. The client rates the knee pain at 5/10. "
     "The right knee circumference is 43 cm."),
    ("Day 2 0610", "The client was found sitting on the bathroom floor and states having slipped while using crutches and "
     "struck the left side of the head on the sink. The client did not lose consciousness. The client is alert and oriented "
     "× 4, with a Glasgow Coma Scale score of 15, and pupils are equal and reactive to light. The client reports a headache "
     "rated 6/10 and mild nausea. A small swelling is present over the left temple. The provider was notified, and an urgent "
     "head CT was requested."))
vitals("Day 2 0615", "37.0° C", "88 beats/min", "16 breaths/min", "138/82 mm Hg", "98% on room air", "6 (head)")
s5 = screen(5, INTRO, C, multiple_choice(251, [
    ("A", "Anticipate a prescription for a factor VIII dose to be given immediately, before the CT scan", True),
    ("B", "Transport the client to CT first, since factor VIII is needed only if a bleed is confirmed", False),
    ("C", "Give acetaminophen for the headache and recheck the neurologic status in 1 hour", False),
    ("D", "Apply an ice pack to the left temple and keep the client on bed rest", False)],
    rationale(
        "<b>Correct {A}:</b> in a person with hemophilia, “even a trivial blow to the head” can cause intracranial "
        "hemorrhage, and a headache after head trauma is treated as a possible bleed. Factor replacement to about 100% begins "
        "<b>immediately, before</b> the CT scan or any other test is completed; waiting for imaging lets a bleed expand. The client's "
        "factor VIII level is falling since last night's dose, so a new dose is needed now.",
        "<b>Incorrect:</b> delaying factor until the CT confirms a bleed risks a fatal hemorrhage {B}. Treating the headache "
        "and waiting an hour misses the window to treat; a normal Glasgow Coma Scale now does not rule out a slowly expanding "
        "bleed {C}. Ice and rest do nothing to stop an intracranial bleed {D}. The nurse continues frequent neurologic checks "
        "once factor is given."),
    preamble="The nurse has reviewed the Nurses' Notes from Day 2 0610 and the Vital Signs.",
    stem="Which action should the nurse take <b>first</b>?"))

# Screen 6
C.notes("nn", "Nurses' Notes",
    ("Day 2 0800", "Factor VIII was given at 0625. The head CT at 0700 showed no intracranial hemorrhage."),
    ("Day 4 1000", "The client's headache has resolved, and neurologic checks are within normal limits. The client rates "
     "the right knee pain at 2/10. The right knee circumference is 38 cm, and the knee lacks 10° of full extension. The "
     "client is walking with crutches. The hematologist and the physiotherapist reviewed home prophylaxis, a graded exercise "
     "plan and a factor dose for any new bleed."))
vitals("Day 4 1000", "36.8° C", "76 beats/min", "16 breaths/min", "124/76 mm Hg", "99% on room air", "2")
C.column("labs", "Laboratory Results", "Laboratory Test and Reference Range", "Day 4 0600", list(zip(
    [LAB[0], LAB[4], LAB[7]], ["121 g/L", "31 s", "62% (trough before dose)"])))
s6 = screen(6, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 2 0800 and Day 4 1000, the Vital Signs, and the "
                "Laboratory Results.",
    "stem": "For each finding, click to specify whether the client's condition has <b>improved</b> or <b>not improved</b> "
            "compared with admission.",
    "matrix": matrix_mc("Finding", ["Improved", "Not Improved"], [
        ("Right knee circumference", 0),
        ("Hemoglobin", 1),
        ("Pain rating", 0),
        ("aPTT", 0),
        ("Knee extension", 0),
        ("Factor VIII activity", 0)]),
    "explanation": rationale(
        "<b>Improved:</b> knee circumference fell from 42 to 38 cm (right) as blood in the joint is reabsorbed; pain fell "
        "from 8/10 to 2/10; the knee now lacks only 10° of extension instead of 30°. Factor VIII replacement corrected the aPTT "
        "(68 s to 31 s) and the trough factor VIII is 62%, within the 50% to 80% target for a severe joint bleed.",
        "<b>Not improved:</b> hemoglobin fell from 138 to 121 g/L, reflecting the blood lost into the knee. It is now "
        "stable, but it is lower than on admission and is rechecked; a further fall would suggest another bleed.",
        "<b>Before discharge:</b> the nurse reinforces regular prophylaxis (missed doses caused this bleed), treating any "
        "bleed early with home factor, avoiding aspirin and NSAIDs, wearing medical identification, regular dental care, "
        "and seeking care at once for headache, vomiting or drowsiness after any head injury."),
})
write_case(1, 2,
    "22-year-old male with severe hemophilia A and an acute knee hemarthrosis after missed prophylaxis, then a minor head "
    "injury: coagulation tests (PT/INR, aPTT, mixing study, factor assays), hemophilia A versus B, factor replacement.",
    [s1, s2, s3, s4, s5, s6],
    "New case written by Claude on 24 Nov 2026 (NURS 1021 Unit 1, batch 1); checked against Merck Manual Professional "
    "(Hemophilia, Jul 2025). Please review: fibrinogen (2.0–4.0 g/L) and factor VIII/IX activity (50%–150%) reference "
    "ranges (not in the MCC list); factor VIII doses (50 units/kg, then 25 units/kg every 12 hours); ice for hemarthrosis "
    "(standard nursing teaching; some guidelines are less firm).")
