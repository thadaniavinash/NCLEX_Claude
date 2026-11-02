"""NURS 1017 Unit 7 Case Study 7: transient ischemic attack (TIA) recognized at a community health clinic.

Nursing focus (second set of Unit 7 cases, user request 2 Nov 2026: follow the OpenStax nursing care structure, less medical):
recognizing stroke warning signs that have resolved, last known well, urgent referral, modifiable and non-modifiable risk factors,
teaching for secondary prevention (FAST, anticoagulant safety, lifestyle), and evaluation of outcomes.
Sources checked: OpenStax Medical-Surgical Nursing 15.2 (TIA: temporary blockage that clears, 90-day stroke risk nearly 18%; risk
factor modification; secondary prevention) ; Heart & Stroke Foundation of Canada FAST; Canadian Stroke Best Practice
Recommendations (TIA with motor or speech symptoms within 48 hours = highest risk, immediate emergency department assessment).
"""
from unit7_common import (NeuroChart, vs, opts, dropdown, matrix_mc, rationale, highlight_tab, screen, write_case)

INTRO = "The nurse at a community health clinic is caring for a 64-year-old female client who has come in for a blood pressure check."
C = NeuroChart()

# ---------------------------------------------------------------- Screen 1: highlight (recognize)
S1 = [("1030", "Client mentions that at about 0730 this morning, while brushing her teeth, {her right hand suddenly went numb and weak "
       "and she dropped her toothbrush|correct}, and {her words came out jumbled for about 15 minutes|correct}; then she felt “back "
       "to normal.” She did not call anyone. {Alert and oriented × 4}; {speech clear}; {smile symmetrical}; {hand grips equal "
       "and strong}. She {stopped taking her amlodipine 2 months ago because of ankle swelling|correct} and did not tell her provider. "
       "{Smokes 1 pack of cigarettes per day|correct}. Has type 2 diabetes managed with metformin; {capillary glucose 7.8 mmol/L}. {Brought her grandson to "
       "the clinic for his immunizations}.")]
S1_VS = [("1030", "{T 36.8° C}, {P 92 beats/min, irregular|correct}, {RR 16 breaths/min}, {BP 172/96 mm Hg|correct}, "
          "{SpO₂ 97% on room air}.")]
C.notes("nn", "Nurses' Notes", *S1)
C.vitals("1030", vs("36.8° C", "92 beats/min, irregular", "16 breaths/min", "172/96 mm Hg", "97% on room air"))
s1 = screen(1, INTRO, C, {
    "type": "highlight",
    "stem": "The nurse reviews the Nurses' Notes and the Vital Signs. <b>Highlight</b> the findings that require follow-up.",
    "options": [],
    "highlightTabs": [highlight_tab("ht1", "Nurses' Notes", S1), highlight_tab("ht2", "Vital Signs", S1_VS)],
    "maxCorrectSelections": None,
    "explanation": rationale(
        "<b>Require follow-up:</b>",
        "<b>Sudden one-sided hand weakness and numbness with jumbled speech that cleared in 15 minutes:</b> these are stroke warning "
        "signs. Even though they have gone, the nurse treats them as a possible transient ischemic attack (TIA) and records when "
        "they started and stopped (last known well: before 0730).",
        "<b>Irregular pulse:</b> may be atrial fibrillation, a common source of clots that travel to the brain; the nurse counts the "
        "apical pulse for a full minute and reports it.",
        "<b>BP 172/96 mm Hg after stopping amlodipine:</b> uncontrolled hypertension is the most important modifiable stroke risk "
        "factor. Stopping a medication because of a side effect without telling the provider is a teaching need.",
        "<b>Smoking:</b> a modifiable risk factor that damages blood vessels and makes blood clot more easily.",
        "<b>Do not require follow-up now:</b> her normal neurological assessment today (alert, clear speech, symmetrical smile, equal "
        "grips), temperature, respirations, oxygen saturation and capillary glucose. A normal glucose also rules out hypoglycemia as the "
        "cause of the episode."),
})

