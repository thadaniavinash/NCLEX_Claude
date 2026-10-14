"""NURS 1017 Unit 6 Case Study 7: fibromyalgia (outcome: myasthenia gravis and fibromyalgia, the
fibromyalgia part). Nursing focus, no treatment decisions."""
from unit6_common import *

ID = "case_1782400000007"
INTRO = "The nurse in a primary care clinic is caring for a 42-year-old female client with widespread pain and fatigue."
C = Chart()

# ---------------------------------------------------------------- Screen 1 (recognize cues): select all
C.notes("nn", "Nurses' Notes", ("Day 1 1400",
    "Reports 8 months of aching pain “all over,” on both sides of her body, above and below the waist, including her neck, shoulders, "
    "back, and hips. Wakes unrefreshed even after 9 hours in bed. Has trouble concentrating and forgets appointments at work (“brain "
    "fog”). Has abdominal cramping with alternating diarrhea and constipation, and tension headaches 3 to 4 times a week. Says a hug or "
    "a tight waistband hurts. Pain 7/10. No joint swelling or redness; full range of motion in all joints; strength 5/5 throughout. Denies "
    "fever, night sweats, or weight loss. Works as a dental hygienist; recently separated from her partner. Takes a multivitamin daily. "
    "Says, “Everyone thinks I'm making this up.”"))
C.vitals("Day 1 1400", vs("36.7° C", "82 beats/min", "16 breaths/min", "122/76 mm Hg", "99% on room air"))
s1 = screen(1, INTRO, C, {
    "type": "select_all",
    "stem": "The nurse reviews the client's history and assessment. Which of the following findings would be consistent with <b>fibromyalgia</b>? <b>Select all that apply.</b>",
    "options": opts(
        ("Pain on both sides of the body, above and below the waist, for 8 months", True),
        ("Wakes unrefreshed after 9 hours in bed", True),
        ("Trouble concentrating and remembering", True),
        ("Abdominal cramping with alternating diarrhea and constipation", True),
        ("A hug or a tight waistband hurts", True),
        ("Tension headaches 3 to 4 times a week", True),
        ("Heart rate 82 beats/min", False),
        ("Takes a multivitamin daily", False),
        ("Blood pressure 122/76 mm Hg", False),
        ("Works as a dental hygienist", False),
        seed="c7s1"),
    "explanation": rationale(
        "<b>Consistent with fibromyalgia:</b> chronic (3 months or more) <b>widespread pain</b> on both sides of the body and above and "
        "below the waist is the core feature. It is accompanied by <b>unrefreshing sleep</b>, <b>fatigue</b>, and <b>cognitive "
        "symptoms</b> (“fibro fog”). Pain from touch that should not hurt (<b>allodynia</b>, such as a hug or a waistband) reflects an "
        "oversensitive pain system. Other functional conditions are common alongside it: <b>irritable bowel syndrome</b>, <b>tension "
        "headaches</b> and migraines, temporomandibular disorder, and anxiety or depression.",
        "<b>Not consistent:</b> a multivitamin, a normal heart rate and blood pressure, and her job. Note also what is absent: no joint "
        "swelling, normal strength and range of motion, and no fever or weight loss. Fibromyalgia does not damage joints or muscles, and "
        "swelling, fever, weight loss or true muscle weakness would suggest another diagnosis."),
})

# ---------------------------------------------------------------- Screen 2 (analyze cues): cloze
C.labs("Day 1 1430", [
    (lab("Hemoglobin (Hgb)", "Female: 115–155 g/L"), "132 g/L"),
    (lab("Erythrocyte sedimentation rate (ESR)", "Female: 0–20 mm/h"), "8 mm/h"),
    (lab("C-reactive protein (CRP)", "≤ 10 mg/L"), "2 mg/L"),
    (lab("Thyrotropin (thyroid-stimulating hormone)", "0.34–5.60 mIU/L"), "2.1 mIU/L"),
    (lab("Creatine kinase (CK)", "Female: 30–190 IU/L"), "96 IU/L"),
    (lab("Rheumatoid factor (RF)", "≤ 20 kIU/L"), "&lt; 10 kIU/L"),
    (lab("Antinuclear antibodies (ANA)", "Negative"), "Negative"),
    (lab("Ferritin", "Female: 11–307 µg/L"), "64 µg/L"),
])
C.notes("nn", "Nurses' Notes", ("Day 10 1000",
    "Client returns for her results. The provider explains that the blood tests are normal and diagnoses fibromyalgia. Client asks, "
    "“If all my tests are normal, why do I hurt so much?”"))
