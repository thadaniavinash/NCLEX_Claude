"""NURS 1017 Unit 7 Case Study 6: Parkinson disease, chronic subdural hematoma and delirium in an older adult.

Learning outcomes: pathophysiology of Parkinson disease (with ALS and MS as contrasts); delirium vs dementia; types of dementia
(Alzheimer, vascular, Lewy body, Parkinson disease dementia, frontotemporal); subdural hematoma (chronic).
Sources checked: OpenStax Medical-Surgical Nursing 17.4 (major neurocognitive disorder, Parkinson disease, ALS) and 17.3 (MS);
Lewis's Medical-Surgical Nursing in Canada (Parkinson disease, delirium and dementia, head injury); Canadian Coalition for Seniors'
Mental Health delirium guidance; Parkinson Canada ("Get it on time"; avoid haloperidol and other dopamine blockers).
"""
from unit7_common import (NeuroChart, vs, lab, opts, dropdown, matrix_mc, rationale, screen, write_case, kv_html)

INTRO = "The nurse in the emergency department is caring for a 76-year-old male client with Parkinson disease brought in by his wife."
C = NeuroChart()

# ---------------------------------------------------------------- Screen 1: select all (recognize)
C.notes("nn", "Nurses' Notes",
    ("Day 1 1400", "Wife states that over the last 10 days he has become increasingly confused and sleepy and has had daily headaches. "
     "“Some hours he's his usual self, and other times he doesn't know where he is.” Up at night, pulling at his clothes. Four weeks "
     "ago he fell in the kitchen and hit his head on a cupboard door, without losing consciousness. Before this he managed his own "
     "medications and finances. Assessment: drowsy, easily distracted, cannot name the days of the week backward; oriented to person "
     "only. Resting tremor of the right hand (“pill-rolling”) that stops when he reaches for a cup; cogwheel rigidity in both arms; "
     "slow, small movements; shuffling gait with reduced arm swing (uses a walker); masklike face; soft, monotone voice. New mild "
     "weakness of the left arm with a downward drift. No muscle twitching or wasting. Last bowel movement 4 days ago."))
C.html("hp", "History and Physical", kv_html([
    ("Medical history", "Parkinson disease (diagnosed 9 years ago), atrial fibrillation, benign prostatic hyperplasia, cataract surgery."),
    ("Home medications", "Carbidopa-levodopa 25/100 mg, 2 tablets PO at 0700, 1100, 1500 and 1900; apixaban 5 mg PO twice daily; "
     "polyethylene glycol 17 g PO daily."),
    ("Social history", "Retired engineer; lives with his wife in a two-storey house. His mother had Alzheimer disease."),
]))
C.column("vs", "Vital Signs", "", "Day 1 1400", [
    ("<b>T</b>", "36.9° C"), ("<b>P</b>", "78 beats/min, irregular"), ("<b>RR</b>", "16 breaths/min"),
    ("<b>BP</b>", "Lying 138/78 mm Hg; standing 108/66 mm Hg"),
    ("<b>Pulse Oximetry Reading (SpO<sub>2</sub>)</b>", "96% on room air")])
