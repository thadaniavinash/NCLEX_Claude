"""Converts 3 unfolding NGN case studies the user created with Claude Opus 5.5's help
(adapted from OpenStax Medical-Surgical Nursing (2024), Chapter 14 -- Integumentary System,
CC BY-NC-SA 4.0) into this app's data format.

Per the user's instruction, no NCSBN copyright footnote is added (this is not NCSBN content).
An OpenStax attribution footnote is added instead, matching the source document's own required
CC BY-NC-SA 4.0 attribution.

Source scoring notes preserved faithfully, including 2 scoring rules not previously used in
this app that required a small, backward-compatible addition to js/scoring.js's dropdown_cloze
scoring (an optional cloze.scoreGroups field: groups of blank indices scored together as one
all-or-nothing point, NCSBN "rationale dyad" style; any blank not in a group is scored
individually as before -- omitting scoreGroups leaves existing items' scoring unchanged):
  - Case 1, Item 3: 4 blanks as two independent dyad pairs (blanks 0+1, blanks 2+3), each
    pair worth 1 point only if both its blanks are correct. Max 2 points.
  - Case 3, Item 2: 5 blanks; blanks 0+1 are one dyad pair (1 point only if both correct);
    blanks 2, 3, 4 are each scored independently (1 point each). Max 4 points.
All other multi-blank dropdown_cloze items in this batch are scored independently per blank
(no scoreGroups), matching their own stated "0/1 scoring: 1 point per blank" rules.
"""
import json
import os

DRAFTS_DIR = os.path.dirname(os.path.abspath(__file__))

FOOTNOTE = (
    "Adapted from OpenStax <i>Medical-Surgical Nursing</i> (2024), Chapter 14 &mdash; "
    "Integumentary System (CC BY-NC-SA 4.0). This derivative work is licensed CC BY-NC-SA 4.0."
)

COURSE = "NURS 1017"
UNIT = "Unit 5 (Integumentary Disorders and Burns)"


def opt(text, correct):
    return {"text": text, "correct": correct}


def opts(*pairs):
    return [opt(t, c) for t, c in pairs]


def table(headers, rows, first_col=""):
    html = ['<table class="nclex-editor-table" style="width:100%; border-collapse:collapse; margin:12px 0;"><thead><tr>']
    html.append(f'<th style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;">{first_col}</th>')
    for h in headers:
        html.append(f'<th style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;">{h}</th>')
    html.append('</tr></thead><tbody>')
    for row_label, cells in rows:
        html.append('<tr>')
        html.append(f'<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;"><b>{row_label}</b></td>')
        for c in cells:
            html.append(f'<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">{c}</td>')
        html.append('</tr>')
    html.append('</tbody></table>')
    return "".join(html)


def note_p(time, text):
    return f'<p class="nurse-note-row"><span class="nurse-note-time">{time}:</span><span class="nurse-note-text">{text}</span></p>'


def dropdown(*pairs, placeholder="Select..."):
    return {"placeholder": placeholder, "options": opts(*pairs)}


def screen(step, question, tabs, intro):
    q = dict(question)
    q.setdefault("footnote", FOOTNOTE)
    return {"step": step, "question": q, "leftContent": {"intro": intro, "tabs": tabs}}


def base_item(item_id, title, screens, description):
    return {
        "id": item_id, "title": title, "course": COURSE, "unit": UNIT,
        "topic": UNIT, "disorder": UNIT, "description": description,
        "screens": screens, "availability": "all",
    }


