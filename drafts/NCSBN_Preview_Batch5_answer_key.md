# NCSBN Exam Preview — Batch 5 (Items 97–113) — Answer Key (final batch)

Source: NCSBN NCLEX-RN® Next Generation NCLEX Exam Preview, ©2022 NCSBN
(https://www.nclex.com/prepare.page — "Download Exam Preview"), fifth attachment (21 pages,
items 97–113). As with every prior batch, **no answer key is published**. This batch also
contains no source screenshot revealing a mid-interaction selection, so every answer below is
this session's own clinical judgment and needs clinician review before publishing.

Item 97 (chest tube priority monitoring) is a repeated page from the previous PDF, already
built in batch 4 as `standalone_1784030000004`, and was skipped here — no duplicate created.

## Discovery: item 112 is a duplicate of an existing, wrong/incomplete item already in the bank

Item 112 ("Bow-Tie Example Screen 1") is NCSBN's own bowtie item-type example: a 79-year-old
female with stroke-like symptoms (facial drooping, hemiparesis, expressive aphasia) whose
random serum glucose (4.2 mmol/L) is below the elderly reference range — hypoglycemia
mimicking stroke.

This exact scenario, with the exact same Nurses' Notes / History and Physical / Laboratory
Results content, is **already in the live bank** as `case_1789577787012` ("Bowtie-Stroke",
filed under course/unit "Others"/"Others"). It is one of the 4 "known incomplete" items
`tools/check.js` has been tolerating in its baseline across every batch this session
("answer key scores 3/5"). Investigating it turned up 2 real bugs, not just incompleteness:

- `bowtieConditions` marked **"ischemic stroke"** correct — the source, and the client's
  glucose level, both point to **hypoglycemia**.
- `bowtieActions` marked "Administer oxygen at 2 L/min via nasal cannula" as one of the 2
  correct actions — the source's 2 correct actions are **"Insert a peripheral venous access
  device (VAD)"** and **"Request an order for 50% dextrose in water to be administered
  intravenously,"** the direct treatment for symptomatic hypoglycemia.
- `bowtieParams` was missing 3 of its 5 options outright (blank placeholders) — this was the
  source of the "3/5" score. The 2 correct parameters are "neurologic status" (confirms the
  deficits resolve once glucose is corrected) and "serum glucose level"; the 5th, non-correct
  option is "electrocardiogram (ECG) rhythm."

Following the same precedent as the appendicitis-case duplicate found in an earlier batch
(and per your instruction there — "fix the existing item"), I fixed `case_1789577787012` in
place rather than creating a new duplicate item: corrected all 3 fields above (verified
against the source's own highlighted correct answers, see the walkthrough PDF pages for item
112), moved it from "Others"/"Others" to **NURS 1017 Unit 11 (Endocrine Disorders)**, renamed
the misleading title "Bowtie-Stroke" to "NURS 1017 Unit 11 Bowtie 1: Hypoglycemia Mimicking
Stroke," added the copyright footnote, and added a full rationale. The Nurses' Notes, History
and Physical, and Laboratory Results tab content are preserved verbatim from the existing
item. Draft file: `drafts/case_1789577787012_FIXED_NURS_1017_Unit_11_Bowtie_1.json`
(`drafts/fix_bowtie_hypoglycemia.py`). It now scores 5/5 — this drops the check.js known-incomplete
count from 4 to 3 once this fix is published.

## Items I'd most want a clinician's second opinion on

