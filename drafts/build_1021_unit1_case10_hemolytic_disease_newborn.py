"""NURS 1021 Unit 1 Case Study 10: Rh(D) hemolytic disease of the newborn in a second-born infant whose mother was
sensitized after her first delivery (no Rho(D) immune globulin); early jaundice, phototherapy, exchange transfusion,
prevention.
Outcome: hemolytic disease of the newborn.
Facts checked against the Merck Manual Professional Edition, "Hemolytic Disease of the Fetus and Neonate" (Apr 2024)
and "Neonatal Hyperbilirubinemia" (Nov 2026): maternal IgG crosses the placenta and lyses fetal red cells; Rh-negative
mother, Rh-positive fetus; sensitization by fetomaternal hemorrhage (delivery, abortion, trauma); the sensitizing
pregnancy is unaffected; anemia, heart failure, hydrops; indirect bilirubin -> bilirubin encephalopathy (lethargy,
poor feeding -> hypotonia, seizures, hypertonia); jaundice in the first 24 hours is pathologic; rise > 5.1 µmol/L/h in
the first 24 h is a red flag; DAT (Coombs), CBC, reticulocytes, blood group of infant and mother; prevention with
Rho(D) immune globulin 300 mcg at 28 weeks and within 72 hours after delivery of an Rh-positive infant (and after
abortion, ectopic, amniocentesis, bleeding, trauma), only if not already sensitized; titers and MCA Doppler in
sensitized pregnancies; phototherapy and exchange transfusion; water or dextrose supplements not advised.
Phototherapy nursing details (eye shields, skin exposure, feeding, temperature, light-shielded samples) are standard
newborn nursing practice; partly from the Merck summary. ABO: Merck's HDFN page says ABO incompatibility does not cause
HDFN, while the hyperbilirubinemia page lists ABO incompatibility as a cause of neonatal jaundice; the case avoids it."""
from nurs1021_common import *

INTRO = ("The nurse on the postpartum and newborn unit is caring for baby boy Okafor, born at 37 weeks by vaginal "
         "delivery 10 hours ago, and his mother, Grace, a 31-year-old G2P2 client.")
C = Chart2()
S1_NOTE = [("Day 1 1700",
    "Newborn assessment at 10 hours of age. {Skin of the face, chest and abdomen yellow; sclerae yellow.|correct} "
    "{Skin and mucous membranes pale under the jaundice.|correct} {Liver edge 3 cm below the right costal margin; spleen "
    "tip palpable.|correct} {Sleepy; needed waking for the last feed and took only 10 mL of formula with a weak suck.|correct} "
    "{Hands and feet slightly bluish; trunk pink.} {Small white papules on a red base over the chest.} {Bluish-grey "
    "patch over the lower back.} {Head slightly elongated from molding.} Mother's chart: blood group O, Rh-negative; "
    "first child born 3 years ago at home in another country; she did not receive Rho(D) immune globulin. Prenatal "
    "antibody screen this pregnancy: anti-D positive, titer 1:64. Father: Rh-positive.")]
C.notes("nn", "Nurses' Notes", *S1_NOTE)
VS = [vrow("T (axillary)", "Newborn: 36.5–37.5° C"), vrow("P", "Newborn: 110–160 beats/min"),
      vrow("RR", "Newborn: 30–60 breaths/min"), vrow(SPO2)]


def vitals(col, *v):
    C.column("vs", "Vital Signs", "", col, list(zip(VS, v)))


vitals("Day 1 1700", "36.8° C", "164 beats/min", "56 breaths/min", "97% on room air")
s1 = screen(1, INTRO, C, {
    "type": "highlight",
    "stem": "The nurse reviews the Nurses' Notes. <b>Highlight</b> the newborn findings that require follow-up.",
    "options": [],
    "highlightTabs": [highlight_tab("ht1", "Nurses' Notes", S1_NOTE)],
    "maxCorrectSelections": None,
    "explanation": rationale(
        "<b>Require follow-up:</b> jaundice that appears in the <b>first 24 hours</b> is pathologic until proven "
        "otherwise; physiologic jaundice appears after the first day. Here maternal antibodies are destroying the baby's "
        "red cells (hemolysis), releasing unconjugated bilirubin faster than the immature liver can conjugate it. Pallor "
        "reflects anemia from hemolysis. The liver and spleen enlarge as they remove damaged cells and make new ones "
        "(extramedullary hematopoiesis). Sleepiness, poor feeding and a weak suck can be early signs of bilirubin "
        "affecting the brain (acute bilirubin encephalopathy) and need urgent assessment.",
        "<b>Expected newborn findings:</b> bluish hands and feet with a pink trunk (acrocyanosis) in the first day, "
        "erythema toxicum (white papules on a red base), congenital dermal melanocytosis over the lower back, and molding "
        "of the head after vaginal birth.",
        "<b>History:</b> an Rh-negative mother, an Rh-positive father, no Rho(D) immune globulin after the first birth and "
        "an anti-D titer of 1:64 (critical titers are usually 1:8 to 1:32) explain the findings."),
})

