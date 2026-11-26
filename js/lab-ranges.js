/* Reference ranges for the Laboratory Results tables, from the Medical Council of Canada's "Normal
   lab values" (https://mcc.ca/examinations-assessments/resources-to-help-with-exam-prep/normal-lab-values/),
   SI values exactly as MCC prints them (read September 2026; the page cites EORLA regional reference
   intervals, the AMA manual of style and the Merck manual). A few MCC values are not strict SI units
   and are kept as printed: blood gases in mm Hg, BNP/NT-proBNP in pg/mL, CD4 in cells/µL, hepatitis B
   surface antibodies in mIU/mL, urinary free cortisol in µg/24 h. LDL is left out: MCC gives
   risk-based treatment targets, not a reference range. When the author types one of these test names in the first column of
   a lab table and leaves the cell, what they typed is set in bold and the range goes on the next line
   (fillLabReferenceRange in js/table-tools.js). Each entry: { name, range, aliases?, labref }.
   labref is the test's fixed address in LabRef, the lab values companion on the Virtual Experiential
   Learning for Nurses site (labRefUrl below); in Practice mode the player links lab-table rows there
   (addLabRefLinks in js/player.js). */

const LAB_REFERENCE_RANGES = [
  { name: "pH, arterial blood", range: "7.38–7.46", aliases: ["pH", "arterial pH", "ABG pH"], labref: "ph-arterial-blood" },
  { name: "PCO₂, arterial blood", range: "32–45 mm Hg", aliases: ["PCO2", "pCO2", "PaCO2", "Pco2", "arterial PCO2"], labref: "pco2-arterial-blood" },
  { name: "PO₂, arterial blood", range: "83–116 mm Hg", aliases: ["PO2", "pO2", "PaO2", "Po2", "arterial PO2"], labref: "po2-arterial-blood" },
  { name: "Bicarbonate (HCO₃), arterial blood", range: "22–27 mmol/L", aliases: ["arterial bicarbonate", "arterial HCO3", "HCO3 arterial", "ABG HCO3", "bicarbonate arterial"], labref: "bicarbonate-hco3-arterial-blood" },
  { name: "Base excess, arterial blood", range: "−2.5 to 2.5 mmol/L", aliases: ["base excess", "BE"], labref: "base-excess-arterial-blood" },
  { name: "Erythrocyte sedimentation rate (ESR)", range: "Female: 0–20 mm/h; Male: 0–10 mm/h", aliases: ["ESR", "sed rate", "erythrocyte sedimentation rate"], labref: "erythrocyte-sedimentation-rate-esr-blood" },
  { name: "Hematocrit (Hct)", range: "0.38–0.50 L/L", aliases: ["Hct", "hematocrit", "haematocrit"], labref: "hematocrit-hct-blood" },
  { name: "Hemoglobin (Hgb)", range: "Female: 115–155 g/L; Male: 125–170 g/L", aliases: ["Hgb", "Hb", "hemoglobin", "haemoglobin"], labref: "hemoglobin-hgb-blood" },
  { name: "Mean corpuscular volume (MCV)", range: "80–100 fL", aliases: ["MCV"], labref: "mean-corpuscular-volume-mcv-blood" },
  { name: "Mean corpuscular hemoglobin (MCH)", range: "Female: 25–34 pg; Male: 27–34 pg", aliases: ["MCH"], labref: "mean-corpuscular-hemoglobin-mch-blood" },
  { name: "Mean corpuscular hemoglobin concentration (MCHC)", range: "315–355 g/L", aliases: ["MCHC"], labref: "mean-corpuscular-hemoglobin-concentration-mchc-blood" },
  { name: "Mean platelet volume (MPV)", range: "9.0–14.0 fL", aliases: ["MPV"], labref: "mean-platelet-volume-mpv-blood" },
  { name: "Platelet count", range: "130–380 × 10⁹/L", aliases: ["platelets", "platelet count", "PLT", "plt"], labref: "platelet-count-blood" },
  { name: "Red blood cell (RBC) count", range: "Female: 3.50–5.00 × 10¹²/L; Male: 4.00–5.50 × 10¹²/L", aliases: ["RBC", "red blood cells", "RBC count", "red blood cell count"], labref: "red-blood-cell-rbc-count-blood" },
  { name: "Red cell distribution width (RDW)", range: "11.5%–15.5%", aliases: ["RDW"], labref: "red-cell-distribution-width-rdw-blood" },
  { name: "Reticulocyte count, absolute", range: "23–90 × 10⁹/L", aliases: ["reticulocytes", "reticulocyte count", "retic count", "absolute reticulocytes"], labref: "reticulocyte-count-absolute-blood" },
  { name: "Reticulocyte percentage", range: "0.5%–1.5%", aliases: ["reticulocyte %", "retic %", "reticulocytes %"], labref: "reticulocyte-percentage-blood" },
  { name: "Bleeding time (Ivy method)", range: "1–9 min", aliases: ["bleeding time"], labref: "bleeding-time-ivy-method-blood" },
  { name: "International normalized ratio (INR), nonanticoagulated", range: "0.9–1.2", aliases: ["INR"], labref: "international-normalized-ratio-inr-nonanticoagulated-blood" },
  { name: "Activated partial thromboplastin time (APTT), nonanticoagulated", range: "22–30 s", aliases: ["APTT", "aPTT", "PTT", "activated partial thromboplastin time"], labref: "activated-partial-thromboplastin-time-aptt-nonanticoagulated-blood" },
  { name: "Prothrombin time (PT)", range: "10–14 s", aliases: ["PT", "prothrombin time"], labref: "prothrombin-time-pt-blood" },
  { name: "White blood cell (WBC) count", range: "3.5–10.5 × 10⁹/L", aliases: ["WBC", "white blood cells", "WBC count", "white blood cell count", "leukocytes"], labref: "white-blood-cell-wbc-count-blood" },
  { name: "Neutrophils, absolute", range: "2.0–7.5 × 10⁹/L", aliases: ["neutrophils", "ANC", "absolute neutrophils", "absolute neutrophil count"], labref: "neutrophils-absolute-blood" },
  { name: "Basophils", range: "0–0.1 × 10⁹/L", labref: "basophils-blood" },
  { name: "Eosinophils", range: "0–0.5 × 10⁹/L", labref: "eosinophils-blood" },
  { name: "Lymphocytes", range: "Female: 0.8–3.3 × 10⁹/L; Male: 0.8–3.5 × 10⁹/L", labref: "lymphocytes-blood" },
  { name: "Monocytes", range: "0.1–1.0 × 10⁹/L", labref: "monocytes-blood" },
  { name: "Ferritin", range: "Female: 11–307 µg/L; Male: 24–336 µg/L", labref: "ferritin-blood" },
  { name: "Iron", range: "Female: 9–30 µmol/L; Male: 12–31 µmol/L", aliases: ["serum iron"], labref: "iron-blood" },
  { name: "Iron-binding capacity, total (TIBC)", range: "45–81 µmol/L", aliases: ["TIBC", "total iron-binding capacity", "total iron binding capacity"], labref: "iron-binding-capacity-total-tibc-blood" },
  { name: "Transferrin", range: "2.0–3.6 g/L", labref: "transferrin-blood" },
  { name: "Transferrin saturation", range: "0.20–0.50", aliases: ["TSAT", "transferrin sat"], labref: "transferrin-saturation-blood" },
  { name: "Thyroid peroxidase antibody", range: "< 35 IU/mL", aliases: ["TPO antibody", "anti-TPO", "TPO Ab"], labref: "thyroid-peroxidase-antibody-blood" },
  { name: "Thyrotropin (thyroid-stimulating hormone)", range: "0.34–5.60 mIU/L", aliases: ["TSH", "thyroid-stimulating hormone", "thyroid stimulating hormone", "thyrotropin"], labref: "thyrotropin-thyroid-stimulating-hormone-blood" },
  { name: "Thyroxine, free (FT4)", range: "7.0–17.0 pmol/L", aliases: ["FT4", "free T4", "free thyroxine"], labref: "thyroxine-free-ft4-blood" },
  { name: "Triiodothyronine, free (FT3)", range: "3.3–6.0 pmol/L", aliases: ["FT3", "free T3", "free triiodothyronine"], labref: "triiodothyronine-free-ft3-blood" },
  { name: "Adrenocorticotropic hormone (ACTH)", range: "At 8 a.m.: 2.2–13.3 pmol/L; At 4 p.m.: < 4.5 pmol/L", aliases: ["ACTH"], labref: "adrenocorticotropic-hormone-acth-blood" },
  { name: "Albumin", range: "34–50 g/L", aliases: ["serum albumin"], labref: "albumin-blood" },
  { name: "Aldosterone", range: "61–978 pmol/L", labref: "aldosterone-blood" },
  { name: "Alkaline phosphatase", range: "50–136 IU/L", aliases: ["ALP", "alk phos"], labref: "alkaline-phosphatase-blood" },
  { name: "Alanine aminotransferase (ALT)", range: "17–63 IU/L", aliases: ["ALT"], labref: "alanine-aminotransferase-alt-blood" },
  { name: "Aspartate aminotransferase (AST)", range: "15–37 IU/L", aliases: ["AST"], labref: "aspartate-aminotransferase-ast-blood" },
  { name: "γ-Glutamyltransferase (GGT)", range: "Female: 5.0–55.0 IU/L; Male: 15.0–85.0 IU/L", aliases: ["GGT", "gamma-glutamyltransferase", "gamma glutamyltransferase"], labref: "gamma-glutamyltransferase-ggt-blood" },
  { name: "Ammonia", range: "≤ 35 µmol/L", labref: "ammonia-blood" },
  { name: "Amylase", range: "25–115 IU/L", labref: "amylase-blood" },
  { name: "Anion gap", range: "5–12 mmol/L", labref: "anion-gap-blood" },
  { name: "Bicarbonate (HCO₃)", range: "21–32 mmol/L", aliases: ["bicarbonate", "HCO3", "serum bicarbonate"], labref: "bicarbonate-hco3-blood" },
  { name: "Bilirubin, direct (conjugated)", range: "2–9 µmol/L", aliases: ["direct bilirubin", "conjugated bilirubin", "bilirubin direct"], labref: "bilirubin-blood" },
  { name: "Bilirubin, total", range: "3–17 µmol/L", aliases: ["total bilirubin", "bilirubin", "bilirubin total"], labref: "bilirubin-blood" },
  { name: "Brain-type natriuretic peptide (BNP)", range: "≤ 50 pg/mL", aliases: ["BNP", "B-type natriuretic peptide"], labref: "brain-type-natriuretic-peptide-bnp-blood" },
  { name: "N-terminal pro–brain-type natriuretic peptide (NT-proBNP)", range: "≤ 125 pg/mL", aliases: ["NT-proBNP", "NT proBNP"], labref: "n-terminal-pro-brain-type-natriuretic-peptide-nt-probnp-blood" },
  { name: "CD4 T-cell count", range: "500–2000 cells/µL", aliases: ["CD4", "CD4 count"], labref: "cd4-t-cell-count-blood" },
  { name: "C-reactive protein", range: "≤ 10 mg/L", aliases: ["CRP"], labref: "c-reactive-protein-blood" },
  { name: "Calcium, total", range: "2.12–2.52 mmol/L", aliases: ["calcium", "total calcium", "Ca", "serum calcium"], labref: "calcium-ca-blood" },
  { name: "Calcium, ionized", range: "1.14–1.28 mmol/L", aliases: ["ionized calcium", "ionised calcium", "iCa"], labref: "calcium-ca-blood" },
  { name: "Cancer antigen (CA) 125", range: "< 35 kIU/L", aliases: ["CA 125", "CA-125", "CA125"], labref: "cancer-antigen-ca-125-blood" },
  { name: "Cancer antigen (CA) 19-9", range: "< 35 kIU/L", aliases: ["CA 19-9", "CA19-9"], labref: "cancer-antigen-ca-19-9-blood" },
  { name: "Carbamazepine", range: "17–51 µmol/L", aliases: ["carbamazepine level"], labref: "carbamazepine-blood" },
  { name: "Carcinoembryonic antigen (CEA)", range: "< 3.0 µg/L", aliases: ["CEA"], labref: "carcinoembryonic-antigen-cea-blood" },
  { name: "Chloride (Cl)", range: "98–107 mmol/L", aliases: ["chloride", "Cl"], labref: "chloride-cl-blood" },
  { name: "Cortisol", range: "a.m.: 185–624 nmol/L; p.m.: ≤ 276 nmol/L", aliases: ["serum cortisol"], labref: "cortisol-blood" },
  { name: "Creatine kinase (CK)", range: "Female: 30–190 IU/L; Male: 30–250 IU/L", aliases: ["CK", "CPK", "creatine kinase"], labref: "creatine-kinase-ck-blood" },
  { name: "Creatinine", range: "Female: 22–75 µmol/L; Male: 49–93 µmol/L", aliases: ["serum creatinine", "Cr", "creat"], labref: "creatinine-blood" },
  { name: "D-dimer", range: "< 600 µg/L", aliases: ["D dimer", "d-dimer"], labref: "d-dimer-blood" },
  { name: "Estimated glomerular filtration rate (eGFR)", range: "≥ 60 mL/min/1.73 m²", aliases: ["eGFR", "GFR"], labref: "estimated-glomerular-filtration-rate-egfr-blood" },
  { name: "α1-Fetoprotein", range: "≤ 9.0 µg/L", aliases: ["AFP", "alpha-fetoprotein", "alpha fetoprotein"], labref: "alpha1-fetoprotein-blood" },
  { name: "Folate (folic acid)", range: "≥ 10.0 nmol/L", aliases: ["folate", "folic acid"], labref: "folate-folic-acid-blood" },
  { name: "Glucose, fasting", range: "4.0–6.0 mmol/L", aliases: ["fasting glucose", "fasting blood glucose", "FBG", "glucose (fasting)"], labref: "glucose-blood" },
  { name: "Glucose, random", range: "4.0–11.0 mmol/L", aliases: ["glucose", "random glucose", "blood glucose", "glucose (random)", "serum glucose"], labref: "glucose-blood" },
  { name: "Hemoglobin A1c (HbA1c)", range: "4.8%–6.0%", aliases: ["HbA1c", "A1C", "A1c", "hemoglobin A1c", "glycated hemoglobin"], labref: "hemoglobin-a1c-hba1c-blood" },
  { name: "Hepatitis B surface antibodies", range: "Positive: ≥ 10 mIU/mL; Negative: < 10 mIU/mL", aliases: ["anti-HBs", "HBsAb", "hepatitis B surface antibody"], labref: "hepatitis-b-surface-antibodies-blood" },
  { name: "Lactate", range: "0.5–2.5 mmol/L", aliases: ["lactic acid", "serum lactate"], labref: "lactate-blood" },
  { name: "Lactate dehydrogenase (LDH)", range: "100–205 IU/L", aliases: ["LDH", "LD"], labref: "lactate-dehydrogenase-ldh-blood" },
  { name: "Lipase", range: "73–393 IU/L", labref: "lipase-blood" },
  { name: "Lithium (Li)", range: "Age 18–65 y: 0.6–1.2 mmol/L; Age > 65 y: 0.4–0.8 mmol/L", aliases: ["lithium", "lithium level", "Li"], labref: "lithium-li-blood" },
  { name: "Magnesium (Mg)", range: "0.74–1.03 mmol/L", aliases: ["magnesium", "Mg"], labref: "magnesium-mg-blood" },
  { name: "Osmolality, serum", range: "275–295 mmol/kg", aliases: ["osmolality", "serum osmolality", "plasma osmolality"], labref: "osmolality-blood" },
  { name: "Parathyroid hormone (PTH)", range: "1.6–9.3 pmol/L", aliases: ["PTH"], labref: "parathyroid-hormone-pth-blood" },
  { name: "Phosphate (PO₄)", range: "0.81–1.58 mmol/L", aliases: ["phosphate", "phosphorus", "PO4"], labref: "phosphate-po4-blood" },
  { name: "Potassium (K)", range: "3.5–5.1 mmol/L", aliases: ["potassium", "K", "serum potassium", "K+"], labref: "potassium-k-blood" },
  { name: "Prostate-specific antigen (PSA)", range: "< 3.1 µg/L", aliases: ["PSA"], labref: "prostate-specific-antigen-psa-blood" },
  { name: "Protein, total", range: "Age 18–<30 y: 65–83 g/L; Age ≥ 30 y: 65–78 g/L", aliases: ["total protein", "protein"], labref: "protein-total-blood" },
  { name: "Rheumatoid factor (RF)", range: "≤ 20 kIU/L", aliases: ["RF", "rheumatoid factor"], labref: "rheumatoid-factor-rf-blood" },
  { name: "Sodium (Na)", range: "136–146 mmol/L", aliases: ["sodium", "Na", "serum sodium", "Na+"], labref: "sodium-na-blood" },
  { name: "Troponin I", range: "≤ 45 ng/L", aliases: ["TnI", "troponin"], labref: "troponin-i-blood" },
  { name: "Troponin T (TnT)", range: "≤ 0.1 µg/L", aliases: ["TnT"], labref: "troponin-t-tnt-blood" },
  { name: "Uric acid", range: "Female: 155–400 µmol/L; Male: 208–400 µmol/L", aliases: ["urate"], labref: "uric-acid-blood" },
  { name: "Urea", range: "2.1–8.0 mmol/L", aliases: ["serum urea"], labref: "urea-blood" },
  { name: "Valproic acid", range: "350–700 µmol/L", aliases: ["valproate", "valproic acid level"], labref: "valproic-acid-blood" },
  { name: "Vitamin B12", range: "133–675 pmol/L", aliases: ["B12", "cobalamin"], labref: "vitamin-b12-blood" },
  { name: "Vitamin D (25-hydroxyvitamin D)", range: "75–250 nmol/L", aliases: ["vitamin D", "25-hydroxyvitamin D", "25-OH vitamin D"], labref: "vitamin-d-25-hydroxyvitamin-d-blood" },
  { name: "Cholesterol, total", range: "3.5–5.2 mmol/L", aliases: ["total cholesterol", "cholesterol"], labref: "cholesterol-total-blood" },
  { name: "Cholesterol, high-density lipoprotein (HDL)", range: "Female: > 1.3 mmol/L; Male: > 1.0 mmol/L", aliases: ["HDL", "HDL cholesterol"], labref: "cholesterol-high-density-lipoprotein-hdl-blood" },
  { name: "Non–high-density lipoprotein (non-HDL)", range: "≤ 4.5 mmol/L", aliases: ["non-HDL", "non-HDL cholesterol"], labref: "non-high-density-lipoprotein-non-hdl-blood" },
  { name: "Triglycerides", range: "≤ 1.7 mmol/L", aliases: ["TG", "triglyceride"], labref: "triglycerides-blood" },
  { name: "Specific gravity, urine", range: "1.005–1.030", aliases: ["specific gravity", "urine specific gravity", "SG"], labref: "specific-gravity-urine" },
  { name: "pH, urine", range: "5.0–8.5", aliases: ["urine pH"], labref: "ph-urine" },
  { name: "Urobilinogen, urine", range: "≤ 16.0 µmol/L", aliases: ["urobilinogen"], labref: "urobilinogen-urine" },
  { name: "Albumin to creatinine ratio, urine", range: "≤ 2.0 g/mol Cr", aliases: ["ACR", "albumin creatinine ratio", "urine ACR"], labref: "albumin-to-creatinine-ratio-urine" },
  { name: "Osmolality, urine", range: "38–1400 mOsm/kg H₂O", aliases: ["urine osmolality"], labref: "osmolality-urine" },
  { name: "Urine calcium (Ca), unrestricted diet, 24-h specimen", range: "2.5–7.5 mmol/24 h", aliases: ["24-h urine calcium", "urine calcium"], labref: "urine-calcium-ca-unrestricted-diet-24-h-specimen" },
  { name: "Urine chloride (Cl), 24-h specimen", range: "110.0–250.0 mmol/24 h", aliases: ["24-h urine chloride", "urine chloride"], labref: "urine-chloride-cl-24-h-specimen" },
  { name: "Urine creatinine, weight-based, 24-h specimen", range: "Female: 5.3–15.9 mmol/24 h; Male: 7.1–17.7 mmol/24 h", aliases: ["24-h urine creatinine", "urine creatinine"], labref: "urine-creatinine-weight-based-24-h-specimen" },
  { name: "Urine metanephrine, 24-h specimen", range: "Female: 0.2–1.3 µmol/24 h; Male: 0.3–2.0 µmol/24 h", aliases: ["urine metanephrine", "24-h urine metanephrine"], labref: "urine-metanephrine-24-h-specimen" },
  { name: "Urine protein, 24-h specimen", range: "< 0.2 g/24 h", aliases: ["24-h urine protein", "urine protein"], labref: "urine-protein-24-h-specimen" },
  { name: "Urine potassium (K), 24-h specimen", range: "25.0–125.0 mmol/24 h", aliases: ["24-h urine potassium", "urine potassium"], labref: "urine-potassium-k-24-h-specimen" },
  { name: "Urinary free cortisol, 24-h specimen", range: "58.0–306.0 µg/24 h", aliases: ["urinary free cortisol", "urine free cortisol"], labref: "urinary-free-cortisol-24-h-specimen" },
  { name: "Urine sodium (Na), 24-h specimen", range: "40.0–220.0 mmol/24 h", aliases: ["24-h urine sodium", "urine sodium"], labref: "urine-sodium-na-24-h-specimen" },
  { name: "Dehydroepiandrosterone sulfate (DHEA-S)", range: "Female 18–20 y: 1.4–8.7 µmol/L; 21–29 y: 0.5–10.6 µmol/L; 30–39 y: 0.6–7.2 µmol/L; 40–49 y: 0.5–6.3 µmol/L; 50–59 y: 0.2–5.1 µmol/L; 60–69 y: 0.3–3.6 µmol/L; 70–118 y: 0.2–4.8 µmol/L. Male 18–20 y: 0.7–14.6 µmol/L; 21–29 y: 2.3–18.7 µmol/L; 30–39 y: 2.9–12.6 µmol/L; 40–49 y: 1.9–13.4 µmol/L; 50–59 y: 1.0–8.5 µmol/L; 60–69 y: 0.7–6.6 µmol/L; 70–118 y: 0.1–6.9 µmol/L", aliases: ["DHEA-S", "DHEAS"], labref: "dehydroepiandrosterone-sulfate-dhea-s-blood" },
  { name: "Estrogens, total", range: "60–400 ng/L", aliases: ["total estrogens", "estrogen"], labref: "estrogens-total-blood" },
  { name: "Estradiol (E2)", range: "Female, follicular phase: 50–100 pmol/L; midcycle peak: 50–200 pmol/L; luteal phase: 70–150 pmol/L. Male: 37–110 pmol/L", aliases: ["estradiol", "E2"], labref: "estradiol-e2-blood" },
  { name: "Follicle-stimulating hormone (FSH)", range: "Female, midfollicular phase: 3.9–8.8 IU/L; midcycle peak: 4.5–22.5 IU/L; midluteal phase: 1.8–5.1 IU/L; postmenopausal: 16.7–113.6 IU/L. Male: 1.0–19.0 IU/L", aliases: ["FSH"], labref: "follicle-stimulating-hormone-fsh-blood" },
  { name: "Human chorionic gonadotropin (β-hCG), nonpregnant", range: "< 5 IU/L", aliases: ["beta-hCG", "hCG", "b-hCG", "β-hCG", "beta hCG"], labref: "human-chorionic-gonadotropin-beta-hcg-nonpregnant-blood" },
  { name: "Luteinizing hormone (LH)", range: "Female, midfollicular phase: 2.1–10.8 IU/L; midcycle peak: 19.2–103.0 IU/L; midluteal phase: 1.2–12.9 IU/L; postmenopausal: 10.9–58.6 IU/L. Male: 1.0–9.0 IU/L", aliases: ["LH"], labref: "luteinizing-hormone-lh-blood" },
  { name: "Progesterone", range: "Female, midfollicular phase: 1.0–4.8 nmol/L; midluteal phase: 16.4–59.0 nmol/L. Male: 0.5–6.6 nmol/L", labref: "progesterone-blood" },
  { name: "Prolactin", range: "Female, premenopausal: 3–27 µg/L; postmenopausal: 3–20 µg/L. Male: 3–13 µg/L", aliases: ["PRL"], labref: "prolactin-blood" },
  { name: "Testosterone", range: "Female: ≤ 2.6 nmol/L; Male: 6.1–27.1 nmol/L", labref: "testosterone-blood" },
  { name: "Ejaculate volume, semen", range: "≥ 1.5 mL", aliases: ["ejaculate volume", "semen volume"], labref: "ejaculate-volume-semen" },
  { name: "pH, semen", range: "≥ 7.2", aliases: ["semen pH"], labref: "ph-semen" },
  { name: "Sperm concentration, semen", range: "≥ 15 × 10⁶ spermatozoa/mL", aliases: ["sperm concentration"], labref: "sperm-concentration-semen" },
  { name: "Total sperm number, semen", range: "≥ 39 × 10⁶ spermatozoa/ejaculate", aliases: ["total sperm number", "total sperm count"], labref: "total-sperm-number-semen" },
  { name: "Motility, semen", range: "≥ 40%", aliases: ["sperm motility", "motility"], labref: "motility-semen" },
  { name: "Forward progression, semen", range: "≥ 32%", aliases: ["forward progression", "progressive motility"], labref: "forward-progression-semen" },
  { name: "Normal morphology, semen", range: "≥ 4% normal", aliases: ["sperm morphology", "normal morphology"], labref: "normal-morphology-semen" },
  { name: "Sperm agglutination, semen", range: "Absent", aliases: ["sperm agglutination"], labref: "sperm-agglutination-semen" },
  { name: "Viscosity, semen", range: "≤ 2-cm thread after liquefaction", aliases: ["semen viscosity"], labref: "viscosity-semen" },
  { name: "Fecal fat", range: "< 5 g/day in patients on a 100-g fat diet", aliases: ["stool fat", "faecal fat"], labref: "fecal-fat" },
];

