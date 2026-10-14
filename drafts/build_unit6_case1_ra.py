"""Builds NURS 1017 Unit 6 Case Study 1 (rheumatoid arthritis) as app-ready JSON.

Written 14 Oct 2026 for the Unit 6 review class (user request). Follows the clinical judgment model
(6 screens), keeps every chart tab and entry on later screens (chart carry-forward), uses SI units and
MCC reference ranges (js/lab-ranges.js) where MCC lists the test. Screen 2 is the matrix multiple-response
question the user asked for: manifestations and results of RA vs osteoarthritis vs osteomyelitis.
"""
import json, os

ID = "case_1782400000001"
TITLE = "NURS 1017 Unit 6 Case Study 1"
UNIT = "Unit 6 (Musculoskeletal Disorders)"
TH = 'style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;"'
TD = 'style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;"'


def table(headers, rows):
    head = "".join(f"<th {TH}>{h}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td {TD}>{c}</td>" for c in r) + "</tr>" for r in rows)
    return (f'<table class="nclex-editor-table" style="width:100%; border-collapse:collapse; margin:12px 0;">'
            f"<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>")


def notes(entries):
    return "".join(f'<p class="nurse-note-row"><span class="nurse-note-time">{t}:</span>'
                   f'<span class="nurse-note-text">{x}</span></p>' for t, x in entries)


def tab(tid, title, content):
    return {"id": tid, "title": title, "content": content}


def opts(*pairs):
    return [{"text": t, "correct": c} for t, c in pairs]


def matrix_mc(header, columns, rows):
    return {"firstColumnHeader": header, "columns": columns,
            "rows": [{"text": t, "correctIndex": i, "correctIndices": [i]} for t, i in rows]}


def matrix_mr(header, columns, rows):
    return {"firstColumnHeader": header, "columns": columns,
            "rows": [{"text": t, "correctIndex": ix[0], "correctIndices": list(ix)} for t, ix in rows]}


def dropdown(*pairs):
    return {"placeholder": "Select...", "options": opts(*pairs)}


def rationale(*items):
    return "<br><br>".join(items)


# ---------------------------------------------------------------- chart content (cumulative)
NOTE_D1 = [
    ("Day 1 0900", "54-year-old female client referred by her primary care provider to the rheumatology clinic. Reports 4 months of pain and swelling "
     "in both hands and wrists, with morning stiffness that lasts about 2 hours: “My hands feel like they are stuck in tight gloves until "
     "lunchtime.” Has trouble opening jars and doing up buttons. Reports fatigue, needing a nap most afternoons, feeling feverish at times, and an "
     "unintended weight loss of 3 kg. Takes ibuprofen 400 mg three times daily with partial relief. Medical history: hypertension (amlodipine "
     "5 mg daily); menopause at age 50. Smokes 20 cigarettes per day for 30 years; drinks 1 to 2 glasses of wine most evenings. Works as a bank "
     "teller. Her mother had “arthritis in her knees” in her 70s."),
    ("Day 1 0920", "Both wrists and the 2nd and 3rd metacarpophalangeal (MCP) and proximal interphalangeal (PIP) joints of both hands are swollen, "
     "warm, and tender, and feel boggy (spongy) on palpation. Distal interphalangeal (DIP) joints are not swollen. Unable to make a full fist; "
     "grip weak bilaterally. Firm, nontender, movable 1-cm subcutaneous nodule over the right olecranon. Right knee: crepitus on flexion, no "
     "warmth or effusion; client reports the knee “aches after long walks” since a soccer injury at age 30. Skin intact, no rash. Lungs clear. "
     "Pain in the hands rated 6/10."),
]
NOTE_D3 = [
    ("Day 3 1400", "Client returns to review her laboratory and X-ray results with the rheumatologist and the nurse. Asks, “My mother had arthritis "
     "too. Is this the same thing she had?”"),
]
NOTE_D3B = [
    ("Day 3 1430", "The rheumatologist confirms a diagnosis of seropositive rheumatoid arthritis of the hands and wrists, and osteoarthritis of the "
     "right knee. Treatment plan discussed (see Orders). Baseline CBC, ALT, albumin, creatinine, hepatitis B and C serology and chest X-ray are "
     "normal. Client states, “I just want my hands back. I can’t afford to lose my job.”"),
]
NOTE_D26 = [
    ("Day 26 0830", "Client arrives at the clinic without an appointment, reporting a sore throat, painful mouth sores, and feeling hot and shaky since "
     "yesterday. Oral mucosa has several shallow ulcers; gums bleed easily. She brings her pill bottles: the pharmacy changed the methotrexate tablet "
     "brand, and she says she has taken methotrexate 15 mg “every morning with my prednisone” for the past 5 days. Last dose at 0700 today. "
     "Provider notified; client admitted to the medical unit (see Orders)."),
]
NOTE_D180 = [
    ("Day 180 0900", "Six-month follow-up. Methotrexate was restarted at 15 mg once weekly (Mondays) after her blood counts recovered, with pharmacist "
     "teaching and a weekly pill organizer; prednisone was tapered off. Morning stiffness now lasts about 15 minutes. Swollen joint count 1 "
     "(right 2nd MCP), was 10 on Day 1. Working full time. Reports no alcohol since Day 26. Now smokes 10 cigarettes per day. Bone mineral density "
     "results reviewed (see Diagnostic Results)."),
    ("Day 180 0920", "Client states: “I take my methotrexate every Monday, and the pill organizer means I can’t take it twice.” Later adds: “My hands "
     "are so much better that I’ll stop the methotrexate when I finish this bottle. I don’t want to take it forever.”"),
]

