"""NURS 1017 Unit 7 Case Study 4: glioblastoma presenting with a first seizure.

Learning outcomes: types of brain tumours (glioma/glioblastoma, meningioma, metastasis); seizure classification (focal impaired
awareness to bilateral tonic-clonic; status epilepticus); increased ICP manifestations; vasogenic vs cytotoxic edema; Monro-Kellie
components and causes of increased ICP by component (including non-communicating vs communicating hydrocephalus).
Sources checked: OpenStax Medical-Surgical Nursing 17.1 (ICP), 17.2 (brain tumours), 17.5 (seizures); Lewis's Medical-Surgical
Nursing in Canada (brain tumours, seizure disorders, ICP); ILAE 2017 seizure classification; status epilepticus at 5 minutes
(lorazepam 0.1 mg/kg IV, maximum 4 mg per dose).
"""
from unit7_common import (NeuroChart, vs, lab, opts, dropdown, matrix_mc, matrix_mr, rationale, highlight_tab, screen, write_case)

INTRO = "The nurse in the emergency department is caring for a 57-year-old female client brought in by her husband after a seizure at home."
C = NeuroChart()

# ---------------------------------------------------------------- Screen 1: highlight (recognize)
S1 = [("1910", "Husband states they were watching television when she {suddenly stopped talking and stared straight ahead}, {smacking "
       "her lips}, with her right hand picking at her shirt; she did not answer him. About a minute later her whole body stiffened and "
       "then jerked for about 2 minutes. {Bit her tongue}; {incontinent of urine}. Over the past 6 weeks she has had {headaches that are "
       "worst when she wakes up and when she coughs or bends over|correct}, and she {vomited on waking twice this week without feeling "
       "nauseated|correct}. He says she has been “irritable and forgetful, not herself,” and has trouble finding words. Now drowsy but "
       "rousable, oriented to person and place, slow to answer. Right hand grip slightly weaker than the left (4/5). Fundoscopic "
       "examination by the ED physician: {bilateral papilledema|correct}. {Point-of-care glucose 6.1 mmol/L}.")]
S1_VS = [("1910", "{T 37.0° C}, {P 92 beats/min}, {RR 18 breaths/min}, {BP 142/86 mm Hg}, {SpO₂ 97% on room air}.")]
C.notes("nn", "Nurses' Notes", *S1)
C.vitals("1910", vs("37.0° C", "92 beats/min", "18 breaths/min", "142/86 mm Hg", "97% on room air"))
s1 = screen(1, INTRO, C, {
    "type": "highlight",
    "stem": "The nurse reviews the Nurses' Notes and the Vital Signs. <b>Highlight</b> the findings that suggest increased intracranial "
            "pressure (ICP).",
    "options": [],
    "highlightTabs": [highlight_tab("ht1", "Nurses' Notes", S1), highlight_tab("ht2", "Vital Signs", S1_VS)],
    "maxCorrectSelections": None,
    "explanation": rationale(
        "<b>Suggest increased ICP:</b>",
        "<b>Headache worst on waking and with coughing or bending:</b> lying flat overnight and mild CO₂ retention during sleep "
        "increase cerebral blood volume; coughing and bending raise intrathoracic pressure and reduce venous drainage from the head.",
        "<b>Vomiting on waking without nausea</b> (often projectile): pressure on the vomiting centre in the medulla.",
        "<b>Bilateral papilledema:</b> swelling of the optic discs because raised CSF pressure is transmitted along the optic nerve "
        "sheaths; a reliable sign of sustained raised ICP.",
        "<b>Not signs of increased ICP:</b> staring, lip smacking, tongue biting and urinary incontinence are features of the seizure; "
        "the glucose rules out hypoglycemia as the cause of the seizure. The vital signs are not those of Cushing's triad (a late sign). "
        "Her drowsiness may be postictal or due to ICP, and the personality change, word-finding difficulty and right-hand weakness are "
        "focal deficits from the lesion itself; the nurse trends all of them."),
})

