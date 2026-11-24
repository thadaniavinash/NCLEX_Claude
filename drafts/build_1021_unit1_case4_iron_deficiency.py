"""NURS 1021 Unit 1 Case Study 4: iron deficiency anemia from heavy menstrual bleeding (uterine fibroids) and a vegan
diet; differentiation from thalassemia trait and anemia of chronic disease; oral iron, then IV iron sucrose.
Outcomes: etiology, pathogenesis and clinical manifestations of iron deficiency anemia (also anemia assessments).
Facts checked against the Merck Manual Professional Edition, "Iron Deficiency Anemia" (full review Mar 2025):
blood loss as the main cause (menstrual loss in premenopausal women); stages (ferritin < 30 ng/mL = 67 pmol/L,
i.e. < 30 µg/L; transferrin saturation < 15%; then microcytosis); high RDW, low reticulocytes; pica (ice), glossitis,
cheilosis, koilonychia, restless legs; oral iron 30 minutes before meals, 65 mg elemental every other day, vitamin C
helps, milk/tea/antacids/fibre impair; reticulocytosis after about 1 week, Hgb rise of about 10 g/L at 14 days,
anemia corrected within 2 months, continue for 6 months after; IV iron for intolerance or ongoing loss; always find
the cause."""
from nurs1021_common import *

INTRO = ("The nurse in a primary care clinic is assessing Amara, a 34-year-old female client who reports increasing "
         "tiredness over the past 4 months.")
C = Chart2()
C.notes("nn", "Nurses' Notes", ("0930",
    "Reports being “exhausted all the time” and short of breath climbing one flight of stairs. Periods have become "
    "heavier over the past year: lasts 8 days, changes a soaked pad every 1 to 2 hours on the heaviest days, passes "
    "large clots. Follows a vegan diet for 3 years. Says she has been craving and chewing ice “all day.” Has an "
    "uncomfortable urge to move her legs when lying in bed at night. Conjunctivae and palms pale. Fingernails thin and "
    "spoon-shaped. Cracks at both corners of the mouth; tongue smooth, red and sore. Soft systolic murmur at the left "
    "sternal border. No numbness or tingling in the hands or feet; gait steady. No jaundice. Seasonal allergies treated "
    "with loratadine. BMI 22.4 kg/m<sup>2</sup>."))
VS = [vrow("T"), vrow("P"), vrow("RR"), vrow("BP"), vrow(SPO2)]


def vitals(col, *v):
    C.column("vs", "Vital Signs", "", col, list(zip(VS, v)))


vitals("0930", "36.8° C", "108 beats/min", "20 breaths/min", "108/68 mm Hg", "98% on room air")
s1 = screen(1, INTRO, C, select_all(411, [
    ("A", "Tiredness and shortness of breath on one flight of stairs", True),
    ("B", "Craving and chewing ice", True),
    ("C", "Thin, spoon-shaped fingernails", True),
    ("D", "Cracks at the corners of the mouth and a smooth, sore tongue", True),
    ("E", "Pale conjunctivae with a heart rate of 108 beats/min", True),
    ("F", "Urge to move the legs when lying in bed at night", True),
    ("G", "No numbness or tingling in the hands or feet", False),
    ("H", "Seasonal allergies treated with loratadine", False)],
    rationale(
        "<b>Consistent with iron deficiency anemia:</b> with less hemoglobin, the blood carries less oxygen, causing "
        "tiredness and dyspnea on exertion {A}, pallor, and a faster heart rate (with a flow murmur) as the heart "
        "compensates {E}. Severe iron deficiency also causes <b>pica</b>, a craving for non-food items, most often ice "
        "(pagophagia) {B}; <b>koilonychia</b>, thin spoon-shaped nails {C}; <b>angular cheilitis</b> and <b>glossitis</b> "
        "{D}; and restless legs syndrome, an unpleasant urge to move the legs at rest {F}.",
        "<b>Not consistent:</b> the absence of numbness and tingling is a relevant negative: neurologic symptoms with "
        "anemia suggest vitamin B12 deficiency, not iron deficiency {G}. Seasonal allergies are unrelated {H}."),
    stem="The nurse reviews the client's history and assessment. Which of the following findings would be consistent "
         "with <b>iron deficiency anemia</b>? Select all that apply."))

# Screen 2
C.notes("nn", "Nurses' Notes", ("Day 2 1100",
    "Laboratory results reviewed by the nurse practitioner. Amara says her sister was told she has thalassemia trait and "
    "asks whether she could have the same thing."))
