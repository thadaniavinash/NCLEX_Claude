"""University of Maryland - CS10: Deep vein thrombosis II (heparin therapy, warfarin discharge teaching), with its
stand-alone bow-tie (pulmonary embolism).
Source: "Deep Vein Thrombosis II DOCX" (medical-surgical); Dawn Leukhardt, MSN, RN, College of Southern Maryland,
La Plata, Maryland; September 1, 2022.
Usage: python3 drafts/build_umd_cs10.py
"""
from umd_common import *  # noqa: F401,F403

N = 10
S = f"{N:02d}"
AUTH = "Dawn Leukhardt, MSN, RN, College of Southern Maryland, La Plata, Maryland"
FN = footnote("Deep Vein Thrombosis II", AUTH, si=False)
FN_B = footnote("Deep Vein Thrombosis II", AUTH, kind="medical-surgical faculty case study, stand-alone bow-tie", si=False)

D1_0930 = note("Day 1 0930", (
    "<b>Admission note:</b> Client admitted from the emergency department via stretcher and transferred to bed. Alert and "
    "oriented. Saline lock IV in the R antecubital vein, patent. R lower extremity has 2+ pedal edema; pain 8/10 in the "
    "right calf. Warmth noted to right calf. Positive motion and sensation in the R lower extremity. Right pedal pulse "
    "weak, palpable. R lower extremity elevated on 2 pillows. VS: BP 145/82, HR 96, RR 16, T 36.7&deg;C (98&deg;F). "
    "Client ordered to be on complete bedrest; client made aware."))
D1_1010 = note("Day 1 1010", ("Radiology called results of right leg ultrasound: positive for deep vein thrombosis of "
                              "the right posterior tibial vein. Provider made aware. New orders pending."))
D1_1018 = note("Day 1 1018", "Orders have been entered.")

ORD_ROWS = [
    ["<b>Labs</b>", "Draw prothrombin time (PT) and partial thromboplastin time (PTT) STAT."],
    ["<b>Medications</b>", "Administer heparin 80 units/kg IV bolus now.<br>After the initial bolus, begin heparin "
     "weight-based protocol continuous IV infusion: <b>starting dose</b> 18 units/kg/hr.<br>Draw PTT 6 hours after the "
     "infusion begins, then every 6 hours. Call results."],
    ["<b>Nursing</b>", "Activity: strict bedrest.<br>Place compression stockings on bilateral lower extremities.<br>Elevate "
     "right lower extremity.<br>Closely monitor for signs of bleeding."],
]
DAY3 = ["<b>Day 3: Discharge planning</b>", "Discharge home. Provide discharge teaching for anticoagulation therapy "
        "(warfarin) and deep vein thrombosis prevention. Follow up in 1 week."]


def orders(day3):
    return table(["Category", "Orders"], ORD_ROWS + ([DAY3] if day3 else []))


PROGRESS = note("Day 3 1015", (
    "Client cleared for discharge home. Heparin discontinued as ordered; warfarin started. Discharge instructions "
    "provided, including warfarin therapy, prevention of deep vein thrombosis, and risk reduction (health and weight "
    "management). Client able to state self-management of discharge teaching; clarification provided as needed. Client "
    "to follow up in 1 week. Discharged via wheelchair with all belongings."))


def tabs(step):
    t = [{"id": f"nn_umd{S}", "title": "Nurses' Notes",
          "content": D1_0930 + (D1_1010 if step >= 4 else "") + (D1_1018 if step >= 5 else "")}]
    if step >= 5:
        t.append({"id": f"ord_umd{S}", "title": "Orders", "content": orders(step >= 6)})
    if step >= 6:
        t.append({"id": f"pn_umd{S}", "title": "Progress Notes", "content": PROGRESS})
    return t


INTRO = ("The nurse on the medical-surgical unit is caring for a 69-year-old male client with pain and swelling of the "
         "right lower extremity.")

