"""University of Maryland - CS2 Trend: the stand-alone trend question that comes with the Tuberculosis
(medical-surgical) faculty case study (University of Maryland - CS2).

Source: "Tuberculosis DOCX" (medical-surgical), Maryland Next Gen NCLEX Test Bank Project, University of
Maryland School of Nursing, https://www.nursing.umaryland.edu/mnwc/initiatives/nextgen-nclex/nextgen-nclex-library/
(author Elizabeth Mackessy-Lloyd, DNP, RN, CNE, Hood University; September 1, 2022).

The source's trend is a grid (improved / declined / unchanged), so it is a matrix question here (the app's
"trend" type is a select-all list). Changes from the source (flag for clinician review):
- Laboratory values in SI units with the author's reference ranges converted; isoniazid 300 mg (the source's
  1000 mg exceeds the maximum daily dose), as in CS2.
- Rationale: the source says the pulse oximetry reading "has increased", but it is 95% on room air at both
  visits and is keyed Unchanged; the rationale now says unchanged. The source's extra paragraph about a daily
  medication log (not part of this question) is left out.

Usage: python3 drafts/build_umd_cs2_trend.py
"""
import json
import os

ITEM_ID = "standalone_1790776800001"
STAMP = "1790776800001"
SOURCE_URL = "https://www.nursing.umaryland.edu/mnwc/initiatives/nextgen-nclex/nextgen-nclex-library/"
FOOTNOTE = (
    "Taken from the Maryland Next Gen NCLEX Test Bank Project, University of Maryland School of Nursing: "
    "&ldquo;Tuberculosis&rdquo; medical-surgical faculty case study, stand-alone trend (Elizabeth Mackessy-Lloyd, "
    f"DNP, RN, CNE, Hood University, September 1, 2022). Available at {SOURCE_URL} (Faculty Case Studies). "
    "Laboratory values shown in SI units."
)
TH = 'border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;'
TD = 'border:1px solid #ccd8e0; padding:8px; min-width:80px; background:white; color:#1e293b;'


def note(label, text):
    return (f'<p class="nurse-note-row"><span class="nurse-note-time">{label}:</span>'
            f'<span class="nurse-note-text">{text}</span></p>')


def table(header, rows):
    head = "".join(f'<th style="{TH}">{h}</th>' for h in header)
    body = "".join("<tr>" + "".join(f'<td style="{TD}">{c}</td>' for c in r) + "</tr>" for r in rows)
    return (f'<table class="nclex-editor-table" style="width:100%; border-collapse:collapse; margin:12px 0;">'
            f"<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>")


def lab(name, rng):
    return f"<b>{name}</b><br>{rng}"


NOTES = note("April 25", (
    "Reports recent extended travel to Asia with a tour group. History of coughing, mild fatigue, and loss of "
    "appetite since return, 3 weeks ago. Complains of pain in chest of 4/10 on coughing. Reports taking an "
    "over-the-counter cough medication with limited results. VS: BP 120/76 sitting, 118/72 standing, HR 78 beats "
    "per minute and regular, T 100&deg;F (37.8&deg;C) orally, RR 20, pulse oximetry reading 95% on room air. Lung "
    "sounds are diminished bilaterally with mild crackles noted in the bases. Weight 210 lb (95 kg), BMI 30. Labs "
    "and chest X-ray obtained.")) + note("May 25", (
    "Client returns for a follow-up appointment 4 weeks after being diagnosed with a tuberculosis infection. "
    "Reports missing several doses of medication. Continues to have a productive cough and is tired most days. "
    "Rates pain with the cough at 3/10, but now has new abdominal pain.<br>"
    "VS: T 98.8&deg;F (37.1&deg;C), P 80, RR 22, BP 144/88, pulse oximetry reading 95% on room air. Repeat WBC "
    "9.0 &times; 10<sup>9</sup>/L."))