VS_COLS = ["", "Day 1 0900", "Day 26 0830", "Day 180 0900"]
VS_ROWS = [
    ("<b>T</b>", ["37.8° C", "38.6° C", "36.7° C"]),
    ("<b>P</b>", ["88 beats/min", "112 beats/min", "76 beats/min"]),
    ("<b>RR</b>", ["16 breaths/min", "20 breaths/min", "16 breaths/min"]),
    ("<b>BP</b>", ["138/84 mm Hg", "112/68 mm Hg", "132/80 mm Hg"]),
    ("<b>Pulse Oximetry Reading (SpO<sub>2</sub>)</b>", ["97% on room air", "96% on room air", "98% on room air"]),
]

LAB_COLS = ["Laboratory Test and Reference Range", "Day 1 0930", "Day 26 0845", "Day 180 0900"]
LAB_ROWS = [
    ("<b>Hemoglobin (Hgb)</b><br>Female: 115–155 g/L", ["108 g/L", "102 g/L", "128 g/L"]),
    ("<b>White blood cell (WBC) count</b><br>3.5–10.5 × 10<sup>9</sup>/L", ["9.6 × 10<sup>9</sup>/L", "1.6 × 10<sup>9</sup>/L", "6.2 × 10<sup>9</sup>/L"]),
    ("<b>Neutrophils, absolute</b><br>2.0–7.5 × 10<sup>9</sup>/L", ["6.4 × 10<sup>9</sup>/L", "0.4 × 10<sup>9</sup>/L", "3.8 × 10<sup>9</sup>/L"]),
    ("<b>Platelet count</b><br>130–380 × 10<sup>9</sup>/L", ["428 × 10<sup>9</sup>/L", "74 × 10<sup>9</sup>/L", "262 × 10<sup>9</sup>/L"]),
    ("<b>Erythrocyte sedimentation rate (ESR)</b><br>Female: 0–20 mm/h", ["48 mm/h", "52 mm/h", "14 mm/h"]),
    ("<b>C-reactive protein (CRP)</b><br>≤ 10 mg/L", ["38 mg/L", "64 mg/L", "4 mg/L"]),
    ("<b>Rheumatoid factor (RF)</b><br>≤ 20 kIU/L", ["86 kIU/L", "", ""]),
    ("<b>Anti-cyclic citrullinated peptide (anti-CCP) antibodies</b><br>&lt; 20 U/mL", ["210 U/mL", "", ""]),
    ("<b>Antinuclear antibodies (ANA)</b><br>Negative", ["Negative", "", ""]),
    ("<b>Uric acid</b><br>Female: 155–400 µmol/L", ["286 µmol/L", "", ""]),
    ("<b>Alanine aminotransferase (ALT)</b><br>17–63 IU/L", ["24 IU/L", "118 IU/L", "28 IU/L"]),
    ("<b>Creatinine</b><br>Female: 22–75 µmol/L", ["64 µmol/L", "72 µmol/L", "66 µmol/L"]),
]