screens = [
    (INTRO, tabs(1), {
        "type": "select_n", "limit": 4,
        "stem": "Select the <b>4</b> findings that are <b>most</b> concerning.",
        "options": opts(("Positive motion of R lower extremity", 0), ("2+ pedal edema", 1), ("Pain 8/10 in right calf", 1),
                        ("Warmth noted to right calf", 1), ("Right pedal pulse weak", 1),
                        ("Right lower extremity elevated", 0), ("Blood pressure 145/82", 0), ("HR 96", 0),
                        ("Positive sensation of R lower extremity", 0)),
        "explanation": (
            "The nurse should recognize signs of a possible deep vein thrombosis: pedal edema, calf pain, warmth of the "
            "right calf, and a weak pedal pulse.<br>Positive motion and sensation are expected and not concerning. The "
            "blood pressure and heart rate are borderline, likely related to the pain, and not a primary concern. The "
            "elevation of the extremity and the bedrest order must be followed but are not concerning findings about "
            "the client&rsquo;s condition."),
    }),
    (INTRO, tabs(2), {
        "type": "matrix_mr",
        "stem": ("For each potential assessment finding, click to indicate if the finding is consistent with a deep vein "
                 "thrombosis, a soft tissue injury, or an infection. Each finding may be consistent with more than one "
                 "condition."),
        "matrix": matrix_mr("Potential Assessment Finding", ["Deep Vein Thrombosis", "Soft Tissue Injury", "Infection"], [
            ("Edema", [0, 1, 2]), ("Decreased pedal pulse", [0]), ("Pain", [0, 1, 2]), ("Warmth to the calf", [0, 2]),
            ("Limited range of motion", [1])]),
        "explanation": (
            "Edema and pain are consistent with all three problems. Warmth of the calf may be seen with infection and "
            "DVT.<br>A decreased pedal pulse is most suggestive of DVT. Limited range of motion is consistent with a soft "
            "tissue injury, but not with DVT."),
    }),
    (INTRO, tabs(3), {
        "type": "drag_drop_cloze",
        "stem": "Drag the most appropriate choice from the list of options to fill in the blank of the following sentence.",
        "cloze": cloze("The nurse should recognize that the client is most likely experiencing [[drop0]].",
                       [("cellulitis of the right lower extremity", 0), ("right leg deep vein thrombosis", 1),
                        ("sprain of the right leg", 0), ("osteomyelitis of the right leg", 0)]),
        "explanation": (
            "The most likely cause of the client&rsquo;s symptoms is a right leg deep vein thrombosis (DVT). Some symptoms "
            "are consistent with other causes, such as a sprain or an infection, but the only diagnosis consistent with "
            "all of the client&rsquo;s symptoms is DVT."),
    }),
    (INTRO, tabs(4), {
        "type": "matrix_mc",
        "preamble": "The nurse has reviewed the Nurses&rsquo; Notes from Day 1 1010 with the radiology results.",
        "stem": ("For each potential intervention, click to specify whether the intervention is indicated or "
                 "contraindicated in the plan of care."),
        "matrix": matrix("Potential Intervention", ["Indicated", "Contraindicated"], [
            ("Obtain partial thromboplastin times", 0), ("Begin anticoagulation therapy", 0),
            ("Compression stockings to bilateral lower extremities", 0), ("Ambulate client 3 times a day", 1),
            ("Elevate right lower extremity", 0), ("Massage right lower extremity 2 times daily", 1)]),
        "explanation": (
            "The nurse should anticipate anticoagulation therapy, which may include an initial bolus dose of heparin "
            "followed by a continuous infusion; heparin requires a baseline PTT and monitoring of the PTT every 6 hours "
            "per protocol. Compression stockings and elevation of the right lower extremity are indicated.<br>Ambulation "
            "is contraindicated until anticoagulation has begun, because of the risk of dislodging the thrombus. Massage "
            "is contraindicated because it can dislodge the thrombus."),
    }),
    (INTRO, tabs(5), {
        "type": "matrix_mc",
        "preamble": "The nurse has reviewed the Nurses&rsquo; Notes from Day 1 1018 and the Orders.",
        "stem": ("For each order, click to specify if the nurse should implement the order immediately, within the next "
                 "hour, or before the end of the shift."),
        "matrix": matrix("Order", ["Immediately", "Within the Hour", "Before the End of the Shift"], [
            ("Draw PT/PTT", 0), ("Administer heparin 80 units/kg IV bolus", 1),
            ("Begin heparin at 18 units/kg/hr", 1), ("Redraw PTT 6 hours after start of heparin", 2),
            ("Strict bedrest", 0), ("Place compression stockings on lower extremities", 2),
            ("Elevate right lower extremity", 1), ("Closely monitor for signs of bleeding", 1)]),
        "explanation": (
            "The PT/PTT should be drawn immediately because it is a STAT order and the heparin cannot be started until "
            "it is done. Strict bedrest is implemented immediately, as ordered.<br>The heparin bolus and the initial "
            "infusion should begin within the hour to prevent extension of the DVT, and monitoring for bleeding begins "
            "with the bolus. The right leg should be elevated soon, but it is not the first priority.<br>The PTT is "
            "redrawn 6 hours after the infusion starts, per the orders. Compression stockings will likely need to be "
            "obtained from supply and can be applied before the end of the shift."),
    }),
    (INTRO, tabs(6), {
        "type": "select_all",
        "preamble": ("The nurse has reviewed the Day 3 Orders and the Progress Notes. The client is reassessed on the "
                     "third day, and discharge orders are received."),
        "stem": "Which client statements indicate the teaching was understood? <b>Select all that apply.</b>",
        "options": opts(("“To relieve my stress, I should have a glass of wine before dinner.”", 0),
                        ("“I will eat more spinach and kale every day.”", 0),
                        ("“I will throw away my straight razor and buy an electric one.”", 1),
                        ("“If I miss a dose of my medicine, I will contact my doctor.”", 1),
                        ("“Controlling my blood pressure is not important.”", 0),
                        ("“When I travel, I will get out and walk every 3–4 hours.”", 0),
                        ("“I set an alarm so I take my medicine at the same time daily.”", 1)),
        "explanation": (
            "Because of the bleeding risk, the client should use an electric razor. Warfarin is taken at the same time "
            "every day, so the client should contact the provider for instructions if a dose is missed.<br>Alcohol "
            "should be avoided because it increases the effect of warfarin and the risk of bleeding. Green leafy "
            "vegetables contain vitamin K, which can decrease the effect of warfarin, so the intake should stay "
            "consistent rather than increase. The client should maintain a healthy weight and control blood pressure to "
            "reduce the risk of another DVT, and when traveling should get up and walk every 1&ndash;2 hours."),
    }),
]

