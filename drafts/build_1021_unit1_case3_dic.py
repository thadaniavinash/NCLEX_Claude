"""NURS 1021 Unit 1 Case Study 3: acute disseminated intravascular coagulation (DIC) in septic shock from
pyelonephritis. Outcomes: etiology, pathogenesis and clinical manifestations of DIC and its impact on homeostasis;
hemostasis and coagulation tests.
Facts checked against the Merck Manual Professional Edition, "Disseminated Intravascular Coagulation" (full review
Jul 2025, updated Sep 2026): tissue factor exposure (gram-negative sepsis, shock, obstetric, cancer, trauma);
thrombin/fibrin formation with fibrinolysis; consumption of platelets and factors causes bleeding; fibrin degradation
products inhibit platelets; microvascular thrombi cause organ dysfunction; schistocytes; acute DIC = bleeding from
puncture sites, ecchymoses at injection sites, GI bleeding; tests: platelets, PT, PTT, fibrinogen, D-dimer, smear;
treatment = correct the cause; platelets for <10-20 x 10^9/L or rapid fall with bleeding; cryoprecipitate for
fibrinogen <1.0 g/L (100 mg/dL) or falling rapidly; FFP; heparin usually not indicated in acute DIC with bleeding."""
from nurs1021_common import *

INTRO = ("The nurse in the intensive care unit is caring for Rosa, a 58-year-old female client admitted from the "
         "emergency department with septic shock from pyelonephritis.")
C = Chart2()
C.notes("nn", "Nurses' Notes",
    ("Day 1 0900", "Admitted to the ICU from the emergency department. Three days of fever, chills and right flank pain; "
     "right costovertebral angle tenderness. Blood and urine cultures drawn in the emergency department at 0640; IV "
     "piperacillin-tazobactam started at 0710; 2 L of IV crystalloid given. Norepinephrine infusing through a central "
     "line. Confused and restless, oriented to person only. Blood oozing from the left antecubital IV site and from two "
     "venipuncture sites despite pressure dressings. Petechiae across the chest; ecchymoses under the BP cuff on the right "
     "arm. Gums bleed when she is given mouth care. Fingertips of both hands cool, mottled and dusky. Pink-tinged urine "
     "in the catheter bag; 15 mL over the past hour."))
VS = [vrow("T"), vrow("P"), vrow("RR"), vrow("BP"), vrow("Mean arterial pressure (MAP)"), vrow(SPO2)]


def vitals(col, *v):
    C.column("vs", "Vital Signs", "", col, list(zip(VS, v)))


vitals("Day 1 0900", "39.4° C", "124 beats/min", "26 breaths/min", "88/50 mm Hg", "63 mm Hg", "93% on 4 L/min nasal cannula")
s1 = screen(1, INTRO, C, select_all(311, [
    ("A", "Blood oozing from the IV site and venipuncture sites", True),
    ("B", "Petechiae on the chest and ecchymoses under the BP cuff", True),
    ("C", "Gums that bleed during mouth care", True),
    ("D", "Pink-tinged urine in the catheter bag", True),
    ("E", "Cool, mottled, dusky fingertips", True),
    ("F", "Temperature of 39.4° C with chills", False),
    ("G", "Right flank pain with costovertebral angle tenderness", False),
    ("H", "Three days of symptoms before admission", False)],
    rationale(
        "<b>Consistent with DIC:</b> in acute DIC, platelets and clotting factors are used up faster than the body can "
        "replace them, so the client bleeds from many sites at once. Typical signs are persistent oozing from IV, arterial and "
        "venipuncture sites {A}, petechiae and bruising where pressure is applied {B}, bleeding gums {C} and hematuria {D}; "
        "gastrointestinal bleeding is also common. At the same time, tiny clots block small vessels: cool, mottled, dusky "
        "fingertips (acrocyanosis) reflect microvascular thrombosis, made worse by shock {E}.",
        "<b>Not DIC:</b> fever and chills are signs of the infection {F}, and flank pain with costovertebral angle "
        "tenderness points to pyelonephritis {G}. These describe the <b>cause</b> (gram-negative sepsis), not DIC itself. "
        "How long she was ill before admission does not describe a manifestation of DIC {H}."),
    stem="The nurse reviews the client's history and assessment. Which of the following findings would be consistent "
         "with <b>disseminated intravascular coagulation (DIC)</b>? Select all that apply."))

# Screen 2
C.notes("nn", "Nurses' Notes", ("Day 1 1000",
    "Laboratory results called to the ICU physician. Urine output 10 mL over the past hour. Daughter asks how an infection "
    "can make her mother bleed and form clots at the same time."))
