"""NURS 1021 Unit 1 Case Study 7: vitamin B12 deficiency (pernicious anemia, with metformin and a proton pump
inhibitor) presenting with neurologic signs and falls; vitamin B12 versus folate deficiency.
Outcomes: etiology, pathogenesis and clinical manifestations of anemia related to vitamin B12 or folate deficiency.
Facts checked against the Merck Manual Professional Edition, "Vitamin B12 Deficiency" (Jun 2026), "Folate
Deficiency" (Nov 2026) and "Megaloblastic Macrocytic Anemias" (Mar 2025): defective DNA synthesis with continued RNA
synthesis (large cells, ineffective erythropoiesis); pernicious anemia from autoimmune atrophic gastritis with loss of
intrinsic factor; also gastric surgery, ileal disease, metformin, reduced acid in older adults; folate deficiency from
poor intake, alcohol use disorder, pregnancy, methotrexate, antiseizure drugs; neurologic signs (position and
vibration loss, paresthesias, ataxia, cognitive change) are unique to B12 deficiency and can be permanent; MCV > 100 fL,
hypersegmented neutrophils; B12 < 145 pmol/L; MMA and homocysteine both high in B12 deficiency, only homocysteine in
folate deficiency; B12 1 mg IM, then monthly, for life; never give folate alone (it can correct the anemia while
neurologic damage progresses); reticulocytes rise within 1 week, blood counts correct within about 6 weeks,
neurologic recovery is slower and may be incomplete."""
from nurs1021_common import *

INTRO = ("The nurse on a medical unit is caring for a 61-year-old female client admitted for investigation of anemia "
         "after two falls at home.")
C = Chart2()
C.notes("nn", "Nurses' Notes", ("Day 1 1500",
    "The client was admitted from the emergency department after a fall at home. X-rays show no fracture. The client's "
    "daughter is at the bedside. The health history and physical assessment were completed."))
S1_HX = [
    sec("Reason for admission", "{The client has fallen twice in the past month, both times at night.|correct} "
        "{The client reports feeling tired for several months.|correct}"),
    sec("Neurological symptoms", "{The client reports numbness and tingling in both feet for 4 months, “like wearing thick "
        "socks.”|correct} {The client feels unsteady when walking in the dark.|correct} The daughter reports {that the "
        "client has become forgetful and irritable.|correct}"),
    sec("Diet and elimination", "{The client eats meat, eggs and dairy products daily.} {The client denies black or bloody "
        "stools.}"),
    sec("Medical history and medications", "Type 2 diabetes treated with metformin for 9 years; hypothyroidism treated "
        "with levothyroxine; gastroesophageal reflux treated with omeprazole for 6 years.")]
S1_PA = [
    sec("Skin", "{The skin is pale with a slight yellow tinge.|correct}"),
    sec("Mouth", "{The tongue is red, smooth and burning.|correct}"),
    sec("Neurological", "{Vibration sense is absent at both great toes, and the client cannot tell whether the toes are "
        "moved up or down.|correct} {The Romberg test is positive.|correct} {Pain and temperature sensation in the feet "
        "are intact.}")]
C.doc("hx", "Health History", *S1_HX)
C.doc("pa", "Physical Assessment", *S1_PA)
VS = [vrow("T"), vrow("P"), vrow("RR"), vrow("BP"), vrow(SPO2)]


def vitals(col, *v):
    C.column("vs", "Vital Signs", "", col, list(zip(VS, v)))