s2 = screen(2, INTRO, C, {
    "type": "dropdown_cloze",
    "preamble": "The nurse has reviewed the Laboratory Results and the Nurses' Notes from Day 10 1000.",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {
        "text": "The normal ESR, CRP, and CK show that the client's pain is not caused by [[drop0]]. Fibromyalgia is best explained by "
                "[[drop1]], in which [[drop2]]. Poor sleep [[drop3]].",
        "dropdowns": [
            dropdown(("inflammation or muscle damage", True), ("stress", False), ("the nervous system", False), seed="c7s2a"),
            dropdown(("central sensitization", True), ("an autoimmune attack on the joints", False),
                     ("degeneration of the joint cartilage", False), ("infection of the muscles", False), seed="c7s2b"),
            dropdown(("the brain and spinal cord amplify pain signals and dampen the body's own pain control", True),
                     ("the muscles release enzymes that damage nerves", False),
                     ("the joints fill with inflammatory fluid", False), seed="c7s2c"),
            dropdown(("lowers the pain threshold and worsens fatigue", True), ("has no effect on her pain", False),
                     ("protects her muscles from injury", False), seed="c7s2d"),
        ],
    },
    "explanation": rationale(
        "<b>Normal tests:</b> fibromyalgia is not an inflammatory, autoimmune or degenerative disease, and it does not damage muscles or "
        "joints. Normal ESR and CRP show no inflammation, a normal CK shows no muscle damage, and a negative RF and ANA make rheumatoid "
        "arthritis and lupus unlikely. A normal TSH rules out hypothyroidism, and normal hemoglobin and ferritin rule out anemia and iron "
        "deficiency as causes of the fatigue. The diagnosis is clinical (widespread pain for 3 months or more with fatigue, unrefreshing "
        "sleep and cognitive symptoms, not better explained by another condition); tender-point counts are no longer required.",
        "<b>Central sensitization:</b> the pain is real, but it comes from how the nervous system processes signals. Pain pathways in the "
        "spinal cord and brain become overactive (more excitatory neurotransmitters such as substance P and glutamate), while the "
        "descending pathways that normally dampen pain (serotonin, norepinephrine) are less active. Ordinary sensations are felt as painful "
        "(allodynia), and painful ones hurt more than they should (hyperalgesia). Stress affects the condition but is not the cause.",
        "<b>Sleep:</b> people with fibromyalgia have less deep, restorative sleep. Poor sleep lowers the pain threshold and worsens fatigue "
        "and concentration, and more pain disturbs sleep further, creating a cycle that nursing care aims to break."),
})

# ---------------------------------------------------------------- Screen 3 (prioritize hypotheses): cloze
C.notes("nn", "Nurses' Notes", ("Day 40 1500",
    "Follow-up visit. Client is tearful. Pain 8/10. Has missed 6 days of work this month and stopped going to her book club. Sleeping "
    "4 to 5 hours a night, then napping 3 hours in the afternoon. Says, “My family thinks it's all in my head. Some days I think everyone "
    "would be better off without me.” Patient Health Questionnaire-9 (PHQ-9) score 17 (moderately severe depression)."))
