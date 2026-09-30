"""University of Maryland - CS18: Care of the client after spine surgery (laminectomy), with its stand-alone bow-tie
(surgical site infection).
Source: "Spine Surgery DOCX" (medical-surgical); Mary DiBartolo, PhD, RN-BC, CNE, FAAN, and Allison Hynson, MSN, RN;
January 25, 2023.
Usage: python3 drafts/build_umd_cs18.py
"""
from umd_common import *  # noqa: F401,F403

N = 18
S = f"{N:02d}"
AUTH = "Mary DiBartolo, PhD, RN-BC, CNE, FAAN, and Allison Hynson, MSN, RN"
FN = footnote("Care of Client Post-Op Spine Surgery (Laminectomy)", AUTH, "January 25, 2023")
FN_B = footnote("Care of Client Post-Op Spine Surgery (Laminectomy)", AUTH, "January 25, 2023",
                "medical-surgical faculty case study, stand-alone bow-tie")

ADMIT = ("Admitted to the surgical unit after an L2&ndash;L4 laminectomy with Jackson-Pratt (JP) drain placement. History "
         "of type 2 diabetes and back pain for 10 years that was unrelieved with pharmacologic pain management. JP drain "
         "had 30 mL of output on arrival to the floor and was emptied. Bloodwork sent to the lab after surgery. Alert and "
         "oriented &times; 4; pupils 3 mm bilaterally; denies numbness or tingling in the extremities; 5/5 strength in all "
         "extremities.{PAIN} Urinary catheter removed before arrival to the floor, around 1100; she is due to void. Surgical "
         "dressing clean, dry, and intact.")
D1_1200 = note("Day 1 1200", ADMIT.format(PAIN=" Pain rated 6/10."))
D1_1330 = note("Day 1 1330", "Pain 3/10 after oxycodone administration.")
D1_1600 = note("Day 1 1600", (
    "Neurologic status remains stable. The client reports that her back feels &ldquo;wet.&rdquo; 0 mL of output from the "
    "JP drain; the drain is uncompressed, and the surgical dressing is saturated with dark red blood. She reports bending "
    "over to get her call bell from the floor. Has not voided since the urinary catheter was removed but reports the urge "
    "to go. Reports her last bowel movement was 2 days before surgery."))
D1_1610 = note("Day 1 1610", (
    "JP drain compressed. Provider notified of dressing status and assessed the surgical site; the incision is open in one "
    "area. New dressing applied."))
D2_0900 = note("Day 2 0900", (
    "Alert and oriented &times; 4; no changes in neurologic status. JP drain output 50 mL overnight. Provider removed the "
    "JP drain; the client is to be discharged. Client fitted for a thoracic-lumbar-sacral orthosis (TLSO) back brace."))

VS_ROWS = [("T", "36.7&deg;C (98.2&deg;F)", "36.8&deg;C (98.4&deg;F)", "37.0&deg;C (98.6&deg;F)"), ("P", "77", "70", "65"),
           ("RR", "20", "16", "18"), ("BP", "110/80", "107/70", "116/74"),
           ("Pulse oximetry reading", "94% on 2 L/min NC", "95% on room air", "98% on room air"),
           ("Pain", "6/10", "4/10", "3/10")]


def vs(cols):
    return vitals(["Day 1 1200", "Day 1 1600", "Day 2 0900"][:cols], [r[:cols + 1] for r in VS_ROWS])


def labs(wbc="10.0"):
    rows = [[lab("Glucose, fasting", "&lt; 5.5 mmol/L"), "7.2 mmol/L"],
            [lab("Hematocrit (Hct)", "Female: 0.35&ndash;0.47 L/L"), "0.30 L/L"],
            [lab("Hemoglobin (Hgb)", "Female: 120&ndash;160 g/L"), "110 g/L"],
            [lab("White blood cell (WBC) count", "4.5&ndash;10.5" + G9), wbc + G9],
            [lab("Hemoglobin A1c (HbA1c)", "&lt; 5.7%"), "6.0%"],
            [lab("INR", "1.0"), "1.0"],
            [lab("Platelet count", "140&ndash;450" + G9), "200" + G9]]
    return table(["Laboratory Test and Reference Range", "Day 1"], rows)


def meds(senna, times):
    """times: the doses of the 5-mg order given so far, one column each (earlier columns never change)."""
    given = (times + ["", "", ""])[:3]
    rows = [["Oxycodone", "5 mg PO every 4 hours as needed for moderate pain (4&ndash;6)"] + given,
            ["Oxycodone", "10 mg PO every 4 hours as needed for severe pain (7&ndash;10)", "", "", ""]]
    if senna:
        rows.append(["Senna", "1 tablet PO twice daily", "", "", ""])
    return table(["Medication", "Dose, Route, Frequency", "Given", "Given", "Given"], rows)


