"""Builds 19 stand-alone items (Items 13-31) from the NCSBN NCLEX-RN Next Generation Exam
Preview PDF (c 2022 NCSBN, https://www.nclex.com/prepare.page), second attachment (Test2.pdf,
19 pages). Same conventions as build_ncsbn_preview_standalone.py (first 6 items): every item
carries the NCSBN copyright question.footnote; items with no matching NURS 1017/1021 unit go
to course/unit "Others" per the user's standing instruction to classify them later.

The source PDF has NO published answer key for any of these 19 items -- every correct answer
and rationale below is this session's own clinical judgment applied to the transcribed stems,
NOT a verified key. ALL 19 items need clinician review before publishing. A subset (noted
inline) involve genuinely close comparative-prioritization calls where a second clinical
opinion matters most: items 14, 15, 19, 20, and 21.
"""
import json
import os
import re

DRAFTS_DIR = os.path.dirname(os.path.abspath(__file__))

FOOTNOTE = (
    "&copy; NCSBN. Taken from https://www.nclex.com/prepare.page; "
    "click on &#39;Download Exam Preview&#39;."
)


def opts(*pairs):
    return [{"text": t, "correct": c} for t, c in pairs]


def screen(question, image=None):
    q = dict(question)
    q.setdefault("footnote", FOOTNOTE)
    if image is not None:
        q["questionImage"] = image
    return [{"step": 1, "question": q, "leftContent": {"intro": "", "tabs": []}}]


def base_item(item_id, title, course, unit, screens):
    return {
        "id": item_id, "title": title, "course": course, "unit": unit,
        "topic": unit, "disorder": unit, "isStandalone": True, "screens": screens,
    }


def slug(text):
    text = re.sub(r"[':]", "", text)
    text = re.sub(r"[^A-Za-z0-9]+", "_", text)
    return re.sub(r"_+", "_", text).strip("_")