def vitals(ncols):
    return tab("ra_vs", "Vital Signs", table(VS_COLS[:ncols + 1], [[r] + v[:ncols] for r, v in VS_ROWS]))


def labs(ncols):
    rows = [[r] + v[:ncols] for r, v in LAB_ROWS]
    return tab("ra_labs", "Laboratory Results", table(LAB_COLS[:ncols + 1], rows))


DX_D3 = [
    ("Day 1 1000", "<b>X-ray, both hands and wrists:</b> periarticular osteopenia; symmetric, uniform joint-space narrowing of the 2nd and 3rd MCP "
     "and PIP joints and both wrists; marginal erosions at the 2nd and 3rd metacarpal heads bilaterally. No osteophytes. DIP joints normal."),
    ("Day 1 1010", "<b>X-ray, right knee:</b> narrowing of the medial joint space with osteophytes (bone spurs) at the joint margins and subchondral "
     "sclerosis. No erosions, effusion, or fracture."),
]
DX_D180 = [
    ("Day 180 0800", "<b>Bone mineral density (DEXA):</b> lumbar spine T-score −2.6; left femoral neck T-score −2.1."),
]


def dx(entries):
    return tab("ra_dx", "Diagnostic Results", notes(entries))


ORD_D3 = [
    ("Day 3 1430", "Methotrexate 15 mg PO once <b>weekly</b>, every Monday.<br>"
     "Folic acid 1 mg PO once daily.<br>"
     "Prednisone 10 mg PO once daily with breakfast for 6 weeks, then taper as directed (until methotrexate takes effect).<br>"
     "CBC, ALT, albumin and creatinine every 4 weeks for 3 months, then every 8 to 12 weeks.<br>"
     "Calcium 1,200 mg/day (diet plus supplement) and vitamin D<sub>3</sub> 1,000 IU PO daily.<br>"
     "Bone mineral density (DEXA) scan.<br>"
     "Occupational therapy (joint protection, resting wrist-hand splints) and physiotherapy referrals.<br>"
     "Smoking cessation counselling.<br>"
     "Vaccines: pneumococcal, recombinant zoster, and annual inactivated influenza."),
]
ORD_D26 = [
    ("Day 26 0900", "Admit to the medical unit, private room.<br>"
     "Hold methotrexate.<br>"
     "Leucovorin (folinic acid) 15 mg IV every 6 hours.<br>"
     "Blood cultures × 2, then piperacillin-tazobactam 4.5 g IV every 6 hours.<br>"
     "Continue prednisone 10 mg PO once daily.<br>"
     "0.9% sodium chloride IV at 100 mL/h.<br>"
     "CBC, ALT and creatinine daily.<br>"
     "Saline mouth rinses every 4 hours while awake."),
]


def orders(entries):
    return tab("ra_ord", "Orders", notes(entries))


def nn(entries):
    return tab("ra_nn", "Nurses' Notes", notes(entries))


INTRO = "The nurse in an outpatient rheumatology clinic is caring for a 54-year-old female client with pain and swelling in both hands."

