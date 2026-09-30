"""University of Maryland - CS11: End-stage renal disease and dialysis (peritonitis on peritoneal dialysis), with its
stand-alone bow-tie (septicemia in a client on hemodialysis).
Source: "End Stage Renal Disease and Dialysis DOCX" (medical-surgical); Laura Sessions, PhD, MScN, RN, CNE, Towson
University; September 1, 2022.
Usage: python3 drafts/build_umd_cs11.py
"""
from umd_common import *  # noqa: F401,F403

N = 11
S = f"{N:02d}"
AUTH = "Laura Sessions, PhD, MScN, RN, CNE, Towson University"
FN = footnote("End Stage Renal Disease and Dialysis", AUTH)
FN_B = footnote("End Stage Renal Disease and Dialysis", AUTH,
                kind="medical-surgical faculty case study, stand-alone bow-tie", si=False)

ADMIT = paras(
    "35-year-old female client diagnosed with chronic glomerulonephritis 5 years ago. Chronic kidney disease progressed "
    "to end-stage renal disease (ESRD) over the last year. Automated peritoneal dialysis started 6 months ago. Developed "
    "fever, vomiting, and abdominal pain 1 day ago.",
    "<b>Current assessment:</b> T 39.1&deg;C (102.4&deg;F), HR 104, RR 16, BP 145/87. Weight 66.8 kg (147 lb). No known "
    "drug allergies. Periumbilical tenderness with guarding and rebound. Erythema and creamy yellow exudate around the "
    "peritoneal dialysis catheter exit site. Dialysate effluent is cloudy yellow. Peritoneal effluent culture obtained. "
    "Labs sent.")

LABS = table(["Laboratory Test and Reference Range", "Admission"], [
    [lab("Urea (BUN)", "3.6&ndash;7.1 mmol/L"), "16.4 mmol/L"],
    [lab("Creatinine", "80&ndash;124 &micro;mol/L"), "946 &micro;mol/L"],
    [lab("C-reactive protein", "&lt; 10 mg/L"), "61.5 mg/L"],
    [lab("Albumin", "34&ndash;54 g/L"), "37 g/L"],
    [lab("Potassium", "3.5&ndash;5.0 mmol/L"), "5.86 mmol/L"],
    [lab("Sodium", "135&ndash;145 mmol/L"), "144 mmol/L"],
    [lab("Calcium, total", "2.15&ndash;2.57 mmol/L"), "1.97 mmol/L"],
    [lab("Phosphate", "0.90&ndash;1.45 mmol/L"), "1.87 mmol/L"],
    [lab("Hemoglobin (Hgb)", "Female: 120&ndash;160 g/L"), "106 g/L"],
    [lab("Hematocrit (Hct)", "Female: 0.35&ndash;0.47 L/L"), "0.31 L/L"],
    [lab("White blood cell (WBC) count, serum", "4.5&ndash;10.5" + G9), "14.22" + G9],
    [lab("Neutrophils, serum", "0.55&ndash;0.70 (55&ndash;70%)"), "0.898 (89.8%)"],
    [lab("WBC count, dialysate", "Few"), "483 &times; 10<sup>6</sup>/L (483 cells/&micro;L)"],
    [lab("Polymorphonuclear cells, dialysate", "Few"), "63%"],
])
MICRO = paras("<b>Type of sample:</b> dialysate effluent.", "<b>Preliminary visual report:</b> gram-negative rods.")


def tabs(step):
    t = [{"id": f"adm_umd{S}", "title": "Admission Note", "content": ADMIT},
         {"id": f"labs_umd{S}", "title": "Laboratory Results", "content": LABS}]
    if step >= 4:
        t.append({"id": f"micro_umd{S}", "title": "Microbiology", "content": MICRO})
    return t


INTRO = ("A 35-year-old female client with end-stage renal disease on peritoneal dialysis is admitted to the "
         "medical-surgical unit with abdominal pain and fever.")

