"""University of Maryland - CS20: Tension Pneumothorax (chest trauma after a motor vehicle collision), with its stand-alone
bow-tie. Source: "Tension Pneumothorax DOCX" (medical-surgical); Denyce Watties-Daniels, DNP, RN, Coppin State University;
September 1, 2022.
Usage: python3 drafts/build_umd_cs20.py
"""
from umd_common import *  # noqa: F401,F403

N = 20
S = f"{N:02d}"
AUTH = "Denyce Watties-Daniels, DNP, RN, Coppin State University"
FN = footnote("Tension Pneumothorax", AUTH)
FN_B = footnote("Tension Pneumothorax", AUTH, kind="medical-surgical faculty case study, stand-alone bow-tie")

N1500 = note("1500", (
    "Lethargic but easy to arouse. Has chest pain and difficulty breathing; chest pain increases to 5/10 with inspiration. "
    "Absent breath sounds on the anterior and posterior left lower chest wall. Asymmetrical chest movement, less on the "
    "left side. Cyanosis of the lips and fingertips. Bruising on the anterior chest from the seat belt. IV of 0.9% sodium "
    "chloride started at 100 mL/hr in the left arm. Oxygen started at 4 L/min per nasal cannula."))
N1530 = note("1530", (
    "Increasing shortness of breath and labored breathing; tachycardic, with a dropping blood pressure. Muffled heart "
    "sounds. Client stuporous. Tracheal deviation noted."))
N1545 = note("1545", (
    "Chest X-ray obtained. Medicated with morphine. The provider used a 14-gauge needle to decompress the chest and "
    "inserted a 28 Fr chest tube in the left lower chest wall. Chest tube connected to water seal drainage with 20 cm "
    "H<sub>2</sub>O wall suction. Fluctuations noted in the water seal chamber. 20 mL of light red drainage collected in "
    "the drainage chamber. Crackles heard in the right lung fields. Diminished breath sounds on the left."))
N1600 = note("1600", (
    "Resting in bed. Chest tube draining a small amount of light red drainage in the collection chamber. Symmetrical chest "
    "movement noted. Lips and fingertips are pink."))

TIMES = ["1500", "1530", "1545", "1600"]
VS_ROWS = [
    ("T", "36.8&deg;C (98.4&deg;F)", "36.6&deg;C (98.0&deg;F)", "36.6&deg;C (98.0&deg;F)", "36.6&deg;C (98.0&deg;F)"),
    ("P", "98", "112", "80", "72"),
    ("RR", "28", "36", "22", "20"),
    ("BP", "138/90", "98/60", "128/70", "124/74"),
    ("Pulse Oximetry Reading (SpO<sub>2</sub>)", "89% on 4 L/min nasal cannula", "80% on 4 L/min nasal cannula",
     "95% on 4 L/min nasal cannula", "98% on room air"),
    ("Pain", "5/10", "10/10", "5/10", "5/10")]


def vs(cols):
    return vitals(TIMES[:cols], [r[:cols + 1] for r in VS_ROWS])


ABG = table(["Laboratory Test and Reference Range", "1530"], [
    [lab("Arterial pH", "7.35&ndash;7.45"), "7.25"],
    [lab("PaO<sub>2</sub>", "75&ndash;100 mm Hg"), "50 mm Hg"],
    [lab("PaCO<sub>2</sub>", "35&ndash;45 mm Hg"), "80 mm Hg"],
    [lab("SaO<sub>2</sub>", "95&ndash;100%"), "84%"],
    [lab("HCO<sub>3</sub><sup>&minus;</sup>", "22&ndash;26 mmol/L"), "27 mmol/L"]])
DIAG = paras("<b>Chest X-ray (1545):</b> fractures of the left 6th and 7th ribs; large left tension pneumothorax.")