def write_draft(item):
    path = os.path.join(DRAFTS_DIR, f"{item['id']}_{item['title'].replace(' ', '_').replace(':', '')}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(item, f, indent=2, ensure_ascii=False)
    print("wrote", path)


# =============================================================================
# CASE 1 -- Flame Burns with Suspected Inhalation Injury (D.R., 46-year-old male)
# =============================================================================
C1_INTRO = "The nurse is caring for a 46-year-old male client brought to the ED after a house fire, with suspected inhalation injury."

c1_hp = note_p("History and Physical", (
    "46-year-old male brought in by EMS after a house fire that began at approximately 0215. "
    "Firefighters found him in a smoke-filled bedroom. Medical history: hypertension "
    "(lisinopril 10 mg daily). No known drug allergies. Tetanus immunization status unknown. "
    "Stated weight 80 kg."
))

c1_vs_p1 = table(["0305"], [
    ("T", ["36.3 &deg;C"]), ("HR", ["122/min"]), ("RR", ["28/min"]), ("BP", ["104/66 mm Hg"]),
    ("SpO<sub>2</sub>", ["98% on O<sub>2</sub> 4 L/min nasal cannula (applied by EMS)"]),
    ("Pain", ["9/10 (chest)"]),
], first_col="")

c1_labs_p1 = table(["0320", "Reference range"], [
    ("Hemoglobin", ["171 g/L (17.1 g/dL)", "135&ndash;175 g/L"]),
    ("Hematocrit", ["0.53 L/L (53%)", "0.40&ndash;0.50 L/L"]),
    ("WBC", ["11.2 &times; 10<sup>9</sup>/L", "4.0&ndash;11.0 &times; 10<sup>9</sup>/L"]),
    ("Sodium", ["137 mmol/L", "135&ndash;145 mmol/L"]),
    ("Potassium", ["5.3 mmol/L", "3.5&ndash;5.0 mmol/L"]),
    ("ABG with carboxyhemoglobin", ["Drawn &mdash; pending", ""]),
], first_col="Test")

c1_notes_p1 = (
    "Client is tearful and repeatedly asking about his dog. Oriented to person only; unsure of "
    "the time or place. Reports headache and nausea. Voice is hoarse and he has a frequent "
    "cough producing black-tinged sputum. Nasal hairs and eyebrows singed; soot around the "
    "nose and mouth. Face reddened and dry without blisters. Expiratory wheezes heard "
    "bilaterally. Anterior chest and abdomen bright red and moist with intact blisters of "
    "varying size; blanches with pressure; rates chest pain 9/10. Entire right arm, "
    "circumferentially from shoulder to wrist, is waxy white and tan, dry, leathery, and "
    "nonblanchable; no pain when touched. Wearing a wedding ring on the right hand and a metal "
    "watch on the right wrist. Right radial pulse 2+; capillary refill 3 seconds."
)

c1_highlight_text = (
    "0305: Client is {tearful and repeatedly asking about his dog.} "
    "{Oriented to person only; unsure of the time or place. Reports headache and nausea.|correct} "
    "{Voice is hoarse and he has a frequent cough|correct}{producing black-tinged sputum.|correct} "
    "{Nasal hairs and eyebrows singed; soot around the nose and mouth.|correct} "
    "Face reddened and dry without blisters. "
    "{Expiratory wheezes heard bilaterally.|correct} "
    "Anterior chest and abdomen bright red and moist with intact blisters of varying size; "
    "blanches with pressure; {rates chest pain 9/10.} "
    "{Entire right arm, circumferentially from shoulder to wrist, is waxy white and tan, dry, "
    "leathery, and nonblanchable; no pain when touched.} "
    "{Wearing a wedding ring on the right hand and a metal watch on the right wrist.} "
    "Right radial pulse 2+; capillary refill 3 seconds."
)

c1_tabs_p1 = [
    {"id": "c1_hp", "title": "History and Physical", "content": c1_hp},
    {"id": "c1_vs", "title": "Vital Signs", "content": c1_vs_p1},
    {"id": "c1_labs", "title": "Laboratory Results", "content": c1_labs_p1},
]

c1_screen1 = screen(1, {
    "stem": "The nurse reviews the Nurses’ Notes. <b>Highlight</b> the findings that indicate the client is at risk for airway compromise or impaired gas exchange.",
    "type": "highlight",
    "preamble": "Phase 1 &mdash; Emergency Department, 0305.",
    "options": [opt("", False) for _ in range(5)],
    "highlightTabs": [{"id": "c1_ht1", "title": "Nurses' Notes", "content": c1_highlight_text}],
    "maxCorrectSelections": None,
    "explanation": (
        "New confusion (oriented to person only) after smoke exposure suggests cerebral hypoxia "
        "from carbon monoxide (CO) and/or impaired gas exchange. Hoarseness signals thermal "
        "injury and swelling of the larynx and upper airway; edema can progress rapidly to "
        "obstruction, so this is a red-flag cue. Black-tinged (carbonaceous) sputum shows that "
        "smoke was inhaled below the vocal cords. Singed nasal hairs and eyebrows with soot "
        "around the nose and mouth are classic external cues of smoke and heat inhalation, "
        "especially after confinement in an enclosed, smoke-filled space. Bilateral expiratory "
        "wheezes indicate bronchospasm and lower-airway irritation from inhaled smoke and "
        "chemicals. Being tearful and asking about his dog is an expected emotional response "
        "that needs support later, but is not a cue of airway or gas-exchange risk. Chest pain "
        "9/10 comes from the partial-thickness (second-degree) burn to the anterior trunk, "
        "which is very painful because nerve endings are exposed; it needs treatment, but it is "
        "not an airway cue. The circumferential full-thickness right arm burn is a circulation "
        "concern (risk for compartment syndrome), not an airway concern in this client -- a "
        "circumferential full-thickness burn of the <i>chest</i> could restrict breathing, but "
        "the arm cannot. The ring and watch on the burned arm must be removed before swelling "
        "develops (a circulation concern), but do not indicate airway risk."
    ),
}, c1_tabs_p1, C1_INTRO)
c1_screen1["leftContent"]["tabs"] = [
    {"id": "c1_hp", "title": "History and Physical", "content": c1_hp},
    {"id": "c1_vs", "title": "Vital Signs", "content": c1_vs_p1},
    {"id": "c1_labs", "title": "Laboratory Results", "content": c1_labs_p1},
    {"id": "c1_notes", "title": "Nurses' Notes", "content": ""},
]

c1_tabs_p1_full = c1_tabs_p1 + [{"id": "c1_notes", "title": "Nurses' Notes", "content": note_p("0305", c1_notes_p1)}]

c1_screen2 = screen(2, {
    "stem": "For each assessment finding, click to specify whether it is consistent with <b>upper airway (inhalation) injury</b>, <b>carbon monoxide poisoning</b>, or <b>hypovolemia related to the burn injury</b>. Each finding may support more than one condition.",
    "type": "matrix_mr",
    "preamble": "Phase 1 &mdash; Emergency Department, 0305.",
    "options": [opt("", False) for _ in range(7)],
    "matrix": {
        "rows": [
            {"text": "Hoarse voice", "correctIndices": [0]},
            {"text": "Singed nasal hairs", "correctIndices": [0]},
            {"text": "Headache and nausea", "correctIndices": [1]},
            {"text": "Oriented to person only", "correctIndices": [0, 1]},
            {"text": "SpO2 98% despite new confusion", "correctIndices": [1]},
            {"text": "HR 122/min with BP 104/66 mm Hg", "correctIndices": [2]},
            {"text": "Hematocrit 0.53 L/L (53%)", "correctIndices": [2]},
        ],
        "columns": ["Upper airway (inhalation) injury", "Carbon monoxide poisoning", "Hypovolemia related to burn"],
        "firstColumnHeader": "Finding / Action",
    },
    "explanation": (
        "Hoarse voice and singed nasal hairs are direct evidence of heat and smoke near the "
        "airway (upper airway/inhalation injury). Headache and nausea are early, nonspecific "
        "symptoms of CO toxicity, since CO binds hemoglobin far more tightly than oxygen, "
        "reducing oxygen delivery to tissues. Confusion (oriented to person only) can come from "
        "hypoxemia caused by airway and lung injury, and from tissue hypoxia caused by CO -- "
        "both apply. A normal-appearing SpO2 of 98% despite new confusion is falsely reassuring: "
        "standard pulse oximeters cannot tell carboxyhemoglobin from oxyhemoglobin, so the COHb "
        "level on the ABG (ordered, pending) is needed to detect CO poisoning. Burns over 20% "
        "TBSA trigger a systemic inflammatory response with fluid shifts that can lead to "
        "hypovolemic shock; tachycardia (HR 122) with a narrowing blood pressure (104/66) is "
        "compensation for that fluid loss. A hematocrit of 53% reflects hemoconcentration: "
        "plasma leaks out of the vessels while red cells stay in, raising the hematocrit as "
        "intravascular volume falls."
    ),
}, c1_tabs_p1_full, C1_INTRO)

c1_screen3 = screen(3, {
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "type": "dropdown_cloze",
    "preamble": "Phase 1 &mdash; Emergency Department, 0305.",
    "options": [opt("", False) for _ in range(4)],
    "cloze": {
        "text": "The client is at highest risk for [[drop0]] as evidenced by [[drop1]]. Once this is addressed, the nurse should next focus on the client's risk for [[drop2]] as evidenced by [[drop3]].",
        "scoreGroups": [[0, 1], [2, 3]],
        "dropdowns": [
            dropdown(
                ("airway obstruction from upper airway edema", True),
                ("wound infection", False), ("hypothermia", False),
                ("compartment syndrome of the right arm", False),
            ),
            dropdown(
                ("the hoarse voice and black-tinged sputum", True),
                ("the circumferential full-thickness burn of the right arm", False),
                ("the temperature of 36.3 °C", False),
                ("the WBC of 11.2 × 10⁹/L", False),
            ),
            dropdown(
                ("hypovolemic shock", True), ("impaired skin integrity", False),
                ("acute pain", False), ("disturbed body image", False),
            ),
            dropdown(
                ("HR 122/min, BP 104/66 mm Hg, and hematocrit 0.53 L/L", True),
                ("the blistered anterior trunk", False), ("the pain rating of 9/10", False),
                ("the potassium of 5.3 mmol/L", False),
            ),
        ],
    },
    "explanation": (
        "The nurse prioritizes with ABCDE, and for burns, ABC is followed by fluid "
        "resuscitation. After smoke inhalation, impaired gas exchange takes priority over "
        "impaired skin integrity. Upper-airway edema can worsen over hours, so early "
        "recognition (the hoarse voice and carbonaceous sputum) allows a controlled intubation "
        "before the airway is lost entirely. Circulation follows airway and breathing: with "
        "about 27% TBSA of partial- and full-thickness burns, large fluid shifts are expected, "
        "and IV access and fluid resuscitation are top priorities after the airway, evidenced "
        "by the tachycardia, low-normal blood pressure, and hemoconcentration (elevated "
        "hematocrit). Wound infection develops over days, not within this timeframe. "
        "Hypothermia is a real risk but is addressed after airway, breathing, and circulation. "
        "Compartment syndrome of the arm threatens a limb and needs frequent checks, but a "
        "threat to the airway threatens life."
    ),
}, c1_tabs_p1_full, C1_INTRO)

c1_notes_p2 = (
    "Client's voice is more hoarse and a high-pitched inspiratory sound is now audible at "
    "rest. Oxygen changed to a non-rebreather mask. The provider, respiratory therapist, and "
    "anesthesia are preparing for endotracheal intubation. Right hand: fingers cool and pale, "
    "capillary refill 5 seconds, right radial pulse faint (1+); client reports numbness and "
    "tingling in the right fingers; right forearm feels tense on palpation. Two large-bore IV "
    "catheters inserted in unburned skin of the left arm."
)
c1_labs_p2 = table(["0335", "Reference range"], [
    ("pH", ["7.30", "7.35&ndash;7.45"]),
    ("PaCO<sub>2</sub>", ["38 mm Hg", "35&ndash;45 mm Hg"]),
    ("PaO<sub>2</sub>", ["92 mm Hg (on non-rebreather)", "80&ndash;100 mm Hg"]),
    ("HCO<sub>3</sub><sup>-</sup>", ["18 mmol/L", "22&ndash;26 mmol/L"]),
    ("Carboxyhemoglobin (COHb)", ["19%", "Less than 3% (non-smoker)"]),
], first_col="Test")
c1_orders_p2 = (
    "<ul>"
    "<li>Oxygen 100% via non-rebreather mask until airway secured</li>"
    "<li>Ringer's lactate (lactated Ringer's) per Parkland formula: 4 mL &times; kg &times; %TBSA (partial- and full-thickness burns only); titrate to urine output</li>"
    "<li>Insert indwelling urinary catheter; hourly urine output</li>"
    "<li>NPO; nasogastric tube to low intermittent suction</li>"
    "<li>Morphine 2&ndash;4 mg IV every 1 hour PRN pain</li>"
    "<li>Tetanus toxoid IM</li>"
    "<li>Chest x-ray; 12-lead ECG</li>"
    "<li>Arrange transfer to regional burn centre</li>"
    "</ul>"
)

c1_tabs_p2 = [
    {"id": "c1_hp", "title": "History and Physical", "content": c1_hp},
    {"id": "c1_vs", "title": "Vital Signs", "content": c1_vs_p1},
    {"id": "c1_labs", "title": "Laboratory Results", "content": c1_labs_p1 + c1_labs_p2},
    {"id": "c1_notes", "title": "Nurses' Notes", "content": note_p("0305", c1_notes_p1) + note_p("0340", c1_notes_p2)},
    {"id": "c1_orders", "title": "Provider Orders", "content": "<p><b>0340:</b></p>" + c1_orders_p2},
]

c1_screen4 = screen(4, {
    "stem": "The nurse plans the client's fluid resuscitation. Use the Nurses’ Notes (Phase 1), the Rule of Nines, and the provider's orders. Complete the following sentences by choosing from the lists of options.",
    "type": "dropdown_cloze",
    "preamble": "Phase 2 &mdash; Emergency Department, 0340.",
    "options": [opt("", False) for _ in range(5)],
    "cloze": {
        "text": "The percentage of TBSA to include in the fluid resuscitation calculation is [[drop0]]. The total volume of Ringer's lactate prescribed for the first 24 hours is [[drop1]]. Half of this volume, [[drop2]], is to be infused over the first 8 hours, timed from [[drop3]]. The nurse will titrate the infusion as prescribed to maintain a urine output of at least [[drop4]].",
        "dropdowns": [
            dropdown(("18%", False), ("27%", True), ("31.5%", False), ("36%", False)),
            dropdown(("4,320 mL", False), ("8,640 mL", True), ("10,080 mL", False), ("11,520 mL", False)),
            dropdown(("2,160 mL", False), ("4,320 mL", True), ("5,040 mL", False), ("5,760 mL", False)),
            dropdown(
                ("0215 (time of injury)", True), ("0300 (arrival in the ED)", False),
                ("the time the IV was started", False), ("the time the order was written", False),
            ),
            dropdown(("20 mL/h", False), ("40 mL/h", True), ("100 mL/h", False), ("160 mL/h", False)),
        ],
    },
    "explanation": (
        "By the Rule of Nines: anterior trunk (chest + abdomen) = 18%; the entire right arm, "
        "anterior 4.5% + posterior 4.5% = 9%. Total 27%. The face is a first-degree "
        "(superficial) burn -- red, dry, no blisters -- and is <b>not</b> counted in "
        "resuscitation calculations. Using the Parkland formula, 4 mL &times; 80 kg &times; 27 "
        "= 8,640 mL over 24 hours. Half of that, 4,320 mL, is given in the first 8 hours; the "
        "remaining 4,320 mL is given over the next 16 hours. The 8-hour clock starts at the "
        "burn, not at arrival -- because 45+ minutes have already passed since 0215, the hourly "
        "rate must make up for lost time. The adult urine-output target is about 0.5 mL/kg/h: "
        "0.5 &times; 80 kg = 40 mL/h. Urine output is the key guide for titration; output well "
        "above 1 mL/kg/h (for example, 100&ndash;160 mL/h) suggests over-resuscitation and risks "
        "edema-related complications."
    ),
}, c1_tabs_p2, C1_INTRO)

c1_screen5 = screen(5, {
    "stem": "For each nursing action, click to specify whether it is <b>indicated</b>, <b>contraindicated</b>, or <b>nonessential</b> for the client at this time.",
    "type": "matrix_mc",
    "preamble": "Phase 2 &mdash; Emergency Department, 0340.",
    "options": [opt("", False) for _ in range(10)],
    "matrix": {
        "rows": [
            {"text": "Notify the provider immediately about the right-hand findings", "correctIndex": 0},
            {"text": "Remove the wedding ring and watch from the right hand and wrist", "correctIndex": 0},
            {"text": "Elevate the right arm on pillows above the level of the heart", "correctIndex": 0},
            {"text": "Apply a snug elastic compression wrap to the right arm to limit swelling", "correctIndex": 1},
            {"text": "Continue 100% oxygen via non-rebreather mask until the airway is secured", "correctIndex": 0},
            {"text": "Administer the prescribed morphine intramuscularly into the unburned thigh", "correctIndex": 1},
            {"text": "Apply ice packs to the blistered chest to relieve pain", "correctIndex": 1},
            {"text": "Offer small sips of an electrolyte drink to replace fluid losses", "correctIndex": 1},
            {"text": "Teach active range-of-motion exercises for the right hand", "correctIndex": 2},
            {"text": "Cover the burns with clean, dry dressings or sheets and keep the room warm", "correctIndex": 0},
        ],
        "columns": ["Indicated", "Contraindicated", "Nonessential"],
        "firstColumnHeader": "Finding / Action",
    },
    "explanation": (
        "Cool, pale fingers, delayed capillary refill, a weakening pulse, paresthesia, and a "
        "tense forearm under a circumferential full-thickness burn signal impending compartment "
        "syndrome; the provider must be notified immediately, and the expected treatment is an "
        "escharotomy (incision through the inelastic eschar). Jewelry and clothing near the "
        "burn should be removed, since once edema develops, a ring or watch acts as a "
        "tourniquet. Elevating the arm above heart level reduces edema formation. Anything "
        "constricting (a compression wrap) worsens the compartment pressure that is already "
        "compromising perfusion. A carboxyhemoglobin of 19% confirms CO poisoning; high-flow "
        "oxygen shortens the half-life of carboxyhemoglobin and continues until the airway is "
        "secured and the COHb falls. During burn shock, peripheral and muscle perfusion is "
        "poor, so IM absorption is unreliable -- little early relief, then possible delayed, "
        "excessive absorption once perfusion returns; the client's orders specify IV morphine. "
        "Ice causes vasoconstriction that can deepen the injury and, over a 27% TBSA burn, "
        "promotes hypothermia; cooling with room-temperature water or saline is used instead. "
        "The client is NPO with an NG tube ordered: intubation is imminent and large burns "
        "commonly cause paralytic ileus, so resuscitation and any fluids are IV, not oral. "
        "Range-of-motion teaching is important later, in rehabilitation, but is not the "
        "priority during an airway emergency with a compromised arm. Clean, dry coverage "
        "protects the wounds from contamination and limits heat loss, and a warm room helps "
        "prevent hypothermia."
    ),
}, c1_tabs_p2, C1_INTRO)

c1_notes_p3 = (
    "Right-arm escharotomy was performed on arrival at the burn centre. Client was extubated "
    "on day 3. Morphine IV given 30 minutes before each dressing change. Silver sulfadiazine "
    "and nonadherent dressings applied to the anterior trunk twice daily. Today's assessment "
    "findings are shown below."
)
c1_findings_p3 = (
    "Urine output averaging 55 mL/h over the past 24 hours. Right hand warm, capillary refill "
    "2 seconds, right radial pulse 2+. SpO2 96% on O2 2 L/min nasal cannula; lungs clear; "
    "speaks in full sentences. Pain rated 3/10 during a dressing change after IV morphine 30 "
    "minutes beforehand. Green-yellow, foul-smelling drainage from the chest wound; redness "
    "extending 2 cm beyond the wound edge. Temperature 38.9 °C; WBC 17.4 × 10⁹/L."
)

c1_tabs_p3 = c1_tabs_p2 + [
    {"id": "c1_notes3", "title": "Progress Notes", "content": note_p("Post-injury Day 5", c1_notes_p3) + f'<p>{c1_findings_p3}</p>'},
]

c1_screen6 = screen(6, {
    "stem": "For each finding on post-injury day 5, click to specify whether it indicates that the plan of care has been <b>effective</b> or <b>not effective</b>.",
    "type": "matrix_mc",
    "preamble": "Phase 3 &mdash; Regional Burn Centre, Post-injury Day 5.",
    "options": [opt("", False) for _ in range(6)],
    "matrix": {
        "rows": [
            {"text": "Urine output averaging 55 mL/h over the past 24 hours", "correctIndex": 0},
            {"text": "Right hand warm, capillary refill 2 seconds, right radial pulse 2+", "correctIndex": 0},
            {"text": "SpO2 96% on O2 2 L/min nasal cannula; lungs clear; speaks in full sentences", "correctIndex": 0},
            {"text": "Pain rated 3/10 during a dressing change after IV morphine 30 minutes beforehand", "correctIndex": 0},
            {"text": "Green-yellow, foul-smelling drainage from the chest wound; redness extending 2 cm beyond the wound edge", "correctIndex": 1},
            {"text": "Temperature 38.9 °C; WBC 17.4 × 10⁹/L", "correctIndex": 1},
        ],
        "columns": ["Effective", "Not effective"],
        "firstColumnHeader": "Finding / Action",
    },
    "explanation": (
        "Urine output of 55 mL/h is above the 40 mL/h (0.5 mL/kg/h) target, showing adequate "
        "renal perfusion after resuscitation. A warm hand with brisk capillary refill and a "
        "palpable pulse matches the expected short-term outcome of no signs of compartment "
        "syndrome: no swelling and no decreased pulses in the affected area. SpO2 96%, clear "
        "lungs, and speaking in full sentences show that gas exchange and airway patency have "
        "been restored after extubation. Pain 3/10 during a dressing change reflects giving "
        "analgesia at least 30 minutes before burn care, with pain that is tolerable before, "
        "during, and after the dressing change. Yellow, foul-smelling discharge with increased "
        "erythema are signs of burn-wound infection; the nurse notifies the provider (a wound "
        "culture and antimicrobials are likely). The short-term goal is a WBC within normal "
        "range; fever with leukocytosis and a purulent wound suggest infection and possible "
        "sepsis, so the provider is notified and this is escalated promptly."
    ),
}, c1_tabs_p3, C1_INTRO)

case1 = base_item(
    "case_1782390000006", "NURS 1017 Unit 5 Case Study 6",
    [c1_screen1, c1_screen2, c1_screen3, c1_screen4, c1_screen5, c1_screen6],
    "A 46-year-old male client with flame burns and suspected inhalation injury, from the "
    "emergency department through fluid resuscitation and early burn-centre recovery.",
)

# =============================================================================
# CASE 2 -- Herpes Zoster Involving the Eye in an Immunosuppressed Older Adult (L.T., 72F)
# =============================================================================
C2_INTRO = "The nurse is caring for a 72-year-old female client with herpes zoster involving the left forehead, scalp, and eye."

c2_hp = note_p("History and Physical", (
    "72-year-old female. Rheumatoid arthritis treated with methotrexate 15 mg PO once weekly "
    "and prednisone 7.5 mg PO daily. Type 2 diabetes (metformin). Had chickenpox as a child; "
    "has not received a shingles vaccine. Lives with her daughter, son-in-law, and 4-month-old "
    "grandson; she provides daytime childcare for the infant. Weight 60 kg."
))
c2_notes_p1 = (
    "Reports 3 days of burning, tingling pain over the left forehead and scalp, fatigue, and "
    "feeling “like I was getting the flu.” Yesterday noticed clusters of blisters. Grouped "
    "vesicles on an erythematous base over the left forehead, left scalp, and left upper "
    "eyelid; one vesicle on the tip of the nose. Lesions stop at the midline. Left eye red and "
    "tearing; client states the eye “feels gritty,” light hurts her eyes, and vision in the "
    "left eye is blurry. Rates pain 8/10, burning, worse with light touch."
)
c2_vs_p1 = table(["1030"], [
    ("T", ["37.9 &deg;C"]), ("HR", ["92/min"]), ("RR", ["18/min"]), ("BP", ["146/84 mm Hg"]),
    ("SpO<sub>2</sub>", ["97% room air"]),
    ("Capillary glucose", ["11.8 mmol/L (213 mg/dL)"]),
])

c2_tabs_p1 = [
    {"id": "c2_hp", "title": "History and Physical", "content": c2_hp},
    {"id": "c2_vs", "title": "Vital Signs", "content": c2_vs_p1},
]

c2_screen1 = screen(1, {
    "stem": "Which findings require <b>immediate</b> follow-up by the nurse? <b>Select all that apply.</b>",
    "type": "select_all",
    "preamble": "Phase 1 &mdash; Primary Care Clinic, 1030.",
    "options": opts(
        ("Vesicle on the tip of the nose", True),
        ("Left-eye redness, sensitivity to light, and blurred vision", True),
        ("Lesions stop at the midline", False),
        ("Takes methotrexate weekly and prednisone daily", True),
        ("Provides daytime care for her 4-month-old grandson", True),
        ("Pain rated 8/10, burning, worse with light touch", True),
        ("Had chickenpox as a child", False),
        ("Temperature 37.9 °C", False),
        ("Grouped vesicles on an erythematous base", False),
        ("Blood pressure 146/84 mm Hg", False),
    ),
    "explanation": (
        "A lesion on the tip or side of the nose (Hutchinson sign) shows involvement of the "
        "nasociliary branch of the ophthalmic (V1) division of the trigeminal nerve, which also "
        "supplies the eye; the provider should be informed immediately of any facial lesion, "
        "especially near the eye or ear. Eye redness, photophobia, and blurred vision are signs "
        "of ocular involvement (conjunctivitis, keratitis, uveitis) that can threaten sight and "
        "need urgent ophthalmology assessment. Methotrexate and prednisone raise the risk of "
        "severe, prolonged, or disseminated zoster, changing the treatment setting (IV "
        "antiviral), the isolation needed, and the monitoring. A young infant is too young for "
        "varicella vaccination and could develop chickenpox from contact with lesion fluid; "
        "this needs immediate teaching and exposure planning. Pain 8/10 with allodynia (pain "
        "worse with light touch) needs prompt management and is linked to a higher risk of "
        "postherpetic neuralgia. Lesions staying on one side and stopping at the midline, "
        "grouped vesicles on a red base, childhood chickenpox, and a mildly elevated "
        "temperature and blood pressure are all expected features of herpes zoster or an "
        "expected response to pain and stress; they do not require immediate follow-up on their "
        "own."
    ),
}, c2_tabs_p1, C2_INTRO)
c2_screen1["leftContent"]["tabs"] = c2_tabs_p1 + [{"id": "c2_notes", "title": "Nurses' Notes", "content": ""}]

c2_tabs_p1_full = c2_tabs_p1 + [{"id": "c2_notes", "title": "Nurses' Notes", "content": note_p("1030", c2_notes_p1)}]

c2_screen2 = screen(2, {
    "stem": "For each finding, click to specify whether it is an <b>expected manifestation of herpes zoster</b>, <b>suggests ocular (eye) involvement</b>, or <b>increases the risk of severe or complicated disease</b>.",
    "type": "matrix_mc",
    "preamble": "Phase 1 &mdash; Primary Care Clinic, 1030.",
    "options": [opt("", False) for _ in range(7)],
    "matrix": {
        "rows": [
            {"text": "Burning, tingling pain for 3 days before the rash appeared", "correctIndex": 0},
            {"text": "Lesions limited to one side, stopping at the midline", "correctIndex": 0},
            {"text": "Low-grade fever and fatigue", "correctIndex": 0},
            {"text": "Vesicle on the tip of the nose", "correctIndex": 1},
            {"text": "Photophobia and blurred vision in the left eye", "correctIndex": 1},
            {"text": "Daily prednisone and weekly methotrexate", "correctIndex": 2},
            {"text": "Age 72", "correctIndex": 2},
        ],
        "columns": ["Expected manifestation", "Suggests ocular involvement", "Increases risk of severe disease"],
        "firstColumnHeader": "Finding / Action",
    },
    "explanation": (
        "The chapter describes a viral prodrome with a burning sensation where the rash will "
        "appear several days later. Zoster follows a single dermatome and does not cross the "
        "midline. Low-grade fever and fatigue are part of the prodrome. A vesicle on the tip of "
        "the nose (Hutchinson sign) is a strong predictor of eye involvement, since the "
        "nasociliary nerve supplies both the tip of the nose and the eye. Photophobia and "
        "blurred vision suggest corneal or intraocular inflammation. Prednisone and methotrexate "
        "suppress cell-mediated immunity, which normally controls varicella-zoster virus, "
        "raising the risk of dissemination and prolonged shedding. Zoster most commonly affects "
        "older adults, and age also raises the risk of complications, including postherpetic "
        "neuralgia."
    ),
}, c2_tabs_p1_full, C2_INTRO)

c2_screen3 = screen(3, {
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "type": "dropdown_cloze",
    "preamble": "Phase 1 &mdash; Primary Care Clinic, 1030.",
    "options": [opt("", False) for _ in range(4)],
    "cloze": {
        "text": "The nurse's priority is to prevent [[drop0]] because [[drop1]]. The nurse's immediate action should be to [[drop2]]. The nurse also recognizes the client's [[drop3]] as a concurrent priority.",
        "dropdowns": [
            dropdown(
                ("permanent vision loss", True), ("secondary bacterial skin infection", False),
                ("scarring of the forehead", False), ("hyperglycemia", False),
            ),
            dropdown(
                ("the virus is affecting the ophthalmic division of the trigeminal nerve", True),
                ("the client is older than 65 years", False), ("the lesions are vesicular", False),
                ("the client had chickenpox as a child", False),
            ),
            dropdown(
                ("notify the provider immediately so that urgent ophthalmology assessment can be arranged", True),
                ("apply antibiotic ointment to the left eyelid", False),
                ("schedule a follow-up visit in 1 week", False),
                ("teach the client to apply warm compresses to the eye", False),
            ),
            dropdown(("acute pain", True), ("fluid volume excess", False), ("impaired gas exchange", False), ("hypothermia", False)),
        ],
    },
    "explanation": (
        "Herpes zoster ophthalmicus can cause keratitis, uveitis, glaucoma, and vision loss. A "
        "threat of permanent loss of function takes priority over skin integrity. The forehead, "
        "scalp, upper eyelid, and nose-tip lesions map to the V1 (ophthalmic) dermatome, "
        "explaining why the eye is at risk. This is stated directly in the chapter for facial "
        "lesions near the eye or ear. Applying ointment to the eye or warm compresses without a "
        "prescription is outside the nurse's scope, and waiting a week risks permanent damage. "
        "Pain rated 8/10 with allodynia must be addressed promptly; adequate pain control is a "
        "recognized priority in zoster care."
    ),
}, c2_tabs_p1_full, C2_INTRO)

c2_notes_p2 = (
    "Admitted for IV antiviral therapy. Ophthalmology confirmed left-eye involvement and "
    "prescribed topical eye medications. Lesions remain confined to the left forehead, scalp, "
    "upper eyelid, and nose tip; assessment for dissemination is in progress. Pain 8/10. "
    "Daughter asks whether she can bring the baby to visit this evening. Admission creatinine "
    "78 µmol/L (0.88 mg/dL)."
)
c2_orders_p2 = (
    "<ul>"
    "<li>Airborne and contact precautions (airborne infection isolation room) until disseminated disease is ruled out</li>"
    "<li>Acyclovir 600 mg (10 mg/kg) IV every 8 hours, infuse over 1 hour</li>"
    "<li>0.9% sodium chloride IV at 75 mL/h</li>"
    "<li>Strict intake and output; serum creatinine daily</li>"
    "<li>Acetaminophen 650 mg PO every 6 hours</li>"
    "<li>Oxycodone 5 mg PO every 4 hours PRN severe pain</li>"
    "<li>Mupirocin 2% ointment to crusted skin lesions twice daily (not for eye)</li>"
    "<li>Ophthalmic medications per ophthalmology</li>"
    "<li>Continue prednisone 7.5 mg PO daily; methotrexate on hold per rheumatology</li>"
    "<li>Slit-lamp examination in eye clinic tomorrow 0900</li>"
    "</ul>"
)
c2_tabs_p2 = c2_tabs_p1_full + [
    {"id": "c2_notes2", "title": "Nurses' Notes 1400", "content": note_p("1400", c2_notes_p2)},
    {"id": "c2_orders", "title": "Provider Orders", "content": c2_orders_p2},
]

c2_screen4 = screen(4, {
    "stem": "The nurse plans care for the client on the medical unit. Which <b>five</b> interventions should the nurse include in the plan of care? <b>Select five.</b>",
    "type": "select_n",
    "limit": 5,
    "preamble": "Phase 2 &mdash; Medical Unit, Same Day 1400.",
    "options": opts(
        ("Place the client in an airborne infection isolation room and use airborne and contact precautions", True),
        ("Assign staff members with documented immunity to varicella", True),
        ("Infuse each acyclovir dose over at least 1 hour, maintain hydration, and keep strict intake and output", True),
        ("Assess left-eye symptoms and visual acuity each shift and report changes", True),
        ("Monitor the serum creatinine daily", True),
        ("Tell the daughter she may bring the baby to visit if she wears a gown and gloves", False),
        ("Gently open intact vesicles to help the lesions dry faster", False),
        ("Apply the prescribed mupirocin ointment to the left eye and eyelid margin", False),
        ("Hold the client's daily prednisone to improve her immune response", False),
        ("Give the recombinant shingles vaccine now to shorten this episode", False),
    ),
    "explanation": (
        "For localized zoster in an immunocompromised client, isolation guidance calls for "
        "airborne and contact precautions until disseminated infection is ruled out. "
        "Varicella-zoster virus spreads to people who are not immune, so non-immune or pregnant "
        "staff should not provide care. IV acyclovir can precipitate as crystals in the renal "
        "tubules and cause acute kidney injury, especially with rapid infusion or dehydration, "
        "so each dose is infused slowly with adequate hydration and strict intake and output. "
        "Eye assessment follows directly from the priority of preventing vision loss; worsening "
        "vision needs prompt reporting to ophthalmology. Daily creatinine detects "
        "acyclovir-related kidney injury early. A 4-month-old is unvaccinated against varicella, "
        "and airborne precautions are in place; a gown and gloves do not protect the infant from "
        "an airborne exposure, so the visit should not be encouraged this way. Opening intact "
        "vesicles increases the risk of secondary bacterial infection and scarring; ointments "
        "are prescribed to prevent secondary infection, not to dry lesions faster. The order "
        "specifies skin lesions only -- only ophthalmic preparations may be placed in the eye. "
        "Stopping long-term corticosteroids abruptly risks adrenal insufficiency; the provider "
        "continued it, and any change needs a prescriber's order. The vaccine prevents future "
        "episodes; it does not treat active zoster, and vaccination is discussed after recovery."
    ),
}, c2_tabs_p2, C2_INTRO)

c2_screen5 = screen(5, {
    "stem": "Complete the sentences by dragging a word choice from the word bank into each blank. Not all word choices will be used, and each is used only once.",
    "type": "drag_drop_cloze",
    "preamble": "Phase 2 &mdash; Medical Unit, Same Day 1400.",
    "options": [opt("", False) for _ in range(5)],
    "cloze": {
        "text": "Before entering the client's room, the nurse performs hand hygiene and dons a gown, gloves, and a [[drop0]]. The door to the client's room must remain [[drop1]]. Before the client is transported to the eye clinic for her slit-lamp examination, the nurse places [[drop2]] and prepares her by [[drop3]]. After administering the prescribed oxycodone for pain rated 8/10, the nurse plans to [[drop4]].",
        "dropdowns": [
            dropdown(
                ("fit-tested N95 respirator", True), ("surgical mask", False), ("closed", False),
                ("open for close observation", False), ("a surgical mask on the client", False),
                ("an N95 respirator on the client", False),
                ("covering the skin lesions with a clean dressing", False),
                ("applying mupirocin ointment to the left eye", False),
                ("reassess pain within 60 minutes", False),
                ("wait until the next scheduled dose to reassess pain", False),
            ),
            dropdown(
                ("fit-tested N95 respirator", False), ("surgical mask", False), ("closed", True),
                ("open for close observation", False), ("a surgical mask on the client", False),
                ("an N95 respirator on the client", False),
                ("covering the skin lesions with a clean dressing", False),
                ("applying mupirocin ointment to the left eye", False),
                ("reassess pain within 60 minutes", False),
                ("wait until the next scheduled dose to reassess pain", False),
            ),
            dropdown(
                ("fit-tested N95 respirator", False), ("surgical mask", False), ("closed", False),
                ("open for close observation", False), ("a surgical mask on the client", True),
                ("an N95 respirator on the client", False),
                ("covering the skin lesions with a clean dressing", False),
                ("applying mupirocin ointment to the left eye", False),
                ("reassess pain within 60 minutes", False),
                ("wait until the next scheduled dose to reassess pain", False),
            ),
            dropdown(
                ("fit-tested N95 respirator", False), ("surgical mask", False), ("closed", False),
                ("open for close observation", False), ("a surgical mask on the client", False),
                ("an N95 respirator on the client", False),
                ("covering the skin lesions with a clean dressing", True),
                ("applying mupirocin ointment to the left eye", False),
                ("reassess pain within 60 minutes", False),
                ("wait until the next scheduled dose to reassess pain", False),
            ),
            dropdown(
                ("fit-tested N95 respirator", False), ("surgical mask", False), ("closed", False),
                ("open for close observation", False), ("a surgical mask on the client", False),
                ("an N95 respirator on the client", False),
                ("covering the skin lesions with a clean dressing", False),
                ("applying mupirocin ointment to the left eye", False),
                ("reassess pain within 60 minutes", True),
                ("wait until the next scheduled dose to reassess pain", False),
            ),
        ],
    },
    "explanation": (
        "Airborne precautions require a fit-tested N95 (or higher) respirator; a surgical mask "
        "does not filter airborne particles adequately. An airborne infection isolation room "
        "keeps negative pressure only with the door closed. During essential transport, the "
        "client wears a surgical mask to contain respiratory secretions; a client is not placed "
        "in an N95 (it is designed to protect the wearer, and may have an exhalation valve). "
        "Covering the skin lesions limits contact and airborne spread from vesicle fluid. "
        "Reassessing pain within the drug's peak time (about 30&ndash;60 minutes for oral "
        "opioids, per agency policy) evaluates effectiveness and sedation."
    ),
}, c2_tabs_p2, C2_INTRO)

c2_notes_p3 = "Dissemination was ruled out on day 2. The nurse reviews today's flowsheet and discharge teaching in preparation for possible discharge tomorrow."

c2_flowsheet_rows = [
    ("Temperature", "37.0 °C", False),
    ("Skin", "All lesions crusted; no new lesions outside the left forehead, scalp, and nose", False),
    ("Pain", "3/10 with scheduled acetaminophen", False),
    ("Left eye", "Less redness; visual acuity unchanged from ophthalmology baseline", False),
    ("Serum creatinine", "163 µmol/L (1.84 mg/dL); admission 78 µmol/L (0.88 mg/dL)", True),
    ("Intake / output (24 h)", "Intake 1,600 mL / urine output 380 mL", True),
    ("Capillary glucose (before lunch)", "7.4 mmol/L (133 mg/dL)", False),
    ("Client statement", "“Once the scabs are gone, any burning that's left doesn't mean anything, so I won't bother anyone about it.”", True),
    ("Client statement", "“After I recover, I should ask my doctor about the two-dose shingles vaccine.”", False),
    ("Client statement", "“I'll keep washing my hands and I won't rub my eye.”", False),
]
c2_flowsheet_html = ['<table class="nclex-editor-table" style="width:100%; border-collapse:collapse; margin:12px 0;"><thead><tr>',
    '<th style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;">Finding</th>',
    '<th style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;">Result</th>',
    '</tr></thead><tbody>']
for finding, result, correct in c2_flowsheet_rows:
    wrapped = "{" + result + ("|correct}" if correct else "}")
    c2_flowsheet_html.append(
        f'<tr><td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;"><b>{finding}</b></td>'
        f'<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">{wrapped}</td></tr>'
    )
c2_flowsheet_html.append('</tbody></table>')
c2_flowsheet_html = "".join(c2_flowsheet_html)

c2_tabs_p3 = c2_tabs_p2 + [{"id": "c2_notes3", "title": "Nurses' Notes Day 4", "content": note_p("Hospital Day 4", c2_notes_p3)}]

c2_screen6 = screen(6, {
    "stem": "The nurse reviews the hospital day 4 flowsheet. <b>Highlight</b> the findings that indicate the client's condition or understanding has <b>not</b> progressed as expected and requires follow-up.",
    "type": "highlight",
    "preamble": "Phase 3 &mdash; Medical Unit, Hospital Day 4.",
    "options": [opt("", False) for _ in range(3)],
    "highlightTabs": [{"id": "c2_ht6", "title": "Hospital Day 4 Flowsheet", "content": c2_flowsheet_html}],
    "maxCorrectSelections": None,
    "explanation": (
        "A creatinine more than doubled from the 78 µmol/L admission baseline suggests "
        "acyclovir-associated acute kidney injury; the nurse notifies the provider promptly, "
        "since the dose may need adjustment and hydration reviewed. Oliguria (a urine output "
        "under about 400 mL/24 h, or under 0.5 mL/kg/h) despite adequate intake also supports "
        "kidney injury. The client's statement that ongoing burning after the scabs are gone "
        "“doesn't mean anything” shows a misunderstanding: pain that persists after the rash "
        "heals may be postherpetic neuralgia, a treatable, reportable neurological "
        "complication, and this teaching needs reinforcement. Temperature, skin, pain, and eye "
        "findings all show expected progress: afebrile, lesions crusted without dissemination, "
        "pain controlled, and eye findings stable. A capillary glucose of 7.4 mmol/L is "
        "acceptable for a client with diabetes taking prednisone. The vaccine and hand-hygiene "
        "statements reflect accurate understanding -- the recombinant (non-live) zoster vaccine "
        "is recommended after recovery, including for people who are immunocompromised."
    ),
}, c2_tabs_p3, C2_INTRO)
c2_screen6["leftContent"]["tabs"] = c2_tabs_p3

case2 = base_item(
    "case_1782390000007", "NURS 1017 Unit 5 Case Study 7",
    [c2_screen1, c2_screen2, c2_screen3, c2_screen4, c2_screen5, c2_screen6],
    "A 72-year-old immunosuppressed female client with herpes zoster involving the left "
    "forehead, scalp, and eye, from the primary care clinic through hospitalization and "
    "discharge planning.",
)

# =============================================================================
# CASE 3 -- Plaque Psoriasis Progressing to Generalized Exfoliative Dermatitis (Erythroderma)
# (J.M., 54-year-old male)
# =============================================================================
C3_INTRO = "The nurse is caring for a 54-year-old male client with plaque psoriasis progressing to generalized exfoliative dermatitis (erythroderma)."

c3_hp = note_p("History and Physical", (
    "54-year-old male with plaque psoriasis for 20 years, managed by a dermatologist with "
    "methotrexate once weekly. Stopped methotrexate 6 weeks ago after being laid off and "
    "losing his drug coverage. Since then drinks “6 to 8 beers a day.” Two weeks ago a "
    "walk-in clinic prescribed a short course of oral prednisone for a flare; he finished it 5 "
    "days ago. Father has psoriasis. Weight 92 kg."
))
c3_notes_p1 = (
    "Over the past 3 days redness spread over “my whole body”; skin peeling in sheets; "
    "intense itching and burning; shaking chills; “I can't get warm.” Dizzy when standing. "
    "Diffuse bright erythema with fine scaling and peeling over approximately 90% of the body, "
    "including palms and soles. Oral mucosa dry. Bilateral 2+ pitting ankle edema. Several "
    "fingernails pitted and ridged. Excoriations on both forearms. Client is tearful: “I've "
    "stopped leaving the house. People stare.”"
)

c3_flowsheet_rows = [
    ("Temperature", "35.6 °C", True),
    ("Heart rate", "116/min", True),
    ("Blood pressure", "96/58 mm Hg lying; 80/50 mm Hg standing, with dizziness", True),
    ("Respiratory rate / SpO2", "18/min / 97% room air", False),
    ("Urine output", "100 mL of dark amber urine in the past 8 hours", True),
    ("Skin", "Bright erythema with scaling and peeling over approximately 90% of the body, including palms and soles", True),
    ("Nails", "Pitting and ridging of several fingernails", False),
    ("Potassium", "3.1 mmol/L (3.5&ndash;5.0)", True),
    ("Magnesium", "0.62 mmol/L (0.70&ndash;1.00)", True),
    ("Creatinine", "132 µmol/L (1.49 mg/dL); 84 µmol/L three months ago", True),
    ("Albumin", "26 g/L (2.6 g/dL) (35&ndash;50 g/L)", True),
    ("ESR", "48 mm/h (0&ndash;20)", False),
    ("Hemoglobin", "124 g/L (135&ndash;175)", False),
    ("ALT", "34 U/L (7&ndash;56)", False),
]

def build_highlight_table(rows, col1="Finding", col2="Result"):
    html = ['<table class="nclex-editor-table" style="width:100%; border-collapse:collapse; margin:12px 0;"><thead><tr>',
        f'<th style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;">{col1}</th>',
        f'<th style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;">{col2}</th>',
        '</tr></thead><tbody>']
    for label, result, correct in rows:
        wrapped = "{" + result + ("|correct}" if correct else "}")
        html.append(
            f'<tr><td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;"><b>{label}</b></td>'
            f'<td style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;">{wrapped}</td></tr>'
        )
    html.append('</tbody></table>')
    return "".join(html)

c3_flowsheet_html = build_highlight_table(c3_flowsheet_rows)

c3_tabs_p1 = [
    {"id": "c3_hp", "title": "History and Physical", "content": c3_hp},
    {"id": "c3_notes", "title": "Nurses' Notes", "content": note_p("2140", c3_notes_p1)},
]

c3_screen1 = screen(1, {
    "stem": "The nurse reviews the ED flowsheet. <b>Highlight</b> the findings that require <b>immediate</b> follow-up.",
    "type": "highlight",
    "preamble": "Phase 1 &mdash; Emergency Department, 2140.",
    "options": [opt("", False) for _ in range(9)],
    "highlightTabs": [{"id": "c3_ht1", "title": "ED Flowsheet", "content": c3_flowsheet_html}],
    "maxCorrectSelections": None,
    "explanation": (
        "Impaired thermoregulation (temperature 35.6 °C) results when the skin barrier is "
        "almost completely lost; the nurse monitors temperature and provides warming measures "
        "in erythroderma. Tachycardia and hypotension with an orthostatic drop reflect "
        "hemodynamic instability from fluid loss through the damaged skin -- hemodynamic "
        "stability is the priority in erythroderma. Only 100 mL of dark, concentrated urine in "
        "8 hours (about 0.14 mL/kg/h in a 92-kg client) shows oliguria from hypovolemia. "
        "Erythema over about 90% of the body meets the chapter's definition of generalized "
        "exfoliative dermatitis (erythroderma), a life-threatening condition managed in "
        "hospital. Low potassium and magnesium are replaced; both raise dysrhythmia risk, and "
        "heavy alcohol use contributes to low magnesium. A creatinine risen from a baseline of "
        "84 to 132 µmol/L suggests prerenal acute kidney injury from hypovolemia. An albumin "
        "of 26 g/L reflects protein loss through the shedding, inflamed skin; this explains the "
        "ankle edema and lowers oncotic pressure. A normal respiratory rate and SpO2 argue "
        "against a respiratory cause for these findings. Nail pitting is a chronic finding of "
        "nail psoriasis, not urgent. An elevated ESR is expected with psoriatic inflammation "
        "and is monitored, but does not require immediate action on its own. Mild anemia and a "
        "normal ALT are not immediately dangerous; the ALT is a useful baseline before starting "
        "systemic therapy."
    ),
}, c3_tabs_p1, C3_INTRO)
c3_screen1["leftContent"]["tabs"] = [
    {"id": "c3_hp", "title": "History and Physical", "content": c3_hp},
    {"id": "c3_notes", "title": "Nurses' Notes", "content": ""},
]

c3_screen2 = screen(2, {
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "type": "dropdown_cloze",
    "preamble": "Phase 1 &mdash; Emergency Department, 2140.",
    "options": [opt("", False) for _ in range(5)],
    "cloze": {
        "text": "The client's hypotension and tachycardia are most likely caused by [[drop0]] as evidenced by [[drop1]]. His temperature of 35.6 °C is most likely due to [[drop2]]. The bilateral ankle edema is most likely related to [[drop3]]. The flare was most likely triggered by [[drop4]].",
        "scoreGroups": [[0, 1]],
        "dropdowns": [
            dropdown(
                ("fluid loss through the widely inflamed, shedding skin", True),
                ("cardiogenic shock", False), ("methotrexate toxicity", False),
                ("anaphylaxis to prednisone", False),
            ),
            dropdown(
                ("the orthostatic blood pressure drop, dry oral mucosa, and low, concentrated urine output", True),
                ("the nail pitting and ridging", False), ("the ESR of 48 mm/h", False),
                ("the SpO2 of 97%", False),
            ),
            dropdown(
                ("heat loss through widespread, dilated skin blood vessels", True),
                ("hypothyroidism", False), ("alcohol withdrawal", False),
                ("a normal evening drop in body temperature", False),
            ),
            dropdown(
                ("a low serum albumin from protein loss through the skin", True),
                ("fluid overload from IV fluids", False), ("right-sided heart failure", False),
                ("bilateral deep vein thrombosis", False),
            ),
            dropdown(
                ("stopping methotrexate, finishing a course of oral prednisone, heavy alcohol use, and stress", True),
                ("a new laundry detergent", False), ("a recent streptococcal throat infection", False),
                ("too much sun exposure", False),
            ),
        ],
    },
    "explanation": (
        "In erythroderma the skin barrier is almost completely absent, so the patient loses "
        "fluid rapidly through the skin. The orthostatic drop, dry mucosa, and low, "
        "concentrated urine output confirm volume depletion; a normal SpO2 and clear lungs "
        "argue against a cardiopulmonary cause, and there is no allergen exposure suggesting "
        "anaphylaxis. Inflamed, vasodilated skin over 90% of the body loses heat rapidly; the "
        "chapter directs frequent temperature monitoring with warming or cooling as needed. The "
        "client has not stopped drinking long enough for significant withdrawal, and alcohol "
        "withdrawal tends to raise, not lower, temperature. An albumin of 26 g/L shows protein "
        "loss through scaling and exudation; low oncotic pressure lets fluid shift into tissues "
        "even while the client is intravascularly depleted, and IV fluids have not yet been "
        "given. The chapter lists stress and excessive alcohol as psoriasis triggers and notes "
        "psoriasis is a contributing cause of erythroderma. Abruptly stopping systemic therapy "
        "and withdrawal of systemic corticosteroids are well-recognized triggers of erythrodermic "
        "flares. A streptococcal infection classically triggers guttate psoriasis; detergents "
        "trigger contact dermatitis, not this presentation."
    ),
}, c3_tabs_p1, C3_INTRO)

c3_screen3 = screen(3, {
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "type": "dropdown_cloze",
    "preamble": "Phase 1 &mdash; Emergency Department, 2140.",
    "options": [opt("", False) for _ in range(3)],
    "cloze": {
        "text": "The priority nursing hypothesis at this time is [[drop0]] because [[drop1]]. Once this is addressed, the nurse's next priority is [[drop2]].",
        "dropdowns": [
            dropdown(
                ("risk for hemodynamic instability related to fluid and electrolyte loss", True),
                ("impaired skin integrity", False), ("disturbed body image", False),
                ("deficient knowledge about medication adherence", False),
            ),
            dropdown(
                ("the skin barrier is almost completely absent, allowing ongoing loss of fluid, protein, electrolytes, and heat", True),
                ("psoriasis is an autoimmune disorder", False),
                ("the client stopped taking methotrexate", False),
                ("the ESR is elevated", False),
            ),
            dropdown(
                ("impaired skin integrity", True), ("disturbed body image", False),
                ("deficient knowledge", False), ("ineffective coping", False),
            ),
        ],
    },
    "explanation": (
        "For ordinary psoriasis, impaired skin integrity is the priority. Once the disease "
        "becomes erythroderma, the priority shifts to hemodynamic instability, because the skin "
        "barrier is almost completely absent -- this is the key clinical-judgment shift in this "
        "case. That widespread loss of the skin barrier is the mechanism that makes "
        "erythroderma life-threatening; the other options are true facts but do not explain the "
        "immediate danger. Impaired skin integrity is the next hypothesis in erythroderma. Body "
        "image, knowledge, and coping are real needs for this client (he is tearful and "
        "isolating) and are addressed once he is physiologically stable, in keeping with the "
        "priority of physiological needs."
    ),
}, c3_tabs_p1, C3_INTRO)

c3_screen4 = screen(4, {
    "stem": "Which interventions should the nurse include in the plan of care for the first 24 hours? <b>Select all that apply.</b>",
    "type": "select_all",
    "preamble": "Phase 1 &mdash; Emergency Department, 2140.",
    "options": opts(
        ("Administer IV isotonic fluids as prescribed", True),
        ("Replace potassium and magnesium as prescribed, with cardiac monitoring", True),
        ("Keep the room warm, apply warm blankets, and monitor temperature frequently", True),
        ("Maintain strict intake and output and obtain a daily weight", True),
        ("Provide lukewarm oatmeal soaks followed by a bland, oil-based emollient", True),
        ("Administer the prescribed oral antihistamine, preferably at bedtime", True),
        ("Monitor for alcohol withdrawal using a validated scale (e.g., CIWA-Ar)", True),
        ("Restrict oral fluids to 1 L/day to reduce the ankle edema", False),
        ("Apply coal tar ointment to all reddened skin", False),
        ("Arrange an ultraviolet phototherapy session for tomorrow", False),
        ("Use hot water and a washcloth to scrub off loose scale", False),
    ),
    "explanation": (
        "Adequate hydration through IV fluid replacement maintains hemodynamic stability. "
        "Potassium, magnesium, and calcium are replaced when indicated; low potassium and "
        "magnesium raise dysrhythmia risk, so cardiac monitoring is prudent. Temperature "
        "monitoring with warming measures as needed addresses impaired thermoregulation. Strict "
        "intake and output and daily weight track the response to fluid replacement and ongoing "
        "losses. Oatmeal baths are recommended for erythroderma, and oil-based emollients are "
        "recommended for psoriasis; lukewarm water avoids further vasodilation and heat loss. "
        "Oral antihistamines (for example, diphenhydramine) are listed for itching in "
        "erythroderma; bedtime dosing uses the sedating effect, with supervision for getting up "
        "because of orthostatic hypotension. He reports 6 to 8 drinks a day; withdrawal can "
        "begin within 6 to 24 hours of the last drink and worsens hemodynamic instability. The "
        "edema comes from low albumin while the client is intravascularly depleted; restricting "
        "fluids would worsen hypotension and kidney injury. Coal tar is a treatment for mild, "
        "localized psoriasis; on inflamed, broken skin over 90% of the body it is irritating "
        "and can worsen erythroderma. Ultraviolet phototherapy is used for more stable "
        "psoriasis; ultraviolet exposure to acutely inflamed skin can aggravate erythroderma, "
        "and he is unstable. Friction and heat from hot water scrubbing further damage the "
        "fragile barrier, increase heat and fluid loss, and invite infection."
    ),
}, c3_tabs_p1, C3_INTRO)

c3_notes_p2 = (
    "BP 118/72 mm Hg, HR 88/min, temperature 36.9 °C; no orthostatic change. Potassium 3.9 "
    "mmol/L. Alcohol withdrawal scores 2&ndash;4. Dermatology plans to start infliximab (a "
    "biologic) by IV infusion today. Client states: “I stopped the methotrexate because I lost "
    "my job and my drug plan. I hate the way people look at my skin. I really do want to cut "
    "down on drinking.”"
)
c3_screening = table(["Result"], [
    ("Interferon-gamma release assay (TB)", ["Negative"]),
    ("Hepatitis B surface antigen / core antibody", ["Negative / Negative"]),
    ("Hepatitis C antibody", ["Negative"]),
    ("Chest x-ray", ["No acute findings"]),
], first_col="Test")

c3_tabs_p2 = c3_tabs_p1 + [
    {"id": "c3_notes2", "title": "Nurses' Notes Day 3", "content": note_p("Hospital Day 3", c3_notes_p2)},
    {"id": "c3_screening", "title": "Screening Results", "content": c3_screening},
]

c3_screen5 = screen(5, {
    "stem": "For each nursing action, click to specify whether it is <b>indicated</b> or <b>contraindicated</b> for the client on hospital day 3.",
    "type": "matrix_mc",
    "preamble": "Phase 2 &mdash; Medical Unit, Hospital Day 3.",
    "options": [opt("", False) for _ in range(8)],
    "matrix": {
        "rows": [
            {"text": "Confirm that the TB and hepatitis screening results are documented before the first infliximab infusion", "correctIndex": 0},
            {"text": "Monitor vital signs and observe for an infusion reaction (fever, chills, dyspnea, hives) during and after the infusion", "correctIndex": 0},
            {"text": "Teach the client to report fever, cough, night sweats, or signs of skin infection promptly", "correctIndex": 0},
            {"text": "Advise the client to get any overdue live vaccines (e.g., MMR) now that infusions are starting", "correctIndex": 1},
            {"text": "Explain that the infusions can be stopped once his skin clears", "correctIndex": 1},
            {"text": "Refer the client to a social worker for drug-coverage options and to a psoriasis support group or counselling", "correctIndex": 0},
            {"text": "Teach stress-reduction strategies and support his plan to reduce alcohol intake", "correctIndex": 0},
            {"text": "Encourage long, hot showers to soften and remove scale", "correctIndex": 1},
        ],
        "columns": ["Indicated", "Contraindicated"],
        "firstColumnHeader": "Finding / Action",
    },
    "explanation": (
        "For systemic and biologic therapy (infliximab is named), the nurse monitors for "
        "serious infections such as tuberculosis and hepatitis. TNF inhibitors can reactivate "
        "latent TB and hepatitis B, so screening must be confirmed first. Infliximab can cause "
        "infusion reactions. Suppressed immunity makes infection more likely and directs "
        "teaching about worsening redness, swelling, or discharge. Live vaccines are avoided "
        "during biologic immunosuppression; needed vaccines should be given before therapy "
        "starts, per prescriber. Psoriasis is chronic with remission and relapse; the nurse "
        "reinforces adherence rather than suggesting therapy can simply be stopped once the "
        "skin clears -- stopping therapy is what precipitated this admission. Addressing the "
        "root cause of non-adherence (lost drug coverage) and the psychosocial impact matters: "
        "support groups and social work are appropriate for coping and financial concerns. "
        "Education to avoid triggers, including stress and excessive alcohol, and "
        "stress-reduction techniques are directed. Heat and prolonged water exposure dry and "
        "irritate the skin and promote heat and fluid loss; lukewarm soaks followed by "
        "emollients are appropriate instead."
    ),
}, c3_tabs_p2, C3_INTRO)

c3_notes_p3 = "First infliximab infusion completed on day 3 without reaction. The nurse reviews today's findings before discharge planning."

c3_tabs_p3 = c3_tabs_p2 + [{"id": "c3_notes3", "title": "Nurses' Notes Day 7", "content": note_p("Hospital Day 7", c3_notes_p3)}]

c3_screen6 = screen(6, {
    "stem": "For each finding on hospital day 7, click to specify whether it indicates that the plan of care has been <b>effective</b> or <b>not effective</b>.",
    "type": "matrix_mc",
    "preamble": "Phase 3 &mdash; Medical Unit, Hospital Day 7.",
    "options": [opt("", False) for _ in range(7)],
    "matrix": {
        "rows": [
            {"text": "BP 124/78 mm Hg and HR 82/min, with no orthostatic change", "correctIndex": 0},
            {"text": "Temperature 36.8 °C", "correctIndex": 0},
            {"text": "Potassium 4.1 mmol/L; magnesium 0.84 mmol/L", "correctIndex": 0},
            {"text": "Erythema reduced to about 40% of the body; less peeling; itch rated 3/10", "correctIndex": 0},
            {"text": "Excoriation on the right shin now has a honey-coloured crust with surrounding redness and warmth", "correctIndex": 1},
            {"text": "Alcohol withdrawal scores 0–2 for the past 72 hours", "correctIndex": 0},
            {"text": "Client states: “If my skin stays clear, I'll just skip the next infusion.”", "correctIndex": 1},
        ],
        "columns": ["Effective", "Not effective"],
        "firstColumnHeader": "Finding / Action",
    },
    "explanation": (
        "Stable blood pressure and heart rate meet the expected outcome of vital signs within "
        "normal limits without fluid imbalance. A normal temperature shows thermoregulation "
        "restored. Normal potassium and magnesium show no electrolyte disturbance. The chapter "
        "expects the skin to begin healing with decreased peeling and itching. A honey-coloured "
        "crust with surrounding redness and warmth is a classic sign of secondary bacterial "
        "infection (impetigo-like); the chapter notes yellow crusts over excoriations signal "
        "infection -- notify the provider; topical mupirocin is commonly prescribed, and "
        "infection risk is higher on a biologic. Low withdrawal scores show withdrawal was "
        "prevented or managed. Planning to skip the next infusion once the skin clears shows "
        "the adherence teaching has not been understood; the chapter directs the nurse to "
        "evaluate education and reinforce continuing treatment."
    ),
}, c3_tabs_p3, C3_INTRO)

case3 = base_item(
    "case_1782390000008", "NURS 1017 Unit 5 Case Study 8",
    [c3_screen1, c3_screen2, c3_screen3, c3_screen4, c3_screen5, c3_screen6],
    "A 54-year-old male client with 20 years of plaque psoriasis who progresses to "
    "generalized exfoliative dermatitis (erythroderma) after stopping methotrexate, from the "
    "emergency department through biologic therapy and discharge planning.",
)

if __name__ == "__main__":
    write_draft(case1)
    write_draft(case2)
    write_draft(case3)
