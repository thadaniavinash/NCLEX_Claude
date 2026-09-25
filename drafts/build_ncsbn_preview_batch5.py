"""Builds the final batch of stand-alone items from the NCSBN NCLEX-RN Next Generation Exam
Preview (c 2022 NCSBN, https://www.nclex.com/prepare.page) as app-ready JSON drafts.

Source: the fifth attachment (21 pages, items 97-113). Item 97 (chest tube priority
monitoring) is a repeated page from the previous PDF, already built in batch 4 as
standalone_1784030000004, and is skipped here. Item 112 (the bowtie hypoglycemia/stroke
example) is handled separately in fix_bowtie_hypoglycemia.py, which corrects the
already-published (and previously wrong/incomplete) case_1789577787012.

This leaves 14 new stand-alone items: 98-111 and 113.

Every item carries a copyright footnote, shown below the Submit button (question.footnote,
rendered by player.js), per the user's request.

The source PDF does not publish an answer key except where a screenshot happens to reveal a
selection mid-interaction (not the case for any item in this batch). Options/rationales below
reflect this session's clinical judgment applied to the transcribed stems -- NOT a verified
answer key. Flagged for clinician review before publish, especially item 101 (alcohol-based
hand rub teaching, where two of the four options are each independently defensible as
correct) and item 99 (occupational vs. physical therapy referral).
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


def preamble(text):
    return text


def screen(question):
    q = dict(question)
    q.setdefault("footnote", FOOTNOTE)
    return [{
        "step": 1,
        "question": q,
        "leftContent": {"intro": "", "tabs": []},
    }]


def base_item(item_id, title, course, unit, screens):
    return {
        "id": item_id,
        "title": title,
        "course": course,
        "unit": unit,
        "topic": unit,
        "disorder": unit,
        "isStandalone": True,
        "screens": screens,
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


# ---------------------------------------------------------------------------
# Item 98 -- Psychiatric unit: acutely symptomatic client, next intervention (Others)
# ---------------------------------------------------------------------------
item98 = base_item(
    "standalone_1790300000038",
    "Psychiatric - Schizophrenia Next Intervention (MCQ)",
    "Others", "Others",
    screen({
        "stem": "Which of the following interventions should the nurse take <b>next</b>?",
        "type": "multiple_choice",
        "preamble": preamble(
            "The nurse in the psychiatric unit has completed the morning assessment of a client. "
            "Progress notes, Day 2, 0830: withdrawn, remains in assigned client room, exhibiting "
            "blunted affect and jumbled, illogical speech, experiencing auditory hallucinations and "
            "paranoid delusions. History and Physical: third admission this year for acute signs and "
            "symptoms of mental illness; family history of schizophrenia. Orders: attend group "
            "sessions when stabilized; risperidone 4 mg p.o. daily."
        ),
        "options": opts(
            ("Encourage the client to attend 1 group session today.", False),
            ("Teach the client's family members about how to prevent a relapse.", False),
            ("Administer the prescribed dose of risperidone.", True),
            ("Prepare to discharge the client to a community treatment program.", False),
        ),
        "explanation": (
            "The client remains acutely symptomatic (withdrawn, blunted affect, illogical speech, "
            "hallucinations, delusions) and is not yet stabilized, so administering the prescribed "
            "antipsychotic (Option 3) is the next appropriate action to work toward stabilization. "
            "The order for group sessions specifically applies once the client is stabilized (Option "
            "1), which has not yet occurred. Family relapse-prevention teaching (Option 2) is "
            "appropriate later in the admission, once the client's acute symptoms are controlled, not "
            "as the next priority action. Discharge planning (Option 4) is premature for a client who "
            "is actively psychotic on day 2 of a third admission this year."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 99 -- Occupational therapy referral -> NURS 1017 Unit 6 (Musculoskeletal)
# ---------------------------------------------------------------------------
item99 = base_item(
    "standalone_1783060000007",
    "Unit 6 Stand-alone 7: Occupational Therapy Referral",
    "NURS 1017", "Unit 6 (Musculoskeletal Disorders)",
    screen({
        "stem": "The nurse should recommend a referral to an occupational therapist for the client with",
        "type": "multiple_choice",
        "preamble": preamble("The nurse is caring for the following clients."),
        "options": opts(
            ("rheumatoid arthritis (RA) who has a 2-month-old infant", True),
            ("an intertrochanteric hip fracture who works as a surgeon", False),
            ("mononucleosis who is a college student", False),
            ("tendonitis who is a professional tennis player", False),
        ),
        "explanation": (
            "Occupational therapy focuses on adapting activities of daily living and teaching joint "
            "protection and energy conservation techniques; a client with RA caring for a newborn "
            "(Option 1) benefits most from OT referral to learn adaptive techniques and equipment for "
            "infant care that protect inflamed joints. The client recovering from a hip fracture "
            "(Option 2) primarily needs physical therapy for mobility and gait training, not OT. "
            "Mononucleosis (Option 3) is a self-limited viral illness managed with rest, not requiring "
            "OT. Tendonitis in an athlete (Option 4) is generally managed with physical therapy and "
            "activity modification rather than OT."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 100 -- Suspected TB, airborne precautions (Others)
# ---------------------------------------------------------------------------
item100 = base_item(
    "standalone_1790300000039",
    "Infection Control - Airborne Precautions Room Placement (MCQ)",
    "Others", "Others",
    screen({
        "stem": "Which of the following infection control precautions should the nurse implement?",
        "type": "multiple_choice",
        "preamble": preamble(
            "The nurse is preparing to admit a client who has pleuritic chest pain and is reporting a "
            "cough productive of yellow sputum for the past 1 week. The client has a pulse oximetry "
            "reading of 90% on room air."
        ),
        "options": opts(
            ("Use a stethoscope that is designated for use with the client only.", False),
            ("Wear sterile gloves when inserting a peripheral venous access device (VAD).", False),
            ("Assign the client to a private room with monitored negative air pressure.", True),
            ("Place a box of surgical masks inside the client's room.", False),
        ),
        "explanation": (
            "A prolonged productive cough with hypoxia raises concern for an airborne infection such "
            "as tuberculosis; the client should be placed in a private room with monitored negative "
            "air pressure (Option 3), the defining room feature of airborne precautions. A "
            "client-dedicated stethoscope (Option 1) is a contact-precaution measure, not specific to "
            "this presentation. Sterile gloves for VAD insertion (Option 2) is standard aseptic "
            "technique unrelated to airborne isolation. Surgical masks kept inside the client's room "
            "(Option 4) are backward; staff should don fit-tested N95 (or higher) respirators before "
            "entering the room, and a surgical mask would be placed on the client only for source "
            "control during transport out of the room."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 101 -- Alcohol-based hand rub staff education (Others)
# ---------------------------------------------------------------------------
item101 = base_item(
    "standalone_1790300000040",
    "Infection Control - Alcohol-Based Hand Rub Staff Education (MCQ)",
    "Others", "Others",
    screen({
        "stem": "Which of the following information about alcohol-based hand rub should the nurse include?",
        "type": "multiple_choice",
        "preamble": preamble(
            "The nurse is planning a staff education program about infection control guidelines."
        ),
        "options": opts(
            ("“Use before touching medical equipment that will come in direct contact with the client.”", True),
            ("“Avoid using when moving your hands from a contaminated body site to a clean body site during client care.”", False),
            ("“Avoid using before caring for clients who have severe neutropenia.”", False),
            ("“Use after contact with body excretions that do not cause your hands to be visibly soiled.”", False),
        ),
        "explanation": (
            "Alcohol-based hand rub should be used before touching medical equipment that will have "
            "direct client contact (Option 1), one of the standard hand-hygiene moments for a "
            "clean/aseptic task. Moving from a contaminated body site to a clean body site during care "
            "(Option 2) is exactly when hand hygiene, including alcohol-based rub, should be "
            "performed, not avoided. Clients with severe neutropenia (Option 3) are at higher "
            "infection risk and hand hygiene, including alcohol-based rub, should be used more "
            "consistently around their care, not avoided. Option 4 describes an appropriate use of "
            "alcohol-based hand rub as well, but is not the single best answer here; this item is "
            "flagged for clinician review since Options 1 and 4 are each independently defensible."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 102 -- Mononucleosis assessment findings -> NURS 1021 Unit 4 (Immune)
# ---------------------------------------------------------------------------
item102 = base_item(
    "standalone_1784040000002",
    "Unit 4 Stand-alone 2: Mononucleosis Assessment Findings",
    "NURS 1021", "Unit 4 (Inflammation and Immune Disorders)",
    screen({
        "stem": "Which of the following findings would support a diagnosis of mononucleosis?",
        "type": "multiple_choice",
        "preamble": preamble("The nurse is assessing a client with suspected mononucleosis."),
        "options": opts(
            ("polyarthralgia", False),
            ("costovertebral pain", False),
            ("cervical lymphadenopathy", True),
            ("left lower quadrant (LLQ) tenderness", False),
        ),
        "explanation": (
            "Cervical lymphadenopathy (Option 3) is a classic finding in infectious mononucleosis, "
            "along with fever, pharyngitis, and fatigue. Polyarthralgia (Option 1) is not a typical "
            "mononucleosis finding. Costovertebral angle tenderness (Option 2) suggests renal "
            "pathology, not mononucleosis. Mononucleosis characteristically causes splenomegaly with "
            "left upper quadrant tenderness, not left lower quadrant tenderness (Option 4)."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 103 -- UAP delegation (Others)
# ---------------------------------------------------------------------------
item103 = base_item(
    "standalone_1790300000041",
    "Leadership - UAP Delegation of Positioning Task (MCQ)",
    "Others", "Others",
    screen({
        "stem": "It would be <b>most appropriate</b> for the nurse to assign UAP to",
        "type": "multiple_choice",
        "preamble": preamble(
            "The nurse and unlicensed assistive personnel (UAP) are caring for assigned clients."
        ),
        "options": opts(
            ("apply a continuous passive motion (CPM) device to the affected extremity of a client who had a total knee replacement", False),
            ("change the bed linens for a client who was admitted 1 hour ago following a closed-head injury and is comatose and is vomiting", False),
            ("reposition a client with hydrocephalus who has a headache and is vomiting", False),
            ("place in the prone position a client who had an above-the-knee amputation (AKA) 1 day ago", True),
        ),
        "explanation": (
            "Prone positioning of a stable client 1 day after an AKA (Option 4) is a routine, "
            "non-invasive comfort/positioning measure used to prevent hip flexion contracture and is "
            "appropriate to delegate to UAP. Applying a CPM device (Option 1) requires assessment and "
            "device setup that exceeds UAP scope. A client 1 hour after a closed-head injury who is "
            "comatose and vomiting (Option 2) is unstable and at risk for increased intracranial "
            "pressure; this client requires ongoing nursing assessment, and handling by UAP without RN "
            "evaluation is not appropriate. A client with hydrocephalus who has a new headache and "
            "vomiting (Option 3) has findings concerning for increased intracranial pressure that "
            "require nursing assessment before any positioning is delegated."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 104 -- Psychiatric group prioritization (Others)
# ---------------------------------------------------------------------------
item104 = base_item(
    "standalone_1790300000042",
    "Psychiatric - Support Group Priority to Intervene (MCQ)",
    "Others", "Others",
    screen({
        "stem": "It would be a <b>priority</b> for the nurse to intervene if the client with",
        "type": "multiple_choice",
        "preamble": preamble(
            "The nurse in the inpatient psychiatric unit is leading a support group for clients."
        ),
        "options": opts(
            ("bipolar I disorder is experiencing a manic episode, is moving the legs, and is looking around the room restlessly", True),
            ("borderline personality disorder is saying that another group member is too disturbed to be attending the session", False),
            ("major depressive disorder is sitting quietly with the eyes downcast", False),
            ("schizophrenia is rocking in place and copying the gestures of another client in the group", False),
        ),
        "explanation": (
            "The client experiencing a manic episode with increased psychomotor activity and "
            "restlessness (Option 1) is at highest risk for escalating agitation and disrupting the "
            "group, making this the priority for intervention. A comment about another member (Option "
            "2), quiet withdrawn behavior consistent with depression (Option 3), and stereotyped "
            "behavior such as echopraxia in schizophrenia (Option 4) are each expected manifestations "
            "of the stated diagnoses and do not represent an immediate safety or escalation risk to "
            "the group."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 105 -- Client rights / staff boundary violation (Others)
# ---------------------------------------------------------------------------
item105 = base_item(
    "standalone_1790300000043",
    "Psychiatric - Client Rights and Staff Boundary Violation (MCQ)",
    "Others", "Others",
    screen({
        "stem": "When the nurse meets privately with the staff member, which of the following statements would be <b>most</b> appropriate for the nurse to make to the staff member?",
        "type": "multiple_choice",
        "preamble": preamble(
            "The nurse has observed a staff member tell a client with bipolar disorder that there will "
            "be consequences for making negative comments about conditions in the facility."
        ),
        "options": opts(
            ("“Threatening a client can result in the immediate dismissal of a staff member.”", False),
            ("“Staff members who have difficulty with control issues often seek power over clients.”", False),
            ("“Clients have a right to provide feedback about services without fear of punishment.”", True),
            ("“Staff should set limits with clients in a nonjudgmental manner.”", False),
        ),
        "explanation": (
            "The core issue is the client's right to voice complaints about care or facility "
            "conditions without fear of retaliation, so the nurse's most appropriate statement centers "
            "that right (Option 3). Framing the conversation around dismissal (Option 1) is punitive "
            "and not the most therapeutic first approach in a private coaching conversation. "
            "Speculating about the staff member's psychology (Option 2) is not appropriate or "
            "professional. Reminding the staff member to set limits nonjudgmentally (Option 4) does "
            "not address the actual problem, since the staff member's statement was a threat, not a "
            "therapeutic limit."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 106 -- Prioritization, pericarditis/pulsus paradoxus -> NURS 1021 Unit 2 (Cardiovascular)
# ---------------------------------------------------------------------------
item106 = base_item(
    "standalone_1784020000005",
    "Unit 2 Stand-alone 5: Prioritization - Pulsus Paradoxus in Pericarditis",
    "NURS 1021", "Unit 2 (Cardiovascular Disorders)",
    screen({
        "stem": "The nurse should <b>first</b> assess the client",
        "type": "multiple_choice",
        "preamble": preamble(
            "The nurse has been made aware of the following client situations."
        ),
        "options": opts(
            ("with chronic obstructive pulmonary disease (COPD) who is using pursed-lip breathing after ambulating in the hallway", False),
            ("with pericarditis who has a systolic blood pressure that is 20 mm Hg higher during expiration than during inspiration", True),
            ("who had a total abdominal hysterectomy (TAH) 12 hours ago and has saturated 1 perineal pad in the past 5 hours", False),
            ("who has Guillain-Barré syndrome and has had an increase in the vital capacity over the past 4 hours", False),
        ),
        "explanation": (
            "A systolic blood pressure drop of more than 10 mm Hg during inspiration (here, 20 mm Hg "
            "higher during expiration than inspiration) is pulsus paradoxus, and in a client with "
            "pericarditis (Option 2) this is a concerning sign of cardiac tamponade, a life-threatening "
            "emergency requiring immediate assessment. Pursed-lip breathing after ambulation in a "
            "client with COPD (Option 1) is an expected, adaptive breathing pattern. Saturating 1 "
            "perineal pad over 5 hours after a TAH (Option 3) is an expected amount of postoperative "
            "drainage, not excessive bleeding. An increasing vital capacity in Guillain-Barré "
            "syndrome (Option 4) is a reassuring, improving sign, since a falling vital capacity is the "
            "finding that signals impending respiratory failure in this condition."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 107 -- Milieu management / de-escalation (Others)
# ---------------------------------------------------------------------------
item107 = base_item(
    "standalone_1790300000044",
    "Psychiatric - Milieu De-escalation During Medication Pass (MCQ)",
    "Others", "Others",
    screen({
        "stem": "Which of the following actions should the nurse take?",
        "type": "multiple_choice",
        "preamble": preamble(
            "The nurse in the psychiatric unit is administering medications when a client with "
            "borderline personality disorder approaches and asks to talk. The nurse suggests having a "
            "talk in 1 hour. The client shouts, “I'll wait, but you will be sorry!” and then picks "
            "up a pitcher of water and throws it onto the floor."
        ),
        "options": opts(
            ("Offer to listen to the client while continuing to administer the medications.", False),
            ("Suggest that the client take a p.r.n. prescribed medication for agitation.", False),
            ("Ask another nurse to finish administering the medications, and talk with the client.", True),
            ("Request assistance from several nearby staff members with controlling the client's behavior.", False),
        ),
        "explanation": (
            "Separating the tasks by asking another nurse to complete medication administration while "
            "the primary nurse gives the client focused, 1:1 attention (Option 3) allows both the "
            "medication pass and therapeutic de-escalation to occur safely, addressing the client's "
            "underlying need to be heard. Offering to listen while continuing to hand out medications "
            "(Option 1) does not give the client focused attention and does not resolve the safety "
            "concern of an agitated client during a medication pass. Suggesting a p.r.n. medication "
            "(Option 2) does not address the client's expressed need to talk and may feel punitive. "
            "Summoning several staff members (Option 4) is a show-of-force response reserved for "
            "imminent danger of harm, which has not yet been established by throwing water onto the "
            "floor; this response risks escalating rather than de-escalating the situation."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 108 -- HIV client teaching evaluation -> NURS 1021 Unit 4 (Immune)
# ---------------------------------------------------------------------------
item108 = base_item(
    "standalone_1784040000003",
    "Unit 4 Stand-alone 3: HIV Client Teaching Evaluation",
    "NURS 1021", "Unit 4 (Inflammation and Immune Disorders)",
    screen({
        "stem": "Which of the following statements by the client would require follow-up?",
        "type": "multiple_choice",
        "preamble": preamble(
            "The nurse is talking with a client who has a positive laboratory test result for human "
            "immunodeficiency virus (HIV) infection."
        ),
        "options": opts(
            ("“I try to eat a well-balanced diet.”", False),
            ("“I avoid crowds when I go outside the house.”", False),
            ("“I am taking a vitamin C tablet daily to help prevent infections.”", False),
            ("“I take echinacea every day to help improve my immune system.”", True),
        ),
        "explanation": (
            "Echinacea and other herbal immune stimulants (Option 4) are not recommended for clients "
            "who are immunocompromised, including those with HIV, both because the effect on an "
            "already dysregulated immune system is not established as beneficial and because herbal "
            "immunostimulants can interact with antiretroviral medications; this statement requires "
            "follow-up. Eating a well-balanced diet (Option 1) and avoiding crowds to reduce exposure "
            "to infection (Option 2) are appropriate self-care measures. A daily vitamin C supplement "
            "(Option 3) is a generally low-risk practice and does not require the same follow-up "
            "concern as an immune-stimulating herbal supplement."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 109 -- Informed consent staff education (SATA) (Others)
# ---------------------------------------------------------------------------
item109 = base_item(
    "standalone_1790300000045",
    "Legal - Informed Consent Staff Education (SATA)",
    "Others", "Others",
    screen({
        "stem": "Which of the following information should the nurse include? <b>Select all that apply.</b>",
        "type": "select_all",
        "preamble": preamble(
            "The nurse is planning a staff education program about informed consent."
        ),
        "options": opts(
            ("“An individual designated by a power of attorney for health care can provide informed consent despite the competency of the client.”", False),
            ("“The nurse has a duty to insist that the client repeat what has been said about a procedure for which consent is necessary.”", True),
            ("“The primary health care provider must disclose the risks if the client declines a recommended procedure.”", True),
            ("“The client should sign the consent form prior to receiving prescribed opioids.”", True),
            ("“Informed consent is not needed for emergency procedures that are in the client's best interest.”", True),
        ),
        "explanation": (
            "A health care power of attorney may consent on the client's behalf only when the client "
            "is not competent to do so; it does not override the client's own decision-making authority "
            "whenever the client remains competent, so the statement that it applies “despite the "
            "competency of the client” (Option 1) is incorrect. The nurse has a role in verifying that "
            "the client understands what was explained about a procedure, including having the client "
            "restate it in their own words (Option 2). The primary health care provider must disclose "
            "the risks of declining a recommended procedure as part of informed refusal (Option 3). "
            "Consent should be obtained before administering sedating medications such as opioids, "
            "since these can impair the client's decision-making capacity (Option 4). Informed consent "
            "is not required when immediate treatment is needed to preserve life or health and the "
            "client is unable to consent (Option 5)."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 110 -- Wrong IV fluid infusing, first action (Others)
# ---------------------------------------------------------------------------
item110 = base_item(
    "standalone_1790300000046",
    "Safety - Wrong IV Fluid Infusing First Action (MCQ)",
    "Others", "Others",
    screen({
        "stem": "Which of the following actions should the nurse take <b>first</b>?",
        "type": "multiple_choice",
        "preamble": preamble(
            "The nurse is caring for a client who has a prescription for an intravenous infusion of "
            "0.45% sodium chloride (half-strength saline). The nurse notes the client is receiving 5% "
            "dextrose in water."
        ),
        "options": opts(
            ("Change the intravenous fluid to the prescribed fluid.", False),
            ("Notify the primary health care provider.", False),
            ("Complete an incident report.", False),
            ("Assess the client.", True),
        ),
        "explanation": (
            "When a nurse discovers the wrong intravenous fluid is infusing, the first action is to "
            "assess the client (Option 4) for any signs of an adverse reaction or complication before "
            "taking further steps. Changing the fluid to the prescribed solution (Option 1), notifying "
            "the primary health care provider (Option 2), and completing an incident report (Option 3) "
            "are all appropriate subsequent actions, but the client's clinical status must be assessed "
            "first."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 111 -- Umbilical cord prolapse (Others; no OB/maternity unit in this curriculum)
# ---------------------------------------------------------------------------
item111 = base_item(
    "standalone_1790300000047",
    "Maternal-Newborn - Umbilical Cord Prolapse Priority Action (MCQ)",
    "Others", "Others",
    screen({
        "stem": "Which of the following actions should the nurse take?",
        "type": "multiple_choice",
        "preamble": preamble(
            "The nurse is caring for a client in the first stage of labor and observes that a segment "
            "of the umbilical cord is visible in the vaginal opening after rupture of the client's "
            "amniotic membranes."
        ),
        "options": opts(
            ("Instruct the client to lie on her left side.", False),
            ("Attempt to place the umbilical cord back into the uterus.", False),
            ("Assist the client into a knee-chest position.", True),
            ("Administer an intravenous tocolytic agent.", False),
        ),
        "explanation": (
            "For umbilical cord prolapse, the priority nursing action is to relieve pressure on the "
            "cord by repositioning the client into a knee-chest or Trendelenburg position (Option 3), "
            "which the nurse can implement immediately and independently. The nurse should never "
            "attempt to push the visible cord back into the uterus (Option 2), which risks further "
            "cord compression and trauma. A left side-lying position alone (Option 1) is less "
            "effective at relieving cord compression than the knee-chest position. An intravenous "
            "tocolytic agent (Option 4) may be part of the overall management to reduce contractions "
            "and pressure on the cord, but it requires a prescription and is not the nurse's first, "
            "independent action."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 113 -- Aminoglycoside, renal labs -> NURS 1021 Unit 7 (Urinary)
# ---------------------------------------------------------------------------
item113 = base_item(
    "standalone_1784070000006",
    "Unit 7 Stand-alone 6: Aminoglycoside - Renal Function Labs",
    "NURS 1021", "Unit 7 (Urinary Disorders)",
    screen({
        "stem": "Which of the following laboratory test results should the nurse review before administering the medication?",
        "type": "multiple_choice",
        "preamble": preamble("The nurse is preparing to administer an aminoglycoside."),
        "options": opts(
            ("serum electrolyte level and serum uric acid level", False),
            ("hemoglobin (Hgb) and white blood cell (WBC) count", False),
            ("serum ammonia level and serum glucose level", False),
            ("blood urea nitrogen (BUN) and serum creatinine", True),
        ),
        "explanation": (
            "Aminoglycosides are nephrotoxic, so the nurse should review blood urea nitrogen (BUN) and "
            "serum creatinine (Option 4) before administration to confirm adequate renal function and "
            "avoid drug accumulation and toxicity. Serum electrolyte and uric acid levels (Option 1), "
            "hemoglobin and WBC count (Option 2), and serum ammonia and glucose levels (Option 3) are "
            "not the primary safety labs associated with aminoglycoside nephrotoxicity."
        ),
    }),
)

if __name__ == "__main__":
    for item in [
        item98, item99, item100, item101, item102, item103, item104, item105,
        item106, item107, item108, item109, item110, item111, item113,
    ]:
        write_draft(item)