def tabs(step):
    cols = {1: 1, 2: 2, 3: 2, 4: 2, 5: 3, 6: 4}[step]
    notes = N1500 + (N1530 if step >= 2 else "") + (N1545 if step >= 5 else "") + (N1600 if step >= 6 else "")
    t = [{"id": f"nn_umd{S}", "title": "Nurses' Notes", "content": notes},
         {"id": f"vs_umd{S}", "title": "Vital Signs", "content": vs(cols)}]
    if step >= 2:
        t.append({"id": f"labs_umd{S}", "title": "Laboratory Results", "content": ABG})
    if step >= 5:
        t.append({"id": f"dx_umd{S}", "title": "Diagnostic Results", "content": DIAG})
    return t


INTRO = "A 58-year-old woman in a severe motor vehicle collision was admitted to the ICU with fractured ribs."

screens = [
    (INTRO, tabs(1), {
        "type": "select_all",
        "stem": "Which assessment findings require <b>immediate</b> follow-up? <b>Select all that apply.</b>",
        "options": opts(("Heart rate of 98/min", 0), ("Respiratory rate of 28/min", 1), ("SpO₂ of 89%", 1),
                        ("Blood pressure of 138/90", 0), ("Pain 5/10 with inspiration", 1),
                        ("Temperature of 36.8°C (98.4°F)", 0), ("Absent breath sounds", 1),
                        ("Bruising on the anterior chest", 0), ("Cyanosis of the lips and fingertips", 1)),
        "explanation": (
            "The nurse assesses the client&rsquo;s airway, breathing, and circulation. The respiratory rate is high and the "
            "SpO<sub>2</sub> is low despite oxygen. Absent breath sounds and cyanosis indicate respiratory compromise and "
            "require immediate intervention. Pain that increases with inspiration requires further assessment and "
            "intervention.<br>The heart rate, blood pressure, and temperature are within normal limits, and the bruising "
            "from the seat belt is expected after the collision."),
    }),
    (INTRO, tabs(2), {
        "type": "matrix_mr",
        "preamble": ("The nurse has reviewed the Nurses&rsquo; Notes from 1530, the Vital Signs, and the Laboratory "
                     "Results. The nurse reassesses the client."),
        "stem": ("For each client finding, click to specify if the finding is consistent with pulmonary contusion, cardiac "
                 "tamponade, or tension pneumothorax. Each finding may be consistent with more than 1 condition. Each "
                 "column must have at least 1 response option selected."),
        "matrix": matrix_mr("Client Finding", ["Pulmonary Contusion", "Cardiac Tamponade", "Tension Pneumothorax"], [
            ("Absent breath sounds", [2]), ("Asymmetrical chest movement", [2]),
            ("Respiratory acidosis with hypoxemia", [0, 2]), ("Hypotension", [0, 1, 2]),
            ("History of chest trauma", [0, 1, 2]), ("Muffled heart sounds", [1, 2]), ("Chest pain", [0, 1, 2]),
            ("Tracheal deviation", [2])]),
        "explanation": (
            "Pulmonary contusion, cardiac tamponade, and pneumothorax may all result from severe chest trauma and may "
            "present with labored breathing and chest pain. All can cause tachycardia and hypotension, by different "
            "mechanisms: a pulmonary contusion is associated with bleeding that can lead to shock, while a tension "
            "pneumothorax and cardiac tamponade decrease cardiac output. Respiratory acidosis with hypoxemia is seen with "
            "pulmonary contusion and pneumothorax, but not with cardiac tamponade. Muffled heart sounds occur with cardiac "
            "tamponade and may occur with a tension pneumothorax. Asymmetrical chest movement, absent breath sounds, and "
            "tracheal deviation are signs of a tension pneumothorax."),
    }),
    (INTRO, tabs(3), {
        "type": "dyad",
        "stem": "Complete the following sentence by choosing from the lists of options.",
        "cloze": dict(cloze("The client is most likely experiencing a [[drop0]], as most evidenced by the [[drop1]].",
                            [("cardiac tamponade", 0), ("pulmonary contusion", 0), ("tension pneumothorax", 1)],
                            [("laboratory report", 0), ("respiratory assessment", 1), ("cardiovascular assessment", 0)]),
                      scoreGroups=[[0, 1]]),
        "explanation": (
            "The client is most likely experiencing a tension pneumothorax, as most evidenced by the respiratory "
            "assessment: increasing shortness of breath, hypoxemia, absent breath sounds on the left, and tracheal "
            "deviation."),
    }),
    (INTRO, tabs(4), {
        "type": "select_all",
        "preamble": "The nurse notifies the provider of the client&rsquo;s condition.",
        "stem": "Which of the following prescriptions should the nurse anticipate? <b>Select all that apply.</b>",
        "options": opts(("Insert an indwelling urinary catheter", 0), ("Assist with needle decompression", 1),
                        ("Administer pain medication", 1), ("Obtain a STAT chest X-ray", 1),
                        ("Transfuse a unit of blood", 0), ("Set up a chest drainage system", 1)),
        "explanation": (
            "The client is most likely experiencing a tension pneumothorax. The nurse prepares for immediate needle "
            "decompression to relieve the pressure in the chest. Treatment then includes inserting a chest tube connected "
            "to suction through a chest drainage system to re-expand the lung. A chest X-ray is done before chest tube "
            "placement if time allows; otherwise it is obtained soon after. The nurse administers pain medication before "
            "the provider decompresses the chest and inserts the chest tube.<br>Whether the client needs blood is decided "
            "if shock or evidence of internal bleeding persists after the pneumothorax is evacuated. An indwelling urinary "
            "catheter is not needed to treat the pneumothorax."),
    }),
    (INTRO, tabs(5), {
        "type": "matrix_mc",
        "preamble": ("The nurse has reviewed the Nurses&rsquo; Notes from 1545, the Vital Signs, and the Diagnostic "
                     "Results. The client is diagnosed with a tension pneumothorax, and the provider has placed a chest "
                     "tube."),
        "stem": "For each nursing action, click to specify if the action is indicated or not indicated.",
        "matrix": matrix("Nursing Action", ["Indicated", "Not Indicated"], [
            ("Administer morphine IV as needed", 0), ("Position the drainage system at heart level", 1),
            ("Ambulate in the hallway", 1), ("Monitor fluctuations in the water seal chamber", 0),
            ("Obtain a repeat chest X-ray in the morning", 0), ("Document chest tube drainage every shift", 0),
            ("Change the chest tube dressing every shift", 1)]),
        "explanation": (
            "The nurse administers pain medication before and after chest tube insertion and as needed. The nurse "
            "monitors the water seal chamber for fluctuations (tidaling), which show the system is functioning. Drainage "
            "is recorded as output. A chest X-ray in the morning documents re-expansion of the lung.<br>The drainage "
            "system is kept below the level of the chest to promote drainage. The client is stuporous and should not "
            "ambulate. An occlusive dressing at the insertion site keeps air from leaking around the tube; it is not "
            "changed routinely, to avoid air entering the chest cavity."),
    }),
    (INTRO, tabs(6), {
        "type": "dyad",
        "preamble": "The nurse has reviewed the Nurses&rsquo; Notes from 1600 and the Vital Signs. The nurse reassesses the client.",
        "stem": "Complete the following sentence by choosing from the lists of options.",
        "cloze": cloze("The nurse determines the client’s status is [[drop0]]. The nurse should now [[drop1]].",
                       [("deteriorating", 0), ("improving", 1), ("unchanged", 0)],
                       [("check for air leaks", 0), ("obtain a STAT blood gas", 0), ("monitor breath sounds", 1)]),
        "explanation": (
            "The vital signs, SpO<sub>2</sub> on room air, symmetrical chest movement, and pink lips and fingertips show "
            "the client is improving. The nurse continues to monitor the client, including the breath sounds, for "
            "improved airflow in the affected lung.<br>A blood gas may not be needed if the client continues to improve. "
            "There is no need to check for air leaks, since the system appears to be functioning."),
    }),
]