function normalizeLabName(text) {
  return (text || '').toLowerCase().replace(/[^a-z0-9%]+/g, ' ').trim();
}

function findLabReference(text) {
  const key = normalizeLabName(text);
  if (!key) return null;
  return LAB_REFERENCE_RANGES.find(r => [r.name, ...(r.aliases || [])].some(n => normalizeLabName(n) === key)) || null;
}

// LabRef, the lab values companion (anatomy-physiology-virtual-labs repo, lab-values/).
const LABREF_BASE_URL = 'https://thadaniavinash.github.io/anatomy-physiology-virtual-labs/lab-values/';

// LabRef's page for a LAB_REFERENCE_RANGES entry (normal range, interpretation, nursing care), or null.
function labRefUrl(ref) {
  return ref && ref.labref ? `${LABREF_BASE_URL}?test=${encodeURIComponent(ref.labref)}` : null;
}

// A looser match used only for the player's LabRef links (the authoring auto-fill keeps the exact
// findLabReference). It also accepts the name without its bracketed abbreviation ("Urea (BUN)"), the
// abbreviation alone when it is 2+ characters ("(aPTT)"), a bracketed qualifier read as part of
// the name ("Glucose, serum (random)"), and ignores blood/serum/plasma qualifiers
// and ion charges ("Blood Lactate", "WBC count, serum", "HCO3−").
function findLabReferenceLoose(text) {
  const exact = findLabReference(text);
  if (exact) return exact;
  const clean = s => String(s || '').replace(/[−+⁻⁺]/g, '').replace(/,\s*(serum|plasma|blood)\b/ig, '').replace(/^(serum|plasma|blood)\s+/i, '').trim();
  const strip = s => s.replace(/\([^)]*\)/g, ' ');
  const abbr = s => (s.match(/\(([^)]{2,})\)/) || [])[1] || '';
  const unbracket = s => s.replace(/\s*\(([^)]*)\)/g, ' $1'); // "Glucose (random)" → "Glucose random"
  const t = clean(text);
  // Strictest reading first, so "Glucose, serum (random)" finds "Glucose, random" before a
  // bracket-dropped alias such as "glucose (fasting)" → "glucose" can claim it.
  const tiers = [[t, unbracket(t)], [abbr(t)], [strip(t)]];
  for (const tier of tiers) {
    const wanted = tier.map(normalizeLabName).filter(Boolean);
    if (!wanted.length) continue;
    for (const loose of [false, true]) {
      const ref = LAB_REFERENCE_RANGES.find(r => [r.name, ...(r.aliases || [])]
        .map(n => normalizeLabName(loose ? strip(n) : n)).some(k => wanted.includes(k)));
      // "Bicarbonate (HCO3⁻)" alone can be the blood-gas value (22–27) or the serum value (21–32); the
      // name cannot tell which, so no link rather than a page that may contradict the chart.
      if (ref) return /^Bicarbonate/.test(ref.name) ? null : ref;
    }
  }
  return null;
}