vitals("Day 1 1500", "36.8° C", "106 beats/min", "20 breaths/min", "122/74 mm Hg", "98% on room air")
s1 = screen(1, INTRO, C, {
    "type": "highlight",
    "stem": "The nurse reviews the Health History and the Physical Assessment. <b>Highlight</b> the findings that are "
            "consistent with vitamin B12 "
            "deficiency.",
    "options": [],
    "highlightTabs": [highlight_doc("ht1", "Health History", S1_HX), highlight_doc("ht2", "Physical Assessment", S1_PA)],
    "maxCorrectSelections": None,
    "explanation": rationale(
        "<b>Anemia:</b> tiredness and pallor; the slight yellow tinge comes from pallor combined with mild jaundice, because "
        "abnormal red cell precursors are destroyed in the marrow (ineffective erythropoiesis) and release bilirubin.",
        "<b>Glossitis:</b> a red, smooth, burning tongue, because rapidly dividing cells of the tongue also need B12 to make "
        "DNA.",
        "<b>Neurologic findings (unique to B12 deficiency):</b> B12 is needed to maintain myelin. Damage to the dorsal "
        "columns of the spinal cord and peripheral nerves causes numbness and tingling in a stocking distribution, loss of "
        "vibration and position sense, a positive Romberg test, and an unsteady gait that is worse in the dark, when the "
        "client cannot use vision to make up for lost position sense; hence falls at night. Cognitive and mood changes "
        "(forgetfulness, irritability, depression) also occur. These can appear before the anemia and become permanent if "
        "treatment is delayed.",
        "<b>Not consistent:</b> pain and temperature sensation are usually spared in B12 deficiency. A diet with meat, eggs "
        "and dairy supplies B12, so the cause is poor absorption, not intake. No black or bloody stools makes blood loss "
        "unlikely."),
})

# Screen 2
C.notes("nn", "Nurses' Notes", ("Day 1 1730",
    "The laboratory results were reviewed with the internist. The client asks whether to start the folic acid tablets "
    "that a neighbour takes for anemia."))
LAB = [lab("Hemoglobin (Hgb)", "Female: 115–155 g/L"), lab("Mean corpuscular volume (MCV)", "80–100 fL"),
       lab("Reticulocyte count, absolute", "23–90 × 10<sup>9</sup>/L"),
       lab("White blood cell (WBC) count", "3.5–10.5 × 10<sup>9</sup>/L"), lab("Platelet count", "130–380 × 10<sup>9</sup>/L"),
       "<b>Peripheral blood smear</b>", lab("Vitamin B12", "133–675 pmol/L"), lab("Folate (folic acid)", "≥ 10.0 nmol/L"),
       lab("Methylmalonic acid (MMA)", "less than 0.40 µmol/L"), lab("Homocysteine", "5–15 µmol/L"),
       lab("Lactate dehydrogenase (LDH)", "100–205 IU/L"), lab("Bilirubin, total", "3–17 µmol/L")]
C.column("labs", "Laboratory Results", "Laboratory Test and Reference Range", "Day 1 1600", list(zip(LAB, [
    "84 g/L", "116 fL", "14 × 10<sup>9</sup>/L", "3.6 × 10<sup>9</sup>/L", "128 × 10<sup>9</sup>/L",
    "Large oval red cells (macro-ovalocytes); hypersegmented neutrophils", "98 pmol/L", "21 nmol/L", "1.9 µmol/L",
    "32 µmol/L", "860 IU/L", "34 µmol/L"])))
