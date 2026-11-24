"""NURS 1017 Unit 3 Case Studies 5-7: revised versions of the three case studies the user wrote (November 2026,
"NURS 1017 Unit 3 - New NGN Case Studies" PDF): 5 Turner syndrome, 6 sickle cell disease and Mendelian
inheritance, 7 teratogens (isotretinoin, rubella, valproic acid) and multifactorial neural tube defects.

The user's storyline, clients and most questions are kept. Main revisions: answer order without a pattern,
plausible distractors, SI units, raw chart data (no "(high)"/"(tachycardic)" labels or interpretation columns),
matrix rows that do not name their own answer, entries labelled by visit/day, preambles that name only what is
new, nurse-scope wording, and the content corrections listed in each case's authorReview note.
Writes drafts/case_178237000000{5,6,7}_NURS_1017_Unit_3_Case_Study_{5,6,7}.json (not published).
"""
import json, os, re
from unit6_common import Chart, table, note_rows, shuffle, matrix_mc, rationale, lab, HERE

UNIT = "Unit 3 (Genetic and Developmental Disorders)"


class Chart3(Chart):
    """unit6_common.Chart plus tabs whose table grows by rows (care plans, family history)."""

    def rows(self, tid, title, headers, rows):
        t = self._tab(tid, title, "rows", headers)
        t["entries"].extend(rows)

    def snapshot(self):
        out = super().snapshot()
        for tab in out:
            t = self.tabs[tab["id"]]
            if t["kind"] == "rows":
                tab["content"] = table(t["header"], t["entries"])
        return out


def vrow(label, expected=None):
    """Vital-sign row label, with the expected range for age on a second line when given."""
    return f"<b>{label}</b>" + (f"<br>{expected}" if expected else "")


def select_all(seed, items, explanation, **q):
    """items: (key, text, correct). Shuffles, then writes "(Option N)" for {key} in the rationale."""
    order = shuffle([{"key": k, "text": t, "correct": c} for k, t, c in items], seed)
    num = {o["key"]: i + 1 for i, o in enumerate(order)}

    def refs(m):
        keys = m.group(1).split(",")
        ns = sorted(num[k] for k in keys)
        if len(ns) == 1:
            return f"(Option {ns[0]})"
        return "(Options " + ", ".join(map(str, ns[:-1])) + f" and {ns[-1]})"
    expl = re.sub(r"\{([A-Z](?:,[A-Z])*)\}", refs, explanation)
    q.update({"type": "select_all", "options": [{"text": o["text"], "correct": o["correct"]} for o in order],
              "explanation": expl})
    return q


def dd(seed, correct, *wrong):
    return {"placeholder": "Select...", "options": shuffle([{"text": correct, "correct": True}] +
                                                           [{"text": w, "correct": False} for w in wrong], seed)}


def screen(step, intro, chart, question):
    question.setdefault("preamble", "")
    return {"step": step, "leftContent": {"intro": intro, "tabs": chart.snapshot()}, "question": question}


def write_case(case_id, n, description, screens, review):
    case = {"id": case_id, "title": f"NURS 1017 Unit 3 Case Study {n}", "course": "NURS 1017", "unit": UNIT,
            "topic": UNIT, "disorder": UNIT, "description": description,
            "authorReview": {"note": review, "flaggedAt": "2026-11-24"}, "screens": screens}
    out = os.path.join(HERE, f"{case_id}_NURS_1017_Unit_3_Case_Study_{n}.json")
    with open(out, "w") as f:
        json.dump(case, f, indent=2, ensure_ascii=False)
    print("wrote", out)


IMC = ["Indicated", "Non-Essential", "Contraindicated"]

# =====================================================================================================
# Case Study 5: Turner syndrome
# =====================================================================================================
C = Chart3()
INTRO1 = ("The nurse in a pediatric endocrinology clinic is assessing Chloe, a 15-year-old female client referred by her "
          "primary care provider for short stature and no menstrual periods.")
C.notes("nn", "Nurses' Notes", ("0900",
    "Arrived with her mother for an endocrine evaluation. Mother reports that Chloe has always been the shortest student in her "
    "class and has not had a menstrual period or any breast development. Chloe is a strong student; she mentions difficulty with "
    "geometry and other visual-spatial math problems. No history of headaches, changes in vision, eating concerns or strenuous "
    "athletic training. Height 142 cm (below the 3rd percentile); weight 44 kg (15th percentile). Short, broad neck with bilateral "
    "webbing and a low posterior hairline. Broad chest with widely spaced nipples. Increased carrying angle at both elbows "
    "(cubitus valgus). Sexual maturity rating: Tanner stage 1 breasts, Tanner stage 2 pubic hair. Grade 2/6 systolic ejection murmur "
    "at the upper left sternal border, also heard between the scapulae. Brachial pulses 3+; femoral pulses 1+ bilaterally and "
    "delayed compared with the radial pulses. Pediatric endocrinologist notified."))
VS1_ROWS = [("T", "36.5–37.5° C"), ("P", "60–100 beats/min"), ("RR", "12–20 breaths/min"),
            ("BP, right arm", "below 120/80 mm Hg"), ("BP, right thigh", "equal to or 10–20 mm Hg above arm BP"),
            ("Pulse Oximetry Reading (SpO<sub>2</sub>)", "95%–100%")]
VS1 = {k: vrow(k, f"Expected: {e}") for k, e in VS1_ROWS}


def vitals5(col, t, p, rr, arm, thigh, spo2):
    C.column("vs", "Vital Signs", "", col, list(zip(VS1.values(), [t, p, rr, arm, thigh, spo2])))


vitals5("0900", "36.7° C", "82 beats/min", "16 breaths/min", "138/84 mm Hg", "98/60 mm Hg", "99% on room air")
c5s1 = screen(1, INTRO1, C, select_all(51, [
    ("A", "Height of 142 cm, below the 3rd percentile for age", True),
    ("B", "No breast development (Tanner stage 1) and no menstrual periods at age 15", True),
    ("C", "Webbed neck, low posterior hairline, and broad chest with widely spaced nipples", True),
    ("D", "Right arm BP 138/84 mm Hg, right thigh BP 98/60 mm Hg, and weak, delayed femoral pulses", True),
    ("E", "Difficulty with visual-spatial math despite strong overall grades", True),
    ("F", "Tanner stage 2 pubic hair", False),
    ("G", "No history of headaches or changes in vision", False),
    ("H", "Temperature 36.7° C and SpO₂ 99% on room air", False)],
    rationale(
        "<b>Consistent with Turner syndrome (45,X):</b> short stature is the most constant feature {A}. Streak ovaries make "
        "too little estrogen, so breasts do not develop and menstruation does not begin {B}. Lymphatic swelling before birth leaves a "
        "webbed neck and low hairline, with a broad, shield-like chest {C}.",
        "Higher blood pressure in the arms than in the legs, with weak, delayed femoral pulses, points to <b>coarctation of the "
        "aorta</b>, a heart defect common in Turner syndrome {D}. Normally, thigh BP is equal to or higher than arm BP.",
        "Intelligence is usually normal, but many girls with Turner syndrome have a specific difficulty with visual-spatial tasks "
        "such as geometry {E}.",
        "<b>Not consistent:</b> pubic hair comes from adrenal androgens (adrenarche), which Turner syndrome does not affect, so "
        "Tanner stage 2 pubic hair does not point to it {F}. No headaches or vision changes makes a pituitary tumor less likely as a "
        "cause of delayed puberty, but says nothing for or against Turner syndrome {G}. Temperature and SpO₂ are normal {H}."),
    stem="The nurse reviews the client's history and assessment. Which of the following findings would be consistent with "
         "<b>Turner syndrome</b>? Select all that apply."))

# Screen 2
C.notes("nn", "Nurses' Notes", ("1030 (Week 2)",
    "Follow-up visit with Chloe and her mother to review test results. The endocrinologist explains that the karyotype confirms "
    "Turner syndrome and that the echocardiogram shows a narrowing of the aorta and a bicuspid aortic valve. Mother asks, “How is "
    "Chloe's missing X different from conditions like Klinefelter syndrome? Did my husband or I pass a bad gene to her?”"))
