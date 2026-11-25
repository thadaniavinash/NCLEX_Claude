"""NURS 1021 Unit 1 Case Study 5: severe aplastic anemia after benzene solvent exposure, with neutropenic fever;
immunosuppressive therapy (equine antithymocyte globulin, cyclosporine, eltrombopag).
Outcomes: etiology, pathogenesis and clinical manifestations of aplastic anemia (pancytopenia).
Facts checked against the Merck Manual Professional Edition, "Aplastic Anemia" (full review Mar 2025, updated Apr
2026): stem cell injury (mostly immune) with a hypocellular marrow and cytopenias; most common in adolescents and
young adults; causes include benzene, drugs, radiation, seronegative hepatitis, EBV/CMV, pregnancy, inherited marrow
failure; anemia = weakness/fatigue, thrombocytopenia = petechiae, ecchymoses, gum bleeding, neutropenia = life-
threatening infections; no splenomegaly; severe = cellularity < 25% plus 2 of ANC < 0.5, absolute reticulocytes < 60,
platelets < 20 x 10^9/L; HSCT is the treatment of choice in younger patients with a matched donor, otherwise equine
ATG + cyclosporine (+/- eltrombopag); ATG causes allergic reactions and serum sickness."""
from nurs1021_common import *

INTRO = ("The nurse on a medical unit is caring for a 24-year-old male client admitted from the emergency department "
         "with fever, bruising and nosebleeds.")
C = Chart2()
C.notes("nn", "Nurses' Notes", ("Day 1 1400",
    "The client was admitted to the medical unit from the emergency department with fever, bruising and nosebleeds. "
    "The health history and physical assessment were completed. The client is anxious about the cause of the symptoms."))
C.doc("hx", "Health History",
    sec("Reason for admission", "Increasing tiredness and shortness of breath when climbing stairs for 6 weeks. Sore "
        "throat and painful mouth ulcers for 1 week. Fever and chills since last night. A nosebleed this morning lasted "
        "40 minutes, and the gums bleed when the client brushes the teeth."),
    sec("Occupational history", "The client works as a maintenance mechanic at a petrochemical plant and cleans machine "
        "parts with a benzene-containing solvent, often without gloves."),
    sec("Medications", "No regular medications."),
    sec("Weight", "78 kg."))
C.doc("pa", "Physical Assessment",
    sec("Skin", "The conjunctivae and nail beds are pale. Petechiae are present over both lower legs. Several bruises are "
        "present on the arms, which the client cannot explain."),
    sec("Mouth", "Two shallow ulcers are present on the inner cheek."),
    sec("Lymph nodes", "No enlarged lymph nodes are palpable."),
    sec("Respiratory", "The lungs are clear on auscultation."),
    sec("Abdomen", "The liver and spleen are not palpable."))
VS = [vrow("T"), vrow("P"), vrow("RR"), vrow("BP"), vrow(SPO2)]


def vitals(col, *v):
    C.column("vs", "Vital Signs", "", col, list(zip(VS, v)))


vitals("Day 1 1400", "38.6° C", "118 beats/min", "22 breaths/min", "112/68 mm Hg", "97% on room air")
s1 = screen(1, INTRO, C, options_q("select_n", 511, [
    ("A", "Temperature of 38.6° C with chills", True),
    ("B", "Nosebleed lasting 40 minutes and bleeding gums", True),
    ("C", "Petechiae on both lower legs and unexplained bruises", True),
    ("D", "Heart rate of 118 beats/min with shortness of breath on stairs", True),
    ("E", "No enlarged lymph nodes", False),
    ("F", "Liver and spleen not palpable", False),
    ("G", "Takes no regular medications", False),
    ("H", "Lungs clear on auscultation", False)],
    rationale(
        "<b>Require follow-up:</b> fever with chills may be the first sign of a serious infection when white cells are low "
        "{A}. Prolonged nosebleeds, bleeding gums {B}, petechiae and unexplained bruising {C} point to a low platelet "
        "count. Tachycardia with exertional dyspnea and pallor reflect anemia: the heart beats faster to deliver oxygen with "
        "less hemoglobin {D}. Together, signs of anemia, infection and bleeding suggest that all three cell lines are low "
        "(<b>pancytopenia</b>), the picture of bone marrow failure.",
        "<b>Do not require follow-up:</b> the absence of enlarged lymph nodes, liver and spleen is a helpful negative: "
        "aplastic anemia does not enlarge the spleen, whereas leukemia and lymphoma often enlarge nodes, liver or spleen "
        "{E,F}. Taking no medications {G} and clear lungs {H} need no action; medication and chemical exposures are still "
        "recorded as possible causes."),
    limit=4,
    stem="The nurse reviews the client's history and assessment. <b>Select the 4 findings</b> that require follow-up."))