# ---------------------------------------------------------------- Screen 2: matrix (analyze)
C.html("hx", "Health History",
    "<p><b>Medical history:</b> hypertension (8 years), type 2 diabetes (5 years; last HbA1c 8.6%), obesity (BMI 33).</p>"
    "<p><b>Family history:</b> father had a stroke at age 70.</p>"
    "<p><b>Social history:</b> lives with her daughter's family; cares for her grandson after school. Smokes 1 pack per day for 40 "
    "years. Walks “only to the bus stop.” Eats take-out meals 4 to 5 times a week.</p>"
    "<p><b>Medications:</b> metformin 1,000 mg PO twice daily; amlodipine 10 mg PO daily (stopped 2 months ago).</p>")
s2 = screen(2, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Health History.",
    "stem": "The nurse identifies the client's risk factors for stroke. For each risk factor, click to specify whether it is "
            "<b>modifiable</b> or <b>non-modifiable</b>.",
    "matrix": matrix_mc("Risk Factor", ["Modifiable", "Non-modifiable"], [
        ("Hypertension", 0),
        ("Age 64 years", 1),
        ("Smoking 1 pack per day", 0),
        ("Father had a stroke", 1),
        ("Physical inactivity", 0),
        ("Type 2 diabetes with an HbA1c of 8.6%", 0),
        ("A previous TIA (today's episode)", 1),
        ("Possible atrial fibrillation", 0),
    ]),
    "explanation": rationale(
        "<b>Why risk factors matter after a TIA:</b> a TIA is a temporary blockage of blood flow to part of the brain; the clot clears "
        "on its own, so the symptoms resolve without permanent damage. It is a warning: the risk of a stroke in the next 90 days is high "
        "(about 18%), and it is greatest in the first 48 hours. Teaching aims at the factors the client can change.",
        "<b>Modifiable</b> (can be treated or changed): hypertension, smoking, physical inactivity, diabetes (glucose control), obesity, "
        "unhealthy diet, high cholesterol, heavy alcohol use, sleep apnea, and atrial fibrillation (treated with anticoagulation and "
        "rate control).",
        "<b>Non-modifiable:</b> age, family history, sex, race and ethnicity, and a previous stroke or TIA. These cannot be changed, but "
        "they raise the client's overall risk, so the modifiable factors matter even more."),
})

# ---------------------------------------------------------------- Screen 3: drop-down cloze (prioritize)
s3 = screen(3, INTRO, C, {
    "type": "dropdown_cloze",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {
        "text": "The client's episode is most consistent with [[drop0]]. The nurse's priority is the client's [[drop1]], so the nurse "
                "[[drop2]].",
        "dropdowns": [
            dropdown(("a hypoglycemic reaction", False), ("a transient ischemic attack", True), ("a migraine", False),
                     ("anxiety", False), seed="u7c7-d0"),
            dropdown(("knowledge of a healthy diet", False), ("high risk of a stroke in the next few days", True),
                     ("ankle swelling from amlodipine", False), ("need for a smoking cessation plan", False), seed="u7c7-d1"),
            dropdown(("books a follow-up appointment with her primary care provider next week", False),
                     ("arranges for her to be assessed in an emergency department today", True),
                     ("restarts her amlodipine from her supply at home", False),
                     ("teaches her to rest and call the clinic if the symptoms return", False), seed="u7c7-d2"),
        ],
    },
    "explanation": rationale(
        "<b>Transient ischemic attack:</b> sudden focal symptoms (one-sided weakness and numbness, speech disturbance) that resolved "
        "completely within minutes, with a normal glucose, fit a TIA rather than hypoglycemia, migraine or anxiety.",
        "<b>Priority:</b> the risk of a disabling stroke is highest in the first 48 hours after a TIA, especially when the symptoms "
        "included weakness or speech problems. Canadian stroke guidelines direct these clients to an emergency department <b>the same "
        "day</b> for brain and vessel imaging, an ECG for atrial fibrillation, and prompt preventive treatment. Diet, smoking and the "
        "medication side effect are all important, but they come after this immediate safety need.",
        "<b>Why not the others:</b> waiting a week for an appointment loses the window when preventive treatment helps most. "
        "Restarting a medication is a provider decision. Telling her to call the clinic delays care; if symptoms return, she calls "
        "9-1-1."),
})

