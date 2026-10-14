"""NURS 1017 Unit 6 Case Study 5: myasthenia gravis, diagnosis to myasthenic crisis (outcome: myasthenia
gravis). Nursing focus, no treatment decisions."""
from unit6_common import *

ID = "case_1782400000005"
INTRO = "The nurse in a neurology clinic is caring for a 34-year-old female client with drooping eyelids and weakness."
C = Chart()

# ---------------------------------------------------------------- Screen 1 (recognize cues): select all
C.notes("nn", "Nurses' Notes", ("Day 1 1500",
    "Reports 3 months of drooping eyelids and double vision that are mild in the morning and worse by late afternoon, especially after "
    "reading or working at her computer. Her jaw gets tired while chewing meat and she rests partway through meals. Her voice becomes soft "
    "and nasal during long phone calls. Her arms tire while blow-drying her hair but recover after a short rest. Denies numbness, tingling, "
    "pain, or muscle twitching. Bilateral ptosis, worse on the left after 60 seconds of looking upward. Pupils equal and reactive. Sensation "
    "intact in all limbs. Reports occasional low back pain after gardening on weekends. Drinks 3 cups of coffee a day. Works as an accountant; has two children aged 4 and 7."))
C.vitals("Day 1 1500", vs("36.8° C", "76 beats/min", "16 breaths/min", "118/74 mm Hg", "99% on room air"))
s1 = screen(1, INTRO, C, {
    "type": "select_all",
    "stem": "The nurse reviews the client's history and assessment. Which of the following findings would be consistent with a <b>disorder of neuromuscular transmission</b>? <b>Select all that apply.</b>",
    "options": opts(
        ("Drooping eyelids and double vision that worsen as the day goes on", True),
        ("Jaw tires while chewing, so she rests partway through meals", True),
        ("Voice becomes soft and nasal during long conversations", True),
        ("Arm weakness while blow-drying her hair that recovers after a short rest", True),
        ("Ptosis that worsens after 60 seconds of looking upward", True),
        ("Low back pain after gardening", False),
        ("Drinks 3 cups of coffee a day", False),
        ("Heart rate 76 beats/min", False),
        ("Blood pressure 118/74 mm Hg", False),
        seed="c5s1"),
    "explanation": rationale(
        "<b>Hallmark: fatigable weakness.</b> In myasthenia gravis (MG), voluntary muscles weaken with repeated use and recover with rest. "
        "Weakness is therefore least in the morning and worst later in the day or after sustained activity.",
        "<b>Ocular muscles</b> are affected first in most clients (ptosis, diplopia). Sustained upward gaze tires the eyelid muscle and "
        "brings out the ptosis.",
        "<b>Bulbar muscles</b> (chewing, swallowing, speaking) are often affected: a tiring jaw, a soft nasal voice, choking. Bulbar "
        "weakness matters because it threatens the airway.",
        "<b>Proximal limb muscles</b> tire with repeated or sustained use, such as holding the arms up.",
        "<b>Not consistent:</b> back pain after gardening is a common strain, her coffee intake is moderate, and her heart rate and blood "
        "pressure are normal.",
        "<b>Also note what she denies:</b> MG affects only the neuromuscular junction, so sensation is normal (numbness and tingling would "
        "suggest a nerve problem) and there is no twitching (fasciculations suggest a motor neuron disease such as ALS). Weakness that is "
        "worst on waking would be the opposite of the MG pattern."),
})

# ---------------------------------------------------------------- Screen 2 (analyze cues): cloze
C.notes("dx", "Diagnostic Results",
    ("Day 1 1530", "<b>Ice pack test:</b> after an ice pack was held over the left eye for 2 minutes, the ptosis improved by 3 mm."),
    ("Day 8 0900", "<b>Acetylcholine receptor antibodies:</b> positive."),
    ("Day 8 1000", "<b>Repetitive nerve stimulation:</b> progressive decrease in muscle response with repeated stimulation."),
    ("Day 10 1400", "<b>CT of the chest:</b> enlarged thymus (thymic hyperplasia); no mass."))
C.notes("nn", "Nurses' Notes", ("Day 14 1000",
    "Client returns to discuss her results. The neurologist confirms a diagnosis of generalized myasthenia gravis. Client asks, “What is "
    "actually wrong with my muscles?”"))
