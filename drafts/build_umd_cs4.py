"""University of Maryland - CS4: Breast cancer (lymphedema after mastectomy), with its stand-alone trend.
Source: "Breast Cancer DOCX" (medical-surgical); Kimberly Allen, DNP, RN, CNE; Stephanie Howard, MS, CRNP, FNP-C;
Lisa Seldomridge, PhD, RN, CNE; Salisbury University; May 14, 2023. See drafts/umd_common.py.
Usage: python3 drafts/build_umd_cs4.py
"""
from umd_common import *  # noqa: F401,F403

N = 4
FN = footnote("Breast Cancer", "Kimberly Allen, DNP, RN, CNE; Stephanie Howard, MS, CRNP, FNP-C; Lisa Seldomridge, "
              "PhD, RN, CNE; Salisbury University", "May 14, 2023")
FN_T = footnote("Breast Cancer", "Kimberly Allen, DNP, RN, CNE; Stephanie Howard, MS, CRNP, FNP-C; Lisa Seldomridge, "
                "PhD, RN, CNE; Salisbury University", "May 14, 2023", "medical-surgical faculty case study, stand-alone trend",
                si=False)
S = f"{N:02d}"

N1000 = note("1000", (
    "Presents with R arm weakness, numbness, tingling, and swelling for the past 48 hours. Significant history includes "
    "a right-sided radical mastectomy and removal of multiple axillary lymph nodes 45 days ago for triple-negative "
    "breast cancer. Client finished her first of six cycles of chemotherapy 10 days ago. L-side single-lumen "
    "implantable port present. Reports, &ldquo;My R arm aches and feels tight. I am really worried about what&rsquo;s "
    "wrong.&rdquo; Spouse at bedside. Right upper extremity Doppler ultrasound pending."))
N1100 = note("1100", "Doppler ultrasound shows no evidence of clots.")
N1130_A = ("Client states, &ldquo;I&rsquo;m so glad that I don&rsquo;t have a blood clot, but my arm still hurts a lot "
           "and I still don&rsquo;t know what is wrong.&rdquo; Orders received for PO amoxicillin and acetaminophen, "
           "sequential pneumatic compression, and physical therapy.")
N1130 = note("1130", N1130_A)
N1130_6 = note("1130", N1130_A + " PO acetaminophen and amoxicillin given with 240 mL fluids. R arm elevated.")
N1400 = note("1400", (
    "Orders received for discharge home. Prescriptions include amoxicillin 500 mg PO twice daily for 10 days; "
    "acetaminophen 500 mg PO twice daily. Consult outpatient physical therapy and home health nursing for sequential "
    "pneumatic compression device. Client states, &ldquo;I am very concerned about how my arm got like this. I am "
    "afraid I won&rsquo;t be able to manage at home.&rdquo;"))

HP = table(None, [
    ["<b>General</b>", "Alert and oriented, anxious; no known sick contacts"],
    ["<b>Cardiac</b>", "HR regular; ECG shows sinus tachycardia"],
    ["<b>Respiratory</b>", "Breath sounds clear, no cough or dyspnea; chest X-ray clear"],
    ["<b>Gastrointestinal</b>", "Poor appetite for 9 days; abdomen soft, nondistended"],
    ["<b>Skin</b>", "Warm and dry; noticeable swelling of right arm and hand; mastectomy incision healed without drainage"],
])

VS_ROWS = [
    ("T", "98&deg;F (36.6&deg;C)", "98&deg;F (36.6&deg;C)", "98.2&deg;F (36.7&deg;C)"),
    ("P", "104", "98", "86"),
    ("RR", "22", "22", "20"),
    ("BP", "136/74", "132/72", "128/70"),
    ("Pulse oximetry reading", "97% on room air", "97% on room air", "96% on room air"),
    ("Pain", "5/10", "5/10", "3/10"),
    ("R upper arm circumference", "39 cm", "39 cm", "39 cm"),
    ("L upper arm circumference", "37 cm", "37 cm", "37 cm"),
]


def vs(cols):
    times = ["1000", "1200", "1400"][:cols]
    return vitals(times, [r[:cols + 1] for r in VS_ROWS])


