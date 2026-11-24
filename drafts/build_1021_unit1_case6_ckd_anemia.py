"""NURS 1021 Unit 1 Case Study 6: anemia of chronic kidney disease (diabetic nephropathy, CKD stage 4, not on
dialysis), with iron deficiency; IV iron sucrose, then darbepoetin alfa; an excessive hemoglobin rise with hypertension.
Outcomes: etiology, pathogenesis and clinical manifestations of anemia of chronic renal failure.
Facts checked against the Merck Manual Professional Edition, "Anemia of Renal Disease" (Mar 2025) and "Chronic
Kidney Disease" (Feb 2026): mainly decreased erythropoietin (plus hepcidin iron sequestration, shortened red cell
survival, blood loss); appears at creatinine clearance < 45 mL/min (stage 3 or worse); normocytic, normochromic,
low reticulocytes; ESA (epoetin or darbepoetin) with iron; target Hb 100-115 g/L; harm (VTE, MI, stroke, death) when Hb
rises above 120-130 g/L; IV iron if not on dialysis when ferritin < 100 and TSAT < 0.40 or ferritin < 300 and TSAT <
0.25; maximum response by 8 to 12 weeks; transfusion if Hb < 80 g/L or symptoms. ESA hypertension is from product
monographs / nursing texts (not named on the Merck pages)."""
from nurs1021_common import *

INTRO = ("The nurse in a nephrology clinic is assessing Margaret, a 67-year-old female client with type 2 diabetes, "
         "hypertension and stage 4 chronic kidney disease, who reports increasing tiredness.")
C = Chart2()
C.notes("nn", "Nurses' Notes", ("Day 1 1000",
    "Reports 3 months of increasing tiredness; has to sit down twice while grocery shopping and becomes short of breath "
    "walking up the driveway. Feels cold even indoors. Conjunctivae and nail beds pale. Skin dry with scratch marks on the "
    "forearms; says she is “itchy all the time.” Notices a metallic taste and a poor appetite. 1+ pitting edema of both "
    "ankles. No blood in stools; no black stools. Medications: insulin glargine, ramipril, amlodipine, furosemide, "
    "atorvastatin. Weight 68 kg."))
VS = [vrow("T"), vrow("P"), vrow("RR"), vrow("BP"), vrow(SPO2)]


def vitals(col, *v):
    C.column("vs", "Vital Signs", "", col, list(zip(VS, v)))


vitals("Day 1 1000", "36.4° C", "104 beats/min", "20 breaths/min", "158/92 mm Hg", "97% on room air")
s1 = screen(1, INTRO, C, select_all(611, [
    ("A", "Tiredness and shortness of breath walking up the driveway", True),
    ("B", "Pale conjunctivae and nail beds", True),
    ("C", "Feeling cold even indoors", True),
    ("D", "Heart rate of 104 beats/min", True),
    ("E", "Itching with scratch marks on the forearms", False),
    ("F", "Metallic taste and poor appetite", False),
    ("G", "1+ pitting edema of both ankles", False),
    ("H", "Blood pressure of 158/92 mm Hg", False)],
    rationale(
        "<b>Consistent with anemia:</b> reduced oxygen delivery causes fatigue and dyspnea on exertion {A}, pallor of the "
        "conjunctivae and nail beds {B}, cold intolerance from reduced tissue oxygenation and vasoconstriction {C}, and a "
        "compensatory tachycardia {D}.",
        "<b>Not anemia:</b> these are manifestations of chronic kidney disease itself. Itching (uremic pruritus) {E} and a "
        "metallic taste with anorexia {F} come from retained uremic waste products. Ankle edema reflects sodium and water "
        "retention {G}, and hypertension is present in over 80% of clients with advanced chronic kidney disease {H}. The "
        "nurse separates them because they are treated differently."),
    stem="The nurse reviews the client's history and assessment. Which of the following findings would be consistent "
         "with <b>anemia</b>? Select all that apply."))

# Screen 2
C.notes("nn", "Nurses' Notes", ("Day 3 1100",
    "Laboratory results reviewed with the nephrologist. Fecal immunochemical test negative. Margaret asks why her kidneys "
    "would affect her blood."))
LAB = [lab("Hemoglobin (Hgb)", "Female: 115–155 g/L"), lab("Mean corpuscular volume (MCV)", "80–100 fL"),
       lab("Reticulocyte count, absolute", "23–90 × 10<sup>9</sup>/L"), lab("Ferritin", "Female: 11–307 µg/L"),
       lab("Transferrin saturation", "0.20–0.50"), lab("Vitamin B12", "133–675 pmol/L"),
       lab("Folate (folic acid)", "≥ 10.0 nmol/L"), lab("Creatinine", "Female: 22–75 µmol/L"),
       lab("Estimated glomerular filtration rate (eGFR)", "≥ 60 mL/min/1.73 m²"), lab("Potassium (K)", "3.5–5.1 mmol/L")]