screens = [
    (INTRO, tabs(1), {
        "type": "select_n", "limit": 5,
        "stem": "Select the <b>5</b> findings that are <b>most</b> concerning.",
        "options": opts(("Heart rate", 0), ("Temperature", 1), ("Respiratory rate", 0), ("Blood pressure", 0),
                        ("Periumbilical tenderness", 1), ("Peritoneal dialysis catheter exit site", 1), ("Urea (BUN)", 0),
                        ("Creatinine", 0), ("Serum WBC count", 1), ("Dialysate WBC count", 1)),
        "explanation": (
            "Fever, abdominal pain, and an elevated WBC count in the serum and in the dialysate effluent indicate "
            "peritonitis, a potentially life-threatening complication of peritoneal dialysis. Erythema and creamy yellow "
            "exudate around the catheter exit site indicate a possible exit-site infection, which may be the source of "
            "the peritonitis.<br>Although the urea and creatinine are high for a person without kidney failure, they are "
            "typical for a client with ESRD on peritoneal dialysis. The blood pressure and heart rate are only slightly "
            "elevated, and the respiratory rate is within the normal range for an adult."),
    }),
    (INTRO, tabs(2), {
        "type": "matrix_mr",
        "stem": ("For each client finding, click to specify if the finding supports the diagnosis of peritonitis or "
                 "end-stage renal disease (ESRD). Each finding may support more than one condition."),
        "matrix": matrix_mr("Finding", ["Peritonitis", "End-Stage Renal Disease (ESRD)"], [
            ("Urea 16.4 mmol/L", [1]), ("Creatinine 946 µmol/L", [1]), ("C-reactive protein 61.5 mg/L", [0]),
            ("Potassium 5.86 mmol/L", [1]), ("Phosphate 1.87 mmol/L", [1]), ("Hemoglobin 106 g/L", [1]),
            ("WBC 14.22 × 10⁹/L", [0]), ("Neutrophils 89.8%", [0])]),
        "explanation": (
            "C-reactive protein is an inflammatory marker that rises with infection and inflammation, and an elevated WBC "
            "count and neutrophil percentage indicate infection: these support peritonitis.<br>Elevated urea, "
            "creatinine, potassium, and phosphate are common in ESRD because the kidneys cannot excrete waste products. "
            "The low hemoglobin (anemia) results from the kidneys&rsquo; inability to produce erythropoietin."),
    }),
    (INTRO, tabs(3), {
        "type": "drag_drop_cloze",
        "preamble": "The client is diagnosed with peritonitis.",
        "stem": "Drag the most appropriate choice from the list of options to fill in the blank of the following sentence.",
        "cloze": cloze("The client is at highest risk for developing [[drop0]].",
                       [("abdominal abscess", 0), ("cellulitis", 0), ("pyelonephritis", 0), ("sepsis", 1)]),
        "explanation": (
            "About 11% of clients with ESRD who develop peritonitis develop sepsis, the body&rsquo;s dysregulated immune "
            "response to an infection. In sepsis, inflammatory mediators impair blood flow to organs such as the brain "
            "and heart, which can lead to tissue damage and organ failure. At its most severe, the response causes "
            "dangerously low blood pressure (septic shock), with a mortality of about one third."),
    }),
    (INTRO, tabs(4), {
        "type": "matrix_mc",
        "preamble": "The nurse has reviewed the Microbiology results.",
        "stem": ("Based on the new laboratory data, for each potential order, click to specify whether the order is "
                 "appropriate or not appropriate to include in the plan of care."),
        "matrix": matrix("Potential Order", ["Appropriate", "Not Appropriate"], [
            ("Daily weights", 0), ("Blood cultures STAT", 0), ("Peritoneal dialysis catheter care every shift", 0),
            ("IV D5 ½ NS with 20 mmol/L KCl at 120 mL/hr", 1), ("Calcium carbonate with meals", 0), ("Vancomycin IV", 1),
            ("Gentamicin intraperitoneally daily", 0), ("Enoxaparin subcutaneous daily", 1), ("Epoetin alfa injections", 0)]),
        "explanation": (
            "<b>Appropriate:</b> Daily weights assess for the hypervolemia of ESRD; inflammation of the peritoneum can "
            "reduce the efficacy of peritoneal dialysis. Blood cultures assess for bacteremia, which may require IV "
            "antibiotics in addition to intraperitoneal antibiotics. Catheter care treats the infection; the catheter "
            "may need to be replaced if the infection does not clear. Gentamicin is a broad-spectrum antibiotic that "
            "treats gram-negative bacteria, and intraperitoneal delivery is more effective than IV for peritonitis; the "
            "antibiotic is adjusted once sensitivities are known. Epoetin alfa treats the anemia of ESRD. Calcium "
            "carbonate, a phosphate binder, is taken with each meal to prevent absorption of phosphate from the gut, "
            "which helps keep the calcium level up.<br><b>Not appropriate:</b> IV D5 &frac12; NS with KCl at 120 mL/hr "
            "would cause hypervolemia and hyperkalemia in a client who is oliguric or anuric. Vancomycin is not effective "
            "against gram-negative organisms. Enoxaparin is cleared by the kidneys, so it accumulates in ESRD and "
            "increases the risk of bleeding."),
    }),
    (INTRO, tabs(5), {
        "type": "matrix_mc",
        "preamble": ("The nurse leads a team that includes an LPN and an unlicensed assistive personnel (UAP) and plans "
                     "the client&rsquo;s care based on the most effective use of the team&rsquo;s skill mix."),
        "stem": "For each task, click to specify if the task should be performed by the RN, the LPN, or the UAP.",
        "matrix": matrix("Task", ["RN", "LPN", "UAP"], [
            ("Vital signs", 2), ("Dialysate exchange", 0), ("Daily weights", 2),
            ("Peritoneal dialysis catheter care every shift", 1), ("Intraperitoneal gentamicin", 0),
            ("Peritoneal dialysis catheter care teaching", 0)]),
        "explanation": (
            "The UAP provides basic care, such as hygiene, and collects limited data such as vital signs and weights. The "
            "LPN performs nursing care in routine situations, such as uncomplicated wound and catheter care.<br>The LPN "
            "cannot implement nonroutine care such as intraperitoneal antibiotics, catheter care teaching, or a "
            "dialysate exchange for this client; those tasks are done by the RN."),
    }),
    (INTRO, tabs(6), {
        "type": "matrix_mc",
        "preamble": "The nurse teaches the client about peritoneal dialysis catheter care to help prevent future infections.",
        "stem": ("For each client statement, click to specify whether the statement indicates the client understands or "
                 "does not understand the teaching about self-care of the peritoneal dialysis catheter."),
        "matrix": matrix("Statement", ["Understands", "Does Not Understand"], [
            ("“Before cleaning the area, I will wash my hands with soap and water and put on clean gloves.”", 0),
            ("“I should remove crusts or scabs at the exit site before washing the site.”", 1),
            ("“I should hold the catheter in place during cleaning to prevent injury to the skin.”", 0),
            ("“I should scrub the exit site vigorously with an antiseptic solution like iodine or chlorhexidine.”", 1),
            ("“I will put antibiotic cream on the skin around the catheter with a cotton-tip swab every time I change "
             "the dressing.”", 0),
            ("“I will not use any creams with petroleum because they can damage the catheter.”", 0),
            ("“I will leave the exit site open to air or covered by loose clothing.”", 1)]),
        "explanation": (
            "Hand hygiene and clean gloves, stabilizing the catheter during cleaning, applying the prescribed antibiotic "
            "cream at each dressing change, and avoiding petroleum-based products (which can damage the catheter) all "
            "show understanding.<br>Crusts or scabs should not be picked off before washing, because this can tear the "
            "skin and increase the risk of infection. The exit site is cleaned gently with a liquid antibacterial soap "
            "and a clean cloth; vigorous scrubbing with antiseptics can dry and crack the skin. The exit site should not "
            "be left open to air; it is covered with sterile gauze, changed each time the site is cleaned."),
    }),
]