# Screen 2
C.notes("nn", "Nurses' Notes", ("Day 1 1530",
    "The hematology service was consulted, and a bone marrow biopsy was performed at the bedside. A pressure dressing is "
    "in place over the right posterior iliac crest, with no bleeding. The client asks, “Why do I have mouth sores, "
    "bleeding and no energy all at the same time?”"))
LAB = [lab("Hemoglobin (Hgb)", "Male: 125–170 g/L"), lab("Mean corpuscular volume (MCV)", "80–100 fL"),
       lab("Reticulocyte count, absolute", "23–90 × 10<sup>9</sup>/L"),
       lab("White blood cell (WBC) count", "3.5–10.5 × 10<sup>9</sup>/L"),
       lab("Neutrophils, absolute", "2.0–7.5 × 10<sup>9</sup>/L"), lab("Platelet count", "130–380 × 10<sup>9</sup>/L"),
       "<b>Peripheral blood smear</b>", lab("Prothrombin time (PT)", "10–14 s"),
       lab("Activated partial thromboplastin time (aPTT)", "22–30 s")]
C.column("labs", "Laboratory Results", "Laboratory Test and Reference Range", "Day 1 1440", list(zip(LAB, [
    "72 g/L", "98 fL", "12 × 10<sup>9</sup>/L", "1.4 × 10<sup>9</sup>/L", "0.3 × 10<sup>9</sup>/L",
    "9 × 10<sup>9</sup>/L", "Few cells of all types; no blasts; no abnormal cells", "12 s", "27 s"])))
s2 = screen(2, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 1 1530 and the Laboratory Results.",
    "stem": "For each finding, click to specify whether it is mainly caused by <b>anemia</b>, <b>neutropenia</b>, or "
            "<b>thrombocytopenia</b>.",
    "matrix": matrix_mc("Finding", ["Anemia", "Neutropenia", "Thrombocytopenia"], [
        ("Tiredness and shortness of breath on exertion", 0),
        ("Painful mouth ulcers and sore throat", 1),
        ("Bleeding gums and a prolonged nosebleed", 2),
        ("Fever with chills", 1),
        ("Petechiae on the lower legs", 2),
        ("Pale conjunctivae and nail beds", 0)]),
    "explanation": rationale(
        "<b>Why all three:</b> in aplastic anemia the hematopoietic stem cells are lost, usually through an immune attack "
        "that may be triggered by a toxin (benzene), a drug, radiation or a virus. The marrow becomes empty and fatty, so it "
        "makes too few red cells, white cells and platelets. The client's results show severe disease: neutrophils "
        "0.3 × 10⁹/L, platelets 9 × 10⁹/L and absolute reticulocytes 12 × 10⁹/L. The smear has no blasts (unlike "
        "leukemia), and the PT and aPTT are normal (unlike DIC).",
        "<b>Anemia:</b> less hemoglobin means less oxygen delivery: fatigue, dyspnea on exertion, pallor and tachycardia. "
        "The low reticulocyte count shows the marrow is not responding.",
        "<b>Neutropenia:</b> without neutrophils, bacteria and fungi invade mucous membranes, causing mouth ulcers, sore "
        "throat and fever. Infections can be life-threatening, and the usual signs (pus, swelling) may be absent.",
        "<b>Thrombocytopenia:</b> platelets form the first plug in small vessels; when they are very low, the client has "
        "petechiae, bruising and mucosal bleeding (gums, nose)."),
})

