# GI Bleed Case Study (H. pylori → PUD → Hemorrhage) — Source Notes

**Item ID:** `case_1786060000003` ("NURS 1021 Unit 6 Case Study 3"). Placement: NURS 1021 Unit 6
(Gastrointestinal Disorders). This is the user's own original content, not sourced from the
NCSBN exam preview — no NCSBN footnote was added. Only the Nurses' Notes tab (all 6 screens)
and Laboratory Tests tab (screens 4–6) are used, per your instruction — Health History, Vital
Signs, and Diagnostic Tests were not built.

## Scenario adjustment: veteran/VA → community hospital

Per your instruction, the client's profile was changed from a veteran seen at a VA medical
clinic to a client seen at a local community hospital, while keeping depression as part of the
psychosocial picture. The original backstory tied depression and homelessness specifically to
military discharge and PTSD; that framing is replaced with a non-military situational stressor
(job loss and a relationship breakdown) that leads to the same homelessness and follow-up
concern the clinical reasoning turns on — Item 1's rationale explicitly hinges on "this client
has been living in a car, and may not desire or be able to follow up," which holds regardless
of the reason for the housing instability. "VA clinic" became "community health clinic"
throughout; "Has PTSD and depression" became "Has depression" as a select-all option (still not
of immediate concern, same rationale logic).

## Note: a scoring correction caught before finalizing

Screen 3's stem has 3 dropdown blanks ("manage the client's [condition] as evidenced by
[finding 1] and [finding 2]"), but your screenshot shows **Score 2/2**, not 3/3. I initially
built all 3 blanks as independently scored (max 3) and caught the mismatch by comparing against
your screenshot's own displayed score. The correct reading: the condition blank and the first
evidence blank are a dyad pair (1 point only if both correct — the same "at risk for X as
evidenced by Y" pattern used throughout your prior case studies), and the second evidence blank
is scored independently (1 point). Fixed using the same `scoreGroups` mechanism added for your
integumentary case studies (`scoreGroups: [[0, 1]]`), giving the correct max of 2. Re-verified
against your screenshot's answered state and it now matches exactly.

## Verification performed this session

- All 6 screens render in the real player (Supabase blocked), score full marks — 3, 2, 2, 5, 5,
  6 — matching every score shown in your screenshots exactly, and pass `itemProblems` (0 issues
  each).
- Editor open-and-save round-trip: empty diff.
- Full `tools/check.js` (84 items, 214 screens): 0 failures, same 4-item known-incomplete
  baseline as every prior batch.
- Full `tools/check-saving.js`: 13/13 checks pass.
- **Not yet done:** clinician sign-off, and publishing. Stays on `claude/modest-galileo-5dtly1`
  — nothing pushed to `main` or Supabase.