C.column("labs", "Laboratory Results", "Laboratory Test and Reference Range", "Day 1", list(zip(LAB, [
    "86 g/L", "88 fL", "18 × 10<sup>9</sup>/L", "64 µg/L", "0.16", "412 pmol/L", "24 nmol/L", "198 µmol/L",
    "22 mL/min/1.73 m²", "5.3 mmol/L"])))
s2 = screen(2, "Margaret returns to review her blood work.", C, {
    "type": "dropdown_cloze",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 3 1100 and the Laboratory Results.",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {"text": "Margaret's damaged kidneys make too little [[drop0]], so her bone marrow produces fewer red cells. "
                      "This is shown by [[drop1]]. Her ferritin and transferrin saturation show [[drop2]].",
              "dropdowns": [
                  dd(621, "erythropoietin", "renin", "intrinsic factor", "thrombopoietin"),
                  dd(622, "normal-sized red cells with a low reticulocyte count",
                     "small, pale red cells with a high platelet count",
                     "large red cells with hypersegmented neutrophils",
                     "a high reticulocyte count with a raised bilirubin"),
                  dd(623, "iron deficiency that must be corrected for treatment to work",
                     "iron overload from earlier transfusions",
                     "normal iron stores that need no treatment",
                     "a deficiency of vitamin B12")]},
    "explanation": rationale(
        "<b>Erythropoietin:</b> cells in the kidney's interstitium sense oxygen delivery and release erythropoietin, which "
        "stimulates the marrow to make red cells. As kidney tissue is lost (anemia usually appears once clearance falls "
        "below about 45 mL/min, stage 3 or worse), erythropoietin falls. Uremia also shortens red cell survival, and blood "
        "is lost through platelet dysfunction and blood draws. Renin raises blood pressure; intrinsic factor is needed for "
        "vitamin B12 absorption; thrombopoietin regulates platelets.",
        "<b>Pattern:</b> the anemia is <b>normocytic and normochromic</b> (MCV 88 fL) with a reticulocyte count that is "
        "inappropriately low for the degree of anemia: the marrow is not being told to make more cells. Small cells with "
        "high platelets suggest iron deficiency; large cells with hypersegmented neutrophils suggest B12 or folate "
        "deficiency (both normal here); a high reticulocyte count with raised bilirubin suggests hemolysis.",
        "<b>Iron:</b> in chronic kidney disease, hepcidin rises and traps iron in stores, and erythropoiesis-stimulating "
        "agents (ESAs) use iron quickly. Her ferritin of 64 µg/L and transferrin saturation of 0.16 show iron deficiency; "
        "without enough iron, an ESA will not work. Her negative fecal immunochemical test makes bleeding from the bowel "
        "less likely."),
})

# Screen 3
C.notes("nn", "Nurses' Notes", ("Day 3 1130",
    "Nephrologist plans IV iron now and darbepoetin alfa once iron is replaced. Margaret says she had to stop on the stairs "
    "twice on her way into the clinic."))
C.rows("orders", "Orders", ["Category", "Order"], [
    ["<b>Iron</b>", "Iron sucrose 200 mg IV over 15 minutes, 5 doses over 2 weeks."],
    ["<b>Erythropoiesis-stimulating agent</b>", "Darbepoetin alfa 30 mcg subcutaneously every 2 weeks, starting week 3. "
                                                "Hold the dose and notify the nephrologist if hemoglobin is above 115 g/L, "
                                                "rises more than 10 g/L in 2 weeks, or BP is above 160/100 mm Hg."],
    ["<b>Monitoring</b>", "Hemoglobin every 2 weeks until stable; ferritin and transferrin saturation every 3 months. BP "
                          "before each dose."]])
