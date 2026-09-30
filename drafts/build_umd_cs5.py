"""University of Maryland - CS5: Burns (second- and third-degree burns, burn shock).
Source: "Burns DOCX" (medical-surgical); Stacy McGrath, EdD, MSN, RN, Salisbury University; September 1, 2022,
updated May 16, 2023. The document's trend is the same question as screen 6, so no stand-alone is added.
Usage: python3 drafts/build_umd_cs5.py
"""
from umd_common import *  # noqa: F401,F403

N = 5
S = f"{N:02d}"
FN = footnote("Burns (2nd &amp; 3rd degree)", "Stacy McGrath, EdD, MSN, RN, Salisbury University",
              "September 1, 2022; updated May 16, 2023", si=False)

N2000 = note("2000", (
    "A 55-year-old female client arrives at the emergency department via ambulance with bilateral second- and "
    "third-degree burns to the front of the lower extremities from a house fire that occurred at 1800 today. Burns "
    "estimated at 36% of total body surface area. Client weighs 220 lb (100 kg). Fluid resuscitation started with "
    "lactated Ringer&rsquo;s IV."))
N2100 = note("2100", (
    "Admitted to the burn unit. Vital signs as noted. Morphine sulfate given for pain. Wound care provided by the "
    "nurse. Breath sounds clear. Bilateral +2 pitting edema noted in the lower extremities. Pedal pulses present by "
    "Doppler."))
N2200 = note("2200", "IV rate increased. Labs drawn. Portable chest X-ray done.")
N2300 = note("2300", "Audible stridor.")

VS = [("T", "37.8&deg;C (100&deg;F)", "37.5&deg;C (99.5&deg;F)", "37.6&deg;C (99.7&deg;F)", "37.6&deg;C (99.7&deg;F)"),
      ("HR", "130", "135", "138", "136"),
      ("RR", "28", "32", "35", "38"),
      ("BP", "88/58", "80/54", "82/56", "84/54"),
      ("Pulse oximetry reading", "92% on 4 L/min NC", "92% on 4 L/min NC", "91% on 4 L/min NC", "90% on 6 L/min NC"),
      ("Pain", "6/10", "4/10", "5/10", "5/10")]
IO = [("IV rate", "1200 mL/hr", "1200 mL/hr", "1320 mL/hr", "1320 mL/hr"),
      ("IV intake", "Started", "600 mL LR", "1200 mL LR", "1320 mL LR"),
      ("Urine output", "", "20 mL", "10 mL", "50 mL")]
TIMES = ["2000", "2100", "2200", "2300"]


def vs(cols):
    return vitals(TIMES[:cols], [r[:cols + 1] for r in VS])


def io(cols):
    return (paras("<b>Fluid resuscitation order:</b> 4 mL lactated Ringer&rsquo;s &times; kg body weight &times; % total "
                  "body surface area burned = 14,400 mL. Give half over the first 8 hours after the burn and the "
                  "second half over the remaining 16 hours.")
            + table(["Hour"] + TIMES[:cols], [[f"<b>{r[0]}</b>"] + list(r[1:cols + 1]) for r in IO]))


ORDERS = paras(
    "Obtain chest X-ray, ABG, complete metabolic panel.",
    "Oxygen per nasal cannula 2&ndash;6 L/min to maintain pulse oximetry reading at 92% or greater.",
    "Titrate IV fluids based on urine output, up to a maximum of 2000 mL/hr:<br>"
    "&nbsp;&nbsp;&lt; 15 mL/hr: increase IV rate 20%<br>&nbsp;&nbsp;15&ndash;29 mL/hr: increase IV rate 10%<br>"
    "&nbsp;&nbsp;30&ndash;50 mL/hr: leave current rate<br>&nbsp;&nbsp;&gt; 50 mL/hr: decrease IV rate 10%",
    "Give 500 mL 5% albumin over 2 hours as needed for systolic BP &lt; 80 mm Hg or diastolic BP &lt; 50 mm Hg.")
DIAG = paras("<b>Chest X-ray (2200):</b> minimal inhalation injury.")