# Screen 2
C.notes("nn", "Nurses' Notes", ("Day 1 1745",
    "Results called to the pediatrician. Grace asks, “Why is this baby sick when my first baby was fine?”"))
LAB = ["<b>Blood group (newborn)</b>", lab("Direct antiglobulin test (DAT, direct Coombs)", "Negative"),
       lab("Hemoglobin (Hgb)", "Newborn: 140–220 g/L"), lab("Reticulocyte percentage", "Newborn: 3%–7%"),
       lab("Bilirubin, total", "See hour-specific chart"), lab("Bilirubin, direct (conjugated)", "2–9 µmol/L"),
       lab("Glucose", "Newborn: 2.6 mmol/L or higher")]
C.column("labs", "Laboratory Results", "Laboratory Test and Reference Range", "Day 1 1715 (10 h)", list(zip(LAB, [
    "O, Rh-positive", "Positive", "118 g/L", "14%", "176 µmol/L", "8 µmol/L", "3.4 mmol/L"])))
s2 = screen(2, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 1 1745 and the Laboratory Results.",
    "stem": "For each finding, click to specify whether it is <b>expected</b> for a healthy newborn or <b>supports "
            "hemolytic disease of the newborn</b>.",
    "matrix": matrix_mc("Finding", ["Expected for a Healthy Newborn", "Supports Hemolytic Disease of the Newborn"], [
        ("Positive direct antiglobulin (Coombs) test", 1),
        ("Glucose 3.4 mmol/L", 0),
        ("Hemoglobin 118 g/L", 1),
        ("Direct (conjugated) bilirubin 8 µmol/L", 0),
        ("Reticulocytes 14%", 1),
        ("Total bilirubin 176 µmol/L at 10 hours of age", 1)]),
    "explanation": rationale(
        "<b>Pathogenesis (answering Grace):</b> during her first delivery, some of the baby's Rh-positive red cells "
        "entered her circulation. Her immune system made anti-D antibodies; the first baby was born before that response "
        "developed and was not affected. In this pregnancy, her IgG anti-D crossed the placenta, coated the baby's "
        "Rh-positive red cells and caused their destruction. A dose of Rho(D) immune globulin within 72 hours of the first "
        "birth would most likely have prevented the sensitization.",
        "<b>Supports hemolytic disease:</b> a positive DAT shows maternal antibody on the baby's red cells. Hemoglobin of "
        "118 g/L is low for a newborn (anemia from hemolysis), and 14% reticulocytes show the marrow trying to replace "
        "the cells. A total bilirubin of 176 µmol/L at 10 hours is far above expected for that age and, with a known "
        "hemolytic cause, is above the phototherapy threshold.",
        "<b>Expected:</b> direct bilirubin is normal: the problem is overproduction of <b>unconjugated</b> bilirubin, not "
        "liver or bile duct disease. Glucose is normal."),
})

# Screen 3
C.notes("nn", "Nurses' Notes", ("Day 1 2300",
    "Repeat bilirubin drawn at 16 hours. Baby fed 15 mL; still sleepy but rouses to handling."))
C.column("labs", "Laboratory Results", "Laboratory Test and Reference Range", "Day 1 2300 (16 h)", list(zip(
    [LAB[4]], ["224 µmol/L"])))
s3 = screen(3, INTRO, C, {
    "type": "dropdown_cloze",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 1 2300 and the Laboratory Results.",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {"text": "The baby's bilirubin rose by about [[drop0]] over 6 hours, which shows [[drop1]]. The nurse's "
                      "priority is preventing [[drop2]].",
              "dropdowns": [
                  dd(1031, "8 µmol/L per hour", "2 µmol/L per hour", "20 µmol/L per hour", "0.5 µmol/L per hour"),
                  dd(1032, "rapid, ongoing hemolysis", "normal physiologic jaundice",
                     "jaundice from breastfeeding", "an obstruction of the bile ducts"),
                  dd(1033, "brain damage from unconjugated bilirubin (kernicterus)", "hypoglycemia",
                     "hypothermia", "infection of the umbilical cord")]},
    "explanation": rationale(
        "<b>Rate of rise:</b> 176 to 224 µmol/L in 6 hours is 48 µmol/L, or 8 µmol/L per hour. A rise faster than about "
        "5 µmol/L per hour in the first 24 hours is a red flag for hemolysis.",
        "<b>Meaning:</b> physiologic jaundice begins after 24 hours and rises slowly; breastfeeding jaundice appears in the "
        "first week with poor intake (this baby is formula-fed); bile duct obstruction raises <b>conjugated</b> bilirubin, "
        "which is normal here.",
        "<b>Priority:</b> unconjugated bilirubin is fat-soluble; when it exceeds the binding capacity of albumin it crosses "
        "the blood-brain barrier and deposits in the basal ganglia and brainstem. Early signs are lethargy and poor "
        "feeding, progressing to high-pitched cry, hypotonia then hypertonia and arching, seizures and permanent damage "
        "(kernicterus: cerebral palsy, hearing loss). Late-preterm birth (37 weeks) and hemolysis increase the risk."),
})