def tabs(step):
    notes = D1_1200 + D1_1330 + D1_1600 + (D1_1610 + D2_0900 if step >= 5 else "")
    return [{"id": f"nn_umd{S}", "title": "Nurses' Notes", "content": notes},
            {"id": f"vs_umd{S}", "title": "Vital Signs", "content": vs(3 if step >= 5 else 2)},
            {"id": f"labs_umd{S}", "title": "Laboratory Results", "content": labs()},
            {"id": f"meds_umd{S}", "title": "Medications",
             "content": meds(step >= 4, ["Day 1 1230", "Day 1 1800", "Day 2 0300"] if step >= 5 else ["Day 1 1230"])}]


INTRO = ("The nurse is caring for a 65-year-old female client who is admitted to the surgical unit following an L2&ndash;L4 "
         "laminectomy.")

screens = [
    (INTRO, tabs(1), {
        "type": "select_n", "limit": 4,
        "preamble": ("At 1330, the nurse reassesses the client&rsquo;s pain after oxycodone administration. At 1600, the "
                     "nurse takes vital signs and performs a neurologic and dressing assessment."),
        "stem": "Select the <b>4</b> findings that require <b>immediate</b> follow-up.",
        "options": opts(("Blood pressure", 0), ("Jackson-Pratt drainage", 1), ("Pain rating", 0),
                        ("Status of surgical dressing", 1), ("Respiratory rate", 0), ("Hemoglobin and hematocrit", 0),
                        ("Urinary retention", 0), ("Client report of bending to get call bell", 1),
                        ("Status of Jackson-Pratt drain", 1)),
        "explanation": (
            "The JP drain is collecting no drainage and is uncompressed, so there is no suction to drain blood and fluid "
            "from the wound. The dressing is saturated, which could have been caused by the incision opening when the "
            "client bent over to get her call bell; she should be taught spinal precautions right away (no bending, "
            "lifting, or twisting).<br>The BP and RR are stable. The hemoglobin and hematocrit are below normal, likely "
            "from surgical blood loss, but are not immediately concerning. Pain of 4/10 after surgery is expected. The "
            "client reports the urge to void, so urinary retention is not a concern unless she is unable to urinate."),
    }),
    (INTRO, tabs(2), {
        "type": "select_all",
        "stem": ("Which laboratory value trends would the nurse expect to see with this client&rsquo;s condition? "
                 "<b>Select all that apply.</b>"),
        "options": opts(("Increase in INR", 0), ("Decrease in hemoglobin", 1), ("Decrease in WBC count", 0),
                        ("Decrease in HbA1c", 0), ("Decrease in hematocrit", 1), ("Increase in platelets", 0)),
        "explanation": (
            "The nurse expects the hemoglobin and hematocrit to drop because of blood loss.<br>The WBC count is not "
            "affected by blood loss. The INR is not expected to change, because there is no indication that the client "
            "is on anticoagulant therapy. The HbA1c reflects the average blood glucose over the past 2&ndash;3 months and "
            "is not affected by postoperative blood loss. The platelets are not expected to increase."),
    }),
    (INTRO, tabs(3), {
        "type": "drag_drop_cloze",
        "stem": "Drag the most appropriate choice from the list of options to fill in the blank of the following sentence.",
        "cloze": cloze("The top priority for this client is [[drop0]].",
                       [("pain management", 0), ("neurologic assessment", 0), ("surgical site management", 1),
                        ("urinary status", 0)]),
        "explanation": (
            "The nurse should assess the incision to determine how to control the bleeding.<br>The client is "
            "neurologically stable. She has not voided 5 hours after the urinary catheter was removed but reports the "
            "urge to go. Her pain appears to be managed by the oxycodone given at 1230."),
    }),
    (INTRO, tabs(4), {
        "type": "matrix_mc",
        "preamble": "The nurse has reviewed the Medications.",
        "stem": ("For each potential nursing or collaborative intervention, click to specify whether the intervention is "
                 "appropriate or not appropriate to include in the plan of care."),
        "matrix": matrix("Potential Intervention", ["Appropriate", "Not Appropriate"], [
            ("Notify provider", 0), ("Administer oxycodone 10 mg", 1), ("Compress JP drain", 0),
            ("Blood draw for hemoglobin and hematocrit", 0), ("Insert indwelling urinary catheter", 1),
            ("Administer senna 1 tablet PO twice daily", 0)]),
        "explanation": (
            "Because the dressing is saturated, the nurse notifies the provider. Compressing the JP drain restores the "
            "suction needed for drainage. Hemoglobin and hematocrit are drawn to monitor blood loss. Senna prevents "
            "straining during a bowel movement; the client has had no bowel movement for several days and is taking "
            "opioids, which cause constipation.<br>The pain is well controlled at 4/10, and the 10-mg oxycodone order is "
            "for pain of 7&ndash;10, so it is not the appropriate dose. An indwelling catheter is not indicated: the "
            "client has the urge to void, and it has not been 8 hours since the catheter was removed."),
    }),
    (INTRO, tabs(5), {
        "type": "select_all",
        "preamble": ("The nurse has reviewed the Nurses&rsquo; Notes from Day 1 1610 and Day 2 0900, the Vital Signs from "
                     "Day 2 0900, and the Medications. At 0900 on day 2, the provider comes to the bedside and places "
                     "discharge orders."),
        "stem": "What should the nurse teach the client before discharge? <b>Select all that apply.</b>",
        "options": opts(("Wear your back brace at all times, including when you sleep.", 0),
                        ("Take a prescribed stool softener daily after discharge to prevent straining.", 1),
                        ("Do not bend, twist, or lift more than 5–10 lb (2–4.5 kg) after surgery.", 1),
                        ("Call the provider’s office if you experience fever or chills.", 1),
                        ("Pull off the adhesive strips over the incision if they begin to peel off the skin.", 0),
                        ("Check the surgical dressing in the mirror daily.", 1),
                        ("Limit your activity for the first 2 weeks after surgery.", 0),
                        ("Take 10 mg of oxycodone for mild pain.", 0)),
        "explanation": (
            "A stool softener prevents straining. Bending, lifting, and twisting are avoided after spine surgery. Fever "
            "or chills could be signs of infection and should be reported. The client should check the surgical dressing "
            "daily to monitor drainage.<br>The TLSO brace is worn when moving around or sitting, not while lying down. "
            "Adhesive strips are left alone to fall off on their own. Clients are encouraged to walk as much as possible "
            "after spine surgery rather than limit activity. Mild pain is managed with a nonopioid such as "
            "acetaminophen."),
    }),
    (INTRO, tabs(6), {
        "type": "matrix_mc",
        "stem": ("For each client statement, click to specify whether the statement indicates an understanding or no "
                 "understanding of the teaching provided."),
        "matrix": matrix("Client Statement", ["Understanding", "No Understanding"], [
            ("“I should take the stool softener only if I feel constipated.”", 1),
            ("“I should walk as much as possible after surgery.”", 0),
            ("“I am able to get my bandage wet and can soak in the tub to relieve pain.”", 1),
            ("“I should only take the opioid medication when I experience moderate or severe pain.”", 0),
            ("“I should leave the adhesive strips on the incision until they fall off.”", 0),
            ("“I should be able to pick up my dog as long as it does not cause pain.”", 1),
            ("“I should wear the brace to sleep but can take it off when I’m walking around.”", 1),
            ("“I do not need to worry about the surgical dressing until I go to the provider in 2 weeks.”", 1)]),
        "explanation": (
            "Walking as much as possible, using the opioid only for moderate or severe pain (mild pain is managed with a "
            "nonopioid such as acetaminophen), and leaving the adhesive strips to fall off on their own show "
            "understanding.<br>The stool softener is taken daily to prevent straining, not only when constipated. The "
            "bandage can get wet in the shower, but the client should not soak in a tub or hot tub. Lifting is limited, "
            "so she should not pick up her dog. The TLSO brace is worn when moving around or sitting, not while lying "
            "down. The surgical site dressing is checked daily to monitor drainage."),
    }),
]

