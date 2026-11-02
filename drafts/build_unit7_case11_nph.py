"""NURS 1017 Unit 7 Case Study 11: normal pressure hydrocephalus (NPH) and a ventriculoperitoneal (VP) shunt.

Nursing focus: recognizing the gait, continence and cognitive changes of NPH; telling them apart from dementia and Parkinson
disease; falls and continence priorities; care after VP shunt insertion (neurological checks, incision and shunt tract, abdomen,
positioning, mobility); recognizing shunt malfunction at home; teaching (programmable valve and MRI/magnets) and evaluation.
Learning outcome: types of hydrocephalus (non-communicating/obstructive, communicating, normal pressure as a communicating type).
Sources checked: OpenStax Medical-Surgical Nursing 17.1 (CSF drainage problems treated with a VP shunt, external ventricular drain or
lumbar drain; nursing care for increased ICP) and 17.4 (major neurocognitive disorder); Lewis's Medical-Surgical Nursing in Canada
(hydrocephalus, shunts); Hydrocephalus Canada patient information on programmable valves.
"""
from unit7_common import (NeuroChart, vs, opts, dropdown, matrix_mc, rationale, highlight_tab, screen, write_case)

INTRO = "The nurse in a neurology clinic is caring for a 74-year-old female client who is accompanied by her daughter."
C = NeuroChart()

# ---------------------------------------------------------------- Screen 1: highlight (recognize)
S1 = [("Day 1 0930", "Daughter reports that over the past 8 months her mother has {started walking with short, shuffling steps, feet "
       "wide apart, “as if her feet are stuck to the floor”|correct}, and has {fallen twice at home|correct}. She has {urgency and "
       "has wet herself several times; now wears pads|correct}. She has become {slower to answer and less interested in her usual "
       "activities, and forgets appointments|correct}. Client is alert and oriented × 3. {Wears hearing aids in both ears}. {Had "
       "cataract surgery 3 years ago}. {No tremor at rest}. {Reports no headache}. Timed Up and Go test: {28 seconds|correct} "
       "(more than 12 seconds indicates a high fall risk). Lives alone in a two-storey house; daughter visits daily.")]
C.notes("nn", "Nurses' Notes", *S1)
C.vitals("Day 1 0930", vs("36.6° C", "72 beats/min", "16 breaths/min", "134/78 mm Hg", "97% on room air"))
s1 = screen(1, INTRO, C, {
    "type": "highlight",
    "stem": "The nurse reviews the Nurses' Notes. <b>Highlight</b> the findings that require follow-up.",
    "options": [],
    "highlightTabs": [highlight_tab("ht1", "Nurses' Notes", S1)],
    "maxCorrectSelections": None,
    "explanation": rationale(
        "<b>Require follow-up:</b> a shuffling, wide-based, “magnetic” gait, two falls and a Timed Up and Go of 28 seconds (high fall "
        "risk, especially living alone on two floors); new urinary urgency and incontinence; and slowed thinking, apathy and "
        "forgetfulness. Together these are the classic <b>triad of normal pressure hydrocephalus</b>: gait disturbance, urinary "
        "incontinence and cognitive decline.",
        "<b>Do not require follow-up now:</b> hearing aids and past cataract surgery are part of her history (the nurse checks that "
        "they are working, since poor hearing and vision add to fall risk). No resting tremor and no headache are pertinent negatives: "
        "they make Parkinson disease and a raised-pressure problem less likely."),
})

# ---------------------------------------------------------------- Screen 2: matrix (analyze)
C.notes("dx", "Diagnostic Results",
    ("Day 1 1100", "<b>MRI brain:</b> enlarged lateral and third ventricles, out of proportion to the mild brain atrophy; no blockage of "
     "CSF flow. Consistent with normal pressure hydrocephalus."),
    ("Day 1 1300", "<b>Lumbar tap test:</b> opening pressure 14 cm H₂O; 40 mL of CSF removed. Timed Up and Go 3 hours later: 17 seconds "
     "(was 28 seconds); steps longer and more confident."))
