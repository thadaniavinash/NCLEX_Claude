# NURS 1021 Unit 6 Case Study 1 (appendicitis) — Fix Notes & Answer Key

**Item ID:** `case_1781741217820` (already published, currently titled "NCSBN - Case Study 1"
under course/unit "Others"/"Others"). This is a **fix to an existing item**, not a new one.
Draft of the fixed item: `drafts/case_1781741217820_FIXED_NURS_1021_Unit_6_Case_Study_1.json`
(built by `drafts/fix_ncsbn_case_study_1.py`). **Nothing has been written to the live database
yet** — see "How to publish this" at the end.

Source: NCSBN NCLEX-RN® Next Generation NCLEX Exam Preview, ©2022 NCSBN
(https://www.nclex.com/prepare.page — "Download Exam Preview"), the Case Study 1 excerpt you
attached (11 pages, all 6 screens, with 2 screens' answer keys visible as revealed selections —
the highlight screen and the dropdown screen — since NCSBN's screenshots show them mid-interaction).

## What changed vs. the existing published item

1. **Screen 1 highlight answer key corrected.** The official PDF's highlighted screenshot shows
   the *entire* vital-signs sentence highlighted as one finding — "Vital signs: T 103.4°F
   (39.7°C), P 92, RR 22, BP 130/86, pulse oximetry reading 98% on room air." — not just the
   temperature/pulse/RR/BP portion. The existing item had "pulse oximetry reading 98% on room
   air" marked as an **incorrect** distractor. I verified this by cropping and zooming the source
   PDF's page 8 at 400 DPI; the highlight unambiguously runs through the whole sentence.
2. **Two typos fixed:** "soadsuds enema" → "soapsuds enema", "computed tomograph" → "computed
   tomography" (screen 4).
3. **Copyright footnote added** to all 6 screens (the same `question.footnote`, shown below the
   Submit button, added to the 6 stand-alone items earlier).
4. **Moved into a real course/unit:** NURS 1021 / Unit 6 (Gastrointestinal Disorders) — the first
   case study in that unit — instead of "Others"/"Others". Title renamed to
   **"NURS 1021 Unit 6 Case Study 1"** to match the naming convention used elsewhere in the bank
   (e.g. "NURS 1017 Unit 3 Case Study 4"). If you'd rather keep the old title or a different
   unit, easy to change before publishing.
5. **Rationales merged/enriched** on all 6 screens — kept the substance of each existing
   explanation and expanded it to address every option/row/blank explicitly.
6. Stray literal tab characters (copy-paste artifacts throughout the existing item's stems,
   preambles, and tab content) normalized to spaces.

## Bonus finding: a real editor bug, now fixed

Opening this item in the authoring editor and saving — with **no edits at all** — was silently
**wiping the row labels "clear liquid diet" and "soapsuds enema" to blank** on screen 4. Cause:
`js/editor.js` had a hardcoded list of "generic placeholder" row labels (`clear liquid diet`,
`soapsuds enema`, `polyuria`, `weight gain`, `New Row 1`, `New Row 2`) that it scrubs back to
empty wherever it finds them — meant to clear out template scaffolding text, but it can't tell
scaffolding apart from a real answer that happens to match. The old item's typo ("soadsuds")
accidentally protected it from this; fixing the spelling would have walked straight into the bug.
Fixed by removing those two specific strings from the blocklist in `js/editor.js` (3 occurrences).
Verified: full `check.js`/`check-saving.js` suite still passes (0 failures, 4 known-incomplete
items, 13/13 saving checks), and this item's editor open-and-save round-trip is now a clean
empty diff.

## Screen-by-screen

### Screen 1 — Recognize Cues (highlight)
*The nurse in the emergency department (ED) is caring for a 41-year-old male client.*
"Click to highlight the findings below that would require follow-up."

Correct (highlighted): **loss of appetite,** · **abdominal pain rated 7/10 ... "kicked me in the
stomach."** · **the full vital signs sentence** (T 103.4°F, P 92, RR 22, BP 130/86, SpO₂ 98%).
Not correct: nausea (alone) · vomiting/fever/constipation (narrative) · soccer once a week · no
significant PMH/PSH · BMI 32 · alcohol/cigarette use.

### Screen 2 — Analyze Cues (matrix, multiple response)
Bowel Obstruction / Appendicitis / Ruptured Spleen — unchanged from the existing item (not
revealed in the new PDF, but internally consistent and already cross-verified elsewhere):
- appetite → Bowel Obstruction, Appendicitis
- pain level → all 3
- bowel pattern → Bowel Obstruction, Appendicitis
- GI symptoms → Bowel Obstruction, Appendicitis

### Screen 3 — Prioritize Hypotheses (select 3)
Correct: **peritonitis, septic shock, hypovolemia**. Not selected: anemia, dysrhythmias, cardiac
arrest (unchanged from the existing item).

### Screen 4 — Generate Solutions (matrix, indicated/not indicated)
Indicated: **abdominal CT scan**. Not indicated: clear liquid diet, soapsuds enema, heating pad
to abdomen, abdominal girth measurements (unchanged from the existing item; typos fixed).

### Screen 5 — Take Action (dropdown cloze)
"The nurse should insert **a nasogastric (NG) tube**. It would be a priority for the nurse to
request a prescription for an **anti-infective medication**. The nurse should prepare the client
for surgery within **6 hours**." — confirmed exactly against the new PDF's revealed dropdown
selections (screens 12–16 of the source PDF).

### Screen 6 — Evaluate Outcomes (select all)
Correct: **incentive spirometry use, performance of leg exercises**. Not correct: clear liquid
diet, board-like abdomen, rebound tenderness, diminished bowel sounds (unchanged from the
existing item).

## Verification performed this session
- All 6 screens render in the real player (Supabase blocked), score full marks against the
  answer key above, and pass `itemProblems` (0 issues).
- Editor open-and-save round-trip: **empty diff** (after the `editor.js` fix).
- Full `tools/check.js` (84 items, 214 screens): 0 failures, 4 known-incomplete items (same
  baseline as before this change — the 2 unrelated pre-existing editor-diff items are unrelated
  to this fix).
- Full `tools/check-saving.js`: 13/13 checks pass.
- **Not yet done:** clinician sign-off on medical accuracy, and the actual publish to the live
  database (see below).

## How to publish this fix

This item is **already live** (in the database, not just a draft), so publishing works
differently from the 6 new stand-alone questions:
- `add` can't be used — it explicitly refuses if the ID already exists.
- Fixing it needs `download` (pull the current live database into `cases-data.js` to make sure
  nothing changed since this draft was built) → replace this one item in `cases-data.js` →
  `upload` (which reads the whole `cases-data.js` and verifies the database matches afterward)
  → `download` again to resync the backup.

I've held off on triggering any of this until you review the walkthrough and confirm you're
happy with the fix (course/unit placement, title, and the merged rationales especially — those
are the most subjective part of this change).
