# NCSBN Exam Preview — 6 Stand-alone Items — Answer Key

Source: NCSBN NCLEX-RN® Next Generation NCLEX Exam Preview, ©2022 NCSBN
(https://www.nclex.com/prepare.page — "Download Exam Preview"). Stems and answer
options are transcribed verbatim from the source PDF. **The source PDF does not
publish an answer key** — it only demonstrates NGN item formats. The correct
answers, option ordering (shuffled where the source's first-listed option was
correct, per this app's authoring convention), and rationales below are this
session's clinical judgment, not a verified NCSBN key. **Every item in this set
should be reviewed by a clinician before publishing**, especially Item 3 (ECG
rhythm interpreted from a scanned strip graphic of uncertain calibration).

Every item carries a footnote crediting NCSBN and linking to the source, per the
user's request, visible on-screen directly under the client scenario.

Course/unit placement: items 1 and 2 (OB/labor, infection control) don't map to
an existing course/unit in `js/state.js`'s `CURRICULUM_COURSES`, so they are filed
under `course: "Others"` / `unit: "Others"` for now, per the user's instruction, to
be classified later. Items 3–6 map to existing NURS 1017/1021 units. Item 3 is the
first stand-alone item ever authored for NURS 1021 in this bank, so its ID uses a
new `1784<unit>0000<seq>` numbering root (parallel to the `1783<unit>0000<seq>`
root already used for NURS 1017 stand-alones); nothing else depends on this choice
and it can be renumbered freely before publish.

---

## Item 1 — Maternal-Newborn: Labor Stage Prioritization (MCQ)

**Draft file:** `standalone_1790300000001_Maternal_Newborn_Labor_Stage_Prioritization_MCQ.json`
**Placement:** course "Others" / unit "Others" *(no matching curriculum unit — OB content)*

*The charge nurse has received a change-of-shift report on the following clients in labor.*

**Question:** The charge nurse should ask a staff member to **first** see the client in the

1. ❌ first stage of labor who has an oral temperature of 99.7° F (37.6° C)
2. ✅ first stage of labor whose contractions are occurring every 30 seconds
3. ❌ second stage of labor who has respirations of 26
4. ❌ second stage of labor whose contractions are lasting for 60 seconds

**Rationale:** Contractions every 30 seconds (Option 2) indicate uterine
tachysystole — too little rest between contractions for adequate uteroplacental
perfusion, risking fetal hypoxia — so this client needs to be seen first. A mildly
elevated temperature of 99.7°F (Option 1) is not acutely concerning. An RR of 26
during active second-stage pushing (Option 3) is an expected exertional finding.
Contractions lasting 60 seconds in the second stage (Option 4) are within the
normal duration for that stage.

---

## Item 2 — Immune/Infection Control: Varicella Precautions (MCQ)

**Draft file:** `standalone_1790300000002_Immune_Infection_Control_Varicella_Precautions_MCQ.json`
**Placement:** course "Others" / unit "Others" *(no matching curriculum unit — general infection control)*

*The nurse is observing a staff member caring for a client who has chickenpox.*

**Question:** Which of the following actions by the staff member would require the nurse to intervene?

1. ❌ placing the client in a private room with monitored negative air pressure
2. ✅ placing a box of disposable face shields outside the client's room
3. ❌ placing an alcohol-based hand rub in the client's room for hand hygiene
4. ❌ placing a surgical mask on the client during transport out of the client's room

**Rationale:** Varicella requires **airborne** precautions. Face shields (Option 2)
are not adequate respiratory protection against airborne transmission — the
staff member needs a fit-tested N95 (or higher) respirator, so this action
requires intervention. Negative-pressure private room (Option 1), in-room
alcohol-based hand rub (Option 3), and a surgical mask on the *client* during
transport (Option 4, source control) are all correct practice.

---

## Item 3 — Symptomatic Bradycardia (ECG Rhythm, Select All That Apply) ⚠️ Flag for clinician review

**Draft file:** `standalone_1784020000001_Unit_2_Stand_alone_1_Symptomatic_Bradycardia_ECG_Rhythm_SATA.json`
**Placement:** NURS 1021 / Unit 2 (Cardiovascular Disorders)

*The nurse is caring for a client who reports feeling faint and is experiencing
the cardiac rhythm shown in the electrocardiogram (ECG) strip below* (cropped
from the source PDF and embedded in the item).

**Question:** Which of the following actions would be appropriate for the nurse to take? **Select all that apply.**

1. ❌ Administer the client's prescribed beta blocker.
2. ✅ Prepare for transcutaneous pacing.
3. ❌ Instruct the client to perform the Valsalva maneuver.
4. ❌ Begin chest compressions.
5. ✅ Assess the client for angina.

**Rationale:** The strip shows a regular, narrow-complex rhythm at a markedly
slow rate — read as symptomatic bradycardia, consistent with the client
"feeling faint." Prepare for pacing (Option 2) and assess for angina (Option 5,
slow rate → reduced coronary perfusion). A beta blocker (Option 1) and the
Valsalva maneuver (Option 3) both slow the heart rate further and are
contraindicated. Chest compressions (Option 4) aren't indicated — the client is
conscious and symptomatic, not pulseless.

**⚠️ Why this needs clinician review:** the source is a scanned clip-art-style
ECG strip on an uncalibrated grid, not a real telemetry printout. I read the
rate qualitatively (three widely-spaced narrow complexes, consistent P wave
before each QRS) rather than trusting a pixel-measured grid calibration, which
gave inconsistent results. A clinician should confirm the rhythm read (and
therefore the answer key) against the original PDF image before this item is
published.

---

## Item 4 — Alzheimer's Disease: Care Planning (MCQ)

**Draft file:** `standalone_1783070000001_Unit_7_Stand_alone_1_Alzheimers_Disease_Care_Planning.json`
**Placement:** NURS 1017 / Unit 7 (Neurological Disorders)

*The nurse is planning care for a client with moderate Alzheimer's disease (AD).*
Options reordered from the source (source listed the correct answer first) so
the correct answer isn't Option 1, per this app's content convention.

**Question:** Which of the following interventions should the nurse include in the client's plan of care?

1. ❌ Confront the client when inappropriate or agitated behaviors occur.
2. ❌ Provide the client with information about activity choices in the morning so the client can make plans for the day.
3. ✅ Encourage the client to reminisce about happy memories.
4. ❌ Administer to the client the cholinesterase inhibitor to reverse the course of AD.

**Rationale:** Reminiscence therapy (Option 3) is validating and appropriate — long-term
memories are typically preserved longer than short-term memory in moderate AD.
Confrontation (Option 1) escalates distress; redirection is preferred. Asking the
client to plan complex activity choices (Option 2) exceeds executive function
typically impaired at this stage. Cholinesterase inhibitors (Option 4) may
slow symptom progression for some clients but do **not** reverse or cure AD, so
this option's claim is factually wrong.

---

## Item 5 — Crutch-Walking Client Teaching (MCQ)

**Draft file:** `standalone_1783060000001_Unit_6_Stand_alone_1_Crutch_Walking_Client_Teaching.json`
**Placement:** NURS 1017 / Unit 6 (Musculoskeletal Disorders)

*The nurse is teaching a client how to ambulate using crutches.*
Options reordered from the source (source listed the correct answer first).

**Question:** Which of the following information should the nurse include?

1. ❌ "Wear slippers when ambulating with the crutches in your home."
2. ❌ "Maintain the crutches 12 in (30 cm) in front of your feet while standing."
3. ❌ "Adjust the hand grips of the crutches so that your elbows are fully extended."
4. ✅ "Use your hands and arms to support your body weight."

**Rationale:** Weight-bearing through the hands/arms (Option 4), not the axillae,
prevents axillary/radial nerve injury ("crutch palsy"). Slippers (Option 1) lack
traction and raise fall risk — sturdy non-skid shoes are correct. Crutch tips
12 in (30 cm) forward (Option 2) is too far forward (correct is ~6 in/15 cm,
to the side and slightly forward) and risks the crutches sliding out. Elbows
fully extended (Option 3) is wrong — elbows should be flexed ~15–30°.

---

## Item 6 — Multiple Sclerosis: Client Teaching Evaluation (MCQ)

**Draft file:** `standalone_1783070000002_Unit_7_Stand_alone_2_Multiple_Sclerosis_Client_Teaching_Evaluation.json`
**Placement:** NURS 1017 / Unit 7 (Neurological Disorders)

*The nurse has taught a client with multiple sclerosis (MS).*
Options reordered from the source (source listed the correct answer first).

**Question:** Which of the following statements by the client would indicate a correct understanding of the teaching?

1. ❌ "I have learned how to massage my bladder to help empty my bladder completely."
2. ❌ "I will take a hot bath in the evening to help me relax if I have had a stressful day at work."
3. ❌ "I should expect the blurred vision to resolve after I have received medications for several weeks."
4. ✅ "I will complete all of my household chores in the morning when I am well rested."

**Rationale:** Doing tasks in the morning when best rested (Option 4) reflects
correct energy-conservation teaching — MS fatigue worsens through the day.
Bladder massage (Option 1) isn't standard MS bladder-management teaching
(self-catheterization or similar is used instead). A hot evening bath (Option 2)
is contraindicated — heat can transiently worsen MS symptoms (Uhthoff
phenomenon). Promising resolution of blurred vision after "several weeks of
medication" (Option 3) overstates what treatment guarantees in a chronic,
relapsing disease.

---

## Verification performed this session

- All 6 items rendered in the real player (Supabase blocked), scored full marks
  against the answer keys above, and produced zero page errors.
- All 6 items pass `itemProblems` (the readiness rule) — none are flagged incomplete.
- Screenshots of each item's question and answered/rationale state are in
  `NCSBN_Preview_Standalone_Walkthrough.pdf` (question page, then answered page,
  per item, in the order above).
- **Not yet done:** clinician sign-off on medical accuracy (all 6 items, per
  CLAUDE.md), and confirmation of the ECG rhythm read (Item 3) specifically.
- **Not yet done:** publishing. These are drafts only — not visible to students
  until published via the Supabase workflow (`action: add`) after you approve them.
