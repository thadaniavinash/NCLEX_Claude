"""NURS 1021 Unit 1 Case Study 9: adult sickle cell anemia (HbSS): vaso-occlusive crisis with priapism, then acute
chest syndrome, opioid oversedation, hydroxyurea teaching.
Outcomes: etiology, pathogenesis and clinical manifestations of sickle cell anemia.
Facts checked against the Merck Manual Professional Edition, "Sickle Cell Disease" (full review Apr 2026): HbS (valine
for glutamic acid at beta-6) polymerizes when deoxygenated; rigid cells occlude vessels and hemolyse; triggers include
infection, fever, dehydration, hypoxia; adult spleen atrophied (functional asplenia, pneumococcal risk); crises:
vaso-occlusive (most common), acute chest syndrome (fever, chest pain, new infiltrate; a common cause of death),
aplastic (parvovirus B19, reticulocytes < 1%), sequestration, priapism; reticulocytes often >= 10%, bilirubin 34-68
µmol/L; liberal opioid analgesia, meperidine with caution, oxygen if hypoxic, antibiotics immediately for suspected
infection or ACS, exchange transfusion for ACS/stroke, transfusion not helpful in uncomplicated pain crisis;
hydroxyurea raises HbF, reduces crises ~45%, causes neutropenia/thrombocytopenia; folic acid 1 mg daily; vaccines.
Incentive spirometry, avoiding overhydration and naloxone for opioid oversedation are standard nursing practice."""
from nurs1021_common import *

INTRO = ("The nurse in the emergency department is caring for Jordan, a 26-year-old male client with sickle cell "
         "anemia (HbSS).")
C = Chart2()
C.notes("nn", "Nurses' Notes", ("Day 1 0700",
    "Spent yesterday skiing; drank little and has vomited twice since midnight. Severe, throbbing pain in his lower back "
    "and both thighs since 0300, rated 9/10; took two tablets of hydromorphone at home without relief. Also reports a "
    "painful erection that began at 0400 and has not gone away. Says this pain “feels like my usual crises.” Sclerae "
    "slightly yellow, which he says is normal for him. Mucous membranes dry. Lungs clear; no chest pain. Spleen not "
    "palpable. Takes folic acid 1 mg daily; stopped hydroxyurea a year ago."))
VS = [vrow("T"), vrow("P"), vrow("RR"), vrow("BP"), vrow(SPO2), vrow("Pain (0–10)")]


def vitals(col, *v):
    C.column("vs", "Vital Signs", "", col, list(zip(VS, v)))


vitals("Day 1 0700", "37.6° C", "116 beats/min", "20 breaths/min", "128/76 mm Hg", "97% on room air", "9")
s1 = screen(1, INTRO, C, select_all(911, [
    ("A", "Lower back and thigh pain rated 9/10, unrelieved by hydromorphone", True),
    ("B", "Painful erection for 3 hours", True),
    ("C", "Vomiting with dry mucous membranes after drinking little while skiing", True),
    ("D", "Heart rate of 116 beats/min", True),
    ("E", "Slightly yellow sclerae, normal for him", False),
    ("F", "Spleen not palpable", False),
    ("G", "SpO₂ 97% on room air with clear lungs", False)],
    rationale(
        "<b>Require follow-up:</b> when HbS gives up oxygen it polymerizes; red cells become rigid and sickled, stick to "
        "the endothelium and block small vessels, causing ischemic pain in bones, back and joints: a "
        "<b>vaso-occlusive crisis</b>, the most common crisis {A}. It needs rapid, generous analgesia, usually IV opioids. "
        "<b>Priapism</b> is vaso-occlusion in the penis; an erection lasting hours is an emergency that can cause permanent "
        "erectile dysfunction, so it is reported at once {B}. Dehydration (vomiting, little fluid, cold and altitude) "
        "concentrates the blood and triggers sickling {C}. Tachycardia reflects pain, dehydration and anemia {D}.",
        "<b>Expected:</b> mild jaundice from ongoing hemolysis is usual for him {E}. In adults with HbSS the spleen has "
        "shrunk from repeated infarctions (functional asplenia), so it is not palpable; this is also why fever is "
        "dangerous {F}. Normal SpO₂ and clear lungs show no sign of acute chest syndrome yet, but they are rechecked "
        "regularly {G}."),
    stem="The nurse reviews the client's history and assessment. Which findings require follow-up? Select all that "
         "apply."))

# Screen 2
C.notes("nn", "Nurses' Notes", ("Day 1 0800",
    "Hydromorphone IV given at 0720 (within 30 minutes of arrival); pain 6/10. Urology aspirated the penis at 0745; "
    "erection resolved. Admitted to the medical unit. Jordan asks how this crisis differs from the time he had "
    "“parvovirus and needed blood” and from when his friend with sickle cell had “a chest crisis.”"))