s3 = screen(3, "Margaret returns to review her blood work.", C, {
    "type": "bowtie",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 3 1130 and the Orders.",
    "stem": "Complete the diagram by dragging from the choices below to specify what condition the client is most likely "
            "experiencing, 2 actions the nurse should take to address that condition, and 2 parameters the nurse should "
            "monitor to assess the client's progress.",
    "bowtieConditions": bowtie_list(631, ["Anemia of chronic kidney disease"], [
        "Iron deficiency anemia from bowel bleeding", "Vitamin B12 deficiency anemia", "Aplastic anemia"]),
    "bowtieActions": bowtie_list(632, [
        "Give the IV iron sucrose as prescribed",
        "Give the darbepoetin as prescribed once iron is replaced"], [
        "Give darbepoetin to raise hemoglobin to 140 g/L",
        "Restrict dietary iron to protect the kidneys",
        "Give vitamin B12 by intramuscular injection"]),
    "bowtieParams": bowtie_list(633, ["Hemoglobin level", "Blood pressure"], [
        "Serum amylase", "INR", "Absolute neutrophil count"]),
    "explanation": rationale(
        "<b>Condition:</b> normocytic anemia with a low reticulocyte count in stage 4 chronic kidney disease is anemia of "
        "chronic kidney disease, with iron deficiency adding to it. The fecal immunochemical test is negative, vitamin B12 "
        "and folate are normal, and only the red cell line is low (not aplastic anemia).",
        "<b>Actions:</b> iron is replaced first, then the ESA (darbepoetin) replaces the missing erythropoietin. The target "
        "hemoglobin is 100 to 115 g/L, not normal: raising it above 120 to 130 g/L increases venous thromboembolism, "
        "myocardial infarction, stroke and death. Restricting iron would worsen the deficiency; B12 is not deficient.",
        "<b>Parameters:</b> hemoglobin shows the response (and protects against overshooting the target); ESAs raise blood "
        "pressure, which is already high in chronic kidney disease, so BP is checked before each dose."),
})

# Screen 4
C.notes("nn", "Nurses' Notes", ("Week 3 1000",
    "All 5 doses of iron sucrose given without reaction. First darbepoetin dose today; Margaret will give her own "
    "injections at home. She asks what she needs to know."))
vitals("Week 3 1000", "36.5° C", "98 beats/min", "18 breaths/min", "146/88 mm Hg", "98% on room air")
C.column("labs", "Laboratory Results", "Laboratory Test and Reference Range", "Week 3", list(zip(
    [LAB[0], LAB[3], LAB[4]], ["92 g/L", "286 µg/L", "0.29"])))
s4 = screen(4, "Three weeks later, Margaret returns to the clinic.", C, select_all(641, [
    ("A", "Check and record your blood pressure at home every day and bring the record to each visit", True),
    ("B", "Report a severe headache, chest pain, sudden weakness or a painful, swollen leg right away", True),
    ("C", "Keep your blood test appointments every 2 weeks so the dose can be adjusted", True),
    ("D", "Store the pre-filled syringes in the refrigerator and do not shake them", True),
    ("E", "The goal is a hemoglobin in the normal range, about 130 g/L", False),
    ("F", "You can stop taking amlodipine because your energy will improve", False),
    ("G", "Expect your energy to improve gradually over several weeks", True),
    ("H", "Double the next dose if you miss one", False)],
    rationale(
        "<b>Include:</b> ESAs raise blood pressure, so home monitoring is essential {A}. A rapid rise in hemoglobin "
        "increases the risk of stroke, myocardial infarction and venous thrombosis; their warning signs are reported at "
        "once {B}. Hemoglobin is checked often so the dose can be lowered or held if it rises too fast {C}. Darbepoetin is "
        "a protein: it is kept refrigerated and not shaken, which can damage it {D}. The marrow needs weeks to respond; the "
        "maximum response takes 8 to 12 weeks {G}.",
        "<b>Do not include:</b> the target is 100 to 115 g/L, not normal, because higher values increase cardiovascular "
        "events and death {E}. Antihypertensives are needed even more on an ESA {F}. Doubling a dose risks an excessive "
        "rise; a missed dose is discussed with the clinic {H}."),
    preamble="The nurse has reviewed the Nurses' Notes from Week 3 1000, the Vital Signs, and the Laboratory Results.",
    stem="Which instructions should the nurse include in Margaret's teaching? Select all that apply."))

# Screen 5
C.notes("nn", "Nurses' Notes", ("Week 9 1000",
    "Visit for her scheduled darbepoetin dose. Reports a throbbing headache for 2 days and that her home BP readings have "
    "been 165 to 175 systolic. No chest pain; no weakness or numbness; speech clear. Says she has “more energy than in "
    "years.”"))