s2 = screen(2, INTRO, C, {
    "type": "dropdown_cloze",
    "preamble": "The nurse has reviewed the Diagnostic Results and the Nurses' Notes from Day 14 1000.",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {
        "text": "In myasthenia gravis, [[drop0]]. With repeated use, the muscle weakens because [[drop1]]. The ice pack improved the "
                "ptosis because cold [[drop2]]. The thymus is examined because it [[drop3]].",
        "dropdowns": [
            dropdown(("antibodies block and destroy acetylcholine receptors at the neuromuscular junction", True),
                     ("the motor neurons in the spinal cord degenerate", False),
                     ("the myelin around peripheral nerves is destroyed", False),
                     ("the muscle fibers lack the protein dystrophin", False), seed="c5s2a"),
            dropdown(("each nerve impulse releases less acetylcholine, and too few receptors remain to respond", True),
                     ("lactic acid builds up and damages the muscle fibers", False),
                     ("the nerve stops conducting impulses altogether", False), seed="c5s2b"),
            dropdown(("slows the breakdown of acetylcholine, so more of it reaches the receptors", True),
                     ("reduces swelling of the eyelid", False),
                     ("destroys the antibodies in the eyelid", False), seed="c5s2c"),
            dropdown(("is often abnormal in myasthenia gravis and is thought to help produce the antibodies", True),
                     ("produces acetylcholine for the muscles", False),
                     ("is where the muscle weakness begins", False), seed="c5s2d"),
        ],
    },
    "explanation": rationale(
        "<b>Autoimmune mechanism:</b> MG is an antibody-mediated autoimmune disease. Antibodies against the acetylcholine (ACh) receptor "
        "on the muscle side of the neuromuscular junction block the receptors, speed their destruction, and activate complement, which "
        "damages the folds of the muscle membrane. Fewer receptors mean a weaker signal to contract. (Motor neuron degeneration is ALS; "
        "demyelination of peripheral nerves is Guillain-Barré syndrome; absent dystrophin is Duchenne muscular dystrophy.)",
        "<b>Fatigability:</b> with each repeated nerve impulse, the amount of ACh released normally falls a little. In healthy muscle there "
        "are plenty of receptors, so this does not matter; in MG there are too few, so contraction fades. This is also what repetitive "
        "nerve stimulation shows: a decreasing response.",
        "<b>Ice pack test:</b> cooling slows acetylcholinesterase, the enzyme that breaks down ACh, so more ACh is available at the "
        "receptors and the eyelid lifts. Heat has the opposite effect, which is why hot weather and hot baths worsen MG.",
        "<b>Thymus:</b> most clients with ACh receptor antibodies have an abnormal thymus (hyperplasia, or a thymoma in about 10% to 15%). "
        "The thymus is thought to help start and maintain the autoimmune response."),
})

# ---------------------------------------------------------------- Screen 3 (prioritize hypotheses): cloze
C.notes("nn", "Nurses' Notes",
    ("Day 240 1900", "Eight months later: admitted to the medical unit with community-acquired pneumonia. Takes pyridostigmine 60 mg PO "
     "four times a day; says she missed two doses yesterday because “it was hard to swallow the pills.”"),
    ("Day 241 0600", "Client is anxious and says she cannot get her breath. Speaks 3 to 4 words at a time in a soft, nasal voice. Pooling "
     "of saliva in the mouth; coughs weakly and cannot clear secretions. Neck flexion weak; cannot lift her head off the pillow. "
     "Bilateral ptosis. Using accessory neck muscles to breathe. No diarrhea, abdominal cramping, or sweating; pupils 4 mm."),
    ("Day 241 0610", "Forced vital capacity (FVC) 1.1 L (was 2.4 L on admission); negative inspiratory force −18 cm H₂O."))