LAB = [lab("Hemoglobin (Hgb)", "Male: 125–170 g/L"), lab("Reticulocyte percentage", "0.5%–1.5%"),
       lab("White blood cell (WBC) count", "3.5–10.5 × 10<sup>9</sup>/L"), lab("Platelet count", "130–380 × 10<sup>9</sup>/L"),
       lab("Bilirubin, total", "3–17 µmol/L"), lab("Lactate dehydrogenase (LDH)", "100–205 IU/L"),
       lab("Creatinine", "Male: 49–93 µmol/L"), "<b>Chest X-ray</b>"]
C.column("labs", "Laboratory Results", "Laboratory Test and Reference Range", "Day 1 0715", list(zip(LAB, [
    "74 g/L (his usual: 82 g/L)", "11.2%", "13.8 × 10<sup>9</sup>/L", "412 × 10<sup>9</sup>/L", "58 µmol/L", "520 IU/L",
    "64 µmol/L", "Clear lungs; no infiltrate"])))
s2 = screen(2, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 1 0800 and the Laboratory Results.",
    "stem": "For each finding, click to specify whether it is most consistent with a <b>vaso-occlusive crisis</b>, "
            "<b>acute chest syndrome</b>, or an <b>aplastic crisis</b>.",
    "matrix": matrix_mc("Finding", ["Vaso-Occlusive Crisis", "Acute Chest Syndrome", "Aplastic Crisis"], [
        ("Fever, chest pain and a new infiltrate on chest X-ray", 1),
        ("Severe pain in the long bones and back with a normal chest X-ray", 0),
        ("Reticulocytes below 1% with hemoglobin well below the usual level", 2),
        ("Falling SpO₂ with crackles and a rising respiratory rate", 1),
        ("Recent parvovirus B19 infection", 2),
        ("Reticulocytes about 11% with hemoglobin slightly below the usual level", 0)]),
    "explanation": rationale(
        "<b>Vaso-occlusive crisis (Jordan now):</b> ischemic pain from blocked small vessels, often in bones, back and "
        "joints, with a clear chest X-ray. Ongoing hemolysis keeps the reticulocyte count high (about 11%), bilirubin and "
        "LDH raised, and hemoglobin near his usual level. The white cell count often rises without infection.",
        "<b>Acute chest syndrome:</b> sickling in the lung vessels (often with infection or fat embolism) causes fever, "
        "chest pain, cough, tachypnea, crackles, falling SpO₂ and a <b>new pulmonary infiltrate</b>. It is a leading "
        "cause of death and often develops 1 to 3 days into a pain crisis.",
        "<b>Aplastic crisis:</b> parvovirus B19 infects red cell precursors and stops red cell production for about a "
        "week. Because sickle cells survive only 10 to 20 days, hemoglobin falls fast, and reticulocytes drop below 1%. It "
        "often needs transfusion."),
})

# Screen 3
C.notes("nn", "Nurses' Notes", ("Day 2 1400",
    "New sharp right-sided chest pain worse on deep breathing, and a cough. Crackles at the right lung base. Using the "
    "PCA pump frequently. Has not used his incentive spirometer since the morning. Chest X-ray: new right lower lobe "
    "infiltrate."))
vitals("Day 2 1400", "38.8° C", "124 beats/min", "28 breaths/min", "118/70 mm Hg", "89% on room air", "8 (chest)")
C.column("labs", "Laboratory Results", "Laboratory Test and Reference Range", "Day 2 1415", list(zip(
    [LAB[0], LAB[1], LAB[2], LAB[3], LAB[7]],
    ["63 g/L", "9.8%", "18.4 × 10<sup>9</sup>/L", "190 × 10<sup>9</sup>/L", "New right lower lobe infiltrate"])))