LABS = table(["Laboratory Test and Reference Range", "1000"], [
    [lab("Glucose, fasting", "&lt; 5.5 mmol/L"), "3.8 mmol/L"],
    [lab("Hematocrit (Hct)", "Male: 0.42&ndash;0.52 L/L; Female: 0.35&ndash;0.47 L/L"), "0.33 L/L"],
    [lab("Hemoglobin (Hgb)", "Male: 130&ndash;180 g/L; Female: 120&ndash;160 g/L"), "110 g/L"],
    [lab("White blood cell (WBC) count", "4.5&ndash;10.5" + G9), "1.5" + G9],
    [lab("Platelet count", "140&ndash;450" + G9), "100" + G9],
    [lab("Potassium", "3.5&ndash;5.0 mmol/L"), "5.1 mmol/L"],
    [lab("Sodium", "135&ndash;145 mmol/L"), "148 mmol/L"],
    [lab("Albumin", "35&ndash;55 g/L"), "28 g/L"],
])


def tabs(step):
    notes = N1000 + (N1100 if step >= 3 else "") + (N1130 if step == 5 else "") + (N1130_6 + N1400 if step >= 6 else "")
    return [
        {"id": f"nn_umd{S}", "title": "Admission Notes", "content": notes},
        {"id": f"hp_umd{S}", "title": "History and Physical", "content": HP},
        {"id": f"vs_umd{S}", "title": "Vital Signs", "content": vs(3 if step >= 6 else 1)},
        {"id": f"labs_umd{S}", "title": "Laboratory Results", "content": LABS},
    ]


INTRO = ("The nurse cares for a 48-year-old female client who presents to the oncology clinic with complications "
         "following a mastectomy.")