C.rows("dx", "Diagnostic Results", ["Test", "Result (Week 2)"], [
    ["<b>Karyotype, peripheral blood</b>", "45,X in 20 of 20 cells counted"],
    [lab("Follicle-stimulating hormone (FSH)", "Female, midfollicular phase: 3.9–8.8 IU/L"), "78 IU/L"],
    [lab("Luteinizing hormone (LH)", "Female, midfollicular phase: 2.1–10.8 IU/L"), "34 IU/L"],
    [lab("Estradiol (E2)", "Female, follicular phase: 50–100 pmol/L"), "less than 37 pmol/L"],
    [lab("Creatinine", "Female: 22–75 µmol/L"), "54 µmol/L"],
    ["<b>Pelvic ultrasound</b>", "Small, prepubertal uterus. Bilateral streak gonads with no visible follicles."],
    ["<b>Echocardiogram</b>", "Discrete juxtaductal coarctation of the aorta, peak gradient 38 mm Hg. Bicuspid aortic valve. "
                              "Aortic root diameter normal for body size."],
    ["<b>Renal ultrasound</b>", "Horseshoe kidney with normal renal parenchyma."]])
c5s2 = screen(2, "Two weeks later, Chloe and her mother return to review the karyotype, hormone levels, pelvic ultrasound and "
                 "echocardiogram.", C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from 1030 (Week 2) and the Diagnostic Results.",
    "stem": "The nurse prepares teaching that compares sex chromosome disorders. For each characteristic, click to specify whether "
            "it applies to <b>Turner syndrome (45,X)</b>, <b>Klinefelter syndrome (47,XXY)</b>, or <b>both</b>.",
    "matrix": matrix_mc("Characteristic", ["Turner Syndrome (45,X)", "Klinefelter Syndrome (47,XXY)", "Both"], [
        ("45 chromosomes; short stature and webbed neck", 0),
        ("Primary gonadal failure with high FSH and LH, and infertility in most affected individuals", 2),
        ("47 chromosomes; tall stature, small firm testes, and gynecomastia", 1),
        ("Coarctation of the aorta, bicuspid aortic valve, and horseshoe kidney", 0),
        ("Usually arises by chance from an error in chromosome separation, not from an inherited single-gene mutation", 2),
        ("Low testosterone, sparse facial and body hair, and language-based learning difficulties", 1)]),
    "explanation": rationale(
        "<b>Turner syndrome (45,X):</b> one X chromosome is missing (monosomy X), so cells have 45 chromosomes. Loss of genes on the "
        "second X causes short stature, a webbed neck, a shield chest, streak ovaries, a horseshoe kidney, and heart defects "
        "(coarctation of the aorta, bicuspid aortic valve).",
        "<b>Klinefelter syndrome (47,XXY):</b> a male with an extra X chromosome (47 chromosomes). The testes become small and firm "
        "and make little testosterone, causing tall stature with long legs, gynecomastia, sparse body hair, infertility, and "
        "language-based learning difficulties.",
        "<b>Both:</b> each is a sex chromosome aneuploidy that usually arises by chance, from nondisjunction during gamete formation "
        "(or, in Turner syndrome, loss of an X chromosome in early cell divisions, which explains mosaic forms). Down syndrome "
        "(47,XX,+21 or 47,XY,+21) arises the same way, but involves an autosome (chromosome 21), not a sex chromosome. Both "
        "conditions cause primary gonadal failure: the gonads do not respond, so the pituitary releases more FSH and LH, and most "
        "affected people are infertile. The parents did not pass on a faulty gene."),
})

# Screen 3
C.notes("nn", "Nurses' Notes", ("1115 (Week 2)",
    "Pediatric cardiology reviewed the echocardiogram: moderate coarctation of the aorta with a bicuspid aortic valve. Repeat right "
    "arm BP 140/86 mm Hg. Chloe reports that her legs get tired when she climbs stairs. Bone age X-ray: 12.5 years, with open "
    "growth plates. Chloe asks quietly whether she will ever be able to have children."))
c5s3 = screen(3, "The nurse reviews Chloe's results with the endocrinologist and cardiologist to set care priorities.", C, {
    "type": "dropdown_cloze",
    "preamble": "The nurse has reviewed the Nurses' Notes from 1115 (Week 2).",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {"text": "Chloe's karyotype shows [[drop0]], which usually arises by chance. The nurse's priority is "
                      "[[drop1]]. Her absent breast development and menstrual periods are caused by [[drop2]].",
              "dropdowns": [
                  dd(5311, "monosomy X (45 chromosomes)", "an extra X chromosome (47,XXY)", "trisomy of chromosome 21",
                     "a single-gene mutation inherited from a carrier parent"),
                  dd(532, "high blood pressure in the arms from coarctation of the aorta",
                     "the risk of kidney injury from the horseshoe kidney",
                     "the limited time left for growth before the growth plates close",
                     "disturbed body image related to her short stature"),
                  dd(533, "streak ovaries that make little estrogen, so FSH and LH rise",
                     "a pituitary gland that releases too little FSH and LH",
                     "an absent uterus from abnormal development",
                     "low body weight suppressing the hypothalamus")]},
    "explanation": rationale(
        "<b>Monosomy X:</b> normal cells have 46 chromosomes (22 pairs of autosomes and one pair of sex chromosomes). In Turner "
        "syndrome one X is missing, leaving 45. An extra X (47,XXY) is Klinefelter syndrome, and trisomy 21 is Down syndrome.",
        "<b>Priority:</b> coarctation makes the left ventricle pump against a narrowed aorta. Her arm BP is rising (140/86 mm Hg) "
        "and her legs tire with exertion. Untreated, it leads to left ventricular hypertrophy, heart failure, and, with a bicuspid "
        "valve, aortic dilation and dissection. The horseshoe kidney (normal creatinine), her growth window and her body image all "
        "matter, but they are not a threat to her circulation now.",
        "<b>Cause of absent puberty:</b> high FSH and LH with low estradiol mean the problem lies in the ovaries (primary or "
        "hypergonadotropic hypogonadism): the pituitary is signalling hard and the streak ovaries cannot respond. A pituitary "
        "problem would give low FSH and LH. The ultrasound shows a uterus, and her weight (15th percentile) and lack of strenuous "
        "training do not suggest hypothalamic suppression."),
})

# Screen 4
C.notes("nn", "Nurses' Notes", ("1300 (Week 2)",
    "Interprofessional care conference. Cardiology plans transcatheter treatment of the coarctation and lifelong follow-up of the "
    "bicuspid aortic valve. Endocrinology plans daily growth hormone injections while the growth plates are open, then low-dose "
    "estrogen increased slowly over about 2 years, with a progestin added later. Chloe is quiet and tearful after hearing that she "
    "will most likely not be able to become pregnant with her own eggs."))
C.rows("plan", "Care Plan", ["Team", "Plan"], [
    ["<b>Pediatric cardiology</b>", "Transcatheter treatment of the coarctation (balloon angioplasty or stent). Echocardiogram or "
                                    "cardiac MRI at regular intervals for the bicuspid valve and aortic root."],
    ["<b>Pediatric endocrinology</b>", "Recombinant human growth hormone (rhGH) subcutaneously every evening. Low-dose transdermal "
                                       "estradiol, increased slowly; cyclic progestin added after breakthrough bleeding or about "
                                       "2 years of estrogen."],
    ["<b>Primary care</b>", "Yearly TSH and free T4; hearing tests; celiac disease screening; bone mineral density scan."],
    ["<b>Psychosocial and genetics</b>", "Counselling for body image and loss of fertility; genetic counselling about the sporadic "
                                         "cause and future options for having children."]])
