# NCSBN Exam Preview — Batch 2 (Items 13–31) — Answer Key

Source: NCSBN NCLEX-RN® Next Generation NCLEX Exam Preview, ©2022 NCSBN
(https://www.nclex.com/prepare.page — "Download Exam Preview"), second attachment (19 pages,
items 13–31). Same situation as batch 1: **the source PDF publishes no answer key** for any of
these — every correct answer and rationale below is this session's own clinical judgment, not
a verified NCSBN key. **All 19 items need clinician review before publishing.**

Per your standing instruction, items with no matching NURS 1017/1021 unit are filed under
`course: "Others"` / `unit: "Others"` to be classified later. Of 19 items, 2 map to NURS 1021
Unit 3 (Respiratory) and 1 to NURS 1017 Unit 7 (Neurological); the remaining 16 are "Others" —
mostly multi-system prioritization and infection-control precaution questions with no matching
curriculum unit at all.

## Items where I'd most want a clinician's second opinion

These are close, comparative-judgment calls where reasonable clinicians could disagree, more so
than the rest of the batch:

- **Item 14** (unit transfer appropriateness) — I read "most appropriate to transfer" as "most
  stable / least specialized nursing need," landing on the afebrile HCV client. An alternative
  reading of the stem is possible.
- **Item 15** and **Item 24** (both "first assess" across 4 unrelated client situations) — I
  prioritized objective red-flag findings (accessory muscle use; bronchial breath sounds + high
  fever) over chronic-disease symptom flares, but these multi-system comparisons are inherently
  more subjective than a single-system question.
- **Item 19** (first assess after thoracic surgery) — hemoptysis in a COPD client vs. expected
  post-pneumonectomy positioning; I'm fairly confident here but it's still a comparative call.
- **Item 20** (pediatric concussion) — all 4 options describe fairly unremarkable findings; I
  reasoned that precise documentation of arousability is the most clinically central parameter
  to hand off in concussion monitoring, but this is my weakest-confidence item in the batch.
- **Item 21** (same-day surgery, first to see) — a hot casted leg (possible compartment
  syndrome) vs. post-cataract nausea (aspiration/IOP risk); I went with the cast, but I talked
  myself into the opposite answer partway through reasoning it out, worth a second look.

## Full item list

| # | Title | Placement | Correct answer |
|---|---|---|---|
| 13 | Positive Pressure Ventilation Client Teaching | NURS 1021 Unit 3 | "Clients may develop stress ulcers and GI bleeding." |
| 14 | Unit Transfer Appropriateness | Others | Client with HCV, afebrile 24h |
| 15 | First Assessment Across Client Situations | Others | COPD client using accessory muscles |
| 16 | Appropriate UAP Task Assignment | Others | Assisting AFib client to shower |
| 17 | Infant Feeding Pattern Follow-up | Others | 9-month-old, 10 bottles 2% milk/day |
| 18 | Client Privacy Violation | Others | Sharing BAL result with police |
| 19 | Priority Assessment After Thoracic Surgery | NURS 1021 Unit 3 | COPD client reporting hemoptysis |
| 20 | Concussion Observation Significance | Others | "Sleeping but easily aroused" |
| 21 | Same-Day Surgery First Assessment | Others | Casted leg feels hot (1h post-cast) |
| 22 | MS Ataxia Care Planning | NURS 1017 Unit 7 | Referral to physical therapist |
| 23 | Home-Health First Visit | Others | Chemo client with fever 101.1°F |
| 24 | First Assessment Across Client Situations 2 | Others | Bacterial pneumonia, bronchial breath sounds + 103.3°F |
| 25 | Pertussis Care Planning | Others | Implement droplet precautions |
| 26 | Precaution Type Teaching Evaluation | Others | Gown for E. coli O157:H7, incontinent |
| 27 | Extrinsic Fall Risk Factors (SATA) | Others | Uneven stairs, throw rugs, dim lighting |
| 28 | Impetigo Contact Precautions (SATA) | Others | Gown for linens, gloves at door |
| 29 | TB Isolation Evaluation | Others | Tissues/trash within reach |
| 30 | Measles Room Assignment | Others | Private room, negative air pressure |
| 31 | Precaution Violation Identification | Others | Gown+gloves only (missing mask) for H. flu meningitis |

Full rationale for each item is in the walkthrough PDF (shown after answering) and in
`drafts/build_ncsbn_preview_batch2.py`.

## Verification performed this session

- All 19 items render in the real player (Supabase blocked), score full marks against the
  answer keys above, and pass `itemProblems` (0 issues each).
- Editor open-and-save round-trip: empty diff for all 19.
- Full `tools/check.js` (84 items, 214 screens): 0 failures, 4 known-incomplete items — same
  baseline as before, unaffected by this batch.
- Full `tools/check-saving.js`: 13/13 checks pass.
- **Not yet done:** clinician sign-off, and publishing. Per your instruction, everything stays
  on this branch (`claude/modest-galileo-5dtly1`) — nothing pushed to `main` or Supabase — until
  you're done sending batches and ready to publish the whole set at once.