# Screen 3
C.notes("nn", "Nurses' Notes", ("Day 1 1600",
    "The preliminary bone marrow report shows a marrow cellularity of about 10%, replaced by fat, with no blasts. The "
    "client's temperature is 38.9° C, with rigors. Blood cultures have not yet been drawn, and no antibiotic has been "
    "prescribed. The client is anxious and asks whether this is leukemia."))
vitals("Day 1 1600", "38.9° C", "124 beats/min", "24 breaths/min", "104/62 mm Hg", "96% on room air")
s3 = screen(3, INTRO, C, {
    "type": "dropdown_cloze",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 1 1600 and the Vital Signs.",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {"text": "The client's results are most consistent with [[drop0]]. The most likely cause is [[drop1]]. The nurse's "
                      "priority is [[drop2]].",
              "dropdowns": [
                  dd(5313, "severe aplastic anemia", "acute leukemia", "iron deficiency anemia",
                     "disseminated intravascular coagulation"),
                  dd(532, "repeated skin contact with a benzene solvent", "a diet low in iron and folate",
                     "an inherited deficiency of factor VIII", "an enlarged spleen trapping blood cells"),
                  dd(533, "sepsis from fever with a very low neutrophil count",
                     "a spontaneous bleed from the low platelet count",
                     "activity intolerance from anemia",
                     "anxiety about the diagnosis")]},
    "explanation": rationale(
        "<b>Severe aplastic anemia:</b> pancytopenia with a hypocellular marrow (about 10%, replaced by fat) and no abnormal "
        "cells. It is severe because cellularity is below 25% and at least two of these are present: neutrophils below "
        "0.5 × 10⁹/L, absolute reticulocytes below 60 × 10⁹/L, platelets below 20 × 10⁹/L. Leukemia fills the marrow with "
        "blasts; DIC prolongs the PT and aPTT.",
        "<b>Cause:</b> benzene is a well-known marrow toxin, absorbed through the skin and lungs; about half of cases have "
        "no cause found. Diet causes deficiency anemias, not pancytopenia with an empty marrow; aplastic anemia does not "
        "enlarge the spleen.",
        "<b>Priority:</b> fever with neutrophils below 0.5 × 10⁹/L is <b>febrile neutropenia</b>, a medical emergency: "
        "infection can progress to septic shock within hours, and the client's heart rate is rising and BP is falling. Blood cultures "
        "are drawn and broad-spectrum IV antibiotics are started within 60 minutes. Bleeding risk is high and is managed "
        "with precautions and platelets, but untreated sepsis is the more immediate threat to life."),
})

# Screen 4
C.notes("nn", "Nurses' Notes", ("Day 1 1700",
    "Blood cultures were drawn from two sites at 1615, and IV piperacillin-tazobactam was started at 1630. The client was "
    "moved to a private room. The hematologist plans immunosuppressive therapy because the client's only sibling is not a "
    "tissue match; a search for an unrelated donor has started."))
C.rows("orders", "Orders", ["Category", "Order"], [
    ["<b>Infection</b>", "Piperacillin-tazobactam 4.5 g IV every 6 hours. Report temperature 38.0° C or higher. Private "
                         "room; neutropenic precautions."],
    ["<b>Blood products</b>", "Platelets 1 adult dose IV now and for platelets below 10 × 10<sup>9</sup>/L or bleeding. "
                              "Red blood cells 1 unit for hemoglobin below 70 g/L. All blood products irradiated and "
                              "leukoreduced. No blood from family members."],
    ["<b>Precautions</b>", "Bleeding precautions. No rectal medications or temperatures. No intramuscular injections. "
                           "No aspirin or NSAIDs."]])