LAB = [lab("Hemoglobin (Hgb)", "Female: 115–155 g/L"), lab("Platelet count", "130–380 × 10<sup>9</sup>/L"),
       lab("Prothrombin time (PT)", "10–14 s"), lab("International normalized ratio (INR)", "0.9–1.2"),
       lab("Activated partial thromboplastin time (aPTT)", "22–30 s"), lab("Fibrinogen", "2.0–4.0 g/L"),
       lab("D-dimer", "less than 600 µg/L"), "<b>Peripheral blood smear</b>", lab("Creatinine", "Female: 22–75 µmol/L"),
       lab("Lactate", "0.5–2.5 mmol/L"), lab("White blood cell (WBC) count", "3.5–10.5 × 10<sup>9</sup>/L")]
C.column("labs", "Laboratory Results", "Laboratory Test and Reference Range", "Day 1 0930", list(zip(LAB, [
    "94 g/L", "18 × 10<sup>9</sup>/L", "22 s", "1.9", "54 s", "0.8 g/L", "8,500 µg/L", "Schistocytes present",
    "212 µmol/L", "5.8 mmol/L", "19.6 × 10<sup>9</sup>/L"])))
s2 = screen(2, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 1 1000 and the Laboratory Results.",
    "stem": "For each finding, click to specify whether it is mainly the result of <b>clots forming in small blood "
            "vessels</b>, <b>consumption of platelets and clotting factors</b>, or <b>breakdown of fibrin "
            "(fibrinolysis)</b>.",
    "matrix": matrix_mc("Finding", ["Clots in Small Vessels", "Consumption of Platelets and Factors", "Fibrinolysis"], [
        ("Platelet count 18 × 10⁹/L", 1),
        ("Schistocytes on the blood smear", 0),
        ("D-dimer 8,500 µg/L", 2),
        ("Fibrinogen 0.8 g/L", 1),
        ("Cool, mottled, dusky fingertips", 0),
        ("PT 22 seconds and aPTT 54 seconds", 1)]),
    "explanation": rationale(
        "<b>How DIC develops:</b> bacterial endotoxin and tissue injury expose <b>tissue factor</b> to the blood. Clotting "
        "is switched on throughout the circulation instead of only at a wound, so thrombin forms fibrin clots in small "
        "vessels everywhere.",
        "<b>Clots in small vessels:</b> microthrombi block blood flow to the fingers (acrocyanosis), kidneys (falling urine "
        "output, rising creatinine), brain (confusion) and other organs, causing multi-organ dysfunction. Red cells forced "
        "through fibrin strands are cut into fragments, seen as <b>schistocytes</b>.",
        "<b>Consumption:</b> the widespread clotting uses up platelets, fibrinogen and other clotting factors. The platelet "
        "count and fibrinogen fall and the PT, INR and aPTT are prolonged, so the client bleeds.",
        "<b>Fibrinolysis:</b> the body breaks the clots down with plasmin. Breaking down cross-linked fibrin releases "
        "<b>D-dimer</b>, which is very high. Fibrin degradation products also interfere with platelet function, adding to "
        "the bleeding. Clotting and bleeding therefore happen at the same time, which answers the daughter's question."),
})

# Screen 3
C.notes("nn", "Nurses' Notes", ("Day 1 1030",
    "Oozing continues from all puncture sites. Small amount of bright red blood in the mouth after suctioning. Urine "
    "output 8 mL over the past half-hour. Remains confused. Physician at the bedside."))
