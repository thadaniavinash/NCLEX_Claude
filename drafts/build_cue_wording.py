"""User request, 14 Oct 2026: "cues" is not NCLEX wording. Screen 1 multiple-response questions that ask which
findings point to a condition now read "The nurse reviews the client's history and assessment. Which of the
following findings would be consistent with <condition>? Select all that apply." Rationales and other stems in
case studies that used "cue(s)" are reworded to match. Writes drafts/cue_wording_patch.json (workflow `patch`).
The image file name u5c6-inhalation-cues.svg is not shown to students and stays as it is."""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
import bank

LEAD = "The nurse reviews the client's history and assessment. Which of the following findings would be consistent with "
SATA = " <b>Select all that apply.</b>"


def stem(condition, lead=LEAD):
    return f"{lead}{condition}?{SATA}"


NEW_STEMS = {  # id -> screen 1 stem
    "case_1782370000001": stem("<b>Down syndrome</b>"),
    "case_1782370000003": stem("<b>prenatal teratogen exposure (such as Fetal Alcohol Syndrome and TORCH infection) or congenital "
                               "developmental defects</b>"),
    "case_1782380000001": stem("a <b>malignant neoplasm</b> rather than a benign tumor"),
    "case_1782380000003": stem("<b>bronchogenic malignancy with regional or metastatic spread</b>"),
    "case_1782380000004": stem("<b>bone marrow suppression (febrile neutropenia, thrombocytopenia, severe anemia) and cancer "
                               "cachexia</b>"),
    "case_1782380000005": stem("<b>paraneoplastic Syndrome of Inappropriate Antidiuretic Hormone (SIADH) and severe dilutional "
                               "hyponatremia</b>"),
    "case_1782390000002": stem("<b>impetigo</b> in Liam and <b>herpes zoster (shingles)</b> in Marcus",
                               lead="The nurse reviews the clients' histories and assessments. Which of the following findings would be "
                                    "consistent with "),
    "case_1782390000003": stem("<b>Systemic Lupus Erythematosus (SLE)</b> and inflammatory cutaneous pathology"),
    "case_1782390000004": stem("<b>inhalation injury and impending airway obstruction</b>"),
    "case_1782390000005": stem("<b>circumferential third-degree full-thickness burn injury with impending compartment syndrome</b>"),
    "case_1782370000004": stem("a <b>progressive inherited neuromuscular disorder</b>"),
    "case_1782400000001": stem("an <b>inflammatory (autoimmune) arthritis</b>"),
    # Unit 6 cases written without "cues" but in a different form; brought to the same wording.
    "case_1782400000005": stem("a <b>disorder of neuromuscular transmission</b>"),
    "case_1782400000007": stem("<b>fibromyalgia</b>"),
    "case_1782400000008": stem("<b>acute gouty arthritis</b>"),
    "case_1782400000009": stem("<b>inflammatory back pain</b> rather than mechanical (strain) back pain"),
}