s1 = screen(1, INTRO, C, {
    "type": "select_all",
    "stem": "The nurse reviews the client's history and assessment. Which of the following findings would be consistent with "
            "<b>Parkinson disease</b>? <b>Select all that apply.</b>",
    "options": opts(
        ("Resting tremor of the hand that stops with purposeful movement", True),
        ("Muscle twitching (fasciculations) and wasting", False),
        ("Cogwheel rigidity", True),
        ("Inability to name the days of the week backward", False),
        ("Slow, small movements (bradykinesia)", True),
        ("Shuffling gait with reduced arm swing", True),
        ("Tremor that worsens as the hand approaches a target", False),
        ("Masklike face and a soft, monotone voice", True),
        ("New weakness of the left arm with a downward drift", False),
        ("A drop in BP from 138/78 mm Hg lying to 108/66 mm Hg standing", True),
        seed="u7c6-s1"),
    "explanation": rationale(
        "<b>Parkinson disease</b> is a progressive neurodegenerative disease. Dopamine-producing neurons of the <b>substantia nigra</b> "
        "degenerate, and many contain <b>Lewy bodies</b> (clumps of misfolded alpha-synuclein). Less dopamine reaches the basal ganglia "
        "(striatum), leaving acetylcholine relatively unopposed. Motor signs appear only after about 60% to 80% of these neurons are lost.",
        "<b>Consistent:</b> the four cardinal signs are a <b>resting tremor</b> (pill-rolling, decreasing with purposeful movement), "
        "<b>rigidity</b> (cogwheel), <b>bradykinesia</b> and <b>postural instability</b> (shuffling, festinating gait with reduced arm "
        "swing, falls). Reduced automatic movement gives a masklike face and a soft, monotone voice. Autonomic involvement causes "
        "<b>orthostatic hypotension</b> (a drop of 20 mm Hg or more systolic on standing; here 30 mm Hg) and constipation.",
        "<b>Not consistent:</b> fasciculations and muscle wasting are signs of lower motor neuron loss, as in <b>amyotrophic lateral "
        "sclerosis (ALS)</b>, which destroys upper and lower motor neurons (weakness, atrophy, spasticity, eventually respiratory "
        "failure) while sensation is spared. A tremor that worsens near a target is an <b>intention tremor</b> from cerebellar disease, "
        "as in <b>multiple sclerosis</b> (autoimmune demyelination of the central nervous system). Inattention and the new one-sided "
        "weakness point to a new problem."),
})

# ---------------------------------------------------------------- Screen 2: matrix (analyze)
s2 = screen(2, INTRO, C, {
    "type": "matrix_mc",
    "stem": "The client's wife asks whether her husband is “getting dementia.” For each feature, click to specify whether it is more "
            "consistent with <b>delirium</b> or <b>dementia</b> (major neurocognitive disorder).",
    "matrix": matrix_mc("Feature", ["Delirium", "Dementia"], [
        ("Develops over hours to days", 0),
        ("Gradual, progressive decline over months to years", 1),
        ("Inattention, such as being unable to name the days of the week backward", 0),
        ("Alert, with attention preserved until the late stages", 1),
        ("Level of consciousness and confusion fluctuate during the day", 0),
        ("Caused by the progressive loss of neurons, as in Alzheimer disease", 1),
        ("Often reversible when the underlying cause is treated", 0),
    ]),
    "explanation": rationale(
        "<b>Delirium</b> is an acute disturbance of attention and awareness caused by a medical problem (infection, drugs, metabolic "
        "changes, hypoxia, a brain lesion). It starts over hours to days, <b>fluctuates</b> during the day, impairs <b>attention</b> "
        "(cannot name days or months backward) and often the level of consciousness (drowsy or agitated), and is often reversible when "
        "the cause is found and treated. It is a medical emergency. This client's 10-day course, fluctuation and inattention point to "
        "delirium.",
        "<b>Dementia</b> (major neurocognitive disorder) is a gradual, progressive decline in memory and other cognitive functions severe "
        "enough to interfere with daily life, caused by the loss of neurons. Attention and alertness are preserved until late stages. "
        "People with dementia (or Parkinson disease) are at higher risk of delirium, and the two can coexist.",
        "<b>Types of dementia:</b> <b>Alzheimer disease</b> (about 60% or more: beta-amyloid plaques, neurofibrillary tangles of tau, "
        "loss of acetylcholine neurons, starting with memory loss). <b>Vascular dementia</b> (multiple infarcts or small-vessel disease; "
        "often a stepwise decline). <b>Lewy body dementia</b> (Lewy bodies in the cortex: fluctuating cognition, visual hallucinations, "
        "parkinsonism and severe sensitivity to antipsychotics). <b>Parkinson disease dementia</b> (develops a year or more after "
        "established Parkinson motor symptoms). <b>Frontotemporal dementia</b> (often before age 65; personality, behaviour or language "
        "change before memory loss)."),
})

# ---------------------------------------------------------------- Screen 3: drop-down cloze (prioritize)
C.notes("dx", "Diagnostic Results",
    ("Day 1 1500", "<b>Urinalysis:</b> negative for nitrites and leukocyte esterase."),
    ("Day 1 1530", "<b>Non-contrast head CT:</b> right frontoparietal crescent-shaped collection, 18 mm thick, mostly low density with a "
     "small area of new blood, consistent with a chronic subdural hematoma with an acute component; 7-mm midline shift to the left. "
     "Generalized brain atrophy."))