s2 = screen(2, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Diagnostic Results.",
    "stem": "The daughter asks whether her mother has dementia or Parkinson disease. For each finding, click to specify whether it is "
            "most consistent with <b>normal pressure hydrocephalus</b>, <b>Alzheimer disease</b>, or <b>Parkinson disease</b>.",
    "matrix": matrix_mc("Finding", ["Normal pressure hydrocephalus", "Alzheimer disease", "Parkinson disease"], [
        ("Walking improves after some CSF is removed by lumbar puncture", 0),
        ("Memory loss is the first problem; walking stays normal until late in the disease", 1),
        ("Resting tremor, rigidity, and slow movement", 2),
        ("Wide-based, “magnetic” gait with urinary incontinence early in the illness", 0),
        ("Enlarged ventricles with no blockage of CSF flow", 0),
        ("Gradual loss of recent memory, getting lost in familiar places, and repeating questions", 1),
    ]),
    "explanation": rationale(
        "<b>Normal pressure hydrocephalus (NPH):</b> CSF builds up in the ventricles because it is not absorbed well, but the pressure "
        "measured by lumbar puncture is normal or only slightly raised. The enlarged ventricles stretch the nerve fibres that run past "
        "them to the legs and bladder and frontal lobes, causing the gait, bladder and thinking changes. Improvement after removing CSF "
        "(tap test) suggests she will benefit from a shunt. NPH is one of the few <b>treatable</b> causes of cognitive decline, which "
        "is why recognizing it matters.",
        "<b>Alzheimer disease</b> begins with memory loss; gait and continence stay normal until late. <b>Parkinson disease</b> causes "
        "a resting tremor, rigidity, bradykinesia and a shuffling, narrow-based gait.",
        "<b>Types of hydrocephalus:</b> <b>non-communicating (obstructive)</b>, when CSF flow is blocked inside the ventricular system "
        "(for example, a narrowed cerebral aqueduct or a tumour); <b>communicating (non-obstructive)</b>, when CSF flows freely but is "
        "not absorbed by the arachnoid villi (for example, after meningitis or a subarachnoid hemorrhage); and <b>normal pressure "
        "hydrocephalus</b>, a form of communicating hydrocephalus in older adults."),
})

# ---------------------------------------------------------------- Screen 3: drop-down cloze (prioritize)
s3 = screen(3, INTRO, C, {
    "type": "dropdown_cloze",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {
        "text": "Until her shunt surgery, the nurse's priority problem for the client is [[drop0]], because she [[drop1]]. The nurse "
                "also addresses [[drop2]], which can increase her risk of falling at night.",
        "dropdowns": [
            dropdown(("risk for falls", True), ("disturbed sensory perception", False), ("social isolation", False),
                     ("risk for infection", False), seed="u7c11-d0"),
            dropdown(("wears hearing aids", False), ("has a magnetic gait, has fallen twice, and lives alone on two floors", True),
                     ("had cataract surgery", False), ("has a normal blood pressure", False), seed="u7c11-d1"),
            dropdown(("her urinary urgency", True), ("her hearing aids", False), ("her lack of headache", False),
                     ("her daughter's daily visits", False), seed="u7c11-d2"),
        ],
    },
    "explanation": rationale(
        "<b>Risk for falls</b> is the priority: a fall could cause a hip fracture or head injury (and older adults with enlarged "
        "ventricles are at risk of subdural bleeding). Her gait, two recent falls, a slow Timed Up and Go and living alone on two floors "
        "make a fall likely.",
        "<b>Urinary urgency</b> sends her rushing to the bathroom, often at night, which is a common time for falls. A toileting "
        "schedule, a night light, a commode near the bed and grab bars reduce both incontinence and falls. Her slowed thinking makes "
        "it harder for her to remember safety measures, so her daughter is included in the plan."),
})