# ---------------------------------------------------------------- Screen 4: select all (generate solutions)
s4 = screen(4, INTRO, C, {
    "type": "select_all",
    "stem": "The provider agrees that the client should go to the emergency department now. Which actions should the nurse include "
            "before she leaves the clinic? <b>Select all that apply.</b>",
    "options": opts(
        ("Tell her she should not drive herself to the emergency department", True),
        ("Write down the time the symptoms started and when they resolved", True),
        ("Give her an aspirin from the clinic supply to take on the way", False),
        ("Teach her and her daughter the FAST signs of stroke and to call 9-1-1 if any return", True),
        ("Send a list of her medications, including the amlodipine she stopped", True),
        ("Reassure her that no further testing is needed because her symptoms are gone", False),
        ("Phone a report to the emergency department nurse", True),
        ("Ask her to come back to the clinic tomorrow if she still feels well", False),
        seed="u7c7-s4"),
    "explanation": rationale(
        "<b>Include:</b> a new neurological event can recur on the way, so she does not drive. The times of onset and resolution guide "
        "the emergency team (and would determine eligibility for clot-dissolving treatment if a stroke followed). <b>FAST</b> (Heart & "
        "Stroke Foundation of Canada): <b>F</b>ace drooping, <b>A</b>rm weakness (cannot raise both arms), <b>S</b>peech jumbled or "
        "slurred, <b>T</b>ime to call 9-1-1 right away; she and her family must not wait to see whether symptoms pass. A medication list "
        "and a nurse-to-nurse report support safe handover of care.",
        "<b>Do not include:</b> aspirin is not given until a hemorrhage has been ruled out and a provider prescribes it. Resolved "
        "symptoms do not mean she is safe; she needs assessment today. Waiting until tomorrow delays care in the highest-risk period."),
})

# ---------------------------------------------------------------- Screen 5: matrix (take action)
C.notes("nn", "Nurses' Notes",
    ("Day 4 1000", "Client returns to the clinic after 1 night in hospital. Diagnosis: TIA; ECG showed atrial fibrillation. CT and CT "
     "angiography showed no stroke and no carotid narrowing. New medications: apixaban 5 mg PO twice daily, perindopril 4 mg PO daily "
     "(replaces amlodipine), atorvastatin 40 mg PO daily. Referral to the stroke prevention clinic in 2 weeks. She asks the nurse to "
     "“go over the new pills and what I need to change.”"))
