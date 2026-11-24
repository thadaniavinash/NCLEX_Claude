"""NURS 1021 Unit 1 Case Study 8: transfusion-dependent beta-thalassemia major in a young adult with cardiac iron
overload (heart failure) after poor adherence to chelation; thalassemia major versus trait.
Outcomes: etiology, pathogenesis and clinical manifestations of thalassemia.
Facts checked against the Merck Manual Professional Edition, "Thalassemias" (full review Apr 2026): reduced globin
chain synthesis (unbalanced chains -> ineffective erythropoiesis and hemolysis); beta = chromosome 11, alpha =
chromosome 16; Mediterranean, Middle Eastern, South and Southeast Asian ancestry; minor (trait) = mild microcytic
anemia, no treatment; major (Cooley) = severe anemia by age 1-2, jaundice, gallstones, splenomegaly, thickened skull
and malar bones, pathologic fractures, delayed growth and puberty; iron overload from transfusion and absorption
causes heart failure and liver cirrhosis; smear: target cells, nucleated red cells; HbA2 > 3.5% in trait, HbF up to
90% in major; transfuse to keep Hb about 90-100 g/L; chelate when ferritin > 1000 µg/L or after 1-2 years of
transfusion; splenectomy; HSCT and gene therapy are potentially curative.
Chelator specifics (deferoxamine, deferiprone with weekly ANC, deferasirox), cardiac T2* MRI and post-splenectomy
precautions are from standard references (TIF guidelines, product monographs), not the Merck page: flagged."""
from nurs1021_common import *

INTRO = ("The nurse in a hematology day unit is caring for Priya, a 24-year-old female client with beta-thalassemia "
         "major who has come for her scheduled red blood cell transfusion.")
C = Chart2()
C.notes("nn", "Nurses' Notes", ("Day 1 0830",
    "Transfused every 3 to 4 weeks since age 1; splenectomy at age 12. Says she stopped taking her deferasirox tablets "
    "about 8 months ago because of stomach upset. Reports increasing tiredness and, over the past 2 weeks, shortness of "
    "breath climbing one flight of stairs, needing two pillows to sleep, and her heart “racing and skipping.” Height "
    "152 cm. Prominent cheekbones and forehead. Skin has a grey-bronze tint; sclerae slightly yellow. Pulse irregular. "
    "Fine crackles at both lung bases. 2+ pitting edema of both ankles. Abdomen: liver edge 4 cm below the right costal "
    "margin; well-healed splenectomy scar."))
VS = [vrow("T"), vrow("P"), vrow("RR"), vrow("BP"), vrow(SPO2)]


def vitals(col, *v):
    C.column("vs", "Vital Signs", "", col, list(zip(VS, v)))


vitals("Day 1 0830", "36.9° C", "112 beats/min, irregular", "22 breaths/min", "104/66 mm Hg", "94% on room air")
s1 = screen(1, INTRO, C, select_all(811, [
    ("A", "Shortness of breath on one flight of stairs and needing two pillows to sleep", True),
    ("B", "Irregular pulse of 112 beats/min with a “racing and skipping” heart", True),
    ("C", "Fine crackles at both lung bases and 2+ ankle edema", True),
    ("D", "Stopped taking her deferasirox 8 months ago", True),
    ("E", "Grey-bronze skin and a liver edge 4 cm below the costal margin", True),
    ("F", "Prominent cheekbones and forehead", False),
    ("G", "Height of 152 cm", False),
    ("H", "Well-healed splenectomy scar", False)],
    rationale(
        "<b>Require follow-up:</b> each unit of red cells adds about 200 mg of iron, which the body cannot excrete, and "
        "thalassemia also increases iron absorption from the gut. Without chelation {D}, iron builds up in the heart, "
        "liver and endocrine glands. Iron in heart muscle causes cardiomyopathy: dyspnea on exertion and orthopnea {A}, "
        "arrhythmias {B}, and crackles and edema from heart failure {C}. Heart failure is the leading cause of death in "
        "thalassemia major. Bronze skin and an enlarged liver reflect iron deposited in skin and liver (hepatic "
        "siderosis), which can progress to cirrhosis {E}.",
        "<b>Long-standing, not new:</b> marrow expansion to compensate for ineffective erythropoiesis thickens the facial "
        "and skull bones in childhood {F}, and severe anemia with iron overload of the pituitary and gonads limits growth "
        "and puberty {G}. Her spleen was removed because enlarged spleens trap and destroy transfused cells {H}. These "
        "need no urgent action, although her asplenia raises her risk of severe infection."),
    stem="The nurse reviews the client's history and assessment. Which findings require follow-up? Select all that "
         "apply."))

