"""NURS 1017 Unit 7 Case Study 3: bacterial (meningococcal) meningitis in a university student.

Learning outcomes: pathophysiology of bacterial meningitis; increased ICP and cerebral edema (vasogenic, cytotoxic, interstitial);
seizure classification (generalized tonic-clonic, status epilepticus); communicating vs non-communicating hydrocephalus; prevention.
Sources checked: OpenStax Medical-Surgical Nursing 17.1, 17.2 (meningitis), 17.5 (seizures); Lewis's Medical-Surgical Nursing in
Canada (meningitis, CSF findings); Canadian guidance: droplet precautions until 24 hours of effective therapy, public health reporting
and chemoprophylaxis for close contacts, MenC-ACYW/MenB vaccines (NACI); ILAE 2017 seizure classification.
CSF reference values are common textbook values (not in the MCC list used by js/lab-ranges.js).
"""
from unit7_common import (NeuroChart, vs, lab, opts, dropdown, matrix_mc, matrix_mr, rationale, screen, write_case)

INTRO = "The nurse in the emergency department is caring for a 19-year-old female university student brought in by her roommate."
C = NeuroChart()

# ---------------------------------------------------------------- Screen 1: select all (recognize)
C.notes("nn", "Nurses' Notes",
    ("Day 1 2200", "Roommate states the client has had a fever, a severe headache and vomiting since this morning, and has become more "
     "confused over the last 2 hours. Client says, “My neck hurts when I bend it” and covers her eyes because the room lights hurt. "
     "Lives in a university residence; a friend on her floor had a “bad cold” last week. Unsure whether she received the school "
     "meningococcal vaccine. Drowsy, opens eyes to voice, oriented to person only (GCS 13: E3 V4 M6). Neck stiff with pain on flexion; "
     "positive Kernig and Brudzinski signs. Nonblanching petechial rash on the legs and trunk. Hands and feet cool; capillary refill 4 "
     "seconds. Pupils equal, 4 mm, reactive. Lungs clear. Abdomen soft, nontender. Last menstrual period 2 weeks ago."))
C.vitals("Day 1 2200", vs("39.6° C", "124 beats/min", "24 breaths/min", "96/58 mm Hg", "96% on room air"))
s1 = screen(1, INTRO, C, {
    "type": "select_all",
    "stem": "The nurse reviews the client's history and assessment. Which of the following findings would be consistent with "
            "<b>bacterial meningitis</b>? <b>Select all that apply.</b>",
    "options": opts(
        ("Temperature 39.6° C", True),
        ("Pupils equal and reactive", False),
        ("Severe headache with vomiting", True),
        ("Neck stiffness with pain on flexion", True),
        ("Abdomen soft and nontender", False),
        ("Positive Kernig and Brudzinski signs", True),
        ("Photophobia", True),
        ("SpO₂ 96% on room air", False),
        ("Confusion and drowsiness", True),
        ("Last menstrual period 2 weeks ago", False),
        seed="u7c3-s1"),
    "explanation": rationale(
        "<b>Consistent with bacterial meningitis:</b> fever, a severe headache and vomiting, and <b>meningeal irritation</b>: neck "
        "stiffness (nuchal rigidity), photophobia, a positive Kernig sign (pain and resistance when the knee is extended with the hip "
        "flexed) and a positive Brudzinski sign (neck flexion causes flexion of the hips and knees). Inflamed meninges are stretched by "
        "these movements. Confusion and drowsiness reflect cerebral inflammation and rising ICP.",
        "<b>Also important:</b> a <b>nonblanching petechial rash</b>, hypotension, tachycardia and poor perfusion point to "
        "meningococcemia (<i>Neisseria meningitidis</i> in the bloodstream), which can progress to septic shock within hours.",
        "<b>Not consistent:</b> equal, reactive pupils, normal oxygen saturation, a soft abdomen and the menstrual history are expected "
        "or unrelated findings."),
})

