"""Builds NURS 1017 Unit 3 Case Study 4 (Duchenne muscular dystrophy) as app-ready JSON."""
import json, os

UNIT = "Unit 3 (Genetic and Developmental Disorders)"
TH = 'style="border:1px solid #ccd8e0; padding:8px; background:#025287; color:white; font-weight:600; text-align:left;"'
TD = 'style="border:1px solid #ccd8e0; padding:8px; background:white; color:#1e293b;"'


def table(headers, rows):
    head = "".join(f"<th {TH}>{h}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td {TD}>{c}</td>" for c in r) + "</tr>" for r in rows)
    return (f'<table class="nclex-editor-table" style="width:100%; border-collapse:collapse; margin:12px 0;">'
            f"<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>")


def notes(*entries):
    return "".join(f'<p class="nurse-note-row"><span class="nurse-note-time">{t}:</span>'
                   f'<span class="nurse-note-text">{x}</span></p>' for t, x in entries)


def tab(tid, title, content):
    return {"id": tid, "title": title, "content": content}


def opts(*pairs):
    return [{"text": t, "correct": c} for t, c in pairs]


def matrix(header, columns, rows):
    return {"firstColumnHeader": header, "columns": columns,
            "rows": [{"text": t, "correctIndex": i, "correctIndices": [i]} for t, i in rows]}


def dropdown(*pairs):
    return {"placeholder": "Select...", "options": opts(*pairs)}


def rationale(*items):
    return "<br><br>".join(items)


# ---------------------------------------------------------------- chart tabs
NN_INTAKE = tab("nn_1", "Nurses' Notes", notes(
    ("0915", "Ethan, a 4-year-old boy, is brought to the pediatric primary care clinic by his mother, Sarah (29 years old), "
     "because his preschool teacher reports that he 'falls more than the other children and cannot keep up on the playground.' "
     "Sarah states he walked independently at 18 months, has never been able to run well, and in the past 6 months has begun "
     "walking on his toes and needs to hold the railing with both hands to climb stairs. She adds that he has a mild expressive speech delay "
     "and is followed by a speech therapist."),
    ("0930", "Gait is wide-based and waddling with an exaggerated lumbar lordosis. When asked to stand up from sitting on the floor, "
     "Ethan rolls to a prone position, pushes up onto his hands and feet, and 'walks' his hands up his thighs to reach standing; "
     "timed rise from the floor is 7 seconds. Both calves are enlarged and feel firm and rubbery on palpation. Unable to hop on one foot. "
     "Heel cords are tight bilaterally with ankle dorsiflexion limited to neutral. Fine motor skills and hand grip are age-appropriate. "
     "No muscle tenderness, rash, or joint swelling."),
    ("0940", "Family history: Sarah's brother died at age 20 of 'heart and breathing failure from a muscle disease' that began when he was a young child. "
     "Ethan has a healthy 2-year-old sister, Lily. Sarah and her partner are planning another pregnancy within the next year. "
     "Immunizations are up to date for age. Primary care provider notified of findings."),
))

VS_INTAKE = tab("vs_1", "Vital Signs & Growth", table(
    ["Parameter", "Ethan (0915)", "Expected for Age 4"],
    [["<b>Temperature</b>", "36.9 °C (tympanic)", "36.5 – 37.5 °C"],
     ["<b>Heart Rate</b>", "104 bpm, regular", "80 – 120 bpm"],
     ["<b>Respiratory Rate</b>", "24 breaths/min, unlabored", "20 – 28 breaths/min"],
     ["<b>Blood Pressure</b>", "98/60 mmHg", "89–112 / 46–72 mmHg"],
     ["<b>SpO<sub>2</sub></b>", "98% on room air", "≥ 95%"],
     ["<b>Weight</b>", "17.2 kg (50th percentile)", "—"],
     ["<b>Height</b>", "102 cm (40th percentile)", "—"]]))

NN_RESULTS = tab("nn_2", "Nurses' Notes", notes(
    ("1400", "Day 10: Ethan and Sarah return to the clinic to review laboratory results with the provider. The provider explains that a markedly elevated "
     "creatine kinase with a normal GGT suggests that the enzymes are leaking from damaged skeletal muscle rather than from the liver, and that "
     "genetic testing has confirmed a diagnosis of Duchenne muscular dystrophy. Sarah is tearful and asks, 'Did I cause this? My brother had the same thing.' "
     "Referral placed to the neuromuscular clinic. Sarah consents to carrier testing."),
))

