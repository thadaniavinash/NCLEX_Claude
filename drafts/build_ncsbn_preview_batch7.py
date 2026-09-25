"""Builds 2 new stand-alone items from the NCSBN NCLEX-RN Next Generation Exam Preview's
"Item Type Examples" pages (c 2022 NCSBN, https://www.nclex.com/prepare.page) -- the seventh
attachment, 6 pages, showing 2 "Trend" examples and 2 "Bow-Tie" examples used to teach the
mechanics of those item types.

Trend Example 2 (page 2, a 10-day-old with projectile vomiting) and Bow-Tie Example 2 (pages
4-6, the 79-year-old with stroke-like symptoms/atrial fibrillation) are confirmed duplicates of
content already built this session (standalone_1784060000006 and case_1789577787012
respectively) -- verified independently, not just re-created, and no new files are written for
them.

The 2 new items here are Trend Example 1 (page 1) and Bow-Tie Example 1 (page 3).

Both "Bow-Tie" example pages in this PDF use a uniform light-blue "card" background across
several cells in the Potential Conditions / Actions to Take columns -- including 2 condition
cells shaded per example, which cannot both be correct in a bowtie (exactly 1 condition is
correct). This confirms the coloring is generic template/drag-card styling, not a revealed
answer (the same trap as the earlier, now-corrected, "Bowtie-Stroke" item). No coloring in this
PDF is treated as an answer reveal; every answer below is this session's own clinical
reasoning, flagged for clinician review where genuinely close.
"""
import json
import os
import re

DRAFTS_DIR = os.path.dirname(os.path.abspath(__file__))

FOOTNOTE = (
    "&copy; NCSBN. Taken from https://www.nclex.com/prepare.page; "
    "click on &#39;Download Exam Preview&#39;."
)


def opt(text, correct):
    return {"text": text, "correct": correct}


def opts(*pairs):
    return [{"text": t, "correct": c} for t, c in pairs]


def preamble(text):
    return text


def screen(question, tabs=None, intro=""):
    q = dict(question)
    q.setdefault("footnote", FOOTNOTE)
    return [{
        "step": 1,
        "question": q,
        "leftContent": {"intro": intro, "tabs": tabs or []},
    }]


def base_item(item_id, title, course, unit, screens, is_standalone=True):
    item = {
        "id": item_id,
        "title": title,
        "course": course,
        "unit": unit,
        "topic": unit,
        "disorder": unit,
        "screens": screens,
    }
    if is_standalone:
        item["isStandalone"] = True
    return item


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
# Item A -- Trend Example 1: breastfed infant, failure to thrive (dyad) (Others)
# ---------------------------------------------------------------------------
WORD_CHOICES_D0 = [
    ("fortify the breast milk", True),
    ("complete a feeding log", False),
    ("feed the client formula for 2 weeks", False),
    ("increase the parent's caloric intake", False),
    ("consult a pediatric surgeon for placement of a gastrostomy tube", False),
]
WORD_CHOICES_D1 = [
    ("fortify the breast milk", False),
    ("complete a feeding log", True),
    ("feed the client formula for 2 weeks", False),
    ("increase the parent's caloric intake", False),
    ("consult a pediatric surgeon for placement of a gastrostomy tube", False),
]

itemA = base_item(
    "standalone_1790300000055",
    "Breastfed Infant Failure to Thrive (Drag-Word Cloze)",
    "Others", "Others",
    screen({
        "stem": "Drag words from the choices below to fill in each blank in the following sentence.",
        "type": "dyad",
        "preamble": preamble(
            "The home-health nurse is caring for a 2-month-old client."
        ),
        "cloze": {
            "text": "The nurse should anticipate that the physician will instruct the parent to [[drop0]] and [[drop1]].",
            "dropdowns": [
                {"placeholder": "Word Choice", "options": opts(*WORD_CHOICES_D0)},
                {"placeholder": "Word Choice", "options": opts(*WORD_CHOICES_D1)},
            ],
        },
        "explanation": (
            "Across 3 weekly visits, the client's weight has trended steadily downward despite "
            "frequent (6 to 8 times daily) breastfeeding on demand, now totaling a 12.5% weight "
            "loss, alongside worsening lethargy -- this is failure to thrive from inadequate "
            "caloric intake. Because breastfeeding on demand makes true intake volumes difficult "
            "to quantify, the physician would first have the parent complete a feeding log to "
            "objectively track how much and how often the client is feeding. At the same time, "
            "fortifying the breast milk (adding measured calories per ounce) increases caloric "
            "density while preserving the benefits of breastfeeding, a less drastic first step "
            "than replacing breastfeeding with formula altogether. Feeding the client formula for "
            "2 weeks is a bigger change in feeding method than this trend supports as a first "
            "step, since fortifying breast milk has not yet been tried. Increasing the parent's "
            "own caloric intake does not directly address the infant's documented weight loss. "
            "Consulting a pediatric surgeon for gastrostomy tube placement is a far more invasive "
            "intervention reserved for failure to thrive that does not respond to less invasive "
            "measures, not an appropriate next step after only 3 visits."
        ),
    }),
)