case = make_case(N, "", "", screens, FN)
case["description"] = ("Maryland Next Gen NCLEX Test Bank Project, January 25, 2023; Authors: Mary DiBartolo and Allison "
                       "Hynson. Spine surgery: a 65-year-old client after an L2-L4 laminectomy with a saturated dressing and "
                       "a nonfunctioning JP drain; priorities, interventions, and discharge teaching.")

B_D2 = note("Day 2 0900", (
    "Vital signs taken; client reports feeling &ldquo;lousy.&rdquo; Alert and oriented &times; 4 with full sensation in all "
    "extremities. JP drain has 10 mL of serosanguineous drainage. Surgical dressing intact with an area of yellow drainage "
    "the size of a quarter. Client reports 9/10 back pain unrelieved by oxycodone given at 0700."))
B_VS = vitals(["Day 1 1200", "Day 2 0900"], [("T", "36.7&deg;C (98.2&deg;F)", "38.4&deg;C (101.2&deg;F)"),
                                             ("P", "77", "89"), ("RR", "20", "18"), ("BP", "110/80", "105/75"),
                                             ("Pulse oximetry reading", "94% on 2 L/min NC", "95% on room air"),
                                             ("Pain", "3/10", "9/10")])
B_LABS = table(["Laboratory Test and Reference Range", "Day 2"], [
    [lab("Glucose, fasting", "&lt; 5.5 mmol/L"), "7.2 mmol/L"],
    [lab("Hematocrit (Hct)", "Male: 0.42&ndash;0.52 L/L; Female: 0.35&ndash;0.47 L/L"), "0.30 L/L"],
    [lab("Hemoglobin (Hgb)", "Male: 130&ndash;180 g/L; Female: 120&ndash;160 g/L"), "110 g/L"],
    [lab("White blood cell (WBC) count", "4.5&ndash;10.5" + G9), "17.0" + G9],
    [lab("Platelet count", "140&ndash;450" + G9), "200" + G9]])
