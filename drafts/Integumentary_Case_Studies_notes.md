# Integumentary Case Studies (with Claude Opus 5.5) — Source Notes

**Placement:** all 3 under NURS 1017 Unit 5 (Integumentary Disorders and Burns), as
`case_1782390000006` ("Case Study 6" — Flame Burns), `case_1782390000007` ("Case Study 7" —
Herpes Zoster), `case_1782390000008` ("Case Study 8" — Erythroderma), continuing the unit's
existing "Case Study 1–5" numbering.

**Attribution:** per your instruction, no NCSBN footnote (this isn't NCSBN content). Since the
source PDFs state they're adapted from OpenStax *Medical-Surgical Nursing* (2024), Ch. 14,
under CC BY-NC-SA 4.0 — a license that requires attribution — I added a footnote crediting
OpenStax instead, matching the source document's own required attribution line, distinct from
the NCSBN one used elsewhere in this bank.

## A small, backward-compatible code change was needed

Your answer key specifies exact NCSBN-style "rationale dyad" scoring in two places:
- Case 1, Item 3: 4 blanks as **two independent pairs** (blanks 1+2, blanks 3+4), each pair
  worth 1 point only if *both* its blanks are correct. Max 2 points.
- Case 3, Item 2: 5 blanks; blanks 1+2 are **one dyad pair** (1 point only if both correct);
  blanks 3, 4, 5 are each scored independently (1 point each). Max 4 points.

The app's existing `dyad` question type only supports a *single* pair of exactly 2 blanks
scored as one point, and `triad` only a single group of exactly 3 — neither covers "two pairs
in one item" or "one pair plus independent blanks." Rather than silently switching to
simpler-but-wrong per-blank scoring (which would have changed your stated max points), I added
an optional `cloze.scoreGroups` field to `js/scoring.js`: an array of blank-index groups scored
together as one all-or-nothing point, with any blank not listed in a group scored individually
as before. **Omitting `scoreGroups` leaves every existing item's scoring completely unchanged**
— this was verified by the full regression suite (`tools/check.js`, 84 items / 214 screens, 0
failures, same baseline as before the change) and by 3 targeted edge-case tests (a pair with
one blank wrong scores 0 for that pair, not partial credit; both pairs correct scores the full
max; both wrong scores 0).

All other multi-blank items in this batch (Case 1 Item 4, Case 2 Item 3, Case 3 Item 3) use
plain independent per-blank scoring, matching their own stated "0/1 scoring: 1 point per blank"
rules — no `scoreGroups` needed there.

## Other structural choices

- **Highlight-table items** (Case 1 Item 1, Case 2 Item 6, Case 3 Item 1): your source shows
  these with a checkbox next to each table row. The app's `highlight` question type is a
  general text/table highlighter (it walks the rendered HTML recursively, so it works inside
  table cells) — I built these as an HTML table with each row's Result cell wrapped as the
  highlightable phrase, which renders and scores identically to a checkbox-per-row list.
- **Drag-and-drop word bank** (Case 2 Item 5): used the app's `drag_drop_cloze` type, giving
  each of the 5 blanks the full 10-word bank with only its own correct word flagged — this
  lets every blank display the identical shared word list (matching a real drag-and-drop UI)
  while still scoring each blank independently by exact text match.
- **Matrix questions**: "consistent with X, Y, or Z (may support more than one)" items use
  `matrix_mr` (multi-select per row, scored cell-by-cell); "specify whether it is X or Y"
  single-answer items use `matrix_mc` (one answer per row).

## Verification performed this session

- All 18 screens across the 3 case studies render in the real player (Supabase blocked), score
  full marks, and pass `itemProblems` (0 issues each). Total points per case — 36, 29, 38 — sum
  to 103, matching your answer key's own "All cases" total exactly.
- Editor open-and-save round-trip: empty diff for all 3 case studies.
- Full `tools/check.js` (84 items, 214 screens): 0 failures, same 4-item known-incomplete
  baseline as every prior batch — confirming the `scoring.js` change didn't affect anything
  else in the bank.
- Full `tools/check-saving.js`: 13/13 checks pass.
- 3 targeted edge-case tests on the new `scoreGroups` logic (see above).
- **Not yet done:** clinician sign-off, and publishing. Everything stays on
  `claude/modest-galileo-5dtly1` — nothing pushed to `main` or Supabase.