# ---------------------------------------------------------------- Screen 2: matrix multiple response (analyze)
C.notes("nn", "Nurses' Notes",
    ("Day 1 2215", "Two sets of blood cultures drawn. Dexamethasone IV given at 2218, then ceftriaxone IV and vancomycin IV started at "
     "2220. Droplet precautions in place."),
    ("Day 1 2310", "Lumbar puncture done after the head CT; CSF sent to the laboratory."))
C.notes("dx", "Diagnostic Results",
    ("Day 1 2240", "<b>Non-contrast head CT:</b> no mass, bleeding or hydrocephalus; ventricles normal in size."),
    ("Day 1 2330", "<b>Cerebrospinal fluid (CSF):</b> opening pressure 32 cm H₂O (reference ≤ 20 cm H₂O); appearance cloudy (reference "
     "clear, colourless); WBC 2,400 × 10⁶/L, 90% neutrophils (reference 0–5 × 10⁶/L, lymphocytes); protein 2.1 g/L (reference "
     "0.15–0.45 g/L); glucose 1.2 mmol/L (reference 2.2–3.9 mmol/L, about 60% of the blood glucose); Gram stain: Gram-negative "
     "diplococci."))
C.labs("Day 1 2215", [
    (lab("White blood cell (WBC) count", "3.5–10.5 × 10<sup>9</sup>/L"), "22.4 × 10<sup>9</sup>/L"),
    (lab("Platelet count", "130–380 × 10<sup>9</sup>/L"), "88 × 10<sup>9</sup>/L"),
    (lab("Lactate", "0.5–2.5 mmol/L"), "4.1 mmol/L"),
    (lab("Glucose, random", "4.0–11.0 mmol/L"), "6.2 mmol/L"),
    (lab("Sodium (Na)", "136–146 mmol/L"), "134 mmol/L"),
    (lab("Creatinine", "Female: 22–75 µmol/L"), "68 µmol/L"),
])
s2 = screen(2, INTRO, C, {
    "type": "matrix_mr",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 1 2215 and 2310, the Diagnostic Results and the Laboratory Results.",
    "stem": "For each finding, click to specify whether it is a sign of <b>meningeal irritation</b>, <b>increased intracranial pressure "
            "(ICP)</b>, or <b>sepsis</b>. Each finding may be a sign of more than one problem.",
    "matrix": matrix_mr("Finding", ["Meningeal irritation", "Increased ICP", "Sepsis"], [
        ("Neck stiffness with pain on flexion", [0]),
        ("Drowsy and oriented to person only", [1, 2]),
        ("Nonblanching petechial rash on the legs and trunk", [2]),
        ("Positive Kernig and Brudzinski signs", [0]),
        ("BP 96/58 mm Hg, cool hands and feet, and a capillary refill of 4 seconds", [2]),
        ("Photophobia", [0]),
        ("CSF opening pressure of 32 cm H₂O", [1]),
        ("Lactate 4.1 mmol/L", [2]),
    ]),
    "explanation": rationale(
        "<b>How bacterial meningitis develops:</b> <i>Neisseria meningitidis</i> spreads by respiratory droplets and close contact "
        "(shared residences). It colonizes the nasopharynx, enters the bloodstream, crosses the blood-brain barrier and multiplies in "
        "the CSF. The body's inflammatory response fills the space around the brain with white cells and pus (the cloudy CSF with "
        "neutrophils, high protein and low glucose on her results), irritates the meninges, and makes the brain swell.",
        "<b>Meningeal irritation</b> (hallmark signs): neck stiffness, photophobia, and positive <b>Kernig</b> (pain and resistance "
        "when the knee is straightened with the hip flexed) and <b>Brudzinski</b> (bending the neck makes the hips and knees flex) "
        "signs, because these movements stretch the inflamed meninges.",
        "<b>Increased ICP:</b> a falling level of consciousness is the earliest sign; the high CSF opening pressure confirms it. "
        "Swelling comes from leaky vessels (vasogenic edema), injured cells (cytotoxic edema) and blocked CSF absorption.",
        "<b>Sepsis:</b> meningococcal bacteria in the blood cause low BP, poor perfusion (cool skin, slow capillary refill), a high "
        "lactate, and a <b>nonblanching petechial or purpuric rash</b> from bleeding into the skin as clotting factors and platelets "
        "are used up (platelets 88 × 10⁹/L). Drowsiness can come from both raised ICP and poor brain perfusion. The rash is a "
        "hallmark of meningococcal disease and must be reported at once."),
})