screens = [
    (INTRO, tabs(1), {
        "type": "select_n", "limit": 4,
        "stem": "Select the <b>4</b> assessment findings that are <b>most</b> significant.",
        "options": opts(("Temperature 98°F (36.6°C)", 0), ("HR 104", 0), ("BP 136/74", 0),
                        ("R arm numbness and tingling", 1), ("R arm pain rated 5/10", 1), ("WBC 1.5 × 10⁹/L", 1),
                        ("Glucose 3.8 mmol/L", 0), ("Poor appetite", 0), ("R arm swelling", 1)),
        "explanation": (
            "Assessing for potential cellulitis in a pancytopenic client, for DVT in a postoperative client, and for "
            "lymphedema given the axillary node removal are important competing hypotheses. The R arm swelling, "
            "numbness and tingling, and pain rated 5/10 are associated with lymphedema, cellulitis, and DVT, and the "
            "WBC of 1.5 × 10⁹/L places the client at high risk for infection.<br>With cellulitis, redness of the skin "
            "of the R arm and an elevated temperature would also be likely. With DVT, the R arm would be red or purple "
            "and warm, and the pain would likely be described as cramping and sore.<br>The elevated heart rate and "
            "blood pressure may be associated with anxiety. Fatigue is a common, non-life-threatening condition after "
            "chemotherapy with poor appetite and nutrition. The temperature is within normal limits (it would be "
            "expected to be elevated with infection). A glucose of 3.8 mmol/L is minimally low."),
    }),
    (INTRO, tabs(2), {
        "type": "matrix_mr",
        "stem": ("For each finding, click to indicate if the finding is consistent with cellulitis, lymphedema, or deep "
                 "vein thrombosis (DVT). Each finding may support more than one condition."),
        "matrix": matrix_mr("Finding", ["Cellulitis", "Lymphedema", "DVT"], [
            ("Right arm swelling", [0, 1, 2]), ("Right arm numbness/tingling", [1, 2]),
            ("Temperature 98°F (36.6°C)", [1, 2]), ("HR 104", [0]), ("Sodium 148 mmol/L", [1]),
            ("Albumin 28 g/L", [1])]),
        "explanation": (
            "R arm swelling can be associated with cellulitis, lymphedema, and DVT. R arm numbness and tingling can "
            "occur with postoperative lymphedema and with DVT. A temperature within the normal range could be seen "
            "with lymphedema and DVT, while an elevated temperature would be expected with cellulitis.<br>"
            "Tachycardia is not usually associated with lymphedema but can accompany the inflammatory response of "
            "cellulitis. Hypernatremia is not usually associated with cellulitis or DVT but could contribute to the "
            "swelling seen in lymphedema, and a low albumin level (reduced oncotic pressure) can also contribute to "
            "lymphedema; it is not usually a factor in DVT or cellulitis."),
    }),
    (INTRO, tabs(3), {
        "type": "drag_drop_cloze",
        "preamble": ("The nurse has reviewed the Admission Notes from 1100. The nurse reviews and documents the results "
                     "of the Doppler ultrasound."),
        "stem": "Drag 1 condition and 1 cause to fill in the blanks of the following sentence.",
        "cloze": dict(cloze("The greatest risk for this client is developing [[drop0]] due to [[drop1]].",
                            [("Sepsis", 0), ("Pulmonary embolism", 0), ("Chronic lymphedema", 1), ("Malnutrition", 0)],
                            [("Deep vein thrombosis and cancer diagnosis", 0), ("Cellulitis with pancytopenia", 0),
                             ("Post-op R radical mastectomy and axillary node dissection", 1),
                             ("Poor intake and effects of chemotherapy", 0)]),
                      scoreGroups=[[0, 1]]),
        "explanation": (
            "This client is displaying signs of lymphedema in the R arm, including swelling, numbness, tingling, and "
            "pain rated 5/10. Because these symptoms are occurring early in the postoperative recovery, treatment is "
            "aimed at reducing the swelling and pain and preventing complications such as chronic lymphedema.<br>The "
            "risk for pulmonary embolism would be associated with a DVT; while the client has R arm swelling and pain, "
            "the Doppler ultrasound does not show a clot. The fatigue, loss of appetite, and anemia can be associated "
            "with the recent chemotherapy and resulting pancytopenia. The low albumin level suggests malnutrition; "
            "nutritional support is indicated, but the priority at this time is managing the lymphedema."),
    }),
    (INTRO, tabs(4), {
        "type": "select_all",
        "preamble": "The nurse suspects that the client has lymphedema.",
        "stem": "What orders does the nurse anticipate including in the plan of care? <b>Select all that apply.</b>",
        "options": opts(("Anticoagulants SC", 0), ("Acetaminophen PO", 1), ("Diet as tolerated", 1),
                        ("Ibuprofen PO", 0), ("Sequential pneumatic compression", 1), ("Amoxicillin PO", 1),
                        ("Physical therapy", 1)),
        "explanation": (
            "Mild pain should be treated with acetaminophen; ibuprofen should be avoided when platelets are low. "
            "Supporting the client&rsquo;s nutritional status is important, and the client can have a diet as "
            "tolerated. Oral antibiotics such as amoxicillin are indicated to treat a possible infection that may have "
            "triggered the lymphedema. Sequential pneumatic compression helps mobilize lymphatic fluid from the hand and "
            "lower arm, and physical therapists can teach techniques and exercises to reduce lymphedema swelling.<br>"
            "Anticoagulants are not indicated because the Doppler ultrasound showed no clot."),
    }),
    (INTRO, tabs(5), {
        "type": "matrix_mc",
        "preamble": ("The nurse has reviewed the Admission Notes from 1130. Based on the additional notes, the nurse "
                     "begins to implement the treatment plan."),
        "stem": ("For each potential nursing action, click to specify whether the action is appropriate or not "
                 "appropriate to include in the plan of care."),
        "matrix": matrix("Potential Intervention", ["Appropriate", "Not Appropriate"], [
            ("Measure circumference of R wrist, forearm, and upper arm", 0),
            ("If needed, collect fingerstick blood glucose from R index finger", 1),
            ("Take blood pressure in L arm", 0), ("Teach client manual lymphatic drainage techniques", 1),
            ("Elevate R arm on two pillows", 0), ("Apply warm compresses to R arm", 1), ("Encourage oral fluids", 0)]),
        "explanation": (
            "When implementing the treatment plan, the nurse uses measures to reduce the risk of complications from "
            "lymphedema, including protecting the hand and arm from trauma: whenever possible, the R hand or arm is not "
            "used for blood pressures, venipuncture, fingersticks, or IV cannulation. Pillows keep the arm elevated to "
            "reduce swelling. Measuring the circumference of the R wrist, forearm, and upper arm documents the progress "
            "of the lymphedema. The client has no dietary restrictions, so the nurse can encourage fluids and food as "
            "tolerated to improve nutrition.<br>Warm compresses are avoided on the R arm because the swelling might "
            "dull pain perception and a burn could occur. Manual lymphatic drainage is provided by specially trained "
            "therapists and should be avoided if the client has a skin infection or a suspected blood clot."),
    }),
    (INTRO, tabs(6), {
        "type": "matrix_mc",
        "preamble": ("The nurse has reviewed the Admission Notes from 1400 and the Vital Signs from 1200 and 1400. The "
                     "nurse begins discharge teaching."),
        "stem": ("For each client statement, click to specify whether the statement indicates an understanding or no "
                 "understanding of the teaching provided."),
        "matrix": matrix("Client Statement", ["Understanding", "No Understanding"], [
            ("“If my arm hurts, I’ll use an ice bag on it.”", 1),
            ("“It’s good to use a gentle moisturizer on my arms every day.”", 0),
            ("“I will wear gloves when I work in the garden.”", 0),
            ("“If I get a cut on my right hand, I will start taking antibiotics immediately.”", 1),
            ("“Losing weight might help the swelling.”", 0),
            ("“Some aching and heaviness in my right arm is expected.”", 1),
            ("“I can resume all upper body exercises as soon as I want.”", 1),
            ("“I will try to wear bracelets on my left arm only.”", 0)]),
        "explanation": (
            "Teaching focuses on protecting the affected hand and arm from trauma and on promoting lymphatic drainage. "
            "A gentle moisturizer reduces dryness and the risk of cracking and helps restore the skin&rsquo;s natural "
            "oils. Gloves protect the hand while gardening. Clothing and jewelry that might constrict lymphatic drainage "
            "on the R side are avoided, so bracelets are worn on the left. Being overweight or obese is a risk factor "
            "for lymphedema, so weight loss can help.<br>Extremes of temperature (ice or heat) are avoided on the "
            "affected arm, because the swelling may dull sensation. A cut on the R hand is cleaned and reported to the "
            "provider rather than self-treated with antibiotics. Aching and heaviness in the arm are signs of worsening "
            "lymphedema to report, not expected findings. Upper body exercises are resumed gradually, as taught by "
            "physical therapy."),
    }),
]

