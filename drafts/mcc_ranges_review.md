# Lab reference ranges aligned with MCC (November 2026)

Source: Medical Council of Canada, *Normal lab values* (last updated December 2020), as stored in `js/lab-ranges.js`.
Generator: `drafts/build_mcc_ranges_patch.js` (Playwright, run against the app with `cases-data.js`) → `drafts/mcc_ranges_patch.json`, applied with the workflow's `patch` action.

- Lab-table rows recognised as MCC tests: 1513
- Already matching MCC: 517; matching MCC for the one sex shown: 201
- **Changed to the MCC range: 644 rows** in 41 items (139 chart tabs). Potassium is 3.5–5.1 mmol/L everywhere it was changed.
- Left as written, for review: 151 rows (below).

Rules: a range was changed only when its units matched MCC (mEq/L → mmol/L for potassium, sodium, chloride and bicarbonate, with the row's result units changed to match), and either every result on the row keeps the same low/normal/high reading or no question in the item mentions the test. If one screen of an item keeps a test's old range, every screen keeps it. Newborn and pediatric items (client under 18) were not changed: MCC lists adult values only.

## Changes that alter the reading of a background result (test not used in any question)

| Item | Test | Old range | MCC range | Result reading |
|---|---|---|---|---|
| University of Maryland - CS3 | PaO2 | 75–100 mm Hg | 83–116 mm Hg | 75 mm Hg: N→L |
| University of Maryland - CS4 | Potassium | 3.5–5.0 mmol/L | 3.5–5.1 mmol/L | 5.1 mmol/L: H→N |
| University of Maryland - CS13 | Hemoglobin (Hgb) | Male: 130–180 g/L; Female: 120–160 g/L | Female: 115–155 g/L; Male: 125–170 g/L | 115 g/L: L→N (F) |
| University of Maryland - CS14 | Urea (BUN) | 3.6–7.1 mmol/L | 2.1–8.0 mmol/L | 7.9 mmol/L: H→N |
| University of Maryland - CS19 | Hematocrit (Hct) | Male: 0.42–0.52 L/L; Female: 0.35–0.47 L/L | 0.38–0.50 L/L | 0.40 L/L: L→N |
| University of Maryland - CS20 | HCO3⁻ | 22–26 mmol/L | 21–32 mmol/L | 27 mmol/L: H→N |
| University of Maryland - CS2 Trend | Hemoglobin A1c (HbA1c) | < 5.7% | 4.8%–6.0% | 6.0%: H→N |
| University of Maryland - CS15 Bowtie | Hematocrit (Hct) | Male: 0.42–0.52 L/L; Female: 0.35–0.47 L/L | 0.38–0.50 L/L | 0.37 L/L: N→L |
| University of Maryland - CS16 Bowtie | Urea (BUN) | 3.6–7.1 mmol/L | 2.1–8.0 mmol/L | 7.9 mmol/L: H→N |
| University of Maryland - CS19 Bowtie | Prothrombin time (PT) | 9.5–12 seconds | 10–14 s | 13.5 seconds: H→N |
| University of Maryland - CS20 Bowtie | HCO3⁻ | 22–26 mmol/L | 21–32 mmol/L | 27 mmol/L: H→N |

## Left as written (review)

| Item | Screen | Test | Range in the chart | MCC | Why |
|---|---|---|---|---|---|
| NURS 1017 Unit 1 Case Study 3 | 2 | Rheumatoid Factor (RF) | < 14 IU/mL | ≤ 20 kIU/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 1 Case Study 3 | 3 | Rheumatoid Factor (RF) | < 14 IU/mL | ≤ 20 kIU/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 1 Case Study 3 | 4 | Rheumatoid Factor (RF) | < 14 IU/mL | ≤ 20 kIU/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 1 Case Study 3 | 5 | Rheumatoid Factor (RF) | < 14 IU/mL | ≤ 20 kIU/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 1 Case Study 3 | 6 | Rheumatoid Factor (RF) | < 14 IU/mL | ≤ 20 kIU/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 4 Case Study 4 | 2 | Absolute Neutrophil Count (ANC) | 1,500 – 8,000 /mm³ | 2.0–7.5 × 10⁹/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 4 Case Study 4 | 3 | Absolute Neutrophil Count (ANC) | 1,500 – 8,000 /mm³ | 2.0–7.5 × 10⁹/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 4 Case Study 4 | 4 | Absolute Neutrophil Count (ANC) | 1,500 – 8,000 /mm³ | 2.0–7.5 × 10⁹/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 4 Case Study 4 | 5 | Absolute Neutrophil Count (ANC) | 1,500 – 8,000 /mm³ | 2.0–7.5 × 10⁹/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 4 Case Study 4 | 6 | Absolute Neutrophil Count (ANC) | 1,500 – 8,000 /mm³ | 2.0–7.5 × 10⁹/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 4 Case Study 5 | 2 | Serum Sodium | 135 – 145 mmol/L | 136–146 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 4 Case Study 5 | 2 | Urine Osmolality | 50 – 1,200 mOsm/kg | 38–1400 mOsm/kg H₂O | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 4 Case Study 5 | 2 | Urine Sodium | > 40 mmol/L in SIADH | 40.0–220.0 mmol/24 h | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 4 Case Study 5 | 3 | Serum Sodium | 135 – 145 mmol/L | 136–146 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 4 Case Study 5 | 3 | Urine Osmolality | 50 – 1,200 mOsm/kg | 38–1400 mOsm/kg H₂O | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 4 Case Study 5 | 3 | Urine Sodium | > 40 mmol/L in SIADH | 40.0–220.0 mmol/24 h | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 4 Case Study 5 | 4 | Serum Sodium | 135 – 145 mmol/L | 136–146 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 4 Case Study 5 | 4 | Urine Osmolality | 50 – 1,200 mOsm/kg | 38–1400 mOsm/kg H₂O | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 4 Case Study 5 | 4 | Urine Sodium | > 40 mmol/L in SIADH | 40.0–220.0 mmol/24 h | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 4 Case Study 5 | 5 | Serum Sodium | Rise ≤ 8–10 mmol/L / 24h | 136–146 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 4 Case Study 5 | 5 | Serum Sodium | 135 – 145 mmol/L | 136–146 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 4 Case Study 5 | 5 | Urine Osmolality | 50 – 1,200 mOsm/kg | 38–1400 mOsm/kg H₂O | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 4 Case Study 5 | 5 | Urine Sodium | > 40 mmol/L in SIADH | 40.0–220.0 mmol/24 h | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 4 Case Study 5 | 6 | Serum Sodium | Rise ≤ 8–10 mmol/L / 24h | 136–146 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 4 Case Study 5 | 6 | Serum Sodium | 135 – 145 mmol/L | 136–146 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 4 Case Study 5 | 6 | Urine Osmolality | 50 – 1,200 mOsm/kg | 38–1400 mOsm/kg H₂O | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 4 Case Study 5 | 6 | Urine Sodium | > 40 mmol/L in SIADH | 40.0–220.0 mmol/24 h | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 5 Case Study 4 | 2 | Hematocrit | 42 – 52% | 0.38–0.50 L/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 5 Case Study 4 | 3 | Hematocrit | 42 – 52% | 0.38–0.50 L/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 5 Case Study 4 | 4 | Hematocrit | 42 – 52% | 0.38–0.50 L/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 5 Case Study 4 | 5 | Hematocrit | 42 – 52% | 0.38–0.50 L/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 5 Case Study 4 | 6 | Hematocrit | 42 – 52% | 0.38–0.50 L/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 5 Case Study 6 | 1 | Hemoglobin | 135–175 g/L | Female: 115–155 g/L; Male: 125–170 g/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 5 Case Study 6 | 2 | Hemoglobin | 135–175 g/L | Female: 115–155 g/L; Male: 125–170 g/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 5 Case Study 6 | 3 | Hemoglobin | 135–175 g/L | Female: 115–155 g/L; Male: 125–170 g/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 5 Case Study 6 | 4 | Hemoglobin | 135–175 g/L | Female: 115–155 g/L; Male: 125–170 g/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 5 Case Study 6 | 5 | Hemoglobin | 135–175 g/L | Female: 115–155 g/L; Male: 125–170 g/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1017 Unit 5 Case Study 6 | 6 | Hemoglobin | 135–175 g/L | Female: 115–155 g/L; Male: 125–170 g/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1021 Unit 6 Case Study 3 | 4 | Creatinine (Cr) | 53–106 mcmol/L (0.6–1.2 mg/dL) | Female: 22–75 µmol/L; Male: 49–93 µmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1021 Unit 6 Case Study 3 | 4 | Glucose | 3.9–6.1 mmol/L (74–106 mg/dL) | 4.0–11.0 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1021 Unit 6 Case Study 3 | 4 | Hematocrit (Hct) | 42%–52% (0.42–0.52 volume fraction) | 0.38–0.50 L/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1021 Unit 6 Case Study 3 | 4 | Hemoglobin (Hgb) | 8.7–11.2 mmol/L (14–18 g/dL) | Female: 115–155 g/L; Male: 125–170 g/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1021 Unit 6 Case Study 3 | 4 | Red blood cells (RBCs) | 4.7–6.1 × 10⁹/L (4.7–6.1 × 10⁶ mcL) | Female: 3.50–5.00 × 10¹²/L; Male: 4.00–5.50 × 10¹²/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1021 Unit 6 Case Study 3 | 5 | Creatinine (Cr) | 53–106 mcmol/L (0.6–1.2 mg/dL) | Female: 22–75 µmol/L; Male: 49–93 µmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1021 Unit 6 Case Study 3 | 5 | Glucose | 3.9–6.1 mmol/L (74–106 mg/dL) | 4.0–11.0 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1021 Unit 6 Case Study 3 | 5 | Hematocrit (Hct) | 42%–52% (0.42–0.52 volume fraction) | 0.38–0.50 L/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1021 Unit 6 Case Study 3 | 5 | Hemoglobin (Hgb) | 8.7–11.2 mmol/L (14–18 g/dL) | Female: 115–155 g/L; Male: 125–170 g/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1021 Unit 6 Case Study 3 | 5 | Red blood cells (RBCs) | 4.7–6.1 × 10⁹/L (4.7–6.1 × 10⁶ mcL) | Female: 3.50–5.00 × 10¹²/L; Male: 4.00–5.50 × 10¹²/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1021 Unit 6 Case Study 3 | 6 | Creatinine (Cr) | 53–106 mcmol/L (0.6–1.2 mg/dL) | Female: 22–75 µmol/L; Male: 49–93 µmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1021 Unit 6 Case Study 3 | 6 | Glucose | 3.9–6.1 mmol/L (74–106 mg/dL) | 4.0–11.0 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1021 Unit 6 Case Study 3 | 6 | Hematocrit (Hct) | 42%–52% (0.42–0.52 volume fraction) | 0.38–0.50 L/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1021 Unit 6 Case Study 3 | 6 | Hemoglobin (Hgb) | 8.7–11.2 mmol/L (14–18 g/dL) | Female: 115–155 g/L; Male: 125–170 g/L | left as written to stay the same as another screen of this case, where it is flagged |
| NURS 1021 Unit 6 Case Study 3 | 6 | Red blood cells (RBCs) | 4.7–6.1 × 10⁹/L (4.7–6.1 × 10⁶ mcL) | Female: 3.50–5.00 × 10¹²/L; Male: 4.00–5.50 × 10¹²/L | left as written to stay the same as another screen of this case, where it is flagged |
| Unit 1 Stand-alone 3: Acute Mesenteric Ischemia & Gangrene | 1 | White Blood Cells (WBC) | 4,500–11,000 /mm³ | 3.5–10.5 × 10⁹/L | left as written to stay the same as another screen of this case, where it is flagged |
| Unit 4 Stand-alone 1: Paraneoplastic SIADH Syndrome | 1 | Urine Osmolality | 300–900 mOsm/kg | 38–1400 mOsm/kg H₂O | left as written to stay the same as another screen of this case, where it is flagged |
| Unit 4 Stand-alone 1: Paraneoplastic SIADH Syndrome | 1 | Urine Sodium | 20–40 mEq/L | 40.0–220.0 mmol/24 h | left as written to stay the same as another screen of this case, where it is flagged |
| Unit 5 Stand-alone 1: Burn Shock Pathophysiology | 1 | Hematocrit | 38–48% | 0.38–0.50 L/L | left as written to stay the same as another screen of this case, where it is flagged |
| Unit 7 Stand-alone 9: Bowtie - Increased ICP After Craniotomy | 1 | hematocrit (HCT) | Male: 42%–52% (0.42–0.52) | 0.38–0.50 L/L | left as written to stay the same as another screen of this case, where it is flagged |
| Unit 7 Stand-alone 9: Bowtie - Increased ICP After Craniotomy | 1 | hemoglobin (Hgb) | Male: 14–18 g/dL (140–180 g/L) | Female: 115–155 g/L; Male: 125–170 g/L | left as written to stay the same as another screen of this case, where it is flagged |
| Unit 7 Stand-alone 9: Bowtie - Increased ICP After Craniotomy | 1 | white blood cell (WBC) count | 4,500–11,000/mm³ (4.5–11 x 10⁹/L) | 3.5–10.5 × 10⁹/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS1 | 3 | Hematocrit | 38 - 50% | 0.38–0.50 L/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS1 | 4 | Hematocrit | 38 - 50% | 0.38–0.50 L/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS1 | 5 | Hematocrit | 38 - 50% | 0.38–0.50 L/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS1 | 6 | Hematocrit | 38 - 50% | 0.38–0.50 L/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS11 | 1 | Neutrophils, serum | 0.55–0.70 (55–70%) | 2.0–7.5 × 10⁹/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS11 | 2 | Neutrophils, serum | 0.55–0.70 (55–70%) | 2.0–7.5 × 10⁹/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS11 | 3 | Neutrophils, serum | 0.55–0.70 (55–70%) | 2.0–7.5 × 10⁹/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS11 | 4 | Neutrophils, serum | 0.55–0.70 (55–70%) | 2.0–7.5 × 10⁹/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS11 | 5 | Neutrophils, serum | 0.55–0.70 (55–70%) | 2.0–7.5 × 10⁹/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS11 | 6 | Neutrophils, serum | 0.55–0.70 (55–70%) | 2.0–7.5 × 10⁹/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS13 | 3 | Cholesterol, total | Normal < 5.2 mmol/L; borderline 5.2–6.2 mmol/L; high ≥ 6.2 mmol/L | 3.5–5.2 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS13 | 3 | Sodium | 135–145 mmol/L | 136–146 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS13 | 4 | Cholesterol, total | Normal < 5.2 mmol/L; borderline 5.2–6.2 mmol/L; high ≥ 6.2 mmol/L | 3.5–5.2 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS13 | 4 | Sodium | 135–145 mmol/L | 136–146 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS13 | 5 | Cholesterol, total | Normal < 5.2 mmol/L; borderline 5.2–6.2 mmol/L; high ≥ 6.2 mmol/L | 3.5–5.2 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS13 | 5 | Sodium | 135–145 mmol/L | 136–146 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS13 | 6 | Cholesterol, total | Normal < 5.2 mmol/L; borderline 5.2–6.2 mmol/L; high ≥ 6.2 mmol/L | 3.5–5.2 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS13 | 6 | Sodium | 135–145 mmol/L | 136–146 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS14 | 1 | Hematocrit (Hct) | Male: 0.42–0.52 L/L; Female: 0.35–0.47 L/L | 0.38–0.50 L/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS14 | 2 | Hematocrit (Hct) | Male: 0.42–0.52 L/L; Female: 0.35–0.47 L/L | 0.38–0.50 L/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS14 | 3 | Hematocrit (Hct) | Male: 0.42–0.52 L/L; Female: 0.35–0.47 L/L | 0.38–0.50 L/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS14 | 4 | Hematocrit (Hct) | Male: 0.42–0.52 L/L; Female: 0.35–0.47 L/L | 0.38–0.50 L/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS14 | 5 | Hematocrit (Hct) | Male: 0.42–0.52 L/L; Female: 0.35–0.47 L/L | 0.38–0.50 L/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS14 | 6 | Hematocrit (Hct) | Male: 0.42–0.52 L/L; Female: 0.35–0.47 L/L | 0.38–0.50 L/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS16 | 1 | Ammonia | 6–47 µmol/L | ≤ 35 µmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS16 | 1 | Glucose, fasting | < 5.5 mmol/L | 4.0–6.0 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS16 | 1 | Urea (BUN) | 3.6–7.1 mmol/L | 2.1–8.0 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS16 | 2 | Ammonia | 6–47 µmol/L | ≤ 35 µmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS16 | 2 | Glucose, fasting | < 5.5 mmol/L | 4.0–6.0 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS16 | 2 | Urea (BUN) | 3.6–7.1 mmol/L | 2.1–8.0 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS16 | 3 | Ammonia | 6–47 µmol/L | ≤ 35 µmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS16 | 3 | Glucose, fasting | < 5.5 mmol/L | 4.0–6.0 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS16 | 3 | Urea (BUN) | 3.6–7.1 mmol/L | 2.1–8.0 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS16 | 4 | Ammonia | 6–47 µmol/L | ≤ 35 µmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS16 | 4 | Glucose, fasting | < 5.5 mmol/L | 4.0–6.0 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS16 | 4 | Urea (BUN) | 3.6–7.1 mmol/L | 2.1–8.0 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS16 | 5 | Ammonia | 6–47 µmol/L | ≤ 35 µmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS16 | 5 | Glucose, fasting | < 5.5 mmol/L | 4.0–6.0 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS16 | 5 | Urea (BUN) | 3.6–7.1 mmol/L | 2.1–8.0 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS16 | 6 | Ammonia | 6–47 µmol/L | ≤ 35 µmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS16 | 6 | Glucose, fasting | < 5.5 mmol/L | 4.0–6.0 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS16 | 6 | Urea (BUN) | 3.6–7.1 mmol/L | 2.1–8.0 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS16 Bowtie (hidden) | 1 | Glucose, fasting | < 5.5 mmol/L | 4.0–6.0 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS18 | 1 | Hemoglobin A1c (HbA1c) | < 5.7% | 4.8%–6.0% | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS18 | 1 | INR | 1.0 | 0.9–1.2 | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS18 | 2 | Hemoglobin A1c (HbA1c) | < 5.7% | 4.8%–6.0% | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS18 | 2 | INR | 1.0 | 0.9–1.2 | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS18 | 3 | Hemoglobin A1c (HbA1c) | < 5.7% | 4.8%–6.0% | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS18 | 3 | INR | 1.0 | 0.9–1.2 | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS18 | 4 | Hemoglobin A1c (HbA1c) | < 5.7% | 4.8%–6.0% | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS18 | 4 | INR | 1.0 | 0.9–1.2 | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS18 | 5 | Hemoglobin A1c (HbA1c) | < 5.7% | 4.8%–6.0% | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS18 | 5 | INR | 1.0 | 0.9–1.2 | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS18 | 6 | Hemoglobin A1c (HbA1c) | < 5.7% | 4.8%–6.0% | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS18 | 6 | INR | 1.0 | 0.9–1.2 | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS2 | 3 | Hemoglobin A1c (HbA1c) | < 5.7% | 4.8%–6.0% | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS2 | 4 | Hemoglobin A1c (HbA1c) | < 5.7% | 4.8%–6.0% | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS2 | 5 | Hemoglobin A1c (HbA1c) | < 5.7% | 4.8%–6.0% | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS2 | 6 | Hemoglobin A1c (HbA1c) | < 5.7% | 4.8%–6.0% | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS21 | 6 | Thyroid-stimulating hormone (TSH) | 0.45–4.5 mU/L | 0.34–5.60 mIU/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS21 Bowtie (hidden) | 1 | Thyroid-stimulating hormone (TSH) | 0.45–4.5 mU/L | 0.34–5.60 mIU/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS3 | 1 | Lactate | 0.5–2.2 mmol/L | 0.5–2.5 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS3 | 2 | Lactate | 0.5–2.2 mmol/L | 0.5–2.5 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS3 | 3 | Lactate | 0.5–2.2 mmol/L | 0.5–2.5 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS3 | 4 | Lactate | 0.5–2.2 mmol/L | 0.5–2.5 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS3 | 5 | Lactate | 0.5–2.2 mmol/L | 0.5–2.5 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS3 | 6 | Lactate | 0.5–2.2 mmol/L | 0.5–2.5 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS4 | 1 | Glucose, fasting | < 5.5 mmol/L | 4.0–6.0 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS4 | 2 | Glucose, fasting | < 5.5 mmol/L | 4.0–6.0 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS4 | 3 | Glucose, fasting | < 5.5 mmol/L | 4.0–6.0 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS4 | 4 | Glucose, fasting | < 5.5 mmol/L | 4.0–6.0 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS4 | 5 | Glucose, fasting | < 5.5 mmol/L | 4.0–6.0 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS4 | 6 | Glucose, fasting | < 5.5 mmol/L | 4.0–6.0 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS6 | 1 | Cholesterol, total | Normal < 5.2 mmol/L; borderline 5.2–6.2 mmol/L; high ≥ 6.2 mmol/L | 3.5–5.2 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS6 | 1 | Platelet count | 140–450 × 10⁹/L | 130–380 × 10⁹/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS6 | 1 | Troponin T | 0–40 ng/L | ≤ 0.1 µg/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS6 | 2 | Cholesterol, total | Normal < 5.2 mmol/L; borderline 5.2–6.2 mmol/L; high ≥ 6.2 mmol/L | 3.5–5.2 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS6 | 2 | Platelet count | 140–450 × 10⁹/L | 130–380 × 10⁹/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS6 | 2 | Troponin T | 0–40 ng/L | ≤ 0.1 µg/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS6 | 3 | Cholesterol, total | Normal < 5.2 mmol/L; borderline 5.2–6.2 mmol/L; high ≥ 6.2 mmol/L | 3.5–5.2 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS6 | 3 | Platelet count | 140–450 × 10⁹/L | 130–380 × 10⁹/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS6 | 3 | Troponin T | 0–40 ng/L | ≤ 0.1 µg/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS6 | 4 | Cholesterol, total | Normal < 5.2 mmol/L; borderline 5.2–6.2 mmol/L; high ≥ 6.2 mmol/L | 3.5–5.2 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS6 | 4 | Platelet count | 140–450 × 10⁹/L | 130–380 × 10⁹/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS6 | 4 | Troponin T | 0–40 ng/L | ≤ 0.1 µg/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS6 | 5 | Cholesterol, total | Normal < 5.2 mmol/L; borderline 5.2–6.2 mmol/L; high ≥ 6.2 mmol/L | 3.5–5.2 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS6 | 5 | Platelet count | 140–450 × 10⁹/L | 130–380 × 10⁹/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS6 | 5 | Troponin T | 0–40 ng/L | ≤ 0.1 µg/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS6 | 6 | Cholesterol, total | Normal < 5.2 mmol/L; borderline 5.2–6.2 mmol/L; high ≥ 6.2 mmol/L | 3.5–5.2 mmol/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS6 | 6 | Platelet count | 140–450 × 10⁹/L | 130–380 × 10⁹/L | left as written to stay the same as another screen of this case, where it is flagged |
| University of Maryland - CS6 | 6 | Troponin T | 0–40 ng/L | ≤ 0.1 µg/L | left as written to stay the same as another screen of this case, where it is flagged |