C.vitals("Day 240 1900", vs("38.3° C", "98 beats/min", "22 breaths/min", "122/76 mm Hg", "95% on 2 L/min by nasal cannula"))
C.vitals("Day 241 0600", vs("38.0° C", "112 beats/min", "30 breaths/min, shallow", "130/82 mm Hg", "93% on 2 L/min by nasal cannula"))
s3 = screen(3, INTRO, C, {
    "type": "dropdown_cloze",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 240 1900 and Day 241 0600 and 0610, and the Vital Signs from Day 240 "
                "and Day 241.",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {
        "text": "The client is most likely experiencing [[drop0]], triggered by [[drop1]]. The finding that best shows how serious her "
                "condition is, is [[drop2]]. The nurse's priority concern is [[drop3]].",
        "dropdowns": [
            dropdown(("myasthenic crisis", True), ("cholinergic crisis", False), ("a stroke", False),
                     ("an anxiety attack", False), seed="c5s3a"),
            dropdown(("the pneumonia and the missed pyridostigmine doses", True), ("the low-flow oxygen", False),
                     ("her anxiety", False), seed="c5s3b"),
            dropdown(("the fall in vital capacity from 2.4 L to 1.1 L", True), ("the SpO₂ of 93%", False),
                     ("the heart rate of 112 beats/min", False), ("the temperature of 38.0° C", False), seed="c5s3c"),
            dropdown(("respiratory failure from weak breathing muscles and inability to clear secretions", True),
                     ("dehydration from fever", False), ("falls from leg weakness", False), seed="c5s3d"),
        ],
    },
    "explanation": rationale(
        "<b>Myasthenic crisis</b> is a sudden worsening of MG in which the breathing and bulbar muscles become too weak to maintain "
        "ventilation and protect the airway. Common triggers are infection (here, pneumonia with fever), missed or too little "
        "cholinesterase inhibitor, surgery, stress, and some medicines.",
        "<b>Why not cholinergic crisis:</b> too much cholinesterase inhibitor can also cause weakness, but with signs of excess acetylcholine "
        "(diarrhea, cramping, sweating, excessive secretions, small pupils, slow heart rate). She has missed doses and has none of these "
        "signs except pooled saliva, which here comes from being unable to swallow. The provider confirms which crisis it is.",
        "<b>Vital capacity</b> measures the strength of the breathing muscles directly and falls before oxygen saturation does. A vital "
        "capacity below about 20 mL/kg (about 1.2 L for a 60-kg client) or a negative inspiratory force weaker than −20 to −30 cm H₂O "
        "signals impending respiratory failure. Pulse oximetry stays reassuring until late because the oxygen she is receiving masks "
        "hypoventilation.",
        "<b>Priority:</b> airway and breathing. Weak respiratory muscles plus weak swallowing and coughing (aspiration risk) can lead to "
        "respiratory arrest within hours."),
})

# ---------------------------------------------------------------- Screen 4 (generate solutions): select all
s4 = screen(4, INTRO, C, {
    "type": "select_all",
    "stem": "Which actions should the nurse take at this time? <b>Select all that apply.</b>",
    "options": opts(
        ("Notify the provider and the rapid response team of the falling vital capacity", True),
        ("Raise the head of the bed and keep suction equipment at the bedside", True),
        ("Hold all food, fluids, and oral medications until her swallowing is assessed", True),
        ("Measure vital capacity and negative inspiratory force as prescribed and report any further decrease", True),
        ("Stay with the client and reassure her while help is on the way", True),
        ("Encourage the client to walk in the hallway to clear lung secretions", False),
        ("Give thin liquids through a straw to keep her hydrated", False),
        ("Lay the client flat to rest her breathing muscles", False),
        ("Rely on pulse oximetry to detect any further decline in breathing", False),
        seed="c5s4"),
    "explanation": rationale(
        "<b>Correct:</b> a vital capacity this low means she may soon need ventilatory support, so the provider and the rapid response team "
        "are called now. Head elevation helps breathing and reduces aspiration, and suction must be ready because she cannot clear her "
        "secretions. Nothing is given by mouth while bulbar weakness makes swallowing unsafe; the nurse tells the provider that oral "
        "medicines are being held so other routes can be ordered. Serial vital capacity and negative inspiratory force track her "
        "breathing muscle strength. Staying with her reduces anxiety and allows rapid response to deterioration.",
        "<b>Incorrect:</b> exertion worsens fatigable weakness and increases oxygen demand. Thin liquids are the hardest to swallow safely "
        "and are easily aspirated. Lying flat makes breathing harder and increases aspiration risk. Pulse oximetry detects respiratory "
        "failure late, especially when the client is receiving oxygen; vital capacity and the client's work of breathing are better "
        "guides."),
})

# ---------------------------------------------------------------- Screen 5 (take action): matrix
C.notes("nn", "Nurses' Notes", ("Day 255 1000",
    "Intubated in the intensive care unit on Day 241; extubated on Day 249 and transferred back to the medical unit. Swallowing assessment "
    "passed; eating a soft diet. Pneumonia resolved. Pyridostigmine 60 mg PO four times a day resumed. Discharge planned for tomorrow. "
    "Client says, “I never want to go through that again. What can I do?”"))