# ---------------------------------------------------------------- screens
screens = [
    {  # 1 Recognize cues
        "step": 1,
        "leftContent": {"intro": INTRO, "tabs": [nn(NOTE_D1), vitals(1)]},
        "question": {
            "type": "select_all",
            "preamble": "",
            "stem": "The nurse reviews the client's history and assessment. Which findings should the nurse recognize as cues of an "
                    "<b>inflammatory (autoimmune) arthritis</b>? <b>Select all that apply.</b>",
            "options": opts(
                ("Crepitus in the right knee, which aches after long walks", False),
                ("Morning stiffness lasting about 2 hours", True),
                ("Blood pressure 138/84 mm Hg", False),
                ("Swelling, warmth, and tenderness of the MCP and PIP joints of both hands and both wrists", True),
                ("DIP joints not swollen", False),
                ("Fatigue, temperature 37.8° C, and an unintended 3-kg weight loss", True),
                ("Mother had arthritis of the knees in her 70s", False),
                ("Joints feel boggy (spongy) on palpation", True),
                ("Firm, nontender subcutaneous nodule over the right olecranon", True),
            ),
            "explanation": rationale(
                "<b>Cues of inflammatory (autoimmune) arthritis:</b>",
                "<b>Prolonged morning stiffness:</b> stiffness lasting more than 1 hour after rest is typical of inflammatory arthritis. Fluid and "
                "inflammatory mediators build up in the inflamed synovium overnight. In osteoarthritis, stiffness usually lasts less than 30 minutes.",
                "<b>Symmetric small-joint swelling:</b> rheumatoid arthritis (RA) classically involves the same small joints on both sides "
                "(MCP, PIP, wrists). Warmth and tenderness show active synovitis.",
                "<b>Boggy joints:</b> a soft, spongy feel comes from thickened, inflamed synovium and joint fluid. Osteoarthritis joints feel hard "
                "and bony.",
                "<b>Systemic signs:</b> fatigue, low-grade fever and weight loss reflect circulating inflammatory cytokines (TNF-α, IL-6). RA is a "
                "systemic disease, not only a joint disease.",
                "<b>Rheumatoid nodule:</b> a firm, nontender nodule over a pressure point such as the olecranon is an extra-articular feature of RA, "
                "seen mostly in seropositive disease.",
                "<b>Not cues:</b> crepitus and pain after activity in one weight-bearing joint (the right knee) after an old injury point to "
                "osteoarthritis. The mother's knee arthritis in her 70s also sounds like osteoarthritis. Sparing of the DIP joints is expected in RA "
                "and is not a sign of disease. The blood pressure reflects her treated hypertension."),
        },
    },
    {  # 2 Analyze cues
        "step": 2,
        "leftContent": {"intro": INTRO, "tabs": [nn(NOTE_D1 + NOTE_D3), vitals(1), labs(1), dx(DX_D3)]},
        "question": {
            "type": "matrix_mr",
            "preamble": "The nurse has reviewed the Nurses' Notes from Day 3 1400, the Laboratory Results and the Diagnostic Results.",
            "stem": "The nurse prepares to answer the client's question about how her condition differs from other bone and joint disorders. For each "
                    "finding, click to specify whether it is consistent with <b>rheumatoid arthritis</b>, <b>osteoarthritis</b>, or "
                    "<b>osteomyelitis</b>. Each finding may support more than one condition.",
            "matrix": matrix_mr("Finding", ["Rheumatoid arthritis", "Osteoarthritis", "Osteomyelitis"], [
                ("Morning stiffness lasting longer than 1 hour", [0]),
                ("Stiffness lasting less than 30 minutes after rest; pain worse with use and relieved by rest", [1]),
                ("Symmetric swelling of the MCP and PIP joints of both hands", [0]),
                ("Hard, bony enlargement of the DIP joints (Heberden nodes)", [1]),
                ("Positive rheumatoid factor and anti-CCP antibodies", [0]),
                ("Elevated ESR and C-reactive protein", [0, 2]),
                ("Elevated WBC count and a bone culture growing Staphylococcus aureus", [2]),
                ("Joint-space narrowing on X-ray", [0, 1]),
                ("Osteophytes (bone spurs) and subchondral sclerosis on X-ray", [1]),
                ("Sequestrum (dead bone) on imaging and a draining sinus tract", [2]),
            ]),
            "explanation": rationale(
                "<b>Rheumatoid arthritis (RA)</b> is a systemic autoimmune disease of the synovium. Long morning stiffness (over 1 hour), symmetric "
                "swelling of small joints (MCP, PIP, wrists), positive rheumatoid factor and especially <b>anti-CCP antibodies</b> (highly specific "
                "for RA) are typical. Inflammation raises the <b>ESR and CRP</b>. X-rays show periarticular osteopenia, uniform "
                "<b>joint-space narrowing</b> and marginal erosions (as in this client's hands).",
                "<b>Osteoarthritis (OA)</b> is a degenerative disease of articular cartilage, not an autoimmune one. Stiffness after rest is brief "
                "(under 30 minutes), and pain worsens with use and eases with rest. Bony enlargement of the DIP joints (<b>Heberden nodes</b>) and "
                "PIP joints (Bouchard nodes) is typical. ESR and CRP are usually normal and serology is negative. X-rays show uneven "
                "<b>joint-space narrowing</b>, <b>osteophytes</b> and subchondral sclerosis (as in this client's right knee).",
                "<b>Osteomyelitis</b> is an infection of bone, most often by <i>Staphylococcus aureus</i>, spread through the blood or from an open "
                "fracture, surgery or a nearby wound. Infection causes fever, an elevated <b>WBC count</b>, and raised <b>ESR and CRP</b> (used to "
                "follow the response to antibiotics). A bone biopsy and culture identify the organism. In chronic osteomyelitis, dead bone "
                "(<b>sequestrum</b>) is walled off by new bone (involucrum), and pus may drain through a <b>sinus tract</b> to the skin.",
                "<b>Shared findings:</b> ESR and CRP rise with inflammation from any cause (RA and osteomyelitis). Joint-space narrowing occurs in "
                "both RA and OA, because both destroy articular cartilage, by different mechanisms."),
        },
    },
    {  # 3 Prioritize hypotheses
        "step": 3,
        "leftContent": {"intro": INTRO, "tabs": [nn(NOTE_D1 + NOTE_D3), vitals(1), labs(1), dx(DX_D3)]},
        "question": {
            "type": "dropdown_cloze",
            "preamble": "",
            "stem": "Complete the following sentences by choosing from the lists of options.",
            "cloze": {
                "text": "The client's hand and wrist findings are most consistent with [[drop0]], as evidenced by [[drop1]]. Her right knee findings "
                        "are most consistent with [[drop2]]. In her hands, joint destruction is caused by [[drop3]].",
                "dropdowns": [
                    dropdown(("gout", False), ("osteoarthritis", False), ("rheumatoid arthritis", True), ("osteomyelitis", False)),
                    dropdown(("the 30 pack-year smoking history", False),
                             ("a normal uric acid level", False),
                             ("symmetric MCP and PIP synovitis, a positive anti-CCP, and marginal erosions", True),
                             ("osteophytes and subchondral sclerosis", False)),
                    dropdown(("osteoarthritis", True), ("rheumatoid arthritis", False), ("osteomyelitis", False), ("gout", False)),
                    dropdown(("bacterial infection spreading through the bone", False),
                             ("urate crystals deposited in the joint", False),
                             ("mechanical wear of cartilage with bone spur formation", False),
                             ("inflamed synovium forming pannus that erodes cartilage and bone", True)),
                ],
            },
            "explanation": rationale(
                "<b>Rheumatoid arthritis of the hands and wrists:</b> symmetric synovitis of the MCP and PIP joints and wrists, a strongly positive "
                "anti-CCP (210 U/mL) and rheumatoid factor, raised ESR and CRP, anemia of chronic inflammation (Hgb 108 g/L), and marginal erosions "
                "on X-ray. Smoking is a risk factor for RA but is not evidence that she has it. A normal uric acid argues against gout but does not "
                "show RA. Osteophytes and subchondral sclerosis are OA findings.",
                "<b>Osteoarthritis of the right knee:</b> one weight-bearing joint, a previous injury, pain after use, crepitus without warmth or "
                "effusion, and osteophytes with subchondral sclerosis on X-ray. A client can have both diseases; her mother's knee arthritis was "
                "most likely OA too, which answers her question.",
                "<b>How RA destroys joints:</b> autoreactive T cells and B cells (producing rheumatoid factor and anti-CCP) drive inflammation of "
                "the synovium. The synovium thickens into <b>pannus</b>, granulation tissue that releases enzymes and activates osteoclasts, eroding "
                "cartilage and the bone at the joint margins. Without early treatment this leads to permanent deformities (ulnar deviation, swan-neck "
                "and boutonnière deformities) and loss of hand function, which is why disease-modifying treatment is started promptly.",
                "<b>Why not the others:</b> mechanical wear with bone spurs is OA; urate crystals cause gout; bacterial infection of bone is "
                "osteomyelitis."),
        },
    },
    {  # 4 Generate solutions
        "step": 4,
        "leftContent": {"intro": INTRO, "tabs": [nn(NOTE_D1 + NOTE_D3 + NOTE_D3B), vitals(1), labs(1), dx(DX_D3), orders(ORD_D3)]},
        "question": {
            "type": "select_all",
            "preamble": "The nurse has reviewed the Nurses' Notes from Day 3 1430 and the Orders.",
            "stem": "The nurse plans teaching for the client. Which instructions should the nurse include? <b>Select all that apply.</b>",
            "options": opts(
                ("Rest the inflamed joints in a flexed position supported by pillows", False),
                ("Take methotrexate once a week on the same day, using a calendar or pill organizer", True),
                ("Expect methotrexate to relieve the joint pain within 2 to 3 days", False),
                ("Avoid alcohol while taking methotrexate", True),
                ("Report fever, sore throat, mouth sores, unusual bruising, or a new dry cough right away", True),
                ("Stop taking prednisone as soon as the joints feel better", False),
                ("Take a warm shower or use warm, moist heat in the morning to ease stiffness", True),
                ("Live vaccines are safe to receive while taking methotrexate", False),
                ("Use large joints and assistive devices to protect the small joints of the hands, and wear the resting splints at night", True),
                ("Stopping smoking can reduce RA activity and improve the response to treatment", True),
            ),
            "explanation": rationale(
                "<b>Weekly methotrexate:</b> for RA, methotrexate is taken <b>once a week</b>. Taking it daily by mistake is a well-known, sometimes "
                "fatal error, so a fixed day and a calendar or pill organizer are taught from the start. Folic acid reduces mouth sores, nausea and "
                "liver enzyme rises.",
                "<b>Alcohol:</b> methotrexate and alcohol are both toxic to the liver, so alcohol should be avoided (the client drinks most evenings).",
                "<b>Warning signs:</b> methotrexate can suppress the bone marrow (infection, bleeding), cause mucositis, and rarely cause "
                "pneumonitis (dry cough, shortness of breath). These are reported promptly.",
                "<b>Heat and joint protection:</b> warm, moist heat eases morning stiffness. Using larger joints (carrying a bag on the forearm), "
                "jar openers and built-up handles, and resting splints at night protect inflamed joints and keep them in a functional position. "
                "Balancing rest with gentle range-of-motion exercise maintains function.",
                "<b>Smoking:</b> smoking increases RA activity and the production of anti-CCP antibodies, and lowers the response to "
                "methotrexate. It is also a risk factor for osteoporosis.",
                "<b>Incorrect:</b> resting joints flexed on pillows leads to flexion contractures. Methotrexate takes about 6 to 12 weeks to work, "
                "which is why prednisone is used as a short bridge. Prednisone must be tapered as prescribed, never stopped suddenly (adrenal "
                "insufficiency). Live vaccines are avoided during immunosuppressive therapy; inactivated and recombinant vaccines (influenza, "
                "pneumococcal, recombinant zoster) are given."),
        },
    },
    {  # 5 Take action
        "step": 5,
        "leftContent": {"intro": INTRO, "tabs": [nn(NOTE_D1 + NOTE_D3 + NOTE_D3B + NOTE_D26), vitals(2), labs(2), dx(DX_D3),
                                                 orders(ORD_D3 + ORD_D26)]},
        "question": {
            "type": "matrix_mc",
            "preamble": "The nurse has reviewed the Nurses' Notes from Day 26 0830, the Vital Signs and Laboratory Results from Day 26, and the "
                        "Orders from Day 26.",
            "stem": "The client is admitted to the medical unit. For each nursing action, click to specify whether it is <b>indicated</b>, "
                    "<b>contraindicated</b>, or <b>nonessential</b> for the client at this time.",
            "matrix": matrix_mc("Nursing Action", ["Indicated", "Contraindicated", "Nonessential"], [
                ("Measure the temperature rectally every 4 hours", 1),
                ("Hold all further doses of methotrexate", 0),
                ("Obtain the blood cultures before giving the first dose of piperacillin-tazobactam", 0),
                ("Hold the prednisone until the infection has resolved", 1),
                ("Administer leucovorin (folinic acid) as prescribed", 0),
                ("Repeat the X-rays of both hands and wrists today", 2),
                ("Provide a soft toothbrush and saline mouth rinses", 0),
                ("Allow visitors with cold symptoms if they wear a mask", 1),
            ]),
            "explanation": rationale(
                "The client took methotrexate daily instead of weekly for 5 days and now has <b>methotrexate toxicity</b>: severe neutropenia "
                "(absolute neutrophils 0.4 × 10⁹/L), thrombocytopenia (74 × 10⁹/L), mucositis, raised ALT, and fever of 38.6° C with tachycardia "
                "(<b>febrile neutropenia</b>, a medical emergency).",
                "<b>Indicated:</b> stop the drug (hold methotrexate). Give <b>leucovorin</b>, the reduced folate that bypasses the enzyme "
                "methotrexate blocks, as the antidote. Draw <b>blood cultures before the first antibiotic dose</b> so the organism can be "
                "identified, then start the antibiotic without delay. A soft toothbrush and saline rinses reduce mucosal injury, bleeding and "
                "infection.",
                "<b>Contraindicated:</b> rectal temperatures can tear the mucosa and introduce bacteria in a neutropenic client with low platelets. "
                "Stopping long-term prednisone suddenly can cause adrenal crisis, and illness raises steroid needs; the order is to continue it. "
                "Visitors with respiratory infections should not visit a severely neutropenic client, even with a mask.",
                "<b>Nonessential:</b> repeat hand X-rays do not change the management of this emergency; joint damage is followed over months."),
        },
    },
    {  # 6 Evaluate outcomes
        "step": 6,
        "leftContent": {"intro": INTRO, "tabs": [nn(NOTE_D1 + NOTE_D3 + NOTE_D3B + NOTE_D26 + NOTE_D180), vitals(3), labs(3),
                                                 dx(DX_D3 + DX_D180), orders(ORD_D3 + ORD_D26)]},
        "question": {
            "type": "matrix_mc",
            "preamble": "The nurse has reviewed the Nurses' Notes from Day 180 0900 and 0920, the Vital Signs and Laboratory Results from Day 180, "
                        "and the Diagnostic Results from Day 180.",
            "stem": "For each finding at the 6-month follow-up, click to specify whether it shows that an <b>expected outcome has been met</b> or "
                    "that it <b>requires follow-up</b>.",
            "matrix": matrix_mc("Finding", ["Expected outcome met", "Requires follow-up"], [
                ("Morning stiffness lasting about 15 minutes", 0),
                ("Lumbar spine T-score −2.6", 1),
                ("Swollen joint count 1, down from 10", 0),
                ("Smokes 10 cigarettes per day", 1),
                ("CRP 4 mg/L and ESR 14 mm/h", 0),
                ("“I’ll stop the methotrexate when I finish this bottle.”", 1),
                ("Absolute neutrophils 3.8 × 10⁹/L and ALT 28 IU/L", 0),
                ("“I take my methotrexate every Monday, and the pill organizer means I can’t take it twice.”", 0),
                ("Hemoglobin 128 g/L", 0),
            ]),
            "explanation": rationale(
                "<b>Expected outcomes met:</b> short morning stiffness, one swollen joint (was 10), and normal CRP and ESR show that the RA is "
                "close to remission on methotrexate. Hemoglobin has risen from 108 to 128 g/L as the anemia of chronic inflammation resolves. "
                "Normal neutrophils and ALT show that the bone marrow and liver have recovered and that weekly methotrexate is tolerated. Her "
                "statement about taking it every Monday with a pill organizer shows she understands the weekly schedule.",
                "<b>Requires follow-up:</b>",
                "<b>Osteoporosis:</b> a T-score of −2.5 or lower is osteoporosis. RA itself, glucocorticoid use, postmenopausal status, smoking and "
                "alcohol all reduce bone density. The nurse reports the result so the provider can consider bone-protecting medication (for "
                "example, a bisphosphonate), and reinforces calcium, vitamin D, weight-bearing exercise and fall prevention.",
                "<b>Smoking:</b> she has halved her smoking, which is progress, but continued smoking worsens RA and bone loss. Ongoing cessation "
                "support is needed.",
                "<b>Plan to stop methotrexate:</b> RA is a chronic disease. Methotrexate controls it but does not cure it; stopping it on her own "
                "would likely cause a flare and further joint damage. Any change must be decided with the rheumatologist."),
        },
    },
]

