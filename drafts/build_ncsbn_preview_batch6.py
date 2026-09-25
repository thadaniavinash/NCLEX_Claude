"""Builds the sixth and final batch of stand-alone items from the NCSBN NCLEX-RN Next
Generation Exam Preview (c 2022 NCSBN, https://www.nclex.com/prepare.page) as app-ready JSON
drafts.

Source: the sixth attachment (17 pages, items 114-130), all 17 stand-alone items, no case
study. The source PDF does NOT publish an answer key and contains no screenshot revealing a
mid-interaction selection or highlighted correct answer anywhere in this batch (confirmed
after an earlier batch's mistaken read of template cell shading as a revealed answer).
Options/rationales below reflect this session's own clinical judgment applied to the
transcribed stems -- NOT a verified answer key. Flagged for clinician review before publish,
especially item 118 (option 1, consent signed a week prior) and item 124 (the "best example of
correct documentation," where options 1 and 4 are each independently defensible).
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
# Item 114 -- ERCP pre-procedure teaching (SATA) -> NURS 1021 Unit 6 (GI)
# ---------------------------------------------------------------------------
item114 = base_item(
    "standalone_1784060000005",
    "Unit 6 Stand-alone 5: ERCP Pre-Procedure Questions",
    "NURS 1021", "Unit 6 (Gastrointestinal Disorders)",
    screen({
        "stem": "Which of the following questions would be important for the nurse to ask? <b>Select all that apply.</b>",
        "type": "select_all",
        "preamble": preamble(
            "The nurse is talking with a client who is scheduled for endoscopic retrograde "
            "cholangiopancreatography (ERCP) in 2 hours in the outpatient department."
        ),
        "options": opts(
            ("“How will you be getting home after the procedure?”", True),
            ("“Do you have access to a thermometer after you leave here?”", True),
            ("“What allergies do you have?”", True),
            ("“Are you wearing dentures?”", True),
            ("“Do you have external hemorrhoids?”", False),
        ),
        "explanation": (
            "ERCP is performed with sedation, so the client must arrange transportation home "
            "and should not drive (Option 1). The client should have a thermometer available at "
            "home to monitor for fever, an early sign of post-ERCP complications such as "
            "pancreatitis or cholangitis (Option 2). ERCP uses contrast dye, so allergies "
            "(particularly to iodine or shellfish) must be identified beforehand (Option 3). "
            "ERCP involves passing an endoscope through the mouth and esophagus, so dentures "
            "must be identified and removed before the procedure (Option 4). External "
            "hemorrhoids (Option 5) are unrelated to ERCP, which examines the upper "
            "gastrointestinal tract and biliary system, not the rectum or anus."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 115 -- Post cardiac catheterization findings -> NURS 1021 Unit 2 (Cardiovascular)
# ---------------------------------------------------------------------------
item115 = base_item(
    "standalone_1784020000006",
    "Unit 2 Stand-alone 6: Post-Cardiac-Catheterization Findings",
    "NURS 1021", "Unit 2 (Cardiovascular Disorders)",
    screen({
        "stem": "Which of the following findings would require <b>immediate</b> follow-up?",
        "type": "multiple_choice",
        "preamble": preamble(
            "The nurse is assessing a client who had cardiac catheterization 2 hours ago."
        ),
        "options": opts(
            ("blood pressure, 104/70 mm Hg", False),
            ("1+ pedal pulse of the affected extremity", True),
            ("heart rate, 98", False),
            ("urine output of 100 mL for the past 2 hours", False),
        ),
        "explanation": (
            "A diminished (1+) pedal pulse in the extremity used for catheter access (Option 2) "
            "requires immediate follow-up because it may indicate arterial occlusion, thrombus, "
            "or a hematoma compressing blood flow -- a vascular emergency after cardiac "
            "catheterization. A blood pressure of 104/70 mm Hg (Option 1) and a heart rate of 98 "
            "(Option 3) are within expected limits. A urine output of 100 mL over 2 hours "
            "(Option 4) is approximately 50 mL/hr, an adequate output that does not require "
            "immediate follow-up."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 116 -- Bacterial conjunctivitis parent teaching -> NURS 1017 Unit 9 (Eyes/Ears)
# ---------------------------------------------------------------------------
item116 = base_item(
    "standalone_1783090000001",
    "Unit 9 Stand-alone 1: Bacterial Conjunctivitis Parent Teaching",
    "NURS 1017", "Unit 9 (Disorders of the Eyes and Ears)",
    screen({
        "stem": "Which of the following statements by the parent would indicate a correct understanding of the teaching?",
        "type": "multiple_choice",
        "preamble": preamble(
            "The nurse has taught the parent of a 9-year-old child who has been newly diagnosed "
            "with bacterial conjunctivitis."
        ),
        "options": opts(
            ("“The infection produces profuse watery discharge.”", False),
            ("“I should clean my child’s eyelids and eyelashes with soap and water prior to instilling the medication.”", True),
            ("“My child’s eyes may be sensitive to light until the infection resolves.”", False),
            ("“The prescribed corticosteroid eyedrops should be used for 1 week.”", False),
        ),
        "explanation": (
            "Cleaning the eyelids and eyelashes with soap and water before instilling eye "
            "medication (Option 2) is correct hygiene technique that removes crusted discharge "
            "and improves medication contact with the eye. Bacterial conjunctivitis typically "
            "produces purulent (thick, yellow-green) discharge, not profuse watery discharge "
            "(Option 1), which is more characteristic of viral or allergic conjunctivitis. "
            "Photophobia (Option 3) is not a typical expected finding of bacterial "
            "conjunctivitis. Corticosteroid eyedrops (Option 4) are not the treatment for "
            "bacterial conjunctivitis, which is treated with antibiotic eyedrops; "
            "corticosteroids can worsen an untreated infection."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 117 -- Insulin pump teaching evaluation -> NURS 1017 Unit 11 (Endocrine)
# ---------------------------------------------------------------------------
item117 = base_item(
    "standalone_1783110000003",
    "Unit 11 Stand-alone 3: Insulin Infusion Pump Teaching Evaluation",
    "NURS 1017", "Unit 11 (Endocrine Disorders)",
    screen({
        "stem": "Which of the following statements by the client would require follow-up?",
        "type": "multiple_choice",
        "preamble": preamble(
            "The nurse is talking with a client who has diabetes mellitus (type 1) and is "
            "receiving insulin via an infusion pump."
        ),
        "options": opts(
            ("“I need a bolus dose of insulin prior to a meal.”", False),
            ("“I should refill the pump with short-duration insulin.”", False),
            ("“I can decrease serum glucose monitoring to twice daily.”", True),
            ("“I will change the infusion needle every 2 to 3 days.”", False),
        ),
        "explanation": (
            "Insulin pump therapy requires frequent blood glucose monitoring, typically 4 or "
            "more times daily, to safely adjust basal and bolus dosing and detect pump "
            "malfunction early; decreasing monitoring to twice daily (Option 3) is unsafe and "
            "requires follow-up. Requiring a bolus dose before meals (Option 1), using "
            "short-duration (rapid-acting) insulin in the pump (Option 2), and changing the "
            "infusion needle every 2 to 3 days (Option 4) are all accurate statements about "
            "correct insulin pump use."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 118 -- Informed consent, spinal fusion (SATA) (Others)
# ---------------------------------------------------------------------------
item118 = base_item(
    "standalone_1790300000048",
    "Legal - Informed Consent Follow-up Situations (SATA)",
    "Others", "Others",
    screen({
        "stem": "Which of the following situations would require follow-up? <b>Select all that apply.</b>",
        "type": "select_all",
        "preamble": preamble(
            "The nurse is caring for a client who is scheduled for a spinal fusion in 1 hour."
        ),
        "options": opts(
            ("The nurse notes that the client signed the consent form 1 week ago.", False),
            ("The nurse determines that the last analgesia the client received was yesterday afternoon.", False),
            ("The client states, “I need to find out why the surgery is needed before I sign the consent form.”", True),
            ("The nurse administers the prescribed preoperative sedation after the client signs the consent form.", False),
            ("The client states, “I am afraid to sign the consent form because I know I am going to die during the surgery.”", True),
            ("The client states, “The surgery may result in some paralysis, but the resolution of the pain is worth the risk to me.”", False),
        ),
        "explanation": (
            "A client stating a need to find out why surgery is needed before signing (Option 3) "
            "indicates the informed consent process is incomplete, since the client does not yet "
            "understand the reason for the procedure; this requires follow-up before consent is "
            "obtained. A client voicing an extreme, unaddressed fear of dying during a routine "
            "spinal fusion (Option 5) reflects unresolved distress that should be addressed before "
            "proceeding and requires follow-up. A consent form signed a week prior (Option 1) is "
            "not itself concerning absent any change in the client's condition or understanding. "
            "Analgesia received the prior afternoon (Option 2) is not close enough to the "
            "procedure to impair the client's current decision-making capacity. Administering "
            "preoperative sedation only after the consent form is signed (Option 4) is the "
            "correct sequence and does not require follow-up. A client who acknowledges the risk "
            "of paralysis but has weighed it against the benefit of pain resolution (Option 6) is "
            "demonstrating understanding of the risks, which is the goal of informed consent, not "
            "a concern requiring follow-up."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 119 -- Psychiatric unit transfer to unlocked unit (Others)
# ---------------------------------------------------------------------------
item119 = base_item(
    "standalone_1790300000049",
    "Psychiatric - Transfer to Unlocked Unit Recommendation (MCQ)",
    "Others", "Others",
    screen({
        "stem": "The charge nurse should recommend for transfer the client with",
        "type": "multiple_choice",
        "preamble": preamble(
            "The charge nurse must transfer a client from a locked psychiatric unit to an "
            "unlocked unit in order to make a bed available."
        ),
        "options": opts(
            ("depression who has suddenly become more animated and involved in unit activities", False),
            ("bipolar I disorder who is experiencing a manic episode, is disrobing, and is laughing with other clients", False),
            ("schizophrenia who is withdrawn and requires assistance with activities of daily living (ADL)", True),
            ("dementia who is delusional about being poisoned by staff members", False),
        ),
        "explanation": (
            "The client with schizophrenia who is withdrawn and needs assistance with ADLs "
            "(Option 3) presents the lowest immediate safety risk of the group -- quiet and "
            "cooperative, without acute agitation, elopement risk, or unsafe behavior -- making "
            "this client the most appropriate candidate for transfer to a less restrictive, "
            "unlocked unit. A previously depressed client who suddenly becomes markedly more "
            "animated (Option 1) is a classic warning sign for increased suicide risk and "
            "requires continued close monitoring, not transfer to a less secure unit. A client "
            "in an acute manic episode who is disrobing and disorganized (Option 2) has impaired "
            "judgment and safety awareness unsuitable for an unlocked unit. A client with "
            "dementia who has active paranoid delusions about being poisoned (Option 4) is at "
            "risk for refusing care, elopement, or agitation and needs continued close "
            "supervision."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 120 -- Infant projectile vomiting, diagnostic workup (SATA) -> NURS 1021 Unit 6 (GI)
# ---------------------------------------------------------------------------
item120 = base_item(
    "standalone_1784060000006",
    "Unit 6 Stand-alone 6: Infant Projectile Vomiting - Diagnostic Workup",
    "NURS 1021", "Unit 6 (Gastrointestinal Disorders)",
    screen({
        "stem": "Which of the following diagnostic procedures should the nurse anticipate the physician would order? <b>Select all that apply.</b>",
        "type": "select_all",
        "preamble": preamble(
            "The nurse in the emergency department (ED) is caring for a 10-day-old client with "
            "recurrent projectile vomiting after feedings, hyperactive bowel sounds, and, by the "
            "most recent assessment, a distended abdomen and inconsolable crying."
        ),
        "options": opts(
            ("barium enema", False),
            ("abdominal x-ray", True),
            ("abdominal ultrasound", True),
            ("complete metabolic panel", True),
            ("esophagogastroduodenoscopy (EGD)", False),
        ),
        "explanation": (
            "This presentation (recurrent projectile vomiting in a neonate, abdominal "
            "distention) is consistent with pyloric stenosis or another upper gastrointestinal "
            "obstructive process. Abdominal ultrasound (Option 3) is the gold-standard imaging "
            "study to visualize a thickened, elongated pylorus. An abdominal x-ray (Option 2) is "
            "a reasonable initial screen for a distended, obstructed abdomen. A complete "
            "metabolic panel (Option 4) is indicated to assess for the hypochloremic, "
            "hypokalemic metabolic alkalosis that results from repeated vomiting of gastric "
            "contents. A barium enema (Option 1) evaluates the lower gastrointestinal tract "
            "(for example, intussusception) and is not indicated for this upper "
            "gastrointestinal/gastric outlet presentation. Esophagogastroduodenoscopy (Option 5) "
            "is an invasive direct-visualization procedure that is not the standard first-line "
            "diagnostic study for suspected pyloric stenosis in an infant."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 121 -- MVC multi-injury prioritization (Others)
# ---------------------------------------------------------------------------
item121 = base_item(
    "standalone_1790300000050",
    "Trauma - MVC Multi-Injury Priority Finding (MCQ)",
    "Others", "Others",
    screen({
        "stem": "Which of the following findings should receive <b>highest</b> priority?",
        "type": "multiple_choice",
        "preamble": preamble(
            "The nurse in the emergency department (ED) is assessing a client with multiple "
            "injuries that occurred as a result of a motor vehicle collision."
        ),
        "options": opts(
            ("avulsion injury of the left index finger", False),
            ("deep laceration on the right forearm with blood oozing from the surface", False),
            ("hematoma on the left side of the neck", True),
            ("open fracture of the right tibia and fibula", False),
        ),
        "explanation": (
            "A neck hematoma (Option 3) is the highest priority because an expanding hematoma in "
            "the neck can compress the airway or major blood vessels, posing an immediate threat "
            "to life. A finger avulsion (Option 1), a forearm laceration with oozing (not "
            "actively hemorrhaging) blood (Option 2), and an open tibia-fibula fracture (Option "
            "4) are all significant injuries but are not immediately life-threatening compared to "
            "a potential airway or major vascular compromise."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 122 -- AAA new back pain prioritization -> NURS 1021 Unit 2 (Cardiovascular)
# ---------------------------------------------------------------------------
item122 = base_item(
    "standalone_1784020000007",
    "Unit 2 Stand-alone 7: Prioritization - New Back Pain in Abdominal Aortic Aneurysm",
    "NURS 1021", "Unit 2 (Cardiovascular Disorders)",
    screen({
        "stem": "The nurse should <b>first</b> assess the client",
        "type": "multiple_choice",
        "preamble": preamble(
            "The nurse has received information about assigned clients."
        ),
        "options": opts(
            ("with multiple sclerosis (MS) who had an indwelling urethral catheter removed 5 hours ago and has not been able to urinate", False),
            ("with an abdominal aortic aneurysm who reports recent onset of low back pain", True),
            ("who had coronary artery bypass graft (CABG) surgery 2 days ago and reports sternal pain when coughing", False),
            ("who has bacterial pneumonia and is requesting a cough suppressant", False),
        ),
        "explanation": (
            "New onset low back pain in a client with a known abdominal aortic aneurysm (Option "
            "2) is a classic warning sign of aneurysm expansion or impending rupture, a "
            "life-threatening emergency requiring immediate assessment. Urinary retention after "
            "recent catheter removal in a client with MS (Option 1) needs assessment but is not "
            "immediately life-threatening. Sternal pain with coughing 2 days after CABG surgery "
            "(Option 3) is an expected postoperative finding. A request for a cough suppressant "
            "in a client with bacterial pneumonia (Option 4) is a reasonable, non-urgent request."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 123 -- COPD malnutrition negligence chart review -> NURS 1021 Unit 3 (Respiratory)
# ---------------------------------------------------------------------------
item123 = base_item(
    "standalone_1784030000005",
    "Unit 3 Stand-alone 5: COPD Nutrition Documentation and Negligence Review",
    "NURS 1021", "Unit 3 (Respiratory Disorders)",
    screen({
        "stem": "Which of the following entries in the client's medical record would help <b>refute</b> the charge of negligence?",
        "type": "multiple_choice",
        "preamble": preamble(
            "The nurse that cared for a client with chronic obstructive pulmonary disease (COPD) "
            "who lost more than 10% of ideal body weight has been named in a lawsuit charging "
            "negligence."
        ),
        "options": opts(
            ("The client has been instructed to eat 3 large meals daily.", False),
            ("The client has been encouraged to maintain a high-calorie, high-protein diet.", True),
            ("The client has been encouraged to drink fluids with meals to promote digestion.", False),
            ("The client has been instructed to exercise 30 minutes before eating to improve appetite.", False),
        ),
        "explanation": (
            "Encouraging a high-calorie, high-protein diet (Option 2) is the correct, "
            "evidence-based nutritional teaching for a client with COPD at risk for malnutrition, "
            "and documentation of this teaching would help refute a claim of negligent care. "
            "Instructing the client to eat 3 large meals daily (Option 1) is incorrect teaching, "
            "since large meals can cause abdominal distention that presses on the diaphragm and "
            "worsens dyspnea; smaller, more frequent meals are recommended instead. Encouraging "
            "fluids with meals (Option 3) is also incorrect, since fluids taken with meals can "
            "cause early satiety and reduce food intake; fluids should be taken between meals. "
            "Instructing the client to exercise immediately before eating (Option 4) is incorrect, "
            "since exertion before a meal increases fatigue and dyspnea and can further reduce "
            "appetite and intake; rest before meals is recommended instead. Documentation of these "
            "3 incorrect teaching points would not help refute, and could support, a negligence "
            "claim."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 124 -- VAD documentation (Others)
# ---------------------------------------------------------------------------
item124 = base_item(
    "standalone_1790300000051",
    "Documentation - Peripheral VAD Charting Example (MCQ)",
    "Others", "Others",
    screen({
        "stem": "Which of the following would be the <b>best</b> example of correct documentation for the nurse to include in the client's medical record?",
        "type": "multiple_choice",
        "preamble": preamble(
            "The nurse is documenting care for a client who had a peripheral venous access "
            "device (VAD) inserted 10 minutes ago."
        ),
        "options": opts(
            ("22-gauge catheter inserted into the right hand.", True),
            ("Secured the site with paper tape to avoid skin tears.", False),
            ("Infusion started slowly due to reports of coolness at the site.", False),
            ("Labeled site, tubing, and intravenous fluid bag.", False),
        ),
        "explanation": (
            "Documenting the specific catheter gauge and insertion site (Option 1) is objective, "
            "factual charting -- exactly what should be recorded after a VAD insertion, without "
            "added interpretation. Stating the site was secured with paper tape “to avoid skin "
            "tears” (Option 2) adds a subjective rationale rather than simply documenting the "
            "objective action taken. Documenting that the infusion was started “slowly” "
            "(Option 3) is vague and not a quantifiable rate, and links the action to a client "
            "report without also documenting the objective assessment findings (such as site "
            "appearance) that prompted it. Labeling the site, tubing, and fluid bag (Option 4) "
            "describes a correct safety action but is flagged here for clinician review, since it "
            "is also a defensible answer to this item."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 125 -- Lab-diagnosis matching -> NURS 1021 Unit 8 (Fluid and Electrolyte)
# ---------------------------------------------------------------------------
item125 = base_item(
    "standalone_1784080000001",
    "Unit 8 Stand-alone 1: Priority Lab Monitoring by Diagnosis",
    "NURS 1021", "Unit 8 (Fluid, Electrolytes, and Acid-Base Imbalances)",
    screen({
        "stem": "It would be <b>most</b> important for the nurse to monitor",
        "type": "multiple_choice",
        "preamble": preamble("The nurse is caring for assigned clients."),
        "options": opts(
            ("serum lipase levels for the client with hypercholesterolemia", False),
            ("arterial blood gas (ABG) results for the client who has an acid-base imbalance", True),
            ("serum glucose levels for the client with diabetes insipidus (DI)", False),
            ("adrenocorticotropic hormone (ACTH) levels for the client who has a fluid imbalance", False),
        ),
        "explanation": (
            "Arterial blood gas results (Option 2) directly assess acid-base status and are the "
            "correct, matched lab for a client with an acid-base imbalance. Serum lipase (Option "
            "1) evaluates pancreatic function, not cholesterol status. Serum glucose (Option 3) "
            "is the relevant lab for diabetes mellitus, not diabetes insipidus, which is a "
            "disorder of antidiuretic hormone and water balance. ACTH (Option 4) reflects "
            "adrenal/pituitary function and is not the most directly relevant lab for a general "
            "fluid imbalance."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 126 -- Collaborative conflict resolution staff education (Others)
# ---------------------------------------------------------------------------
item126 = base_item(
    "standalone_1790300000052",
    "Leadership - Collaborative Conflict Resolution Example (MCQ)",
    "Others", "Others",
    screen({
        "stem": "Which of the following would <b>best</b> describe implementation of a collaborative conflict resolution strategy?",
        "type": "multiple_choice",
        "preamble": preamble(
            "The nurse is planning a staff education program about collaborative conflict "
            "resolution strategies."
        ),
        "options": opts(
            ("“A staff nurse is working with the nurse manager and offering suggestions about an upcoming new procedure.”", False),
            ("“The clinical nurse leader is flattered by being asked to help create a clinical ladder for nursing staff members.”", False),
            ("“The charge nurse is working with staff nurses and the nurse manager to develop shared goals and a plan for the new staffing format.”", True),
            ("“A new nurse has offered to work on a holiday in exchange for having the following weekend off.”", False),
        ),
        "explanation": (
            "The charge nurse working together with staff nurses and the nurse manager to "
            "develop shared goals and a plan for a potentially contentious issue (a new staffing "
            "format) (Option 3) reflects the collaborating conflict-resolution style, in which "
            "multiple stakeholders work together toward a mutually satisfying, shared outcome. "
            "Offering suggestions about a new procedure (Option 1) and being flattered by an "
            "invitation to help with a project (Option 2) do not describe an active conflict "
            "being resolved collaboratively. A nurse trading a holiday shift for a weekend off "
            "(Option 4) reflects a compromising style (a give-and-take trade-off between 2 "
            "parties), not the collaborating style, which involves shared goal-setting among "
            "multiple parties."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 127 -- TB contact investigation (Others)
# ---------------------------------------------------------------------------
item127 = base_item(
    "standalone_1790300000053",
    "Infection Control - TB Contact Investigation (MCQ)",
    "Others", "Others",
    screen({
        "stem": "The nurse should recognize that after this notification the local health department will",
        "type": "multiple_choice",
        "preamble": preamble(
            "The nurse is caring for a client who lives with a spouse and 2 adolescent children "
            "and who has been admitted to a hospital for treatment of active pulmonary "
            "tuberculosis (TB). The local health department has been notified about the client's "
            "diagnosis."
        ),
        "options": opts(
            ("schedule periodic examinations of the client's chest and sputum", False),
            ("contact the client's family to arrange for family members to be examined", True),
            ("immunize those persons with whom the client has been in contact", False),
            ("isolate members of the client's immediate family at home until diagnostic studies rule out TB", False),
        ),
        "explanation": (
            "Contact investigation is a core public health function following a reportable TB "
            "diagnosis: the health department contacts close contacts, such as household family "
            "members, to arrange examination and testing for TB exposure (Option 2). Scheduling "
            "periodic exams of the index client's own chest and sputum (Option 1) describes "
            "ongoing monitoring of the already-diagnosed client, not the health department's "
            "contact-investigation role. Routine immunization of contacts (Option 3) is not "
            "standard TB practice in the United States, where the BCG vaccine is not routinely "
            "used. Preemptively isolating asymptomatic family members at home (Option 4) is not "
            "standard practice; contacts are examined and tested, not isolated without evidence of "
            "infection."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 128 -- Disaster drill triage (Others)
# ---------------------------------------------------------------------------
item128 = base_item(
    "standalone_1790300000054",
    "Disaster Triage - Priority Client (MCQ)",
    "Others", "Others",
    screen({
        "stem": "The nurse should give <b>priority</b> for treatment to a",
        "type": "multiple_choice",
        "preamble": preamble(
            "The nurse is participating in a community-based disaster drill."
        ),
        "options": opts(
            ("2-year-old client with a bleeding scalp laceration and briskly reactive pupils", False),
            ("15-year-old client who is restless and has a distended, firm abdomen", True),
            ("30-year-old client who has a leg wound exposing the femur, a blood pressure of 120/76 mm Hg, and a pulse of 90", False),
            ("60-year-old client with heart failure whose pulse oximetry reading is 92% on room air and whose respirations are 26", False),
        ),
        "explanation": (
            "Restlessness together with a distended, firm abdomen (Option 2) suggests internal "
            "hemorrhage with early signs of hypoperfusion (restlessness reflecting altered "
            "mental status from shock), which is an immediate, life-threatening priority in "
            "disaster triage. A scalp laceration with briskly reactive pupils (Option 1) reflects "
            "an intact neurologic status and a non-life-threatening injury. An open femur wound "
            "with stable vital signs (blood pressure and pulse within normal limits) (Option 3) "
            "is a serious but not immediately life-threatening injury in this context. A pulse "
            "oximetry reading of 92% and a respiratory rate of 26 (Option 4) reflect mild "
            "respiratory compromise, less acute than the signs of impending shock in Option 2."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 129 -- Cast neurovascular compromise callback -> NURS 1017 Unit 6 (Musculoskeletal)
# ---------------------------------------------------------------------------
item129 = base_item(
    "standalone_1783060000008",
    "Unit 6 Stand-alone 8: Cast Neurovascular Compromise Telephone Triage",
    "NURS 1017", "Unit 6 (Musculoskeletal Disorders)",
    screen({
        "stem": "The nurse should <b>first</b> return the telephone call to the parent of a",
        "type": "multiple_choice",
        "preamble": preamble(
            "The nurse in a community-based setting has received the following telephone "
            "messages."
        ),
        "options": opts(
            ("3-year-old child who sustained a concussion and was irritable when awakened every 2 hours during the night", False),
            ("4-year-old child with impetigo contagiosa who has eruptions spreading around the mouth and nose that are draining thin yellow fluid", False),
            ("5-year-old child with Ewing sarcoma who is receiving external radiation and the irradiated area appears reddened", False),
            ("6-year-old child with a right long-leg cast whose toes on the affected extremity are swollen and cool to the touch", True),
        ),
        "explanation": (
            "Swollen, cool toes distal to a cast (Option 4) are signs of neurovascular compromise "
            "and possible compartment syndrome from a cast that is too tight, an urgent, "
            "limb-threatening complication requiring the first callback. Irritability when "
            "awakened for periodic neuro checks after a concussion (Option 1) is an expected part "
            "of monitoring, and being arousable is a reassuring sign. Thin yellow drainage and "
            "spreading perioral/nasal eruptions (Option 2) are the expected clinical picture of "
            "impetigo contagiosa. Redness of the skin in an irradiated area (Option 3) is an "
            "expected, anticipated side effect of external radiation therapy."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 130 -- Clopidogrel teaching -> NURS 1021 Unit 1 (Blood)
# ---------------------------------------------------------------------------
item130 = base_item(
    "standalone_1784010000003",
    "Unit 1 Stand-alone 3: Clopidogrel Client Teaching",
    "NURS 1021", "Unit 1 (Blood Disorders)",
    screen({
        "stem": "Which of the following information should the nurse include?",
        "type": "multiple_choice",
        "preamble": preamble(
            "The nurse is teaching a client who is receiving newly prescribed clopidogrel."
        ),
        "options": opts(
            ("“Notify your primary health care provider if you experience unusual bruising.”", True),
            ("“Avoid taking over-the-counter (OTC) medications containing acetaminophen.”", False),
            ("“Avoid driving your car for a short time until your response to the medication is known.”", False),
            ("“Have a blood specimen obtained every 3 months to check your serum albumin level.”", False),
        ),
        "explanation": (
            "Clopidogrel is an antiplatelet medication, so the client should report unusual "
            "bruising or bleeding to the primary health care provider (Option 1). Acetaminophen "
            "(Option 2) does not carry the same bleeding-risk interaction with clopidogrel that "
            "NSAIDs or aspirin do, so this restriction is not appropriate teaching. Clopidogrel "
            "does not cause sedation or impair driving ability, so a driving restriction (Option "
            "3) is not indicated. Routine serum albumin monitoring (Option 4) is not part of "
            "standard clopidogrel therapy monitoring."
        ),
    }),
)

if __name__ == "__main__":
    for item in [
        item114, item115, item116, item117, item118, item119, item120, item121,
        item122, item123, item124, item125, item126, item127, item128, item129, item130,
    ]:
        write_draft(item)