case = make_case(N, "", "", screens, FN)
case["description"] = ("Maryland Next Gen NCLEX Test Bank Project, September 1, 2022; Author: Laura Sessions, Towson "
                       "University. ESRD and dialysis: a 35-year-old client on peritoneal dialysis with peritonitis; "
                       "differentiating ESRD and infection, orders, delegation, and catheter-care teaching.")

BOW_NOTE = paras(
    "A 39-year-old male client came to the emergency department with shaking chills; maximum temperature reported as "
    "101.2&deg;F (38.4&deg;C). Weight 109.1 kg (240 lb). No known drug allergies. History of end-stage renal disease "
    "secondary to heroin nephrotoxicity; on hemodialysis for approximately 7 months.",
    "<b>Current assessment:</b> left upper arm arteriovenous (AV) fistula with a positive thrill and bruit. The AV fistula "
    "is red and inflamed. Labs sent.")
BOW_VS = vitals(["1500", "1600"], [
    ("T", "39.2&deg;C (102.6&deg;F)", "40.2&deg;C (104.4&deg;F)"), ("HR", "104", "121"), ("RR", "18", "26"),
    ("BP", "150/92", "100/64"), ("Pulse oximetry reading", "95% on room air", "90% on room air"),
    ("Pain (AV fistula site)", "6/10", "8/10")])