case = make_case(N, "", "", screens, FN)
case["description"] = ("Maryland Next Gen NCLEX Test Bank Project, September 1, 2022; Author: Denyce Watties-Daniels, "
                       "Coppin State University. Tension pneumothorax: a 58-year-old client with rib fractures after a "
                       "motor vehicle collision; recognizing deterioration, needle decompression and chest tube care.")

bow = make_standalone(N, 1, "Bowtie", "Stand-alone bow-tie for University of Maryland - CS20 (tension pneumothorax).",
                      INTRO, tabs(2),
                      dict({"type": "bowtie",
                            "preamble": "The nurse assesses the client 30 minutes after admission.",
                            "stem": ("Complete the diagram by dragging from the choices below to specify what condition "
                                     "the client is most likely experiencing, 2 actions the nurse should take to address "
                                     "that condition, and 2 parameters the nurse should monitor to assess the "
                                     "client&rsquo;s progress."),
                            "explanation": (
                                "The vital signs, absent breath sounds, and tracheal deviation indicate the client is "
                                "developing a tension pneumothorax. The nurse calls the rapid response team so emergency "
                                "treatment (needle decompression and a chest tube) can be given. A STAT chest X-ray can "
                                "help confirm the diagnosis, but it must not delay decompression.<br>Improved respiratory "
                                "status (breath sounds) and hemodynamic status (blood pressure and pulse) are the best "
                                "indicators that the tension pneumothorax has resolved. Pain may stay elevated because of "
                                "the rib fractures. Blood gases are obtained as needed; if the respiratory status improves, "
                                "another blood gas may not be needed.")},
                           **bowtie([("Administer a diuretic", 0), ("Obtain a STAT chest X-ray", 1),
                                     ("Administer a fluid bolus", 0), ("Call the rapid response team", 1),
                                     ("Prepare for intubation", 0)],
                                    [("Cardiac tamponade", 0), ("Pulmonary contusion", 0), ("Pulmonary embolism", 0),
                                     ("Tension pneumothorax", 1)],
                                    [("Pain level", 0), ("Blood pressure", 1), ("Urine output", 0), ("Breath sounds", 1),
                                     ("Hourly blood gases", 0)])), FN_B)