# ---------------------------------------------------------------------------
# Item B -- Bow-Tie Example 1: gastrostomy tube site infection -> NURS 1021 Unit 6 (GI)
# ---------------------------------------------------------------------------
NOTES_TAB_B = (
    '<p class="nurse-note-row"><span class="nurse-note-time">0800:</span>'
    '<span class="nurse-note-text">Client admitted with increased irritability and a leaking '
    'gastrostomy feeding tube, which was placed 2 weeks ago for failure to thrive. The feeding '
    'tube insertion site, which is on the left side of the abdomen, is covered with a dressing '
    'that is saturated with old formula. On removal of the dressing, the skin surrounding the '
    'feeding tube site is erythematous and flaking, and the feeding tube is loose. At the '
    'insertion site, a small amount of thick, yellow drainage is noted. Peripheral pulses are '
    'weak. Extremities are cool to the touch. Capillary refill is 3 seconds. Client is '
    'intermittently pulling at the tube and scratching at the site. Parent reports giving the '
    'client acetaminophen last night before bedtime, but the client was still intermittently '
    'waking and irritable throughout the night. Parent attempted to feed the client through the '
    'feeding tube 8 hours ago. Vital signs: temporal T 100.6° F (38.1° C), P 171, RR 42, '
    'BP 74/62, pulse oximetry reading 97% on room air. Parent has a history of a penicillin '
    'allergy.</span></p>'
)

itemB = base_item(
    "standalone_1784060000007",
    "Unit 6 Stand-alone 7: Bowtie - Infected Gastrostomy Tube Site",
    "NURS 1021", "Unit 6 (Gastrointestinal Disorders)",
    screen({
        "stem": "Complete the diagram by dragging from the choices below to specify what condition the client is most likely experiencing, 2 actions the nurse should take to address that condition, and 2 parameters the nurse should monitor to assess the client’s progress.",
        "type": "bowtie",
        "options": [opt("", False) for _ in range(5)],
        "preamble": preamble(
            "The nurse is reviewing the client’s assessment data to prepare the client’s "
            "plan of care."
        ),
        "explanation": (
            "Thick, yellow drainage and erythematous, flaking skin at the gastrostomy tube site, "
            "together with fever, marked tachycardia (P 171), and early signs of poor perfusion "
            "(weak peripheral pulses, cool extremities, capillary refill of 3 seconds), indicate "
            "an infection of the gastrostomy tube site that is causing early systemic "
            "compromise, not simply the expected appearance of a healing site. This is not "
            "refeeding syndrome, which results from electrolyte shifts (hypophosphatemia, "
            "hypokalemia, hypomagnesemia) after reintroducing nutrition to a malnourished client "
            "and is not suggested by any finding here. The nurse should request an intravenous "
            "fluid bolus to support perfusion given the signs of early shock, and request a wound "
            "consultation given the infected, draining, loose tube site, which needs specialized "
            "evaluation beyond routine dressing care. The nurse should monitor skin integrity to "
            "track the infected site and vital signs every 30 minutes to closely track the "
            "client’s hemodynamic status while systemic compromise is a concern. Changing the "
            "site dressing is reasonable general care but is a lower-priority action than "
            "addressing perfusion and obtaining specialized wound input; obtaining an "
            "electrocardiogram is more relevant if refeeding syndrome were suspected, which it is "
            "not here; and reassuring the parent that the findings are a normal progression of "
            "healing is incorrect, since the findings described are abnormal. This item is "
            "flagged for clinician review: reasonable practice could also prioritize changing the "
            "saturated dressing among the top 2 actions."
        ),
        "bowtieParams": [
            opt("stool output", False),
            opt("skin integrity", True),
            opt("feeding tolerance", False),
            opt("vital signs every 30 minutes", True),
            opt("parent's ability to administer a tube feeding", False),
        ],
        "bowtieActions": [
            opt("change the site dressing", False),
            opt("request a wound consultation", True),
            opt("obtain an electrocardiogram (ECG)", False),
            opt("request a bolus of intravenous 0.9% sodium chloride (normal saline)", True),
            opt("reassure the parent that the site findings are the normal progression of healing", False),
        ],
        "bowtieCol1Header": "Actions to Take",
        "bowtieCol2Header": "Potential Conditions",
        "bowtieCol3Header": "Parameters to Monitor",
        "bowtieConditions": [
            opt("refeeding syndrome", False),
            opt("infection of the gastrostomy tube site", True),
            opt("normal gastrostomy tube findings", False),
            opt("intolerance to gastrostomy tube feedings", False),
        ],
        "bowtieLeftPlaceholder": "",
        "bowtieRightPlaceholder": "",
        "bowtieCenterPlaceholder": "",
    }, tabs=[
        {"id": "nn_1784060000007", "title": "Nurses' Notes", "content": NOTES_TAB_B},
    ], intro="The nurse in the pediatric unit is caring for a 6-month-old client."),
)

if __name__ == "__main__":
    for item in [itemA, itemB]:
        write_draft(item)
