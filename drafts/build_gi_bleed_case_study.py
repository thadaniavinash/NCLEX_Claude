"""Converts a 6-screen case study the user created (with AI help, in the style of their prior
NGN case studies) into this app's data format: a 54-year-old client with H. pylori-associated
gastritis/peptic ulcer disease that progresses to a GI bleed and hypovolemia.

The user supplied all 6 screens' stems, Nurses' Notes and Laboratory Results content, answer
options, correct answers, and full rationales via screenshots. Per the user's instruction, only
the Nurses' Notes tab (always) and Laboratory Tests tab (from screen 4 onward) are used -- the
Health History, Vital Signs, and Diagnostic Tests tabs visible in the source are not built.

Per the user's instruction, the client's profile was changed from a veteran seen at a VA
medical clinic to a client seen at a local community hospital, while keeping depression as
part of the psychosocial picture (the PTSD/military-discharge backstory specific to the veteran
framing was replaced with a non-military situational stressor -- job loss and a relationship
breakdown -- that leads to the same clinically relevant homelessness/follow-up-capacity concern
the original rationale turns on). This is the user's own original content, not sourced from the
NCSBN exam preview, so no NCSBN copyright footnote is added.
"""
import json
import os

DRAFTS_DIR = os.path.dirname(os.path.abspath(__file__))

COURSE = "NURS 1021"
UNIT = "Unit 6 (Gastrointestinal Disorders)"


def opt(text, correct):
    return {"text": text, "correct": correct}


def opts(*pairs):
    return [opt(t, c) for t, c in pairs]


def dropdown(*pairs, placeholder="Select..."):
    return {"placeholder": placeholder, "options": opts(*pairs)}


def note_p(time, text):
    return f'<p class="nurse-note-row"><span class="nurse-note-time">{time}:</span><span class="nurse-note-text">{text}</span></p>'


def lab_table(rows):
    html = ['<table class="nclex-editor-table" style="width:100%; border-collapse:collapse; margin:12px 0;"><thead><tr>',
        '<th style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;">Laboratory Test</th>',
        '<th style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;">Result</th>',
        '<th style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;">Normal Reference Range</th>',
        '</tr></thead><tbody>']
    for test, result, flag, ref in rows:
        flag_color = "#c0392b" if flag == "H" else "#1d4ed8"
        flag_html = f' <span style="color:{flag_color}; font-weight:600;">{flag}</span>' if flag else ''
        html.append(
            f'<tr><td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;"><b>{test}</b></td>'
            f'<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">{result}{flag_html}</td>'
            f'<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">{ref}</td></tr>'
        )
    html.append('</tbody></table>')
    return "".join(html)


def screen(step, question, tabs, intro):
    return {"step": step, "question": question, "leftContent": {"intro": intro, "tabs": tabs}}


INTRO = "The nurse is caring for a 54-year-old client with H. pylori-associated gastritis/peptic ulcer disease."

# ---------------------------------------------------------------------------
# Shared content
# ---------------------------------------------------------------------------
notes_1330 = (
    "Presents to the community health clinic with report of worsening epigastric pain and "
    "anorexia that have continued for the past 2 weeks. Tries to avoid foods that make pain "
    "worse, such as onions and garlic; excessive alcohol also increases pain. States has not "
    "been eating well for months since the client's partner “threw” the client out of the "
    "house after the client lost a longtime job and became depressed. Has been living in the "
    "car most nights, but stays at the homeless shelter when the weather gets too cold. Is "
    "unemployed but the client's family members sometimes give the client money to buy food or "
    "gas. Alert and oriented × 3. No adventitious breath sounds; no shortness of breath. S1 "
    "S2 present; BS present × 4. VS: T 36.6° C (97.8° F), HR 84 BPM, RR 18 bpm, BP "
    "126/78 mmHg, SpO2 95% on RA. Current wt. 68.9 kg (152 lb), ht. 175.3 cm (69 in). States "
    "that weight has been about the same for 5 years. Confirmed H. pylori +."
)
notes_1330_discharge = (
    "The client is seen by the physician and was prescribed a 10-day course of PPI-triple "
    "therapy. Health teaching was done about how to take the medication and the need for "
    "adherence to the medication regimen. The client was discharged with a follow-up clinic "
    "visit in 2 weeks."
)
notes_0815 = (
    "54-year-old client brought to the ED by ambulance after falling at the local homeless "
    "shelter. Was diagnosed with probable peptic ulcer disease last week at the community "
    "health clinic. Admits lack of adherence with prescribed PPI-triple therapy drug regimen. "
    "Currently drowsy but arousable; oriented × 2 and reporting pain of 8/10 in “stomach "
    "area.” States has had several vomiting episodes during the day. One episode of 120 mL "
    "hematemesis while in ED. VS: T 37.9° C (100.2° F), HR 110 BPM, RR 16 bpm, BP 98/56 "
    "mmHg lying position, SpO2 95% on RA."
)
notes_transfer = (
    "Client transferred to the medical unit after receiving 2 units of packed red blood cells "
    "and IV fluid resuscitation in the ED. Repeat assessment: alert and oriented × 3. No "
    "further episodes of hematemesis. VS: BP 118/70 mmHg, SpO2 97% on RA. Reports pain 4/10."
)