# ---------------------------------------------------------------- Screen 3: drop-down cloze (prioritize)
s3 = screen(3, INTRO, C, {
    "type": "dropdown_cloze",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {
        "text": "The client is at highest risk for [[drop0]] as a result of [[drop1]]. She is also at risk for [[drop2]], as shown by "
                "[[drop3]].",
        "dropdowns": [
            dropdown(("autonomic dysreflexia", False), ("increased intracranial pressure", True), ("spinal shock", False),
                     ("acute ischemic stroke", False), seed="u7c3-d0"),
            dropdown(("a hematoma from a fall", False), ("demyelination of the central nervous system", False),
                     ("cerebral edema from the inflammatory response", True), ("obstruction by a brain tumor", False), seed="u7c3-d1"),
            dropdown(("septic shock and disseminated intravascular coagulation", True), ("anaphylaxis", False),
                     ("neurogenic shock", False), ("hypovolemic shock from vomiting alone", False), seed="u7c3-d2"),
            dropdown(("photophobia and neck stiffness", False), ("a friend's recent cold", False),
                     ("hypotension, a nonblanching rash, a high lactate, and a low platelet count", True),
                     ("a serum sodium of 134 mmol/L", False), seed="u7c3-d3"),
        ],
    },
    "explanation": rationale(
        "<b>Increased ICP from cerebral edema:</b> the opening pressure of 32 cm H₂O and the falling level of consciousness show raised "
        "ICP. Meningitis causes all three types of cerebral edema: <b>vasogenic</b> (inflammation makes the blood-brain barrier leaky, "
        "so plasma moves into the brain's extracellular space), <b>cytotoxic</b> (toxins and ischemia make cell membrane pumps fail, so "
        "water moves into cells), and <b>interstitial</b> (purulent exudate blocks CSF absorption, causing hydrocephalus). Raised ICP can "
        "lead to herniation.",
        "<b>Septic shock and DIC:</b> meningococcemia releases large amounts of endotoxin, causing vasodilation and capillary leak "
        "(BP 96/58 mm Hg, cool extremities, slow capillary refill, lactate 4.1 mmol/L) and widespread clotting that uses up platelets "
        "(88 × 10⁹/L) and clotting factors, causing the <b>nonblanching petechial rash</b> that can become purpura and skin necrosis.",
        "<b>Why not the others:</b> photophobia and neck stiffness are meningeal signs, not signs of sepsis; the friend's cold is an "
        "exposure clue; the sodium is only slightly low. Autonomic dysreflexia, spinal and neurogenic shock follow spinal cord injury; "
        "demyelination is multiple sclerosis."),
})

# ---------------------------------------------------------------- Screen 4: select all (generate solutions)
C.notes("ord", "Provider Orders",
    ("Day 1 2345", "Admit to the intensive care unit. Droplet precautions.<br>"
     "Ceftriaxone 2 g IV every 12 hours; vancomycin IV as dosed by pharmacy, with trough levels and creatinine.<br>"
     "Dexamethasone 10 mg IV every 6 hours for 4 days; capillary glucose every 6 hours.<br>"
     "0.9% sodium chloride 1,000 mL IV bolus, then 125 mL/h; norepinephrine infusion if MAP stays below 65 mm Hg.<br>"
     "Neurological checks and vital signs every hour.<br>"
     "Acetaminophen 650 mg PO/PR every 4 hours PRN for fever or headache.<br>"
     "Report the case to public health."))