c5s4 = screen(4, "The nurse works with cardiology, endocrinology and psychosocial services on Chloe's plan of care.", C,
    select_all(54, [
        ("A", "Arrange cardiology follow-up and teach the family that the aorta and heart valve need lifelong monitoring", True),
        ("B", "Teach Chloe and her mother how to give the daily subcutaneous growth hormone injection", True),
        ("C", "Explain that low-dose estrogen, increased slowly, will promote breast development and protect bone density", True),
        ("D", "Tell Chloe that once estrogen therapy starts, her ovaries will begin releasing eggs", False),
        ("E", "Acknowledge Chloe's feelings about fertility and offer a Turner syndrome peer support group", True),
        ("F", "Schedule screening for hypothyroidism, hearing loss, and celiac disease", True),
        ("G", "Teach Chloe how to give testosterone injections to speed up her growth", False)],
        rationale(
            "<b>Include:</b> coarctation and a bicuspid aortic valve need lifelong cardiology follow-up, even after repair {A}. "
            "Growth hormone works only while the growth plates are open, so daily injections start now; the nurse teaches the "
            "technique and site rotation {B}. Estrogen started at a low dose and increased slowly brings on breast development and "
            "protects bone without closing the growth plates too early {C}. Chloe is grieving the likely loss of fertility; "
            "acknowledging it and offering peer support helps her cope, and egg donation can be discussed later {E}. Turner "
            "syndrome raises the lifetime risk of autoimmune thyroid disease, hearing loss and celiac disease {F}.",
            "<b>Do not include:</b> estrogen replaces the hormone the ovaries cannot make, but it does not create egg follicles, so "
            "it does not restore fertility {D}. Testosterone treats the hormone deficit of males with Klinefelter syndrome; it has "
            "no place in Turner syndrome {G}."),
        preamble="The nurse has reviewed the Nurses' Notes from 1300 (Week 2) and the Care Plan.",
        stem="Which interventions should the nurse include in Chloe's plan of care? Select all that apply."))

# Screen 5
C.notes("nn", "Nurses' Notes", ("0930 (Week 6)",
    "Chloe returns to start endocrine therapy and for teaching before her coarctation procedure next week. Alert and cooperative. "
    "Mother asks whether Chloe can start “full adult-strength estrogen right away so she can catch up with her friends,” and "
    "whether Chloe's 11-year-old sister needs testing to see if she “carries the Turner gene.”"))
vitals5("Week 6 0930", "36.8° C", "80 beats/min", "16 breaths/min", "136/82 mm Hg", "96/58 mm Hg", "99% on room air")
c5s5 = screen(5, "Four weeks later, Chloe returns to the clinic.", C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from 0930 (Week 6) and the Vital Signs.",
    "stem": "For each nursing action, click to specify whether the action is <b>Indicated</b>, <b>Non-Essential</b>, or "
            "<b>Contraindicated</b>.",
    "matrix": matrix_mc("Nursing Action", IMC, [
        ("Measure BP in all four limbs and compare the radial and femoral pulses", 0),
        ("Tell Chloe that estrogen alone, without a progestin, can be taken long term", 2),
        ("Explain that estrogen starts at a low dose and is increased slowly to protect her final height", 0),
        ("Request a sweat chloride test to look for another cause of her short stature", 1),
        ("Explain that Turner syndrome usually occurs by chance and is not caused by a gene her sister could carry", 0),
        ("Tell Chloe that cardiology follow-up can stop once the coarctation is repaired", 2)]),
    "explanation": rationale(
        "<b>Measure BP in all four limbs (Indicated):</b> the arm-to-leg gradient (40 mm Hg today) and femoral pulses show how "
        "severe the coarctation is and give a baseline for judging the repair.",
        "<b>Estrogen alone long term (Contraindicated):</b> in anyone with a uterus, estrogen without a progestin causes "
        "endometrial hyperplasia and raises the risk of endometrial cancer. A cyclic progestin is added after breakthrough bleeding "
        "or about 2 years of estrogen.",
        "<b>Low dose, increased slowly (Indicated):</b> full adult doses early would close the growth plates quickly and cut short "
        "the height gained with growth hormone; a slow increase also gives more natural breast development.",
        "<b>Sweat chloride test (Non-Essential):</b> it diagnoses cystic fibrosis. Her short stature is explained by the 45,X "
        "karyotype; the test adds nothing.",
        "<b>Explain the sporadic cause (Indicated):</b> 45,X Turner syndrome is a chance error in chromosome separation, not a "
        "Mendelian gene, so her sister's risk is not increased and she does not need testing because of Chloe's diagnosis.",
        "<b>Stop cardiology follow-up after repair (Contraindicated):</b> after repair, people with Turner syndrome and a bicuspid "
        "valve remain at risk of re-narrowing, high blood pressure, and aortic dilation and dissection, so follow-up is lifelong."),
})

# Screen 6
C.notes("nn", "Nurses' Notes", ("1000 (Month 12)",
    "Twelve-month follow-up after transcatheter stent placement for the coarctation, 12 months of growth hormone and 6 months of "
    "low-dose transdermal estradiol. Chloe smiles and says she joined a Turner syndrome teen group. Gives her own rhGH injection "
    "each evening, rotating sites; no skin changes at injection sites. Chloe says she wants to understand her diagnosis before she "
    "moves to adult care."))
vitals5("Month 12 1000", "36.6° C", "74 beats/min", "14 breaths/min", "114/70 mm Hg", "118/72 mm Hg", "99% on room air")
C.rows("fu", "Follow-Up Results", ["Measure", "Baseline (age 15)", "Month 12 (age 16)"], [
    ["<b>Height</b>", "142.0 cm", "149.5 cm"],
    ["<b>Growth velocity</b>", "2.1 cm/year", "7.5 cm/year"],
    ["<b>Breast development</b>", "Tanner stage 1", "Tanner stage 2"],
    [lab("Thyrotropin (TSH)", "0.34–5.60 mIU/L"), "2.4 mIU/L", "2.8 mIU/L"],
    [lab("Thyroxine, free (FT4)", "7.0–17.0 pmol/L"), "13.1 pmol/L", "12.6 pmol/L"],
    ["<b>Echocardiogram</b>", "Coarctation, peak gradient 38 mm Hg; bicuspid aortic valve",
     "Stent in place, residual gradient 8 mm Hg; bicuspid aortic valve unchanged; aortic root normal"]])
c5s6 = screen(6, "Twelve months later, Chloe (now 16 years old) returns to the clinic.", C, {
    "type": "dropdown_cloze",
    "preamble": "The nurse has reviewed the Nurses' Notes from 1000 (Month 12), the Vital Signs, and the Follow-Up Results.",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {"text": "Chloe's growth velocity of 7.5 cm/year, equal arm and leg blood pressures, and Tanner stage 2 breast "
                      "development show [[drop0]]. When Chloe explains that her 45,X chromosome makeup is her [[drop1]] and "
                      "her short stature is her phenotype, she shows understanding. Before she moves to adult care, the nurse "
                      "confirms she understands that she needs [[drop2]].",
              "dropdowns": [
                  dd(561, "a positive response to the coarctation repair and hormone therapy",
                     "a normal growth spurt that would have happened without treatment",
                     "persistent coarctation that needs a repeat procedure",
                     "that growth hormone can now be stopped because she has reached adult height"),
                  dd(562, "genotype", "phenotype", "allele", "mutation"),
                  dd(563, "lifelong cardiology and endocrine follow-up",
                     "cardiology follow-up only until the stent has healed",
                     "endocrine follow-up only, since her heart is repaired",
                     "follow-up only if she plans a pregnancy")]},
    "explanation": rationale(
        "<b>Response to treatment:</b> growth velocity rose from 2.1 to 7.5 cm/year on growth hormone, the arm-to-leg BP gradient "
        "is gone (thigh BP now above arm BP, as expected), and estrogen has started breast development. Without treatment, girls "
        "with Turner syndrome do not have a pubertal growth spurt. She is still growing, so growth hormone continues until growth "
        "slows and the growth plates close. Treatment does not change the karyotype.",
        "<b>Genotype and phenotype:</b> the genotype is the genetic (here chromosomal) makeup, 45,X. The phenotype is what can be "
        "observed: short stature, webbed neck, streak ovaries.",
        "<b>Lifelong follow-up:</b> even after a good repair, she remains at risk of re-narrowing, hypertension and aortic "
        "dilation or dissection (higher in pregnancy), and needs ongoing estrogen and progestin, thyroid, hearing and bone "
        "monitoring as an adult."),
})
write_case("case_1782370000005", 5,
    "15-year-old female with short stature, no puberty, webbed neck and an arm-to-leg BP gradient: Turner syndrome (45,X) with "
    "coarctation of the aorta, compared with Klinefelter and Down syndromes, through endocrine and cardiac care.",
    [c5s1, c5s2, c5s3, c5s4, c5s5, c5s6],
    "Revised by Claude on 24 Nov 2026 from the author's draft (New Case Study 1). Please check: SI lab values and adult reference "
    "ranges for FSH, LH and estradiol; growth hormone started at a bone age of 12.5 years alongside estrogen; Tanner stage 2 pubic "
    "hair used as a distractor (adrenarche is normal in Turner syndrome).")