LABS = tab("lab_2", "Laboratory Results", table(
    ["Test", "Ethan (Day 3)", "Reference Range"],
    [["<b>Creatine kinase (CK)</b>", "<b>18,450 U/L</b> (critical high)", "30 – 200 U/L"],
     ["<b>AST</b>", "<b>168 U/L</b> (high)", "10 – 40 U/L"],
     ["<b>ALT</b>", "<b>212 U/L</b> (high)", "7 – 40 U/L"],
     ["<b>GGT</b>", "14 U/L", "5 – 32 U/L"],
     ["<b>Total bilirubin</b>", "0.4 mg/dL", "0.1 – 1.2 mg/dL"],
     ["<b>TSH</b>", "2.1 mIU/L", "0.7 – 5.7 mIU/L"],
     ["<b>Potassium</b>", "4.3 mEq/L", "3.5 – 5.0 mEq/L"]]))

GENETIC = tab("gen_2", "Genetic Testing Report", table(
    ["Item", "Result"],
    [["<b>Test</b>", "DMD gene deletion/duplication analysis (MLPA), peripheral blood"],
     ["<b>Gene / Locus</b>", "DMD (dystrophin), Xp21.2"],
     ["<b>Finding</b>", "Hemizygous deletion of exons 45–50"],
     ["<b>Reading frame</b>", "Out-of-frame (frameshift) — predicted absence of functional dystrophin protein"],
     ["<b>Interpretation</b>", "Pathogenic. Consistent with a diagnosis of Duchenne muscular dystrophy (DMD)."],
     ["<b>Recommendation</b>", "Genetic counseling; carrier testing for the mother; neuromuscular specialist referral."]]))

NN_COUNSEL = tab("nn_3", "Nurses' Notes", notes(
    ("1000", "Week 3: Genetic counseling visit with Sarah and her partner, Daniel. Sarah's carrier testing has resulted (see Family Genetics tab). "
     "Couple asks what the results mean for Lily and for a future pregnancy. Sarah states, 'Everyone keeps asking about Ethan's liver. "
     "Is his liver failing too?'"),
))

FAMILY = tab("fam_3", "Family Genetics", table(
    ["Family Member", "Status"],
    [["<b>Ethan (4 y, proband)</b>", "Affected — DMD exons 45–50 deletion (hemizygous)"],
     ["<b>Sarah (mother, 29 y)</b>", "<b>Heterozygous carrier</b> of the same DMD exons 45–50 deletion"],
     ["<b>Daniel (father, 31 y)</b>", "Unaffected; not tested (X-linked; not relevant to transmission to sons)"],
     ["<b>Maternal uncle</b>", "Deceased at 20 y — clinical DMD (not genetically confirmed)"],
     ["<b>Maternal grandmother (58 y)</b>", "Presumed carrier; testing offered"],
     ["<b>Lily (sister, 2 y)</b>", "Not tested"]]))

NN_PLAN = tab("nn_4", "Nurses' Notes", notes(
    ("1100", "Month 2: Neuromuscular clinic visit. Ethan (now 4 y 3 mo, 17.6 kg) remains ambulatory; timed rise from floor 7.4 seconds. "
     "The neurologist plans to begin daily oral glucocorticoid therapy to slow the loss of muscle strength and discusses the multidisciplinary care plan. "
     "Chart review: Ethan received 1 dose of varicella vaccine at 12 months; varicella IgG titer pending."),
))

ORDERS_PLAN = tab("ord_4", "Care Plan Orders", table(
    ["Service", "Order"],
    [["<b>Neurology</b>", "Prednisone 0.75 mg/kg (13 mg) PO once daily with breakfast — start after immunization review"],
     ["<b>Cardiology</b>", "Baseline 12-lead ECG and echocardiogram"],
     ["<b>Pulmonology</b>", "Baseline assessment; pulmonary function testing when able to cooperate"],
     ["<b>Physical therapy</b>", "Evaluate and treat; home stretching program; night-time ankle-foot orthoses"],
     ["<b>Nutrition</b>", "Dietitian consult; 25-hydroxyvitamin D level; calcium intake assessment"],
     ["<b>Genetics</b>", "Follow-up counseling for extended family"]]))

