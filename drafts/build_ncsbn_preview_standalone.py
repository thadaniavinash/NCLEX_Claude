"""Builds the 6 stand-alone items from the NCSBN NCLEX-RN Next Generation Exam Preview
(c 2022 NCSBN, https://www.nclex.com/prepare.page) as app-ready JSON drafts.

Source: a 10-page PDF exam preview the user attached. It contains 6 complete stand-alone
items (no published answer key) followed by the first 3 of 6 screens of an unfolding case
study (screens 4-6 are not in the source and are handled separately, in a later session).

Every item carries a copyright footnote, shown below the Submit button (question.footnote,
rendered by player.js), per the user's request:
"(c) NCSBN. Taken from https://www.nclex.com/prepare.page; click on 'Download Exam Preview'."

The source PDF does not publish an answer key. Options/rationales below reflect this
session's clinical judgment applied to the transcribed stems -- NOT a verified answer key.
Flagged for clinician review before publish, especially item 3 (ECG rhythm read from a
scanned strip graphic of uncertain calibration).
"""
import base64
import json
import os
import re

DRAFTS_DIR = os.path.dirname(os.path.abspath(__file__))
ECG_IMAGE_PATH = os.path.join(DRAFTS_DIR, "assets", "ncsbn_preview_item3_ecg.png")

# Rendered by player.js below the Submit button (question.footnote), not inline with
# the scenario text, so it stays styled/positioned consistently across all items.
FOOTNOTE = (
    "&copy; NCSBN. Taken from https://www.nclex.com/prepare.page; "
    "click on &#39;Download Exam Preview&#39;."
)


def opts(*pairs):
    return [{"text": t, "correct": c} for t, c in pairs]


def preamble(text):
    return text


