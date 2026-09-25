# DVT → Pulmonary Embolism Case Study — Source Notes

**Item ID:** `case_1786010000001` ("NURS 1021 Unit 1 Case Study 1"). Placement: NURS 1021 Unit 1
(Blood Disorders) — a coagulation/anticoagulation-focused case fits this unit better than
Cardiovascular. This is the user's own original content from an earlier version of this app,
not sourced from the NCSBN exam preview — no NCSBN copyright footnote was added. Only the
Nurses' Notes tab is used, per the user's instruction (the Health History / Physician's Orders
/ Diagnostic Tests tabs visible in the source screenshots were not built).

## The screen 5 fix

In the source, screen 5 read as a standalone paragraph that re-introduced the client from
scratch ("a 71-year-old client who was admitted to the medical unit yesterday morning for right
leg DVT... the client is receiving continuous IV heparin") before describing new findings —
structurally disconnected from the Nurses' Notes tab used on every other screen, making it read
like a new patient encounter. Fixed by moving the clinical findings into the same accumulating
Nurses' Notes tab as a new dated entry ("Day 2, 0700") and trimming the screen's preamble to a
short framing line matching the style of every other screen, instead of a paragraph that
restates the client's demographics and diagnosis.

## Screen-by-screen summary

1. **Recognize Cues** (select_all, 10 options/4 correct) — ED presentation: painful, red, warm,
   swollen right leg with inability to ambulate, plus elevated BP, are immediate concerns; a
   diminished-but-present pedal pulse, well-managed diabetes/hypercholesterolemia, prior DVT
   history, normal SpO2 and glucose are not.
2. **Analyze Cues** (matrix_mr, 6 findings × DVT/PAD) — pain supports both; redness/warmth/
   swelling point to DVT; cool feet, diminished pulses, and the diabetes history point to PAD.
3. **Prioritize Hypotheses** (dropdown_cloze, 1 blank) — priority monitoring for a client on
   continuous heparin is hemorrhage.
4. **Generate Solutions** (select_all, 5 options/4 correct) — appropriate teaching: occult
   blood testing, an eventual switch to an LMWH, the DVT-history rationale for IV heparin, and
   reporting chest discomfort/dyspnea; INR monitoring is a distractor (that's for warfarin, not
   heparin — aPTT is the correct heparin-monitoring lab).
5. **Take Action** (select_all, 11 options grouped by body system/8 correct) — a submassive PE
   response: continuous pulse ox, O2, elevated HOB (not incentive spirometry or only-every-shift
   lung assessment); IV crystalloid, hourly vitals, CT chest (all 3 cardiovascular actions);
   monitor LOC and reassure the client (not routine q4h neuro checks).
6. **Evaluate Outcomes** (matrix_mc, 6 findings compared 2-days-ago → today) — chest discomfort,
   shortness of breath, HR, BP, and SpO2 have all improved; the client's anxiety has not.

## Flagged for clinician review

Screen 5's "Initiate continuous pulse oximetry monitoring" option was not explicitly confirmed
correct or incorrect in the user's rationale text (which explicitly addresses oxygen therapy,
incentive spirometry, and the every-shift-lung-assessment items, but not this one by name). I
included it as correct, reasoning it as a direct extension of "immediately start oxygen
therapy" for a client with a new, clinically significant desaturation (SpO2 90%) — this is
flagged in the item's own explanation text as well.

## Verification performed this session

- All 6 screens render in the real player (Supabase blocked), score full marks against the
  answer keys above, and pass `itemProblems` (0 issues).
- Editor open-and-save round-trip: empty diff.
- Full `tools/check.js` (84 items, 214 screens): 0 failures, 4 known-incomplete items — same
  baseline as every prior batch, unaffected.
- Full `tools/check-saving.js`: 13/13 checks pass.
- **Not yet done:** clinician sign-off, and publishing. Stays on `claude/modest-galileo-5dtly1`
  — nothing pushed to `main` or Supabase.