NN_ED = tab("nn_5", "Nurses' Notes", notes(
    ("1615", "One year later: Ethan, now 5 years old, is brought to the emergency department after tripping at the park and falling onto an outstretched right hand. "
     "Right distal forearm is swollen and angulated; X-ray shows a displaced distal radius fracture. Radial pulse 2+, capillary refill < 2 seconds, fingers warm "
     "and able to wiggle. Pain 6/10 (FACES). Ethan has taken prednisone 13 mg daily for the past 10 months; last dose at 0730 today. "
     "Orthopedics plans closed reduction under procedural sedation. Ethan last ate at 1230."),
))

VS_ED = tab("vs_5", "Vital Signs", table(
    ["Parameter", "1615"],
    [["<b>Heart Rate</b>", "118 bpm"],
     ["<b>Respiratory Rate</b>", "24 breaths/min"],
     ["<b>Blood Pressure</b>", "104/64 mmHg"],
     ["<b>Temperature</b>", "36.8 °C"],
     ["<b>SpO<sub>2</sub></b>", "99% on room air"],
     ["<b>Weight</b>", "20.1 kg"]]))

NN_FU = tab("nn_6", "Nurses' Notes", notes(
    ("0930", "18 months after starting prednisone: Routine neuromuscular clinic follow-up. Ethan (now 5 y 10 mo) is walking independently, and Sarah reports that falls have decreased "
     "from several per day to about 1 per week since starting prednisone. He attends kindergarten with an individualized education program (IEP). "
     "Sarah is concerned that he 'is always hungry,' has 'grown out of his clothes sideways,' and has more frequent temper outbursts."),
))

FU_DATA = tab("fu_6", "Follow-Up Data", table(
    ["Parameter", "Before Prednisone (4 y 3 mo)", "Now (5 y 10 mo)"],
    [["<b>Timed rise from floor</b>", "7.4 seconds", "7.1 seconds"],
     ["<b>10-meter walk/run time</b>", "6.8 seconds", "6.5 seconds"],
     ["<b>Weight</b>", "17.6 kg (55th percentile)", "<b>24.3 kg (92nd percentile)</b>"],
     ["<b>Height</b>", "103 cm (40th percentile)", "<b>108 cm (15th percentile)</b>"],
     ["<b>BMI</b>", "16.6 kg/m² (65th percentile)", "<b>20.8 kg/m² (98th percentile)</b>"],
     ["<b>Blood pressure</b>", "96/58 mmHg", "104/64 mmHg"],
     ["<b>25-hydroxyvitamin D</b>", "26 ng/mL", "<b>16 ng/mL</b> (goal ≥ 30 ng/mL)"],
     ["<b>Echocardiogram</b>", "EF 64%, normal", "EF 63%, normal"]]))