bow = make_standalone(N, 1, "Bowtie", ("Stand-alone bow-tie for University of Maryland - CS11 (ESRD and dialysis): "
                                       "septicemia in a client on hemodialysis."),
                      ("A 39-year-old male client with end-stage renal disease on hemodialysis is seen in the emergency "
                       "department with fever."),
                      [{"id": f"adm_umd{S}b", "title": "Admission Note", "content": BOW_NOTE},
                       {"id": f"vs_umd{S}b", "title": "Vital Signs", "content": BOW_VS}],
                      dict({"type": "bowtie",
                            "stem": ("Based on the client information, complete the diagram by dragging from the choices "
                                     "below to specify what condition the client is most likely experiencing, "
                                     "<b>2</b> actions the nurse should take to address that condition, and <b>2</b> "
                                     "parameters the nurse should monitor to assess the client&rsquo;s progress."),
                            "explanation": (
                                "The client has evidence of an infection at the AV fistula site. The falling blood "
                                "pressure and pulse oximetry reading suggest septicemia progressing to septic shock. "
                                "Broad-spectrum IV antibiotics and oxygen are most needed, and the nurse monitors "
                                "perfusion through the pulse oximetry reading and blood pressure.<br>Urine output is not "
                                "a good measure of perfusion in a client on dialysis.")},
                           **bowtie([("Administer oxygen", 1), ("Raise head of bed", 0),
                                     ("Administer broad-spectrum antibiotics IV", 1), ("Prepare for intubation", 0),
                                     ("Begin epinephrine drip", 0)],
                                    [("Cardiogenic shock", 0), ("Acute respiratory distress syndrome", 0),
                                     ("Multisystem organ failure", 0), ("Septicemia", 1)],
                                    [("Pain", 0), ("Urinary output", 0), ("Pulse oximetry reading", 1),
                                     ("Blood pressure", 1), ("Liver enzymes", 0)])), FN_B)

NOTES = [
    "Screen 2: the source's finding rows had values that differ from the lab report (creatinine 11.7 vs 10.7 mg/dL, "
    "phosphorus 5.4 vs 5.8 mg/dL, neutrophils 89% vs 89.8%); the chart's values are used, in SI units.",
    "Screen 4: enoxaparin keyed \"not appropriate in ESRD\". Dose-adjusted enoxaparin is sometimes used in severe CKD, "
    "though unfractionated heparin is preferred; consider \"Enoxaparin 40 mg subcutaneous daily\" wording or a clearer "
    "rationale. Vancomycin keyed not appropriate (gram-negative rods); note that empiric PD-peritonitis therapy "
    "(ISPD) covers gram-positive organisms too until cultures return.",
    "Screen 5 uses LPN (US term); in Ontario this is the RPN. Delegation keys follow US scope; please confirm for your "
    "program.",
    "Screen 6: \"leave the exit site open to air or covered by loose clothing\" is keyed does not understand (rationale: "
    "cover with sterile gauze). Exit-site dressing practice varies once the site is healed; please confirm with your "
    "program's PD teaching.",
    "Dialysate WBC reference range is \"Few\" in the source; the usual peritonitis threshold is > 100 cells/µL with > 50% "
    "neutrophils. Consider adding it as the reference range.",
    "Labs in SI with the author's ranges: urea 46 mg/dL → 16.4 mmol/L (3.6-7.1); creatinine 10.7 mg/dL → 946 µmol/L "
    "(80-124); CRP 61.5 mg/L (< 10 mg/L; source range \"< 1.0 mg/dL\"); albumin \"3.7 g/L\" (typo for 3.7 g/dL) → 37 g/L; "
    "calcium 7.9 mg/dL → 1.97 mmol/L; phosphorus 5.8 mg/dL → 1.87 mmol/L; Hgb 10.6 g/dL → 106 g/L; Hct 0.31.",
    "Bow-tie: \"Adult respiratory distress syndrome\" now reads \"Acute respiratory distress syndrome\".",
    "Screen 1 options were reordered so a correct answer is not listed first.",
]

write([case, bow], N, "End Stage Renal Disease and Dialysis", "End-Stage-Renal-Disease-and-Dialysis.docx", NOTES)