# ---------------------------------------------------------------- Screen 2: matrix multiple response (analyze)
C.notes("dx", "Diagnostic Results",
    ("2200", "<b>MRI brain with contrast:</b> 4.8-cm mass in the left frontotemporal lobe with ring enhancement and a necrotic centre, "
     "infiltrating the surrounding white matter. Extensive surrounding vasogenic edema; 6-mm midline shift to the right. Most "
     "consistent with a high-grade glioma (glioblastoma)."),
    ("2330", "<b>CT chest, abdomen and pelvis:</b> no primary tumor elsewhere."))
C.labs("1915", [
    (lab("Sodium (Na)", "136–146 mmol/L"), "139 mmol/L"),
    (lab("Glucose, random", "4.0–11.0 mmol/L"), "6.1 mmol/L"),
    (lab("White blood cell (WBC) count", "3.5–10.5 × 10<sup>9</sup>/L"), "8.4 × 10<sup>9</sup>/L"),
    (lab("Creatinine", "Female: 22–75 µmol/L"), "61 µmol/L"),
])
s2 = screen(2, INTRO, C, {
    "type": "matrix_mr",
    "preamble": "The nurse has reviewed the Diagnostic Results and the Laboratory Results.",
    "stem": "For each finding, click to specify whether it is related to the <b>tumor's location</b> (a focal deficit), to <b>increased "
            "intracranial pressure (ICP)</b>, or to the <b>seizure</b>. Each finding may be related to more than one cause.",
    "matrix": matrix_mr("Finding", ["Tumor's location", "Increased ICP", "Seizure"], [
        ("Trouble finding words", [0]),
        ("Headaches worst on waking and with coughing or bending", [1]),
        ("Bitten tongue and urinary incontinence", [2]),
        ("Weaker grip in the right hand", [0]),
        ("Bilateral papilledema", [1]),
        ("Irritable and forgetful, “not herself”", [0]),
        ("Drowsy and slow to answer in the emergency department", [1, 2]),
    ]),
    "explanation": rationale(
        "<b>Tumor location (focal deficits):</b> a left frontotemporal tumor affects language (word-finding difficulty), movement of "
        "the opposite (right) side, and the frontal lobe's control of personality and memory. The nurse documents these as her baseline "
        "and watches for change.",
        "<b>Increased ICP:</b> the tumor and the swelling around it take up space (Monro-Kellie doctrine: the skull holds brain tissue, "
        "blood and CSF, and when one increases, ICP rises once the others can no longer make room). Morning headache, headache with "
        "coughing or bending, vomiting and papilledema are its hallmark signs.",
        "<b>Seizure:</b> tongue biting and incontinence happen during a tonic-clonic seizure. Drowsiness can be <b>postictal</b> or a "
        "sign of increased ICP, so the nurse checks whether it improves over the next hour; if it does not, or worsens, it is reported.",
        "<b>Types of brain tumors:</b> <b>gliomas</b> arise from the brain's supporting (glial) cells; <b>glioblastoma</b> is the most "
        "common malignant primary brain tumor in adults, grows quickly and infiltrates surrounding brain. <b>Meningiomas</b> arise from "
        "the meninges, are usually benign and slow-growing, and press on the brain from outside. <b>Metastases</b> from cancers such as "
        "lung, breast and melanoma are the most common brain tumors overall (which is why her chest, abdomen and pelvis were scanned). "
        "Any of them can cause headache, seizures and focal deficits."),
})