s2 = screen(2, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 1 1730 and the Laboratory Results.",
    "stem": "The nurse explains the differences between the two vitamin deficiencies. For each finding, click to specify "
            "whether it occurs in <b>vitamin B12 deficiency</b>, <b>folate deficiency</b>, or <b>both</b>.",
    "matrix": matrix_mc("Finding", ["Vitamin B12 Deficiency", "Folate Deficiency", "Both"], [
        ("MCV above 100 fL with hypersegmented neutrophils", 2),
        ("Loss of vibration and position sense with an unsteady gait", 0),
        ("Raised methylmalonic acid", 0),
        ("Raised homocysteine", 2),
        ("Common in alcohol use disorder and in pregnancy without supplements", 1),
        ("Caused by a lack of intrinsic factor", 0)]),
    "explanation": rationale(
        "<b>Both:</b> B12 and folate are both needed to make DNA. Without either, cells keep growing (RNA and protein "
        "synthesis continue) but divide poorly, so red cells are large (megaloblastic, MCV above 100 fL) and neutrophils "
        "have extra nuclear lobes. Folate needs B12 to be recycled, and both are needed to convert homocysteine to "
        "methionine, so homocysteine rises in both.",
        "<b>Vitamin B12 only:</b> B12 is also needed to convert methylmalonyl-CoA, so methylmalonic acid rises only in B12 "
        "deficiency; the client's MMA of 1.9 µmol/L with a B12 of 98 pmol/L and normal folate confirm B12 deficiency. Neurologic "
        "damage occurs only in B12 deficiency. Intrinsic factor, made by gastric parietal cells, is needed to absorb B12 in "
        "the terminal ileum.",
        "<b>Folate only:</b> folate stores last only months, so deficiency develops with poor intake (alcohol use disorder), "
        "increased need (pregnancy) or drugs such as methotrexate and phenytoin.",
        "<b>Folic acid alone:</b> it could improve the blood count while the nerve damage progresses, so the nurse advises "
        "the client not to take it unless prescribed."),
})

# Screen 3
C.notes("nn", "Nurses' Notes", ("Day 2 0900",
    "The intrinsic factor antibody test is positive, and the internist has diagnosed pernicious anemia; metformin and "
    "long-term omeprazole may also reduce B12 absorption. At 0300 the client got up alone to use the bathroom and was "
    "found holding on to the doorframe. The client did not fall."))
C.column("labs", "Laboratory Results", "Laboratory Test and Reference Range", "Day 2 0800", list(zip(
    [lab("Intrinsic factor antibodies", "Negative"), lab("Thyrotropin (TSH)", "0.34–5.60 mIU/L")], ["Positive", "2.1 mIU/L"])))
s3 = screen(3, INTRO, C, {
    "type": "dropdown_cloze",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 2 0900 and the Laboratory Results.",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {"text": "The client's red cells are large because [[drop0]]. The deficiency is mainly caused by [[drop1]]. The "
                      "nurse's priority is [[drop2]].",
              "dropdowns": [
                  dd(731, "DNA synthesis is impaired, so precursor cells grow but divide too few times",
                     "too little iron is available to make hemoglobin",
                     "the cells swell from too much water inside them",
                     "the spleen releases young red cells early"),
                  dd(732, "antibodies that block intrinsic factor (pernicious anemia)",
                     "too little vitamin B12 in the diet",
                     "blood loss from the stomach",
                     "too little folate in the diet"),
                  dd(733, "preventing falls caused by loss of position sense",
                     "preventing infection from a low white cell count",
                     "relieving the burning tongue",
                     "teaching the client how to give injections")]},
    "explanation": rationale(
        "<b>Large cells:</b> without B12, DNA synthesis is impaired while RNA and protein synthesis continue, so precursors "
        "grow large but divide fewer times; many die in the marrow (ineffective erythropoiesis), raising LDH and bilirubin. "
        "Iron deficiency makes cells small.",
        "<b>Cause:</b> in pernicious anemia, autoimmune gastritis destroys parietal cells, and antibodies block intrinsic "
        "factor, so B12 cannot be absorbed in the ileum. It is often associated with other autoimmune diseases such as "
        "autoimmune thyroid disease. Metformin and reduced stomach acid (omeprazole) add to poor absorption. The client's diet "
        "contains B12, and folate is normal.",
        "<b>Priority:</b> the client has already fallen twice, has lost position sense and gets up alone at night: injury "
        "from falls is the most immediate risk. The white cell count is only mildly low; glossitis and teaching follow."),
})