# ---------------------------------------------------------------- Screen 4: select all (generate solutions)
C.notes("nn", "Nurses' Notes",
    ("Day 15 1500", "Admitted to the neurosurgical unit after insertion of a right ventriculoperitoneal (VP) shunt with a programmable "
     "valve behind the right ear. Small incisions on the right side of the head and on the abdomen. Alert and oriented × 3; pupils "
     "equal and reactive; moves all limbs equally."))
C.notes("ord", "Provider Orders",
    ("Day 15 1500", "Neurological checks every 2 hours for 24 hours, then every 4 hours.<br>"
     "Head of bed 30 degrees for 24 hours, then as tolerated.<br>"
     "Up with assistance this evening; physiotherapy Day 16.<br>"
     "Do not pump the shunt valve.<br>"
     "Acetaminophen 650 mg PO every 6 hours PRN for pain."))
s4 = screen(4, INTRO, C, {
    "type": "select_all",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 15 1500 and the Provider Orders.",
    "stem": "Which interventions should the nurse include in the client's plan of care after shunt insertion? <b>Select all that "
            "apply.</b>",
    "options": opts(
        ("Compare each neurological check with her baseline before surgery", True),
        ("Inspect the head and abdominal incisions and the skin along the shunt tract for redness, swelling or drainage", True),
        ("Press the shunt valve behind her ear every hour to keep it working", False),
        ("Assess the abdomen for pain, distension and bowel sounds", True),
        ("Have her lie on her right side so the valve stays warm", False),
        ("Walk with her using a gait belt, and offer the toilet every 2 hours", True),
        ("Restrict her fluid intake to reduce CSF production", False),
        ("Include her daughter in teaching about the shunt", True),
        seed="u7c11-s4"),
    "explanation": rationale(
        "<b>Include:</b> comparing neurological checks with her baseline detects early problems (bleeding, shunt malfunction). The "
        "incisions and the tunnelled path of the tubing under the skin (head, neck, chest, abdomen) are checked for infection or CSF "
        "leakage. The lower end of the shunt drains into the peritoneal cavity, so abdominal pain, distension or absent bowel sounds "
        "are reported. Early, assisted walking and scheduled toileting address her fall risk and urgency. Her daughter will help "
        "watch for problems at home.",
        "<b>Do not include:</b> the valve is pumped only if the neurosurgeon orders it. Lying on the valve side puts pressure on the "
        "incision and valve; she is positioned off the operative side as ordered. Fluid restriction does not change CSF production and "
        "risks dehydration, constipation and delirium."),
})

# ---------------------------------------------------------------- Screen 5: select all (take action)
C.notes("nn", "Nurses' Notes",
    ("Week 6 1100", "Home care visit. Daughter says her mother walked much better for the first 4 weeks after surgery, but over the last "
     "3 days she has been sleepy, has vomited twice this morning, has a headache, and is shuffling again and incontinent. Today she is "
     "drowsy but rousable and oriented to person only. Pupils equal and reactive. Incisions healed, no redness. Two days ago she had "
     "an MRI of her knee at the hospital; daughter is not sure whether the shunt valve was checked afterwards."))
