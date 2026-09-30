"""University of Maryland - CS14: HIV with an opportunistic infection (Pneumocystis pneumonia), with its trend.
Source: "HIV with Opportunistic Infection DOCX" (medical-surgical); Denyce Watties-Daniels, DNP, RN, Coppin State
University; September 1, 2022.
Usage: python3 drafts/build_umd_cs14.py
"""
from umd_common import *  # noqa: F401,F403

N = 14
S = f"{N:02d}"
AUTH = "Denyce Watties-Daniels, DNP, RN, Coppin State University"
FN = footnote("HIV with an Opportunistic Infection", AUTH)
FN_T = footnote("HIV with an Opportunistic Infection", AUTH, kind="medical-surgical faculty case study, stand-alone trend",
                si=False)

N1100 = note("1100", (
    "A 25-year-old male client who has been HIV positive for 3 years is admitted with a dry cough and a fever of "
    "101.0&deg;F (38.3&deg;C). Client has fatigue, shortness of breath, a respiratory rate of 28, and a pulse oximetry "
    "reading of 90% on room air. Breathing is slightly labored, with a tight feeling in the chest on deep inspiration. "
    "Has been on antiretroviral medications since the diagnosis of HIV but recently stopped taking them after being laid "
    "off from his job. Symptoms did not improve with over-the-counter medications after 3 days. IV of 0.9% sodium "
    "chloride started in the right arm at 75 mL/hr. Labs drawn. Bronchoalveolar lavage completed; cytology report "
    "pending."))
LABS = table(["Laboratory Test and Reference Range", "1100"], [
    [lab("Urea (BUN)", "3.6&ndash;7.1 mmol/L"), "7.9 mmol/L"],
    [lab("Creatinine", "80&ndash;124 &micro;mol/L"), "133 &micro;mol/L"],
    [lab("Hematocrit (Hct)", "Male: 0.42&ndash;0.52 L/L; Female: 0.35&ndash;0.47 L/L"), "0.48 L/L"],
    [lab("Hemoglobin (Hgb)", "Male: 130&ndash;180 g/L; Female: 120&ndash;160 g/L"), "150 g/L"],
    [lab("White blood cell (WBC) count", "4.5&ndash;10.5" + G9), "15.2" + G9],
    [lab("Platelet count", "140&ndash;450" + G9), "300" + G9],
    [lab("Prothrombin time (PT)", "9.5&ndash;12 seconds"), "10 seconds"],
    [lab("Activated partial thromboplastin time (aPTT)", "20&ndash;39 seconds"), "25 seconds"],
    [lab("Potassium", "3.5&ndash;5.0 mmol/L"), "4.5 mmol/L"],
    [lab("Sodium", "135&ndash;145 mmol/L"), "148 mmol/L"],
    [lab("CD4 T-cell count", "500&ndash;1600 cells/&micro;L"), "178 cells/&micro;L"],
])
DIAG = paras("<b>Bronchoalveolar lavage:</b> specimen shows <i>Pneumocystis jirovecii</i>.")


def tabs(step):
    t = [{"id": f"nn_umd{S}", "title": "Nurses' Notes", "content": N1100},
         {"id": f"labs_umd{S}", "title": "Laboratory Results", "content": LABS}]
    if step >= 4:
        t.append({"id": f"dx_umd{S}", "title": "Diagnostic Results", "content": DIAG})
    return t


INTRO = ("The nurse cares for a 25-year-old male client with a history of HIV admitted to the medical-surgical unit with "
         "respiratory distress.")