labs_0815 = [
    ("Blood urea nitrogen (BUN)", "8.6 mmol/L (24 mg/dL)", "H", "2.9–8.2 mmol/L (10–20 mg/dL)"),
    ("Creatinine (Cr)", "106 mcmol/L (1.2 mg/dL)", "", "53–106 mcmol/L (0.6–1.2 mg/dL)"),
    ("Sodium (Na)", "131 mmol/L (131 mEq/L)", "L", "136–145 mmol/L (136–145 mEq/L)"),
    ("Potassium (K)", "3.4 mmol/L (3.4 mEq/L)", "L", "3.5–5.0 mmol/L (3.5–5.0 mEq/L)"),
    ("Glucose", "3.9 mmol/L (74 mg/dL)", "", "3.9–6.1 mmol/L (74–106 mg/dL)"),
    ("Red blood cells (RBCs)", "4.2 × 10⁹/L (4.2 × 10⁶ mcL)", "L", "4.7–6.1 × 10⁹/L (4.7–6.1 × 10⁶ mcL)"),
    ("Hemoglobin (Hgb)", "6.95 mmol/L (11.2 g/dL)", "L", "8.7–11.2 mmol/L (14–18 g/dL)"),
    ("Hematocrit (Hct)", "36% (0.36 volume fraction)", "L", "42%–52% (0.42–0.52 volume fraction)"),
    ("White blood cells (WBCs)", "13.5 × 10⁹/L (13,500/mm³)", "H", "5.0–10.0 × 10⁹/L (5,000–10,000/mm³)"),
]
labs_transfer = [
    ("Sodium (Na)", "137 mmol/L (137 mEq/L)", "", "136–145 mmol/L (136–145 mEq/L)"),
    ("Potassium (K)", "4.0 mmol/L (4.0 mEq/L)", "", "3.5–5.0 mmol/L (3.5–5.0 mEq/L)"),
    ("Blood urea nitrogen (BUN)", "8.2 mmol/L (20 mg/dL)", "", "2.9–8.2 mmol/L (10–20 mg/dL)"),
]

tabs_s1s2 = [
    {"id": "gi_notes", "title": "Nurses' Notes", "content": note_p("1330", notes_1330)},
]
tabs_s3 = [
    {"id": "gi_notes", "title": "Nurses' Notes", "content": note_p("1330", notes_1330) + f"<p>{notes_1330_discharge}</p>" + note_p("0815", notes_0815)},
]
tabs_s4s5 = tabs_s3 + [
    {"id": "gi_labs", "title": "Laboratory Tests", "content": lab_table(labs_0815)},
]
tabs_s6 = [
    {"id": "gi_notes", "title": "Nurses' Notes", "content": note_p("1330", notes_1330) + f"<p>{notes_1330_discharge}</p>" + note_p("0815", notes_0815) + note_p("Medical Unit", notes_transfer)},
    {"id": "gi_labs", "title": "Laboratory Tests", "content": lab_table(labs_0815) + "<p><b>Medical Unit (repeat draw):</b></p>" + lab_table(labs_transfer)},
]