def write_draft(item):
    path = os.path.join(DRAFTS_DIR, f"{item['id']}_{slug(item['title'])}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(item, f, indent=2, ensure_ascii=False)
    print("wrote", path)


items = []

# ---------------------------------------------------------------------------
# Item 13 -- Positive pressure ventilation teaching -> NURS 1021 Unit 3 (Respiratory)
# ---------------------------------------------------------------------------
items.append(base_item(
    "standalone_1784030000001",
    "Unit 3 Stand-alone 1: Positive Pressure Ventilation Client Teaching",
    "NURS 1021", "Unit 3 (Respiratory Disorders)",
    screen({
        "stem": "Which of the following statements by the nurse would indicate a correct understanding of the teaching?",
        "type": "multiple_choice",
        "preamble": "The nurse has attended a staff education program about caring for clients who are receiving positive pressure mechanical ventilation.",
        "options": opts(
            ("“Clients should avoid range-of-motion (ROM) exercises until weaned from ventilation.”", False),
            ("“Clients may develop stress ulcers and gastrointestinal bleeding.”", True),
            ("“Clients will be chemically paralyzed to improve oxygenation.”", False),
            ("“Clients will experience diuresis and polyuria.”", False),
        ),
        "explanation": (
            "Mechanically ventilated clients are at risk for stress ulcers and gastrointestinal bleeding "
            "(Option 2) due to the physiologic stress of critical illness; stress-ulcer prophylaxis "
            "(e.g., a proton pump inhibitor or H2 blocker) is standard care. ROM exercises (Option 1) "
            "should continue, not be avoided, to prevent contractures, pressure injury, and venous "
            "thromboembolism during ventilation. Chemical paralysis (Option 3) is reserved for specific "
            "situations such as severe ventilator dyssynchrony or ARDS, not a routine expectation for "
            "every ventilated client. Positive pressure ventilation decreases venous return and cardiac "
            "output, which activates the renin-angiotensin-aldosterone system and typically causes fluid "
            "retention and decreased urine output, not diuresis and polyuria (Option 4)."
        ),
    }),
))

# ---------------------------------------------------------------------------
# Item 14 -- Unit transfer appropriateness -> Others
# ---------------------------------------------------------------------------
items.append(base_item(
    "standalone_1790300000003",
    "Care Prioritization - Unit Transfer Appropriateness (MCQ)",
    "Others", "Others",
    screen({
        "stem": "It would be most appropriate for the nurse to transfer the client who is",
        "type": "multiple_choice",
        "preamble": "The charge nurse must transfer a female client from the medical-surgical unit to the maternity unit to make a bed available.",
        "options": opts(
            ("28 years old, had a right mastectomy and has a closed-wound drainage system", False),
            ("49 years old, has diabetes mellitus (type 2) and has begun receiving insulin", False),
            ("56 years old, has hepatitis C (HCV), and has been afebrile for 24 hours", True),
            ("70 years old, has a fractured left tibia and had an external fixation device applied 48 hours ago", False),
        ),
        "explanation": (
            "The client with hepatitis C who has been afebrile for 24 hours (Option 3) is the most "
            "stable and has the least complex ongoing nursing needs: HCV is a bloodborne pathogen "
            "requiring only standard precautions (not a transmission risk to postpartum clients or "
            "newborns through casual contact), and being afebrile indicates no acute infectious process. "
            "The client recovering from a mastectomy with a closed-wound drainage system (Option 1) "
            "needs surgical drain management. The client newly started on insulin (Option 2) needs close "
            "glucose monitoring and hypoglycemia assessment as the regimen is titrated. The client with a "
            "recently applied external fixation device (Option 4) needs pin-site care and neurovascular "
            "monitoring; maternity unit staff are not positioned to provide this specialized medical-"
            "surgical monitoring as safely as a med-surg unit can."
        ),
    }),
))

# ---------------------------------------------------------------------------
# Item 15 -- First assess across 4 client situations -> Others
# ---------------------------------------------------------------------------
items.append(base_item(
    "standalone_1790300000004",
    "Care Prioritization - First Assessment Across Client Situations (MCQ)",
    "Others", "Others",
    screen({
        "stem": "The nurse should <b>first</b> assess the client with",
        "type": "multiple_choice",
        "preamble": "The nurse has been made aware of the following client situations.",
        "options": opts(
            ("heart failure who has a productive cough and is anxious", False),
            ("regional enteritis (Crohn's disease) who is reporting cramping abdominal pain and diarrhea", False),
            ("idiopathic thrombocytopenic purpura (ITP) who has petechiae on the trunk and is reporting heavy menses", False),
            ("chronic obstructive pulmonary disease (COPD) who has dyspnea with exertion and is using accessory muscles to breathe", True),
        ),
        "explanation": (
            "Use of accessory muscles to breathe (Option 4) is an ominous sign of significantly increased "
            "work of breathing and impending respiratory failure, making this client the priority to "
            "assess first. A productive cough and anxiety in a client with heart failure (Option 1) can "
            "reflect early pulmonary congestion but is a less acute presentation than active accessory "
            "muscle use. Cramping and diarrhea (Option 2) are expected exacerbation symptoms of Crohn's "
            "disease. Petechiae and heavy menses in a client with ITP (Option 3) reflect the client's "
            "known thrombocytopenia and warrant follow-up but are not as immediately life-threatening as "
            "a client showing active signs of respiratory decompensation."
        ),
    }),
))

# ---------------------------------------------------------------------------
# Item 16 -- Appropriate UAP task delegation -> Others
# ---------------------------------------------------------------------------
items.append(base_item(
    "standalone_1790300000005",
    "Delegation - Appropriate UAP Task Assignment (MCQ)",
    "Others", "Others",
    screen({
        "stem": "Which of the following tasks would be appropriate for the nurse to assign to UAP?",
        "type": "multiple_choice",
        "preamble": "The nurse and unlicensed assistive personnel (UAP) are caring for assigned clients.",
        "options": opts(
            ("assisting a client with atrial fibrillation to shower", True),
            ("checking the ability of a client to swallow water after a transesophageal echocardiogram (TEE)", False),
            ("observing while a client with dysphagia begins a thickened liquid diet", False),
            ("transporting a client with respiratory distress to the radiology department for a chest radiograph", False),
        ),
        "explanation": (
            "Assisting a stable client with a basic activity of daily living such as showering (Option 1) "
            "is within the scope of UAP practice and does not require nursing assessment or clinical "
            "judgment; atrial fibrillation alone does not change this. Checking a client's ability to "
            "swallow water after a TEE (Option 2) is a clinical swallow screen assessing for post-"
            "procedure aspiration risk and requires a licensed nurse's judgment. Observing a client with "
            "known dysphagia as they begin a new thickened liquid consistency (Option 3) similarly "
            "requires skilled assessment for aspiration. Transporting a client who is in respiratory "
            "distress (Option 4) requires a licensed staff member who can monitor for and respond to "
            "deterioration en route."
        ),
    }),
))

# ---------------------------------------------------------------------------
# Item 17 -- Infant nutrition follow-up -> Others
# ---------------------------------------------------------------------------
items.append(base_item(
    "standalone_1790300000006",
    "Pediatric Nutrition - Infant Feeding Pattern Follow-up (MCQ)",
    "Others", "Others",
    screen({
        "stem": "It would be a priority for the nurse to follow up with the",
        "type": "multiple_choice",
        "preamble": "The nurse has taken a nutritional history from parents of clients.",
        "options": opts(
            ("5-month-old client whose only source of nutrition is 5 formula feedings daily", False),
            ("7-month-old client who eats several crackers as finger food", False),
            ("9-month-old client whose typical daily diet includes 10 bottles of 2% milk, 1 cup of apple juice, and 3 servings of infant cereal", True),
            ("1-year-old client whose typical food intake includes 4 breast-feedings and 3 servings of cooked vegetables, pears, or sliced cheese", False),
        ),
        "explanation": (
            "The 9-month-old's diet (Option 3) requires follow-up for 2 reasons: 2% (reduced-fat) cow's "
            "milk is not recommended before 12 months of age, and 10 bottles per day is an excessive "
            "volume that can displace iron-rich solid foods and increase the risk of iron-deficiency "
            "(“milk”) anemia. Exclusive formula feeding at 5 months (Option 1) is developmentally "
            "appropriate, since solids are not introduced until around 6 months. Introducing finger foods "
            "such as crackers at 7 months (Option 2) is developmentally appropriate. A 1-year-old eating "
            "breast milk along with a variety of vegetables, fruit, and cheese (Option 4) reflects an "
            "appropriately varied diet for that age."
        ),
    }),
))

# ---------------------------------------------------------------------------
# Item 18 -- Privacy violation -> Others
# ---------------------------------------------------------------------------
items.append(base_item(
    "standalone_1790300000007",
    "Legal-Ethical - Client Privacy Violation (MCQ)",
    "Others", "Others",
    screen({
        "stem": "Which of the following scenarios should the nurse include as an example of a violation of client privacy?",
        "type": "multiple_choice",
        "preamble": "The nurse is planning a staff education program about client privacy.",
        "options": opts(
            ("discussing with an unlicensed assistive personnel (UAP) that the UAP's assigned client will require a smaller condom catheter", False),
            ("sharing the client's blood alcohol level (BAL) test result with the police officer who brought the client to the emergency department (ED)", True),
            ("responding to the call light of the client who is assigned to another nurse and needs assistance in the bathroom", False),
            ("allowing a nursing student who has been assigned to the client to review the client's medical record", False),
        ),
        "explanation": (
            "Sharing a client's blood alcohol level with a police officer without the client's consent or "
            "proper legal authority such as a warrant or a specific legal exception (Option 2) is a "
            "privacy violation; law enforcement is not automatically entitled to protected health "
            "information. Discussing a care need with the UAP assigned to that same client (Option 1) is "
            "appropriate, need-to-know care coordination. Responding to another nurse's client's call "
            "light for bathroom assistance (Option 3) is appropriate teamwork, not a privacy breach. A "
            "nursing student assigned to a client's care reviewing that client's record (Option 4) is a "
            "normal, permitted part of clinical education and the care team's access to the record."
        ),
    }),
))

# ---------------------------------------------------------------------------
# Item 19 -- First assess after thoracic surgery -> NURS 1021 Unit 3 (Respiratory)
# ---------------------------------------------------------------------------
items.append(base_item(
    "standalone_1784030000002",
    "Unit 3 Stand-alone 2: Priority Assessment After Thoracic Surgery",
    "NURS 1021", "Unit 3 (Respiratory Disorders)",
    screen({
        "stem": "The nurse should <b>first</b> assess the client",
        "type": "multiple_choice",
        "preamble": "The nurse has become aware of the following client situations.",
        "options": opts(
            ("who had a right pneumonectomy 24 hours ago and is in the high-Fowler's position while lying on the right side", False),
            ("with chronic obstructive pulmonary disease (COPD) who is using pursed-lip breathing and reporting hemoptysis", True),
            ("who had a wedge resection of the left lung 24 hours ago and is sitting in the high-Fowler's position", False),
            ("with heart failure who has a productive cough and is restless", False),
        ),
        "explanation": (
            "Hemoptysis (Option 2) is a new, objective finding that is never an expected part of a COPD "
            "client's baseline presentation and can signal a serious complication such as infection, "
            "pulmonary embolism, or malignancy; it requires the most urgent assessment. Positioning on "
            "the operative (right) side in the high-Fowler's position after a right pneumonectomy "
            "(Option 1) is the expected, correct post-pneumonectomy position, since it allows the "
            "remaining lung to expand and prevents fluid from draining toward it. Sitting upright after a "
            "wedge resection (Option 3) is also the expected position to maximize lung expansion. A "
            "productive cough and restlessness in a client with heart failure (Option 4) can reflect "
            "pulmonary congestion and warrants follow-up but is a less acute, objectively alarming finding "
            "than new hemoptysis."
        ),
    }),
))

# ---------------------------------------------------------------------------
# Item 20 -- Pediatric concussion observation significance -> Others
# ---------------------------------------------------------------------------
items.append(base_item(
    "standalone_1790300000008",
    "Pediatric Neuro - Concussion Observation Significance (MCQ)",
    "Others", "Others",
    screen({
        "stem": "Which of the following observations would be most significant for the nurse to report to the oncoming shift?",
        "type": "multiple_choice",
        "preamble": "The nurse is caring for a 3-year-old client with a cerebral concussion who is being observed overnight in the pediatric unit.",
        "options": opts(
            ("The client has a blood pressure of 84/58 mm Hg and an apical pulse of 90.", False),
            ("The client is sleeping but is easily aroused.", True),
            ("The client's pupils are equal and reactive to light.", False),
            ("The client has an axillary temperature of 99.0° F (37.2° C) and respirations of 24.", False),
        ),
        "explanation": (
            "Level of consciousness and arousability are the central parameters tracked during concussion "
            "observation, since a change in either is the earliest and most sensitive sign of "
            "deterioration such as an expanding intracranial bleed. Precisely reporting that the client is "
            "“sleeping but easily aroused” (Option 2) gives the oncoming shift the exact "
            "baseline needed to detect any subsequent decline in arousability, which is more clinically "
            "significant to hand off than the other findings listed. The blood pressure and pulse "
            "(Option 1), pupil findings (Option 3), and temperature and respirations (Option 4) in this "
            "scenario are each within a broadly expected range for a 3-year-old and do not by themselves "
            "signal a change in neurologic status."
        ),
    }),
))

# ---------------------------------------------------------------------------
# Item 21 -- Same-day surgery first assessment -> Others
# ---------------------------------------------------------------------------
items.append(base_item(
    "standalone_1790300000009",
    "Care Prioritization - Same-Day Surgery First Assessment (MCQ)",
    "Others", "Others",
    screen({
        "stem": "The nurse should <b>first</b> see the client who had",
        "type": "multiple_choice",
        "preamble": "The nurse in the same-day surgical center has received a change-of-shift report on the following clients.",
        "options": opts(
            ("closed reduction of a fractured tibia with cast application 1 hour ago and is reporting that the casted leg feels hot", True),
            ("extraction of a cataract lens 2 hours ago and is reporting nausea", False),
            ("an arthroscopy of the right knee 3 hours ago and is reporting knee pain rated as 4 on a scale of 0 (no pain) to 10 (severe pain)", False),
            ("a laparoscopic cholecystectomy 4 hours ago and is reporting right shoulder pain", False),
        ),
        "explanation": (
            "A casted extremity that feels hot only 1 hour after cast application (Option 1) is a red "
            "flag for acute compartment syndrome, a limb-threatening emergency that develops as swelling "
            "occurs under a rigid cast in the first hours after application, and requires the most urgent "
            "assessment (checking the 5 P's, and cast tightness). Nausea after cataract surgery (Option 2) "
            "matters because vomiting can transiently raise intraocular pressure, but it is more readily "
            "managed with an antiemetic than a possible compartment syndrome is. Knee pain rated 4/10 3 "
            "hours after arthroscopy (Option 3) is mild, well-controlled pain and is a reassuring finding. "
            "Right shoulder pain after a laparoscopic cholecystectomy (Option 4) is expected, benign "
            "referred pain from diaphragmatic irritation caused by residual carbon dioxide used to "
            "insufflate the abdomen during the procedure."
        ),
    }),
))

# ---------------------------------------------------------------------------
# Item 22 -- MS ataxia care planning -> NURS 1017 Unit 7 (Neurological)
# ---------------------------------------------------------------------------
items.append(base_item(
    "standalone_1783070000003",
    "Unit 7 Stand-alone 3: Multiple Sclerosis Ataxia Care Planning",
    "NURS 1017", "Unit 7 (Neurological Disorders)",
    screen({
        "stem": "Which of the following interventions should the nurse include in the client's plan of care?",
        "type": "multiple_choice",
        "preamble": "The nurse is planning care for a client with multiple sclerosis (MS) who has ataxia.",
        "options": opts(
            ("Add thickener to thin liquids for the client.", False),
            ("Obtain a referral to a physical therapist for the client.", True),
            ("Face the client directly when speaking with the client.", False),
            ("Provide a board with pictures to help the client communicate needs.", False),
        ),
        "explanation": (
            "Ataxia in MS reflects impaired coordination and balance from cerebellar or proprioceptive "
            "pathway involvement, and a physical therapy referral (Option 2) is the appropriate "
            "intervention to address gait, balance, and coordination training and reduce fall risk. "
            "Adding thickener to liquids (Option 1) addresses dysphagia, a different MS symptom not "
            "described here. Facing the client directly when speaking (Option 3) is an intervention for "
            "hearing loss or receptive communication difficulty, not ataxia. A picture communication board "
            "(Option 4) addresses expressive communication impairment (such as from dysarthria or "
            "aphasia), not a coordination/balance problem."
        ),
    }),
))

# ---------------------------------------------------------------------------
# Item 23 -- Home-health first visit -> Others
# ---------------------------------------------------------------------------
items.append(base_item(
    "standalone_1790300000010",
    "Care Prioritization - Home-Health First Visit (MCQ)",
    "Others", "Others",
    screen({
        "stem": "The nurse should <b>first</b> visit the client with",
        "type": "multiple_choice",
        "preamble": "The home-health nurse is assigned to visit the following clients who live within 3 miles (4.8 km) of one another.",
        "options": opts(
            ("breast cancer who had a mastectomy 2 days ago and has had 25 mL of drainage from the closed-wound drainage system in the past 12 hours", False),
            ("lung cancer who received a dose of chemotherapy 2 weeks ago and has a temperature of 101.1° F (38.4° C)", True),
            ("chronic obstructive pulmonary disease (COPD) who is reporting expectorating large amounts of thick, yellow mucus", False),
            ("diabetes mellitus (type 1) who had a right below-the-knee amputation (BKA) and is reporting right toe pain", False),
        ),
        "explanation": (
            "A fever in a client who received chemotherapy within the past 2 to 3 weeks (Option 2) is a "
            "medical emergency until proven otherwise, since chemotherapy-induced neutropenia leaves the "
            "client unable to mount a normal immune response and febrile neutropenia can progress rapidly "
            "to sepsis; this client must be seen first. A drainage volume of about 25 mL over 12 hours "
            "from a mastectomy drain (Option 1) is within the expected, gradually decreasing range for a "
            "closed-wound drainage system. Thick, yellow sputum in a client with COPD (Option 3) suggests "
            "a possible infection or exacerbation and needs follow-up but is not immediately "
            "life-threatening. Right toe pain after a right below-the-knee amputation (Option 4) most "
            "likely represents phantom limb pain, a real and important symptom to manage but not an "
            "emergency."
        ),
    }),
))

# ---------------------------------------------------------------------------
# Item 24 -- First assess across 4 client situations 2 -> Others
# ---------------------------------------------------------------------------
items.append(base_item(
    "standalone_1790300000011",
    "Care Prioritization - First Assessment Across Client Situations 2 (MCQ)",
    "Others", "Others",
    screen({
        "stem": "The nurse should <b>first</b> assess the client",
        "type": "multiple_choice",
        "preamble": "The nurse has become aware of the following client situations.",
        "options": opts(
            ("who had a total abdominal hysterectomy (TAH) 1 day ago and is unable to void 7 hours after the indwelling urethral catheter was removed", False),
            ("who had a total knee replacement 24 hours ago", False),
            ("with bacterial pneumonia who has bronchial breath sounds auscultated between the scapulae and a temperature of 103.3° F (39.6° C)", True),
            ("with hepatic cirrhosis who has an elevated aspartate aminotransferase (AST) level and respirations of 24", False),
        ),
        "explanation": (
            "Bronchial breath sounds heard over a peripheral lung field (between the scapulae, rather "
            "than over the large airways where they are normally heard) indicate lung consolidation, and "
            "combined with a high fever, this client (Option 3) shows signs of a worsening infection with "
            "risk for respiratory decompensation or sepsis, making this the priority. Urinary retention 7 "
            "hours after catheter removal (Option 1) is uncomfortable and needs intervention (such as a "
            "straight catheterization) but is not immediately life-threatening. A client 24 hours after an "
            "uncomplicated total knee replacement with no other findings reported (Option 2) is the most "
            "stable of the group. An elevated AST is an expected, chronic finding in hepatic cirrhosis "
            "rather than a new acute change, and a respiratory rate of 24 (Option 4) is only mildly "
            "elevated."
        ),
    }),
))

# ---------------------------------------------------------------------------
# Item 25 -- Pertussis care planning -> Others
# ---------------------------------------------------------------------------
items.append(base_item(
    "standalone_1790300000012",
    "Infection Control - Pertussis Care Planning (MCQ)",
    "Others", "Others",
    screen({
        "stem": "Which of the following interventions should the nurse include in the client's plan of care?",
        "type": "multiple_choice",
        "preamble": "The nurse is planning care for a pediatric client being admitted with pertussis.",
        "options": opts(
            ("Keep the client NPO.", False),
            ("Place a dehumidifier in the client's room.", False),
            ("Encourage the client to ambulate frequently.", False),
            ("Implement droplet precautions.", True),
        ),
        "explanation": (
            "Pertussis (Bordetella pertussis) is transmitted by respiratory droplets, so droplet "
            "precautions (Option 4) are the correct, standard isolation precaution. There is no reason to "
            "keep the client NPO (Option 1); oral intake is not restricted for pertussis. A humidifier, "
            "not a dehumidifier (Option 2), helps loosen respiratory secretions; dry air from a "
            "dehumidifier can worsen airway irritation and coughing. Frequent ambulation (Option 3) is "
            "reasonable general activity but is not the priority, targeted intervention for this "
            "infection-control diagnosis."
        ),
    }),
))

# ---------------------------------------------------------------------------
# Item 26 -- Infection control precaution teaching evaluation -> Others
# ---------------------------------------------------------------------------
items.append(base_item(
    "standalone_1790300000013",
    "Infection Control - Precaution Type Teaching Evaluation (MCQ)",
    "Others", "Others",
    screen({
        "stem": "It would indicate a correct understanding of the teaching if the nurse is observed",
        "type": "multiple_choice",
        "preamble": "The nurse has attended a staff education program about infection control precautions.",
        "options": opts(
            ("wearing a particulate respirator mask (N95) when entering the room of a client with Haemophilus influenzae pneumonia", False),
            ("placing a client with streptococcal pneumonia in a room with a client who has respiratory syncytial virus (RSV)", False),
            ("wearing a protective gown when entering the room of a client with Escherichia coli O157:H7 who is incontinent", True),
            ("placing a client with pediculosis capitis (head lice) in a room with a client who has scabies", False),
        ),
        "explanation": (
            "Escherichia coli O157:H7 requires contact precautions, and a gown (Option 3) is appropriate "
            "PPE for contact with an incontinent client at high risk for fecal contamination of the "
            "environment and caregiver's clothing. Haemophilus influenzae pneumonia (Option 1) requires "
            "droplet precautions, not airborne precautions; an N95 respirator is not the correct PPE for "
            "this organism. Cohorting a client with streptococcal pneumonia (a bacterial droplet-"
            "precaution infection) with a client who has RSV (a different, viral, contact/droplet-"
            "precaution infection) (Option 2) risks cross-infecting each client with the other's organism "
            "and should not be done. Cohorting a client with head lice and a client with scabies "
            "(Option 4) similarly risks cross-infestation between 2 different ectoparasites and is not "
            "appropriate even though both require contact precautions."
        ),
    }),
))

# ---------------------------------------------------------------------------
# Item 27 -- Extrinsic fall risk factors -> Others
# ---------------------------------------------------------------------------
items.append(base_item(
    "standalone_1790300000014",
    "Safety - Extrinsic Fall Risk Factors (SATA)",
    "Others", "Others",
    screen({
        "stem": "Which of the following are extrinsic risk factors for falling? <b>Select all that apply.</b>",
        "type": "select_all",
        "preamble": "The nurse is assessing an older adult client who is scheduled for discharge and is at risk for falls.",
        "options": opts(
            ("uneven stairs", True),
            ("throw rugs", True),
            ("hemiparesis", False),
            ("dim lighting", True),
            ("confusion", False),
        ),
        "explanation": (
            "Extrinsic (environmental) fall risk factors are hazards in the client's surroundings: uneven "
            "stairs, throw rugs, and dim lighting (Options 1, 2, and 4) are all environmental hazards the "
            "nurse and client can modify. Hemiparesis (Option 3) and confusion (Option 5) are intrinsic "
            "risk factors, arising from the client's own physical and cognitive condition rather than the "
            "environment."
        ),
    }),
))

# ---------------------------------------------------------------------------
# Item 28 -- Impetigo contact precautions -> Others
# ---------------------------------------------------------------------------
items.append(base_item(
    "standalone_1790300000015",
    "Infection Control - Impetigo Contact Precautions (SATA)",
    "Others", "Others",
    screen({
        "stem": "Which of the following infection control precautions should the nurse implement? <b>Select all that apply.</b>",
        "type": "select_all",
        "preamble": "The nurse is caring for a 3-year-old client with impetigo.",
        "options": opts(
            ("Wear a surgical mask when bathing the client.", False),
            ("Wear a protective gown when changing the client's bed linens.", True),
            ("Keep the door to the client's room closed.", False),
            ("Place a box of clean gloves outside the client's door.", True),
            ("Place a surgical mask on the client during transport to other departments.", False),
        ),
        "explanation": (
            "Impetigo is a skin infection requiring contact precautions, so a gown for direct contact "
            "with contaminated linens (Option 2) and gloves readily available at the point of care "
            "(Option 4) are correct. A surgical mask when bathing the client (Option 1) is unnecessary, "
            "since impetigo is not spread by the respiratory route. Keeping the door closed (Option 3) is "
            "an airborne-precaution measure (to maintain negative pressure), not required for a contact-"
            "precaution skin infection. Placing a mask on the client during transport (Option 5) is "
            "similarly unnecessary, since impetigo does not spread by droplet or airborne transmission."
        ),
    }),
))

# ---------------------------------------------------------------------------
# Item 29 -- TB isolation evaluation -> Others
# ---------------------------------------------------------------------------
items.append(base_item(
    "standalone_1790300000016",
    "Infection Control - Tuberculosis Isolation Evaluation (MCQ)",
    "Others", "Others",
    screen({
        "stem": "Which of the following actions by the staff member would indicate to the nurse an understanding of the principles of infection control for tuberculosis isolation?",
        "type": "multiple_choice",
        "preamble": "The nurse is evaluating a staff member's care of a client with active pulmonary tuberculosis (TB).",
        "options": opts(
            ("instructing visitors to wash their hands before entering the client's room", False),
            ("putting on a mask, gown, and gloves before entering the client's room", False),
            ("placing tissues and a trash receptacle within the client's reach", True),
            ("asking the client to put on a clean mask each time someone enters the room", False),
        ),
        "explanation": (
            "Placing tissues and a trash receptacle within the client's reach (Option 3) supports "
            "respiratory hygiene and cough etiquette, helping contain infectious droplet nuclei at the "
            "source, and is an important, correctly targeted TB infection-control measure. Hand hygiene "
            "for visitors (Option 1) is good general practice but does not address the airborne "
            "transmission route that defines TB precautions, which specifically require a fit-tested N95 "
            "(or higher-level) respirator, not just hand hygiene. Gown and gloves (Option 2) are contact-"
            "precaution PPE and are not needed for airborne-only pulmonary TB; describing generic “a "
            "mask” also fails to specify the N95 respirator that TB actually requires. The engineering "
            "controls of the client's own negative-pressure isolation room, plus staff wearing an N95 on "
            "entry, are what protect others; routinely re-masking the client every time someone enters "
            "their own isolation room (Option 4) is not the standard practice (a mask on the client is "
            "used mainly during transport outside the room)."
        ),
    }),
))

# ---------------------------------------------------------------------------
# Item 30 -- Measles room assignment -> Others
# ---------------------------------------------------------------------------
items.append(base_item(
    "standalone_1790300000017",
    "Infection Control - Measles Room Assignment (MCQ)",
    "Others", "Others",
    screen({
        "stem": "The nurse should assign the client to a",
        "type": "multiple_choice",
        "preamble": "The nurse in the pediatric unit is preparing to admit a client with rubeola (measles).",
        "options": opts(
            ("private room at the end of the hallway", False),
            ("private room with monitored negative air pressure", True),
            ("room with a client who has chickenpox", False),
            ("room with a client who has atopic dermatitis (eczema)", False),
        ),
        "explanation": (
            "Measles (rubeola) requires airborne precautions, so a private room with monitored negative "
            "air pressure (Option 2) is the correct assignment. Physical distance from other rooms alone "
            "(Option 1) does not provide airborne isolation without negative pressure. Cohorting the "
            "client with a client who has chickenpox (varicella) (Option 3) is not appropriate; although "
            "both require airborne precautions, they are different organisms, and cohorting different "
            "airborne infections risks cross-infection. A client with atopic dermatitis (Option 4) has a "
            "disrupted skin barrier and is at increased risk for severe or complicated measles infection, "
            "making this an unsafe roommate pairing."
        ),
    }),
))

# ---------------------------------------------------------------------------
# Item 31 -- Infection control violation identification -> Others
# ---------------------------------------------------------------------------
items.append(base_item(
    "standalone_1790300000018",
    "Infection Control - Precaution Violation Identification (MCQ)",
    "Others", "Others",
    screen({
        "stem": "It would require intervention if a",
        "type": "multiple_choice",
        "preamble": "The charge nurse is observing the following client situations.",
        "options": opts(
            ("client with hepatitis B (HBV) is eating food brought into the facility by a visitor", False),
            ("visitor is sitting on the side of the bed of a client with acute pancreatitis", False),
            ("staff member is entering the room of a client with Haemophilus influenzae meningitis wearing a protective gown and gloves", True),
            ("family member of a client with mycoplasma pneumonia leaves the door to the client's room open", False),
        ),
        "explanation": (
            "Haemophilus influenzae meningitis requires droplet precautions, and the key required PPE is "
            "a mask; a staff member wearing only a gown and gloves (Option 3) is missing the mask that "
            "actually protects against droplet transmission, so this requires intervention. Hepatitis B "
            "(Option 1) is a bloodborne pathogen, not transmitted through food or casual contact, so a "
            "visitor sharing food is not a concern. A visitor sitting on the side of the bed of a client "
            "with pancreatitis (Option 2), a noninfectious condition with no isolation precautions, does "
            "not require intervention. Mycoplasma pneumoniae (Option 4) is managed with standard "
            "precautions in most settings and does not require the door to remain closed."
        ),
    }),
))

if __name__ == "__main__":
    for item in items:
        write_draft(item)
    print(f"\n{len(items)} items written.")