screens = [
    (INTRO, tabs(1), {
        "type": "select_all",
        "preamble": "The nurse reviews the client&rsquo;s laboratory report.",
        "stem": "Which laboratory findings are concerning? <b>Select all that apply.</b>",
        "options": opts(("Hematocrit", 0), ("Platelets", 0), ("Sodium", 0), ("CD4 T-cell count", 1), ("Potassium", 0),
                        ("WBC count", 1)),
        "explanation": (
            "As HIV replicates, the CD4 count declines because the virus destroys CD4 T cells. When the CD4 count falls "
            "below 500 cells/&micro;L, the person becomes susceptible to opportunistic infections, and a count below 200 "
            "cells/&micro;L means the client&rsquo;s HIV infection has progressed to AIDS. The elevated WBC count "
            "indicates that the client has an infection.<br>The hematocrit, platelets, and potassium are within normal "
            "limits."),
    }),
    (INTRO, tabs(2), {
        "type": "select_all",
        "stem": "Which client findings are risks for an opportunistic infection? <b>Select all that apply.</b>",
        "options": opts(("Three-year use of antiretroviral medications", 0), ("History of HIV", 1), ("Being 25 years old", 0),
                        ("Use of over-the-counter medications", 0), ("Stopped taking his medication", 1),
                        ("Low CD4 T-cell count", 1)),
        "explanation": (
            "Discontinuing HIV medications allows the viral load to increase. As the viral load increases, the CD4 T-cell "
            "count decreases, making the client vulnerable to opportunistic infections; AIDS is diagnosed when the CD4 "
            "count falls below 200 cells/&micro;L.<br>Taking antiretroviral medications, the client&rsquo;s age, and the "
            "use of over-the-counter medications are not risks for opportunistic infection."),
    }),
    (INTRO, tabs(3), {
        "type": "dyad",
        "preamble": "The nurse reviews the client&rsquo;s chart.",
        "stem": "Complete the following sentences by choosing from the lists of options.",
        "cloze": cloze("The nurse should first address the client&rsquo;s [[drop0]]. Next, the nurse should address the "
                       "client&rsquo;s [[drop1]].",
                       [("fever", 0), ("immunity", 0), ("infection", 0), ("oxygenation", 1)],
                       [("fever", 0), ("immunity", 0), ("infection", 1), ("oxygenation", 0)]),
        "explanation": (
            "The priority is the client&rsquo;s oxygenation: oxygen should be started immediately. Clients with HIV and a "
            "CD4 count below 200 cells/&micro;L are susceptible to opportunistic infections, and the next priority is to "
            "treat the infection.<br>The client will need to resume antiretroviral therapy to restore immunity, but that "
            "improvement occurs more slowly. The fever needs to be treated, but treating the infection is most important "
            "to recovery."),
    }),
    (INTRO, tabs(4), {
        "type": "matrix_mc",
        "preamble": ("The nurse has reviewed the Diagnostic Results. The client is diagnosed with <i>Pneumocystis</i> "
                     "pneumonia (PCP)."),
        "stem": ("For each potential order, click to specify if the order is anticipated or not anticipated in the plan "
                 "of care."),
        "matrix": matrix("Potential Order", ["Anticipated", "Not Anticipated"], [
            ("Titrate oxygen to keep pulse oximetry reading above 95%", 0), ("Administer ibuprofen as needed for fever", 0),
            ("Administer trimethoprim/sulfamethoxazole", 0), ("Administer vancomycin", 1),
            ("Gargle with lidocaine solution", 1), ("Schedule a stress test in the morning", 1),
            ("Refer to social work", 0)]),
        "explanation": (
            "Clinical manifestations of <i>Pneumocystis</i> pneumonia include fever, chills, and flu-like symptoms. Oxygen "
            "supports the respiratory compromise, and an antipyretic reduces the fever. Trimethoprim/sulfamethoxazole is "
            "effective against PCP. A social work consult is needed because the client is out of work, without insurance, "
            "and facing a long-term illness.<br>Vancomycin is not effective against <i>Pneumocystis</i>, a fungus. PCP "
            "does not cause a sore throat, so lidocaine gargles are not indicated, and the client has no history of "
            "cardiovascular illness, so a stress test is not indicated."),
    }),
    (INTRO, tabs(5), {
        "type": "select_all",
        "preamble": "The nurse teaches the client how to reduce the risk of opportunistic infections.",
        "stem": "What should the nurse teach the client about preventing opportunistic infections? <b>Select all that "
                "apply.</b>",
        "options": opts(("Get an HIV test every 4 months.", 0), ("Wash your hands frequently.", 1),
                        ("Get tested for tuberculosis.", 1), ("Get tested for sexually transmitted infections.", 1),
                        ("Get a yearly influenza vaccine.", 1), ("Do not drink untreated water.", 1),
                        ("Have a complete blood count every month.", 0),
                        ("Have viral load testing every 4 to 6 months.", 1),
                        ("Take antiretroviral medications as prescribed.", 1)),
        "explanation": (
            "Hand washing is a major strategy to prevent infection, and untreated water carries waterborne diseases. "
            "Clients with HIV should be tested routinely for tuberculosis and sexually transmitted infections, and a "
            "yearly influenza vaccine is recommended for immunocompromised clients. Regular viral load testing shows how "
            "well the treatment is controlling the virus, and a daily antiretroviral regimen preserves immune function and "
            "reduces complications.<br>Repeat HIV tests are not needed once the diagnosis is made, and a monthly CBC is "
            "not needed."),
    }),
    (INTRO, tabs(6), {
        "type": "matrix_mc",
        "preamble": ("The nurse assesses the client&rsquo;s understanding of the teaching on reducing the risk of "
                     "opportunistic infections."),
        "stem": ("For each client statement, click to specify if the statement indicates understanding or no "
                 "understanding of the teaching provided."),
        "matrix": matrix("Client Statement", ["Understanding", "No Understanding"], [
            ("“My low CD4 count shows I am at higher risk for infection.”", 0),
            ("“I should avoid crowds when possible.”", 0),
            ("“It is a good practice to keep hand sanitizer in my car and my pocket.”", 0),
            ("“I can stop wearing a mask when I feel better.”", 1),
            ("“Washing my hands frequently is one of the best ways to prevent infection.”", 0),
            ("“I need to keep using safe sex practices.”", 0),
            ("“I will schedule an HIV test every 6 months.”", 1),
            ("“I will stay current with my vaccinations.”", 0),
            ("“Eating a balanced diet and maintaining good nutrition will help improve my immune system.”", 0),
            ("“Not taking a full course of antibiotics could put me at risk for future drug-resistant infections.”", 0)]),
        "explanation": (
            "The statements showing understanding reflect behaviors that control infection and maintain health with HIV: "
            "recognizing the meaning of a low CD4 count, avoiding crowds, hand hygiene, safe sex, staying current with "
            "vaccinations, good nutrition, and completing the full course of antibiotics.<br>Protective measures such as "
            "wearing a mask in crowded settings continue while the CD4 count is low, even when the client feels better. "
            "Repeat HIV tests are not needed once HIV has been diagnosed."),
    }),
]