# =====================================================================================================
# Case Study 6: Sickle cell disease and Mendelian inheritance
# =====================================================================================================
C = Chart3()
INTRO2 = ("The nurse in the pediatric emergency department is assessing Marcus, a 6-year-old boy with sickle cell disease "
          "(HbSS), brought in by his parents for severe leg and lower-back pain.")
C.notes("nn", "Nurses' Notes",
    ("1400", "Marcus (diagnosed with sickle cell disease on newborn screening) arrives with his mother and father. Runny nose and "
     "mild cough for 2 days; has been drinking very little. Over the past 12 hours, worsening deep, throbbing pain in both thighs, "
     "knees and lower back; rates pain 8/10 on the FACES scale and refuses to walk. Irritable, guarding both legs. Mild scleral "
     "icterus and pale conjunctivae, which his mother says are “how his eyes usually look.” Oral mucous membranes dry; capillary "
     "refill 3 seconds. Lungs clear to auscultation bilaterally; no chest pain. Abdomen soft and non-tender; spleen not palpable. "
     "No focal neurologic deficits."),
    ("1415", "Family history: both parents are healthy and have sickle cell trait (HbAS). Marcus's mother says her 44-year-old "
     "brother was recently diagnosed with Huntington disease and asks whether Marcus could get it too. Marcus's father says his "
     "sister's 9-year-old son has hemophilia B. Pediatrician and hematology notified."))
VS6 = [vrow("T", "Expected: 36.5–37.5° C"), vrow("P", "Age 6: 75–115 beats/min"), vrow("RR", "Age 6: 18–25 breaths/min"),
       vrow("BP", "Age 6: 90–110/55–75 mm Hg"), vrow("Pulse Oximetry Reading (SpO<sub>2</sub>)", "Expected: 95%–100%"),
       vrow("Pain (FACES, 0–10)")]


def vitals6(col, *values):
    C.column("vs", "Vital Signs", "", col, list(zip(VS6, values)))


vitals6("1400", "38.3° C", "134 beats/min", "26 breaths/min", "102/62 mm Hg", "93% on room air", "8")
c6s1 = screen(1, INTRO2, C, select_all(61, [
    ("A", "Thigh, knee and lower-back pain rated 8/10, refusing to walk", True),
    ("B", "Temperature 38.3° C", True),
    ("C", "SpO₂ 93% on room air with RR 26 breaths/min", True),
    ("D", "Heart rate 134 beats/min", True),
    ("E", "Dry oral mucous membranes, capillary refill 3 seconds, and little fluid intake for 2 days", True),
    ("F", "Lungs clear to auscultation with no chest pain", False),
    ("G", "Spleen not palpable", False),
    ("H", "BP 102/62 mm Hg with no focal neurologic deficits", False)],
    rationale(
        "<b>Require follow-up:</b> deep bone and joint pain that stops a child walking is the hallmark of a <b>vaso-occlusive "
        "crisis</b>: sickled red cells block small vessels and the tissue becomes ischemic {A}. A temperature of 38.3° C is urgent "
        "in sickle cell disease: repeated splenic infarcts leave the spleen unable to clear encapsulated bacteria (functional "
        "asplenia), so fever can mean life-threatening bacteremia {B}. Low SpO₂ with a fast RR increases sickling and can be the "
        "start of acute chest syndrome {C}. Tachycardia reflects pain, fever, dehydration and anemia {D}. Dehydration raises blood "
        "viscosity and, with the viral illness, likely triggered this crisis {E}.",
        "<b>Do not require follow-up now:</b> clear lungs without chest pain make acute chest syndrome less likely at this moment, "
        "though it can develop later {F}. By school age, most children with HbSS have a small, scarred spleen that cannot be felt; a "
        "newly enlarged spleen would suggest splenic sequestration {G}. Normal BP and no focal deficits are reassuring; a sudden "
        "deficit would suggest a stroke {H}. The mild icterus and pallor are his usual signs of chronic hemolysis; his hemoglobin "
        "will be compared with his baseline."),
    stem="The nurse reviews the client's history and assessment. Which findings require follow-up? Select all that apply."))

# Screen 2
C.notes("nn", "Nurses' Notes", ("1500",
    "Laboratory results reviewed with hematology. Admitted to the pediatric unit for IV fluids, pain management and fever "
    "monitoring. Parents ask how sickle cell disease is inherited differently from Huntington disease and hemophilia B."))
LABS6 = [lab("Hemoglobin (Hgb)", "Age 6–11 years: 115–145 g/L"), lab("Reticulocyte percentage", "0.5%–1.5%"),
         lab("Bilirubin, total", "3–17 µmol/L"), lab("Bilirubin, direct (conjugated)", "2–9 µmol/L"),
         lab("White blood cell (WBC) count", "Age 6 years: 5.0–14.5 × 10<sup>9</sup>/L"), "<b>Peripheral blood smear</b>",
         "<b>Hemoglobin electrophoresis</b>"]
C.column("labs", "Laboratory Results", "Laboratory Test and Reference Range", "1440", list(zip(LABS6, [
    "72 g/L (his usual: 86 g/L)", "11.4%", "62 µmol/L", "7 µmol/L", "18.6 × 10<sup>9</sup>/L",
    "Sickled red blood cells, target cells, Howell-Jolly bodies", "At age 2: HbS 88%, HbF 10%, HbA<sub>2</sub> 2%, HbA 0%"])))
C.rows("fh", "Family History", ["Relative", "History"], [
    ["<b>Mother (34)</b>", "Healthy. Sickle cell trait (HbAS)."],
    ["<b>Father (36)</b>", "Healthy. Sickle cell trait (HbAS)."],
    ["<b>Maternal grandmother</b>", "Died at 58; involuntary movements and memory loss from her late 40s."],
    ["<b>Maternal uncle (44)</b>", "Huntington disease, diagnosed this year."],
    ["<b>Paternal aunt (38)</b>", "Healthy; no bleeding problems."],
    ["<b>Paternal aunt's son (9)</b>", "Hemophilia B (factor IX deficiency)."]])
c6s2 = screen(2, "Laboratory results return and the nurse reviews Marcus's family history with his parents.", C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from 1500, the Laboratory Results, and the Family History.",
    "stem": "For each finding, click to specify whether it is consistent with <b>autosomal dominant</b>, <b>autosomal "
            "recessive</b>, or <b>X-linked recessive</b> inheritance.",
    "matrix": matrix_mc("Family History Finding", ["Autosomal Dominant", "Autosomal Recessive", "X-Linked Recessive"], [
        ("Marcus has sickle cell disease although both of his parents are healthy", 1),
        ("Marcus's maternal grandmother and her son both developed a movement disorder in adulthood", 0),
        ("Marcus's father's sister is healthy, but her son has hemophilia B", 2),
        ("Each of Marcus's parents has one HbS allele and no symptoms", 1),
        ("Symptoms may not begin until mid-adulthood, often after the person has had children", 0),
        ("The disorder occurs almost only in males, who inherit the gene from their mothers", 2)]),
    "explanation": rationale(
        "<b>Autosomal recessive (sickle cell disease):</b> disease appears only with two mutated alleles (homozygous HbSS). "
        "Carriers (heterozygous HbAS) are healthy, so an affected child often has two unaffected parents. Marcus's results show "
        "active hemolysis: hemoglobin below his usual level, high reticulocytes (the marrow compensating) and high indirect "
        "bilirubin. Howell-Jolly bodies on the smear mean the spleen no longer filters the blood.",
        "<b>Autosomal dominant (Huntington disease):</b> one mutated allele causes the disease, so it appears in every generation "
        "(grandmother, then her son) and affects males and females alike. Because symptoms usually start between 30 and 50, people "
        "often have children before they know they carry it. Marcus's mother has a 50% chance of carrying the gene, so Marcus's "
        "own risk is 25% at present; predictive testing of children is not recommended and is left for him to decide as an adult.",
        "<b>X-linked recessive (hemophilia B):</b> the gene is on the X chromosome. Males have one X, so one mutated copy causes "
        "disease; females with one normal X are usually healthy carriers who pass it to half their sons. The paternal aunt is a "
        "carrier. Marcus's father is an unaffected male, so he does not carry the gene and cannot pass it to Marcus."),
})