def tabs(step):
    cols = 4 if step >= 6 else 2
    t = [{"id": f"nn_umd{S}", "title": "Nurses' Notes", "content": N2000 + N2100 + (N2200 + N2300 if step >= 6 else "")},
         {"id": f"vs_umd{S}", "title": "Vital Signs", "content": vs(cols)},
         {"id": f"io_umd{S}", "title": "Intake and Output", "content": io(cols)}]
    if step >= 5:
        t.append({"id": f"ord_umd{S}", "title": "Orders", "content": ORDERS})
    if step >= 6:
        t.append({"id": f"dx_umd{S}", "title": "Diagnostic Results", "content": DIAG})
    return t


INTRO = "The nurse cares for a 55-year-old female client admitted to the burn unit following a house fire."

screens = [
    (INTRO, tabs(1), {
        "type": "select_n", "limit": 4,
        "stem": "Select the <b>4</b> findings that are <b>most</b> urgent to follow up.",
        "options": opts(("Respirations", 1), ("Pitting edema", 0), ("Blood pressure", 1), ("Urine output", 1),
                        ("Heart rate", 1), ("Temperature", 0), ("Pulse oximetry reading", 0), ("Pain", 0)),
        "explanation": (
            "The nurse needs to follow up on findings that indicate the client may be developing respiratory distress "
            "or shock: increasing respirations, a drop in blood pressure, tachycardia, and decreased urine output.<br>"
            "The pulse oximetry reading is low but not critical. A client with burns will have pitting edema as a result "
            "of fluid shifting, but it is not a priority over airway and circulation. Clients with burns have "
            "thermoregulation and pain issues, but the airway and blood pressure need to be addressed first."),
    }),
    (INTRO, tabs(2), {
        "type": "matrix_mr",
        "stem": ("For each client finding, click to specify whether the finding is consistent with compartment "
                 "syndrome, inhalation injury, or distributive shock. Each finding may support more than one condition."),
        "matrix": matrix_mr("Finding", ["Compartment Syndrome", "Inhalation Injury", "Distributive Shock"], [
            ("Urine output", [2]), ("Tachypnea", [1, 2]), ("Blood pressure", [2]), ("Peripheral edema", [0, 2]),
            ("Pain", [0])]),
        "explanation": (
            "A client progressing into shock from burn injuries has a low blood pressure and an elevated heart rate and "
            "respiratory rate. Fluid shifts cause peripheral edema, and as the client becomes hypovolemic the urine "
            "output declines.<br>Clients with compartment syndrome have pain and peripheral edema. Clients with burns "
            "can develop airway obstruction at any point after the event from smoke or inhalation injury, which "
            "manifests as tachypnea, dyspnea, or changes in breath sounds."),
    }),
    (INTRO, tabs(3), {
        "type": "dyad",
        "stem": "Complete the following sentences by choosing from the lists of options.",
        "cloze": cloze("The client is at most risk for complications associated with [[drop0]]. The client care priority "
                       "is to [[drop1]].",
                       [("compartment syndrome", 0), ("inhalation injury", 0), ("distributive shock", 1)],
                       [("assist with intubation", 0), ("increase fluids", 1), ("relieve compression", 0)]),
        "explanation": (
            "Clients with major burns can go into shock because of massive fluid shifts. Signs of distributive shock "
            "include an increased heart rate and respiratory rate and a decreased blood pressure, so the priority is to "
            "increase fluids.<br>While the respiratory rate is increasing, the pulse oximetry reading is not "
            "decreasing on low-flow oxygen. Edema is seen with compartment syndrome, but the pain is typically severe "
            "and there would be other neurovascular findings."),
    }),
    (INTRO, tabs(4), {
        "type": "matrix_mc",
        "preamble": "The nurse contacts the physician about the client&rsquo;s status.",
        "stem": ("What orders does the nurse anticipate including in the plan of care? For each potential order, click "
                 "to specify whether the order is indicated or not indicated."),
        "matrix": matrix("Potential Order", ["Indicated", "Not Indicated"], [
            ("Obtain a blood gas", 0), ("Double the IV infusion rate", 1), ("Monitor basic metabolic panel", 0),
            ("Obtain a chest X-ray", 0), ("Culture wounds", 1)]),
        "explanation": (
            "Aggressive fluid resuscitation is needed, but it must be done judiciously to prevent fluid overload and "
            "pulmonary complications; IV rates are typically increased by no more than 20% per hour, so doubling the "
            "rate is not indicated. A chest X-ray and blood gas should be obtained to assess pulmonary status, and "
            "monitoring the metabolic panel helps assess fluid and electrolyte imbalances.<br>It is too soon to suspect "
            "a wound infection, so wound cultures are not indicated."),
    }),
    (INTRO, tabs(5), {
        "type": "multiple_choice",
        "preamble": "The nurse has reviewed the Orders. The physician assesses the client, and the nurse receives orders.",
        "stem": "What action should the nurse take <b>first</b>?",
        "options": opts(("Obtain a chest X-ray", 0), ("Obtain an ABG", 0), ("Increase the IV rate", 1),
                        ("Give albumin", 0)),
        "explanation": (
            "The most critical intervention is to increase the IV fluids: urine output was 20 mL in the last hour, and "
            "the order calls for a 10% increase for 15&ndash;29 mL/hr. The chest X-ray and blood gas can be done after "
            "the fluids are increased. The vital signs do not yet meet the parameters for albumin."),
    }),
    (INTRO, tabs(6), {
        "type": "matrix_mc",
        "preamble": ("The nurse has reviewed the Nurses&rsquo; Notes from 2200 and 2300, the Vital Signs and Intake and "
                     "Output from 2200 and 2300, and the Diagnostic Results. The nurse reassesses the client at 2300."),
        "stem": ("For each finding, click to indicate if the finding indicates the client&rsquo;s condition has improved, "
                 "declined, or is unchanged."),
        "matrix": matrix("Finding", ["Improved", "Declined", "Unchanged"], [
            ("Blood pressure", 2), ("Heart rate", 2), ("Urine output", 0), ("Oxygen saturation", 1),
            ("Breath sounds", 1), ("Temperature", 2)]),
        "explanation": (
            "The client&rsquo;s hemodynamic status is stabilizing, with fairly consistent heart rate and blood pressure "
            "measurements, and the temperature has remained stable. A urine output of 50 mL in the last hour is a sign "
            "of improved renal perfusion.<br>Stridor and a decreasing pulse oximetry reading on more oxygen suggest the "
            "development of upper airway edema."),
    }),
]

