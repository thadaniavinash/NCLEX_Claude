"""University of Maryland - CS8: COPD I (COPD exacerbation in the emergency department).
Source: "COPD I DOCX" (medical-surgical); Suzana Jarquin, MSN, RN, CNEcl, Frederick Community College; September 1,
2022. The document's trend is the same question as screen 6 (same findings and key), so no stand-alone is added.
Usage: python3 drafts/build_umd_cs8.py
"""
from umd_common import *  # noqa: F401,F403

N = 8
S = f"{N:02d}"
FN = footnote("Chronic Obstructive Pulmonary Disease (COPD I)", "Suzana Jarquin, MSN, RN, CNEcl, Frederick Community "
              "College", si=False)

N1000 = note("1000", (
    "Client arrives in the emergency department with worsening shortness of breath over the past week, a strong "
    "productive cough with green-tinged sputum, and fatigue. History of chronic obstructive pulmonary disease "
    "(emphysema); has been using the &ldquo;relief&rdquo; inhaler at home with no relief of symptoms. Lives independently "
    "at home and smokes approximately 1 pack of cigarettes per day. Ambulatory, alert and oriented &times; 4. Coarse "
    "crackles auscultated in bilateral lower lung fields; barrel chest appearance; using accessory muscles; expiratory "
    "wheeze on auscultation. Client states there is &ldquo;less room&rdquo; to take a deep breath. Clubbing noted in all "
    "digits bilaterally."))
N1015 = note("1015", (
    "Client has increasing dyspnea and prefers to sit up in the chair. Requesting &ldquo;rescue inhaler.&rdquo; Provider "
    "notified. IV started. Ipratropium bromide and albuterol nebulizer treatment started."))
N1045 = note("1045", (
    "Ipratropium bromide and albuterol nebulizer and IV methylprednisolone completed. Assisted client onto the bed and "
    "placed in high-Fowler&rsquo;s position. Coarse crackles in bilateral upper and lower lung fields; no expiratory "
    "wheezing. Client continues to report &ldquo;severe&rdquo; shortness of breath."))

VS = [("T (oral)", "99.0&deg;F (37.2&deg;C)", "99.0&deg;F (37.2&deg;C)", "99.0&deg;F (37.2&deg;C)"),
      ("P", "104", "108", "117"), ("RR", "27", "30", "34"), ("BP", "157/86", "159/88", "167/94"),
      ("Pulse oximetry reading", "91% on room air", "90% on room air", "88% on room air"), ("Pain", "0/10", "0/10", "0/10")]


def vs(cols):
    return vitals(["1000", "1015", "1045"][:cols], [r[:cols + 1] for r in VS])


MEDS = title("Provider-ordered medications (emergency department)") + table(["Medication", "Dose, Route, Frequency"], [
    ["Ipratropium bromide and albuterol", "3 mL (ipratropium bromide 0.5 mg and albuterol 2.5 mg) by nebulizer 4 times a "
     "day; first dose now"],
    ["Acetaminophen", "500 mg PO once, as needed for moderate to severe back pain"],
    ["Methylprednisolone sodium succinate", "40 mg IV push, 1 dose now"],
    ["Amoxicillin/clavulanate", "875 mg/125 mg PO every 12 hours"],
    ["Albuterol sulfate", "2.5 mg/3 mL by nebulizer every 4 hours as needed"]])


def tabs(step):
    t = [{"id": f"nn_umd{S}", "title": "Nurses' Notes",
          "content": N1000 + (N1015 if step >= 5 else "") + (N1045 if step >= 6 else "")},
         {"id": f"vs_umd{S}", "title": "Vital Signs", "content": vs(3 if step >= 6 else 2 if step >= 5 else 1)}]
    if step >= 5:
        t.append({"id": f"meds_umd{S}", "title": "Medication Orders", "content": MEDS})
    return t


INTRO = ("A 74-year-old female client is admitted to the emergency department with increasing dyspnea, productive "
         "cough, and fatigue.")