vitals("Week 9 1000", "36.6° C", "84 beats/min", "18 breaths/min", "174/98 mm Hg", "98% on room air")
C.column("labs", "Laboratory Results", "Laboratory Test and Reference Range", "Week 7", list(zip([LAB[0]], ["102 g/L"])))
C.column("labs", "Laboratory Results", "Laboratory Test and Reference Range", "Week 9", list(zip([LAB[0]], ["121 g/L"])))
s5 = screen(5, "At week 9, Margaret returns to the clinic.", C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Week 9 1000, the Vital Signs, and the Laboratory Results.",
    "stem": "For each nursing action, click to specify whether the action is <b>Indicated</b>, <b>Non-Essential</b>, or "
            "<b>Contraindicated</b>.",
    "matrix": matrix_mc("Nursing Action", IMC, [
        ("Give today's scheduled darbepoetin dose", 2),
        ("Hold the dose and notify the nephrologist", 0),
        ("Recheck the BP after 5 minutes of rest and assess for neurologic changes", 0),
        ("Review her home BP record and whether she is taking her antihypertensives", 0),
        ("Request a repeat vitamin B12 level", 1),
        ("Tell Margaret to take an extra amlodipine tablet tonight", 2)]),
    "explanation": rationale(
        "<b>Contraindicated:</b> her hemoglobin is 121 g/L, above the 115 g/L hold limit, it rose 19 g/L in 2 weeks, and "
        "her BP is above 160/100 mm Hg, so all three hold criteria are met; giving the dose would raise the risk of stroke "
        "and thrombosis. The nurse does not change antihypertensive doses without a prescription.",
        "<b>Indicated:</b> the dose is held and the nephrologist notified to adjust the ESA and her BP treatment. A headache "
        "with a BP of 174/98 mm Hg needs a repeat reading and a neurologic check (speech, strength, vision) to exclude "
        "hypertensive emergency or stroke. Missed antihypertensive doses are a common, correctable cause of high BP.",
        "<b>Non-Essential:</b> her vitamin B12 was normal, and B12 deficiency does not explain a rising hemoglobin."),
})

# Screen 6
C.notes("nn", "Nurses' Notes", ("Week 16 1000",
    "Darbepoetin was held for 2 weeks, then restarted at 20 mcg every 2 weeks; amlodipine was increased. No headaches. "
    "Walks to the grocery store and shops without needing to sit down."))
vitals("Week 16 1000", "36.5° C", "80 beats/min", "16 breaths/min", "138/84 mm Hg", "98% on room air")
C.column("labs", "Laboratory Results", "Laboratory Test and Reference Range", "Week 16", list(zip(
    [LAB[0], LAB[3], LAB[4], LAB[7], LAB[8], LAB[9]],
    ["108 g/L", "254 µg/L", "0.27", "214 µmol/L", "20 mL/min/1.73 m²", "5.4 mmol/L"])))
s6 = screen(6, "At week 16, Margaret returns for follow-up.", C, options_q("trend", 6617, [
    ("A", "Hemoglobin of 108 g/L at week 16", True),
    ("B", "Ferritin of 254 µg/L and transferrin saturation of 0.27", True),
    ("C", "Blood pressure of 138/84 mm Hg", True),
    ("D", "Shops without needing to sit down", True),
    ("E", "Hemoglobin of 121 g/L at week 9", False),
    ("F", "Creatinine of 214 µmol/L", False),
    ("G", "Potassium of 5.4 mmol/L", False)],
    rationale(
        "<b>Goals met:</b> her hemoglobin is within the 100 to 115 g/L target {A}; iron stores are replete (transferrin "
        "saturation above 0.20 and ferritin above 100 µg/L), so the ESA can work {B}; BP is controlled after the dose "
        "adjustment {C}; and her exercise tolerance has improved, the aim of treating the anemia {D}.",
        "<b>Not evidence of goals met:</b> a hemoglobin of 121 g/L was above target and led to the dose being held {E}. "
        "Creatinine and potassium reflect kidney function, which ESAs and iron do not improve; her slowly rising creatinine "
        "and high-normal potassium are followed by the nephrologist {F,G}."),
    preamble="The nurse has reviewed the Nurses' Notes from Week 16 1000, the Vital Signs, and the Laboratory Results.",
    stem="Based on the trends in the client's chart, which findings indicate that the treatment of the anemia is meeting "
         "its goals? Select all that apply."))
write_case(1, 6,
    "67-year-old female with diabetic nephropathy (stage 4 chronic kidney disease) and anemia: erythropoietin deficiency, "
    "anemia versus uremic manifestations, IV iron, darbepoetin alfa teaching, hold criteria and target hemoglobin.",
    [s1, s2, s3, s4, s5, s6],
    "New case written by Claude on 25 Nov 2026 (NURS 1021 Unit 1, batch 2); checked against Merck Manual Professional "
    "(Anemia of Renal Disease, Mar 2025; Chronic Kidney Disease, Feb 2026). Please review: darbepoetin 30 mcg every 2 "
    "weeks (about 0.45 mcg/kg) and the clinic hold criteria (example protocol); ESA-induced hypertension (product "
    "monograph, not on the Merck pages); folate reference range ≥ 10.0 nmol/L (MCC).")