C.vitals("Day 40 1500", vs("36.8° C", "88 beats/min", "16 breaths/min", "124/78 mm Hg", "99% on room air"))
s3 = screen(3, INTRO, C, {
    "type": "dropdown_cloze",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 40 1500 and the Vital Signs from Day 40.",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {
        "text": "The nurse's priority concern is the client's risk for [[drop0]], as evidenced by [[drop1]]. Her long afternoon naps "
                "[[drop2]].",
        "dropdowns": [
            dropdown(("suicide", True), ("falls", False), ("acute pain", False), ("ineffective work performance", False),
                     seed="c7s3a"),
            dropdown(("her statement that everyone would be better off without her and her PHQ-9 score of 17", True),
                     ("her pain rating of 8/10", False), ("the 6 missed workdays", False), seed="c7s3b"),
            dropdown(("worsen her night-time sleep and keep the pain–sleep cycle going", True),
                     ("are needed to restore her energy", False), ("have no effect on her symptoms", False), seed="c7s3c"),
        ],
    },
    "explanation": rationale(
        "<b>Risk for suicide:</b> “everyone would be better off without me” is an indirect statement of suicidal thinking. With a PHQ-9 "
        "of 17, social withdrawal, the loss of her relationship, and chronic pain (which on its own raises suicide risk), safety is the "
        "priority over pain, sleep or work concerns. The nurse never dismisses such a statement.",
        "<b>Pain, missed work and isolation</b> are important and will be addressed, but they are not immediately life-threatening.",
        "<b>Daytime napping:</b> long afternoon naps reduce the drive to sleep at night, which leads to short, unrefreshing night sleep; "
        "poor sleep then lowers the pain threshold. Short naps (under 30 minutes, early afternoon) or none are better."),
})

# ---------------------------------------------------------------- Screen 4 (generate solutions): matrix
s4 = screen(4, INTRO, C, {
    "type": "matrix_mc",
    "stem": "For each nursing action, click to specify whether it is <b>indicated</b>, <b>contraindicated</b>, or <b>nonessential</b> for "
            "the client at this visit.",
    "matrix": matrix_mc("Nursing Action", ["Indicated", "Contraindicated", "Nonessential"], [
        ("Ask the client directly whether she is thinking about ending her life and whether she has a plan", 0),
        ("Promise to keep her suicidal thoughts a secret if she asks", 1),
        ("Report her statement and PHQ-9 score to the provider before she leaves the clinic", 0),
        ("Tell her that everyone feels this way sometimes and it will pass", 1),
        ("Give her the 9-8-8 Suicide Crisis Helpline number (call or text)", 0),
        ("Repeat the ESR and CRP today", 2),
        ("Stay with her, or make sure someone stays with her, until the assessment is complete", 0),
    ]),
    "explanation": rationale(
        "<b>Indicated:</b> asking directly about suicidal thoughts, a plan and the means does not plant the idea; it opens the "
        "conversation and is the only way to judge the level of risk. The provider must know before she leaves so that a safety plan and "
        "mental health follow-up are arranged. Canada's 9-8-8 Suicide Crisis Helpline is available 24/7 by phone or text. A client who may "
        "be at risk is not left alone until the risk has been assessed.",
        "<b>Contraindicated:</b> the nurse cannot promise secrecy about a risk to the client's life; the information must be shared with the "
        "team. Saying “everyone feels this way” dismisses her distress and closes the conversation.",
        "<b>Nonessential:</b> her inflammatory markers were normal and repeating them does not address her current risk."),
})

# ---------------------------------------------------------------- Screen 5 (take action): select all
C.notes("nn", "Nurses' Notes", ("Day 40 1600",
    "Client denies a plan or intent to harm herself; agreed to a safety plan with the provider and has an appointment with the mental "
    "health team in 2 days. Her sister is driving her home and will stay with her tonight. Client asks, “Is there anything I can do "
    "myself for the pain and tiredness?”"))