# Screen 3
C.notes("nn", "Nurses' Notes", ("1600",
    "Transferred to the pediatric unit. Pain 8/10 despite acetaminophen given at home this morning. No chest pain; lungs clear. "
    "Spleen not palpable. Blood cultures drawn and IV access established. Parents ask, “Since we both carry the trait, what is the "
    "chance another baby would have sickle cell disease like Marcus?”"))
vitals6("1600", "38.6° C", "138 beats/min", "28 breaths/min", "100/60 mm Hg", "92% on room air", "8")
c6s3 = screen(3, "Marcus is admitted to the pediatric unit.", C, {
    "type": "dropdown_cloze",
    "preamble": "The nurse has reviewed the Nurses' Notes from 1600 and the Vital Signs.",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {"text": "Sickle cell disease is caused by a [[drop0]] in the beta-globin (HBB) gene. Given Marcus's temperature, "
                      "SpO₂ and respiratory rate, the nurse's priority is to prevent [[drop1]]. Because both parents are carriers "
                      "(HbAS), each future pregnancy has a [[drop2]] chance of a child with sickle cell disease.",
              "dropdowns": [
                  dd(6311, "point mutation (one base substituted)", "trinucleotide repeat expansion",
                     "nondisjunction of chromosome 11", "teratogenic exposure before birth"),
                  dd(632, "acute chest syndrome and sepsis", "splenic sequestration crisis", "ischemic stroke",
                     "acute kidney injury from dehydration"),
                  dd(633, "25% (1 in 4)", "50% (1 in 2)", "75% (3 in 4)", "67% (2 in 3)")]},
    "explanation": rationale(
        "<b>Point mutation:</b> a single base change in HBB puts valine in place of glutamic acid in beta-globin, creating the "
        "HbS allele. A trinucleotide (CAG) repeat expansion causes Huntington disease; nondisjunction causes aneuploidy such as "
        "Down syndrome; a teratogen damages development without changing the genes.",
        "<b>Priority:</b> fever of 38.6° C in a child without a working spleen can progress to overwhelming sepsis within hours, "
        "and falling SpO₂ (92%) with a rising RR (28 breaths/min) increases sickling in the lungs, the path to acute chest "
        "syndrome, the leading cause of death in sickle cell disease. A non-palpable spleen and normal neurologic findings do not "
        "point to sequestration or stroke now; dehydration is being treated with IV fluids.",
        "<b>25%:</b> HbAS × HbAS gives, with each pregnancy, 25% HbAA (unaffected, not a carrier), 50% HbAS (carrier) and 25% HbSS "
        "(affected). 50% is the chance of a carrier child, 75% the chance of an unaffected child, and 2 in 3 the chance that an "
        "unaffected sibling is a carrier."),
})

# Screen 4
C.notes("nn", "Nurses' Notes", ("1630",
    "Hematology admission orders received. Chest X-ray clear, no infiltrates. Marcus cries when his legs are moved and asks for a "
    "warm blanket."))
C.rows("orders", "Orders", ["Category", "Order"], [
    ["<b>Fluids</b>", "D5 0.45% NaCl IV at 1.25 times the maintenance rate. Encourage oral fluids."],
    ["<b>Pain</b>", "Morphine 0.1 mg/kg IV every 3 hours (scheduled). Ketorolac 0.5 mg/kg IV every 6 hours for up to 48 hours."],
    ["<b>Breathing</b>", "Oxygen by nasal cannula to keep SpO<sub>2</sub> 95% or higher. Incentive spirometry 10 breaths every "
                         "2 hours while awake."],
    ["<b>Infection and fever</b>", "Ceftriaxone 75 mg/kg IV every 24 hours (blood cultures drawn). Acetaminophen 15 mg/kg PO "
                                   "every 6 hours as needed for fever."],
    ["<b>Monitoring</b>", "Vital signs, SpO<sub>2</sub>, pain and sedation score every 2 hours. Spleen size every shift. CBC and "
                          "reticulocyte count every morning."]])
c6s4 = screen(4, "The nurse plans Marcus's care with the pediatric hospitalist and hematology team.", C,
    select_all(64, [
        ("A", "Run the IV fluids at the ordered rate and offer oral fluids often", True),
        ("B", "Give the scheduled morphine and ketorolac and reassess pain with the FACES scale", True),
        ("C", "Apply ice packs to the painful knees and lower back for 20 minutes every hour", False),
        ("D", "Give oxygen to keep SpO₂ at 95% or higher and coach incentive spirometry every 2 hours while awake", True),
        ("E", "Give the first dose of ceftriaxone without delay now that blood cultures are drawn", True),
        ("F", "Cover Marcus with a warm blanket and keep the room comfortably warm", True),
        ("G", "Request IV fluid boluses at twice the maintenance rate to flush out the sickled cells", False)],
        rationale(
            "<b>Include:</b> hydration lowers blood viscosity and slows sickling {A}. Vaso-occlusive pain is severe ischemic pain; "
            "scheduled opioid plus NSAID with regular reassessment controls it better than waiting for the child to ask {B}. Oxygen "
            "corrects hypoxemia, and incentive spirometry prevents the atelectasis that leads to acute chest syndrome, especially "
            "when opioids and splinting make breathing shallow {D}. With functional asplenia, a febrile child receives IV "
            "antibiotics promptly once cultures are drawn {E}. Warmth dilates vessels and eases pain {F}.",
            "<b>Do not include:</b> cold causes vasoconstriction, which slows blood flow and worsens sickling {C}. Fluids are given "
            "at about 1 to 1.5 times maintenance once dehydration is corrected; overhydration can cause pulmonary edema and "
            "trigger acute chest syndrome {G}."),
        preamble="The nurse has reviewed the Nurses' Notes from 1630 and the Orders.",
        stem="Which interventions should the nurse include in Marcus's plan of care? Select all that apply."))

# Screen 5
C.notes("nn", "Nurses' Notes", ("2200",
    "Pain 4/10 (FACES); resting with a warm blanket. Oxygen 1 L/min by nasal cannula. Completed 10 incentive spirometer breaths "
    "with coaching. Urine output 1.8 mL/kg/hour. Lungs clear; no chest pain; no sudden pallor. Sedation score: awake and alert."))
vitals6("2200", "37.8° C", "108 beats/min", "22 breaths/min", "98/58 mm Hg", "97% on 1 L/min nasal cannula", "4")
c6s5 = screen(5, "It is 2200. Marcus has received IV fluids, ceftriaxone and scheduled morphine.", C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from 2200 and the Vital Signs.",
    "stem": "For each nursing action, click to specify whether the action is <b>Indicated</b>, <b>Non-Essential</b>, or "
            "<b>Contraindicated</b>.",
    "matrix": matrix_mc("Nursing Action", IMC, [
        ("Request IV meperidine for breakthrough pain", 2),
        ("Monitor for new chest pain, cough, fast breathing or falling SpO₂", 0),
        ("Request a repeat hemoglobin electrophoresis each morning", 1),
        ("Check the spleen size and watch for sudden pallor or a drop in hemoglobin", 0),
        ("Place ice packs on the thighs and lower back between morphine doses", 2),
        ("Assess respiratory rate and sedation level before and after each morphine dose", 0)]),
    "explanation": rationale(
        "<b>Meperidine (Contraindicated):</b> its metabolite normeperidine accumulates with repeated doses and lowers the seizure "
        "threshold; it is not used for sickle cell pain.",
        "<b>Watch for acute chest syndrome (Indicated):</b> it often develops 24 to 72 hours into an admission for a pain crisis: "
        "new chest pain, cough, fever, tachypnea, falling SpO₂ and a new infiltrate on X-ray.",
        "<b>Daily electrophoresis (Non-Essential):</b> his HbSS genotype does not change; the daily CBC and reticulocyte count "
        "track the anemia.",
        "<b>Spleen and pallor (Indicated):</b> splenic sequestration (sudden spleen enlargement trapping blood) and aplastic crisis "
        "(often after parvovirus B19) both cause a rapid fall in hemoglobin and need emergency care.",
        "<b>Ice packs (Contraindicated):</b> cold causes vasoconstriction and more sickling.",
        "<b>Respiratory rate and sedation (Indicated):</b> opioid-induced hypoventilation would worsen hypoxemia and sickling; "
        "increasing sedation comes before respiratory depression."),
})