case = make_case(N, "Breast cancer (lymphedema after mastectomy)", None, screens, FN)
case["description"] = ("Maryland Next Gen NCLEX Test Bank Project, May 14, 2023; Authors: Kimberly Allen, Stephanie "
                       "Howard, Lisa Seldomridge, Salisbury University. Breast cancer: a client with pancytopenia after "
                       "chemotherapy presents with right-arm lymphedema after a radical mastectomy; cellulitis and DVT "
                       "are ruled out, and the nurse plans care and discharge teaching.")

# ---- Stand-alone trend (flow sheet; its own data, a different question from screen 6) ----
T_NOTES = N1000 + N1100 + N1130_6 + note("1400", (
    "Orders received for discharge home. Prescriptions reviewed and consult ordered for outpatient physical therapy "
    "and home health nursing for sequential pneumatic compression device. Client states, &ldquo;I am very concerned "
    "about how my arm got like this. I am afraid I won&rsquo;t be able to manage at home.&rdquo;"))
T_FLOW = vitals(["1000", "1200", "1400"], [
    ("T", "98&deg;F (36.6&deg;C)", "98&deg;F (36.6&deg;C)", "98.2&deg;F (36.7&deg;C)"), ("P", "104", "98", "86"),
    ("RR", "22", "22", "20"), ("BP", "136/74", "126/72", "128/70"),
    ("Pulse oximetry reading", "97% on room air", "97% on room air", "96% on room air"), ("Pain", "5/10", "5/10", "3/10"),
    ("R upper arm circumference", "39 cm", "39 cm", "39 cm"), ("L upper arm circumference", "37 cm", "37 cm", "37 cm")])