C.labs("Day 1 1500", [
    (lab("Sodium (Na)", "136–146 mmol/L"), "139 mmol/L"),
    (lab("Glucose, random", "4.0–11.0 mmol/L"), "6.4 mmol/L"),
    (lab("White blood cell (WBC) count", "3.5–10.5 × 10<sup>9</sup>/L"), "7.2 × 10<sup>9</sup>/L"),
    (lab("Hemoglobin (Hgb)", "Male: 125–170 g/L"), "131 g/L"),
    (lab("Creatine kinase (CK)", "Male: 30–250 IU/L"), "180 IU/L"),
])
s3 = screen(3, INTRO, C, {
    "type": "dropdown_cloze",
    "preamble": "The nurse has reviewed the Diagnostic Results and the Laboratory Results.",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {
        "text": "The client's acute confusion is most likely [[drop0]] caused by [[drop1]]. This type of bleed comes from [[drop2]], and his "
                "risk was increased by [[drop3]].",
        "dropdowns": [
            dropdown(("Alzheimer disease", False), ("delirium", True), ("progression of Parkinson disease dementia", False),
                     ("depression", False), seed="u7c6-d0"),
            dropdown(("an acute ischemic stroke", False), ("a urinary tract infection", False),
                     ("a chronic subdural hematoma", True), ("an epidural hematoma", False), seed="u7c6-d1"),
            dropdown(("torn bridging veins", True), ("a torn middle meningeal artery", False), ("a ruptured berry aneurysm", False),
                     ("a bleeding brain tumor", False), seed="u7c6-d2"),
            dropdown(("his levodopa therapy", False), ("brain atrophy, frequent falls, and anticoagulant therapy", True),
                     ("a high fluid intake", False), ("his cataract surgery", False), seed="u7c6-d3"),
        ],
    },
    "explanation": rationale(
        "<b>Delirium caused by a chronic subdural hematoma:</b> the CT shows a crescent-shaped collection over the right hemisphere with a "
        "midline shift, which explains the confusion, drowsiness, headaches and the <b>left</b> (opposite-side) arm weakness. The normal "
        "urinalysis, sodium, glucose and WBC make infection or a metabolic cause unlikely.",
        "<b>How it develops:</b> <b>bridging veins</b> cross from the brain surface to the dural sinuses. With age the brain shrinks "
        "(<b>atrophy</b>), stretching these veins, so a minor blow, such as his fall 4 weeks ago, can tear them. Low-pressure venous "
        "bleeding collects slowly between the dura and the arachnoid; the clot breaks down and may rebleed (the new blood on CT), and "
        "symptoms appear weeks later. <b>Anticoagulants</b> (apixaban) and <b>falls</b> (Parkinson disease, orthostatic hypotension) "
        "greatly raise the risk.",
        "<b>Why not the others:</b> an arterial (middle meningeal) bleed causes an epidural hematoma with rapid deterioration; a "
        "ruptured aneurysm causes a subarachnoid hemorrhage. Alzheimer disease and Parkinson disease dementia progress over years, not "
        "days."),
})

# ---------------------------------------------------------------- Screen 4: matrix indicated / contraindicated (generate solutions)
C.notes("ord", "Provider Orders",
    ("Day 1 1630", "Admit to neurosurgery. Hold apixaban. Burr-hole drainage of the subdural hematoma planned for Day 2 at 0800; NPO "
     "after midnight except medications with sips of water.<br>"
     "Carbidopa-levodopa 25/100 mg, 2 tablets PO at 0700, 1100, 1500 and 1900.<br>"
     "Neurological checks every 2 hours. Fall precautions; bed alarm.<br>"
     "Haloperidol 0.5 mg IV every 4 hours PRN for agitation."))