# Screen 6
C.notes("nn", "Nurses' Notes", ("Day 3 1000",
    "Walking in the hallway without guarding; pain 1/10 on oral ibuprofen. Afebrile for 24 hours; blood cultures negative at 48 "
    "hours. Hematology recommends starting daily oral hydroxyurea, which the parents declined last year; they now agree. "
    "Discharge home today with hematology follow-up in 2 weeks. The nurse reviews the discharge plan with the parents."))
vitals6("Day 3 1000", "36.8° C", "96 beats/min", "20 breaths/min", "100/62 mm Hg", "98% on room air", "1")
C.column("labs", "Laboratory Results", "Laboratory Test and Reference Range", "Day 3 0600", list(zip(LABS6[:5], [
    "83 g/L", "9.2%", "41 µmol/L", "6 µmol/L", "11.2 × 10<sup>9</sup>/L"])))
C.rows("dc", "Discharge Plan", ["Area", "Plan"], [
    ["<b>Hydroxyurea</b>", "Once daily by mouth. CBC every 4 weeks at first (the dose is adjusted to blood counts). Handle "
                           "capsules with gloves or wash hands after."],
    ["<b>Infection</b>", "Pneumococcal, meningococcal and yearly influenza vaccines up to date. Go to the emergency department for "
                         "a temperature of 38.5° C or higher."],
    ["<b>Preventing crises</b>", "Plenty of fluids every day; avoid getting cold or overheated; dress warmly; rest when tired."],
    ["<b>Genetics</b>", "Genetic counselling offered to the parents about future pregnancies and to Marcus's mother about "
                        "Huntington disease in her family."]])
c6s6 = screen(6, "On hospital day 3, Marcus is ready for discharge.", C, {
    "type": "dropdown_cloze",
    "preamble": "The nurse has reviewed the Nurses' Notes from Day 3 1000, the Vital Signs, the Laboratory Results, and the "
                "Discharge Plan.",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {"text": "The parents show understanding when they say they will bring Marcus to the emergency department for "
                      "[[drop0]]. They understand that hydroxyurea prevents crises by [[drop1]]. Marcus's mother understands "
                      "that if she carries the Huntington disease gene, each of her children has [[drop2]] of inheriting it.",
              "dropdowns": [
                  dd(661, "a temperature of 38.5° C or higher, chest pain, fast breathing or sudden pallor",
                     "leg pain of 3/10 that eases with fluids, rest and ibuprofen",
                     "a runny nose with a normal temperature",
                     "yellow-tinged eyes that look the same as usual"),
                  dd(662, "raising fetal hemoglobin (HbF), which keeps HbS from polymerizing",
                     "replacing the HbS allele with a normal beta-globin allele",
                     "thinning the blood the way an anticoagulant does",
                     "restoring the spleen's ability to filter bacteria"),
                  dd(663, "a 50% chance, whether the child is a boy or a girl", "a 25% chance, the same as sickle cell disease",
                     "a 50% chance for sons and no chance for daughters",
                     "no chance unless she develops symptoms herself")]},
    "explanation": rationale(
        "<b>When to come to the emergency department:</b> fever of 38.5° C or higher (sepsis risk without a working spleen), chest "
        "pain, cough or fast breathing (acute chest syndrome), sudden pallor, weakness or an enlarging abdomen (splenic "
        "sequestration or aplastic crisis), any neurologic change (stroke), priapism, or pain not relieved at home. Mild pain that "
        "settles with home measures, a cold without fever, and his usual mild icterus can be managed at home.",
        "<b>Hydroxyurea:</b> it raises fetal hemoglobin (HbF), which does not polymerize and dilutes HbS inside the red cell, so "
        "cells sickle less; crises, acute chest syndrome and transfusions become less frequent. It does not change his genes. It can "
        "lower blood counts, so CBCs are monitored.",
        "<b>Autosomal dominant inheritance:</b> one mutated allele is enough, so a parent who carries the gene passes it to each "
        "child with a 50% chance, regardless of sex. Carriers develop symptoms later in life, so not yet having symptoms does not "
        "rule it out. 25% applies to two carriers of a recessive condition; sex-limited risk applies to X-linked conditions."),
})
write_case("case_1782370000006", 6,
    "6-year-old boy with sickle cell disease (HbSS) in a vaso-occlusive crisis with fever; carrier parents and a family history "
    "of Huntington disease and hemophilia B, comparing autosomal recessive, autosomal dominant and X-linked recessive inheritance.",
    [c6s1, c6s2, c6s3, c6s4, c6s5, c6s6],
    "Revised by Claude on 24 Nov 2026 from the author's draft (New Case Study 2). Please check: pediatric reference ranges "
    "(hemoglobin 115–145 g/L, WBC 5.0–14.5 × 10⁹/L, vital signs for age 6); fluid rate 1.25 × maintenance and fever threshold "
    "38.5° C against local sickle cell protocols; hydroxyurea started at discharge after earlier refusal.")

# =====================================================================================================
# Case Study 7: Teratogens and multifactorial disorders
# =====================================================================================================
C = Chart3()
INTRO3 = ("The nurse in a maternal-fetal medicine clinic is completing a first prenatal visit for Elena, a 28-year-old client "
          "(G1P0) at 10 weeks and 2 days of gestation.")
C.notes("nn", "Nurses' Notes",
    ("0900", "First prenatal visit; positive home pregnancy test 4 weeks ago. Dating ultrasound this morning: single live "
     "intrauterine pregnancy, 10 weeks 2 days. Juvenile myoclonic epilepsy controlled with valproic acid 500 mg PO twice daily; "
     "seizure-free for 2 years. Did not take folic acid before conception. Took isotretinoin 40 mg PO daily for severe cystic acne "
     "until 6 weeks of gestation, stopping when her pregnancy test was positive. Works at a preschool; never received the MMR "
     "vaccine. At 5 weeks of gestation, during a confirmed rubella outbreak at work, she had 3 days of low-grade fever, swollen "
     "lymph nodes behind her ears and a fine pink rash. Started a prenatal vitamin with iron at 10 weeks. Denies alcohol, tobacco "
     "and drug use. BMI 23.2 kg/m<sup>2</sup>."),
    ("0920", "Family history: her partner's sister's son was born with spina bifida. Elena is anxious and asks, “Did these "
     "medicines and that rash change my baby's DNA? Should I stop my seizure pills right now?” Maternal-fetal medicine specialist "
     "notified."))
VS7 = [vrow("T"), vrow("P"), vrow("RR"), vrow("BP"), vrow("Pulse Oximetry Reading (SpO<sub>2</sub>)")]


def vitals7(col, *values):
    C.column("vs", "Vital Signs", "", col, list(zip(VS7, values)))


vitals7("0900", "36.8° C", "78 beats/min", "16 breaths/min", "114/70 mm Hg", "99% on room air")
c7s1 = screen(1, INTRO3, C, select_all(71, [
    ("A", "Isotretinoin 40 mg daily until 6 weeks of gestation", True),
    ("B", "No MMR vaccine, with fever, rash and swollen nodes behind the ears at 5 weeks of gestation", True),
    ("C", "Valproic acid 500 mg twice daily throughout early pregnancy", True),
    ("D", "No folic acid before conception", True),
    ("E", "Partner's sister's son was born with spina bifida", True),
    ("F", "Age 28 years, first pregnancy", False),
    ("G", "BP 114/70 mm Hg and BMI 23.2 kg/m²", False),
    ("H", "Started a prenatal vitamin with iron at 10 weeks", False)],
    rationale(
        "<b>Risk factors:</b> isotretinoin (a vitamin A derivative) is one of the most potent known teratogens {A}. Rubella "
        "infection in early pregnancy can cross the placenta and cause congenital rubella syndrome; the rash, fever and "
        "posterior auricular nodes during an outbreak in a non-immune client suggest primary infection {B}. Valproic acid raises the "
        "risk of neural tube defects and other malformations and impairs brain development {C}. Folic acid taken before conception "
        "lowers the risk of neural tube defects; she had none, while taking a folate antagonist {D}. Neural tube defects are "
        "multifactorial: a relative with spina bifida (here, a cousin of the baby) adds some genetic susceptibility {E}.",
        "<b>Timing:</b> gestational age is counted from the last menstrual period, about 2 weeks before conception. The embryonic "
        "period, when organs form, runs from about 3 to 8 weeks after conception, or about 5 to 10 weeks of gestation. Her rubella "
        "infection, isotretinoin and valproic acid all overlapped it.",
        "<b>Not risk factors:</b> age 28 does not raise the risk of chromosomal conditions the way maternal age over 35 does {F}. "
        "BP and BMI are normal {G}. Starting a prenatal vitamin is healthy, though too late to prevent a neural tube defect {H}."),
    stem="The nurse reviews the client's history and assessment. Which findings are risk factors for a congenital anomaly in "
         "this pregnancy? Select all that apply."))