trend = make_standalone(N, 1, "Trend", (
    "Stand-alone trend for University of Maryland - CS4 (breast cancer, lymphedema): changes over the 4-hour clinic "
    "visit."),
    "The nurse cares for a 48-year-old female client in the oncology clinic who is being evaluated for complications "
    "following a mastectomy.",
    [{"id": f"nn_umd{S}t", "title": "Nurses' Notes", "content": T_NOTES},
     {"id": f"hp_umd{S}t", "title": "History and Physical", "content": HP},
     {"id": f"flow_umd{S}t", "title": "Flow Sheet", "content": T_FLOW}],
    {"type": "matrix_mc",
     "stem": ("For each finding, click to specify if the finding indicates that the client&rsquo;s status has improved, "
              "declined, or is unchanged since admission to the clinic."),
     "matrix": matrix("Finding", ["Improved", "Declined", "Unchanged"], [
         ("Temperature", 2), ("Pain", 0), ("HR", 0), ("RR", 0), ("R upper arm circumference", 2), ("Anxiety", 1)]),
     "explanation": ("The vital signs have stabilized since admission (HR 104 to 86, RR 22 to 20), and the pain has "
                     "improved slightly (5/10 to 3/10). The temperature and the swelling of the arm (circumference) "
                     "have not changed.<br>The client&rsquo;s anxiety has increased: the client is now worried about "
                     "what caused the arm swelling, numbness, tingling, and pain and is afraid of not being able to "
                     "manage at home.")}, FN_T)

NOTES = [
    "Screen 2 (matrix, more than one answer per row): the author's key marks numbness/tingling for lymphedema AND DVT, "
    "and HR 104 for cellulitis only, but the author's rationale said numbness is \"only associated with lymphedema\" "
    "and that tachycardia \"could be associated with DVT\". The key was kept; the rationale was rewritten to match it. "
    "Please confirm the key.",
    "Screen 2: \"Sodium 148 mmol/L\" keyed as consistent with lymphedema (rationale: hypernatremia could add to the "
    "swelling) is a weak link. Consider replacing that row.",
    "Screen 4: amoxicillin is keyed as an anticipated order \"to treat a possible infection that triggered the "
    "lymphedema\", although the client is afebrile with no redness (cellulitis not suspected). The client is also "
    "neutropenic (WBC 1.5 × 10⁹/L). Please confirm the antibiotic order and rationale.",
    "Discharge prescriptions (1400 note): acetaminophen 500 mg PO twice daily is an unusual frequency for pain "
    "(usually every 4-6 hours as needed). Please review.",
    "Screen 6: the source's rationale repeated screen 5; it was rewritten for the statements actually asked (ice bag, "
    "antibiotics for a cut, aching and heaviness, resuming exercises). \"Ice bag = no understanding\" follows the "
    "usual advice to avoid temperature extremes on the affected arm; please confirm.",
    "Screen 1: WBC 1.5 × 10⁹/L is keyed as one of the 4 most significant findings (not explained in the source "
    "rationale; a sentence was added).",
    "Lab values converted to SI with the author's ranges: glucose 68 mg/dL → 3.8 mmol/L (< 5.5); Hgb 11 g/dL → "
    "110 g/L; Hct 33% → 0.33 L/L; albumin 2.8 g/dL → 28 g/L (35-55); WBC/platelets × 10⁹/L; K+/Na+ mmol/L.",
    "Screen 3: \"drag 1 condition and 1 cause\" is a drag-and-drop with both blanks scored together (1 point, "
    "\"rationale rule\" in the source).",
    "Screen 4 options were reordered so a correct answer is not listed first.",
    "Trend (stand-alone): uses the source's own flow sheet, where the 1200 BP is 126/72 (screen 6 of the case shows "
    "132/72, as in the source). No question depends on it.",
]

write([case, trend], N, "Breast Cancer", "Breast-Cancer.docx", NOTES)