C.vitals("Day 4 1000", vs("36.7° C", "84 beats/min, irregular", "16 breaths/min", "148/88 mm Hg", "97% on room air"))
s5 = screen(5, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 4 1000 and the Vital Signs from Day 4 1000.",
    "stem": "For each teaching point, click to specify whether the nurse should <b>include</b> it or <b>not include</b> it in the "
            "client's teaching.",
    "matrix": matrix_mc("Teaching Point", ["Include", "Do not include"], [
        ("Take apixaban twice a day, about 12 hours apart, every day", 0),
        ("If you miss a dose of apixaban, take two tablets at the next dose", 1),
        ("Report black stools, blood in the urine, or bleeding gums that do not stop", 0),
        ("Use ibuprofen for headaches", 1),
        ("Use a soft toothbrush and an electric razor", 0),
        ("Check with the pharmacist before taking any herbal products or supplements", 0),
        ("Stop the perindopril on your own if you develop a dry cough", 1),
        ("Ask about the free smoking cessation program and nicotine replacement", 0),
    ]),
    "explanation": rationale(
        "<b>Include:</b> apixaban protects against clots from atrial fibrillation only if it is taken regularly; it is taken twice a day "
        "about 12 hours apart. It increases bleeding risk, so the client learns the signs of bleeding to report and uses a soft "
        "toothbrush and an electric razor. Many herbal products (for example, ginkgo, garlic and St. John's wort) change bleeding risk or "
        "drug levels. Stopping smoking is one of the most effective ways to lower stroke risk; provincial cessation programs offer "
        "counselling and nicotine replacement.",
        "<b>Do not include:</b> a missed apixaban dose is taken as soon as it is remembered on the same day, then the usual schedule "
        "continues; doses are never doubled. NSAIDs such as ibuprofen add to bleeding risk; acetaminophen is preferred. Stopping her "
        "antihypertensive on her own is what happened with the amlodipine; she reports side effects (an ACE inhibitor can cause a dry "
        "cough) so the provider can change the drug."),
})

# ---------------------------------------------------------------- Screen 6: matrix (evaluate)
C.notes("nn", "Nurses' Notes",
    ("Month 3 1000", "Follow-up visit. Client states: “I quit smoking 6 weeks ago with the patch.” Walks 30 minutes most days with a "
     "neighbour. Says she sometimes misses the evening apixaban “a few times a week because I forget.” Describes FAST correctly and "
     "says she would call 9-1-1. HbA1c today 8.4%. No bleeding or bruising."))
C.vitals("Month 3 1000", vs("36.8° C", "78 beats/min, irregular", "16 breaths/min", "128/78 mm Hg", "98% on room air"))
s6 = screen(6, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Month 3 1000 and the Vital Signs from Month 3 1000.",
    "stem": "For each finding, click to specify whether it shows that an <b>expected outcome has been met</b> or that it <b>requires "
            "follow-up</b>.",
    "matrix": matrix_mc("Finding", ["Expected outcome met", "Requires follow-up"], [
        ("BP 128/78 mm Hg", 0),
        ("Misses the evening apixaban dose a few times a week", 1),
        ("Quit smoking 6 weeks ago", 0),
        ("HbA1c 8.4%", 1),
        ("Walks 30 minutes most days", 0),
        ("Describes the FAST signs and says she would call 9-1-1", 0),
    ]),
    "explanation": rationale(
        "<b>Outcomes met:</b> her BP is now within the target (below 130/80 mm Hg for most people after a stroke or TIA), she has "
        "stopped smoking, she is active on most days, and she can recognize stroke signs and knows to call 9-1-1.",
        "<b>Require follow-up:</b> missed apixaban doses leave her unprotected against clots from atrial fibrillation; the nurse "
        "explores the reason and suggests strategies (phone alarm, pill organizer, linking the dose to supper) and informs the provider. "
        "An HbA1c of 8.4% is above the usual target of 7% or lower, so diabetes management (diet, activity, medications, follow-up with "
        "the diabetes educator) needs attention."),
})

write_case(7,
    "64-year-old female client at a community health clinic who reports a resolved episode of right-hand weakness and jumbled speech: "
    "recognizing a TIA, modifiable and non-modifiable stroke risk factors, same-day emergency referral, FAST teaching, anticoagulant "
    "and antihypertensive teaching, and evaluation of secondary prevention.",
    [s1, s2, s3, s4, s5, s6],
    ["- Nursing-focused case (assessment, priorities, teaching, evaluation), following OpenStax 15.2 for TIA and stroke prevention.",
     "- Referral pathway follows the Canadian Stroke Best Practice Recommendations (same-day emergency assessment for a TIA with "
     "weakness or speech symptoms within 48 hours).",
     "- Clinician review: the missed-dose rule for apixaban and the BP target after TIA."],
    "TIA")