# ---------------------------------------------------------------- Screen 3: drop-down cloze (prioritize)
s3 = screen(3, INTRO, C, {
    "type": "dropdown_cloze",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {
        "text": "The nurse documents the seizure the husband described as a [[drop0]]. The client's signs of increased ICP are mainly "
                "caused by [[drop1]], which is expected to improve with [[drop2]], so the nurse monitors her for [[drop3]].",
        "dropdowns": [
            dropdown(("generalized-onset tonic-clonic seizure", False), ("generalized absence seizure", False),
                     ("focal impaired awareness seizure that progressed to a bilateral tonic-clonic seizure", True),
                     ("focal aware motor seizure", False), seed="u7c4-d0"),
            dropdown(("cytotoxic edema", False), ("vasogenic edema", True), ("interstitial edema from hydrocephalus", False),
                     ("bleeding into the tumor", False), seed="u7c4-d1"),
            dropdown(("levetiracetam", False), ("dexamethasone", True), ("a hypotonic IV fluid", False), ("acetaminophen", False),
                     seed="u7c4-d2"),
            dropdown(("hypoglycemia", False), ("bradycardia", False), ("hyperglycemia", True), ("hypotension", False),
                     seed="u7c4-d3"),
        ],
    },
    "explanation": rationale(
        "<b>Seizure type:</b> staring and not answering (impaired awareness) with lip smacking and picking at her clothing "
        "(automatisms) is a <b>focal impaired awareness seizure</b>; it then spread to both sides of the brain (stiffening and jerking "
        "of the whole body), a <b>focal to bilateral tonic-clonic seizure</b>. Describing the start of a seizure accurately helps the "
        "team classify it. A first seizure in adulthood always prompts a search for a cause such as a tumor.",
        "<b>Vasogenic edema:</b> the tumor's abnormal blood vessels leak fluid through a damaged blood-brain barrier into the "
        "surrounding white matter. Corticosteroids (dexamethasone) stabilize the barrier and reduce this swelling. <b>Cytotoxic "
        "edema</b> is different: brain cells swell when they lack oxygen (ischemia, a prolonged seizure) and corticosteroids do not "
        "help it.",
        "<b>Adverse effects of dexamethasone:</b> high blood glucose (the most common), stomach irritation (given with food, often "
        "with a stomach-protecting drug), insomnia, mood changes, infection risk and, over time, thrush and muscle weakness. Glucose is "
        "checked as ordered and high readings are reported."),
})

# ---------------------------------------------------------------- Screen 4: matrix indicated / contraindicated (generate solutions)
C.notes("ord", "Provider Orders",
    ("2345", "Admit to the neurosurgical unit. Head of bed 30 degrees. Seizure precautions.<br>"
     "Dexamethasone 4 mg IV every 6 hours.<br>"
     "Pantoprazole 40 mg PO daily.<br>"
     "Levetiracetam 500 mg PO every 12 hours.<br>"
     "Docusate 100 mg PO twice daily.<br>"
     "Capillary blood glucose before meals and at bedtime.<br>"
     "Neurological checks every 2 hours.<br>"
     "Craniotomy for tumor resection planned for Day 3."))
s4 = screen(4, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Provider Orders.",
    "stem": "The nurse plans care to keep the client safe and prevent increases in ICP before surgery. For each intervention, click to "
            "specify whether it is <b>indicated</b> or <b>contraindicated</b>.",
    "matrix": matrix_mc("Intervention", ["Indicated", "Contraindicated"], [
        ("Keep the head of the bed at 30 degrees with her head in line with her body", 0),
        ("Encourage her to cough forcefully every hour to keep her lungs clear", 1),
        ("Give the stool softener and teach her not to strain or hold her breath during bowel movements", 0),
        ("Keep the bed low with the side rails padded and up", 0),
        ("Check her capillary glucose as ordered and report high readings", 0),
        ("Lay her flat with her legs raised when she has a headache", 1),
        ("Watch for drowsiness, dizziness, and mood changes after starting levetiracetam", 0),
        ("Apply wrist restraints if she becomes restless", 1),
    ]),
    "explanation": rationale(
        "<b>Indicated:</b> the head of the bed at 30 degrees with the head aligned helps venous blood drain from the brain. Straining "
        "and breath-holding (the Valsalva manoeuvre) raise pressure in the chest and head, so a stool softener and teaching prevent it. "
        "A low bed with padded rails protects her if she has another seizure. Dexamethasone raises blood glucose, so glucose is "
        "checked and high values are reported. Levetiracetam commonly causes drowsiness and dizziness (fall risk) and can cause "
        "irritability or low mood, which can be mistaken for tumor effects, so the nurse watches and reports.",
        "<b>Contraindicated:</b> forceful coughing raises ICP; deep breathing and gentle coughing are used instead. Lying flat with the "
        "legs raised reduces venous drainage from the head and raises ICP. Restraints increase agitation and ICP and can cause injury.",
        "<b>Linking the plan to the Monro-Kellie doctrine:</b> each measure limits an increase in one of the three volumes in the skull: "
        "brain tissue (swelling; reduced with dexamethasone), blood (venous drainage, avoiding straining, fever and too much sedation, "
        "since high CO₂ widens brain blood vessels) and CSF (watching for headache, vomiting and drowsiness that could mean blocked CSF "
        "flow, called non-communicating or obstructive hydrocephalus)."),
})