LABS = table(
    ["Laboratory Test and Reference Range", "April 25"],
    [
        [lab("White blood cell (WBC) count", "5.0&ndash;10.0 &times; 10<sup>9</sup>/L"), "12.0 &times; 10<sup>9</sup>/L"],
        [lab("Platelet count", "150&ndash;400 &times; 10<sup>9</sup>/L"), "358 &times; 10<sup>9</sup>/L"],
        [lab("Hemoglobin (Hgb)", "115&ndash;155 g/L"), "108 g/L"],
        [lab("Hematocrit (Hct)", "0.36&ndash;0.48 L/L"), "0.35 L/L"],
        [lab("Hemoglobin A1c (HbA1c)", "&lt; 5.7%"), "6.0%"],
        [lab("Cholesterol, total", "&lt; 5.2 mmol/L"), "5.7 mmol/L"],
        [lab("Aspartate aminotransferase (AST)", "9&ndash;32 U/L"), "30 U/L"],
        [lab("Alanine aminotransferase (ALT)", "19&ndash;25 U/L"), "21 U/L"],
        [lab("Sputum culture", "Negative"), "Pending"],
    ]) + table(["Diagnostic Study", "April 25"], [["<b>Chest X-ray</b>", "Moderate bilateral pleural effusion"]])

ORDERS = note("April 25", "Rifapentine 1200 mg PO daily<br>Moxifloxacin 400 mg PO daily<br>"
                          "Isoniazid 300 mg PO daily<br>Pyrazinamide 2000 mg PO daily")

rows = [("Missing several doses of medication", 1), ("Pulse oximetry reading", 2), ("Productive cough", 2),
        ("Blood pressure", 1), ("Temperature", 0), ("Fatigue", 2), ("WBC count", 0), ("Pain characteristics", 1)]

item = {
    "id": ITEM_ID,
    "title": "University of Maryland - CS2 Trend",
    "course": "Others",
    "unit": "Others",
    "topic": "Others",
    "disorder": "Others",
    "description": ("Maryland Next Gen NCLEX Test Bank Project September 1, 2022; Author: Elizabeth Mackessy-Lloyd, "
                    "DNP, RN, CNE, Hood University. Stand-alone trend for the Tuberculosis case (University of "
                    "Maryland - CS2): changes between the first visit and the 4-week follow-up."),
    "isStandalone": True,
    "availability": "all",
    # Added hidden from students until the author has reviewed it.
    "draft": True,
    "screens": [{
        "step": 1,
        "leftContent": {
            "intro": "A 48-year-old female client with tuberculosis is seen in the clinic at a 4-week follow-up appointment.",
            "tabs": [
                {"id": f"nn_{STAMP}", "title": "Nurses' Notes", "content": NOTES},
                {"id": f"labs_{STAMP}", "title": "Laboratory and Diagnostic Results", "content": LABS},
                {"id": f"orders_{STAMP}", "title": "Orders", "content": ORDERS},
            ],
        },
        "question": {
            "type": "matrix_mc",
            "preamble": "",
            "stem": ("For each finding, click to specify if the finding indicates the client's status has improved, "
                     "declined, or is unchanged."),
            "matrix": {"firstColumnHeader": "Finding", "columns": ["Improved", "Declined", "Unchanged"],
                       "rows": [{"text": t, "correctIndex": i, "correctIndices": [i]} for t, i in rows]},
            "explanation": ("The elevated blood pressure and the missed doses of medication are cause for further "
                            "assessment and client education. The new abdominal pain could be a sign of a medication "
                            "side effect or liver involvement.<br>The temperature is now normal, and the WBC count is "
                            "within normal limits.<br>The pulse oximetry reading (95% on room air), the productive "
                            "cough, and the fatigue are unchanged from the initial visit."),
            "footnote": FOOTNOTE,
        },
    }],
}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{ITEM_ID}_University_of_Maryland_-_CS2_Trend.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(item, f, indent=2, ensure_ascii=False)
print("wrote", os.path.basename(out))