# Screen 4
C.notes("nn", "Nurses' Notes", ("Day 1 2330",
    "Pediatrician orders intensive phototherapy and transfer to the neonatal intensive care unit. Grace asks how she can "
    "help care for her baby."))
C.rows("orders", "Orders", ["Category", "Order"], [
    ["<b>Phototherapy</b>", "Intensive LED phototherapy, continuous. Interrupt only briefly for feeds."],
    ["<b>Bilirubin</b>", "Serum total bilirubin every 4 hours. Exchange transfusion if bilirubin reaches the exchange "
                         "threshold on the hour-specific chart or signs of encephalopathy appear."],
    ["<b>Feeding</b>", "Formula 30 to 45 mL every 3 hours. Strict intake and output; weigh daily."],
    ["<b>Blood bank</b>", "Crossmatch O Rh-negative red cells, compatible with the mother's plasma, for possible exchange "
                          "transfusion."]])
s4 = screen(4, INTRO, C, select_all(1041, [
    ("A", "Cover the baby's eyes with eye shields while the lights are on", True),
    ("B", "Undress the baby except for a diaper to expose as much skin as possible", True),
    ("C", "Check the baby's temperature at least every 3 to 4 hours", True),
    ("D", "Feed every 3 hours and record wet diapers and stools", True),
    ("E", "Protect each bilirubin sample from light", True),
    ("F", "Apply lotion to the skin to prevent drying under the lights", False),
    ("G", "Give glucose water between feeds to flush out the bilirubin", False),
    ("H", "Judge the response by how yellow the baby's skin looks", False)],
    rationale(
        "<b>Include:</b> blue-green light changes bilirubin in the skin into water-soluble forms excreted in bile and urine "
        "without conjugation. Eyes are shielded to protect the retina {A}. Maximal skin exposure increases the dose of "
        "light {B}. Phototherapy can cause overheating or heat loss, so temperature is monitored {C}. Feeding promotes "
        "stooling (bilirubin leaves in stool) and replaces increased insensible water loss; loose green stools are expected "
        "{D}. Bilirubin breaks down in light, so samples are shielded to avoid falsely low results {E}.",
        "<b>Do not include:</b> lotions and oils can cause burns under the lights {F}. Water or dextrose does not lower "
        "bilirubin and displaces milk, which is needed for stooling {G}. Phototherapy bleaches the skin while serum "
        "bilirubin can remain high, so the response is judged by serum bilirubin, not skin color {H}."),
    preamble="The nurse has reviewed the Nurses' Notes from Day 1 2330 and the Orders.",
    stem="Which interventions should the nurse include in the baby's plan of care? Select all that apply."))

# Screen 5
C.notes("nn", "Nurses' Notes", ("Day 2 0700",
    "Baby in the NICU under intensive phototherapy. Bilirubin still rising. Difficult to rouse; poor suck. High-pitched "
    "cry when handled. Neonatologist plans an exchange transfusion through an umbilical venous catheter."))
vitals("Day 2 0700", "37.1° C", "172 beats/min", "58 breaths/min", "96% on room air")
C.column("labs", "Laboratory Results", "Laboratory Test and Reference Range", "Day 2 0300 (20 h)", list(zip(
    [LAB[4]], ["262 µmol/L"])))
C.column("labs", "Laboratory Results", "Laboratory Test and Reference Range", "Day 2 0700 (24 h)", list(zip(
    [LAB[2], LAB[4]], ["104 g/L", "294 µmol/L"])))