# ---------------------------------------------------------------- screens
screens = [
    {  # 1 Recognize cues
        "step": 1,
        "leftContent": {"intro": "The nurse in a pediatric primary care clinic is assessing Ethan, a 4-year-old boy brought in by his mother for frequent falls.",
                        "tabs": [NN_INTAKE, VS_INTAKE]},
        "question": {
            "type": "select_all",
            "stem": "The nurse reviews Ethan's history and physical assessment. Which findings should the nurse recognize as cues of a <b>progressive inherited neuromuscular disorder</b>? <b>Select all that apply.</b>",
            "preamble": "",
            "options": opts(
                ("Uses his hands to push up on his thighs to rise from the floor, taking 7 seconds", True),
                ("Heart rate 104 bpm and respiratory rate 24 breaths/min", False),
                ("Enlarged, firm, rubbery calf muscles bilaterally", True),
                ("Maternal uncle died at age 20 of heart and breathing failure from a childhood-onset muscle disease", True),
                ("Age-appropriate hand grip and fine motor skills", False),
                ("Waddling gait with exaggerated lumbar lordosis and difficulty climbing stairs", True),
                ("Height at the 40th percentile and weight at the 50th percentile", False),
                ("Walked independently at 18 months, with frequent falls and toe-walking", True),
            ),
            "explanation": rationale(
                "<b>Correct cues:</b>",
                "<b>Gowers sign</b> (climbing up the thighs with the hands to stand) reflects weakness of the proximal hip and thigh muscles, the first muscles affected in Duchenne muscular dystrophy (DMD).",
                "<b>Calf pseudohypertrophy:</b> the calves look large, but damaged muscle fibers are being replaced by fat and fibrous connective tissue, which makes them feel firm and rubbery. They are not stronger.",
                "<b>Family history:</b> an affected male relative on the mother's side (her brother) who died young of cardiac and respiratory failure strongly suggests an X-linked recessive disorder passed through the maternal line.",
                "<b>Waddling (Trendelenburg) gait, lumbar lordosis and trouble with stairs</b> compensate for weak hip and trunk muscles.",
                "<b>Late walking (after about 15–18 months), frequent falls and toe-walking</b> are early motor signs. Toe-walking comes from tight heel cords (Achilles contractures).",
                "<b>Not cues:</b> heart rate, respiratory rate and growth are normal for a 4-year-old. Grip and fine motor skills are usually preserved early because DMD weakens proximal muscles before distal ones."),
        },
    },
    {  # 2 Analyze cues
        "step": 2,
        "leftContent": {"intro": "Ethan's laboratory and genetic test results are now available.",
                        "tabs": [NN_RESULTS, LABS, GENETIC]},
        "question": {
            "type": "matrix_mc",
            "stem": "The nurse compares Duchenne muscular dystrophy with Becker muscular dystrophy to prepare family teaching. For each feature, click to specify whether it is characteristic of <b>Duchenne muscular dystrophy</b>, <b>Becker muscular dystrophy</b>, or <b>Both</b>.",
            "preamble": "",
            "matrix": matrix("Feature", ["Duchenne", "Becker", "Both"], [
                ("Out-of-frame DMD gene deletion resulting in absent dystrophin protein", 0),
                ("In-frame DMD gene deletion producing a shortened, partially functional dystrophin protein", 1),
                ("X-linked recessive inheritance affecting mostly males", 2),
                ("Onset of weakness in early childhood with loss of independent walking by about age 12 without treatment", 0),
                ("Milder course, with many people still walking into their late teens or adulthood", 1),
                ("Elevated serum creatine kinase and risk of cardiomyopathy", 2),
            ]),
            "explanation": rationale(
                "Both disorders are <b>X-linked recessive</b> and are caused by mutations in the same gene, DMD, which codes for dystrophin. Dystrophin anchors the inside of the muscle fiber to its outer membrane and protects the membrane during contraction.",
                "<b>Duchenne:</b> an out-of-frame deletion (such as Ethan's exons 45–50) shifts the genetic reading frame, so almost no functional dystrophin is made. Muscle membranes tear with everyday use, and fibers die and are replaced by fat and fibrous tissue. Weakness starts in early childhood, and without treatment children usually stop walking by about age 12.",
                "<b>Becker:</b> an in-frame deletion keeps the reading frame intact, so a shorter but partly working dystrophin is made. The course is milder and later, and many people still walk into their late teens or adulthood.",
                "<b>Both:</b> damaged muscle leaks creatine kinase (CK) into the blood, so CK is elevated in both conditions. Heart muscle also needs dystrophin, so both carry a risk of dilated cardiomyopathy."),
        },
    },
    {  # 3 Analyze cues / prioritize hypotheses
        "step": 3,
        "leftContent": {"intro": "Three weeks after diagnosis, Ethan's parents meet with the nurse and genetic counselor to review carrier test results.",
                        "tabs": [NN_COUNSEL, FAMILY, LABS]},
        "question": {
            "type": "dropdown_cloze",
            "stem": "The nurse reinforces the genetic counselor's teaching. Complete the following sentences by choosing from the lists of options.",
            "preamble": "",
            "cloze": {
                "text": "Because Sarah is a heterozygous carrier, each of her sons has a [[drop0]] chance of being affected by DMD, and each daughter has a [[drop1]] chance of being a carrier. "
                        "Ethan's elevated AST and ALT with a normal GGT and bilirubin most likely reflect [[drop2]].",
                "dropdowns": [
                    dropdown(("25%", False), ("50%", True), ("100%", False)),
                    dropdown(("0%", False), ("50%", True), ("100%", False)),
                    dropdown(("enzyme release from damaged skeletal muscle", True),
                             ("early liver failure", False),
                             ("a side effect of his vaccinations", False)),
                ],
            },
            "explanation": rationale(
                "<b>X-linked recessive inheritance:</b> a carrier mother has one normal X and one X with the DMD mutation, and passes one of them to each child at random.",
                "<b>Sons</b> get their only X from their mother (and a Y from their father), so each son has a <b>50% chance</b> of inheriting the mutated X and being affected.",
                "<b>Daughters</b> get one X from each parent. Each daughter has a <b>50% chance</b> of receiving the mutated X and being a carrier; because she also has her father's normal X, she is usually unaffected. Carrier women do have a risk of cardiomyopathy and should have periodic heart screening.",
                "<b>Liver enzymes:</b> AST and ALT are found in skeletal muscle as well as the liver. When they rise alongside a very high CK while liver-specific markers (GGT, bilirubin) are normal, the source is damaged muscle, not the liver. Recognizing this prevents unnecessary liver work-ups such as a liver biopsy."),
        },
    },
    {  # 4 Generate solutions
        "step": 4,
        "leftContent": {"intro": "Two months after diagnosis, the nurse is coordinating Ethan's multidisciplinary plan of care at the neuromuscular clinic.",
                        "tabs": [NN_PLAN, ORDERS_PLAN]},
        "question": {
            "type": "select_all",
            "stem": "The nurse is planning care and teaching for Ethan and his family. Which interventions should the nurse include in the plan of care? <b>Select all that apply.</b>",
            "preamble": "",
            "options": opts(
                ("Confirm varicella immunity and complete any outstanding immunizations before starting prednisone", True),
                ("Limit Ethan to bed and wheelchair rest to conserve remaining muscle strength", False),
                ("Teach the family a daily home stretching program for the heel cords and hips, and use night-time ankle-foot orthoses", True),
                ("Encourage swimming and tricycle riding, and avoid trampolines and repeated downhill running", True),
                ("Recommend a high-calorie diet to build muscle mass", False),
                ("Place an alert in Ethan's chart and provide a wallet card stating that succinylcholine and inhaled volatile anesthetics must be avoided", True),
                ("Recommend that Sarah, as a confirmed carrier, have periodic cardiac screening", True),
                ("Monitor serum creatine kinase every week to measure how fast the disease is progressing", False),
            ),
            "explanation": rationale(
                "<b>Immunizations first:</b> daily glucocorticoids weaken the immune response. Varicella immunity should be confirmed and vaccines completed before steroid therapy begins, and annual inactivated influenza vaccination continues afterward.",
                "<b>Stretching and night splints:</b> daily stretching and resting ankle-foot orthoses slow the development of heel-cord and hip contractures, which hasten the loss of walking.",
                "<b>The right kind of activity:</b> gentle, submaximal aerobic activity such as swimming or cycling helps maintain function. Eccentric and high-impact exercise (trampolines, running downhill) and heavy resistance training cause more muscle damage and should be avoided.",
                "<b>Anesthesia alert:</b> in dystrophin-deficient muscle, succinylcholine and inhaled volatile anesthetics can cause sudden muscle breakdown (rhabdomyolysis), a life-threatening rise in potassium, and cardiac arrest.",
                "<b>Carrier heart screening:</b> female carriers can develop dilated cardiomyopathy and need periodic cardiac evaluation.",
                "<b>Incorrect:</b> bed rest speeds up muscle loss and contractures. Extra calories do not build dystrophic muscle; they cause obesity (made worse by steroids), which further limits mobility. CK does not track disease progression and actually falls over time as muscle mass is lost."),
        },
    },
    {  # 5 Take action
        "step": 5,
        "leftContent": {"intro": "One year later, Ethan is brought to the emergency department after a fall and needs a fracture reduction under procedural sedation.",
                        "tabs": [NN_ED, VS_ED]},
        "question": {
            "type": "matrix_mc",
            "stem": "The emergency department nurse is preparing Ethan for closed reduction of his forearm fracture. For each nursing action, click to specify whether the action is <b>Indicated</b>, <b>Non-Essential</b>, or <b>Contraindicated</b>.",
            "preamble": "",
            "matrix": matrix("Nursing Action", ["Indicated", "Non-Essential", "Contraindicated"], [
                ("Tell the provider that Ethan has taken prednisone daily for 10 months, so a stress dose of steroids can be considered", 0),
                ("Hold Ethan's prednisone for the next several days while he is recovering", 2),
                ("Prepare succinylcholine as the paralytic agent in case airway management is needed", 2),
                ("Assess neurovascular status of the right hand before and after the reduction", 0),
                ("Obtain a serum creatine kinase level before the procedure", 1),
                ("Keep Ethan on strict bed rest for 2 weeks after the reduction", 2),
            ]),
            "explanation": rationale(
                "<b>Indicated – stress-dose steroids:</b> long-term glucocorticoid use suppresses the body's own adrenal response. Procedures and injuries raise cortisol needs, so the provider must know about Ethan's steroid use in order to consider stress dosing and prevent adrenal crisis (low blood pressure, shock).",
                "<b>Contraindicated – holding prednisone:</b> stopping chronic steroids abruptly can cause adrenal insufficiency. The daily dose must continue unless the prescriber changes it.",
                "<b>Contraindicated – succinylcholine:</b> in DMD it can cause rhabdomyolysis, severe hyperkalemia and cardiac arrest. The nurse should speak up and point out the anesthesia alert.",
                "<b>Indicated – neurovascular checks:</b> checking pulses, capillary refill, color, warmth, movement and sensation before and after reduction detects vascular injury or compartment syndrome.",
                "<b>Non-Essential – CK level:</b> CK is chronically elevated in DMD and does not guide this procedure.",
                "<b>Contraindicated – strict bed rest:</b> immobility in DMD can cause permanent loss of walking within days to weeks. Children should be up and moving as early as it is safe, with physical therapy."),
        },
    },
    {  # 6 Evaluate outcomes
        "step": 6,
        "leftContent": {"intro": "Ethan returns to the neuromuscular clinic 18 months after starting prednisone for a routine evaluation.",
                        "tabs": [NN_FU, FU_DATA]},
        "question": {
            "type": "dropdown_cloze",
            "stem": "The nurse evaluates Ethan's response to the plan of care. Complete the following sentences by choosing from the lists of options.",
            "preamble": "",
            "cloze": {
                "text": "Ethan's stable timed rise from the floor and 10-meter walk/run time indicate that prednisone therapy is [[drop0]]. "
                        "His weight gain, slowed growth in height, and vitamin D level of 16 ng/mL indicate a need to [[drop1]]. "
                        "When Sarah asks whether the prednisone can simply be stopped because of the weight gain, the nurse explains that it [[drop2]].",
                "dropdowns": [
                    dropdown(("achieving its goal of slowing the loss of muscle strength", True),
                             ("curing the underlying genetic defect", False),
                             ("no longer needed because Ethan's strength has stabilized", False)),
                    dropdown(("request a dietitian referral and discuss vitamin D and calcium supplementation with the provider", True),
                             ("stop physical therapy until his weight improves", False),
                             ("give extra calories to support muscle growth", False)),
                    dropdown(("must never be stopped suddenly; any change must be a gradual taper directed by the provider", True),
                             ("can be stopped at home once his weight returns to normal", False),
                             ("should be stopped for 1 week each month to allow a steroid holiday", False)),
                ],
            },
            "explanation": rationale(
                "<b>Expected outcome:</b> in DMD, steroids aim to slow the decline, not to cure. For a 5–6-year-old with Duchenne, holding his motor function steady (rise time 7.4 → 7.1 s) and falling less shows the treatment is working. It does not mean the treatment can stop; the underlying dystrophin deficiency remains.",
                "<b>Adverse effects needing a plan change:</b> steroid-related weight gain (BMI now at the 98th percentile), slowed growth in height, and vitamin D deficiency. Steroid treatment and reduced mobility both weaken bones and raise fracture risk, as Ethan's broken arm showed. The nurse should arrange nutrition counseling and discuss vitamin D and calcium supplementation with the provider. Behavior changes and increased appetite are also common steroid effects that the family should know about.",
                "<b>Safety teaching:</b> chronic glucocorticoids suppress the adrenal glands. Stopping them suddenly can cause a life-threatening adrenal crisis, so any change in dose must be a gradual taper ordered by the prescriber."),
        },
    },
]

case = {
    "id": "case_1782370000004",
    "title": "NURS 1017 Unit 3 Case Study 4",
    "topic": UNIT,
    "unit": UNIT,
    "disorder": UNIT,
    "course": "NURS 1017",
    "description": "4-year-old boy with frequent falls, Gowers sign, calf pseudohypertrophy, and a maternal family history of early death from muscle disease, "
                   "unfolding through genetic diagnosis of Duchenne muscular dystrophy, X-linked recessive carrier counseling, glucocorticoid therapy, "
                   "anesthesia safety, and evaluation of treatment outcomes.",
    "screens": screens,
}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "case_1782370000004_NURS_1017_Unit_3_Case_Study_4.json")
with open(out, "w") as f:
    json.dump(case, f, indent=2, ensure_ascii=False)
print("wrote", out)