s4 = screen(4, INTRO, C, {
    "type": "select_all",
    "preamble": "The nurse has reviewed the Provider Orders.",
    "stem": "Which interventions should the nurse include in the client's plan of care? <b>Select all that apply.</b>",
    "options": opts(
        ("Maintain droplet precautions until she has received 24 hours of effective antibiotic therapy", True),
        ("Place her in a negative-pressure room and wear an N95 respirator for all care", False),
        ("Keep the room quiet and dimly lit", True),
        ("Restrict fluids to 500 mL per day to prevent cerebral edema", False),
        ("Elevate the head of the bed to 30 degrees", True),
        ("Watch for flushing, itching and low BP during the vancomycin infusion", True),
        ("Support the neck in flexion on two pillows to ease the neck pain", False),
        ("Implement seizure precautions", True),
        ("Check her capillary glucose while she receives dexamethasone", True),
        ("Confirm that public health has been notified so close contacts can receive preventive antibiotics", True),
        seed="u7c3-s4"),
    "explanation": rationale(
        "<b>Include:</b> <i>N. meningitidis</i> spreads by large respiratory droplets, so <b>droplet precautions</b> (surgical mask "
        "within 2 metres, private room) continue until 24 hours of effective therapy. A quiet, dim room eases photophobia and headache "
        "and avoids stimulation that can raise ICP. The head of the bed at 30 degrees aids venous drainage. Irritation of the brain "
        "surface makes seizures common, so seizure precautions are in place. Meningococcal disease is reportable: public health traces "
        "close contacts (roommates, partners, people who shared drinks) and arranges preventive antibiotics and vaccination.",
        "<b>Medication adverse effects:</b> vancomycin infused too quickly can cause a <b>vancomycin infusion reaction</b> (flushing and "
        "itching of the face, neck and upper body, sometimes low BP); the nurse slows or stops the infusion and reports it. Vancomycin "
        "can also harm the kidneys, so creatinine and trough levels are followed. Dexamethasone raises blood glucose (and can cause "
        "gastric irritation, mood change and insomnia), so glucose is monitored.",
        "<b>Do not include:</b> airborne precautions with a negative-pressure room are for diseases such as tuberculosis or measles, "
        "not meningococcus. Fluid restriction would worsen her shock; she needs fluids to maintain perfusion (sodium is monitored, "
        "because meningitis can cause water retention). Neck flexion is painful and can obstruct venous outflow from the head; the "
        "neck is kept in a neutral position.",
        "<b>Prevention:</b> in Canada, the MenC-ACYW vaccine is given in the school program and the MenB vaccine to people at higher "
        "risk; both are part of the nurse's teaching for students in shared housing."),
})

# ---------------------------------------------------------------- Screen 5: matrix indicated / contraindicated (take action)
C.notes("nn", "Nurses' Notes",
    ("Day 2 0545", "Client had a generalized tonic-clonic seizure lasting 2 minutes: sudden stiffening of the whole body, then rhythmic "
     "jerking of all four limbs; no warning or focal movements beforehand. Now postictal: snoring respirations, opens eyes to pain only "
     "(GCS 8). Headache had been worsening overnight, with two episodes of vomiting. Pupils equal, 4 mm, sluggish."))
C.vitals("Day 2 0600", vs("38.9° C", "68 beats/min", "14 breaths/min, irregular", "152/64 mm Hg", "91% on room air"))
C.notes("ord", "Provider Orders",
    ("Day 2 0550", "Lorazepam 4 mg IV for a seizure lasting 5 minutes or longer; may repeat once.<br>"
     "Levetiracetam 60 mg/kg IV (maximum 4,500 mg) loading dose now, then 1,000 mg IV every 12 hours.<br>"
     "STAT non-contrast head CT. Neurosurgery consult."))