# Screen 4
C.notes("nn", "Nurses' Notes", ("Day 2 1000", "Orders were received from the internist."))
C.rows("orders", "Orders", ["Category", "Order"], [
    ["<b>Vitamin B12</b>", "Cyanocobalamin 1,000 mcg IM daily for 7 days, then weekly for 4 weeks, then monthly for life."],
    ["<b>Safety</b>", "Fall precautions. Physiotherapy for gait and balance."],
    ["<b>Diet</b>", "Soft diet as tolerated."],
    ["<b>Monitoring</b>", "Reticulocyte count and CBC on day 7. Gastroscopy as an outpatient."]])
s4 = screen(4, INTRO, C, select_all(741, [
    ("A", "Give the cyanocobalamin injections as prescribed", True),
    ("B", "Keep the bed low, the call bell in reach and a night light on, and assist the client when walking", True),
    ("C", "Inspect the client's feet daily for injuries the client may not feel", True),
    ("D", "Offer soft, bland foods and mouth care with a soft toothbrush", True),
    ("E", "Give folic acid tablets instead of injections, since they are easier to take", False),
    ("F", "Teach the client that eating more meat and dairy will correct the deficiency", False),
    ("G", "Keep the client on bed rest until the hemoglobin is normal", False)],
    rationale(
        "<b>Include:</b> in pernicious anemia the oral B12 in food cannot be absorbed, so B12 is given by injection {A}. "
        "Fall precautions protect the client while position sense is lost {B}. Loss of sensation in the feet means injuries can go "
        "unnoticed {C}. Glossitis makes spicy, hot and acidic foods painful {D}.",
        "<b>Do not include:</b> folic acid can correct the anemia but not the nerve damage, which can progress {E}. Without "
        "intrinsic factor, dietary B12 is not absorbed {F}. Bed rest increases weakness and deconditioning; the client walks with "
        "assistance and physiotherapy {G}."),
    preamble="The nurse has reviewed the Nurses' Notes from Day 2 1000 and the Orders.",
    stem="Which interventions should the nurse include in the client's plan of care? Select all that apply."))

# Screen 5
C.notes("nn", "Nurses' Notes", ("Day 2 1100",
    "A covering physician left a verbal message to start folic acid 5 mg PO daily and “hold the B12 until after the "
    "gastroscopy.” The client's daughter asks whether the injection could be given through the IV to spare the client a "
    "needle."))
s5 = screen(5, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 2 1100.",
    "stem": "For each nursing action, click to specify whether the action is <b>Indicated</b>, <b>Non-Essential</b>, or "
            "<b>Contraindicated</b>.",
    "matrix": matrix_mc("Nursing Action", IMC, [
        ("Contact the internist to clarify the message before changing the treatment", 0),
        ("Give folic acid 5 mg PO daily and hold the cyanocobalamin", 2),
        ("Give today's cyanocobalamin dose into the deltoid muscle", 0),
        ("Give the cyanocobalamin as an IV push to avoid an injection", 2),
        ("Request a bone marrow biopsy to confirm the diagnosis", 1),
        ("Walk with the client using a gait belt to the bathroom", 0)]),
    "explanation": rationale(
        "<b>Contraindicated:</b> giving folate alone to a client with B12 deficiency can improve the blood count while the "
        "neurologic damage continues, and holding B12 delays treatment that should start at once; gastroscopy does not "
        "require it to be held. Cyanocobalamin is given IM (or deep subcutaneously); given IV, most of it is lost in the "
        "urine before it can be used.",
        "<b>Indicated:</b> an order that conflicts with the diagnosis and the existing plan is clarified with the "
        "prescriber before acting. The prescribed IM dose is given. A gait belt and assistance protect the client from falls.",
        "<b>Non-Essential:</b> low B12, high methylmalonic acid and positive intrinsic factor antibodies already confirm "
        "the diagnosis; a bone marrow biopsy is not needed."),
})