# Screen 2
C.notes("nn", "Nurses' Notes", ("Day 1 1000",
    "Results reviewed with the hematologist. Echocardiogram and cardiac MRI booked for this afternoon. Priya's partner "
    "asks whether their future children could have thalassemia; he was told years ago that he has “thalassemia trait.”"))
LAB = [lab("Hemoglobin (Hgb)", "Female: 115–155 g/L"), lab("Mean corpuscular volume (MCV)", "80–100 fL"),
       "<b>Peripheral blood smear</b>", lab("Ferritin", "Female: 11–307 µg/L"),
       lab("Alanine aminotransferase (ALT)", "17–63 IU/L"), lab("Bilirubin, total", "3–17 µmol/L"),
       lab("Creatinine", "Female: 22–75 µmol/L"), lab("Neutrophils, absolute", "2.0–7.5 × 10<sup>9</sup>/L"),
       lab("Brain-type natriuretic peptide (BNP)", "≤ 50 pg/mL")]
C.column("labs", "Laboratory Results", "Laboratory Test and Reference Range", "Day 1 0845", list(zip(LAB, [
    "78 g/L", "71 fL", "Small, pale red cells; target cells; nucleated red cells; Howell-Jolly bodies", "2,840 µg/L",
    "88 IU/L", "41 µmol/L", "62 µmol/L", "4.2 × 10<sup>9</sup>/L", "640 pg/mL"])))
s2 = screen(2, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 1 1000 and the Laboratory Results.",
    "stem": "The nurse answers the partner's question. For each statement, click to specify whether it describes "
            "<b>beta-thalassemia major</b>, <b>beta-thalassemia trait (minor)</b>, or <b>both</b>.",
    "matrix": matrix_mc("Statement", ["Beta-Thalassemia Major", "Beta-Thalassemia Trait", "Both"], [
        ("Two altered beta-globin genes, one inherited from each parent", 0),
        ("Small (microcytic) red blood cells", 2),
        ("Usually no symptoms and no treatment needed", 1),
        ("Severe anemia by age 1 to 2 years, needing regular transfusions", 0),
        ("One altered beta-globin gene; the other is normal", 1),
        ("Marrow expansion that thickens the skull and facial bones", 0)]),
    "explanation": rationale(
        "<b>Pathogenesis:</b> beta-thalassemia is an inherited defect in making beta-globin chains (gene on chromosome "
        "11). With too few beta chains, excess alpha chains have no partner; they precipitate inside red cell precursors, "
        "which die in the marrow (ineffective erythropoiesis) or are destroyed in the spleen (hemolysis). Cells that "
        "survive are small and pale with target cells; nucleated red cells appear in the blood. It is common in people of "
        "Mediterranean, Middle Eastern, South Asian and Southeast Asian ancestry.",
        "<b>Major:</b> both beta genes are affected (autosomal recessive), so beta-chain production is very low. Severe "
        "anemia appears once fetal hemoglobin falls, by age 1 to 2; without transfusion, the marrow expands (thick skull "
        "and malar bones, fractures), the spleen enlarges and growth fails. HbF may be up to 90%.",
        "<b>Trait (minor):</b> one gene is affected; there is mild microcytic anemia, usually without symptoms, and no "
        "treatment. HbA2 above 3.5% to 4% on electrophoresis is diagnostic; it is often mistaken for iron deficiency.",
        "<b>Both</b> make small cells. If the partner has beta-thalassemia trait, each pregnancy has a 50% chance of a child "
        "with thalassemia major (Priya passes one affected gene to every child) and a 50% chance of a child with trait; "
        "genetic counselling is offered."),
})

# Screen 3
C.notes("nn", "Nurses' Notes", ("Day 1 1530",
    "Cardiac MRI shows severe myocardial iron loading (T2* 7 ms; severe if below 10 ms); echocardiogram shows a left "
    "ventricular ejection fraction of 45%. Hematologist plans admission for intensified chelation and a slower "
    "transfusion."))