# ---------------------------------------------------------------------------
# Screen 1 -- Recognize Cues (select_all)
# ---------------------------------------------------------------------------
screen1 = screen(1, {
    "stem": "Which client findings would be of <b>immediate</b> concern to the nurse at this time? <b>Select all that apply.</b>",
    "type": "select_all",
    "preamble": "The nurse reviews the nurses’ note for a 54-year-old client who was seen in the community health clinic.",
    "options": opts(
        ("Worsening epigastric pain", True),
        ("Anorexia", False),
        ("Avoids foods that make pain worse", False),
        ("Has depression", False),
        ("Lives in a car", True),
        ("SpO2 95% on RA", False),
        ("H. pylori +", True),
    ),
    "explanation": (
        "The client reports worsening epigastric pain that has continued for 2 weeks. The "
        "client avoids foods that make the pain worse and notes that alcohol can aggravate the "
        "pain. However, these actions to decrease pain are not of concern at this time. "
        "Epigastric pain combined with confirmed H. pylori would be of immediate concern to the "
        "nurse because this type of bacteria can cause a number of stomach disorders, including "
        "cancer, if not treated promptly. Any treatment that is initiated would need to be "
        "carefully adhered to and followed up. However, this client has been living in a car, "
        "and may not desire or be able to follow up, which would be of immediate concern to the "
        "nurse. Having anorexia would be expected for a client who has epigastric pain, so this "
        "finding is not of immediate concern to the nurse, especially because the client's "
        "weight has been stable. The client's peripheral oxygen saturation level is normal and "
        "is not of concern. Although the client may have depression, this mental health problem "
        "is not of immediate concern but could be important later if it impacts the treatment "
        "plan."
    ),
}, tabs_s1s2, INTRO)

# ---------------------------------------------------------------------------
# Screen 2 -- Analyze Cues (dropdown_cloze, 2 independent blanks)
# ---------------------------------------------------------------------------
screen2 = screen(2, {
    "stem": "Complete the following sentence by selecting from the list of options below.",
    "type": "dropdown_cloze",
    "preamble": (
        "The nurse reviews the nurses’ note entries for a 54-year-old client who was seen "
        "in the community health clinic. The client is seen by the physician and was "
        "prescribed a 10-day course of PPI-triple therapy. Health teaching was done about how "
        "to take the medication and the need for adherence to the medication regimen. The "
        "client was discharged with a follow-up clinic visit in 2 weeks."
    ),
    "options": [opt("", False) for _ in range(2)],
    "cloze": {
        "text": "The nurse analyzes the client findings and determines that they are <b>most</b> consistent with [[drop0]] or [[drop1]].",
        "dropdowns": [
            dropdown(("Cholecystitis", False), ("Gastritis", True), ("Pancreatitis", False), ("Peptic ulcer disease", False)),
            dropdown(("Cholecystitis", False), ("Gastritis", False), ("Pancreatitis", False), ("Peptic ulcer disease", True)),
        ],
    },
    "explanation": (
        "H. pylori may be found in clients who have gastritis, peptic ulcer disease, or "
        "gastric cancer. The client has not experienced weight loss, which commonly occurs in "
        "those who have gastric cancer. Therefore, the client likely has either gastritis or "
        "peptic ulcer disease, which are both manifested by epigastric pain. The client was "
        "also started on a regimen of PPI-triple therapy, which is a combination of three "
        "antibiotics specifically prescribed to treat H. pylori. Cholecystitis is not "
        "associated with H. pylori and is characterized by right upper quadrant pain that "
        "occurs most often after eating fatty foods. Pancreatitis is also not associated with "
        "H. pylori and is characterized by left upper quadrant pain."
    ),
}, tabs_s1s2, INTRO)