s4 = screen(4, INTRO, C, select_all(541, [
    ("A", "Perform hand hygiene before and after every contact with the client", True),
    ("B", "Check the client's temperature every 4 hours and report 38.0° C or higher at once", True),
    ("C", "Provide a soft toothbrush or foam swabs and an electric razor", True),
    ("D", "Check that every blood product is labelled irradiated and leukoreduced", True),
    ("E", "Keep fresh flowers and potted plants out of the room", True),
    ("F", "Give a glycerin suppository if the client becomes constipated", False),
    ("G", "Arrange for the client's brother to donate platelets", False),
    ("H", "Give ibuprofen for the mouth pain", False)],
    rationale(
        "<b>Include:</b> hand hygiene is the most effective way to prevent infection in a neutropenic client {A}. Fever may "
        "be the only sign of infection when neutrophils are absent, so it is reported at once {B}. Soft brushes, swabs and "
        "electric razors prevent bleeding from gums and skin {C}. Irradiation prevents transfusion-associated "
        "graft-versus-host disease in clients receiving antithymocyte globulin, and leukoreduction lowers the risk of "
        "sensitization to donor cells and of cytomegalovirus transmission {D}. Flowers, plants and standing water can carry "
        "bacteria and fungi such as Aspergillus {E}.",
        "<b>Do not include:</b> suppositories, enemas and rectal temperatures can injure the rectal mucosa, causing bleeding "
        "and a portal for bacteria {F}. Blood from relatives is avoided in clients who may need a stem cell transplant, "
        "because it can sensitize them to a family donor's tissue antigens {G}. NSAIDs inhibit platelet function {H}."),
    preamble="The nurse has reviewed the Nurses' Notes from Day 1 1700 and the Orders.",
    stem="Which interventions should the nurse include in the client's plan of care? Select all that apply."))

# Screen 5
C.notes("nn", "Nurses' Notes", ("Day 4 0800",
    "The client has been afebrile for 48 hours, and blood cultures are negative. The platelet count is 18 × 10<sup>9</sup>/L "
    "after transfusion. The client starts equine antithymocyte globulin (ATG) today, daily for 4 days, with cyclosporine PO "
    "twice daily and eltrombopag PO daily. A central venous catheter is in place."))
vitals("Day 4 0800", "37.1° C", "96 beats/min", "18 breaths/min", "118/72 mm Hg", "98% on room air")
s5 = screen(5, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 4 0800 and the Vital Signs.",
    "stem": "For each nursing action, click to specify whether the action is <b>Indicated</b>, <b>Non-Essential</b>, or "
            "<b>Contraindicated</b> for the first ATG infusion.",
    "matrix": matrix_mc("Nursing Action", IMC, [
        ("Give the prescribed premedications (acetaminophen, an antihistamine and a corticosteroid) before the infusion", 0),
        ("Give the ATG as a rapid IV push to shorten the time the client is exposed to it", 2),
        ("Infuse the ATG through an in-line filter over at least 4 hours", 0),
        ("Keep epinephrine and resuscitation equipment at the bedside", 0),
        ("Weigh the client before each dose of ATG", 1),
        ("Stop the infusion and call for help if the client develops wheezing, hypotension or throat tightness", 0)]),
    "explanation": rationale(
        "<b>Indicated:</b> ATG is an animal (horse) antibody against human T cells; it removes the T cells that attack the "
        "stem cells. Because it is a foreign protein, infusion reactions (fever, chills, rash) and anaphylaxis can occur, so "
        "premedication is given, the infusion runs slowly through an in-line filter over at least 4 hours, emergency drugs "
        "and equipment are at hand, and the infusion is stopped at the first sign of anaphylaxis. Serum sickness (fever, "
        "rash, joint pain) can follow 1 to 2 weeks later.",
        "<b>Contraindicated:</b> a rapid IV push greatly increases the risk of a severe reaction.",
        "<b>Non-Essential:</b> the ATG dose is calculated from the client's weight on admission; weighing before each daily dose adds "
        "nothing to safety."),
})