case = make_case(N, "", "", screens, FN)
case["description"] = ("Maryland Next Gen NCLEX Test Bank Project, September 1, 2022; Author: Denyce Watties-Daniels, "
                       "Coppin State University. HIV with an opportunistic infection: a 25-year-old client who stopped "
                       "antiretroviral therapy develops Pneumocystis pneumonia; priorities, orders, and prevention teaching.")

T_FLOW = vitals(["Day 1 1100", "Day 1 1500", "Day 2 0800"], [
    ("T", "38.3&deg;C (101.0&deg;F)", "37.2&deg;C (99.0&deg;F)", "37.1&deg;C (98.8&deg;F)"), ("P", "102", "98", "88"),
    ("RR", "28", "24", "22"), ("BP", "138/86", "138/86", "134/80"),
    ("Pulse oximetry reading", "90% on room air", "93% on 2 L/min NC", "98% on 3 L/min NC"), ("Pain", "4/10", "2/10", "0/10")])
T_NOTES = (note("Day 1 1100", (
    "A 25-year-old male client who has been HIV positive for 3 years is admitted with a dry cough and fever. Client has "
    "fatigue, shortness of breath, and tachypnea. Breathing is slightly labored, with a tight feeling in the chest on "
    "deep inspiration. Has been on antiretroviral medications since the diagnosis of HIV but recently stopped taking them "
    "after being laid off from his job. Symptoms not improving with over-the-counter medications for 3 days. Oxygen and "
    "antibiotics started."))
    + note("Day 1 1500", ("Client resting in bed, sleeping at intervals. Frequent dry cough. Skin warm and dry. 0.9% "
                          "sodium chloride IV infusing in the right arm at 75 mL/hr."))
    + note("Day 2 0800", ("Client is afebrile. Lungs slightly congested. No shortness of breath. 0.9% sodium chloride "
                          "infusing in the right arm at 75 mL/hr. Skin warm and dry. Coughing less frequently.")))
