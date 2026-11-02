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
    ("2200", "<b>MRI brain with contrast:</b> 4.8-cm mass in the left frontotemporal lobe with irregular ring enhancement, a necrotic "
     "centre and poorly defined margins infiltrating the surrounding white matter. Extensive surrounding vasogenic edema; 6-mm midline "
     "shift to the right; left lateral ventricle compressed. Ventricles not enlarged. Most consistent with a high-grade glioma "
     "(glioblastoma); metastasis less likely (single lesion). No dural-based mass."),
    ("2330", "<b>CT chest, abdomen and pelvis:</b> no primary tumor elsewhere."))
s2 = screen(2, INTRO, C, {
    "type": "matrix_mr",
    "preamble": "The nurse has reviewed the Diagnostic Results.",
    "stem": "The client's husband asks what kind of tumor this might be. For each feature, click to specify whether it is typical of a "
            "<b>glioblastoma</b>, a <b>meningioma</b>, or a <b>brain metastasis</b>. Each feature may apply to more than one tumor.",
    "matrix": matrix_mr("Feature", ["Glioblastoma", "Meningioma", "Brain metastasis"], [
        ("Arises from the meninges (arachnoid cells), outside the brain tissue", [1]),
        ("Arises from glial cells (astrocytes) within the brain tissue", [0]),
        ("Spreads to the brain through the blood from cancers such as lung, breast, or melanoma", [2]),
        ("Can cause seizures, headache, and focal neurological deficits", [0, 1, 2]),
        ("Usually benign and slow-growing; often cured by complete removal", [1]),
        ("Ring-enhancing lesion with surrounding edema on MRI", [0, 2]),
        ("Infiltrates the surrounding brain, so complete removal is rarely possible", [0]),
        ("Most common malignant primary brain tumor in adults", [0]),
    ]),
    "explanation": rationale(
        "<b>Gliomas</b> arise from the glial (supporting) cells of the brain: astrocytomas, oligodendrogliomas and ependymomas. "
        "<b>Glioblastoma</b> (grade 4 astrocytoma) is the most common malignant primary brain tumor in adults. It grows quickly, has a "
        "necrotic centre with ring enhancement, and sends cells along white matter tracts, so it cannot be removed completely and "
        "usually recurs; treatment is surgery, then radiation with temozolomide chemotherapy.",
        "<b>Meningiomas</b> arise from arachnoid cells of the meninges and press on the brain from outside (extra-axial, dural-based). "
        "They are the most common primary intracranial tumor, are usually benign and slow-growing, and are often cured by complete "
        "removal, but their location can still cause seizures, headache and deficits. Other tumor types include pituitary adenomas and "
        "vestibular schwannomas (acoustic neuromas).",
        "<b>Brain metastases</b> are the most common brain tumors overall in adults. Cancer cells reach the brain through the blood "
        "(most often from lung, breast, melanoma, kidney and colon) and are often multiple, at the grey-white matter junction, with "
        "ring enhancement and edema; that is why her chest, abdomen and pelvis were scanned.",
        "Any brain tumor can raise ICP (mass and edema), irritate the cortex (seizures) and cause deficits according to its location."),
})

# ---------------------------------------------------------------- Screen 3: drop-down cloze (prioritize)
s3 = screen(3, INTRO, C, {
    "type": "dropdown_cloze",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {
        "text": "The seizure the husband described is best classified as a [[drop0]]. The client's signs of increased ICP are mainly caused "
                "by [[drop1]], which results from [[drop2]] and is expected to improve with [[drop3]].",
        "dropdowns": [
            dropdown(("generalized-onset tonic-clonic seizure", False), ("generalized absence seizure", False),
                     ("focal impaired awareness seizure that progressed to a bilateral tonic-clonic seizure", True),
                     ("focal aware motor seizure", False), seed="u7c4-d0"),
            dropdown(("cytotoxic edema", False), ("vasogenic edema", True), ("interstitial edema from hydrocephalus", False),
                     ("bleeding into the tumor", False), seed="u7c4-d1"),
            dropdown(("failure of the sodium-potassium pump in oxygen-deprived brain cells", False),
                     ("blocked CSF absorption at the arachnoid villi", False),
                     ("abnormal tumor blood vessels that let plasma leak through a damaged blood-brain barrier", True),
                     ("a low serum albumin", False), seed="u7c4-d2"),
            dropdown(("levetiracetam", False), ("dexamethasone", True), ("a hypotonic IV fluid", False), ("acetaminophen", False),
                     seed="u7c4-d3"),
        ],
    },
    "explanation": rationale(
        "<b>Seizure type:</b> the seizure began in one hemisphere (the left temporal lobe near the tumor): staring and unresponsiveness "
        "(impaired awareness) with automatisms (lip smacking, picking at clothing with the right hand) is a <b>focal impaired awareness "
        "seizure</b> (formerly complex partial). It then spread to both hemispheres: a <b>focal to bilateral tonic-clonic seizure</b> "
        "(formerly secondarily generalized). A generalized-onset seizure involves both hemispheres from the start, without a focal "
        "beginning; an absence seizure is a brief stare without convulsions; in a focal aware seizure the person stays aware. A new "
        "seizure starting in adulthood always needs a search for a structural cause such as a tumor.",
        "<b>Vasogenic edema:</b> the tumor makes new, abnormal blood vessels whose walls lack normal tight junctions, so the blood-brain "
        "barrier leaks plasma proteins and water into the extracellular space, mostly in the white matter around the tumor. "
        "Corticosteroids (<b>dexamethasone</b>) stabilize the barrier and reduce this edema within hours to days.",
        "<b>Cytotoxic edema</b> is different: oxygen-deprived cells (ischemia, hypoxia, prolonged seizures) cannot run the "
        "sodium-potassium pump, so sodium and water enter the cells and they swell, in grey and white matter; it does <b>not</b> respond "
        "to corticosteroids. Levetiracetam prevents seizures but does not reduce edema; hypotonic fluids worsen edema."),
})