def screen(question, image=None):
    q = dict(question)
    q.setdefault("footnote", FOOTNOTE)
    if image is not None:
        q["questionImage"] = image
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
# Item 1 -- OB/Labor prioritization (no matching curriculum unit -> Others)
# ---------------------------------------------------------------------------
item1 = base_item(
    "standalone_1790300000001",
    "Maternal-Newborn - Labor Stage Prioritization (MCQ)",
    "Others", "Others",
    screen({
        "stem": "The charge nurse should ask a staff member to <b>first</b> see the client in the",
        "type": "multiple_choice",
        "preamble": preamble("The charge nurse has received a change-of-shift report on the following clients in labor."),
        "options": opts(
            ("first stage of labor who has an oral temperature of 99.7&deg; F (37.6&deg; C)", False),
            ("first stage of labor whose contractions are occurring every 30 seconds", True),
            ("second stage of labor who has respirations of 26", False),
            ("second stage of labor whose contractions are lasting for 60 seconds", False),
        ),
        "explanation": (
            "Contractions occurring every 30 seconds (Option 2) indicate uterine tachysystole, which "
            "shortens the interval available for uteroplacental perfusion between contractions and places "
            "the fetus at risk for hypoxia; this finding requires the most urgent follow-up. A mildly "
            "elevated oral temperature of 99.7&deg;F (Option 1) is not acutely concerning and does not "
            "require immediate follow-up ahead of a more urgent finding. A respiratory rate of 26 during "
            "active pushing in the second stage (Option 3) is an expected finding related to the work of "
            "bearing down. Contractions lasting 60 seconds in the second stage (Option 4) are within the "
            "expected duration for that stage of labor."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 2 -- Varicella (chickenpox) airborne precautions (no matching unit -> Others)
# ---------------------------------------------------------------------------
item2 = base_item(
    "standalone_1790300000002",
    "Immune-Infection Control - Varicella Precautions (MCQ)",
    "Others", "Others",
    screen({
        "stem": "Which of the following actions by the staff member would require the nurse to intervene?",
        "type": "multiple_choice",
        "preamble": preamble("The nurse is observing a staff member caring for a client who has chickenpox."),
        "options": opts(
            ("placing the client in a private room with monitored negative air pressure", False),
            ("placing a box of disposable face shields outside the client's room", True),
            ("placing an alcohol-based hand rub in the client's room for hand hygiene", False),
            ("placing a surgical mask on the client during transport out of the client's room", False),
        ),
        "explanation": (
            "Varicella (chickenpox) requires airborne precautions. Placing disposable face shields outside "
            "the room instead of fit-tested N95 (or higher-level) respirators (Option 2) would require the "
            "nurse to intervene, because face shields alone do not filter airborne droplet nuclei and do not "
            "provide adequate respiratory protection against airborne transmission. A private room with "
            "monitored negative air pressure (Option 1) is the correct room placement for airborne "
            "precautions. An alcohol-based hand rub available in the room (Option 3) supports correct hand "
            "hygiene practice. Placing a surgical mask on the client during transport (Option 4) is "
            "appropriate source control to reduce transmission risk to others outside the room."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 3 -- Symptomatic bradycardia ECG (SATA) -> NURS 1021 Unit 2 (Cardiovascular)
# ---------------------------------------------------------------------------
with open(ECG_IMAGE_PATH, "rb") as f:
    ecg_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")

item3 = base_item(
    "standalone_1784020000001",
    "Unit 2 Stand-alone 1: Symptomatic Bradycardia (ECG Rhythm SATA)",
    "NURS 1021", "Unit 2 (Cardiovascular Disorders)",
    screen({
        "stem": "Which of the following actions would be appropriate for the nurse to take? <b>Select all that apply.</b>",
        "type": "select_all",
        "preamble": preamble(
            "The nurse is caring for a client who reports feeling faint and is experiencing the cardiac "
            "rhythm shown in the electrocardiogram (ECG) strip below."
        ),
        "options": opts(
            ("Administer the client's prescribed beta blocker.", False),
            ("Prepare for transcutaneous pacing.", True),
            ("Instruct the client to perform the Valsalva maneuver.", False),
            ("Begin chest compressions.", False),
            ("Assess the client for angina.", True),
        ),
        "explanation": (
            "The rhythm strip shows a regular, narrow-complex rhythm with a markedly slow ventricular rate "
            "consistent with symptomatic bradycardia, correlating with the client's report of feeling faint "
            "(pre-syncope from reduced cardiac output). The nurse should prepare for transcutaneous pacing "
            "(Option 2) because pacing may be required to increase heart rate and cardiac output if the "
            "client remains symptomatic. The nurse should also assess the client for angina (Option 5), "
            "since a slow heart rate can reduce coronary perfusion and precipitate ischemic chest pain, and "
            "this finding would guide further treatment. Administering a beta blocker (Option 1) is "
            "contraindicated because beta blockers further slow heart rate and conduction, worsening "
            "bradycardia. Instructing the client to perform the Valsalva maneuver (Option 3) is incorrect "
            "because vagal maneuvers slow the heart rate further and are used to treat tachyarrhythmias, not "
            "bradycardia. Beginning chest compressions (Option 4) is not indicated because the client is "
            "conscious and reporting symptoms, indicating a perfusing rhythm with a pulse; compressions are "
            "reserved for pulseless arrest."
        ),
    }, image=ecg_b64),
)

# ---------------------------------------------------------------------------
# Item 4 -- Alzheimer's disease care planning -> NURS 1017 Unit 7 (Neurological)
# ---------------------------------------------------------------------------
item4 = base_item(
    "standalone_1783070000001",
    "Unit 7 Stand-alone 1: Alzheimer's Disease Care Planning",
    "NURS 1017", "Unit 7 (Neurological Disorders)",
    screen({
        "stem": "Which of the following interventions should the nurse include in the client's plan of care?",
        "type": "multiple_choice",
        "preamble": preamble("The nurse is planning care for a client with moderate Alzheimer's disease (AD)."),
        "options": opts(
            ("Confront the client when inappropriate or agitated behaviors occur.", False),
            ("Provide the client with information about activity choices in the morning so the client can make plans for the day.", False),
            ("Encourage the client to reminisce about happy memories.", True),
            ("Administer to the client the cholinesterase inhibitor to reverse the course of AD.", False),
        ),
        "explanation": (
            "Encouraging reminiscence about happy memories (Option 3) is a therapeutic, validating "
            "intervention appropriate for a client with moderate Alzheimer's disease (AD) because long-term "
            "memories often remain accessible longer than short-term memory, and this approach reduces "
            "anxiety and supports self-esteem. Confronting the client during agitated or inappropriate "
            "behavior (Option 1) is not therapeutic and can escalate distress; redirection and a calm "
            "approach are preferred instead. Providing complex activity choices and asking the client to "
            "plan the day (Option 2) exceeds the executive functioning and decision-making capacity "
            "typically impaired in moderate AD; a simple, structured routine is more appropriate. "
            "Cholinesterase inhibitors (Option 4) may temporarily slow symptom progression for some clients "
            "but do not reverse or cure the underlying course of AD, making this statement inaccurate."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 5 -- Crutch-walking teaching -> NURS 1017 Unit 6 (Musculoskeletal)
# ---------------------------------------------------------------------------
item5 = base_item(
    "standalone_1783060000001",
    "Unit 6 Stand-alone 1: Crutch-Walking Client Teaching",
    "NURS 1017", "Unit 6 (Musculoskeletal Disorders)",
    screen({
        "stem": "Which of the following information should the nurse include?",
        "type": "multiple_choice",
        "preamble": preamble("The nurse is teaching a client how to ambulate using crutches."),
        "options": opts(
            ("“Wear slippers when ambulating with the crutches in your home.”", False),
            ("“Maintain the crutches 12 in (30 cm) in front of your feet while standing.”", False),
            ("“Adjust the hand grips of the crutches so that your elbows are fully extended.”", False),
            ("“Use your hands and arms to support your body weight.”", True),
        ),
        "explanation": (
            "Weight should be borne through the hands and arms (Option 4) rather than the axillae, to "
            "prevent axillary nerve compression and radial nerve palsy ('crutch palsy'); this is a priority "
            "safety teaching point. Slippers (Option 1) do not provide adequate traction and increase fall "
            "risk; sturdy, well-fitting, non-skid shoes should be worn instead. Positioning the crutch tips "
            "12 in (30 cm) in front of the feet (Option 2) places the base of support too far forward and "
            "increases the risk of the crutches sliding out and the client falling backward; crutch tips "
            "should be placed approximately 6 in (15 cm) in front of and to the side of each foot. Elbows "
            "fully extended at the hand grips (Option 3) prevents the client from adequately pushing off and "
            "controlling the crutches; the hand grips should instead be adjusted so the elbows are flexed "
            "approximately 15 to 30 degrees."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item 6 -- Multiple sclerosis teaching evaluation -> NURS 1017 Unit 7 (Neurological)
# ---------------------------------------------------------------------------
item6 = base_item(
    "standalone_1783070000002",
    "Unit 7 Stand-alone 2: Multiple Sclerosis Client Teaching Evaluation",
    "NURS 1017", "Unit 7 (Neurological Disorders)",
    screen({
        "stem": "Which of the following statements by the client would indicate a correct understanding of the teaching?",
        "type": "multiple_choice",
        "preamble": preamble("The nurse has taught a client with multiple sclerosis (MS)."),
        "options": opts(
            ("“I have learned how to massage my bladder to help empty my bladder completely.”", False),
            ("“I will take a hot bath in the evening to help me relax if I have had a stressful day at work.”", False),
            ("“I should expect the blurred vision to resolve after I have received medications for several weeks.”", False),
            ("“I will complete all of my household chores in the morning when I am well rested.”", True),
        ),
        "explanation": (
            "Completing tasks in the morning when the client is best rested (Option 4) reflects correct "
            "understanding of energy conservation teaching for multiple sclerosis (MS), since fatigue is a "
            "hallmark symptom that worsens as the day progresses. Bladder massage (Option 1) is not a taught "
            "or effective technique for the neurogenic bladder dysfunction seen in MS; intermittent "
            "self-catheterization or other prescribed bladder-management strategies are used instead. A hot "
            "bath in the evening (Option 2) is contraindicated because heat exposure can transiently worsen "
            "MS symptoms (Uhthoff phenomenon) through slowed nerve conduction in demyelinated fibers. "
            "Stating that blurred vision will resolve after several weeks of medication (Option 3) is "
            "inaccurate; MS is a chronic, relapsing condition, and while an acute exacerbation such as optic "
            "neuritis may improve with treatment, this is not a guaranteed or universal expected outcome."
        ),
    }),
)

if __name__ == "__main__":
    for item in [item1, item2, item3, item4, item5, item6]:
        write_draft(item)