case = make_case(N, "", "", screens, FN)
case["description"] = ("Maryland Next Gen NCLEX Test Bank Project, September 1, 2022; Author: Dawn Leukhardt, College of "
                       "Southern Maryland. Deep vein thrombosis II: a 69-year-old client with a right leg DVT; heparin "
                       "protocol, prioritizing orders, and warfarin discharge teaching.")

bow = make_standalone(N, 1, "Bowtie", "Stand-alone bow-tie for University of Maryland - CS10 (DVT II): pulmonary embolism.",
                      ("A 69-year-old male client with a recent diagnosis of deep vein thrombosis is seen in the emergency "
                       "department."),
                      [{"id": f"nn_umd{S}b", "title": "Nurses' Notes", "content": note("1520", (
                          "<b>Emergency department triage note:</b> The client arrives by ambulance with difficulty "
                          "breathing, sharp chest pain on inspiration, and cough, with onset 2 hours before arrival. Lung "
                          "sounds diminished bilaterally. Client diaphoretic, tachypneic, using accessory muscles with "
                          "inspiration. VS: BP 166/103, HR 122, RR 36, T 37.2&deg;C, pulse oximetry reading 88% on room "
                          "air. Client immediately placed in a room. Provider called to bedside for rapid assessment."))}],
                      dict({"type": "bowtie",
                            "stem": ("Complete the diagram by dragging from the choices below to specify what condition "
                                     "the client is most likely experiencing, 2 actions the nurse should take to address "
                                     "that condition, and 2 parameters the nurse should monitor to assess the "
                                     "client&rsquo;s progress."),
                            "explanation": (
                                "Pulmonary embolism is the most common serious complication of deep vein thrombosis; it "
                                "presents with difficulty breathing, inspiratory chest pain, and cough. The nurse elevates "
                                "the head of the bed (high-Fowler&rsquo;s position) to promote oxygenation and prepares the "
                                "client for a STAT CT scan of the chest to confirm the diagnosis. Respiratory status and "
                                "continuous cardiac monitoring are monitored closely.<br>Oxygen is needed, but a target "
                                "saturation of 99&ndash;100% is not realistic. Antibiotics and blood cultures are not "
                                "indicated. Arterial blood gases are indicated but not hourly. BP is checked frequently "
                                "but not continuously, and renal function is checked before a contrast CT but is not the "
                                "priority for ongoing monitoring.")},
                           **bowtie([("Place client in high-Fowler’s position", 1),
                                     ("Titrate oxygen to maintain oxygen saturation of 99–100%", 0),
                                     ("Administer broad-spectrum antibiotics STAT", 0), ("Obtain 2 sets of blood cultures", 0),
                                     ("Prepare client for a STAT CT scan of the chest", 1)],
                                    [("Pneumonia", 0), ("Myocardial infarction", 0), ("Pulmonary embolism", 1),
                                     ("Fat embolism", 0)],
                                    [("Hourly arterial blood gases", 0), ("Continuous noninvasive BP monitoring", 0),
                                     ("Respiratory status", 1), ("Renal function", 0), ("Continuous cardiac monitoring", 1)])),
                      FN_B)