LAB = [lab("Hemoglobin (Hgb)", "Female: 115–155 g/L"), lab("Hematocrit (Hct)", "0.38–0.50 L/L"),
       lab("Red blood cell (RBC) count", "Female: 3.50–5.00 × 10<sup>12</sup>/L"),
       lab("Mean corpuscular volume (MCV)", "80–100 fL"), lab("Red cell distribution width (RDW)", "11.5%–15.5%"),
       lab("Reticulocyte percentage", "0.5%–1.5%"), lab("Platelet count", "130–380 × 10<sup>9</sup>/L"),
       lab("Ferritin", "Female: 11–307 µg/L"), lab("Iron", "Female: 9–30 µmol/L"),
       lab("Iron-binding capacity, total (TIBC)", "45–81 µmol/L"), lab("Transferrin saturation", "0.20–0.50"),
       "<b>Peripheral blood smear</b>"]
C.column("labs", "Laboratory Results", "Laboratory Test and Reference Range", "Day 1 1015", list(zip(LAB, [
    "86 g/L", "0.29 L/L", "3.62 × 10<sup>12</sup>/L", "68 fL", "19.8%", "0.6%", "452 × 10<sup>9</sup>/L", "4 µg/L",
    "4 µmol/L", "88 µmol/L", "0.05", "Small, pale (microcytic, hypochromic) red cells of varying size; pencil cells"])))
s2 = screen(2, "Amara returns the next day to review her blood work.", C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 2 1100 and the Laboratory Results.",
    "stem": "The nurse explains how microcytic anemias are told apart. For each finding, click to specify whether it is "
            "most consistent with <b>iron deficiency anemia</b>, <b>beta-thalassemia trait</b>, or <b>anemia of chronic "
            "disease</b>.",
    "matrix": matrix_mc("Finding", ["Iron Deficiency Anemia", "Beta-Thalassemia Trait", "Anemia of Chronic Disease"], [
        ("Raised hemoglobin A2 on hemoglobin electrophoresis", 1),
        ("Ferritin below 30 µg/L", 0),
        ("Low serum iron with normal or low TIBC and normal or high ferritin, in a client with rheumatoid arthritis", 2),
        ("Total iron-binding capacity above the reference range", 0),
        ("Marked microcytosis with a normal RDW and a normal or high red cell count", 1),
        ("Mild anemia with normal-sized red cells that develops over months of chronic inflammation", 2)]),
    "explanation": rationale(
        "<b>Iron deficiency anemia:</b> iron stores are used up first, so <b>ferritin</b> (stored iron) falls; a ferritin "
        "below 30 µg/L is specific for iron deficiency. The liver makes more transferrin to capture what iron there is, so "
        "the TIBC rises while serum iron and transferrin saturation fall. Only then are red cells made small and pale, with "
        "a wide range of sizes (high RDW). Amara has all of these: ferritin 4 µg/L, TIBC 88 µmol/L, saturation 0.05, MCV "
        "68 fL, RDW 19.8%. The low reticulocyte count shows the marrow cannot respond without iron, and a raised platelet "
        "count is common in iron deficiency.",
        "<b>Beta-thalassemia trait:</b> reduced beta-globin chain production makes small cells even though iron is "
        "normal, so ferritin is normal. Cells are uniformly small (normal RDW) and the marrow makes more of them, so the red "
        "cell count is normal or high. Hemoglobin electrophoresis shows a raised HbA2. Her low ferritin and high RDW point to "
        "iron deficiency; thalassemia trait can coexist and is checked once iron is replaced if microcytosis persists.",
        "<b>Anemia of chronic disease:</b> inflammation raises hepcidin, which traps iron in stores. Serum iron is low but "
        "ferritin is normal or high and the TIBC normal or low. The anemia is usually mild and normocytic."),
})

# Screen 3
C.notes("nn", "Nurses' Notes", ("Day 2 1130",
    "Pelvic ultrasound last month (ordered by her family physician for heavy periods) showed two uterine fibroids. "
    "Amara works 12-hour shifts as a warehouse supervisor, climbing stairs and ladders. Says she felt dizzy on standing "
    "twice this week. Orthostatic vital signs taken."))
C.column("vs", "Vital Signs", "", "Day 2 1130 (lying)", list(zip(VS[1:4], ["96 beats/min", "18 breaths/min", "110/70 mm Hg"])))
C.column("vs", "Vital Signs", "", "Day 2 1133 (standing)", list(zip(VS[1:4], ["112 beats/min", "18 breaths/min",
                                                                                "104/68 mm Hg"])))