# Screen 2
C.notes("nn", "Nurses' Notes", ("1100",
    "Prenatal laboratory results reviewed with the maternal-fetal medicine specialist, who explains the possible effects of each "
    "exposure and plans detailed fetal assessment. Elena has had no seizures."))
LABS7 = [lab("Rubella IgM", "Negative"), lab("Rubella IgG avidity", "High avidity: past infection or immunization"),
         lab("Valproic acid", "350–700 µmol/L"), lab("Folate (folic acid)", "≥ 10.0 nmol/L")]
C.column("labs", "Laboratory Results", "Laboratory Test and Reference Range", "0930",
         list(zip(LABS7, ["Positive", "Low avidity", "471 µmol/L", "9.5 nmol/L"])))
c7s2 = screen(2, "Elena's prenatal laboratory results return.", C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from 1100 and the Laboratory Results.",
    "stem": "The nurse prepares teaching about the possible effects of each exposure. For each fetal or newborn finding, click to "
            "specify whether it is most closely associated with <b>isotretinoin</b>, <b>rubella virus</b>, or "
            "<b>valproic acid</b>.",
    "matrix": matrix_mc("Fetal or Newborn Finding", ["Isotretinoin", "Rubella Virus", "Valproic Acid"], [
        ("Lumbosacral myelomeningocele", 2),
        ("Cataracts and sensorineural hearing loss", 1),
        ("Small or absent external ears and a small jaw", 0),
        ("Patent ductus arteriosus and purple “blueberry muffin” skin lesions", 1),
        ("Conotruncal heart defect with a small thymus", 0),
        ("Lower IQ and higher rates of autism spectrum disorder in childhood", 2)]),
    "explanation": rationale(
        "<b>Isotretinoin:</b> a retinoid that disrupts neural crest cells, which form much of the face, ears, thymus and the "
        "heart's outflow tract. Typical findings are small or absent ears (microtia, anotia), a small jaw, conotruncal heart "
        "defects (such as tetralogy of Fallot), thymic hypoplasia and brain malformations.",
        "<b>Rubella virus:</b> a TORCH infection. Positive IgM with low-avidity IgG confirms a recent primary infection. Infection in "
        "the first trimester can cause congenital rubella syndrome: cataracts, sensorineural hearing loss and heart defects "
        "(especially patent ductus arteriosus), with growth restriction, microcephaly and purpuric skin lesions in the newborn.",
        "<b>Valproic acid:</b> antagonizes folate and disrupts neural tube closure, raising the risk of spina bifida "
        "(myelomeningocele) about tenfold; it also impairs brain development throughout pregnancy, lowering IQ and increasing autism "
        "spectrum disorder. Her level is therapeutic and her folate is low."),
})

# Screen 3
C.notes("nn", "Nurses' Notes", ("1145",
    "Elena is tearful: “Should I throw away my valproic acid tonight so I don't hurt the baby any more? And if the baby has a birth "
    "defect from the acne pills or the rubella, will the baby pass it on to their own children?” The nurse stays with Elena and "
    "answers her questions."))
c7s3 = screen(3, "The nurse responds to Elena's questions.", C, {
    "type": "dropdown_cloze",
    "preamble": "The nurse has reviewed the Nurses' Notes from 1145.",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {"text": "Isotretinoin, rubella virus and valproic acid are each a [[drop0]]: an outside agent that disrupts "
                      "development without changing the genes the child will pass on. Because Elena's exposures occurred during "
                      "[[drop1]], the main risk is a structural malformation. The nurse's priority regarding valproic acid is "
                      "[[drop2]].",
              "dropdowns": [
                  dd(731, "teratogen", "mutagen", "mutation", "allele"),
                  dd(732, "the embryonic period (3 to 8 weeks after conception)",
                     "the pre-implantation period (first 2 weeks after conception)",
                     "the fetal period (from 9 weeks after conception)", "the third trimester"),
                  dd(733, "advising her not to stop it on her own and arranging a prompt neurology review",
                     "advising her to stop it tonight because it is a known teratogen",
                     "advising her to skip doses on days she feels well to lower fetal exposure",
                     "reassuring her that the risk ended once the neural tube closed")]},
    "explanation": rationale(
        "<b>Teratogen:</b> an outside agent (medicine, infection, alcohol, radiation) that causes a congenital anomaly by "
        "disrupting development. The child's genes are unchanged, so the anomaly is not passed on to the child's own children. A "
        "mutagen changes DNA, and a mutation is a change in DNA.",
        "<b>Embryonic period:</b> about 3 to 8 weeks after conception (5 to 10 weeks of gestation), when the organs form, so "
        "exposures cause major structural malformations. Exposures in the first 2 weeks tend to have an all-or-none effect "
        "(pregnancy loss or no harm); in the fetal period they mainly affect growth and function, including brain development.",
        "<b>Valproic acid:</b> stopping an antiseizure medicine abruptly can cause seizures or status epilepticus, with maternal "
        "and fetal hypoxia, injury or pregnancy loss. Skipping doses has the same danger. The neural tube closes about 28 days after "
        "conception, but valproic acid still affects the developing brain, so its use is reviewed promptly by neurology. Any "
        "change is directed and supervised by the neurologist."),
})

# Screen 4
C.notes("nn", "Nurses' Notes", ("1330",
    "Neurology consultation completed: the neurologist begins a supervised change from valproic acid to levetiracetam, with "
    "seizure precautions and close follow-up. The maternal-fetal medicine specialist prescribes folic acid 4 mg PO daily and plans "
    "maternal serum alpha-fetoprotein (MSAFP) at 16 weeks and a detailed anatomy ultrasound and fetal echocardiogram at 18 to 20 "
    "weeks. A genetic counsellor will meet Elena and her partner."))
C.rows("plan", "Care Plan", ["Team", "Plan"], [
    ["<b>Maternal-fetal medicine</b>", "Confirm isotretinoin stopped and remaining capsules returned to the pharmacy. Folic acid "
                                       "4 mg PO daily. MSAFP at 16 weeks; detailed anatomy ultrasound and fetal echocardiogram "
                                       "at 18 to 20 weeks."],
    ["<b>Neurology</b>", "Supervised change from valproic acid to levetiracetam; seizure precautions; follow-up every 4 weeks."],
    ["<b>Genetic counselling</b>", "Non-directive counselling about the risks for this pregnancy, testing options and support."],
    ["<b>Prenatal nursing</b>", "Teaching on avoiding further teratogens (alcohol, tobacco, unnecessary radiation). MMR vaccine "
                                "after delivery."]])
