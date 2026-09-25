# NCSBN Exam Preview — Batch 3 (Items 32–64) — Answer Key

Source: NCSBN NCLEX-RN® Next Generation NCLEX Exam Preview, ©2022 NCSBN
(https://www.nclex.com/prepare.page — "Download Exam Preview"), third attachment (38 pages,
items 32–64: one 6-screen case study + 27 stand-alone items). As with batches 1 and 2, **no
answer key is published** for these except where the source screenshots happen to show a
selection mid-interaction (the case study's screen 3 dropdown and screen 6 highlight — both
confirmed against the source and built exactly as shown). Everything else is this session's
own clinical judgment and needs clinician review before publishing.

## Case Study — NURS 1021 Unit 6 Case Study 2 (splenic laceration / hemothorax)

**Item ID:** `case_1786060000002`. A 17-year-old male struck by a pitched baseball, LUQ
bruising/tenderness, diminished left breath sounds, tachycardia, hypotension, anemia →
splenic laceration + left hemothorax → splenectomy → postop day 3 with concerning findings
(incentive spirometer refusal, maximal PCA use, continued nausea/vomiting).

- **Screen 1** (select-all, "requires immediate follow-up"): lung sounds, shoulder pain
  (possible Kehr's sign), lab results, abdominal findings, vitals (P/RR/BP) — **not** productive
  cough or temp/pulse ox.
- **Screen 2** (select-all, "at risk of developing"): hemothorax, bowel perforation, splenic
  laceration — **not** stroke, PE, or AAA.
- **Screen 3** (dropdown): "respiratory status" — ✅ **confirmed by the source's revealed
  selection**.
- **Screen 4** (matrix, indicated/not indicated): IV fluids, type & screen, NG tube, and pain
  medication = Indicated; chest percussion therapy = Not Indicated.
- **Screen 5** (select-all, pre-op actions): mark surgical site, medication reconciliation,
  insert VAD, assess prior surgery/anesthesia experience — **not** ice chips, obtaining consent
  (client is a minor), informing about risks/benefits (surgeon's role), or excluding parents.
- **Screen 6** (highlight, "worsening status"): the incentive-spirometer refusal + maximal
  PCA + continued nausea/vomiting sentence — ✅ **confirmed by the source's revealed
  highlight**, cropped and verified at 400 DPI the same way as the first case study.

## Items I'd most want a clinician's second opinion on

- **Item 51** (ineffective coping post-MI) — I picked the "financial catastrophizing"
  statement over the "trouble believing this happened" (denial) statement; reasonable people
  could argue denial at day 3 is the more classic "ineffective coping" answer.
- **Item 50** (PRBC transfusion, VAD gauge) — I read "24-gauge or larger" as meaning 24g is the
  minimum acceptable (larger-bore/lower-numbered gauges also fine); this phrasing is genuinely
  ambiguous and worth a nursing-instructor's read.
- **Item 56** (pediatric dysfunctional grieving) — I picked sleep refusal over the three
  "magical thinking" options (mock funerals, expecting the grandparent to visit, wanting to
  play at the cemetery), which I read as developmentally normal for a 4-year-old; a child/adol
  psych specialist may disagree on where the line sits.
- **Item 26** (batch 2, for reference) type of close call — same pattern here with **Item 43**
  (thoracic expansion assessment technique): both the posterior ("thumbs toward spine") and
  anterior ("thumbs toward xiphoid") descriptions are legitimate techniques; I went with the
  posterior/classic textbook version as the single correct answer.

## Full item list

| # | Title | Placement | Correct answer |
|---|---|---|---|
| 38 | Acute Kidney Injury Order Clarification | NURS 1021 Unit 7 | CT scan with IV contrast |
| 39 | Restraint Use Client Teaching | Others | "Requires an order from the PHCP" |
| 40 | Tuberculosis Plan of Care | Others | Mask on client during transport |
| 41 | Impetigo Parent Teaching | Others | Don't share towels with siblings |
| 42 | Bioterrorism Agent Transmission | Others | Bubonic plague statement (needs correction) |
| 43 | Thoracic Expansion Assessment Technique | NURS 1021 Unit 3 | Posterior hands/thumbs-to-spine technique |
| 44 | Perimenopause Hot Flash Management | NURS 1021 Unit 9 | Wearing clothing in layers |
| 45 | Health Promotion for Clients Over 65 | Others | Same pharmacy for all medications |
| 46 | Highest Risk for Leukemia | NURS 1017 Unit 4 | Colon cancer + chemotherapy |
| 47 | Older Adult Postop Priority Need | Others | Early mobilization |
| 48 | Pediatric UTI Prevention (SATA) | NURS 1021 Unit 7 | Empty bladder, fluids, perineal care, non-carbonated drinks |
| 49 | AD Family Teaching – Agitation (SATA) | NURS 1017 Unit 7 | Distraction, calendars, simple sentences, daytime exercise |
| 50 | PRBC Transfusion Preparation | NURS 1021 Unit 1 | VAD 24-gauge or larger |
| 51 | Ineffective Coping After MI | NURS 1021 Unit 2 | "Let down my family financially" statement |
| 52 | End-of-Life Comfort Care Teaching | Others | "Offering healthy foods frequently" (needs follow-up) |
| 53 | Informed Consent Validity (SATA) | Others | Voluntary, adequate disclosure, understanding |
| 54 | Sexual Assault Crisis Response (SATA) | Others | "Did the best you could" + "You are safe here" |
| 55 | AD Daily Care Planning (SATA) | NURS 1017 Unit 7 | Routine, scheduled voiding, self-introduction, clock/calendar |
| 56 | Pediatric Dysfunctional Grieving | Others | Refuses to sleep at night |
| 57 | Low-Sodium Diet Teaching | NURS 1021 Unit 2 | Fresh broccoli with herbs/spices |
| 58 | Post-Mastectomy ROM Exercise | NURS 1017 Unit 4 | "Wall climbing" with fingers |
| 59 | Expressive Aphasia Spouse Communication (SATA) | NURS 1017 Unit 7 | "Fine" may not be accurate, picture board, speech therapy |
| 60 | Buck Traction Immediate Intervention | NURS 1017 Unit 6 | Pillow under the knee |
| 61 | AD Home Care Teaching | NURS 1017 Unit 7 | Picture on bathroom door |
| 62 | Diverticulosis Client Teaching | NURS 1021 Unit 6 | Bulk-forming laxative may be prescribed |
| 63 | Medication Safety – Unfamiliar Dosage | Others | Contact the pharmacist |
| 64 | Neuroleptic Malignant Syndrome Priority Finding | Others | Fever |

Full rationale for each item is in the walkthrough PDF (shown after answering) and in
`drafts/build_ncsbn_preview_batch3.py` / `drafts/build_ncsbn_preview_case2.py`.

## Verification performed this session

- The case study and all 27 stand-alone items render in the real player (Supabase blocked),
  score full marks against the answer keys above, and pass `itemProblems` (0 issues each).
- Editor open-and-save round-trip: empty diff for all 28 items.
- Full `tools/check.js` (84 items, 214 screens): 0 failures, 4 known-incomplete items — same
  baseline as every prior batch, unaffected.
- Full `tools/check-saving.js`: 13/13 checks pass.
- **Not yet done:** clinician sign-off, and publishing. Everything stays on
  `claude/modest-galileo-5dtly1` — nothing pushed to `main` or Supabase — until you're done
  sending batches and ready to publish the whole set together.

## Running total across all 3 batches

- **52 stand-alone questions** (6 + 19 + 27)
- **2 case studies** (the fixed existing appendicitis case + this new splenic laceration case)
- All still sitting on the branch, unpublished, per your instruction.