s3 = screen(3, "Amara returns the next day to review her blood work.", C, {
    "type": "dropdown_cloze",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 2 1130 and the Vital Signs.",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {"text": "Amara's anemia is caused by [[drop0]], so her marrow makes small, pale red cells with too little "
                      "hemoglobin. The main reason her iron stores are depleted is [[drop1]]. The nurse's priority concern "
                      "is [[drop2]].",
              "dropdowns": [
                  dd(431, "too little iron to make hemoglobin", "too little vitamin B12 to make DNA",
                     "early destruction of red cells", "failure of the bone marrow stem cells"),
                  dd(432, "ongoing blood loss from heavy menstrual bleeding", "a vegan diet that contains no iron",
                     "loratadine blocking iron absorption", "an inherited defect in globin chains"),
                  dd(433, "a risk of falls from dizziness and reduced oxygen delivery",
                     "a risk of bleeding from a low platelet count",
                     "nerve damage from vitamin deficiency",
                     "an altered body image from nail changes")]},
    "explanation": rationale(
        "<b>Pathogenesis:</b> iron is needed to build heme. Without it, red cell precursors keep dividing while they wait "
        "for hemoglobin, so the cells end up small (microcytic) and pale (hypochromic). Vitamin B12 deficiency impairs DNA "
        "synthesis and makes large cells; hemolysis and marrow failure have other laboratory patterns.",
        "<b>Cause:</b> in a premenopausal woman, menstrual loss is the most common cause; each 1 mL of blood holds about "
        "0.5 mg of iron, and heavy bleeding (here from fibroids) loses several times the normal amount every cycle. Her vegan "
        "diet adds to the problem because plant (non-heme) iron is absorbed less well than iron from meat, but plant foods "
        "do contain iron. Iron therapy without finding the source of loss is poor practice, so the fibroids are referred to "
        "gynecology. Loratadine does not affect iron absorption; her ferritin rules out thalassemia as the cause.",
        "<b>Priority:</b> her heart rate rises 16 beats/min on standing, she has had dizziness, and she climbs ladders at "
        "work: reduced oxygen-carrying capacity puts her at risk of falls and injury. Her platelet count is high, not low, "
        "and she has no neurologic signs."),
})

# Screen 4
C.notes("nn", "Nurses' Notes", ("Day 2 1145",
    "Nurse practitioner prescribes ferrous sulfate 300 mg (60 mg elemental iron) PO every other day and a referral to "
    "gynecology. Amara asks how to take the tablets and which foods will help."))
s4 = screen(4, "Amara returns the next day to review her blood work.", C, select_all(441, [
    ("A", "Take the iron tablet 30 minutes before a meal, with a glass of orange juice", True),
    ("B", "Take the tablet at least 2 hours apart from milk, tea, coffee and antacids", True),
    ("C", "Expect your stools to turn dark green or black while taking iron", True),
    ("D", "Eat beans, lentils, tofu and iron-fortified cereals with foods rich in vitamin C", True),
    ("E", "Drink more fluids and eat more fibre if you become constipated", True),
    ("F", "Take the tablet with a glass of milk to prevent an upset stomach", False),
    ("G", "Stop taking the iron once you no longer feel tired", False),
    ("H", "Take two tablets the next day if you miss a dose", False)],
    rationale(
        "<b>Include:</b> iron is absorbed best on an empty stomach, about 30 minutes before meals; vitamin C (orange juice "
        "or a 500 mg tablet) keeps iron in the absorbable ferrous form {A}. Calcium in milk, tannins in tea, polyphenols in "
        "coffee, antacids and some antibiotics bind iron, so they are separated from the dose {B}. Dark green or black "
        "stools are an expected, harmless effect; tarry stools with abdominal pain or dizziness are reported {C}. A vegan "
        "diet can supply enough iron if non-heme sources are eaten with vitamin C {D}. Constipation is the most common "
        "adverse effect {E}.",
        "<b>Do not include:</b> milk reduces absorption {F}. Feeling better comes before the stores are refilled; iron "
        "continues for about 6 months after the hemoglobin is normal {G}. Doubling a dose increases nausea and constipation "
        "and is not absorbed well; every-other-day dosing is used because each dose raises hepcidin, which blocks the "
        "absorption of the next one for about a day {H}."),
    preamble="The nurse has reviewed the Nurses' Notes from Day 2 1145.",
    stem="Which instructions should the nurse include in Amara's teaching? Select all that apply."))

# Screen 5
C.notes("nn", "Nurses' Notes", ("Week 4 1000",
    "Amara stopped the iron tablets after 10 days because of nausea and constipation. Periods remain heavy; gynecology "
    "appointment in 6 weeks. Hemoglobin today 88 g/L. The nurse practitioner prescribes iron sucrose 200 mg IV over "
    "15 minutes, once a week for 5 doses, starting today in the clinic."))