vitals("Day 1 1030", "39.0° C", "128 beats/min", "28 breaths/min", "84/48 mm Hg", "60 mm Hg", "92% on 4 L/min nasal cannula")
s3 = screen(3, INTRO, C, {
    "type": "bowtie",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 1 1030 and the Vital Signs.",
    "stem": "Complete the diagram by dragging from the choices below to specify what condition the client is most likely "
            "experiencing, 2 actions the nurse should take to address that condition, and 2 parameters the nurse should "
            "monitor to assess the client's progress.",
    "bowtieConditions": bowtie_list(321, ["Disseminated intravascular coagulation"], [
        "Immune thrombocytopenia", "Thrombotic thrombocytopenic purpura", "Hemophilia A"]),
    "bowtieActions": bowtie_list(322, [
        "Give the prescribed antibiotic doses on time",
        "Give the prescribed platelets and cryoprecipitate"], [
        "Start a continuous heparin infusion",
        "Hold the antibiotics until the bleeding stops",
        "Give the prescribed vitamin K by IM injection"]),
    "bowtieParams": bowtie_list(3231, [
        "Platelet count and fibrinogen level",
        "Bleeding from puncture sites, mouth and urine"], [
        "Hemoglobin A1C",
        "Serum potassium",
        "Factor VIII inhibitor level"]),
    "explanation": rationale(
        "<b>Condition: DIC.</b> Low platelets with a prolonged PT and aPTT, low fibrinogen, a very high D-dimer and "
        "schistocytes in a client with gram-negative sepsis fit acute DIC. Immune thrombocytopenia lowers platelets but "
        "leaves the PT, aPTT and fibrinogen normal. Thrombotic thrombocytopenic purpura causes low platelets and "
        "schistocytes, but clotting factors are not consumed, so the PT, aPTT and fibrinogen are usually normal. Hemophilia "
        "A prolongs only the aPTT.",
        "<b>Actions:</b> the most important treatment of DIC is treating its cause, so antibiotics are given on time and "
        "without interruption (with fluids and vasopressors for shock). Because she is bleeding with platelets of "
        "18 × 10⁹/L and fibrinogen of 0.8 g/L, platelets and cryoprecipitate (which replaces fibrinogen) are given. Heparin "
        "is usually not used in acute DIC with bleeding; it is reserved for slowly developing DIC with thrombosis. "
        "Intramuscular injections cause hematomas and are avoided; vitamin K corrects vitamin K deficiency, not "
        "consumption.",
        "<b>Parameters:</b> serial platelet counts and fibrinogen show whether consumption is slowing, and bleeding sites "
        "show whether replacement is working. Hemoglobin A1C, potassium and factor VIII inhibitors do not track DIC."),
})

# Screen 4
C.notes("nn", "Nurses' Notes", ("Day 1 1100",
    "Physician orders received; 1 adult dose of platelets and 10 units of cryoprecipitate requested from the blood bank. "
    "The nurse plans care to protect Rosa from further bleeding."))
C.rows("orders", "Orders", ["Category", "Order"], [
    ["<b>Infection</b>", "Piperacillin-tazobactam 4.5 g IV every 6 hours."],
    ["<b>Circulation</b>", "Norepinephrine infusion titrated to MAP 65 mm Hg or higher. Lactated Ringer's 500 mL IV bolus now."],
    ["<b>Blood products</b>", "Platelets 1 adult dose IV now. Cryoprecipitate 10 units IV now."],
    ["<b>Monitoring</b>", "CBC, PT/INR, aPTT and fibrinogen every 6 hours. Hourly urine output."],
    ["<b>Precautions</b>", "Bleeding precautions. No intramuscular injections. Acetaminophen for fever; no aspirin or "
                           "NSAIDs."]])
s4 = screen(4, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 1 1100 and the Orders.",
    "stem": "For each nursing intervention, click to specify whether it is <b>indicated</b> or <b>contraindicated</b> "
            "for Rosa.",
    "matrix": matrix_mc("Nursing Intervention", ["Indicated", "Contraindicated"], [
        ("Measure the temperature by the rectal route for accuracy", 1),
        ("Hold firm pressure on puncture sites for at least 5 minutes", 0),
        ("Use foam swabs instead of a toothbrush for mouth care", 0),
        ("Give the prescribed opioid for pain by intramuscular injection", 1),
        ("Turn and reposition Rosa gently using a lift sheet", 0),
        ("Check stool, urine and gastric secretions for blood", 0)]),
    "explanation": rationale(
        "<b>Indicated:</b> prolonged firm pressure lets a clot form at puncture sites despite low platelets. Foam swabs "
        "avoid injuring bleeding gums. Gentle turning with a lift sheet avoids friction and shearing that cause bruising "
        "and bleeding. Checking stool, urine and gastric contents detects hidden (occult) bleeding early.",
        "<b>Contraindicated:</b> a rectal thermometer can injure the rectal mucosa and cause bleeding; oral, tympanic or "
        "temporal routes are used. Intramuscular injections cause hematomas in a client with low platelets and clotting "
        "factors; medications are given IV or by mouth."),
})

# Screen 5
C.notes("nn", "Nurses' Notes", ("Day 1 1150",
    "Platelets ready in the blood bank. Informed consent for blood products signed by Rosa's daughter as substitute "
    "decision-maker. Blood administration set primed with 0.9% sodium chloride."))