# (id, screen index, field, old, new): exact phrase replacements; each old text must occur.
PHRASES = [
    ("case_1782390000003", 2, "stem", "The nurse synthesizes Maya's clinical cues and laboratory markers to prioritize systemic risks.",
     "The nurse reviews Maya's clinical findings and laboratory results to prioritize systemic risks."),
    ("case_1782350000002", 4, "explanation", "prodromal warning cues", "prodromal warning signs"),
    ("case_1782360000001", 4, "explanation", "are alarm cues suggesting", "are alarm signs suggesting"),
    ("case_1782370000002", 0, "explanation", "are phenotypic cues of Marfan syndrome", "are phenotypic features of Marfan syndrome"),
    ("case_1782370000003", 0, "explanation", "Cues indicative of prenatal teratogenic insult", "Findings indicative of prenatal teratogenic insult"),
    ("case_1782380000002", 0, "explanation", "are not cues of malignancy", "are not signs of malignancy"),
    ("case_1782380000005", 0, "explanation", "The clinical cues include:", "The consistent findings include:"),
    ("case_1782390000001", 0, "explanation", "Clinical cues of cutaneous malignancy include:", "Findings consistent with cutaneous malignancy include:"),
    ("case_1782390000004", 0, "explanation", "Critical cues of thermal inhalation injury include:",
     "Findings consistent with thermal inhalation injury include:"),
    ("case_1782390000005", 0, "explanation", "Hallmark cues include:", "Hallmark findings include:"),
    ("case_1782370000004", 0, "explanation", "<b>Correct cues:</b>", "<b>Consistent findings:</b>"),
    ("case_1782370000004", 0, "explanation", "<b>Not cues:</b>", "<b>Not consistent:</b>"),
    ("case_1782390000006", 0, "explanation", "with the inhalation injury cues labelled", "with the inhalation injury findings labelled"),
    ("case_1782390000006", 0, "explanation", "Smoke inhalation injury: D.R.'s cues from the face down to the lungs.",
     "Smoke inhalation injury: D.R.'s findings from the face down to the lungs."),
    ("case_1782390000006", 0, "explanation", "so hoarseness is a red-flag cue.", "so hoarseness is a red-flag finding."),
    ("case_1782390000006", 0, "explanation", "Why the other phrases are not airway cues", "Why the other phrases are not signs of airway compromise"),
    ("case_1782390000006", 0, "explanation", "but it is not an airway cue.", "but it is not a sign of airway compromise."),
    ("case_1782400000001", 0, "explanation", "<b>Cues of inflammatory (autoimmune) arthritis:</b>",
     "<b>Consistent with inflammatory (autoimmune) arthritis:</b>"),
    ("case_1782400000001", 0, "explanation", "<b>Not cues:</b>", "<b>Not consistent:</b>"),
    ("case_1782400000005", 0, "explanation", "<b>Not cues:</b>", "<b>Not consistent:</b>"),
    ("case_1782400000006", 0, "explanation", "<b>Not OA cues:</b>", "<b>Not consistent with OA:</b>"),
    ("case_1782400000007", 0, "explanation", "<b>Not cues:</b>", "<b>Not consistent:</b>"),
    ("case_1782400000008", 0, "explanation", "<b>Not cues:</b>", "<b>Not consistent:</b>"),
    ("case_1782400000009", 0, "explanation", "<b>Not cues:</b>", "<b>Not consistent:</b>"),
]


def main():
    cases, _ = bank.load()
    by_id = {c["id"]: c for c in cases}
    patch = {}

    def change(cid, idx, field, new):
        q = by_id[cid]["screens"][idx]["question"]
        key = (cid, idx, field)
        if key not in patch:
            patch[key] = {"row": "cases", "id": cid, "path": ["screens", idx, "question", field], "before": q[field], "after": q[field]}
        patch[key]["after"] = new

    for cid, new in NEW_STEMS.items():
        change(cid, 0, "stem", new)
    for cid, idx, field, old, new in PHRASES:
        key = (cid, idx, field)
        cur = patch[key]["after"] if key in patch else by_id[cid]["screens"][idx]["question"][field]
        if cur.count(old) != 1:
            raise SystemExit(f"{cid} S{idx + 1} {field}: expected one {old!r}, found {cur.count(old)}")
        change(cid, idx, field, cur.replace(old, new))

    out = [p for p in patch.values() if p["before"] != p["after"]]
    leftover = []
    for c in cases:
        for i, s in enumerate(c["screens"]):
            for f in ("stem", "preamble", "explanation"):
                key = (c["id"], i, f)
                text = patch[key]["after"] if key in patch else s["question"].get(f) or ""
                text = text.replace("u5c6-inhalation-cues.svg", "")
                if re.search(r"\bcues?\b", text, re.I):
                    leftover.append(f"{c['id']} S{i + 1} {f}")
    if leftover:
        raise SystemExit("still mentions cues: " + ", ".join(leftover))
    path = os.path.join(HERE, "cue_wording_patch.json")
    json.dump(out, open(path, "w"), indent=1, ensure_ascii=False)
    print(f"wrote {path}: {len(out)} field changes in {len({p['id'] for p in out})} case studies")


if __name__ == "__main__":
    main()