C.vitals("Week 6 1100", vs("36.9° C", "64 beats/min", "16 breaths/min", "152/80 mm Hg", "96% on room air"))
s5 = screen(5, INTRO, C, {
    "type": "select_all",
    "preamble": "The nurse has reviewed the Nurses' Notes from Week 6 1100 and the Vital Signs from Week 6 1100.",
    "stem": "Which actions should the nurse take? <b>Select all that apply.</b>",
    "options": opts(
        ("Contact the neurosurgery team now and arrange urgent transport to the emergency department", True),
        ("Tell the daughter to watch her mother and call if she is not better in a few days", False),
        ("Tell the emergency team about the recent MRI and the programmable valve", True),
        ("Give her a large meal to settle her stomach before she leaves", False),
        ("Perform and document a full neurological assessment", True),
        ("Press the shunt valve several times to restart the drainage", False),
        ("Keep her lying down with the head of the bed raised and stay with her until transport arrives", True),
        seed="u7c11-s5"),
    "explanation": rationale(
        "Return of her gait, bladder and thinking problems with new drowsiness, headache, vomiting, a slower pulse and a higher BP "
        "suggests <b>shunt malfunction</b> with rising pressure. Here the MRI may have changed the setting of her programmable valve "
        "(the magnet of an MRI scanner can reset some valves).",
        "<b>Correct:</b> shunt malfunction is urgent: the neurosurgery team is contacted and she is assessed in hospital (valve setting "
        "check, imaging). The nurse reports the MRI and the valve type. A full neurological assessment gives a baseline for the "
        "emergency team. Keeping her in bed with the head raised and staying with her prevents falls and aspiration if she vomits.",
        "<b>Incorrect:</b> waiting risks a serious decline. She is vomiting and drowsy, so she is not given food (aspiration risk, and "
        "she may need a procedure). The nurse does not pump the valve without an order."),
})

# ---------------------------------------------------------------- Screen 6: matrix (evaluate)
C.notes("nn", "Nurses' Notes",
    ("Week 6 1700", "In the emergency department, the valve setting was found to have changed after the MRI; it was reset by the "
     "neurosurgeon. Drowsiness, headache and vomiting resolved overnight."),
    ("Month 3 1000", "Clinic follow-up. Timed Up and Go 14 seconds; no falls since surgery. Continent with a toileting schedule. "
     "Daughter says her mother is “more like herself” and has started her book club again. The nurse reviews the teaching with the "
     "client and her daughter."))
s6 = screen(6, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Week 6 1700 and Month 3 1000.",
    "stem": "For each statement, click to specify whether it indicates an <b>understanding</b> of the teaching or a <b>need for "
            "further teaching</b>.",
    "matrix": matrix_mc("Statement", ["Understanding", "Needs further teaching"], [
        ("Daughter: “Before any MRI, we'll tell the staff she has a programmable shunt so the setting can be checked afterwards.”", 0),
        ("Client: “Now that I have the shunt, I don't need my walker or the grab bars any more.”", 1),
        ("Daughter: “If she gets sleepy, has headaches or vomiting, or her walking gets worse again, we'll call neurosurgery right away.”",
         0),
        ("Daughter: “Redness or fluid along the tubing, a fever, or pain in her belly needs to be reported.”", 0),
        ("Client: “The shunt is permanent, so I won't need any more check-ups.”", 1),
        ("Client: “I'll carry the card that says what kind of shunt valve I have.”", 0),
    ]),
    "explanation": rationale(
        "<b>Understanding:</b> programmable valves can be changed by strong magnets (MRI, some magnetic toys or devices held to the "
        "head), so staff must know and the setting is checked after an MRI. Return of NPH symptoms, drowsiness, headache or vomiting "
        "can mean shunt malfunction; fever, redness or fluid along the tubing, or abdominal pain can mean infection. A shunt card gives "
        "emergency staff the valve details.",
        "<b>Needs further teaching:</b> her walking has improved, but she should keep using her walker and home safety measures until "
        "physiotherapy advises otherwise; falls remain a risk. A shunt needs lifelong follow-up because it can block, break, become "
        "infected or drain too much or too little."),
})

write_case(11,
    "74-year-old female client with normal pressure hydrocephalus: recognizing the gait, continence and thinking changes, telling them "
    "apart from Alzheimer and Parkinson disease, the types of hydrocephalus, falls and continence priorities, care after a "
    "ventriculoperitoneal shunt, recognizing shunt malfunction at home after an MRI, and teaching about a programmable valve.",
    [s1, s2, s3, s4, s5, s6],
    ["- Nursing-focused case (falls, continence, shunt care and teaching); covers the hydrocephalus learning outcome.",
     "- Clinician review: shunt positioning orders, the MRI and programmable-valve scenario, Timed Up and Go cut-off (12 seconds)."],
    "Hydrocephalus")