s5 = screen(5, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 2 0545, the Vital Signs from Day 2 0600 and the Provider Orders from "
                "Day 2 0550.",
    "stem": "For each action, click to specify whether it is <b>indicated</b> or <b>contraindicated</b> for the client at this time.",
    "matrix": matrix_mc("Nursing Action", ["Indicated", "Contraindicated"], [
        ("Turn the client onto her side and suction the mouth as needed", 0),
        ("Place a padded tongue blade between her teeth in case another seizure occurs", 1),
        ("Apply oxygen and monitor her airway and breathing closely", 0),
        ("Administer the levetiracetam loading dose", 0),
        ("Prepare her for a repeat lumbar puncture to drain CSF and lower the pressure", 1),
        ("Discontinue droplet precautions because she has received 8 hours of antibiotics", 1),
        ("Prepare her for the STAT head CT", 0),
    ]),
    "explanation": rationale(
        "<b>Seizure classification</b> (International League Against Epilepsy): seizures are <b>focal onset</b> (starting in one "
        "hemisphere; with awareness or with impaired awareness; may spread to a <b>focal to bilateral tonic-clonic</b> seizure), "
        "<b>generalized onset</b> (both hemispheres from the start: motor, such as tonic-clonic, tonic, clonic, myoclonic and atonic, or "
        "non-motor, such as absence), or <b>unknown onset</b>. This seizure began with whole-body stiffening and jerking without focal "
        "signs, so it is described as a generalized tonic-clonic seizure. A seizure lasting 5 minutes or longer, or repeated seizures "
        "without recovery between them, is <b>status epilepticus</b>.",
        "<b>Indicated:</b> after the seizure she is postictal with snoring respirations and SpO₂ 91%: a side-lying position and "
        "suction keep the airway clear, and oxygen is given. The loading dose of levetiracetam prevents further seizures. Her worsening "
        "headache, vomiting, falling GCS and Cushing's triad (widening pulse pressure, relative bradycardia, irregular breathing) signal "
        "rising ICP, so she goes for the STAT CT.",
        "<b>Contraindicated:</b> nothing is placed in the mouth during a seizure (broken teeth, airway obstruction, bitten fingers). A "
        "lumbar puncture with suspected raised ICP can cause herniation. Droplet precautions continue until 24 hours of effective "
        "therapy."),
})

# ---------------------------------------------------------------- Screen 6: matrix (evaluate)
C.notes("dx", "Diagnostic Results",
    ("Day 2 0640", "<b>Non-contrast head CT:</b> enlargement of the lateral, third and fourth ventricles with no obstructing lesion, "
     "consistent with communicating hydrocephalus. Diffuse cerebral edema."),
    ("Day 2 2200", "<b>Blood and CSF cultures:</b> <i>Neisseria meningitidis</i>, serogroup B, sensitive to ceftriaxone."))
C.notes("nn", "Nurses' Notes",
    ("Day 2 0730", "External ventricular drain (EVD) inserted by neurosurgery; opening ICP 28 mm Hg. Draining clear, slightly cloudy CSF."),
    ("Day 12 1000", "EVD removed on Day 8; repeat CT shows normal ventricles. Client alert and oriented, ambulating. No seizures since "
     "Day 2. Reports she “can't hear well” in her right ear. Dark, dry areas of skin on two toes of the left foot. Roommates and her "
     "boyfriend received ciprofloxacin on Day 2. Discharge planned for Day 14."))