s5 = screen(5, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 2 0700, the Vital Signs, and the Laboratory Results.",
    "stem": "For each nursing action, click to specify whether the action is <b>Indicated</b>, <b>Non-Essential</b>, or "
            "<b>Contraindicated</b> while the exchange transfusion is prepared.",
    "matrix": matrix_mc("Nursing Action", IMC, [
        ("Continue intensive phototherapy until the exchange transfusion begins", 0),
        ("Turn off the phototherapy to observe the baby's skin color", 2),
        ("Report the high-pitched cry and difficulty rousing to the neonatologist at once", 0),
        ("Place the baby on a cardiorespiratory monitor and keep him warm under a radiant warmer", 0),
        ("Give the baby Rho(D) immune globulin", 2),
        ("Repeat the direct antiglobulin test before the exchange", 1)]),
    "explanation": rationale(
        "<b>Indicated:</b> phototherapy continues to lower bilirubin while blood is prepared. A high-pitched cry, poor suck "
        "and difficulty rousing are signs of acute bilirubin encephalopathy: urgent exchange transfusion can prevent "
        "permanent damage. An exchange transfusion replaces about twice the baby's blood volume in small aliquots, "
        "removing bilirubin and antibody-coated cells and correcting anemia; heart rate, breathing, temperature, glucose "
        "and calcium are monitored closely.",
        "<b>Contraindicated:</b> stopping phototherapy lets bilirubin rise further; skin color does not reflect serum "
        "bilirubin. Rho(D) immune globulin is given to Rh-negative <b>mothers</b> to prevent sensitization; it is never "
        "given to an Rh-positive baby, whose red cells it would destroy.",
        "<b>Non-Essential:</b> the DAT is already positive and will not change management."),
})

# Screen 6
C.notes("nn", "Nurses' Notes",
    ("Day 2 1300", "Exchange transfusion completed without complications. Bilirubin 158 µmol/L; hemoglobin 148 g/L."),
    ("Day 6 1000", "Phototherapy stopped on day 4; bilirubin stable. Alert, feeding well, normal tone and cry. Hearing "
     "screen (automated brainstem response) passed. The nurse reviews discharge and future-pregnancy teaching with "
     "Grace."))
C.column("labs", "Laboratory Results", "Laboratory Test and Reference Range", "Day 6 0600", list(zip(
    [LAB[2], LAB[3], LAB[4]], ["132 g/L", "6%", "142 µmol/L"])))
s6 = screen(6, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 2 1300 and Day 6 1000 and the Laboratory Results.",
    "stem": "For each statement Grace makes, click to specify whether it shows that the teaching was <b>understood</b> or "
            "that she <b>needs further teaching</b>.",
    "matrix": matrix_mc("Client Statement", ["Understood", "Needs Further Teaching"], [
        ("“Rho(D) immune globulin won't help me now, because I already have the antibodies.”", 0),
        ("“In my next pregnancy, I'll have antibody tests and ultrasounds to check the baby for anemia.”", 0),
        ("“Our next baby will be fine, because the problem came from this pregnancy.”", 1),
        ("“The baby needs blood tests over the next few weeks, because he can still become anemic.”", 0),
        ("“If my baby turns yellow again, we'll just put him in the sunlight at home.”", 1),
        ("“My sister is Rh-negative too, so she should ask about the immune globulin in her pregnancy.”", 0)]),
    "explanation": rationale(
        "<b>Understood:</b> Rho(D) immune globulin prevents sensitization (given at 28 weeks and within 72 hours after the "
        "birth of an Rh-positive baby, and after bleeding, trauma, amniocentesis, miscarriage or ectopic pregnancy); once "
        "antibodies exist, it cannot remove them. In later pregnancies the antibody titer is followed and, above the "
        "critical titer, middle cerebral artery Doppler ultrasound detects fetal anemia, which can be treated with "
        "intrauterine transfusion. Maternal antibodies keep destroying the baby's cells for weeks, so late anemia is "
        "watched for. An unsensitized Rh-negative relative benefits from prophylaxis.",
        "<b>Needs further teaching:</b> sensitization is permanent and the disease usually becomes more severe with each "
        "Rh-positive pregnancy. Sunlight is not a safe or measurable treatment and can burn or overheat a baby; returning "
        "jaundice, poor feeding or sleepiness need prompt assessment."),
})
write_case(1, 10,
    "Newborn with Rh(D) hemolytic disease (mother sensitized after her first birth without Rho(D) immune globulin): early "
    "jaundice, anemia, rising bilirubin, phototherapy, signs of bilirubin encephalopathy, exchange transfusion and "
    "prevention.",
    [s1, s2, s3, s4, s5, s6],
    "New case written by Claude on 25 Nov 2026 (NURS 1021 Unit 1, batch 3); checked against Merck Manual Professional "
    "(Hemolytic Disease of the Fetus and Neonate, Apr 2024; Neonatal Hyperbilirubinemia, Nov 2026). Please review: "
    "newborn reference ranges (hemoglobin 140–220 g/L, reticulocytes 3%–7%, glucose ≥ 2.6 mmol/L, vital signs); bilirubin "
    "values against the hour-specific phototherapy/exchange chart your program uses (no thresholds are quoted in the "
    "case); phototherapy nursing points (standard practice); this is a maternal-newborn topic within a med-surg unit.")