c7s4 = screen(4, "The nurse works with maternal-fetal medicine, neurology and genetic counselling on Elena's plan of care.", C,
    select_all(74, [
        ("A", "Confirm that Elena has stopped isotretinoin and returns any remaining capsules to the pharmacy", True),
        ("B", "Reinforce that Elena follows the neurologist's medication change plan rather than stopping on her own", True),
        ("C", "Give the MMR vaccine today to protect the fetus from further rubella effects", False),
        ("D", "Teach Elena to take folic acid 4 mg daily and keep her MSAFP, anatomy ultrasound and fetal echocardiogram "
              "appointments", True),
        ("E", "Offer non-directive emotional support and confirm the genetic counselling appointment", True),
        ("F", "Teach Elena to avoid alcohol, tobacco, and unnecessary X-rays or CT scans for the rest of the pregnancy", True),
        ("G", "Tell Elena to stop all seizure medicines until after the baby is born", False)],
        rationale(
            "<b>Include:</b> confirming that isotretinoin has stopped prevents further exposure {A}. Following the neurologist's "
            "supervised plan protects mother and fetus from seizures {B}. Folic acid 4 mg daily is recommended in pregnancy for "
            "clients taking antiseizure medicines; it can no longer prevent a neural tube defect that would already have formed, so "
            "MSAFP and the anatomy ultrasound check for one, and the fetal echocardiogram checks the heart {D}. Non-directive "
            "counselling supports Elena while respecting her own decisions {E}. Avoiding alcohol (fetal alcohol spectrum disorder), "
            "tobacco (growth restriction) and unnecessary radiation prevents further harm {F}.",
            "<b>Do not include:</b> MMR is a live vaccine and is not given in pregnancy; it cannot treat an infection that has "
            "already occurred. A non-immune client receives it after delivery {C}. Stopping antiseizure medicine risks "
            "life-threatening seizures {G}."),
        preamble="The nurse has reviewed the Nurses' Notes from 1330 and the Care Plan.",
        stem="Which interventions should the nurse include in Elena's plan of care? Select all that apply."))

# Screen 5
C.notes("nn", "Nurses' Notes", ("1015 (14 weeks)",
    "Seizure-free during the change to levetiracetam; taking folic acid 4 mg daily. Fetal heart rate 152 beats/min by Doppler. "
    "Elena asks whether she could have “a CT scan for a clearer picture of the baby,” and whether her own chromosomes should be "
    "tested to see if the isotretinoin damaged them."))
vitals7("1015 (14 weeks)", "36.7° C", "82 beats/min", "16 breaths/min", "110/68 mm Hg", "99% on room air")
c7s5 = screen(5, "At 14 weeks of gestation, Elena returns for prenatal follow-up.", C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Nurses' Notes from 1015 (14 weeks) and the Vital Signs.",
    "stem": "For each nursing action, click to specify whether the action is <b>Indicated</b>, <b>Non-Essential</b>, or "
            "<b>Contraindicated</b>.",
    "matrix": matrix_mc("Nursing Action", IMC, [
        ("Give the MMR vaccine today so Elena becomes immune to rubella", 2),
        ("Reinforce taking levetiracetam as prescribed and reporting any seizure activity", 0),
        ("Request a maternal karyotype to check whether isotretinoin changed Elena's chromosomes", 1),
        ("Request an abdominal CT scan to give Elena a clearer picture of the baby", 2),
        ("Confirm the dates of the MSAFP, detailed anatomy ultrasound and fetal echocardiogram", 0),
        ("Document a reminder to give the MMR vaccine after delivery", 0)]),
    "explanation": rationale(
        "<b>MMR today (Contraindicated):</b> live vaccines (MMR, varicella) are not given in pregnancy because of the theoretical "
        "risk to the fetus.",
        "<b>Seizure control (Indicated):</b> stable seizure control during and after the medication change prevents maternal and "
        "fetal hypoxia and injury.",
        "<b>Maternal karyotype (Non-Essential):</b> isotretinoin is a teratogen: it disrupts the embryo's development and does not "
        "change the mother's chromosomes. A karyotype would add nothing.",
        "<b>CT for a clearer picture (Contraindicated):</b> CT exposes the fetus to ionizing radiation, a physical teratogen, "
        "without any benefit here. Fetal anatomy is assessed with ultrasound (and MRI without gadolinium if needed). A single "
        "diagnostic CT is below the dose linked to malformations, so it is not withheld when truly needed, but it is never done for "
        "a picture of the baby.",
        "<b>Screening dates (Indicated):</b> MSAFP screens for open neural tube defects; the detailed anatomy ultrasound and fetal "
        "echocardiogram look for structural and heart defects.",
        "<b>MMR after delivery (Indicated):</b> it is safe during breastfeeding and protects future pregnancies from congenital "
        "rubella."),
})

# Screen 6
C.notes("nn", "Nurses' Notes", ("1400 (20 weeks)",
    "Results reviewed with Elena and her partner. Elena remains seizure-free on levetiracetam. The nurse reviews what Elena has "
    "learned about the causes of congenital anomalies and planning for a future pregnancy."))
C.rows("mfm", "Diagnostic Results", ["Test", "Result", "Plan"], [
    ["<b>MSAFP (16 weeks)</b><br>Below 2.5 MoM", "1.1 MoM", "None"],
    ["<b>Detailed anatomy ultrasound (19 weeks)</b>", "Spine and skull intact. Estimated fetal weight at the 12th percentile, "
                                                      "symmetric.", "Growth ultrasound every 4 weeks"],
    ["<b>Fetal echocardiogram (19 weeks)</b>", "Small muscular ventricular septal defect; normal outflow tracts.",
     "Pediatric cardiology assessment after birth"],
    ["<b>Newborn plan</b>", "First-trimester maternal rubella", "Newborn rubella PCR and IgM, hearing test and eye examination at "
                                                                "birth"]])
c7s6 = screen(6, "At 20 weeks of gestation, Elena returns to review her test results.", C, {
    "type": "dropdown_cloze",
    "preamble": "The nurse has reviewed the Nurses' Notes from 1400 (20 weeks) and the Diagnostic Results.",
    "stem": "Complete the following sentences by choosing from the lists of options.",
    "cloze": {"text": "Elena shows understanding of her partner's family history when she describes spina bifida as [[drop0]]. "
                      "To lower the risk of a congenital anomaly in a future pregnancy, Elena states she will [[drop1]]. She "
                      "correctly explains that an anomaly caused by a teratogen [[drop2]].",
              "dropdowns": [
                  dd(7611, "multifactorial: several genes interacting with factors such as folate",
                     "autosomal recessive: both parents must be carriers",
                     "X-linked recessive: passed from carrier mothers to sons",
                     "chromosomal: caused by an extra chromosome"),
                  dd(762, "take folic acid and review her seizure medicine with neurology before trying to conceive",
                     "stop her seizure medicine as soon as she has a positive pregnancy test",
                     "get the MMR vaccine early in her next pregnancy, once it is confirmed",
                     "rely on an early ultrasound in her next pregnancy to prevent birth defects"),
                  dd(763, "is not passed on to the child's own children",
                     "is passed on to half of the child's children",
                     "will happen again in each of her future pregnancies",
                     "changes the child's karyotype")]},
    "explanation": rationale(
        "<b>Multifactorial:</b> neural tube defects, cleft lip and palate and many heart defects come from several genes plus "
        "environmental factors (low folate, valproic acid, maternal diabetes). They do not follow Mendelian ratios; the risk rises "
        "modestly with each affected relative. Normal MSAFP and an intact spine on ultrasound make a neural tube defect very "
        "unlikely in this pregnancy.",
        "<b>Before the next pregnancy:</b> organs form 3 to 8 weeks after conception, often before a pregnancy is known, so "
        "prevention starts before conception: folic acid, a neurology review of antiseizure medicines, confirmed rubella immunity "
        "(MMR at least 4 weeks before conceiving, never during pregnancy), two forms of contraception during any isotretinoin "
        "treatment, and no alcohol. Stopping medicine abruptly is dangerous, and ultrasound detects anomalies but cannot prevent "
        "them.",
        "<b>Not inherited:</b> a teratogen changes development, not the child's genes, so the anomaly is not passed to the next "
        "generation. It recurs in a later pregnancy only if the exposure recurs. The ventricular septal defect and mild growth lag "
        "may relate to rubella or isotretinoin; the newborn will be assessed at birth."),
})
write_case("case_1782370000007", 7,
    "28-year-old client at 10 weeks of gestation exposed to isotretinoin, primary rubella and valproic acid, with a family history "
    "of spina bifida: teratogens versus mutations, timing of exposure, multifactorial disorders and preconception prevention.",
    [c7s1, c7s2, c7s3, c7s4, c7s5, c7s6],
    "Revised by Claude on 24 Nov 2026 from the author's draft (New Case Study 3). Clinician review needed: switching from valproic "
    "acid to levetiracetam at 10 weeks of gestation (practice varies once organogenesis is largely over; kept from the author's "
    "draft, framed as the neurologist's decision); folic acid 4 mg daily for clients on antiseizure medicines (Canadian guidance); "
    "the CT rationale (single diagnostic CT below the 50 mGy threshold).")