C.vitals("Day 255 1000", vs("36.7° C", "78 beats/min", "16 breaths/min", "116/72 mm Hg", "98% on room air"))
s5 = screen(5, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 255 1000 and the Vital Signs from Day 255.",
    "stem": "For each instruction, click to specify whether it is <b>appropriate</b> or <b>not appropriate</b> to include in the "
            "client's discharge teaching.",
    "matrix": matrix_mc("Instruction", ["Appropriate", "Not appropriate"], [
        ("Take pyridostigmine on time, about 30 to 60 minutes before meals", 0),
        ("Take hot baths to relax your muscles in the evening", 1),
        ("Plan demanding tasks for times of the day when you feel strongest, and rest between activities", 0),
        ("Skip a dose of pyridostigmine on days when you feel strong", 1),
        ("Check with your provider or pharmacist before taking any new medicine, including antibiotics", 0),
        ("Wear a medical alert bracelet that says you have myasthenia gravis", 0),
        ("Eat your largest meal in the evening, when you are hungriest", 1),
        ("Seek emergency care for trouble swallowing, a weak cough, or shortness of breath", 0),
    ]),
    "explanation": rationale(
        "<b>Appropriate:</b> pyridostigmine (a cholinesterase inhibitor) works for 3 to 4 hours, so doses are taken on time, and before "
        "meals so chewing and swallowing are strongest while eating. Energy conservation (doing demanding tasks when strength is best, "
        "resting between activities) works with the fatigable pattern. Many medicines can worsen MG (for example some antibiotics such as "
        "fluoroquinolones and aminoglycosides, magnesium, and beta-blockers), so new medicines are checked first. A medical alert bracelet "
        "informs emergency staff. Difficulty swallowing, a weak cough or breathlessness can signal a crisis and need emergency care.",
        "<b>Not appropriate:</b> heat worsens neuromuscular transmission (hot baths, saunas, hot weather). Missing doses can trigger a "
        "crisis, as it did before. Fatigue is worst in the evening, so large evening meals raise the risk of choking; smaller meals at "
        "times of best strength are safer."),
})

# ---------------------------------------------------------------- Screen 6 (evaluate outcomes): matrix
C.notes("nn", "Nurses' Notes",
    ("Day 285 1000", "Clinic follow-up, 1 month after discharge. FVC 2.6 L. Swallows thin liquids without coughing. Ptosis only late in "
     "the evening; double vision rare. Reports choking on liquids at supper on 2 evenings this week, with a weak voice by bedtime."),
    ("Day 285 1015", "Client states: “I wear my medical alert bracelet.” “I sometimes skip my bedtime dose when I feel strong.” “I got my "
     "flu shot, and I stay away from people with colds.” “I started a hot yoga class to build up my strength.”"))
C.vitals("Day 285 1000", vs("36.6° C", "74 beats/min", "14 breaths/min", "114/70 mm Hg", "99% on room air"))
s6 = screen(6, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 285 1000 and 1015 and the Vital Signs from Day 285.",
    "stem": "For each finding, click to specify whether it indicates that the plan of care has been <b>effective</b> or <b>not "
            "effective</b>.",
    "matrix": matrix_mc("Finding", ["Effective", "Not effective"], [
        ("FVC 2.6 L", 0),
        ("“I sometimes skip my bedtime dose when I feel strong.”", 1),
        ("Ptosis only late in the evening; double vision rare", 0),
        ("Choking on liquids at supper, with a weak voice by bedtime", 1),
        ("“I wear my medical alert bracelet.”", 0),
        ("“I started a hot yoga class to build up my strength.”", 1),
        ("“I got my flu shot, and I stay away from people with colds.”", 0),
    ]),
    "explanation": rationale(
        "<b>Effective:</b> her vital capacity has recovered to a safe level, her ocular symptoms are mild and limited to the end of the day "
        "(expected in MG), and she has taken steps that reduce the risk of another crisis (medical alert bracelet, influenza vaccination "
        "with an inactivated vaccine, avoiding infection).",
        "<b>Not effective:</b> skipping doses and choking with a weak voice in the evening show that bulbar weakness is not controlled at the "
        "end of the day; this puts her at risk of aspiration and another crisis. The nurse reinforces taking every dose on time and reports "
        "the evening choking to the provider. Hot yoga exposes her to heat, which worsens neuromuscular transmission; gentle exercise in a "
        "cool environment, paced with rest, is safer."),
})

write_case(ID, 5,
    "34-year-old female client with fatigable ocular, bulbar and limb weakness diagnosed as myasthenia gravis (acetylcholine receptor "
    "antibodies, decremental response, thymic hyperplasia); autoimmune pathophysiology, myasthenic crisis triggered by pneumonia and "
    "missed doses, airway priorities, discharge teaching, and evaluation.",
    [s1, s2, s3, s4, s5, s6],
    ["Screen 3: thresholds for respiratory failure (vital capacity below about 20 mL/kg, negative inspiratory force weaker than −20 to "
     "−30 cm H₂O) are commonly cited values.",
     "Screen 5: the list of medicines that can worsen myasthenia gravis is given as examples."])