s3 = screen(3, INTRO, C, {
    "type": "dropdown_cloze",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 1 1530.",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {"text": "Priya's red cells are small because [[drop0]]. Her body has accumulated iron mainly because "
                      "[[drop1]]. The nurse's priority is [[drop2]].",
              "dropdowns": [
                  dd(831, "too few beta-globin chains are made, so cells contain too little hemoglobin",
                     "she lacks iron to make heme", "her red cells are destroyed by antibodies",
                     "she lacks vitamin B12 to make DNA"),
                  dd(832, "every transfusion adds iron that the body cannot excrete",
                     "she eats a diet high in red meat",
                     "her kidneys cannot excrete iron",
                     "her spleen was removed"),
                  dd(833, "heart failure and arrhythmias from iron in the heart muscle",
                     "liver damage from iron deposits",
                     "infection after splenectomy",
                     "body image concerns about her bones")]},
    "explanation": rationale(
        "<b>Small cells:</b> hemoglobin is built from globin chains plus heme; with too few beta chains, each cell holds "
        "less hemoglobin, so cells are microcytic and hypochromic even though iron is plentiful (ferritin 2,840 µg/L). "
        "Giving iron would be harmful.",
        "<b>Iron overload:</b> about 200 mg of iron enters with every unit transfused, and humans have no way to excrete "
        "extra iron; ineffective erythropoiesis also increases absorption from the gut. Chelation is started once ferritin "
        "exceeds about 1,000 µg/L or after 1 to 2 years of transfusions, and must be taken continuously.",
        "<b>Priority:</b> severe cardiac iron (T2* 7 ms), a falling ejection fraction, crackles, edema and an irregular "
        "pulse put her at risk of fatal heart failure and arrhythmias. Liver iron, infection risk and body image matter, "
        "but the threat to her circulation comes first."),
})

# Screen 4
C.notes("nn", "Nurses' Notes", ("Day 1 1700", "Admitted to the medical unit. Implanted port accessed. Orders received."))
C.rows("orders", "Orders", ["Category", "Order"], [
    ["<b>Transfusion</b>", "2 units of leukoreduced, phenotype-matched red blood cells, each over 3 to 4 hours. Furosemide "
                           "20 mg IV between units. Pre-transfusion hemoglobin goal 95–105 g/L."],
    ["<b>Chelation</b>", "Deferoxamine 50 mg/kg/day by continuous IV infusion through the port. Deferiprone 25 mg/kg PO "
                         "three times a day. Absolute neutrophil count weekly."],
    ["<b>Cardiac</b>", "Continuous cardiac monitoring. Daily weight. Fluid intake 1.5 L/day."]])
s4 = screen(4, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 1 1700 and the Orders.",
    "stem": "For each nursing action, click to specify whether the action is <b>Indicated</b>, <b>Non-Essential</b>, or "
            "<b>Contraindicated</b>.",
    "matrix": matrix_mc("Nursing Action", IMC, [
        ("Infuse each unit over 3 to 4 hours and give the furosemide between units", 0),
        ("Give oral ferrous sulfate to help her make more hemoglobin", 2),
        ("Tell Priya that her urine may turn orange-red during the deferoxamine infusion", 0),
        ("Give the deferoxamine as a rapid IV bolus to remove iron faster", 2),
        ("Request a hemoglobin electrophoresis before each transfusion", 1),
        ("Check the absolute neutrophil count every week while she takes deferiprone", 0)]),
    "explanation": rationale(
        "<b>Indicated:</b> with heart failure, red cells are given slowly with a diuretic between units to prevent fluid "
        "overload. Deferoxamine binds iron to form ferrioxamine, excreted in urine and bile, which turns urine orange-red: "
        "an expected, harmless effect. Deferiprone can cause agranulocytosis, so the neutrophil count is checked every "
        "week and fever or sore throat is reported at once.",
        "<b>Contraindicated:</b> she has iron overload; iron supplements add to the damage. Rapid IV deferoxamine causes "
        "flushing, hypotension and shock; it is given by slow continuous infusion.",
        "<b>Non-Essential:</b> her diagnosis is established; electrophoresis does not change before each transfusion. A "
        "type and screen (crossmatch) is what each transfusion needs."),
})

# Screen 5
C.notes("nn", "Nurses' Notes", ("Day 6 1000",
    "Breathing easier; sleeps flat; ankle edema 1+. Pulse regular. Will go home on deferiprone three times a day and "
    "deferoxamine by subcutaneous pump overnight 5 nights a week. Priya says she wants to “do it properly this time.”"))