s5 = screen(5, INTRO, C, {
    "type": "ordered_response",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 1 1150.",
    "stem": "The nurse prepares to give the platelets. Place the nurse's actions in the order in which they should be "
            "performed.",
    "options": [],
    "orderedOptions": [
        "Confirm the prescription and that informed consent is documented",
        "Take baseline vital signs, including temperature",
        "Pick up the platelets from the blood bank",
        "Check the client's identity and the product label at the bedside with a second qualified person",
        "Start the platelets slowly and stay with the client for the first 15 minutes"],
    "explanation": rationale(
        "<b>Order:</b> (1) The prescription and consent are confirmed before any product is requested, so that nothing is "
        "issued that cannot be given. (2) Baseline vital signs are taken before the product arrives; any change during the "
        "transfusion is compared with them (a fever already present, as here, must be documented). (3) The product is then "
        "picked up; platelets are kept at room temperature and never refrigerated. (4) At the bedside, two qualified people "
        "match the client's identity (two identifiers) and the product label against the prescription. (5) The infusion "
        "starts slowly through a blood administration set primed with 0.9% sodium chloride, and the nurse stays with the "
        "client for the first 15 minutes, when severe reactions usually appear, then rechecks vital signs.",
        "Platelets are given within 4 hours of leaving the blood bank. Nothing else is added to the blood line."),
})

# Screen 6
C.notes("nn", "Nurses' Notes",
    ("Day 1 1300", "Platelets and cryoprecipitate given without reaction."),
    ("Day 3 0800", "Alert and oriented × 3. Norepinephrine stopped at 0200. Blood cultures growing Escherichia coli "
     "sensitive to the current antibiotic. No oozing from puncture sites; gums no longer bleeding; urine yellow. Fingertips "
     "warm and pink. New petechiae noted on both lower legs. Urine output 45 to 60 mL/hour over the past 12 hours."))
vitals("Day 3 0800", "37.6° C", "96 beats/min", "20 breaths/min", "112/66 mm Hg", "81 mm Hg", "96% on room air")
C.column("labs", "Laboratory Results", "Laboratory Test and Reference Range", "Day 3 0600", list(zip(LAB, [
    "86 g/L", "46 × 10<sup>9</sup>/L", "15 s", "1.3", "36 s", "1.6 g/L", "3,200 µg/L", "Occasional schistocytes",
    "118 µmol/L", "1.8 mmol/L", "12.4 × 10<sup>9</sup>/L"])))
s6 = screen(6, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 1 1300 and Day 3 0800, the Vital Signs, and the "
                "Laboratory Results.",
    "stem": "For each finding, click to specify whether Rosa's condition has <b>improved</b> or <b>not improved</b> "
            "since Day 1.",
    "matrix": matrix_mc("Finding", ["Improved", "Not Improved"], [
        ("Fibrinogen", 0),
        ("Hemoglobin", 1),
        ("Urine output", 0),
        ("Skin of the lower legs", 1),
        ("Platelet count", 0),
        ("Mental status", 0)]),
    "explanation": rationale(
        "<b>Improved:</b> with the infection treated, consumption is slowing: fibrinogen rose from 0.8 to 1.6 g/L, platelets "
        "from 18 to 46 × 10⁹/L, and the PT, aPTT and D-dimer are falling. Better perfusion and fewer microthrombi show in a "
        "urine output of 45 to 60 mL/hour (creatinine 212 to 118 µmol/L), warm fingertips and a clear mind (alert and "
        "oriented, lactate 1.8 mmol/L).",
        "<b>Not improved:</b> hemoglobin fell further, from 94 to 86 g/L, from blood lost through bleeding and hemolysis; "
        "it is followed and red cells are given if prescribed. New petechiae on the legs show that the platelet count is "
        "still low enough for small-vessel bleeding, so bleeding precautions continue until it recovers."),
})
write_case(1, 3,
    "58-year-old female in septic shock from pyelonephritis who develops acute disseminated intravascular coagulation: "
    "manifestations, pathogenesis (clotting, consumption, fibrinolysis), coagulation tests, bleeding precautions and "
    "blood product administration.",
    [s1, s2, s3, s4, s5, s6],
    "New case written by Claude on 24 Nov 2026 (NURS 1021 Unit 1, batch 1); checked against Merck Manual Professional "
    "(DIC, Jul 2025). Please review: fibrinogen reference range (2.0–4.0 g/L, not in the MCC list); transfusion steps "
    "against your hospital's blood administration policy (order of baseline vital signs and product pickup; 15 minutes "
    "with the client); platelet and cryoprecipitate doses as Canadian adult doses.")