vitals("Week 4 1000", "36.7° C", "104 beats/min", "18 breaths/min", "106/66 mm Hg", "98% on room air")
s5 = screen(5, "Four weeks later, Amara returns for follow-up.", C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Week 4 1000 and the Vital Signs.",
    "stem": "For each nursing action, click to specify whether the action is <b>Indicated</b>, <b>Non-Essential</b>, or "
            "<b>Contraindicated</b> for the IV iron infusion.",
    "matrix": matrix_mc("Nursing Action", IMC, [
        ("Take vital signs before the infusion and monitor during it", 0),
        ("Check the IV site for patency and leakage during the infusion", 0),
        ("Give the iron by intramuscular injection if the IV insertion is difficult", 2),
        ("Give a test dose of iron sucrose before the first full dose", 1),
        ("Observe Amara for at least 30 minutes after the infusion", 0),
        ("Tell Amara to take her iron tablets on infusion days for a faster response", 2)]),
    "explanation": rationale(
        "<b>Indicated:</b> IV iron can cause hypersensitivity reactions (flushing, chest tightness, dyspnea, hypotension), "
        "so vital signs are taken before and during the infusion and the client is observed for at least 30 minutes after; "
        "the infusion is stopped and help called at the first sign of a reaction. Leakage of iron into the tissues causes "
        "pain and long-lasting brown staining of the skin, so the site is checked throughout.",
        "<b>Non-Essential:</b> current iron sucrose products do not need a test dose; test doses were used with the old "
        "high-molecular-weight iron dextran.",
        "<b>Contraindicated:</b> iron sucrose is given only IV; intramuscular iron is painful, stains the skin and is no "
        "longer used. Oral iron is not combined with IV iron; IV iron raises hepcidin, so oral iron would be poorly "
        "absorbed and would only add adverse effects."),
})

# Screen 6
S6_NOTE = [("Week 12 1000",
    "Received all 5 doses of iron sucrose without reaction. {Says she has “far more energy” and climbs stairs at work "
    "without stopping.|correct} {No longer craves ice.|correct} {Legs no longer restless at night.|correct} "
    "{Corners of the mouth healed.|correct} {Nails still thin and spoon-shaped.} {Periods still heavy, with clots; "
    "gynecology visit next week.} {Heart rate 82 beats/min.|correct} {Hemoglobin 121 g/L|correct} and "
    "{ferritin 142 µg/L.|correct} {MCV 79 fL.}")]
C.notes("nn", "Nurses' Notes", *S6_NOTE)
vitals("Week 12 1000", "36.6° C", "82 beats/min", "16 breaths/min", "112/70 mm Hg", "99% on room air")
C.column("labs", "Laboratory Results", "Laboratory Test and Reference Range", "Week 12 0900", list(zip(
    [LAB[0], LAB[3], LAB[4], LAB[5], LAB[7], LAB[10]], ["121 g/L", "79 fL", "17.2%", "1.2%", "142 µg/L", "0.26"])))
s6 = screen(6, "Twelve weeks after her first visit, Amara returns for follow-up.", C, {
    "type": "highlight",
    "preamble": "The nurse has reviewed the Nurses' Notes from Week 12 1000, the Vital Signs, and the Laboratory Results.",
    "stem": "<b>Highlight</b> the findings that indicate that the treatment of Amara's anemia has been effective.",
    "options": [],
    "highlightTabs": [highlight_tab("ht6", "Nurses' Notes", S6_NOTE)],
    "maxCorrectSelections": None,
    "explanation": rationale(
        "<b>Effective:</b> more energy and climbing stairs without stopping show better oxygen delivery, as do a heart rate "
        "down from 108 to 82 beats/min. Hemoglobin rose from 86 to 121 g/L and ferritin from 4 to 142 µg/L, showing that "
        "the stores are refilled (with IV iron, ferritin rises quickly). Pica, restless legs and angular cheilitis resolve "
        "as iron is replaced.",
        "<b>Not yet evidence of effect:</b> nails take months to grow out, so spoon-shaped nails persist for some time. The "
        "MCV (79 fL) is still slightly low because cells made before treatment are still circulating; it normalizes as "
        "they are replaced over about 120 days. Ongoing heavy bleeding is the <b>cause</b>, which iron does not treat: "
        "without gynecologic treatment of the fibroids, she will become iron deficient again."),
})
write_case(1, 4,
    "34-year-old female with fatigue, pica and koilonychia from heavy menstrual bleeding (fibroids) and a vegan diet: "
    "iron deficiency anemia, iron studies compared with thalassemia trait and anemia of chronic disease, oral iron "
    "teaching and IV iron sucrose.",
    [s1, s2, s3, s4, s5, s6],
    "New case written by Claude on 24 Nov 2026 (NURS 1021 Unit 1, batch 1); checked against Merck Manual Professional "
    "(Iron Deficiency Anemia, Mar 2025). Please review: ferrous sulfate 300 mg (60 mg elemental) every other day "
    "(Merck's alternate-day dosing; many Canadian prescribers still use daily dosing); iron sucrose 200 mg IV weekly × 5 "
    "and the 30-minute observation (check against your agency's policy).")