- **Item 101** (alcohol-based hand rub staff education) — genuinely ambiguous: Options 1
  ("use before touching medical equipment that will have direct client contact") and 4 ("use
  after contact with body excretions that do not cause visible soiling") are each
  independently defensible as the single correct statement per CDC hand-hygiene guidance. I
  went with Option 1 as the cleaner, unconditional "moment" statement, but a nursing
  instructor's read would help.
- **Item 99** (occupational vs. physical therapy referral) — I read the RA client with a
  newborn as needing OT (joint-protection/adaptive-equipment teaching for ADLs), but the
  postop hip-fracture surgeon is also a plausible OT candidate (fine-motor return-to-work
  planning); the intended distinction may be OT-vs-PT scope rather than which client "needs
  more help."
- **Item 111** (umbilical cord prolapse) — I chose the knee-chest position as the nurse's
  independent action over left-side-lying; both are taught techniques for relieving cord
  compression, and some programs teach a modified Sims/left-lateral-with-hips-elevated
  position as equally correct.
- **Item 89 (not in this batch, but a running note):** none open from prior batches remain
  besides what's already flagged in their own docs.

## Full item list

| # | Title | Placement | Correct answer |
|---|---|---|---|
| 98 | Psychiatric Next Intervention (Schizophrenia) | Others | Administer prescribed risperidone |
| 99 | Occupational Therapy Referral | NURS 1017 Unit 6 | RA client with a 2-month-old infant |
| 100 | Airborne Precautions Room Placement | Others | Private room, monitored negative air pressure |
| 101 | Alcohol-Based Hand Rub Staff Education | Others | Use before touching equipment with direct client contact |
| 102 | Mononucleosis Assessment Findings | NURS 1021 Unit 4 | Cervical lymphadenopathy |
| 103 | UAP Delegation of Positioning Task | Others | Prone-position stable AKA client, POD1 |
| 104 | Support Group Priority to Intervene | Others | Manic client, restless/moving legs |
| 105 | Client Rights / Staff Boundary Violation | Others | "Clients have a right to provide feedback...without fear of punishment." |
| 106 | Prioritization — Pulsus Paradoxus in Pericarditis | NURS 1021 Unit 2 | Pericarditis client (cardiac tamponade risk) |
| 107 | Milieu De-escalation During Medication Pass | Others | Ask another nurse to finish meds; primary nurse talks with client |
| 108 | HIV Client Teaching Evaluation | NURS 1021 Unit 4 | "I take echinacea..." (needs follow-up) |
| 109 | Informed Consent Staff Education (SATA) | Others | Nurse verifies understanding, PHCP discloses risk of refusal, consent before opioids, emergency exception |
| 110 | Wrong IV Fluid Infusing — First Action | Others | Assess the client |
| 111 | Umbilical Cord Prolapse Priority Action | Others | Knee-chest position |
| 112 | (fix, existing item) Hypoglycemia Mimicking Stroke (Bowtie) | NURS 1017 Unit 11 | Hypoglycemia; insert VAD + request IV dextrose; monitor neuro status + glucose |
| 113 | Aminoglycoside — Renal Function Labs | NURS 1021 Unit 7 | BUN and serum creatinine |

Full rationale for each item is in the walkthrough PDF (shown after answering) and in
`drafts/build_ncsbn_preview_batch5.py` / `drafts/fix_bowtie_hypoglycemia.py`.

## Verification performed this session

- All 14 new stand-alone items and the corrected bowtie item render in the real player
  (Supabase blocked), score full marks against the answer keys above, and pass `itemProblems`
  (0 issues each).
- Editor open-and-save round-trip: empty diff for all 15 items.
- Full `tools/check.js` against the **live, unpublished** bank (84 items, 214 screens): 0
  failures, 4 known-incomplete items — same baseline as every prior batch. (This is expected:
  the bowtie fix above is still a draft file and hasn't been published, so the live bank still
  shows `case_1789577787012` scoring 3/5. That count will drop to 3 once this batch is
  published.) Note: this run also reported the editor's open-and-save changing 2 pre-existing
  items unrelated to this session (`standalone_1783010000003`, `standalone_1781726101855`) —
  confirmed via `git diff --stat HEAD` that this branch's tracked files are unmodified from the
  last commit, so this is a pre-existing condition on the branch, not something introduced by
  this batch; flagging it here for a future session to look into.
- Full `tools/check-saving.js`: 13/13 checks pass.
- **Not yet done:** clinician sign-off, and publishing. Everything stays on
  `claude/modest-galileo-5dtly1` — nothing pushed to `main` or Supabase.

## Running total across all 5 batches (this is the last one)

- **93 stand-alone questions** (6 + 19 + 27 + 27 + 14)
- **3 case studies** (2 new + 1 fixed existing — appendicitis)
- **1 existing item corrected** in addition to the case studies (the bowtie/hypoglycemia item)
- All still sitting on the branch, unpublished, per your instruction — this was the last batch
  of PDFs, so the next step is your call on publishing (merge to `main`, then the Supabase
  `add`/`upload` workflow) whenever you're ready.