# Screen 6
C.notes("nn", "Nurses' Notes",
    ("Day 2 1200", "The internist confirmed the original plan, and cyanocobalamin was given IM."),
    ("Week 6 1000", "The client attends a clinic visit. The client reports improved energy, and the tongue is no longer "
     "sore. Tingling in the feet has lessened but is still present. The client walks with a cane and has had no further "
     "falls. The nurse reviews the client's understanding of the condition."))
vitals("Week 6 1000", "36.7° C", "82 beats/min", "16 breaths/min", "124/76 mm Hg", "99% on room air")
C.column("labs", "Laboratory Results", "Laboratory Test and Reference Range", "Day 7", list(zip(
    [LAB[0], LAB[2]], ["88 g/L", "198 × 10<sup>9</sup>/L"])))
C.column("labs", "Laboratory Results", "Laboratory Test and Reference Range", "Week 6", list(zip(
    [LAB[0], LAB[1], LAB[2], LAB[3], LAB[4]],
    ["121 g/L", "94 fL", "62 × 10<sup>9</sup>/L", "5.8 × 10<sup>9</sup>/L", "214 × 10<sup>9</sup>/L"])))
s6 = screen(6, "Six weeks later, the client returns to the clinic.", C, select_all(761, [
    ("A", "“I will need B12 injections every month for the rest of my life.”", True),
    ("B", "“The numbness in my feet may take months to improve and might not go away completely.”", True),
    ("C", "“I'll check my feet every day, because I may not feel a cut or blister.”", True),
    ("D", "“Now that my blood count is normal, I can stop the injections.”", False),
    ("E", "“I can switch to my neighbour's folic acid tablets instead of the injections.”", False),
    ("F", "“I'll tell my doctor if the tingling gets worse or my balance changes.”", True),
    ("G", "“Eating liver once a week will keep my B12 up.”", False)],
    rationale(
        "<b>Response:</b> reticulocytes rose sharply by day 7 (14 to 198 × 10⁹/L), the expected first sign of response, "
        "and by week 6 hemoglobin, MCV, white cells and platelets have returned to normal. Neurologic recovery is slower.",
        "<b>Understood:</b> the cause, loss of intrinsic factor, is permanent, so B12 is given for life {A}. Nerve recovery "
        "takes months and may be incomplete, especially when symptoms were present for a long time {B}. Reduced sensation "
        "means daily foot checks {C}. Worsening neurologic symptoms suggest inadequate treatment {F}.",
        "<b>Needs more teaching:</b> stopping injections leads to relapse {D}. Folic acid does not treat B12 deficiency and "
        "can hide it while nerve damage progresses {E}. Dietary B12 cannot be absorbed without intrinsic factor {G}."),
    preamble="The nurse has reviewed the Nurses' Notes from Day 2 1200 and Week 6 1000, the Vital Signs, and the "
             "Laboratory Results.",
    stem="Which statements by the client indicate an understanding of the teaching? Select all that apply."))
write_case(1, 7,
    "61-year-old female with pernicious anemia (plus metformin and omeprazole) presenting with falls, paresthesias and "
    "glossitis: megaloblastic anemia, vitamin B12 versus folate deficiency (methylmalonic acid, homocysteine), IM "
    "cyanocobalamin and why folate alone is unsafe.",
    [s1, s2, s3, s4, s5, s6],
    "New case written by Claude on 25 Nov 2026 (NURS 1021 Unit 1, batch 2); checked against Merck Manual Professional "
    "(Vitamin B12 Deficiency, Jun 2026; Folate Deficiency, Nov 2026; Megaloblastic Macrocytic Anemias, Mar 2025). Please "
    "review: methylmalonic acid (< 0.40 µmol/L) and homocysteine (5–15 µmol/L) reference ranges (not in the MCC list); "
    "the cyanocobalamin schedule (daily × 7, weekly × 4, then monthly; Merck gives 1 mg IM 1–4 times a week, then "
    "monthly); outpatient gastroscopy at diagnosis of pernicious anemia.")