# ---------------------------------------------------------------- Screen 4: matrix (generate solutions)
C.notes("ord", "Provider Orders",
    ("2345", "Admit to the neurosurgical unit. Head of bed 30 degrees. Seizure precautions.<br>"
     "Dexamethasone 4 mg IV every 6 hours.<br>"
     "Pantoprazole 40 mg PO daily.<br>"
     "Levetiracetam 500 mg PO every 12 hours.<br>"
     "Capillary blood glucose before meals and at bedtime.<br>"
     "Neurological checks every 2 hours.<br>"
     "Craniotomy for tumor resection planned for Day 3."))
s4 = screen(4, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Provider Orders.",
    "stem": "The nurse plans care to keep the client's ICP from rising further. For each factor, click to specify which intracranial "
            "volume it increases: <b>brain tissue</b>, <b>blood</b>, or <b>cerebrospinal fluid (CSF)</b>.",
    "matrix": matrix_mc("Factor", ["Brain tissue", "Blood", "CSF"], [
        ("Vasogenic edema around the tumor", 0),
        ("Hypoventilation from oversedation, raising the PaCO₂", 1),
        ("A tumor blocking the cerebral aqueduct (non-communicating hydrocephalus)", 2),
        ("Neck flexion or rotation that compresses the jugular veins", 1),
        ("Cytotoxic edema after a prolonged seizure with hypoxia", 0),
        ("Scarring of the arachnoid villi that impairs CSF absorption (communicating hydrocephalus)", 2),
        ("Fever, which increases brain metabolism", 1),
    ]),
    "explanation": rationale(
        "<b>Monro-Kellie doctrine:</b> the skull holds brain tissue (about 80%), blood (about 10%) and CSF (about 10%). An increase in "
        "any one must be offset by a decrease in another, or ICP rises. The nurse plans care around all three.",
        "<b>Brain tissue:</b> the tumor mass and edema. Vasogenic edema is treated with dexamethasone; cytotoxic edema after a long "
        "seizure with hypoxia is prevented by stopping seizures quickly and keeping oxygenation normal (seizure precautions, "
        "levetiracetam on time).",
        "<b>Blood:</b> CO₂ is a strong cerebral vasodilator, so hypoventilation (oversedation, opioids) raises cerebral blood volume; "
        "sedation is monitored. A flexed or rotated neck obstructs jugular venous outflow; the head is kept midline with the head of the "
        "bed at 30 degrees. Fever and seizures increase metabolism and therefore cerebral blood flow; fever is treated promptly.",
        "<b>CSF:</b> CSF builds up if its flow is blocked inside the ventricular system (<b>non-communicating</b> or obstructive "
        "hydrocephalus, for example a tumor at the cerebral aqueduct or fourth ventricle) or if it is not absorbed by the arachnoid villi "
        "(<b>communicating</b> hydrocephalus, after meningitis or subarachnoid hemorrhage). Her ventricles are not enlarged now, but "
        "headache, vomiting and drowsiness after surgery could signal hydrocephalus and are reported."),
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
        seed="u7c4-s5"),
    "explanation": rationale(
        "The seizure has lasted more than 5 minutes: this is <b>status epilepticus</b>, a medical emergency. The longer it lasts, the "
        "less likely it is to stop on its own, and continuous neuronal firing causes hypoxia, excitotoxic (cytotoxic) brain injury and "
        "rising ICP.",
        "<b>Correct:</b> a side-lying position lets saliva drain and keeps the tongue from blocking the airway. Lorazepam is the "
        "first-line drug and is given at 5 minutes, as ordered. Oxygen and suction treat the hypoxia (dusky lips). Hypoglycemia can "
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
    "57-year-old female client with a first seizure in adulthood from a left frontotemporal glioblastoma: signs of increased ICP, "
    "glioblastoma vs meningioma vs brain metastasis, focal impaired awareness to bilateral tonic-clonic seizure, vasogenic vs "
    "cytotoxic edema, Monro-Kellie components and hydrocephalus types, status epilepticus after craniotomy, and corticosteroid "
    "complications at discharge.",
    [s1, s2, s3, s4, s5, s6],
    ["- Learning outcomes: brain tumour types, seizure classification, vasogenic vs cytotoxic edema, Monro-Kellie components and causes "
     "of increased ICP, non-communicating vs communicating hydrocephalus.",
     "- Screen 4 is a knowledge matrix framed as care planning (which volume each factor increases); please confirm it fits your "
     "Generate Solutions expectations.",
     "- The capillary glucose target (4.0–7.0 mmol/L before meals) is the Diabetes Canada target, not an MCC laboratory range.",
     "- Clinician review: dexamethasone, levetiracetam and lorazepam doses."],
    "Brain_Tumour")