# ---------------------------------------------------------------- Screen 5: select all (take action)
C.notes("nn", "Nurses' Notes",
    ("Day 3 1500", "Returned from craniotomy and subtotal resection of the left frontotemporal tumor. Awake, oriented, mild word-finding "
     "difficulty unchanged from before surgery. Dressing dry."),
    ("Day 4 0710", "Called to the room by a nursing assistant: client is having a generalized tonic-clonic seizure that started at 0705 "
     "and is still continuing. Lips dusky; frothy saliva. Side rails up and padded; IV saline lock patent."))
C.notes("ord", "Provider Orders",
    ("Day 3 1500", "Lorazepam 4 mg IV for a seizure lasting 5 minutes or longer; may repeat once in 5 minutes. Notify provider for any "
     "seizure."))
s5 = screen(5, INTRO, C, {
    "type": "select_all",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 3 1500 and Day 4 0710 and the Provider Orders from Day 3 1500.",
    "stem": "Which actions should the nurse take now? <b>Select all that apply.</b>",
    "options": opts(
        ("Turn the client onto her side", True),
        ("Restrain her arms and legs to prevent injury", False),
        ("Administer the prescribed IV lorazepam", True),
        ("Insert a padded tongue blade between her teeth", False),
        ("Apply oxygen and have suction ready", True),
        ("Withhold medication until the seizure has lasted 15 minutes", False),
        ("Check her capillary blood glucose", True),
        ("Call for help and notify the provider", True),
        ("Monitor her breathing and level of sedation after the lorazepam is given", True),
        seed="u7c4-s5"),
    "explanation": rationale(
        "The seizure has lasted more than 5 minutes: this is <b>status epilepticus</b>, a medical emergency. The longer it lasts, the "
        "less likely it is to stop on its own, and continuous neuronal firing causes hypoxia, excitotoxic (cytotoxic) brain injury and "
        "rising ICP.",
        "<b>Correct:</b> a side-lying position lets saliva drain and keeps the tongue from blocking the airway. Lorazepam is "
        "given as ordered; it can depress breathing and cause deep sedation, so the nurse watches her breathing and level of "
        "consciousness afterwards. Oxygen and suction treat the hypoxia (dusky lips). Hypoglycemia can "
        "cause or prolong seizures, and dexamethasone affects glucose, so the glucose is checked. Help is needed to manage the airway, "
        "drugs and monitoring, and the provider must be notified.",
        "<b>Incorrect:</b> restraints can cause fractures and soft tissue injury; nearby objects are moved and the head is protected "
        "instead. Nothing is put in the mouth. Waiting to treat lets the seizure become harder to stop and the brain injury worse."),
})

# ---------------------------------------------------------------- Screen 6: matrix (evaluate)
C.notes("dx", "Diagnostic Results",
    ("Day 5 1400", "<b>Pathology:</b> glioblastoma, IDH-wildtype (WHO grade 4)."))