NOTES = [
    "Screen 4 option \"Assist with thoracentesis\" changed to \"Assist with needle decompression\" (a tension pneumothorax "
    "is relieved by needle decompression/thoracostomy, not thoracentesis, which drains fluid). Rationale and the 1545 note "
    "reworded to match (\"14-gauge spinal needle to aspirate air\" -> \"14-gauge needle to decompress the chest\").",
    "Screen 4 keys \"Obtain a STAT chest X-ray\" as anticipated and the bow-tie keys it as an action. Tension pneumothorax is "
    "a clinical diagnosis and imaging must not delay decompression; the rationales say so. Consider replacing it in the "
    "bow-tie.",
    "Screen 4 keys an indwelling urinary catheter as not anticipated; in a hypotensive, stuporous trauma client in the ICU "
    "one is often placed for output monitoring. Please confirm.",
    "Screen 2 keys \"Muffled heart sounds\" for tension pneumothorax as well as tamponade (classically a tamponade sign, "
    "Beck's triad). The row \"Blood gas\" was renamed \"Respiratory acidosis with hypoxemia\". Please review the grid.",
    "Screen 5 keys \"Document chest tube drainage every shift\" as indicated; after insertion drainage is usually "
    "checked/recorded hourly at first (bleeding). Consider rewording (e.g. \"Measure and record drainage hourly\").",
    "1545 note: \"Rales heard in the right lung fields\" (the uninjured side) is unexplained; kept as \"Crackles in the right "
    "lung fields\". Also: chest tube \"connected to 20 cm wall suction\" now reads 20 cm H2O suction.",
    "SpO2 98% on room air at 1600, 15 minutes after the chest tube: oxygen removed quickly; confirm intended.",
    "ABG labels corrected (P02/PC02/SaP02/HC03 -> PaO2/PaCO2/SaO2/HCO3-); HCO3- 27 mEq/L -> 27 mmol/L; gases stay in mm Hg. "
    "The ABG is charted at 1530 (the source gives no time). Temperatures shown in °C with °F.",
    "Screen 3 uses rationale scoring (1 point only if both blanks are correct), as in the source. Screen 4 options were "
    "reordered so a correct answer is not listed first.",
    "The bow-tie uses the chart at 1530 (as in the source); it overlaps screens 2-4, so it is a separate stand-alone.",
]

write([case, bow], N, "Tension Pneumothorax", "Tension-Pneumothorax.docx", NOTES)