case = make_case(N, "", "", screens, FN)
case["description"] = ("Maryland Next Gen NCLEX Test Bank Project, September 1, 2022 (updated May 16, 2023); Author: "
                       "Stacy McGrath, Salisbury University. Burns: a 55-year-old client with 2nd- and 3rd-degree burns "
                       "develops burn shock during fluid resuscitation and then signs of upper airway edema.")

NOTES = [
    "Total body surface area: the source says 36% TBSA for burns to the front of both lower extremities; by the rule "
    "of nines, the anterior surfaces of both legs are about 18%. The 14,400 mL Parkland calculation (4 mL × 100 kg × "
    "36%) depends on 36%. Consider changing the burn description (e.g. front and back of both legs) so the numbers "
    "agree.",
    "Intake and Output: at 2200 the urine output was 10 mL/hr, which under the titration order (< 15 mL/hr: increase "
    "20%) should raise the rate at 2300 (1320 → about 1584 mL/hr), but the chart keeps 1320 mL/hr. Kept as in the "
    "source; please review.",
    "Fluid order wording: the source says \"give half 8 hours since burn event and the second half over remaining 24 "
    "hours\"; it now reads \"over the first 8 hours ... over the remaining 16 hours\" (the Parkland formula).",
    "Vital signs: screens 3 and 4 of the source label the second column 2030 (2100 elsewhere); 2100 is used "
    "throughout.",
    "Screen 1 (\"drag the 4 findings\") is a Select 4 question in the app (same content and 0/1 scoring).",
    "Screen 5 rationale: a sentence tying \"increase the IV rate\" to the urine-output titration order was added.",
    "Albumin order: \"systolic B/P<80, diastolic B/P<50\" now reads \"systolic BP < 80 or diastolic BP < 50\"; please "
    "confirm \"or\" vs \"and\".",
    "No laboratory values in this case (no SI conversion needed). The document's trend is the same question as screen "
    "6, so no stand-alone was added.",
]

write([case], N, "Burns", "Burn.docx", NOTES)