screens = [
    (INTRO, tabs(1), {
        "type": "select_all",
        "preamble": "The nurse reviews the client&rsquo;s initial assessment.",
        "stem": "Which priority findings require <b>immediate</b> follow-up? <b>Select all that apply.</b>",
        "options": opts(("Bilateral digital clubbing", 0), ("Accessory muscle use", 1), ("Coarse crackles", 1),
                        ("Current tobacco smoker", 0), ("Green-tinged sputum", 1), ("Medication noncompliance", 0),
                        ("Temperature 99.0°F (37.2°C)", 0), ("Tachypnea", 1)),
        "explanation": (
            "Impaired gas exchange, shown by tachypnea, accessory muscle use, coarse crackles, and green-tinged sputum, "
            "is the priority.<br>The client is afebrile at 99.0&deg;F (37.2&deg;C). Digital clubbing reflects chronic "
            "hypoxemia, and the smoking history and medication noncompliance are less acute, nonurgent findings that do "
            "not require priority nursing intervention."),
    }),
    (INTRO, tabs(2), {
        "type": "matrix_mr",
        "stem": ("For each client finding, click to indicate if the finding is consistent with asthma, chronic "
                 "obstructive pulmonary disease (COPD), pneumonia, or pulmonary embolism. Each finding may support more "
                 "than one condition."),
        "matrix": matrix_mr("Finding", ["Asthma", "COPD", "Pneumonia", "Pulmonary Embolism"], [
            ("Dyspnea", [0, 1, 2, 3]), ("Productive cough", [0, 1, 2]), ("Barrel chest appearance", [1]),
            ("Digital clubbing", [1]), ("Expiratory wheezing", [0, 1, 2])]),
        "explanation": (
            "Clinical manifestations of COPD include dyspnea, cough, an increased anteroposterior diameter (barrel "
            "chest), digital clubbing, and expiratory wheezing. A barrel chest and digital clubbing are not "
            "manifestations of pneumonia, asthma, or pulmonary embolism.<br>Dyspnea occurs with all four conditions. "
            "Wheezing is rare with pulmonary embolism, and the cough is dry or blood-tinged."),
    }),
    (INTRO, tabs(3), {
        "type": "multiple_choice",
        "stem": "Which condition is the client most likely experiencing?",
        "options": opts(("Acute asthma attack", 0), ("COPD exacerbation", 1), ("Pneumonia", 0), ("Pulmonary embolism", 0)),
        "explanation": (
            "The client has a known history of COPD (emphysema), is hypoxic, uses accessory muscles to breathe, and "
            "reports worsening shortness of breath. Based on these signs, symptoms, and clinical manifestations, the "
            "client is most likely experiencing a COPD exacerbation."),
    }),
    (INTRO, tabs(4), {
        "type": "select_all",
        "preamble": "The nurse anticipates the provider&rsquo;s orders and considers possible nursing interventions.",
        "stem": "Which orders should the nurse include in the plan of care at this time? <b>Select all that apply.</b>",
        "options": opts(("Nursing: Administer oxygen via a high-flow oxygen face mask", 0),
                        ("Nursing: Place client in a high-Fowler’s position", 1),
                        ("Nursing: Encourage client use of incentive spirometer", 1),
                        ("Medication: Ondansetron", 0), ("Medication: Ipratropium bromide and albuterol", 1),
                        ("Medication: Methylprednisolone", 1)),
        "explanation": (
            "The client is experiencing a COPD exacerbation. A high-Fowler&rsquo;s position and the incentive spirometer "
            "maximize lung expansion and improve ventilatory effort. Ipratropium bromide with albuterol and "
            "methylprednisolone relieve the airway narrowing and inflammation causing the exacerbation.<br>Uncontrolled "
            "high-flow oxygen in a client with COPD can cause carbon dioxide retention (CO<sub>2</sub> narcosis); oxygen "
            "is titrated to a target saturation instead. Ondansetron is not indicated because the client has no nausea "
            "or vomiting."),
    }),
    (INTRO, tabs(5), {
        "type": "multiple_choice",
        "preamble": ("The nurse has reviewed the Nurses&rsquo; Notes and Vital Signs from 1015 and the Medication Orders. "
                     "The ipratropium bromide and albuterol treatment is given."),
        "stem": "Which medication should the nurse give next?",
        "options": opts(("Acetaminophen", 0), ("Methylprednisolone sodium succinate", 1), ("Albuterol", 0),
                        ("Amoxicillin/clavulanate", 0)),
        "explanation": (
            "IV methylprednisolone is ordered now and will reduce airway inflammation to ease breathing. The antibiotic "
            "can be given after the corticosteroid.<br>Albuterol was just given with the ipratropium nebulizer; the "
            "client needs to be reassessed to determine whether another PRN dose is needed. The client reports 0/10 "
            "pain, so acetaminophen is not needed at this time."),
    }),
    (INTRO, tabs(6), {
        "type": "matrix_mc",
        "preamble": ("The nurse has reviewed the Nurses&rsquo; Notes and Vital Signs from 1045. The nurse administers the "
                     "ordered medications and reassesses the client at 1045."),
        "stem": ("For each client finding, click to specify if the finding indicates that the client&rsquo;s status has "
                 "improved, declined, or is unchanged."),
        "matrix": matrix("Finding", ["Improved", "Declined", "Unchanged"], [
            ("Respiratory rate", 1), ("Heart rate", 1), ("Pulse oximetry reading", 1), ("Blood pressure", 1),
            ("Wheezing", 0), ("Breath sounds", 1), ("Temperature", 2)]),
        "explanation": (
            "The client&rsquo;s respiratory rate, breath sounds (crackles now in the upper and lower fields), heart rate, "
            "oxygen saturation, and blood pressure have all declined despite the ordered medications. The client no "
            "longer has expiratory wheezing, and the temperature is unchanged.<br>The nurse should promptly alert the "
            "provider, as the client&rsquo;s respiratory status is rapidly deteriorating."),
    }),
]