NOTES = [
    "Screen 2: the source table's finding labels are BLANK (only the answer marks survive). The rows were rebuilt from "
    "the rationale: Edema (all 3), Decreased pedal pulse (DVT), Pain (all 3), Warmth to the calf (DVT + infection), "
    "Limited range of motion (soft tissue injury). Please confirm the labels and their order against the online "
    "version.",
    "A weak pedal pulse is keyed as a DVT finding (screens 1 and 2). DVT is a venous problem and does not usually reduce "
    "arterial pulses; a weak pulse suggests arterial compromise. Consider revising the chart finding and key.",
    "Screens 4-5: strict bedrest and \"ambulation contraindicated\" reflect older practice. Current guidelines "
    "(CHEST/ASH) support early ambulation once anticoagulation has started. Consider rewording (e.g. \"until "
    "anticoagulation is therapeutic\") or changing the key. Compression stockings for acute DVT are also no longer "
    "routinely recommended.",
    "Heparin orders are weight-based (80 units/kg bolus, 18 units/kg/hr), but no weight is charted. Consider adding the "
    "client's weight.",
    "Screen 6: \"I will eat more spinach and kale every day\" is keyed no understanding (source: avoid green leafy "
    "vegetables). Current teaching is to keep vitamin K intake consistent rather than avoid it; the rationale now says so.",
    "Screens 3-4 of the source add \"Positive Homan's sign\" to the admission note, but screens 1, 2, 5 and 6 do not. It "
    "was left out everywhere (Homans' sign is unreliable and no longer taught as a DVT sign), so the chart does not "
    "change between screens.",
    "Screen 1 options were reordered so a correct answer is not listed first. No laboratory values in this case.",
]

write([case, bow], N, "Deep Vein Thrombosis II", "Deep-Vein-Thrombosis-II.docx", NOTES)