trend = make_standalone(N, 1, "Trend", ("Stand-alone trend for University of Maryland - CS14 (HIV with Pneumocystis "
                                        "pneumonia): response to treatment by day 2."),
                        INTRO,
                        [{"id": f"nn_umd{S}t", "title": "Nurses' Notes", "content": T_NOTES},
                         {"id": f"flow_umd{S}t", "title": "Flow Sheet", "content": T_FLOW}],
                        {"type": "matrix_mc",
                         "preamble": "The nurse reassesses the client on day 2.",
                         "stem": ("For each client finding, click to indicate if the finding reflects that the "
                                  "client&rsquo;s condition has improved or is unchanged."),
                         "matrix": matrix("Finding", ["Improved", "Unchanged"], [
                             ("Temperature", 0), ("Cough", 0), ("Pulse", 0), ("Dyspnea", 0), ("Blood pressure", 1),
                             ("Pulse oximetry reading", 0), ("Pain", 0)]),
                         "explanation": (
                             "On admission, the client&rsquo;s temperature, pulse, and respirations were elevated and the "
                             "pulse oximetry reading was low. On day 2, the temperature, pulse, and pulse oximetry reading "
                             "are within normal limits, the respiratory rate is lower, the cough has decreased, the client "
                             "is no longer short of breath, and the pain has resolved.<br>The blood pressure has been "
                             "consistently within normal limits.")}, FN_T)

NOTES = [
    "Screen 4 keys \"Administer ibuprofen as needed for fever\" as anticipated; the client's creatinine is elevated "
    "(1.5 mg/dL = 133 µmol/L), where NSAIDs are usually avoided (acetaminophen preferred). Consider changing the order "
    "to acetaminophen.",
    "PCP with hypoxemia (SpO2 90% on room air): adjunctive corticosteroids are usually given with TMP-SMX when PaO2 < 70 "
    "mm Hg. Not part of any question; consider adding to the orders/rationale.",
    "Screen 1: sodium 148 mmol/L (above range) is not keyed as concerning. Consider keying it or changing the value.",
    "Screen 6 keys \"I can stop wearing a mask when I feel better\" as no understanding; masks are not a standard "
    "precaution for PCP itself. The rationale now frames it as protection while the CD4 count is low; please confirm.",
    "Screen 6: the source rationale was generic; it now explains each statement.",
    "Source rationale said the normal CD4 count is 800-1200 cells/mm3 while the lab report range is 500-1600; the "
    "rationale no longer quotes a range.",
    "Labs in SI with the author's ranges: BUN 22 mg/dL → urea 7.9 mmol/L; creatinine 1.5 mg/dL → 133 µmol/L; Hct 0.48 "
    "L/L; Hgb 150 g/L; WBC 15.2 × 10⁹/L (source \"15.2 mm3\"); platelets 300 × 10⁹/L; CD4 kept in cells/µL (as MCC "
    "prints it).",
    "Screen 5 options were reordered so a correct answer is not listed first.",
]

write([case, trend], N, "HIV with an Opportunistic Infection", "HIV-with-Opportunistic-Infection.docx", NOTES)