s4 = screen(4, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Provider Orders.",
    "stem": "For each intervention, click to specify whether it is <b>indicated</b> or <b>contraindicated</b> for the client.",
    "matrix": matrix_mc("Intervention", ["Indicated", "Contraindicated"], [
        ("Give the carbidopa-levodopa at the exact scheduled times, including while he is NPO", 0),
        ("Give the PRN haloperidol if he becomes agitated", 1),
        ("Reorient him with a clock and calendar, his glasses and hearing aids, and his wife's presence", 0),
        ("Apply wrist restraints at night so he does not get out of bed", 1),
        ("Have him sit and dangle his legs before standing, with assistance", 0),
        ("Keep the room brightly lit and the television on all night to keep him oriented", 1),
        ("Perform the ordered neurological checks, including pupils and arm strength", 0),
    ]),
    "explanation": rationale(
        "<b>Indicated:</b> levodopa has a short half-life; late or missed doses quickly cause severe rigidity, immobility, swallowing "
        "problems and falls, so Parkinson medications are given <b>on time</b>, even when NPO (with sips of water, as ordered). "
        "Non-drug delirium measures come first: reorientation, sensory aids, family presence, a normal sleep-wake cycle, mobility and "
        "hydration. Dangling before standing reduces falls from orthostatic hypotension. Neurological checks detect expansion of the "
        "hematoma (falling level of consciousness, a dilated pupil, worsening left-sided weakness).",
        "<b>Contraindicated:</b> <b>haloperidol</b> and other dopamine-blocking drugs (for example, metoclopramide) worsen Parkinson "
        "disease and can cause severe, even fatal, reactions in Lewy body disease; the nurse questions the order. Restraints increase "
        "agitation, delirium, injury and falls. Bright light and noise all night disrupt sleep and worsen delirium."),
})

# ---------------------------------------------------------------- Screen 5: select all (take action)
C.notes("nn", "Nurses' Notes",
    ("Day 2 1400", "Surgery postponed to 1600 because of an emergency case. The 0700 and 1100 carbidopa-levodopa doses were not given "
     "because the client was NPO. Client now rigid throughout and unable to turn in bed or swallow his saliva well; more confused; "
     "skin hot and sweaty. Pupils equal and reactive; left arm drift unchanged."))
C.vitals("Day 2 1400", vs("38.8° C", "118 beats/min, irregular", "22 breaths/min", "162/90 mm Hg", "95% on room air"))
C.labs("Day 2 1415", [
    (lab("Sodium (Na)", "136–146 mmol/L"), "144 mmol/L"),
    (lab("Glucose, random", "4.0–11.0 mmol/L"), "7.1 mmol/L"),
    (lab("White blood cell (WBC) count", "3.5–10.5 × 10<sup>9</sup>/L"), "9.8 × 10<sup>9</sup>/L"),
    (lab("Hemoglobin (Hgb)", "Male: 125–170 g/L"), "134 g/L"),
    (lab("Creatine kinase (CK)", "Male: 30–250 IU/L"), "2,850 IU/L"),
])
s5 = screen(5, INTRO, C, {
    "type": "select_all",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 2 1400, the Vital Signs from Day 2 1400 and the Laboratory Results "
                "from Day 2 1415.",
    "stem": "Which actions should the nurse take? <b>Select all that apply.</b>",
    "options": opts(
        ("Notify the provider of the missed doses and the client's condition", True),
        ("Give the PRN haloperidol for the increased confusion", False),
        ("Ask the provider how to give the carbidopa-levodopa now (for example, by nasogastric tube)", True),
        ("Continue to hold the carbidopa-levodopa until after surgery", False),
        ("Apply cooling measures", True),
        ("Encourage him to drink water to cool down", False),
        ("Monitor urine output and colour", True),
        seed="u7c6-s5"),
    "explanation": rationale(
        "Missing two levodopa doses has caused <b>parkinsonism-hyperpyrexia syndrome</b> (acute levodopa withdrawal), which resembles "
        "neuroleptic malignant syndrome: severe rigidity, fever, tachycardia, labile BP, sweating, confusion and a high <b>creatine "
        "kinase</b> from muscle breakdown (rhabdomyolysis, which can cause acute kidney injury). It can be fatal.",
        "<b>Correct:</b> notify the provider at once. Restarting dopaminergic therapy is the key treatment; because he cannot swallow "
        "safely, the provider may order the tablets crushed through a nasogastric tube. Cool him (fever raises brain metabolism and "
        "ICP). Watch urine output and colour (tea-coloured urine suggests myoglobin) and give IV fluids as ordered.",
        "<b>Incorrect:</b> haloperidol blocks dopamine and would worsen the syndrome. Continuing to hold levodopa prolongs it; NPO orders "
        "for surgery allow Parkinson medications with sips of water or another route. He cannot swallow his saliva safely, so drinking "
        "water would risk aspiration."),
})

