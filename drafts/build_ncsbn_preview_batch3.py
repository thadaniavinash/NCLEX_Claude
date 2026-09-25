"""Builds 27 stand-alone items (Items 38-64, excluding the case study 32-37 which is built
separately by build_ncsbn_preview_case2.py) from the NCSBN NCLEX-RN Next Generation Exam
Preview PDF (c 2022 NCSBN), third attachment (Test3.pdf). Same conventions as the earlier
batches: every item carries question.footnote; no source answer key exists for any of these,
so every correct answer/rationale is this session's own clinical judgment, flagged for
clinician review. Items with no matching NURS 1017/1021 unit go to course/unit "Others".
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


def screen(question):
    q = dict(question)
    q.setdefault("footnote", FOOTNOTE)
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

# Item 38 -- AKI order to clarify -> NURS 1021 Unit 7 (Urinary)
items.append(base_item(
    "standalone_1784070000001", "Unit 7 Stand-alone 1: Acute Kidney Injury Order Clarification",
    "NURS 1021", "Unit 7 (Urinary Disorders)",
    screen({
        "stem": "Which of the following orders should the nurse clarify?",
        "type": "multiple_choice",
        "preamble": "The nurse is reviewing the orders of a client who has acute kidney injury.",
        "options": opts(
            ("computed tomography (CT) scan of the abdomen with intravenous contrast media", True),
            ("urine specimen for urinalysis", False),
            ("blood specimen for arterial blood gas (ABG)", False),
            ("referral to registered dietitian for parenteral nutrition evaluation", False),
        ),
        "explanation": (
            "Intravenous contrast media is nephrotoxic and can worsen kidney function in a client "
            "who already has acute kidney injury (AKI); this order should be clarified with the "
            "prescriber, who may choose an alternative imaging study or non-contrast CT. A urinalysis "
            "(Option 2) and an ABG (Option 3) are appropriate, expected diagnostic studies for "
            "evaluating AKI. A dietitian referral (Option 4) is appropriate, since nutritional needs "
            "commonly must be adjusted in AKI."
        ),
    }),
))

# Item 39 -- Restraints teaching -> Others
items.append(base_item(
    "standalone_1790300000019", "Safety - Restraint Use Client Teaching (MCQ)",
    "Others", "Others",
    screen({
        "stem": "Which of the following information should the nurse include?",
        "type": "multiple_choice",
        "preamble": "The nurse is planning a staff education program about caring for clients with restraints.",
        "options": opts(
            ("“Restraints should be removed once during a shift to perform passive range-of-motion (ROM) exercises.”", False),
            ("“Restraints should be secured to the side rails of the client's bed for quick release.”", False),
            ("“Restraints require an order from the primary health care provider.”", True),
            ("“Restraints may be used p.r.n. for clients who are confused.”", False),
        ),
        "explanation": (
            "Restraints require a time-limited order from the primary health care provider (Option "
            "3); they cannot be applied solely at nursing discretion. Restraints should be released "
            "and the limb assessed and repositioned at least every 2 hours, not just once per shift "
            "(Option 1). Restraints must be secured to the bed frame, never to a movable side rail "
            "(Option 2), which is a safety hazard if the rail is lowered. Restraint orders cannot be "
            "written as p.r.n. (Option 4); confusion alone does not automatically justify restraint "
            "use, and the least restrictive alternative must be tried first."
        ),
    }),
))

# Item 40 -- TB plan of care -> Others (infection control)
items.append(base_item(
    "standalone_1790300000020", "Infection Control - Tuberculosis Plan of Care (MCQ)",
    "Others", "Others",
    screen({
        "stem": "Which of the following should the nurse include in the client's plan of care?",
        "type": "multiple_choice",
        "preamble": "The nurse is caring for a client with active pulmonary tuberculosis (TB).",
        "options": opts(
            ("placing the client in a private room with the door open", False),
            ("putting a surgical mask on the client during transport to the radiology department", True),
            ("instructing the primary caregivers to wear surgical masks when caring for the client", False),
            ("instituting the standards for droplet precautions", False),
        ),
        "explanation": (
            "TB requires airborne precautions, and placing a surgical mask on the client for source "
            "control during transport outside the negative-pressure room (Option 2) is correct "
            "practice. The private room's door must stay closed, not open (Option 1), to maintain "
            "negative pressure. Caregivers need a fit-tested N95 (or higher-level) respirator, not a "
            "surgical mask (Option 3), to protect against airborne transmission. TB requires airborne "
            "precautions, not droplet precautions (Option 4)."
        ),
    }),
))

# Item 41 -- Impetigo parent teaching -> Others (infection control)
items.append(base_item(
    "standalone_1790300000021", "Infection Control - Impetigo Parent Teaching (MCQ)",
    "Others", "Others",
    screen({
        "stem": "Which of the following information should the nurse include?",
        "type": "multiple_choice",
        "preamble": "The home-health nurse is teaching the parents of a 4-year-old client with impetigo.",
        "options": opts(
            ("“Put a surgical mask on your child when around siblings.”", False),
            ("“Cleanse the lesions with a povidone-iodine solution daily.”", False),
            ("“Apply petroleum jelly to the lesions daily.”", False),
            ("“Instruct your child not to use the same towels as siblings.”", True),
        ),
        "explanation": (
            "Impetigo spreads by direct and indirect contact (including shared linens and towels), so "
            "not sharing towels with siblings (Option 4) is standard, correct contact-precaution "
            "teaching. A mask (Option 1) is unnecessary, since impetigo does not spread by the "
            "respiratory route. Daily cleansing is typically with gentle soap and water rather than "
            "povidone-iodine (Option 2). Petroleum jelly (Option 3) is not the standard treatment; "
            "prescribed topical or oral antibiotics are used instead, and an occlusive ointment is not "
            "the recommended lesion care."
        ),
    }),
))

# Item 42 -- Bioterrorism transmission -> Others
items.append(base_item(
    "standalone_1790300000022", "Bioterrorism Agent Transmission Teaching (MCQ)",
    "Others", "Others",
    screen({
        "stem": "Which of the following statements by the nurse would require follow-up?",
        "type": "multiple_choice",
        "preamble": "The nurse has attended a staff education program about bioterrorism.",
        "options": opts(
            ("“Botulism is transmitted by ingestion of contaminated canned foods.”", False),
            ("“Hemorrhagic fever is spread by direct contact with blood or body fluids.”", False),
            ("“Anthrax is spread through direct contact with the bacteria and its spores.”", False),
            ("“Bubonic plague is transmitted from person to person via airborne droplets.”", True),
        ),
        "explanation": (
            "Bubonic plague (Option 4) is transmitted primarily through the bite of infected fleas, "
            "not person-to-person via airborne droplets; it is pneumonic plague, a different clinical "
            "form, that can spread person to person via respiratory droplets, so this statement is "
            "incorrect and requires follow-up. Botulism from contaminated canned foods (Option 1), "
            "hemorrhagic fever spread by contact with blood/body fluids (Option 2), and anthrax spread "
            "through direct contact with the bacteria and spores (Option 3) are all accurate "
            "statements that do not require follow-up."
        ),
    }),
))

# Item 43 -- Thoracic expansion assessment technique -> NURS 1021 Unit 3 (Respiratory)
items.append(base_item(
    "standalone_1784030000003", "Unit 3 Stand-alone 3: Thoracic Expansion Assessment Technique",
    "NURS 1021", "Unit 3 (Respiratory Disorders)",
    screen({
        "stem": "Which of the following would indicate that the coworker is using the correct assessment technique?",
        "type": "multiple_choice",
        "preamble": "The nurse observes a coworker who is assessing a client's thoracic expansion.",
        "options": opts(
            ("percussion from the apex of the scapula downward on each side", False),
            ("placement of the hands flat on the back with the thumbs at the level of the tenth ribs pointing to the spine, then asking the client to inhale", True),
            ("measurement of the anteroposterior diameter of the chest", False),
            ("placement of the palms at the level of the tenth ribs with thumbs pointing to the xiphoid process, then asking the client to inhale", False),
        ),
        "explanation": (
            "Posterior thoracic (respiratory) excursion is assessed by placing the hands flat against "
            "the client's back with the thumbs at about the level of the tenth ribs pointing toward "
            "the spine, then observing the thumbs move symmetrically apart as the client inhales "
            "(Option 2). Percussion from the scapula downward (Option 1) assesses lung resonance/"
            "diaphragmatic excursion, a different parameter, not chest wall expansion. Measuring the "
            "anteroposterior diameter (Option 3) assesses chest configuration (for example, a barrel "
            "chest), not excursion during breathing."
        ),
    }),
))

# Item 44 -- Perimenopause hot flashes -> NURS 1021 Unit 9 (Reproductive)
items.append(base_item(
    "standalone_1784090000001", "Unit 9 Stand-alone 1: Perimenopause Hot Flash Management",
    "NURS 1021", "Unit 9 (Reproductive Disorders)",
    screen({
        "stem": "Which of the following lifestyle modifications would be appropriate for the nurse to recommend?",
        "type": "multiple_choice",
        "preamble": "The nurse at a health fair is talking with a client who is in perimenopause and is experiencing hot flashes.",
        "options": opts(
            ("increasing fluid intake", False),
            ("exercising daily", False),
            ("decreasing sodium intake", False),
            ("wearing clothing in layers", True),
        ),
        "explanation": (
            "Wearing clothing in layers (Option 4) is a standard, practical recommendation for "
            "managing hot flashes, since layers can be quickly removed when a hot flash occurs and "
            "added back as it resolves. Increasing fluid intake (Option 1) and decreasing sodium "
            "intake (Option 3) are general health measures not specifically targeted at hot flash "
            "management. Daily exercise (Option 2) supports overall menopausal health but is not the "
            "specific, targeted recommendation for managing an acute hot flash episode the way "
            "dressing in layers is."
        ),
    }),
))

# Item 45 -- Health promotion >65 -> Others
items.append(base_item(
    "standalone_1790300000023", "Health Promotion for Clients Over 65 (MCQ)",
    "Others", "Others",
    screen({
        "stem": "Which of the following information should the nurse include?",
        "type": "multiple_choice",
        "preamble": "The nurse in a community-based setting is teaching clients over 65 years of age about health promotion activities.",
        "options": opts(
            ("“Purchase all of your prescribed medications at the same pharmacy.”", True),
            ("“Schedule an appointment for a vision screening every 3 years.”", False),
            ("“Participate in daily aerobic exercises for 60 minutes.”", False),
            ("“Increase your intake of fat-soluble vitamins.”", False),
        ),
        "explanation": (
            "Using a single pharmacy (Option 1) allows the pharmacist to screen all of a client's "
            "medications together for interactions and duplications, an important safety measure for "
            "older adults. Vision screening (Option 2) should generally occur annually for this age "
            "group, not every 3 years. Recommending 60 minutes of daily aerobic exercise (Option 3) "
            "exceeds standard general guidelines (about 150 minutes per week of moderate activity) and "
            "may not be realistic or safe as a blanket recommendation. Increasing fat-soluble vitamin "
            "intake (Option 4) is not a general health-promotion recommendation, and excess fat-"
            "soluble vitamins (A, D, E, K) can accumulate to toxic levels."
        ),
    }),
))

# Item 46 -- Leukemia risk factors -> NURS 1017 Unit 4 (Neoplasia)
items.append(base_item(
    "standalone_1783040000001", "Unit 4 Stand-alone 1: Highest Risk for Leukemia",
    "NURS 1017", "Unit 4 (Neoplasia)",
    screen({
        "stem": "At <b>highest</b> risk for developing leukemia is the client who",
        "type": "multiple_choice",
        "preamble": "The nurse is screening clients for those at increased risk for developing cancer.",
        "options": opts(
            ("received more than 3 blood transfusions", False),
            ("has a magnetic resonance imaging (MRI) scan annually", False),
            ("has polycythemia vera and requires phlebotomy treatments", False),
            ("had colon cancer and received chemotherapy treatments", True),
        ),
        "explanation": (
            "Certain chemotherapy agents, particularly alkylating agents and topoisomerase II "
            "inhibitors commonly used to treat colon cancer, are well-established causes of "
            "treatment-related (secondary) leukemia, making this client's risk the highest of those "
            "listed. Multiple blood transfusions (Option 1) are not an established leukemia risk "
            "factor. MRI (Option 2) uses no ionizing radiation and is not a cancer risk factor, unlike "
            "CT or x-ray imaging. Polycythemia vera (Option 3) carries some increased risk of "
            "transformation to acute leukemia over time, but this risk is generally smaller in "
            "magnitude than the risk associated with leukemogenic chemotherapy."
        ),
    }),
))

# Item 47 -- Older adult postop increased need -> Others
items.append(base_item(
    "standalone_1790300000024", "Older Adult Postoperative Priority Need (MCQ)",
    "Others", "Others",
    screen({
        "stem": "The nurse should know that this client, compared with younger clients in the postoperative period, will have an <b>increased</b> need for",
        "type": "multiple_choice",
        "preamble": "The nurse is caring for an older adult client in the postoperative period.",
        "options": opts(
            ("oral hygiene", False),
            ("analgesics", False),
            ("high-calorie foods", False),
            ("early mobilization", True),
        ),
        "explanation": (
            "Older adults have an increased need for early mobilization after surgery (Option 4) "
            "because they are at substantially higher risk than younger clients for complications of "
            "immobility such as pneumonia, venous thromboembolism, pressure injury, and functional "
            "decline, and they recover mobility more slowly. Oral hygiene (Option 1) is important for "
            "all postoperative clients but is not specifically increased by age. Analgesic needs "
            "(Option 2) are often lower, not higher, in older adults due to altered pharmacokinetics "
            "and increased sensitivity to side effects. Caloric needs (Option 3) are generally "
            "decreased, not increased, in older adults due to a lower metabolic rate."
        ),
    }),
))

# Item 48 -- Pediatric UTI prevention -> NURS 1021 Unit 7 (Urinary)
items.append(base_item(
    "standalone_1784070000002", "Unit 7 Stand-alone 2: Pediatric Urinary Tract Infection Prevention",
    "NURS 1021", "Unit 7 (Urinary Disorders)",
    screen({
        "stem": "Which of the following information should the nurse include? <b>Select all that apply.</b>",
        "type": "select_all",
        "preamble": "The nurse is planning a staff education program about the prevention of urinary tract infections (UTIs) in children.",
        "options": opts(
            ("“Teach the child to perform Kegel exercises.”", False),
            ("“Encourage the child to empty the bladder completely.”", True),
            ("“Encourage the child to maintain an adequate fluid intake.”", True),
            ("“Teach the child how to properly cleanse the perineal area.”", True),
            ("“Offer the child noncarbonated, decaffeinated beverage choices.”", True),
        ),
        "explanation": (
            "Complete bladder emptying (Option 2) prevents urinary stasis that allows bacteria to "
            "multiply. Adequate fluid intake (Option 3) helps flush bacteria from the urinary tract. "
            "Proper perineal cleansing technique, such as front-to-back wiping (Option 4), prevents "
            "introducing bacteria into the urethra. Noncarbonated, decaffeinated beverages (Option 5) "
            "avoid bladder irritants that carbonation and caffeine can cause. Kegel exercises (Option "
            "1) strengthen pelvic floor muscles for continence and are not a standard pediatric UTI "
            "prevention teaching point."
        ),
    }),
))

# Item 49 -- AD family teaching, agitation -> NURS 1017 Unit 7 (Neurological)
items.append(base_item(
    "standalone_1783070000004", "Unit 7 Stand-alone 4: Alzheimer's Disease Family Teaching (Agitation)",
    "NURS 1017", "Unit 7 (Neurological Disorders)",
    screen({
        "stem": "Which of the following interventions should the nurse include in the teaching? <b>Select all that apply.</b>",
        "type": "select_all",
        "preamble": "The nurse is teaching the family member of a client with moderate Alzheimer's disease (AD).",
        "options": opts(
            ("Use distraction when the client becomes agitated.", True),
            ("Place calendars within clear view of the client.", True),
            ("Use short, simple sentences and provide step-by-step instructions for the client.", True),
            ("Avoid reminiscing with the client about past experiences in order to avoid feelings of loss and loneliness.", False),
            ("Encourage the client to participate in a daytime exercise program to promote restful sleep at night.", True),
        ),
        "explanation": (
            "Distraction (Option 1) is a standard de-escalation technique for agitation in AD. "
            "Calendars (Option 2) support reality orientation. Short, simple sentences with step-by-"
            "step instructions (Option 3) match the client's cognitive processing ability. A daytime "
            "exercise program (Option 5) helps regulate the sleep-wake cycle and can reduce "
            "sundowning and improve nighttime rest. Reminiscence about long-term memories (Option 4) "
            "should be encouraged, not avoided, since long-term memory is often preserved in AD and "
            "reminiscing is a validating, anxiety-reducing activity."
        ),
    }),
))

# Item 50 -- PRBC transfusion prep -> NURS 1021 Unit 1 (Blood Disorders)
items.append(base_item(
    "standalone_1784010000001", "Unit 1 Stand-alone 1: Packed Red Blood Cell Transfusion Preparation",
    "NURS 1021", "Unit 1 (Blood Disorders)",
    screen({
        "stem": "Which of the following actions should the nurse take?",
        "type": "multiple_choice",
        "preamble": "The nurse is preparing to administer a unit of packed red blood cells (PRBCs) to a client.",
        "options": opts(
            ("Assess the client's recent urine output.", False),
            ("Prime a Y-tubing blood administration set with lactated Ringer's solution.", False),
            ("Ensure that the client has a peripheral venous access device (VAD) that is 24-gauge or larger.", True),
            ("Verify with another nurse that the client's room number is on both the blood product label and the client's identification band.", False),
        ),
        "explanation": (
            "Blood is administered through a VAD of at least 24-gauge (that is, 24-gauge or a larger-"
            "bore catheter such as 22, 20, or 18-gauge) to allow safe infusion of the product (Option "
            "3). Blood administration sets must be primed with 0.9% sodium chloride only, never "
            "lactated Ringer's solution (Option 2), because the calcium in Ringer's solution can cause "
            "the blood product to clot. Room number is never an acceptable client identifier for "
            "verifying a blood product against the client's identification band (Option 4); a full "
            "name and a unique identifier such as a medical record number must be used instead. "
            "Assessing recent urine output (Option 1) is not a required immediate pre-transfusion "
            "action; it is more relevant to monitoring after the transfusion begins."
        ),
    }),
))

# Item 51 -- MI coping (ineffective) -> NURS 1021 Unit 2 (Cardiovascular)
items.append(base_item(
    "standalone_1784020000002", "Unit 2 Stand-alone 2: Ineffective Coping After Myocardial Infarction",
    "NURS 1021", "Unit 2 (Cardiovascular Disorders)",
    screen({
        "stem": "Which of the following statements by the client would indicate ineffective coping?",
        "type": "multiple_choice",
        "preamble": "The nurse is assessing the coping strategies of a client who had a myocardial infarction (MI) 3 days ago.",
        "options": opts(
            ("“I know that stopping smoking will be difficult.”", False),
            ("“I plan to attend a cardiac rehabilitation support group.”", False),
            ("“I have trouble believing this has really happened to me.”", False),
            ("“I have let down my family because I will not be able to financially support them any longer.”", True),
        ),
        "explanation": (
            "Assuming, only 3 days after an MI, that the client will permanently be unable to work and "
            "support their family (Option 4) reflects catastrophic thinking and hopelessness not "
            "grounded in the client's actual prognosis, indicating ineffective coping and warranting "
            "further assessment for depression or excessive guilt. Acknowledging that quitting smoking "
            "will be difficult (Option 1) and planning to attend cardiac rehabilitation (Option 2) "
            "both reflect realistic, adaptive coping and engagement with recovery. Some difficulty "
            "believing the MI happened (Option 3) reflects an early, commonly expected stage of "
            "processing a sudden diagnosis rather than clearly ineffective coping at only 3 days out."
        ),
    }),
))

# Item 52 -- EOL comfort care -> Others
items.append(base_item(
    "standalone_1790300000025", "End-of-Life Comfort Care Caregiver Teaching (MCQ)",
    "Others", "Others",
    screen({
        "stem": "Which of the following statements by the caregiver would require follow-up?",
        "type": "multiple_choice",
        "preamble": "The hospice nurse has taught an in-home caregiver about comfort care for a client at the end of life.",
        "options": opts(
            ("“I have been applying petroleum jelly to keep the client's lips moist.”", False),
            ("“I have been offering healthy foods frequently to keep up the client's strength.”", True),
            ("“A blowing fan seems to be less anxiety-producing for the client than an oxygen mask.”", False),
            ("“Sitting upright seems to reduce the client's noisy breathing more than lying down in the bed.”", False),
        ),
        "explanation": (
            "Frequently offering food to “keep up strength” (Option 2) requires follow-up, "
            "because appetite naturally declines at the end of life and end-of-life care focuses on "
            "comfort, not on forcing intake to build strength; frequent food offers can cause "
            "discomfort or distress. Petroleum jelly for dry lips (Option 1) is an appropriate comfort "
            "measure. A fan blowing air on the face (Option 3) is a well-supported way to relieve the "
            "sensation of dyspnea, often with less associated anxiety than an oxygen mask. Sitting "
            "upright to reduce noisy breathing (“death rattle”) (Option 4) is an accurate, "
            "appropriate observation, since upright positioning can improve secretion drainage."
        ),
    }),
))

# Item 53 -- Informed consent validity -> Others
items.append(base_item(
    "standalone_1790300000026", "Legal-Ethical - Informed Consent Validity (SATA)",
    "Others", "Others",
    screen({
        "stem": "Which of the following conditions should the nurse recognize must be met to ensure the consent is valid? <b>Select all that apply.</b>",
        "type": "select_all",
        "preamble": "The nurse is witnessing the client's signature on a consent form.",
        "options": opts(
            ("The client gave consent voluntarily.", True),
            ("The client received adequate disclosure.", True),
            ("The consent form is witnessed by 2 health care professionals.", False),
            ("The client understands the scheduled procedure or treatment.", True),
            ("The consent form is signed within 24 hours of the scheduled procedure or treatment.", False),
        ),
        "explanation": (
            "Valid informed consent requires that it be given voluntarily (Option 1), that the client "
            "received adequate disclosure of the risks, benefits, and alternatives (Option 2), and "
            "that the client demonstrates understanding of the procedure or treatment (Option 4). "
            "Consent forms typically require only 1 witness signature, not 2 health care professionals "
            "(Option 3). There is no universal requirement that consent be signed within a specific "
            "24-hour window of the procedure (Option 5)."
        ),
    }),
))

# Item 54 -- Sexual assault crisis intervention -> Others
items.append(base_item(
    "standalone_1790300000027", "Crisis Intervention - Sexual Assault Response (SATA)",
    "Others", "Others",
    screen({
        "stem": "Which of the following would be an appropriate response for the nurse to make? <b>Select all that apply.</b>",
        "type": "select_all",
        "preamble": "The nurse is talking with a client who has been sexually assaulted. The client states, “I never should have walked home late at night. I am to blame for what has happened to me.”",
        "options": opts(
            ("“The police officers who brought you into the hospital will be with you during this interview.”", False),
            ("“You should take a warm, calming shower in order to feel more relaxed.”", False),
            ("“You did the best you could in very difficult circumstances.”", True),
            ("“Sometimes the victim's behavior causes the violence.”", False),
            ("“You are safe here.”", True),
        ),
        "explanation": (
            "“You did the best you could in very difficult circumstances” validates the "
            "client and counters self-blame. “You are safe here” provides appropriate "
            "reassurance and helps establish a sense of safety. Having police remain present during a "
            "sensitive forensic/medical interview is not standard best practice; the client should "
            "have control over who is present, generally a support person or advocate of the client's "
            "choosing. Recommending a shower before a forensic examination is incorrect and harmful, "
            "since showering destroys evidence needed for the examination. Suggesting that “the "
            "victim's behavior causes the violence” is victim-blaming and is never an appropriate "
            "statement."
        ),
    }),
))

# Item 55 -- AD care plan (routine) -> NURS 1017 Unit 7 (Neurological)
items.append(base_item(
    "standalone_1783070000005", "Unit 7 Stand-alone 5: Alzheimer's Disease Daily Care Planning",
    "NURS 1017", "Unit 7 (Neurological Disorders)",
    screen({
        "stem": "Which of the following interventions should the nurse include in the client's plan of care? <b>Select all that apply.</b>",
        "type": "select_all",
        "preamble": "The nurse is planning care for a client with moderate Alzheimer's disease (AD).",
        "options": opts(
            ("Establish a daily routine for the client.", True),
            ("Assist the client to void every 2 hours.", True),
            ("Introduce self upon interacting with the client.", True),
            ("Display a clock and calendar in the client's room.", True),
            ("Keep the client's television on during the day to distract the client.", False),
        ),
        "explanation": (
            "A consistent daily routine (Option 1) reduces confusion and anxiety in AD. Scheduled "
            "toileting every 2 hours (Option 2) is a proactive continence strategy. Reintroducing "
            "oneself at each interaction (Option 3) accommodates impaired recognition memory and "
            "reduces fear or confusion. A clock and calendar (Option 4) support reality orientation. "
            "Keeping the television on continuously (Option 5) is not appropriate; excess background "
            "stimulation tends to increase confusion and agitation in AD rather than help, and a calm, "
            "low-stimulation environment is generally preferred."
        ),
    }),
))

# Item 56 -- Pediatric dysfunctional grieving -> Others
items.append(base_item(
    "standalone_1790300000028", "Pediatric Dysfunctional Grieving Indicator (MCQ)",
    "Others", "Others",
    screen({
        "stem": "The nurse should understand that the child may be experiencing dysfunctional grieving if the parent reports that the child",
        "type": "multiple_choice",
        "preamble": "A parent is discussing with the nurse the behaviors of a 4-year-old child following the death of a grandparent.",
        "options": opts(
            ("conducts mock funerals with stuffed animals", False),
            ("refuses to go to sleep at night", True),
            ("continues to talk about the grandparent coming to visit", False),
            ("asks to play with the grandparent while at the cemetery", False),
        ),
        "explanation": (
            "Persistent refusal to sleep at night (Option 2) reflects ongoing anxiety and dysregulation "
            "that goes beyond the expected, developmentally typical grief responses of a preschooler "
            "and can indicate the grieving process is becoming dysfunctional. Reenacting funerals "
            "through play (Option 1), continuing to talk about the deceased returning (Option 3), and "
            "asking to play with the grandparent at the cemetery (Option 4) all reflect the magical "
            "thinking and play-based processing that are normal, expected features of how preschool-"
            "age children process death, since children this age do not yet fully grasp its "
            "permanence."
        ),
    }),
))

# Item 57 -- Low-sodium diet teaching -> NURS 1021 Unit 2 (Cardiovascular)
items.append(base_item(
    "standalone_1784020000003", "Unit 2 Stand-alone 3: Low-Sodium Diet Teaching Evaluation",
    "NURS 1021", "Unit 2 (Cardiovascular Disorders)",
    screen({
        "stem": "Which of the following statements by the client would indicate a correct understanding of the teaching?",
        "type": "multiple_choice",
        "preamble": "The nurse has taught a client who has been ordered a low-sodium diet about appropriate food choices.",
        "options": opts(
            ("“I will eat steamed, fresh broccoli with herbs and spices for an evening meal.”", True),
            ("“I will add cottage cheese and other dairy products to my daily diet.”", False),
            ("“I am glad I can still enjoy eating cereals, such as bran flakes with raisins.”", False),
            ("“I am glad I can eat lean meats daily because I eat ham sandwiches for an afternoon meal.”", False),
        ),
        "explanation": (
            "Fresh steamed vegetables seasoned with herbs and spices instead of salt (Option 1) is "
            "exactly the substitution pattern taught for a low-sodium diet. Cottage cheese (Option 2) "
            "and many processed breakfast cereals such as bran flakes (Option 3) are common hidden-"
            "sodium sources that clients often mistakenly consider low-sodium choices. Ham (Option 4) "
            "is a cured, processed meat that is very high in sodium and is not an appropriate "
            "substitute for a fresh lean meat on a low-sodium diet."
        ),
    }),
))

# Item 58 -- Post-mastectomy ROM -> NURS 1017 Unit 4 (Neoplasia)
items.append(base_item(
    "standalone_1783040000002", "Unit 4 Stand-alone 2: Post-Mastectomy Range-of-Motion Exercise",
    "NURS 1017", "Unit 4 (Neoplasia)",
    screen({
        "stem": "Which of the following, if reported by the client on her return visit to the clinic, would indicate to the nurse that the instructions have been followed correctly?",
        "type": "multiple_choice",
        "preamble": "The nurse is caring for a client who had a left modified radical mastectomy. The client received discharge instructions for performing range-of-motion (ROM) exercises on her left arm.",
        "options": opts(
            ("regular squeezing of a tennis ball in her left hand", False),
            ("placing her left palm against a wall and “climbing” the wall with the left fingers", True),
            ("carrying light hand weights while walking 1 mile every other day", False),
            ("performing isometric exercises with both arms extended", False),
        ),
        "explanation": (
            "“Wall climbing” with the fingers of the affected arm (Option 2) is the classic, "
            "specifically taught postmastectomy exercise for restoring shoulder range of motion. "
            "Carrying weights with the affected arm (Option 3) is generally discouraged early in "
            "recovery because of the risk of lymphedema, particularly after axillary lymph node "
            "involvement. Squeezing a tennis ball (Option 1) exercises the hand but is not the "
            "specific shoulder ROM exercise taught for this surgery. Isometric exercises with the arms "
            "extended (Option 4) are not part of the standard early postmastectomy ROM teaching."
        ),
    }),
))

# Item 59 -- Expressive aphasia spouse communication -> NURS 1017 Unit 7 (Neurological)
items.append(base_item(
    "standalone_1783070000006", "Unit 7 Stand-alone 6: Expressive Aphasia Spouse Communication",
    "NURS 1017", "Unit 7 (Neurological Disorders)",
    screen({
        "stem": "Which of the following statements by the client's spouse would indicate a correct understanding of the client's communication abilities and interaction needs? <b>Select all that apply.</b>",
        "type": "select_all",
        "preamble": "The nurse is planning care for a client who has expressive aphasia after a left-sided stroke.",
        "options": opts(
            ("“My spouse's response of 'fine' when I asked how the day has been may or may not be what my spouse meant to communicate.”", True),
            ("“I can anticipate what my spouse wants to say, so I complete my spouse's sentences to make communication quicker.”", False),
            ("“I will purchase a picture board to help my spouse express common needs, thoughts, and feelings when communication is difficult.”", True),
            ("“My spouse's angry response when we have a conversation makes me hesitant to try further communication.”", False),
            ("“I have arranged for my spouse to meet with a speech therapist twice each week to improve communication skills.”", True),
        ),
        "explanation": (
            "Recognizing that a simple response like “fine” may not accurately reflect what "
            "the client intends to say (Option 1) reflects correct understanding of expressive "
            "aphasia, in which producing intended language is impaired. Obtaining a picture "
            "communication board (Option 3) and arranging regular speech therapy (Option 5) are both "
            "appropriate, standard interventions for expressive aphasia. Habitually finishing the "
            "client's sentences (Option 2) is not recommended, since it can be frustrating and does "
            "not reliably reflect what the client intends to say; the client should be given time to "
            "communicate. Becoming hesitant to attempt further communication because of the client's "
            "frustration (Option 4) is an avoidant response, not an appropriate coping strategy."
        ),
    }),
))

# Item 60 -- Buck traction -> NURS 1017 Unit 6 (Musculoskeletal)
items.append(base_item(
    "standalone_1783060000002", "Unit 6 Stand-alone 2: Buck Traction Immediate Intervention",
    "NURS 1017", "Unit 6 (Musculoskeletal Disorders)",
    screen({
        "stem": "Which of the following would require <b>immediate</b> intervention?",
        "type": "multiple_choice",
        "preamble": "The nurse is caring for a client who is in Buck traction.",
        "options": opts(
            ("A pillow is placed under the knee.", True),
            ("The foot is 2 in (5 cm) away from the foot plate.", False),
            ("The weights attached to the pulley are 6 in (15 cm) from the floor.", False),
            ("A pillow is placed under the lower leg with the heel off the bed.", False),
        ),
        "explanation": (
            "Buck traction requires the affected leg to remain straight and in line with the pull of "
            "the traction; placing a pillow under the knee (Option 1) flexes the knee, misaligns the "
            "traction, and undermines its therapeutic effect, requiring immediate intervention. The "
            "foot being a short distance from the foot plate (Option 2) is an acceptable, expected "
            "finding. Weights hanging freely a few inches off the floor (Option 3) is the correct, "
            "expected setup. A pillow supporting the length of the lower leg while keeping the heel "
            "off the bed (Option 4) is an appropriate technique to prevent heel pressure injury "
            "without disrupting alignment."
        ),
    }),
))

# Item 61 -- AD home care safety -> NURS 1017 Unit 7 (Neurological)
items.append(base_item(
    "standalone_1783070000007", "Unit 7 Stand-alone 7: Alzheimer's Disease Home Care Teaching",
    "NURS 1017", "Unit 7 (Neurological Disorders)",
    screen({
        "stem": "Which of the following statements by the adult child would indicate a correct understanding of the teaching?",
        "type": "multiple_choice",
        "preamble": "The nurse has taught the adult child caregiver of a client with moderate Alzheimer's disease (AD) about home care.",
        "options": opts(
            ("“I will only allow my parent to smoke while my parent is outdoors.”", False),
            ("“I will place a picture on the bathroom door to indicate which room is the bathroom.”", True),
            ("“I will encourage family members to visit in large groups to keep my parent interested in the conversation.”", False),
            ("“I will encourage my parent to take walks in the park when the weather permits to get the exercise needed.”", False),
        ),
        "explanation": (
            "A picture on the bathroom door (Option 2) is a well-established, effective wayfinding aid "
            "for clients with AD who have difficulty with word/symbol recognition. Location alone does "
            "not address the core safety issue with smoking (Option 1); a client with AD needs direct "
            "supervision while smoking regardless of setting, due to fire-safety risk and impaired "
            "judgment. Large group visits (Option 3) tend to overstimulate and confuse clients with "
            "AD; small, quiet visits are generally recommended instead. Unsupervised walks in the park "
            "(Option 4) raise a significant wandering and safety risk for a client with AD."
        ),
    }),
))

# Item 62 -- Diverticulosis teaching -> NURS 1021 Unit 6 (GI)
items.append(base_item(
    "standalone_1784060000001", "Unit 6 Stand-alone 1: Diverticulosis Client Teaching",
    "NURS 1021", "Unit 6 (Gastrointestinal Disorders)",
    screen({
        "stem": "Which of the following information should the nurse include?",
        "type": "multiple_choice",
        "preamble": "The nurse is teaching a client newly diagnosed with diverticulosis.",
        "options": opts(
            ("“Limit your daily fluid intake to 2 L to avoid bloating.”", False),
            ("“You may be prescribed a bulk-forming laxative.”", True),
            ("“Limit your intake of dairy products such as milk and yogurt.”", False),
            ("“You should avoid consuming cooked vegetables.”", False),
        ),
        "explanation": (
            "A bulk-forming laxative such as psyllium (Option 2) is commonly prescribed for "
            "diverticulosis to promote regular, soft bowel movements and reduce intraluminal pressure. "
            "Diverticulosis management encourages adequate, not limited, fluid intake (Option 1) "
            "alongside a high-fiber diet to prevent constipation. There is no standard indication to "
            "limit dairy products (Option 3). Cooked vegetables (Option 4) are a recommended source of "
            "fiber and are not restricted; the older recommendation to avoid seeds, nuts, and popcorn "
            "is now considered outdated and not evidence-based, and cooked vegetables were never part "
            "of that restriction."
        ),
    }),
))

# Item 63 -- Med safety, unfamiliar dosage -> Others
items.append(base_item(
    "standalone_1790300000029", "Medication Safety - Unfamiliar Dosage Verification (MCQ)",
    "Others", "Others",
    screen({
        "stem": "Which of the following actions should the nurse take <b>next</b>?",
        "type": "multiple_choice",
        "preamble": "The nurse is preparing to administer lorazepam 2 mg, IV, now to a client who is scheduled for surgery in 30 minutes. The nurse is unfamiliar with the dosage for the medication.",
        "options": opts(
            ("Check the medication dosage in a medication reference source.", False),
            ("Ask another nurse whether the prescribed dose is a safe dose.", False),
            ("Clarify that the dose is correct with the primary health care provider.", False),
            ("Contact the pharmacist to verify the safe dosage range for the medication.", True),
        ),
        "explanation": (
            "The pharmacist is the medication expert and the most authoritative, reliable resource for "
            "verifying a safe dosage range, especially in a time-sensitive situation (Option 4). "
            "Checking a general reference (Option 1) is reasonable but less authoritative than a "
            "pharmacist consultation for verifying a specific order. Asking a peer nurse (Option 2) is "
            "not an authoritative safety check. Contacting the prescriber (Option 3) is appropriate if "
            "there is concern the order itself is wrong, but the nurse's stated problem here is simply "
            "unfamiliarity with the medication, which the pharmacist is best positioned to resolve."
        ),
    }),
))

# Item 64 -- Phenothiazine NMS -> Others
items.append(base_item(
    "standalone_1790300000030", "Neuroleptic Malignant Syndrome Priority Finding (MCQ)",
    "Others", "Others",
    screen({
        "stem": "When evaluating the client for a life-threatening syndrome related to the medication, it would be a priority for the nurse to report",
        "type": "multiple_choice",
        "preamble": "The nurse is caring for a client who is receiving a high dose of a phenothiazine.",
        "options": opts(
            ("dry mouth", False),
            ("orthostatic hypotension", False),
            ("fever", True),
            ("photophobia", False),
        ),
        "explanation": (
            "Fever is a cardinal sign of neuroleptic malignant syndrome (NMS) (Option 3), a rare but "
            "life-threatening reaction to phenothiazines and other antipsychotics that also includes "
            "muscle rigidity, altered mental status, and autonomic instability; it must be reported "
            "immediately. Dry mouth (Option 1) and orthostatic hypotension (Option 2) are common, "
            "expected anticholinergic and alpha-blocking side effects of phenothiazines, not signs of "
            "NMS. Photophobia (Option 4) is not a typical finding of either routine phenothiazine side "
            "effects or NMS."
        ),
    }),
))

if __name__ == "__main__":
    for item in items:
        write_draft(item)
    print(f"\n{len(items)} items written.")