# ---------------------------------------------------------------------------
# Screen 3 -- Prioritize Hypotheses (dropdown_cloze, 3 independent blanks)
# ---------------------------------------------------------------------------
screen3 = screen(3, {
    "stem": "Complete the following sentence by selecting from the lists of options below.",
    "type": "dropdown_cloze",
    "preamble": (
        "One week following the community clinic visit: the client is brought to the ED and "
        "following an assessment, the nurse documents in the Nurses’ Notes."
    ),
    "options": [opt("", False) for _ in range(3)],
    "cloze": {
        "text": "The nurse determines that the <b>priority</b> for care is to manage the client's [[drop0]] as evidenced by [[drop1]] and [[drop2]].",
        "scoreGroups": [[0, 1]],
        "dropdowns": [
            dropdown(("Pain", False), ("Hypovolemia", True), ("Vomiting", False), ("Fluid overload", False)),
            dropdown(("Hematemesis", False), ("Disorientation", False), ("Hypotension", True), ("Tachycardia", False)),
            dropdown(("Hematemesis", False), ("Disorientation", False), ("Hypotension", False), ("Tachycardia", True)),
        ],
    },
    "explanation": (
        "The assessment findings support that the client has hypovolemia (dehydration) because "
        "the client's blood pressure is low and heart rate is high to compensate for the fluid "
        "deficit by circulating less blood more often through the body. The client has lost "
        "body fluids, sodium, and potassium because of vomiting. Inadequate blood volume exerts "
        "less pressure on the walls of arterial vessels, causing a decrease in blood pressure. "
        "Although the client's pain is important to address, it can be managed once the fluid "
        "volume state is corrected. The client's vomiting can also be managed once the fluid "
        "abnormalities are addressed. The client is not at risk for fluid overload. Although "
        "hematemesis and disorientation are related to hypovolemia, hypotension and tachycardia "
        "provide direct evidence of hypovolemia."
    ),
}, tabs_s3, INTRO)

# ---------------------------------------------------------------------------
# Screen 4 -- Generate Solutions (matrix_mc)
# ---------------------------------------------------------------------------
screen4 = screen(4, {
    "stem": "For each potential nursing action below, indicate which actions are <b>Indicated</b> (needed and useful) and which actions are <b>Contraindicated</b> (possibly harmful or not useful) at this time.",
    "type": "matrix_mc",
    "preamble": (
        "One week following the community clinic visit: the client is brought to the ED and "
        "following an assessment, the nurse documents in the Nurses’ Notes. Laboratory "
        "studies are prescribed and the nurse reviews the results."
    ),
    "options": [opt("", False) for _ in range(5)],
    "matrix": {
        "rows": [
            {"text": "Give client clear liquids as tolerated", "correctIndex": 1},
            {"text": "Type and crossmatch 2 units packed RBCs", "correctIndex": 0},
            {"text": "Insert nasogastric tube (NGT) and connect to suction", "correctIndex": 0},
            {"text": "Start IV infusion with NS and 20 mEq potassium via large-bore catheter", "correctIndex": 0},
            {"text": "Begin supplemental oxygen 3 L/min via NC", "correctIndex": 0},
        ],
        "columns": ["Indicated", "Contraindicated"],
        "firstColumnHeader": "Potential Nursing Action",
    },
    "explanation": (
        "The potential nursing actions for the client's condition are directed primarily "
        "toward correcting the client's fluid and electrolyte imbalances. IV fluids would be "
        "initiated to replace vital fluids and electrolytes. A large-bore IV catheter would be "
        "inserted because the client may need a blood transfusion if bleeding does not stop. "
        "Therefore, typing and crossmatching several units of packed cells is indicated at this "
        "time in case it is needed. The client would be NPO and not be allowed to have any oral "
        "intake until the hypovolemia caused by GI bleeding and vomiting is under control. "
        "Therefore, giving clear liquids as tolerated would be contraindicated. An NGT would be "
        "inserted to decompress the stomach so that it can rest to begin the healing process "
        "and prevent additional vomiting. Clients who are hypovolemic may not have adequate "
        "oxygen to perfuse the brain and other vital organs. Therefore, providing low-flow "
        "oxygen administration would help ensure adequate organ perfusion."
    ),
}, tabs_s4s5, INTRO)