C.notes("nn", "Nurses' Notes",
    ("Day 9 1000", "No further seizures since Day 4 (levetiracetam increased to 1,000 mg every 12 hours). Headache 2/10, no vomiting. "
     "Incision clean and dry, staples intact. White patches on the tongue and inner cheeks that do not wipe off easily. Dexamethasone "
     "now 4 mg PO twice daily with a planned taper. Referred to the cancer centre for radiation and temozolomide. The nurse reviews the "
     "discharge teaching."),
    ("Day 9 1030", "Client states: “I'll stop the dexamethasone once my headaches are gone.” Also states: “I won't drive until my doctor "
     "tells me it's safe.” Husband states: “If she has a seizure, I'll turn her on her side, time it, and call 911 if it lasts 5 "
     "minutes.”"))
C.labs("Day 9 1630", [(lab("Glucose, capillary (before supper)", "4.0–7.0 mmol/L before meals"), "14.8 mmol/L")])
s6 = screen(6, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Diagnostic Results from Day 5, the Nurses' Notes from Day 9 1000 and 1030, and the Laboratory "
                "Results.",
    "stem": "For each finding, click to specify whether it shows that an <b>expected outcome has been met</b> or that it "
            "<b>requires follow-up</b>.",
    "matrix": matrix_mc("Finding", ["Expected outcome met", "Requires follow-up"], [
        ("No seizures since Day 4", 0),
        ("Capillary glucose 14.8 mmol/L before supper", 1),
        ("Headache 2/10 with no vomiting", 0),
        ("“I'll stop the dexamethasone once my headaches are gone.”", 1),
        ("White patches on the tongue and inner cheeks", 1),
        ("“I won't drive until my doctor tells me it's safe.”", 0),
        ("Husband's plan for managing a seizure at home", 0),
        ("Incision clean and dry, staples intact", 0),
    ]),
    "explanation": rationale(
        "<b>Outcomes met:</b> no further seizures on the increased levetiracetam dose; less headache and no vomiting (edema and ICP "
        "reduced after resection and dexamethasone); a healing incision. In Canada, a seizure leads to a period without driving set by "
        "provincial rules and the provider, and she understands this. The husband's plan is correct: protect, side-lying, time the "
        "seizure, and call 911 at 5 minutes.",
        "<b>Require follow-up:</b> <b>dexamethasone-induced hyperglycemia</b> (glucocorticoids raise hepatic glucose production and "
        "insulin resistance) needs to be reported for treatment. White patches that do not wipe off suggest <b>oral candidiasis</b> "
        "(thrush) from corticosteroid immunosuppression. Stopping dexamethasone suddenly can cause adrenal insufficiency and rebound "
        "cerebral edema: it must be <b>tapered</b> as prescribed, so this statement needs further teaching."),
})

write_case(4,
    "57-year-old female client with a first seizure in adulthood from a glioblastoma: recognizing signs of increased ICP, focal "
    "deficits and seizure features, documenting the seizure type, vasogenic edema and dexamethasone adverse effects, a care plan "
    "that keeps her safe and prevents rises in ICP, status epilepticus after craniotomy, and corticosteroid effects at discharge.",
    [s1, s2, s3, s4, s5, s6],
    ["- Revised 2 Nov 2026 to the nursing-focused rules: screen 2 now sorts findings into tumor location, increased ICP and seizure "
     "(tumor types in the rationale); screen 3 adds the dexamethasone adverse effect; screen 4 is a nursing care plan (Monro-Kellie "
     "and hydrocephalus in the rationale); screen 5 adds monitoring after lorazepam.",
     "- The capillary glucose target (4.0–7.0 mmol/L before meals) is the Diabetes Canada target, not an MCC laboratory range.",
     "- Clinician review: dexamethasone, levetiracetam and lorazepam orders."],
    "Brain_Tumour",
    intro_note="Case written by Claude on 2 Nov 2026 for the Unit 7 learning outcomes and revised the same day to be more "
               "nursing-focused; please review before using it with students:")