# ---------------------------------------------------------------- Screen 6: matrix (evaluate)
C.notes("nn", "Nurses' Notes",
    ("Day 3 0900", "Levodopa restarted by NG tube at 1530 on Day 2; rigidity and fever settled overnight. Burr-hole drainage of the "
     "subdural hematoma done at 0730 today. CK falling."),
    ("Day 8 1000", "Alert, oriented, attentive (names the months backward). Headache gone; left arm strength equal to the right. Taking "
     "carbidopa-levodopa on time by mouth. Discharge home tomorrow with a home care referral. Apixaban to stay on hold until the "
     "neurosurgery follow-up. The nurse reviews the discharge teaching with the client and his wife."))
C.vitals("Day 8 1000", vs("36.8° C", "76 beats/min, irregular", "16 breaths/min", "132/76 mm Hg", "96% on room air"))
s6 = screen(6, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 3 0900 and Day 8 1000 and the Vital Signs from Day 8 1000.",
    "stem": "For each statement, click to specify whether it indicates an <b>understanding</b> of the teaching or a <b>need for further "
            "teaching</b>.",
    "matrix": matrix_mc("Statement", ["Understanding", "Needs further teaching"], [
        ("Wife: “His confusion cleared once the blood was drained, so it was delirium, not dementia.”", 0),
        ("Client: “I'll take my levodopa with my high-protein breakfast to settle my stomach.”", 1),
        ("Wife: “If he gets a new headache or becomes sleepy or confused again, I'll take him to emergency.”", 0),
        ("Client: “Now that my head is better, I can restart my apixaban tonight.”", 1),
        ("Wife: “His mother had Alzheimer disease, so his confusion means he has it too.”", 1),
        ("Wife: “I'll remove the throw rugs and keep a night light on.”", 0),
        ("Wife: “If he is in hospital again, I'll ask that his Parkinson pills be given on time.”", 0),
    ]),
    "explanation": rationale(
        "<b>Understanding:</b> the confusion was delirium from the hematoma, and it resolved when the cause was treated. A chronic "
        "subdural hematoma can recur (in about 1 in 10 clients), so new headache, drowsiness, confusion or weakness need prompt "
        "assessment. Removing rugs and using a night light reduce falls. Insisting that Parkinson medications are given on time in "
        "hospital prevents the problem that occurred on Day 2.",
        "<b>Needs further teaching:</b> dietary protein (amino acids) competes with levodopa for absorption and transport into the brain; "
        "levodopa is best taken about 30 minutes before meals, or with a low-protein snack if it causes nausea, and protein is spread "
        "through the day. Apixaban is restarted only when neurosurgery says it is safe. Delirium does not mean Alzheimer disease; a "
        "family history raises risk slightly, but his cognition has returned to normal."),
})

write_case(6,
    "76-year-old male client with Parkinson disease taking apixaban who develops delirium from a chronic subdural hematoma weeks after a "
    "fall: Parkinson disease vs ALS and MS findings, delirium vs dementia and the types of dementia, bridging-vein bleeding, "
    "delirium-safe care, levodopa withdrawal (parkinsonism-hyperpyrexia syndrome), and discharge teaching.",
    [s1, s2, s3, s4, s5, s6],
    ["- Learning outcomes: Parkinson disease pathophysiology (ALS and MS as contrasts), delirium vs dementia, types of dementia, "
     "subdural hematoma.",
     "- Screen 5 tests parkinsonism-hyperpyrexia syndrome (levodopa withdrawal); please confirm this depth suits the course.",
     "- Clinician review: haloperidol order used as an unsafe order to question; recurrence rate of chronic subdural hematoma."],
    "Parkinson_Subdural")