# ---------------------------------------------------------------------------
# Screen 5 -- Take Action (select_n)
# ---------------------------------------------------------------------------
screen5 = screen(5, {
    "stem": "Select <b>5</b> assessment parameters that would be <b>essential</b> for the nurse to monitor as part of the client's care.",
    "type": "select_n",
    "limit": 5,
    "preamble": (
        "The client is brought to the ED and following an assessment, the nurse documents in "
        "the Nurses’ Notes. Laboratory studies are prescribed and results are reported."
    ),
    "options": opts(
        ("Urinary output", True),
        ("Oxygen saturation", True),
        ("Oral intake", False),
        ("Blood pressure", True),
        ("Hematemesis", True),
        ("Pain intensity", True),
        ("Finger-stick blood glucose", False),
    ),
    "explanation": (
        "Monitoring client findings is an essential nursing action as part of the plan of "
        "care. For the client, who has hypovolemia, the nurse would monitor urinary output and "
        "cardiac output to ensure adequate perfusion to vital organs. Oxygen saturation helps "
        "to determine perfusion in the periphery. Blood pressure is an important indicator of "
        "blood volume and would be carefully monitored. Additional episodes of hematemesis and "
        "pain intensity would be monitored to determine whether the client's condition is "
        "improving. Oral intake would not be monitored because the client would be NPO. There "
        "is no indication that the client would need FSBG monitoring. The client's blood "
        "glucose level is 3.9 mmol/L (74 mg/dL)."
    ),
}, tabs_s4s5, INTRO)

# ---------------------------------------------------------------------------
# Screen 6 -- Evaluate Outcomes (matrix_mc)
# ---------------------------------------------------------------------------
screen6 = screen(6, {
    "stem": "Indicate whether the client is <b>Progressing</b> or <b>Not Progressing</b> by comparing the current client findings listed below with earlier findings when the client was admitted to the ED.",
    "type": "matrix_mc",
    "preamble": (
        "The nurse on the medical unit performs an admission assessment and compares current "
        "client findings with earlier findings in the Nurses’ Notes and laboratory results "
        "from when the client was admitted to the ED."
    ),
    "options": [opt("", False) for _ in range(6)],
    "matrix": {
        "rows": [
            {"text": "BP 118/70 mmHg", "correctIndex": 0},
            {"text": "SpO2 97% on RA", "correctIndex": 0},
            {"text": "Pain 4/10", "correctIndex": 0},
            {"text": "Na 137 mmol/L (137 mEq/L)", "correctIndex": 0},
            {"text": "K 4.0 mmol/L (4.0 mEq/L)", "correctIndex": 0},
            {"text": "BUN 8.2 mmol/L (20 mg/dL)", "correctIndex": 0},
        ],
        "columns": ["Progressing", "Not Progressing"],
        "firstColumnHeader": "Current Client Finding",
    },
    "explanation": (
        "All of the listed current client findings are improving, demonstrating that the "
        "client is progressing. The client's systolic blood pressure is well above 100 mmHg, "
        "and the pain level has decreased from an 8/10 to a 4/10 on a pain scale of 0 to 10 "
        "(the worst possible pain). Sodium, potassium, and BUN values have all normalized, and "
        "the SpO2 is at a normal of 95% or greater for the client's age."
    ),
}, tabs_s6, INTRO)

item = {
    "id": "case_1786060000003",
    "title": "NURS 1021 Unit 6 Case Study 3",
    "course": COURSE, "unit": UNIT, "topic": UNIT, "disorder": UNIT,
    "description": (
        "A 54-year-old client with H. pylori-associated gastritis/peptic ulcer disease that "
        "progresses to a GI bleed and hypovolemia, from a community health clinic visit "
        "through ED stabilization and transfer to the medical unit."
    ),
    "screens": [screen1, screen2, screen3, screen4, screen5, screen6],
    "availability": "all",
}

if __name__ == "__main__":
    path = os.path.join(DRAFTS_DIR, f"{item['id']}_NURS_1021_Unit_6_Case_Study_3.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(item, f, indent=2, ensure_ascii=False)
    print("wrote", path)
