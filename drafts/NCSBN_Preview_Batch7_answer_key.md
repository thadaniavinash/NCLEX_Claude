# NCSBN Exam Preview — Batch 7 (Item Type Examples) — Answer Key

Source: NCSBN NCLEX-RN® Next Generation NCLEX Exam Preview, ©2022 NCSBN
(https://www.nclex.com/prepare.page — "Download Exam Preview"), seventh attachment (6 pages) —
NCSBN's own "Item Type Examples" section, showing 2 "Trend" examples and 2 "Bow-Tie" examples
used to teach the mechanics of those question types. **No answer key is published.**

## Duplicates confirmed (no new files)

- **Trend Example 2** (page 2, 10-day-old with projectile vomiting after feeding) is the exact
  source of `standalone_1784060000006`, built in batch 6. Every flow-sheet value and finding
  matches; no changes needed.
- **Bow-Tie Example 2** (pages 4–6, 79-year-old with facial drooping/hemiparesis/aphasia and
  an irregular pulse) is the exact source of `case_1789577787012`, already corrected in this
  session's earlier work (ischemic stroke with atrial fibrillation, not hypoglycemia). Every
  finding matches; no changes needed.

## Important note on this PDF's coloring

Both "Bow-Tie" example pages (page 3 and pages 4–6) render several "Potential Conditions" and
"Actions to Take" cells with the same light-blue background — including **2 condition cells
shaded per example**, which cannot both be the correct answer in a bowtie (exactly 1 condition
is correct). This is the same generic "draggable choice card" template styling that led to an
error earlier in this session on the Bowtie-Stroke item, and it is **not** an answer reveal.
Nothing in this PDF's coloring was used to pick an answer; every answer below is this session's
own clinical reasoning. (As a sanity check, the app's own bowtie player renders every
undragged choice card with the identical light-blue background regardless of correctness —
confirming this is just UI styling, not a signal.)

## The 2 new items

### Item A — Breastfed Infant Failure to Thrive (drag-word cloze / "dyad")

**Item ID:** `standalone_1790300000055`. Placement: Others (no maternal-newborn/pediatric-growth
unit exists in either course). A 2-month-old's weight trends steadily downward across 3 weekly
home-health visits (7 lb → 6 lb 9 oz → 6 lb 2 oz, a 12.5% total loss) despite frequent
breastfeeding on demand, with worsening lethargy.

**Answer:** fortify the breast milk **and** complete a feeding log.

**Reasoning:** breastfeeding on demand makes true intake hard to quantify, so a feeding log
gives objective tracking; fortifying the breast milk increases caloric density while
preserving breastfeeding, a smaller step than switching to formula outright (which hasn't been
tried yet) or referring for a gastrostomy tube (reserved for failure to thrive refractory to
less invasive measures). Increasing the *parent's* own caloric intake doesn't address the
infant's documented weight loss.

**Flag for clinician review:** "feed the client formula for 2 weeks" is a plausible alternative
if a program teaches formula supplementation as the first-line response to this degree of
weight loss/lethargy rather than fortifying breast milk first.

### Item B — Bowtie: Infected Gastrostomy Tube Site

**Item ID:** `standalone_1784060000007`. Placement: NURS 1021 Unit 6 (Gastrointestinal
Disorders). A 6-month-old with a gastrostomy tube (placed 2 weeks ago for failure to thrive)
presents with a leaking tube, erythematous/flaking skin and thick yellow drainage at the site,
a loose tube, fever, marked tachycardia (P 171), and early poor-perfusion signs (weak pulses,
cool extremities, capillary refill 3 seconds).

**Condition:** infection of the gastrostomy tube site (not refeeding syndrome — no electrolyte
findings support that; not normal findings or feeding intolerance — the site findings and
vitals are clearly abnormal).

**Actions:** request a wound consultation (specialized management of an infected, draining,
loose site) + request an IV 0.9% NS bolus (early perfusion compromise).

**Parameters:** skin integrity (tracks the infected site) + vital signs every 30 minutes
(tracks the systemic/hemodynamic compromise).

**Flag for clinician review:** "change the site dressing" is a reasonable action too (the
dressing is saturated); I prioritized wound consultation and the fluid bolus as the higher-acuity
pair, but reasonable practice could pick the dressing change instead.

## Verification performed this session

- Both items render in the real player (Supabase blocked), score full marks (1/1 and 5/5), and
  pass `itemProblems` (0 issues each) — the dyad item initially failed `itemProblems`
  ("drop-down without exactly one answer") because both dropdowns shared one options list with
  2 items marked correct; fixed by giving each dropdown its own list with exactly 1 correct
  option, while both still show the same 5 draggable words to the student.
- Editor open-and-save round-trip: empty diff for both items.
- Full `tools/check.js` (84 items, 214 screens): 0 failures, 4 known-incomplete items — same
  baseline as every prior batch, unaffected.
- Full `tools/check-saving.js`: 13/13 checks pass.
- **Not yet done:** clinician sign-off, and publishing. Everything stays on
  `claude/modest-galileo-5dtly1` — nothing pushed to `main` or Supabase.

## Running total

- **112 stand-alone questions** (6 + 19 + 27 + 27 + 14 + 17 + 2)
- **3 case studies** (2 new + 1 fixed existing — appendicitis)
- **1 existing item corrected** in addition to the case studies (the bowtie/ischemic-stroke
  item)