s5 = screen(5, INTRO, C, {
    "type": "select_all",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 40 1600.",
    "stem": "Which instructions should the nurse include in the client's self-management teaching? <b>Select all that apply.</b>",
    "options": opts(
        ("Start with gentle aerobic exercise, such as walking or warm-water exercise, a few minutes at a time, and increase slowly", True),
        ("Go to bed and get up at the same times every day, and limit naps", True),
        ("Avoid caffeine after noon and screens for an hour before bed", True),
        ("Pace yourself: break tasks into smaller parts and alternate activity with rest", True),
        ("Practise relaxation, such as slow breathing or mindfulness, to manage stress", True),
        ("Avoid exercise until the pain improves", False),
        ("Do as much as you can on good days to catch up", False),
        ("Increase your coffee intake to fight the fatigue", False),
        ("Since your tests are normal, try to ignore the pain", False),
        seed="c7s5"),
    "explanation": rationale(
        "<b>Correct:</b> regular aerobic exercise has the strongest evidence for reducing fibromyalgia pain and fatigue. It must start low "
        "and build slowly, because doing too much at once causes a flare. A regular sleep schedule, limited naps, and avoiding caffeine "
        "and screens before bed improve sleep quality (sleep hygiene). Pacing prevents the “boom-and-bust” pattern of overdoing it on good "
        "days and crashing afterward. Relaxation and stress management calm the overactive stress and pain systems.",
        "<b>Incorrect:</b> avoiding exercise leads to deconditioning and more pain. Catching up on good days triggers flares. Extra caffeine "
        "disrupts sleep. Telling her to ignore the pain dismisses a real condition and damages trust; normal tests mean no tissue damage, "
        "not that the pain is imaginary."),
})

# ---------------------------------------------------------------- Screen 6 (evaluate outcomes): matrix
C.notes("nn", "Nurses' Notes",
    ("Day 130 1000", "Follow-up visit, 3 months later. Pain 4/10 (was 8/10). Sleeps about 7 hours and wakes rested on 4 nights a week. "
     "Walks 20 minutes, 5 days a week. Has returned to work part-time. PHQ-9 score 6; denies thoughts of self-harm; sees a counsellor "
     "every 2 weeks."),
    ("Day 130 1015", "Client states: “On good days I clean the whole house, and then I'm in bed for 2 days.” “I drink 5 cups of coffee a "
     "day, the last one around 8 at night.” “I still don't see my friends; I never know how I'll feel.”"))
C.vitals("Day 130 1000", vs("36.6° C", "76 beats/min", "14 breaths/min", "118/74 mm Hg", "99% on room air"))
s6 = screen(6, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 130 1000 and 1015 and the Vital Signs from Day 130.",
    "stem": "For each finding, click to specify whether it indicates that the plan of care has been <b>effective</b> or <b>not "
            "effective</b>.",
    "matrix": matrix_mc("Finding", ["Effective", "Not effective"], [
        ("Pain 4/10, down from 8/10", 0),
        ("“On good days I clean the whole house, and then I'm in bed for 2 days.”", 1),
        ("Sleeps about 7 hours and wakes rested 4 nights a week", 0),
        ("Drinks 5 cups of coffee a day, the last around 2000", 1),
        ("PHQ-9 score 6; denies thoughts of self-harm", 0),
        ("Walks 20 minutes, 5 days a week", 0),
        ("“I still don't see my friends; I never know how I'll feel.”", 1),
        ("Has returned to work part-time", 0),
    ]),
    "explanation": rationale(
        "<b>Effective:</b> less pain, better sleep, regular aerobic exercise, a return to work, and a much lower depression score with no "
        "suicidal thoughts show that the plan is working. Fibromyalgia is chronic; the goal is better function and quality of life, not a "
        "cure.",
        "<b>Not effective:</b> the boom-and-bust pattern shows she is not yet pacing herself. Late, heavy caffeine intake undermines sleep. "
        "Avoiding friends increases isolation and the risk of depression. The nurse reinforces pacing and sleep hygiene, and explores ways to "
        "keep social contact (shorter visits, plans that can be changed)."),
})

write_case(ID, 7,
    "42-year-old female client with 8 months of widespread pain, unrefreshing sleep, cognitive symptoms, irritable bowel and headaches, "
    "diagnosed with fibromyalgia after normal tests; central sensitization, the pain–sleep cycle, suicide risk screening, self-management "
    "teaching, and evaluation at 3 months.",
    [s1, s2, s3, s4, s5, s6],
    ["Screen 3–4: the case includes an indirect suicidal statement and the Canadian 9-8-8 Suicide Crisis Helpline; consider mentioning "
     "this to the class before using it.",
     "Screen 2: the diagnostic criteria are described as in the ACR 2010/2016 criteria (tender points no longer required)."])