C.vitals("Day 12 1000", vs("36.9° C", "82 beats/min", "16 breaths/min", "118/72 mm Hg", "98% on room air"))
C.labs("Day 12 0600", [
    (lab("White blood cell (WBC) count", "3.5–10.5 × 10<sup>9</sup>/L"), "8.1 × 10<sup>9</sup>/L"),
    (lab("Platelet count", "130–380 × 10<sup>9</sup>/L"), "214 × 10<sup>9</sup>/L"),
    (lab("Lactate", "0.5–2.5 mmol/L"), "1.1 mmol/L"),
    (lab("Glucose, random", "4.0–11.0 mmol/L"), "5.4 mmol/L"),
    (lab("Sodium (Na)", "136–146 mmol/L"), "139 mmol/L"),
])
s6 = screen(6, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Diagnostic Results from Day 2, the Nurses' Notes from Day 2 0730 and Day 12 1000, and the "
                "Vital Signs and Laboratory Results from Day 12.",
    "stem": "For each finding, click to specify whether it shows that an <b>expected outcome has been met</b> or that it "
            "<b>requires follow-up</b>.",
    "matrix": matrix_mc("Finding", ["Expected outcome met", "Requires follow-up"], [
        ("Alert and oriented, with no seizures since Day 2", 0),
        ("Reduced hearing in the right ear", 1),
        ("Normal ventricles on CT after removal of the drain", 0),
        ("Dark, dry areas of skin on two toes", 1),
        ("Platelet count 214 × 10⁹/L and lactate 1.1 mmol/L", 0),
        ("Close contacts received preventive antibiotics", 0),
        ("Temperature 36.9° C and WBC 8.1 × 10⁹/L", 0),
    ]),
    "explanation": rationale(
        "<b>Hydrocephalus</b> is an excess of CSF in the ventricles. In <b>non-communicating (obstructive) hydrocephalus</b>, CSF flow is "
        "blocked <b>within</b> the ventricular system (for example, aqueductal stenosis, a tumor or a clot), so only the ventricles above "
        "the block enlarge. In <b>communicating (non-obstructive) hydrocephalus</b>, CSF flows through the ventricles but is not absorbed "
        "by the arachnoid villi (granulations), as after meningitis or subarachnoid hemorrhage, so all ventricles enlarge, as in this "
        "client. <b>Normal pressure hydrocephalus</b> is a communicating type in older adults with gait disturbance, urinary incontinence "
        "and dementia. The EVD drained CSF until absorption recovered.",
        "<b>Outcomes met:</b> a normal level of consciousness without seizures, normal ventricles, a normal platelet count and lactate "
        "(DIC and shock resolved), no fever with a normal WBC (infection controlled), and close contacts treated to prevent secondary "
        "cases.",
        "<b>Require follow-up:</b> <b>sensorineural hearing loss</b> is the most common lasting complication of bacterial meningitis "
        "(inflammation of the inner ear and cranial nerve VIII); she needs an urgent audiology assessment, because early treatment, "
        "including cochlear implants, matters. Dark, dry skin on the toes suggests necrosis from the clotting in small vessels during "
        "meningococcemia and needs wound care assessment."),
})

write_case(3,
    "19-year-old university student with meningococcal meningitis and early sepsis: recognizing the hallmark signs of meningeal "
    "irritation, increased ICP and sepsis (including the nonblanching rash), nursing priorities, droplet precautions, a quiet "
    "environment, seizure precautions and public health follow-up, monitoring for vancomycin and dexamethasone adverse effects, "
    "care during and after a seizure, communicating hydrocephalus, and evaluation of complications such as hearing loss.",
    [s1, s2, s3, s4, s5, s6],
    ["- Revised 2 Nov 2026 to the nursing-focused rules: screen 2 now sorts findings into meningeal irritation, increased ICP and "
     "sepsis (CSF results stay in the chart and rationale); screen 4 adds monitoring for vancomycin and dexamethasone adverse effects.",
     "- CSF reference values are common textbook values (not in the MCC list): please check them against your course text.",
     "- Clinician review: antibiotic, dexamethasone and levetiracetam orders; chemoprophylaxis wording."],
    "Meningitis",
    intro_note="Case written by Claude on 2 Nov 2026 for the Unit 7 learning outcomes and revised the same day to be more "
               "nursing-focused; please review before using it with students:")
