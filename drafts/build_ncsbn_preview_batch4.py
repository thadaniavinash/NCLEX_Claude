"""Builds 27 stand-alone items (Items 71-97, excluding the case study 65-70, built separately
by build_ncsbn_preview_case3.py) from the NCSBN NCLEX-RN Next Generation Exam Preview PDF
(c 2022 NCSBN), fourth attachment (Test4.pdf). Same conventions as earlier batches: every
item carries question.footnote; no source answer key exists for any of these, so every
correct answer/rationale is this session's own clinical judgment, flagged for clinician
review. Items with no matching NURS 1017/1021 unit go to course/unit "Others".
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

# 71 -- Transfusion reaction actions -> NURS 1021 Unit 1 (Blood)
items.append(base_item(
    "standalone_1784010000002", "Unit 1 Stand-alone 2: Acute Transfusion Reaction Response",
    "NURS 1021", "Unit 1 (Blood Disorders)",
    screen({
        "stem": "Which of the following actions should the nurse take? <b>Select all that apply.</b>",
        "type": "select_all",
        "preamble": "The nurse is caring for a client who is receiving a blood transfusion and states, “I feel chilled and am having back pain.”",
        "options": opts(
            ("Stop the transfusion.", True),
            ("Check the client's vital signs.", True),
            ("Notify the client's primary health care provider.", True),
            ("Return the blood and infusion tubing to the blood bank.", True),
            ("Infuse 5% dextrose in water through the intravenous catheter.", False),
            ("Administer a dose of an antiemetic prescribed p.r.n. to the client.", False),
        ),
        "explanation": (
            "Chills and back pain during a transfusion are classic signs of an acute transfusion "
            "reaction. The nurse should stop the transfusion immediately, check vital signs, notify "
            "the primary health care provider, and return the blood bag and tubing to the blood bank "
            "for reaction workup. The line should be kept open with 0.9% sodium chloride, not 5% "
            "dextrose in water (Option 5), which can cause hemolysis. An antiemetic (Option 6) does "
            "not address this client's presenting symptoms (chills and back pain, not nausea) and is "
            "not one of the immediate reaction-response actions."
        ),
    }),
))

# 72 -- TPN teaching -> NURS 1021 Unit 6 (GI)
items.append(base_item(
    "standalone_1784060000002", "Unit 6 Stand-alone 2: Total Parenteral Nutrition Teaching",
    "NURS 1021", "Unit 6 (Gastrointestinal Disorders)",
    screen({
        "stem": "Which of the following information should the nurse include? <b>Select all that apply.</b>",
        "type": "select_all",
        "preamble": "The nurse is preparing a staff education program about total parenteral nutrition (TPN).",
        "options": opts(
            ("“The TPN intravenous tubing should be changed once a week.”", False),
            ("“TPN can be administered through a peripherally inserted central catheter (PICC).”", True),
            ("“Clients receiving TPN should be weighed daily.”", True),
            ("“An infusion pump is used to deliver TPN.”", True),
            ("“Serum glucose levels should be monitored in clients receiving TPN.”", True),
        ),
        "explanation": (
            "TPN can be safely infused through a PICC line, a form of central venous access "
            "appropriate for TPN's high osmolarity. Daily weights track fluid and nutritional status. "
            "An infusion pump ensures precise, controlled delivery. Serum glucose must be monitored "
            "because of TPN's high dextrose content and hyperglycemia risk. TPN tubing must be "
            "changed every 24 hours, not weekly (Option 1), because of the high infection risk from "
            "its glucose- and lipid-rich composition."
        ),
    }),
))

# 73 -- Lithium teaching -> Others
items.append(base_item(
    "standalone_1790300000031", "Lithium Client Teaching Evaluation (MCQ)",
    "Others", "Others",
    screen({
        "stem": "Which of the following statements by the client would indicate a correct understanding of the teaching?",
        "type": "multiple_choice",
        "preamble": "The nurse has taught a client with bipolar I disorder who is experiencing a manic episode and is receiving lithium.",
        "options": opts(
            ("“I will increase my oral fluid intake to 2 to 3 L daily while taking the medication.”", True),
            ("“I will experience an improvement in my condition 5 weeks after starting the medication.”", False),
            ("“I should decrease my intake of dietary sodium after starting the medication.”", False),
            ("“I should limit time spent in a sauna to 1 hour weekly while taking the medication.”", False),
        ),
        "explanation": (
            "Maintaining generous fluid intake (2 to 3 L daily) is essential lithium teaching, since "
            "dehydration increases lithium reabsorption and raises toxicity risk. Lithium's antimanic "
            "effect is generally expected within 1 to 3 weeks, not 5 (Option 2). Decreasing sodium "
            "intake (Option 3) is dangerous and backward: low sodium causes the kidneys to retain "
            "more lithium, increasing toxicity risk; sodium intake should stay consistent. Prolonged "
            "heat exposure and sweating, such as from a sauna (Option 4), promote dehydration and "
            "should generally be avoided or closely managed, not simply “limited to 1 hour "
            "weekly” as though that were safe."
        ),
    }),
))

# 74 -- Haloperidol immediate follow-up -> Others
items.append(base_item(
    "standalone_1790300000032", "Haloperidol Immediate Follow-up Finding (MCQ)",
    "Others", "Others",
    screen({
        "stem": "Which of the following findings would require <b>immediate</b> follow-up?",
        "type": "multiple_choice",
        "preamble": "The nurse has administered haloperidol to a client with schizophrenia who is agitated.",
        "options": opts(
            ("continued lack of motivation", False),
            ("reports of muscle stiffness", True),
            ("inappropriate emotional expressions", False),
            ("difficulty focusing due to blurred vision", False),
        ),
        "explanation": (
            "Muscle stiffness after a high-potency typical antipsychotic like haloperidol raises "
            "concern for an acute extrapyramidal reaction (dystonia) or early neuroleptic malignant "
            "syndrome, both of which require immediate follow-up. Lack of motivation (Option 1) and "
            "inappropriate emotional expressions (Option 3) are negative/baseline symptoms of "
            "schizophrenia, not acute medication emergencies. Blurred vision (Option 4) is a common, "
            "less dangerous anticholinergic side effect."
        ),
    }),
))

# 75 -- Propylthiouracil teaching -> NURS 1017 Unit 11 (Endocrine)
items.append(base_item(
    "standalone_1783110000001", "Unit 11 Stand-alone 1: Propylthiouracil Client Teaching",
    "NURS 1017", "Unit 11 (Endocrine Disorders)",
    screen({
        "stem": "Which of the following information should the nurse include?",
        "type": "multiple_choice",
        "preamble": "The nurse is teaching a client who is receiving newly prescribed propylthiouracil.",
        "options": opts(
            ("“Carry emergency identification with you listing your condition and medication regimen.”", True),
            ("“The medication dose will need to be reduced if you develop agranulocytosis.”", False),
            ("“You will experience weight loss if the medication is effective.”", False),
            ("“Increase your daily intake of foods containing iodine.”", False),
        ),
        "explanation": (
            "Propylthiouracil carries a risk of agranulocytosis, so carrying emergency identification "
            "helps ensure prompt recognition and evaluation (such as a CBC) if the client develops "
            "fever or signs of infection. Agranulocytosis requires stopping the medication, not "
            "reducing the dose (Option 2). Propylthiouracil treats hyperthyroidism; as it becomes "
            "effective and the metabolism normalizes, the client would be expected to gain weight or "
            "stabilize, not continue losing weight (Option 3). Iodine intake should generally be "
            "limited, not increased, in a client on antithyroid medication (Option 4)."
        ),
    }),
))

# 76 -- Beta blocker contraindication -> NURS 1021 Unit 2 (Cardiovascular)
items.append(base_item(
    "standalone_1784020000004", "Unit 2 Stand-alone 4: Beta Blocker Contraindication",
    "NURS 1021", "Unit 2 (Cardiovascular Disorders)",
    screen({
        "stem": "Which of the following would be a contraindication to administer the medication?",
        "type": "multiple_choice",
        "preamble": "The nurse is preparing to administer a beta blocker to a client.",
        "options": opts(
            ("heart block", True),
            ("myocardial infarction (MI)", False),
            ("heart failure", False),
            ("angina pectoris", False),
        ),
        "explanation": (
            "Beta blockers are contraindicated in heart block, since they further slow "
            "atrioventricular conduction and can worsen the block. Beta blockers are actually "
            "standard, indicated therapy following an MI (Option 2) and for angina (Option 4), both "
            "of which reduce myocardial oxygen demand. Certain beta blockers are also indicated for "
            "stable chronic heart failure (Option 3); heart failure is not a blanket contraindication "
            "the way heart block is."
        ),
    }),
))

# 77 -- Informed consent staff education -> Others
items.append(base_item(
    "standalone_1790300000033", "Informed Consent Staff Education (SATA)",
    "Others", "Others",
    screen({
        "stem": "Which of the following information should the nurse include? <b>Select all that apply.</b>",
        "type": "select_all",
        "preamble": "The nurse is planning a staff education program about informed consent.",
        "options": opts(
            ("“The main value of informed consent is for protection against lawsuits.”", False),
            ("“Clients may withdraw consent after signing the informed consent form.”", True),
            ("“Clients must sign the informed consent form before receiving preprocedural medication.”", True),
            ("“Nurses witness the signing of the informed consent form to confirm that consent is voluntary.”", True),
            ("“The signed consent form serves as evidence that the informed consent process has taken place.”", True),
        ),
        "explanation": (
            "Clients retain the right to withdraw consent at any time, even after signing. Consent "
            "must be obtained before administering sedating preprocedural medication, so the client's "
            "capacity to consent is not impaired. The nurse witnessing the signature helps confirm the "
            "client is signing voluntarily and is who they say they are. The signed form documents "
            "that the informed consent process took place. The main value of informed consent is "
            "protecting the client's right to self-determination, not primarily shielding the "
            "institution from lawsuits (Option 1)."
        ),
    }),
))

# 78 -- Alendronate teaching -> NURS 1017 Unit 6 (Musculoskeletal)
items.append(base_item(
    "standalone_1783060000003", "Unit 6 Stand-alone 3: Alendronate Client Teaching",
    "NURS 1017", "Unit 6 (Musculoskeletal Disorders)",
    screen({
        "stem": "Which of the following statements by the client would indicate a correct understanding of the teaching? <b>Select all that apply.</b>",
        "type": "select_all",
        "preamble": "The nurse has taught a client who is receiving alendronate.",
        "options": opts(
            ("“I will take alendronate a half hour before I eat breakfast.”", True),
            ("“I should avoid weight-bearing exercises while taking alendronate.”", False),
            ("“I should discontinue alendronate if I experience nausea or vomiting.”", False),
            ("“I will need to remain in an upright position for 30 minutes after I take alendronate.”", True),
            ("“I should notify my primary health care provider if I experience difficulty swallowing while taking alendronate.”", True),
        ),
        "explanation": (
            "Alendronate must be taken on an empty stomach, at least 30 minutes before the first food, "
            "beverage, or other medication of the day, and the client must remain upright for at least "
            "30 minutes afterward to prevent esophageal irritation. Difficulty swallowing should be "
            "reported promptly, since it can signal esophagitis or ulceration. Weight-bearing exercise "
            "(Option 2) should be encouraged, not avoided, to support bone density. Nausea or vomiting "
            "should be reported to the primary health care provider, not managed by self-"
            "discontinuing the medication (Option 3)."
        ),
    }),
))

# 79 -- SCI indwelling catheter priority -> NURS 1021 Unit 7 (Urinary)
items.append(base_item(
    "standalone_1784070000003", "Unit 7 Stand-alone 3: Spinal Cord Injury Indwelling Catheter Care",
    "NURS 1021", "Unit 7 (Urinary Disorders)",
    screen({
        "stem": "Which of the following would be a priority for the nurse to include in the plan of care?",
        "type": "multiple_choice",
        "preamble": "The nurse is developing a plan of care for a client with a spinal cord injury at C5 who has an indwelling urethral catheter.",
        "options": opts(
            ("encouraging the client to drink 6 to 8 glasses of fluid per day", False),
            ("maintaining the urine collection bag in a dependent position", True),
            ("teaching the client about foods high in fiber", False),
            ("assessing the color of the urine output", False),
        ),
        "explanation": (
            "Keeping the urine collection bag below the level of the bladder (a dependent position) "
            "is a fundamental catheter-care priority that prevents urine reflux and reduces infection "
            "risk, and applies regardless of other considerations. Adequate fluid intake (Option 1) "
            "supports urinary health but is a general goal rather than a catheter-specific priority. "
            "High-fiber foods (Option 3) address bowel, not bladder, management. Assessing urine color "
            "(Option 4) is reasonable general monitoring but is not as fundamental a safety priority as "
            "proper drainage positioning."
        ),
    }),
))

# 80 -- Multi-client first assist -> Others
items.append(base_item(
    "standalone_1790300000034", "Care Prioritization - First Assist Among 4 Clients (MCQ)",
    "Others", "Others",
    screen({
        "stem": "The nurse should <b>first</b> assist the client who had",
        "type": "multiple_choice",
        "preamble": "The nurse has been made aware that the following 4 clients require assistance.",
        "options": opts(
            ("an abdominal hysterectomy 5 hours ago and is reporting severe incisional pain", False),
            ("a transurethral resection of the prostate (TURP) yesterday and whose catheter has become disconnected", False),
            ("a lumbar laminectomy 2 days ago and is reporting that the feet are still numb", False),
            ("a spinal cord injury at T2 two weeks ago and is currently diaphoretic and nauseated", True),
        ),
        "explanation": (
            "New diaphoresis and nausea in a client with a spinal cord injury at T2 (above T6) are "
            "classic signs of autonomic dysreflexia, a life-threatening emergency that can rapidly "
            "progress to severe hypertension and stroke if the triggering stimulus (commonly bladder "
            "distension or bowel impaction) is not identified and relieved; this client must be seen "
            "first. Severe incisional pain (Option 1) needs treatment but is not immediately life-"
            "threatening. A disconnected catheter (Option 2) is a quick fix, not an emergency. "
            "Persistent numbness 2 days after a lumbar laminectomy (Option 3) needs evaluation but is "
            "not as acutely dangerous as untreated autonomic dysreflexia."
        ),
    }),
))

# 81 -- HIV viral load teaching -> NURS 1021 Unit 4 (Immune)
items.append(base_item(
    "standalone_1784040000001", "Unit 4 Stand-alone 1: HIV Viral Load Test Teaching",
    "NURS 1021", "Unit 4 (Inflammation and Immune Disorders)",
    screen({
        "stem": "Which of the following statements by the client would indicate a correct understanding of the teaching?",
        "type": "multiple_choice",
        "preamble": "The nurse has taught a client who has a positive laboratory test result for human immunodeficiency virus (HIV) infection. The client is scheduled for a viral load test.",
        "options": opts(
            ("“The viral load test is used to determine my response to the treatment regimen I am receiving for HIV.”", True),
            ("“The viral load test can rapidly detect HIV-specific antibodies in the blood.”", False),
            ("“I will be able to decrease the dosage of my prescribed medications if my viral load is low.”", False),
            ("“I am unlikely to develop acquired immune deficiency syndrome (AIDS) if my viral load is high.”", False),
        ),
        "explanation": (
            "The viral load test measures the amount of HIV RNA in the blood and is used to monitor "
            "how well antiretroviral therapy is controlling the virus. It does not detect HIV-specific "
            "antibodies (Option 2), which is what an antibody/ELISA test does. Maintaining the full "
            "prescribed regimen, not reducing the dose, is what keeps the viral load low; reducing "
            "medication (Option 3) risks resistance and viral rebound. A high, not low, viral load "
            "(Option 4) reflects poor disease control and increases the risk of progression to AIDS."
        ),
    }),
))

# 82 -- 24-hour urine collection -> NURS 1021 Unit 7 (Urinary)
items.append(base_item(
    "standalone_1784070000004", "Unit 7 Stand-alone 4: 24-Hour Urine Collection Teaching",
    "NURS 1021", "Unit 7 (Urinary Disorders)",
    screen({
        "stem": "Which of the following information should the nurse include? <b>Select all that apply.</b>",
        "type": "select_all",
        "preamble": "The nurse is teaching a client who is scheduled for a 24-hour urine collection.",
        "options": opts(
            ("“You will be asked to urinate when starting the collection, and the initial urine will be discarded.”", True),
            ("“A sign will be posted on the bathroom door as a reminder to save your urine.”", True),
            ("“You will be asked to void at the end of the designated time period to complete the urine collection.”", True),
            ("“You should discard urine that is dark or pink in color.”", False),
            ("“The collected urine will be sent to the laboratory at the end of each shift.”", False),
        ),
        "explanation": (
            "The standard protocol discards the first void to mark the true start time, saves every "
            "void afterward, posts a reminder sign, and includes the final void at the end of the "
            "collection period. All urine must be saved regardless of its color or appearance (Option "
            "4); discarding any portion compromises the accuracy of the total collection. The complete "
            "collection is kept together (often on ice or refrigerated) and sent to the laboratory as "
            "one specimen at the end of the full 24 hours, not sent in portions at the end of each "
            "shift (Option 5)."
        ),
    }),
))

# 83 -- Diabetic foot care -> NURS 1017 Unit 11 (Endocrine)
items.append(base_item(
    "standalone_1783110000002", "Unit 11 Stand-alone 2: Diabetic Foot Care Teaching",
    "NURS 1017", "Unit 11 (Endocrine Disorders)",
    screen({
        "stem": "Which of the following statements by the client would indicate a correct understanding of the teaching? <b>Select all that apply.</b>",
        "type": "select_all",
        "preamble": "The nurse has taught a client with diabetes mellitus (type 2) about foot care.",
        "options": opts(
            ("“I will check my shoes for foreign objects prior to putting them on.”", True),
            ("“I should use a large, coarse file to remove dry skin from a bunion.”", False),
            ("“I will apply a petroleum-based ointment between my toes after bathing.”", False),
            ("“I should avoid crossing my legs to prevent decreased circulation to my feet.”", True),
            ("“I should wear new shoes for a few hours for several days until they fit well.”", True),
        ),
        "explanation": (
            "Checking shoes for foreign objects protects against unnoticed injury given possible "
            "diabetic neuropathy. Avoiding crossing the legs prevents impaired circulation to the "
            "feet. Gradually breaking in new shoes over several days prevents blisters and injury. "
            "Aggressive self-filing of a bunion or callus with a coarse file (Option 2) risks skin "
            "breakdown; this should be done by a podiatrist. Ointment applied between the toes (Option "
            "3) increases moisture and maceration risk in that area, promoting fungal infection; "
            "moisturizer should go on the tops and soles of the feet, not between the toes."
        ),
    }),
))

# 84 -- THA teaching -> NURS 1017 Unit 6 (Musculoskeletal)
items.append(base_item(
    "standalone_1783060000004", "Unit 6 Stand-alone 4: Total Hip Arthroplasty Teaching",
    "NURS 1017", "Unit 6 (Musculoskeletal Disorders)",
    screen({
        "stem": "Which of the following information should the nurse include? <b>Select all that apply.</b>",
        "type": "select_all",
        "preamble": "The nurse is teaching a client who is scheduled for a total hip arthroplasty via a posterior approach.",
        "options": opts(
            ("“The type of prosthesis used is based on the muscle strength and joint function of your upper extremities.”", False),
            ("“Do not bend the affected hip more than 90 degrees after surgery.”", True),
            ("“Skin preparation and cleansing is mandatory before surgery.”", True),
            ("“Use an elevated toilet seat for at least 6 weeks after surgery.”", True),
            ("“You can resume sexual intercourse after surgery if your partner is in a dependent position.”", False),
        ),
        "explanation": (
            "Posterior-approach hip precautions include avoiding hip flexion beyond 90 degrees and "
            "using an elevated toilet seat to help maintain that precaution; pre-operative skin "
            "preparation and cleansing is standard surgical teaching. Prosthesis selection is based on "
            "the hip and lower-extremity anatomy and function, not the upper extremities (Option 1). "
            "Resuming intercourse safely depends on the client's own hip positioning to avoid excessive "
            "flexion, adduction, or internal rotation, not on the partner's position (Option 5)."
        ),
    }),
))

# 85 -- Venous spasm -> Others
items.append(base_item(
    "standalone_1790300000035", "IV Site Sharp Pain and Slowed Infusion (MCQ)",
    "Others", "Others",
    screen({
        "stem": "The nurse should recognize that the client is <b>most</b> likely experiencing",
        "type": "multiple_choice",
        "preamble": "The nurse is caring for a client who is receiving an intravenous infusion via a peripheral venous access device (VAD). The client reports sharp pain at the VAD site. The nurse notes the intravenous fluid is infusing more slowly than prescribed.",
        "options": opts(
            ("venous spasm", True),
            ("nerve damage", False),
            ("septicemia", False),
            ("hematoma", False),
        ),
        "explanation": (
            "Venous spasm, a reflexive narrowing of the vein in response to irritation, classically "
            "causes both localized sharp pain and a reduced infusion rate because the vessel lumen "
            "narrows. Nerve damage (Option 2) would cause pain but would not mechanically slow the "
            "infusion. Septicemia (Option 3) would present with systemic signs such as fever and "
            "hypotension, not an isolated site finding. A hematoma (Option 4) classically presents "
            "with localized swelling and bruising rather than sharp pain as the primary symptom."
        ),
    }),
))

# 86 -- Central VAD blood specimen -> Others
items.append(base_item(
    "standalone_1790300000036", "Central VAD Blood Specimen Collection Evaluation (MCQ)",
    "Others", "Others",
    screen({
        "stem": "Which of the following statements by the nurse would require follow-up?",
        "type": "multiple_choice",
        "preamble": "The nurse has attended a staff education program about obtaining blood specimens from a central venous access device (VAD).",
        "options": opts(
            ("“I will use a 3 mL syringe to flush the catheter port.”", True),
            ("“The injection cap should be cleansed with antiseptic and allowed to air-dry.”", False),
            ("“I will aspirate 5 mL of blood and discard the syringe in the biohazard container before obtaining the specimen.”", False),
            ("“The infusion should be turned off for at least 1 minute before the specimen is aspirated.”", False),
        ),
        "explanation": (
            "A central VAD should never be flushed with a syringe smaller than 10 mL, since a smaller "
            "syringe generates higher pressure that can rupture or otherwise damage the catheter, so "
            "this statement requires follow-up. Cleansing and air-drying the injection cap, discarding "
            "an initial waste sample before collecting the actual specimen, and briefly pausing any "
            "infusion before aspirating are all correct, standard practices."
        ),
    }),
))

# 87 -- Osteoporosis prevention post-surgical menopause -> NURS 1017 Unit 6 (Musculoskeletal)
items.append(base_item(
    "standalone_1783060000005", "Unit 6 Stand-alone 5: Osteoporosis Prevention After Surgical Menopause",
    "NURS 1017", "Unit 6 (Musculoskeletal Disorders)",
    screen({
        "stem": "Which of the following statements by the client would indicate correct understanding of the teaching?",
        "type": "multiple_choice",
        "preamble": "The nurse has taught about preventing osteoporosis to a 45-year-old client who has had a hysterectomy and bilateral salpingo-oophorectomy.",
        "options": opts(
            ("“I will begin to take dancing lessons.”", True),
            ("“I will get more rest at night.”", False),
            ("“I will take a multivitamin supplement daily.”", False),
            ("“I will add more fiber to my diet.”", False),
        ),
        "explanation": (
            "Dancing is a weight-bearing exercise, and weight-bearing exercise stimulates bone "
            "formation and is a cornerstone of osteoporosis prevention, especially important after "
            "surgical menopause removes the protective effect of estrogen. Getting more rest (Option "
            "2) and adding fiber (Option 4) are not targeted osteoporosis-prevention measures. A "
            "general multivitamin (Option 3) does not reliably provide the specific calcium and "
            "vitamin D intake that bone health requires."
        ),
    }),
))

# 88 -- VAD insertion technique -> Others
items.append(base_item(
    "standalone_1790300000037", "Peripheral VAD Insertion Technique (MCQ)",
    "Others", "Others",
    screen({
        "stem": "Which of the following actions should the nurse take?",
        "type": "multiple_choice",
        "preamble": "The nurse is preparing to insert a peripheral venous access device (VAD) for a client.",
        "options": opts(
            ("Ask the client to open and close the fist multiple times.", False),
            ("Tap the client's vein multiple times to promote dilation.", True),
            ("Apply the tourniquet 9 to 10 in (22.5 to 25 cm) above the venipuncture site.", False),
            ("Palpate for a vein after cleansing the selected site.", False),
        ),
        "explanation": (
            "Light tapping over the vein promotes venodilation and is a simple, widely endorsed "
            "technique with no downside. Repetitive fist clenching (Option 1) is now discouraged by "
            "current practice standards because it can artificially alter certain lab values (such as "
            "potassium and lactate) if blood is drawn from that site. The tourniquet should be applied "
            "closer to the site, typically about 4 to 6 in (10 to 15 cm) above it (Option 3), not 9 to "
            "10 in away. The vein should be selected and palpated before cleansing the site, not after "
            "(Option 4), since palpating after cleansing recontaminates the prepared site."
        ),
    }),
))

# 89 -- Burn injury immediate follow-up -> NURS 1017 Unit 5 (Integumentary/Burns)
items.append(base_item(
    "standalone_1783050000011", "Unit 5 Stand-alone 11: Burn Injury Immediate Follow-up Finding",
    "NURS 1017", "Unit 5 (Integumentary Disorders and Burns)",
    screen({
        "stem": "Which of the following findings would require <b>immediate</b> follow-up?",
        "type": "multiple_choice",
        "preamble": "The nurse is assessing a newly admitted client who sustained partial-thickness (second-degree) burns to the anterior thorax in a house fire.",
        "options": opts(
            ("dizziness and confusion", True),
            ("hypoactive bowel sounds and nausea", False),
            ("vesicular breath sounds throughout the lung fields", False),
            ("pain rated 5 on a scale of 0 (no pain) to 10 (severe pain)", False),
        ),
        "explanation": (
            "Dizziness and confusion in a client burned in a house fire are highly concerning for "
            "smoke inhalation injury, hypoxia, or carbon monoxide poisoning, and require immediate "
            "follow-up (assessing airway patency and obtaining a carboxyhemoglobin level). Hypoactive "
            "bowel sounds and nausea (Option 2) reflect an expected postburn stress ileus. Vesicular "
            "breath sounds (Option 3) are the normal breath sounds heard throughout most of the lung "
            "fields, not an abnormal finding. Moderate pain of 5/10 (Option 4) is expected with a burn "
            "injury and is manageable, not an emergency."
        ),
    }),
))

# 90 -- Hiatal hernia teaching -> NURS 1021 Unit 6 (GI)
items.append(base_item(
    "standalone_1784060000003", "Unit 6 Stand-alone 3: Hiatal Hernia Client Teaching",
    "NURS 1021", "Unit 6 (Gastrointestinal Disorders)",
    screen({
        "stem": "Which of the following statements by the client would indicate a correct understanding of the teaching?",
        "type": "multiple_choice",
        "preamble": "The nurse has taught a client with a hiatal hernia about interventions for the condition.",
        "options": opts(
            ("“I will consume 3 regular-sized meals daily.”", False),
            ("“Wearing an abdominal binder can help relieve symptoms.”", False),
            ("“I should elevate the head of the bed on 6 in (15 cm) blocks.”", True),
            ("“Eating foods with a high fat content will increase gastric emptying.”", False),
        ),
        "explanation": (
            "Elevating the head of the bed reduces nighttime reflux and is standard hiatal hernia/GERD "
            "teaching. Small, frequent meals are recommended instead of 3 regular-sized meals (Option "
            "1), to reduce abdominal pressure. An abdominal binder (Option 2) increases intra-"
            "abdominal pressure and would worsen symptoms. High-fat foods (Option 4) delay, rather "
            "than increase, gastric emptying, which worsens reflux risk."
        ),
    }),
))

# 91 -- Gout diagnosis support -> NURS 1017 Unit 6 (Musculoskeletal)
items.append(base_item(
    "standalone_1783060000006", "Unit 6 Stand-alone 6: Gout Assessment Findings",
    "NURS 1017", "Unit 6 (Musculoskeletal Disorders)",
    screen({
        "stem": "Which of the following findings would support a diagnosis of gout? <b>Select all that apply.</b>",
        "type": "select_all",
        "preamble": "The nurse is assessing a client with suspected gout.",
        "options": opts(
            ("elevated serum uric acid level", True),
            ("a swollen, red joint", True),
            ("reports of moderate fatigue", False),
            ("distal extremities cool to touch", False),
            ("pain associated with movement of the affected extremity", True),
            ("intolerance of dairy products", False),
        ),
        "explanation": (
            "An elevated serum uric acid level (hyperuricemia), a swollen and red joint, and pain with "
            "movement of the affected joint are all classic gout findings, reflecting acute "
            "monoarticular inflammatory arthritis from urate crystal deposition. Fatigue is a "
            "nonspecific finding not characteristic of gout. Gout causes a warm, not cool, joint, so "
            "extremities cool to touch (Option 4) do not support the diagnosis. Dairy intolerance "
            "(Option 6) is unrelated to gout."
        ),
    }),
))

# 92 -- Endometriosis diagnosis support -> NURS 1021 Unit 9 (Reproductive)
items.append(base_item(
    "standalone_1784090000002", "Unit 9 Stand-alone 2: Endometriosis Assessment Finding",
    "NURS 1021", "Unit 9 (Reproductive Disorders)",
    screen({
        "stem": "Which of the following findings would support a diagnosis of endometriosis?",
        "type": "multiple_choice",
        "preamble": "The nurse is assessing a client with suspected endometriosis.",
        "options": opts(
            ("dyspareunia", True),
            ("hot flashes", False),
            ("weight gain", False),
            ("amenorrhea", False),
        ),
        "explanation": (
            "Dyspareunia (painful intercourse) is a classic symptom of endometriosis. Hot flashes "
            "(Option 2) are associated with menopause, not endometriosis. Weight gain (Option 3) is "
            "not a characteristic endometriosis finding. Endometriosis is typically associated with "
            "dysmenorrhea and abnormal bleeding, not amenorrhea (absence of menses) (Option 4)."
        ),
    }),
))

# 93 -- Cirrhosis diagnosis support -> NURS 1021 Unit 6 (GI)
items.append(base_item(
    "standalone_1784060000004", "Unit 6 Stand-alone 4: Cirrhosis Assessment Finding",
    "NURS 1021", "Unit 6 (Gastrointestinal Disorders)",
    screen({
        "stem": "Which of the following findings would be consistent with a diagnosis of cirrhosis?",
        "type": "multiple_choice",
        "preamble": "The nurse is assessing a client with cirrhosis.",
        "options": opts(
            ("steatorrhea", False),
            ("deep vein thrombosis (DVT)", False),
            ("high fever", False),
            ("spontaneous bruising", True),
        ),
        "explanation": (
            "Spontaneous bruising is a classic cirrhosis finding, resulting from decreased synthesis "
            "of clotting factors by the diseased liver. Steatorrhea (Option 1) is more characteristic "
            "of pancreatic insufficiency or malabsorption. DVT (Option 2) is not a hallmark cirrhosis "
            "finding. High fever (Option 3) is not a defining feature of cirrhosis itself, though it "
            "can occur with a complication such as spontaneous bacterial peritonitis."
        ),
    }),
))

# 94 -- Syphilis diagnosis support -> NURS 1021 Unit 9 (Reproductive)
items.append(base_item(
    "standalone_1784090000003", "Unit 9 Stand-alone 3: Syphilis Assessment Finding",
    "NURS 1021", "Unit 9 (Reproductive Disorders)",
    screen({
        "stem": "Which of the following findings would support a diagnosis of syphilis?",
        "type": "multiple_choice",
        "preamble": "The nurse is assessing a male client who has suspected syphilis.",
        "options": opts(
            ("urethritis", False),
            ("conjunctivitis", False),
            ("chancre lesions", True),
            ("penile discharge", False),
        ),
        "explanation": (
            "A chancre, a painless genital ulcer, is the classic, pathognomonic finding of primary "
            "syphilis. Urethritis and penile discharge (Options 1 and 4) are more characteristic of "
            "gonorrhea or chlamydia. Conjunctivitis (Option 2) is not a classic syphilis finding."
        ),
    }),
))

# 95 -- Spinal shock manifestations -> NURS 1017 Unit 7 (Neurological)
items.append(base_item(
    "standalone_1783070000008", "Unit 7 Stand-alone 8: Spinal Shock Manifestations Evaluation",
    "NURS 1017", "Unit 7 (Neurological Disorders)",
    screen({
        "stem": "Follow-up is required if the nurse states that manifestations of spinal shock include",
        "type": "multiple_choice",
        "preamble": "The nurse has attended a staff education program about spinal shock following acute spinal cord injury.",
        "options": opts(
            ("bowel dysfunction", False),
            ("bladder dysfunction", False),
            ("spastic paralysis below the level of injury", True),
            ("loss of sensation below the level of injury", False),
        ),
        "explanation": (
            "Spinal shock causes flaccid, not spastic, paralysis below the level of injury, along with "
            "areflexia; spasticity typically develops later, after spinal shock resolves. This "
            "statement is incorrect and requires follow-up. Bowel dysfunction, bladder dysfunction, "
            "and loss of sensation below the level of injury are all accurate, expected manifestations "
            "of spinal shock."
        ),
    }),
))

# 96 -- AV shunt care -> NURS 1021 Unit 7 (Urinary)
items.append(base_item(
    "standalone_1784070000005", "Unit 7 Stand-alone 5: Arteriovenous Shunt Care Planning",
    "NURS 1021", "Unit 7 (Urinary Disorders)",
    screen({
        "stem": "Which of the following interventions should the nurse include in the client's plan of care?",
        "type": "multiple_choice",
        "preamble": "The nurse is planning care for a client who has an arteriovenous (AV) shunt in the left arm.",
        "options": opts(
            ("Instruct the client to protect the AV shunt by tucking the left arm under the body while sleeping.", False),
            ("Check for a bruit by palpating the AV shunt.", False),
            ("Administer prescribed intravenous fluids through the AV shunt.", False),
            ("Avoid obtaining blood pressure measurements in the arm with the AV shunt.", True),
        ),
        "explanation": (
            "Blood pressure measurements, venipuncture, and IV access should never be performed in the "
            "extremity with an AV shunt or fistula, to protect it from pressure damage or occlusion. "
            "Tucking the arm under the body (Option 1) risks compressing and occluding the shunt. A "
            "bruit is assessed by auscultation (listening), while a thrill is assessed by palpation "
            "(feeling); “checking for a bruit by palpating” (Option 2) describes the wrong "
            "technique for the wrong finding. The AV shunt is reserved exclusively for dialysis access "
            "and should not be used for routine IV fluid administration (Option 3)."
        ),
    }),
))

# 97 -- Chest tube priority monitoring -> NURS 1021 Unit 3 (Respiratory)
items.append(base_item(
    "standalone_1784030000004", "Unit 3 Stand-alone 4: Chest Tube Priority Monitoring",
    "NURS 1021", "Unit 3 (Respiratory Disorders)",
    screen({
        "stem": "It would be a priority for the nurse to monitor the client for",
        "type": "multiple_choice",
        "preamble": "The nurse is caring for a client who has a chest tube attached to a closed-chest drainage system.",
        "options": opts(
            ("tracheal deviation", True),
            ("pain at the insertion site", False),
            ("subcutaneous emphysema", False),
            ("redness or swelling at the insertion site", False),
        ),
        "explanation": (
            "Tracheal deviation signals a tension pneumothorax and mediastinal shift, a life-"
            "threatening emergency that can rapidly cause cardiovascular collapse, making it the "
            "priority finding to monitor for. Pain at the insertion site (Option 2) is an expected, "
            "manageable finding. Subcutaneous emphysema (Option 3) can occur with a chest tube and "
            "needs monitoring but is generally not as immediately life-threatening as tracheal "
            "deviation. Redness or swelling at the insertion site (Option 4) may suggest local "
            "infection but is not an acute emergency."
        ),
    }),
))

if __name__ == "__main__":
    for item in items:
        write_draft(item)
    print(f"\n{len(items)} items written.")