B_MEDS = table(["Medication", "Dose, Route, Frequency", "Times Given"], [
    ["Oxycodone", "5 mg PO every 4 hours as needed for moderate pain (4&ndash;6)", ""],
    ["Oxycodone", "10 mg PO every 4 hours as needed for severe pain (7&ndash;10)", "Day 2 0700"]])
bow = make_standalone(N, 1, "Bowtie", "Stand-alone bow-tie for University of Maryland - CS18 (spine surgery): surgical site "
                      "infection.", INTRO,
                      [{"id": f"nn_umd{S}b", "title": "Nurses' Notes",
                        "content": note("Day 1 1200", ADMIT.format(PAIN="")) + B_D2},
                       {"id": f"vs_umd{S}b", "title": "Vital Signs", "content": B_VS},
                       {"id": f"labs_umd{S}b", "title": "Laboratory Results", "content": B_LABS},
                       {"id": f"meds_umd{S}b", "title": "Medications", "content": B_MEDS}],
                      dict({"type": "bowtie",
                            "stem": ("Complete the diagram by dragging from the choices below to specify what condition "
                                     "the client is most likely experiencing, 2 actions the nurse should take to address "
                                     "that condition, and 2 parameters the nurse should monitor to assess the "
                                     "client&rsquo;s progress."),
                            "explanation": (
                                "The client has a surgical site infection, shown by the yellow drainage on the dressing, "
                                "the fever, the increased pain, and the elevated WBC count. The nurse gives acetaminophen "
                                "to reduce the fever and removes the dressing to assess the surgical site for other signs "
                                "of infection, then monitors the temperature (response to acetaminophen) and the WBC count "
                                "(improvement or worsening of the infection).<br>Reinforcing the dressing is not "
                                "appropriate, because the incision needs to be assessed. Ibuprofen is avoided after spine "
                                "surgery because of the bleeding risk. The JP drain has only 10 mL and does not need to be "
                                "emptied. The neurologic status, respiratory rate, and blood pressure are stable.")},
                           **bowtie([("Reinforce surgical dressing", 0), ("Administer acetaminophen", 1),
                                     ("Administer ibuprofen", 0), ("Assess surgical site", 1), ("Empty JP drain", 0)],
                                    [("Clotting of the JP drain", 0), ("Postoperative pain", 0),
                                     ("Surgical site infection", 1), ("Sepsis", 0)],
                                    [("Temperature", 1), ("Neurologic status", 0), ("Respiratory rate", 0),
                                     ("Blood pressure", 0), ("WBC count", 1)])), FN_B)

NOTES = [
    "Nurses' notes: pupils were recorded as \"3 cm\"; changed to 3 mm.",
    "Screen 1 listed \"Urinary retention\" twice; it appears once.",
    "Bow-tie: a surgical site infection on postoperative day 1-2 is early (SSIs usually appear after day 3-5; early "
    "fever is more often atelectasis or inflammation). Consider moving the bow-tie to day 4-5. The source's 10-mg "
    "oxycodone line was missing its dose on the bow-tie; filled in as 10 mg.",
    "Discharge teaching mixes \"stool softener\" (screen 5-6) with the senna order (a stimulant laxative). Consider "
    "docusate, or calling senna a laxative.",
    "Screen 5 key: \"Check the surgical dressing in the mirror daily\" is correct; consider whether a family member should "
    "check it (hard to see a lumbar incision in a mirror).",
    "\"Steri-strips\" (a brand name) now read \"adhesive strips\".",
    "Labs in SI with the author's ranges: glucose 130 mg/dL → 7.2 mmol/L; Hct 0.30 L/L; Hgb 110 g/L; WBC 10.0 × 10⁹/L "
    "(bow-tie 17.0); platelets 200 × 10⁹/L; HbA1c 6.0% (< 5.7%, US range; see CS2 note).",
    "Screen 5 options were reordered so a correct answer is not listed first.",
]

write([case, bow], N, "Care of Client Post-Op Spine Surgery (Laminectomy)", "Spine-Surgery.docx", NOTES)