vitals("Day 6 1000", "36.7° C", "88 beats/min, regular", "18 breaths/min", "112/70 mm Hg", "97% on room air")
s5 = screen(5, INTRO, C, select_all(8512, [
    ("A", "Go to the emergency department for a fever or sore throat, even if you feel well otherwise", True),
    ("B", "Have your neutrophil count checked every week", True),
    ("C", "Report any change in your hearing or vision", True),
    ("D", "Do not take iron supplements or multivitamins that contain iron", True),
    ("E", "Carry information that you have no spleen and keep your vaccines up to date", True),
    ("F", "Take a vitamin C 1,000 mg tablet each day to boost your energy", False),
    ("G", "You can stop the chelation once your transfusions are spaced further apart", False),
    ("H", "Skip deferiprone on the nights you use the deferoxamine pump", False)],
    rationale(
        "<b>Include:</b> deferiprone can cause agranulocytosis, and without a spleen she is at risk of overwhelming "
        "infection with encapsulated bacteria; fever or sore throat needs urgent assessment and a neutrophil count {A,B}. "
        "Deferoxamine can damage hearing and vision (ototoxicity, retinopathy), so these are checked yearly and changes "
        "reported {C}. Extra iron worsens overload {D}. After splenectomy, pneumococcal, meningococcal and Haemophilus "
        "vaccines and medical identification are recommended {E}.",
        "<b>Do not include:</b> vitamin C increases iron absorption and, in iron overload, can increase iron toxicity to "
        "the heart; it is taken only if the hematologist prescribes it with deferoxamine {F}. Iron keeps accumulating as "
        "long as transfusions continue, so chelation is lifelong {G}. The two chelators are prescribed together for heavy "
        "cardiac iron; skipping one reduces iron removal {H}."),
    preamble="The nurse has reviewed the Nurses' Notes from Day 6 1000 and the Vital Signs.",
    stem="Which instructions should the nurse include in Priya's discharge teaching? Select all that apply."))

# Screen 6
C.notes("nn", "Nurses' Notes", ("Month 6 1000",
    "Clinic visit. Takes deferiprone daily and uses the pump 5 nights a week; no missed doses. Walks 30 minutes without "
    "breathlessness. No ankle edema. Repeat cardiac MRI: T2* 11 ms. Reports a sore throat since yesterday; no fever."))
vitals("Month 6 1000", "37.3° C", "82 beats/min, regular", "16 breaths/min", "114/72 mm Hg", "98% on room air")
C.column("labs", "Laboratory Results", "Laboratory Test and Reference Range", "Month 6 0900", list(zip(
    [LAB[0], LAB[3], LAB[4], LAB[7], LAB[8]],
    ["98 g/L", "1,640 µg/L", "52 IU/L", "0.8 × 10<sup>9</sup>/L", "42 pg/mL"])))
s6 = screen(6, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Month 6 1000, the Vital Signs, and the Laboratory Results.",
    "stem": "For each finding, click to specify whether it shows that Priya's condition has <b>improved</b> or "
            "<b>not improved</b> since admission.",
    "matrix": matrix_mc("Finding", ["Improved", "Not Improved"], [
        ("Ferritin", 0),
        ("Absolute neutrophil count", 1),
        ("Cardiac MRI T2*", 0),
        ("Ankle edema", 0),
        ("Pre-transfusion hemoglobin", 0),
        ("BNP", 0)]),
    "explanation": rationale(
        "<b>Improved:</b> ferritin fell from 2,840 to 1,640 µg/L and cardiac T2* rose from 7 to 11 ms (above 10 ms, less "
        "severe), showing iron is leaving the heart; BNP has normalized and edema has resolved as heart failure improved. "
        "Pre-transfusion hemoglobin is now within the 95 to 105 g/L goal, which also suppresses the marrow expansion that "
        "drives extra iron absorption.",
        "<b>Not improved:</b> a neutrophil count of 0.8 × 10⁹/L (below 1.0, severe below 0.5) with a sore throat in a "
        "client on deferiprone without a spleen needs urgent action: the nurse notifies the hematologist at once; "
        "deferiprone is usually held and the client is assessed for infection."),
})
write_case(1, 8,
    "24-year-old female with transfusion-dependent beta-thalassemia major and cardiac iron overload after stopping "
    "chelation: pathogenesis, thalassemia major versus trait, transfusion with heart failure, deferoxamine and deferiprone.",
    [s1, s2, s3, s4, s5, s6],
    "New case written by Claude on 25 Nov 2026 (NURS 1021 Unit 1, batch 3); checked against Merck Manual Professional "
    "(Thalassemias, Apr 2026). Please review (from standard references, not the Merck page): chelation regimen "
    "(deferoxamine IV/SC, deferiprone 25 mg/kg three times a day with weekly ANC); cardiac T2* thresholds (< 10 ms severe); "
    "pre-transfusion Hb goal 95–105 g/L (TIF; Merck says about 90–100 g/L); vitamin C advice; BNP (pg/mL, as MCC "
    "prints it).")