case = {
    "id": ID,
    "title": TITLE,
    "course": "NURS 1017",
    "unit": UNIT,
    "topic": UNIT,
    "disorder": UNIT,
    "description": "54-year-old female client with symmetric hand and wrist synovitis diagnosed as seropositive rheumatoid arthritis (with "
                   "osteoarthritis of the right knee), compared with osteoarthritis and osteomyelitis; methotrexate teaching, methotrexate "
                   "toxicity with febrile neutropenia after daily dosing, and evaluation at 6 months including osteoporosis.",
    "authorReview": {
        "note": "New case written by Claude on 14 Oct 2026 for the Unit 6 review class; please review before using it with students:\n"
                "Screen 2: anti-CCP has no MCC reference range; the range used (< 20 U/mL) varies by laboratory.\n"
                "Screen 4: folic acid 1 mg daily is one common regimen (5 mg once weekly is also used in Canada); adjust to your course's "
                "reference.\n"
                "Screen 5: leucovorin dose/route and the antibiotic are examples; the key does not depend on them.\n"
                "Screen 6: osteoporosis after about 10 weeks of prednisone is attributed to several risk factors together; check the wording "
                "suits your teaching.",
        "flaggedAt": "2026-10-14",
    },
    "screens": screens,
}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{ID}_NURS_1017_Unit_6_Case_Study_1.json")
with open(out, "w") as f:
    json.dump(case, f, indent=2, ensure_ascii=False)
print("wrote", out)