case = make_case(N, "", "", screens, FN)
case["description"] = ("Maryland Next Gen NCLEX Test Bank Project, September 1, 2022; Author: Suzana Jarquin, Frederick "
                       "Community College. COPD I: a 74-year-old client with a COPD exacerbation in the emergency "
                       "department; differentiating COPD from other respiratory conditions, priorities, and response "
                       "to treatment.")

NOTES = [
    "Oxygen: the client's SpO2 falls from 91% to 88% on ROOM AIR and no oxygen is ever started. Controlled oxygen "
    "(target 88-92%) is standard in a COPD exacerbation; consider adding low-flow oxygen to the 1015 note or orders, "
    "or explaining why it is withheld.",
    "Screen 2 keys digital clubbing as consistent with COPD. Clubbing is not a typical feature of COPD itself (it "
    "suggests another cause, such as lung cancer or bronchiectasis). Please review this row.",
    "Screen 4 keys \"Encourage use of incentive spirometer\" as correct during an acute exacerbation with severe "
    "dyspnea; please confirm. (Source is a grouped Nursing/Medication question; it is a Select All with the category at "
    "the start of each option.)",
    "Medication orders: acetaminophen 500 mg PO once \"PRN for moderate to severe back pain\" (the client has no "
    "back pain, and acetaminophen is usually for mild pain/fever); please review.",
    "Vital signs: the source labels the third column 1015 again; it is 1045 here (matching the 1045 note).",
    "Screen 5 rationale contained leftover text (\"Albuterol was just givenfor Q4 you can make ,\"); cleaned up. The "
    "antibiotic sentence now says it can be given after the corticosteroid.",
    "Screen 1 options were reordered so a correct answer is not listed first.",
    "No laboratory values in this case. The document's trend repeats screen 6, so no stand-alone was added.",
]

write([case], N, "COPD I", "COPD.docx", NOTES)