s3 = screen(3, INTRO, C, {
    "type": "bowtie",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 2 1400, the Vital Signs, and the Laboratory Results.",
    "stem": "Complete the diagram by dragging from the choices below to specify what condition the client is most likely "
            "experiencing, 2 actions the nurse should take to address that condition, and 2 parameters the nurse should "
            "monitor to assess the client's progress.",
    "bowtieConditions": bowtie_list(931, ["Acute chest syndrome"], [
        "Aplastic crisis", "Splenic sequestration", "Uncomplicated vaso-occlusive crisis"]),
    "bowtieActions": bowtie_list(932, [
        "Give oxygen to keep SpO₂ at 95% or higher",
        "Give the prescribed IV antibiotics without delay"], [
        "Give meperidine for the chest pain",
        "Give a 2 L IV fluid bolus to flush the lungs",
        "Keep him flat in bed to reduce oxygen demand"]),
    "bowtieParams": bowtie_list(933, ["Oxygen saturation and respiratory rate", "Hemoglobin level"], [
        "Serum amylase", "INR", "Blood glucose"]),
    "explanation": rationale(
        "<b>Condition:</b> fever, chest pain, cough, tachypnea, hypoxemia (89%) and a new infiltrate during a pain crisis "
        "define acute chest syndrome. Reticulocytes remain high (not aplastic crisis), and the spleen in an adult with HbSS "
        "is atrophied (sequestration is mainly a childhood crisis).",
        "<b>Actions:</b> hypoxemia increases sickling, so oxygen is given; broad-spectrum antibiotics are started at once "
        "because infection often triggers or complicates the syndrome. Hematology is called for transfusion (often "
        "exchange transfusion to lower the HbS percentage). Meperidine's metabolite can cause seizures; large fluid boluses "
        "can cause pulmonary edema and worsen the syndrome; lying flat worsens atelectasis: he sits upright and uses the "
        "incentive spirometer.",
        "<b>Parameters:</b> SpO₂ and respiratory rate show whether lung involvement is improving; hemoglobin, which has "
        "fallen from 74 to 63 g/L, guides transfusion."),
})

# Screen 4
C.notes("nn", "Nurses' Notes", ("Day 2 1500",
    "Hematology at the bedside: exchange transfusion planned tonight. Consent signed. Orders received."))
C.rows("orders", "Orders", ["Category", "Order"], [
    ["<b>Breathing</b>", "Oxygen to keep SpO<sub>2</sub> 95% or higher. Incentive spirometry 10 breaths every 2 hours while "
                         "awake."],
    ["<b>Infection</b>", "Ceftriaxone 1 g IV every 24 hours and azithromycin 500 mg IV every 24 hours."],
    ["<b>Transfusion</b>", "Red cell exchange transfusion tonight; leukoreduced, sickle-negative, phenotype-matched red "
                           "cells."],
    ["<b>Pain</b>", "Hydromorphone PCA: 0.2 mg per dose, 10-minute lockout, no basal rate. Sedation score and RR every "
                    "hour."],
    ["<b>Fluids</b>", "0.45% NaCl IV at 100 mL/h. Strict intake and output."]])
s4 = screen(4, INTRO, C, select_all(941, [
    ("A", "Coach incentive spirometry every 2 hours while he is awake", True),
    ("B", "Assess sedation and respiratory rate every hour while he uses the PCA", True),
    ("C", "Keep him sitting upright and help him walk as tolerated", True),
    ("D", "Run the IV fluid at the ordered rate and monitor intake, output and lung sounds", True),
    ("E", "Check that the red cells for the exchange are leukoreduced and phenotype-matched", True),
    ("F", "Apply cool cloths and a fan to bring his temperature down", False),
    ("G", "Encourage him to push the PCA button before every breath to stay pain-free", False),
    ("H", "Increase the IV rate to 250 mL/h to reverse sickling faster", False)],
    rationale(
        "<b>Include:</b> incentive spirometry and sitting upright expand the lung bases and reduce atelectasis, which "
        "worsens acute chest syndrome {A,C}. Opioids are needed for chest and bone pain, but sedation comes before "
        "respiratory depression, which would worsen hypoxemia {B}. Fluids maintain hydration without overload, which can "
        "cause pulmonary edema {D}. Clients with sickle cell disease receive many transfusions and often form antibodies "
        "against red cell antigens; phenotype-matched, leukoreduced, sickle-negative cells reduce reactions {E}.",
        "<b>Do not include:</b> cold causes vasoconstriction and sickling; fever is treated with acetaminophen {F}. Only "
        "the client presses the PCA button, when he needs it; pressing it constantly risks oversedation {G}. Overhydration "
        "can trigger pulmonary edema and worsen acute chest syndrome {H}."),
    preamble="The nurse has reviewed the Nurses' Notes from Day 2 1500 and the Orders.",
    stem="Which interventions should the nurse include in Jordan's plan of care? Select all that apply."))

# Screen 5
C.notes("nn", "Nurses' Notes", ("Day 3 0300",
    "Exchange transfusion completed at 2300. At 0300 Jordan is difficult to rouse; falls asleep mid-sentence. "
    "Respirations shallow. His mother says she has been pressing the PCA button “so he won't wake up in pain.”"))
vitals("Day 3 0300", "37.4° C", "84 beats/min", "8 breaths/min", "108/66 mm Hg", "86% on 4 L/min nasal cannula",
       "unable to rate")