# Screen 6
C.notes("nn", "Nurses' Notes", ("Month 3 1000",
    "The client attends a clinic visit 3 months after ATG. The client needed 2 platelet transfusions in the past month, "
    "compared with 6 in the first month. The client takes cyclosporine and eltrombopag and has not returned to work. The "
    "nurse reviews the client's teaching."))
vitals("Month 3 1000", "36.8° C", "84 beats/min", "16 breaths/min", "134/86 mm Hg", "99% on room air")
C.column("labs", "Laboratory Results", "Laboratory Test and Reference Range", "Month 3 0900", list(zip(
    [LAB[0], LAB[2], LAB[3], LAB[4], LAB[5]],
    ["94 g/L", "48 × 10<sup>9</sup>/L", "2.6 × 10<sup>9</sup>/L", "1.1 × 10<sup>9</sup>/L", "38 × 10<sup>9</sup>/L"])))
s6 = screen(6, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Month 3 1000, the Vital Signs, and the Laboratory Results.",
    "stem": "For each statement the client makes, click to specify whether it shows that the teaching was <b>understood</b> or "
            "that the client <b>needs further teaching</b>.",
    "matrix": matrix_mc("Client Statement", ["Understood", "Needs Further Teaching"], [
        ("“I'll go to the emergency department if my temperature is 38.0° C or higher.”", 0),
        ("“My counts are coming up, so I can stop the cyclosporine once I feel well.”", 1),
        ("“I'll keep my blood tests and check my blood pressure, because cyclosporine can affect my kidneys and "
         "blood pressure.”", 0),
        ("“I'll go back to cleaning parts with the solvent, but I'll wear gloves.”", 1),
        ("“I'll avoid grapefruit and check with the pharmacist before taking any new medicine.”", 0),
        ("“It may take several months for my blood counts to recover.”", 0)]),
    "explanation": rationale(
        "<b>Response so far:</b> neutrophils (0.3 to 1.1 × 10⁹/L), platelets (9 to 38 × 10⁹/L) and reticulocytes are "
        "rising and the client needs fewer transfusions: a partial response. About 60% to 70% of clients respond to ATG and "
        "cyclosporine, usually over 3 to 6 months, so treatment continues.",
        "<b>Understood:</b> fever is still an emergency while neutrophils are low. Cyclosporine is nephrotoxic and raises "
        "blood pressure (134/86 mm Hg today), so creatinine, cyclosporine levels and BP are checked. Grapefruit and many "
        "drugs raise cyclosporine levels. Recovery takes months.",
        "<b>Needs further teaching:</b> stopping cyclosporine early risks relapse; it is tapered only on the hematologist's "
        "instruction. Benzene is a marrow toxin absorbed through the skin and by inhalation; gloves alone do not remove "
        "the exposure, so the client should not return to that work and should discuss it with occupational health."),
})
write_case(1, 5,
    "24-year-old male with severe aplastic anemia after benzene solvent exposure: pancytopenia (anemia, neutropenia, "
    "thrombocytopenia), febrile neutropenia, neutropenic and bleeding precautions, antithymocyte globulin and cyclosporine.",
    [s1, s2, s3, s4, s5, s6],
    "New case written by Claude on 25 Nov 2026 (NURS 1021 Unit 1, batch 2); checked against Merck Manual Professional "
    "(Aplastic Anemia, Mar 2025). Please review: irradiated/leukoreduced products and avoiding family-donor blood (standard "
    "hematology practice, not on the Merck page); excluding flowers and plants (agency policies vary); ATG infusion details "
    "(premedication, in-line filter, at least 4 hours) against the product monograph and your agency.")
