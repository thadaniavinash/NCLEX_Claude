# NCSBN Exam Preview — Batch 6 (Items 114–130) — Answer Key (final batch)

Source: NCSBN NCLEX-RN® Next Generation NCLEX Exam Preview, ©2022 NCSBN
(https://www.nclex.com/prepare.page — "Download Exam Preview"), sixth and **final**
attachment (17 pages, items 114–130: all 17 stand-alone items, no case study). As with every
batch, **no answer key is published**, and this batch contains no screenshot revealing a
mid-interaction selection or highlighted correct answer anywhere — every answer below is this
session's own clinical judgment and needs clinician review before publishing.

## Items I'd most want a clinician's second opinion on

- **Item 124** (VAD charting, "best example of correct documentation") — genuinely close call
  between Option 1 ("22-gauge catheter inserted into the right hand," precise objective
  device/site charting) and Option 4 ("labeled site, tubing, and intravenous fluid bag," a
  standard line-labeling safety practice). I went with Option 1 as the cleanest, most
  unambiguous objective statement, but a nursing-instructor's read would help.
- **Item 118** (informed consent, spinal fusion SATA) — I did not flag "the nurse notes that
  the client signed the consent form 1 week ago" as a follow-up situation, reasoning that a
  week-old signature isn't inherently a problem absent a change in the client's condition or
  understanding; some programs teach that consent should be reconfirmed closer to the day of
  surgery, which would make this option also correct.
- **Item 116** (bacterial conjunctivitis) — I read "eyes may be sensitive to light until the
  infection resolves" as not classically taught for bacterial conjunctivitis, but photophobia
  can occur with any significant ocular irritation; worth a second look.
- **Item 128** (disaster triage) — I picked the 15-year-old with a distended, firm abdomen
  over the 60-year-old with heart failure (SpO2 92%, RR 26) as higher priority; both reflect
  early decompensation and the relative ranking between "possible internal hemorrhage" and
  "worsening heart failure" in a mass-casualty context is a judgment call.

## Full item list

| # | Title | Placement | Correct answer |
|---|---|---|---|
| 114 | ERCP Pre-Procedure Questions (SATA) | NURS 1021 Unit 6 | Transportation home, thermometer access, allergies, dentures |
| 115 | Post-Cardiac-Catheterization Findings | NURS 1021 Unit 2 | 1+ pedal pulse, affected extremity |
| 116 | Bacterial Conjunctivitis Parent Teaching | NURS 1017 Unit 9 | Clean eyelids/eyelashes with soap and water before instilling medication |
| 117 | Insulin Infusion Pump Teaching Evaluation | NURS 1017 Unit 11 | "Decrease glucose monitoring to twice daily" (needs follow-up) |
| 118 | Informed Consent Follow-up Situations (SATA) | Others | Client unsure why surgery needed; client's fear of dying unaddressed |
| 119 | Transfer to Unlocked Unit Recommendation | Others | Schizophrenia, withdrawn, needs ADL assistance |
| 120 | Infant Projectile Vomiting - Diagnostic Workup (SATA) | NURS 1021 Unit 6 | Abdominal x-ray, ultrasound, complete metabolic panel |
| 121 | MVC Multi-Injury Priority Finding | Others | Hematoma on left side of neck |
| 122 | Prioritization - New Back Pain in AAA | NURS 1021 Unit 2 | AAA client, new low back pain |
| 123 | COPD Nutrition Documentation / Negligence Review | NURS 1021 Unit 3 | High-calorie, high-protein diet entry |
| 124 | Peripheral VAD Charting Example | Others | "22-gauge catheter inserted into the right hand" |
| 125 | Priority Lab Monitoring by Diagnosis | NURS 1021 Unit 8 | ABG for acid-base imbalance client |
| 126 | Collaborative Conflict Resolution Example | Others | Charge nurse + staff nurses + manager developing shared goals/plan |
| 127 | TB Contact Investigation | Others | Health department contacts family for examination |
| 128 | Disaster Triage Priority Client | Others | 15-year-old, restless, distended firm abdomen |
| 129 | Cast Neurovascular Compromise Telephone Triage | NURS 1017 Unit 6 | Swollen, cool toes in casted extremity |
| 130 | Clopidogrel Client Teaching | NURS 1021 Unit 1 | Report unusual bruising |

Full rationale for each item is in the walkthrough PDF (shown after answering) and in
`drafts/build_ncsbn_preview_batch6.py`.

## Note: unit label mismatch caught during review

While building this batch, 2 items (116, placed in NURS 1017 Unit 9; and 125, placed in NURS
1021 Unit 8) initially used unit label text that didn't exactly match the strings in
`CURRICULUM_COURSES` (`js/state.js`) — e.g. "Unit 9 (Sensory: Eyes and Ears)" instead of the
app's actual "Unit 9 (Disorders of the Eyes and Ears)". This caused the editor's unit dropdown
to silently reset the field on open-and-save, which the review pipeline's round-trip diff
check caught immediately (`.unit`, `.topic`, `.disorder` all changed). Both were corrected to
match `CURRICULUM_COURSES` exactly before this doc's final verification pass below.

## Verification performed this session

- All 17 stand-alone items render in the real player (Supabase blocked), score full marks
  against the answer keys above, and pass `itemProblems` (0 issues each).
- Editor open-and-save round-trip: empty diff for all 17 items (after the unit-label fix
  above).
- Full `tools/check.js` (84 items, 214 screens): 0 failures, 4 known-incomplete items — same
  baseline as every prior batch, unaffected. (The pre-existing, unrelated 2-item editor diff
  noted in the batch 5 doc is still present and still confirmed unrelated to this session's
  work.)
- Full `tools/check-saving.js`: 13/13 checks pass.
- **Not yet done:** clinician sign-off, and publishing. Everything stays on
  `claude/modest-galileo-5dtly1` — nothing pushed to `main` or Supabase.

## Running total across all 6 batches (this is genuinely the last one)

- **110 stand-alone questions** (6 + 19 + 27 + 27 + 14 + 17)
- **3 case studies** (2 new + 1 fixed existing — appendicitis)
- **1 existing item corrected** in addition to the case studies (the bowtie/ischemic-stroke
  item)
- All still sitting on the branch, unpublished, per your instruction — the next step is your
  call on publishing (merge to `main`, then the Supabase `add`/`upload` workflow) whenever
  you're ready.