s5 = screen(5, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 3 0300 and the Vital Signs.",
    "stem": "For each nursing action, click to specify whether the action is <b>Indicated</b>, <b>Non-Essential</b>, or "
            "<b>Contraindicated</b>.",
    "matrix": matrix_mc("Nursing Action", IMC, [
        ("Stop the PCA infusion", 0),
        ("Give a PCA dose so he does not wake in pain", 2),
        ("Stimulate him, support his airway and give the prescribed naloxone", 0),
        ("Remove the oxygen to measure his SpO₂ on room air", 2),
        ("Explain to his mother why only Jordan may press the PCA button", 0),
        ("Request a repeat hemoglobin electrophoresis", 1)]),
    "explanation": rationale(
        "<b>Indicated:</b> a respiratory rate of 8 breaths/min, SpO₂ 86% and increasing sedation mean opioid-induced "
        "respiratory depression. The opioid is stopped, he is roused and his airway supported, and naloxone is given as "
        "prescribed (diluted and titrated, so his pain does not return all at once); hypoventilation also increases "
        "sickling. PCA by proxy defeats the safety of PCA: a sleeping client cannot press the button, so the family is "
        "taught not to.",
        "<b>Contraindicated:</b> more opioid worsens the respiratory depression; removing oxygen from a hypoxemic client "
        "is unsafe.",
        "<b>Non-Essential:</b> electrophoresis after the exchange shows the HbS percentage but does nothing for the "
        "emergency."),
})

# Screen 6
C.notes("nn", "Nurses' Notes",
    ("Day 3 0315", "Naloxone 0.04 mg IV given twice; RR 14 breaths/min, SpO₂ 95%, rousable to voice."),
    ("Day 7 1000", "Afebrile 72 hours. SpO₂ 97% on room air; walking the hallway. Pain 2/10 on oral analgesics. Hemoglobin "
     "92 g/L; HbS 28% after the exchange. Hematology restarts hydroxyurea; the nurse completes discharge teaching."))
vitals("Day 7 1000", "36.8° C", "84 beats/min", "16 breaths/min", "122/74 mm Hg", "97% on room air", "2")
s6 = screen(6, INTRO, C, {
    "type": "dropdown_cloze",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 3 0315 and Day 7 1000 and the Vital Signs.",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {"text": "Jordan shows that he understands his teaching when he says that hydroxyurea prevents crises by "
                      "[[drop0]], that he needs [[drop1]] while taking it, and that he will go to the emergency department "
                      "for [[drop2]].",
              "dropdowns": [
                  dd(961, "raising fetal hemoglobin, which does not sickle", "thinning his blood",
                     "replacing the sickle cell gene", "strengthening his spleen"),
                  dd(962, "regular blood counts, because it can lower white cells and platelets",
                     "a low-iron diet", "monthly chest X-rays", "to stop folic acid"),
                  dd(963, "a temperature of 38.5° C or higher, chest pain or shortness of breath, or an erection that "
                          "will not go away",
                     "pain that settles with fluids, rest and his usual tablets",
                     "his usual slight yellowing of the eyes",
                     "tiredness after a long day")]},
    "explanation": rationale(
        "<b>Hydroxyurea:</b> it increases fetal hemoglobin (HbF), which does not polymerize and dilutes HbS in each cell, "
        "so cells sickle less. It reduces painful crises by about 45% and lowers acute chest syndrome and transfusion "
        "needs. It does not change the gene. It suppresses the marrow (neutropenia, thrombocytopenia), so blood counts "
        "are checked regularly and the dose adjusted; it should not be used during pregnancy or when planning one.",
        "<b>Emergency signs:</b> fever (risk of sepsis without a functioning spleen), chest pain or dyspnea (acute chest "
        "syndrome), priapism, sudden weakness, numbness or speech change (stroke) and pain not controlled at home. Pain "
        "that settles at home, his usual mild jaundice and ordinary tiredness do not need emergency care.",
        "<b>Also taught:</b> drink plenty of fluids, avoid cold, altitude and overexertion, take folic acid, keep "
        "pneumococcal, meningococcal, influenza and COVID-19 vaccines up to date, and use the incentive spirometer at home "
        "when ill."),
})
write_case(1, 9,
    "26-year-old male with sickle cell anemia: vaso-occlusive crisis with priapism after dehydration, then acute chest "
    "syndrome, exchange transfusion, PCA oversedation and hydroxyurea teaching.",
    [s1, s2, s3, s4, s5, s6],
    "New case written by Claude on 25 Nov 2026 (NURS 1021 Unit 1, batch 3); checked against Merck Manual Professional "
    "(Sickle Cell Disease, Apr 2026). Please review (standard practice, not on the Merck page): oxygen target 95% or "
    "higher, IV fluid rate, PCA settings and naloxone dose (0.04 mg increments), fever threshold 38.5° C for adults; "
    "urology aspiration for priapism.")
