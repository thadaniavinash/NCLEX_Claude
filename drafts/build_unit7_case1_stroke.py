"""Builds NURS 1017 Unit 7 Case Study 1 (acute ischemic stroke, symptomatic hemorrhage during alteplase) as app-ready JSON.

Source: the user's own case "Unfolding NGN Case Study: Acute Ischemic Stroke" (PDF, 2 Nov 2026), converted with the
corrections the user approved the same day ("approve all"):
A1 Item 6 CT finding is a PH1 parenchymal hematoma (not HI1) managed in the neuro ICU; the update is Day 7 on the stroke unit.
A2 weight 82 kg in the H&P; alteplase order written out (74 mg: 7.4 mg bolus, 66.6 mg over 60 minutes).
A3 CT angiography (left M1 occlusion) in the Diagnostic Results; thrombectomy referral in the orders and rationale.
A4 last known well = witnessed onset 0800; window "4.5 hours from last known well".
A5 the 0915 vital signs are part of the highlight passage; BP 198/108 mm Hg is a correct phrase.
A6 right leg strength 4/5 (drifts, does not touch the bed within 5 seconds).
A7 invasive-line rationale softened (delay if safely possible; many protocols 24 hours); tenecteplase noted.
A8 SLP assessment (dysphagia, mildly thick liquids) in the Day 7 notes.
B1 Item 2 stem rewritten, "reversible with dextrose" removed; B3 Item 6 row 3 done by the spouse;
B4 "type and crossmatch" in option and rationale; B5 extra Item 4 row (neuro checks every 15 minutes).
C  SI units only, "mm Hg", "beats/min", "° C"; no "cues"; "client"; chart tabs only grow; random answer order.
Item 2 also gained a sixth row (declining LOC with a unilateral dilated pupil -> increased ICP) as a set-up for Item 5.
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unit6_common import (Chart, vs, lab, opts, dropdown, matrix_mc, rationale, highlight_tab, screen, HERE)  # noqa: E402

ID = "case_1782410000001"
TITLE = "NURS 1017 Unit 7 Case Study 1"
UNIT = "Unit 7 (Neurological Disorders)"
INTRO = ("The nurse in the emergency department is caring for a 68-year-old male client who arrived by ambulance with sudden "
         "difficulty speaking.")


class StrokeChart(Chart):
    def html(self, tid, title, content):
        """A free-text tab (History & Physical): content is fixed HTML, added once."""
        t = self._tab(tid, title, "html")
        t["content"] = content

    def snapshot(self):
        out = super().snapshot() if all(self.tabs[t]["kind"] != "html" for t in self.order) else None
        if out is not None:
            return out
        saved = {t: self.tabs[t] for t in self.order if self.tabs[t]["kind"] == "html"}
        for t in saved:
            self.tabs[t] = dict(saved[t], kind="notes", entries=[])
        out = super().snapshot()
        for t, tab in saved.items():
            self.tabs[t] = tab
            for o in out:
                if o["id"] == t:
                    o["content"] = tab["content"]
        return out


C = StrokeChart()

# ---------------------------------------------------------------- Screen 1 (recognize): highlight
S1_NOTES = [
    ("0915", "Arrived in the emergency department by ambulance with his wife. Wife states he {went to bed feeling fine at 2200 last night}. "
     "He {woke up at 0730 at his usual baseline and was eating breakfast with her at 0800 when he suddenly dropped his coffee mug and "
     "could not get his words out clearly|correct}."),
    ("0920", "Rapid neurological assessment started. Client is awake and appears frustrated when trying to speak. {Speech is halting, "
     "effortful, and non-fluent, though he follows 1-step commands|correct} (“squeeze my hand,” “close your eyes”). {Flattening of the "
     "right nasolabial fold with an asymmetrical smile|correct}. {Right upper extremity (RUE) drifts down to the bed within 3 seconds when "
     "held extended; right lower extremity (RLE) drifts but does not touch the bed within 5 seconds (strength 4/5)|correct}. {Left upper and "
     "lower extremities have full strength (5/5)}. {Cough is weak when clearing his throat}. National Institutes of Health Stroke Scale "
     "(NIHSS) score 11. Code Stroke activated."),
]
HP_MARKED = [
    ("Medical history", "Hypertension (diagnosed 12 years ago), paroxysmal atrial fibrillation, hyperlipidemia, type 2 diabetes mellitus, "
     "{gastroesophageal reflux disease (GERD)}."),
    ("Surgical history", "{Laparoscopic cholecystectomy 8 years ago}."),
    ("Social history", "{Retired accountant}; lives with his wife; former smoker (quit 10 years ago)."),
    ("Weight", "82 kg."),
    ("Home medications", "Lisinopril 20 mg PO daily, metoprolol succinate 50 mg PO daily, atorvastatin 40 mg PO daily, metformin 1,000 mg PO "
     "BID, pantoprazole 40 mg PO daily. Wife reports he {stopped taking his prescribed apixaban 3 months ago because of out-of-pocket "
     "costs|correct}."),
]
VS_MARKED = [("0915", "{T 37.1° C}, {P 114 beats/min, irregularly irregular|correct}, {RR 18 breaths/min, even and unlabored}, "
              "{BP 198/108 mm Hg|correct}, {SpO₂ 96% on room air}.")]


def hp_html(entries):
    from unit6_common import strip_marks
    return "".join(f"<p><b>{k}:</b> {strip_marks(v)}</p>" for k, v in entries)


def hp_marked_html(entries):
    return "".join(f"<p><b>{k}:</b> {v}</p>" for k, v in entries)


C.notes("nn", "Nurses' Notes", *S1_NOTES)
C.html("hp", "History and Physical", hp_html(HP_MARKED))
C.vitals("0915", vs("37.1° C", "114 beats/min, irregularly irregular", "18 breaths/min", "198/108 mm Hg", "96% on room air"))

s1 = screen(1, INTRO, C, {
    "type": "highlight",
    "stem": "The nurse reviews the Nurses' Notes, the History and Physical, and the Vital Signs. <b>Highlight</b> the findings that are "
            "directly relevant to identifying the client's acute condition and his eligibility for time-sensitive reperfusion therapy.",
    "options": [],
    "highlightTabs": [
        highlight_tab("ht1", "Nurses' Notes", S1_NOTES),
        {"id": "ht2", "title": "History and Physical", "content": hp_marked_html(HP_MARKED)},
        highlight_tab("ht3", "Vital Signs", VS_MARKED),
    ],
    "maxCorrectSelections": None,
    "explanation": rationale(
        "<b>Relevant findings:</b>",
        "<b>Time of onset:</b> his wife saw him at his usual baseline until the sudden onset at 0800, so his <b>last known well is 0800</b> "
        "(not bedtime at 2200, which would apply only if he had woken up with the deficits). Intravenous thrombolysis (alteplase or "
        "tenecteplase) can be considered up to <b>4.5 hours from last known well</b>, so the exact time is the most important piece of "
        "history.",
        "<b>Non-fluent (Broca's) aphasia with intact comprehension, right facial droop, and right-sided weakness (arm weaker than leg):</b> "
        "a sudden focal deficit that localizes to the dominant (left) hemisphere, in the territory of the left middle cerebral artery (MCA). "
        "The MCA supplies the face and arm more than the leg.",
        "<b>Irregularly irregular pulse and apixaban stopped 3 months ago:</b> untreated atrial fibrillation lets thrombus form in the left "
        "atrial appendage and embolize to the brain (cardioembolic stroke). It also means he has taken no direct oral anticoagulant in the "
        "last 48 hours, which would otherwise be a contraindication to thrombolysis.",
        "<b>BP 198/108 mm Hg:</b> blood pressure must be below 185/110 mm Hg before thrombolysis can start, so it must be treated first.",
        "<b>Not directly relevant now:</b> bedtime at 2200, full strength on the left side, GERD, the cholecystectomy, his former occupation, "
        "the temperature, RR and SpO₂. The weak cough matters for aspiration risk and the swallowing screen, but it does not identify the "
        "acute condition or decide reperfusion eligibility."),
})

# ---------------------------------------------------------------- Screen 2 (analyze): matrix multiple choice
s2 = screen(2, INTRO, C, {
    "type": "matrix_mc",
    "stem": "The nurse considers conditions that could explain sudden neurological changes. For each finding, click to specify the condition "
            "that the finding is most consistent with. Each row has one answer.",
    "matrix": matrix_mc("Finding", ["Left hemisphere ischemic stroke", "Hypoglycemia", "Increased intracranial pressure (ICP)"], [
        ("Expressive (non-fluent) aphasia", 0),
        ("Diaphoresis, tremor, and hunger", 1),
        ("Right-sided weakness and facial droop", 0),
        ("Cushing's triad (bradycardia, widened pulse pressure, irregular respirations)", 2),
        ("Irregularly irregular pulse of 114 beats/min", 0),
        ("Declining level of consciousness with one dilated, sluggish pupil", 2),
    ]),
    "explanation": rationale(
        "<b>Left hemisphere ischemic stroke:</b> Broca's area lies in the left frontal lobe in most people, so ischemia there causes "
        "<b>expressive aphasia</b> while comprehension stays largely intact. The motor tracts cross in the medulla, so a left hemisphere "
        "lesion causes <b>right-sided weakness and facial droop</b>. An <b>irregularly irregular pulse</b> suggests atrial fibrillation, a "
        "leading cause of cardioembolic ischemic stroke.",
        "<b>Hypoglycemia:</b> diaphoresis, tremor and hunger are adrenergic (sympathetic) responses to low blood glucose. Hypoglycemia is a "
        "well-known stroke mimic and can even cause focal weakness or speech changes, which is why a point-of-care glucose is checked before "
        "imaging or thrombolysis.",
        "<b>Increased ICP:</b> Cushing's triad is a late sign of severely raised ICP with brainstem compression. A falling level of "
        "consciousness with one dilated, sluggish pupil (pressure on the oculomotor nerve, cranial nerve III) signals herniation. Neither is "
        "a typical early finding of an uncomplicated ischemic stroke; both must be reported immediately."),
})

# ---------------------------------------------------------------- Screen 3 (prioritize): drop-down cloze
C.vitals("0935", vs("", "110 beats/min, irregular", "18 breaths/min", "196/106 mm Hg", "95% on room air"))
C.notes("dx", "Diagnostic Results",
    ("0930", "<b>12-lead ECG:</b> atrial fibrillation with a rapid ventricular response, rate 112 beats/min. No acute ST-segment elevation."),
    ("0932", "<b>Non-contrast head CT:</b> no acute intracranial hemorrhage or mass effect. Early loss of gray-white matter differentiation "
     "in the left insular ribbon, consistent with acute ischemia in the left middle cerebral artery (MCA) territory."),
    ("0934", "<b>CT angiography, head and neck:</b> occlusion of the proximal left MCA (M1 segment)."))
C.labs("0935", [
    (lab("Glucose, random (point-of-care)", "4.0–11.0 mmol/L"), "7.7 mmol/L"),
    (lab("Platelet count", "130–380 × 10<sup>9</sup>/L"), "245 × 10<sup>9</sup>/L"),
    (lab("International normalized ratio (INR)", "0.9–1.2"), "1.0"),
    (lab("Creatinine", "Male: 49–93 µmol/L"), "84 µmol/L"),
])
s3 = screen(3, INTRO, C, {
    "type": "dropdown_cloze",
    "preamble": "The nurse has reviewed the Vital Signs from 0935, the Diagnostic Results and the Laboratory Results.",
    "stem": "Complete the following sentence by choosing from the lists of options.",
    "cloze": {
        "text": "The client's highest priority problem is [[drop0]] secondary to [[drop1]], which places the client at immediate risk for "
                "[[drop2]] if his blood pressure is not reduced before fibrinolytic therapy.",
        "dropdowns": [
            dropdown(("impaired verbal communication", False), ("ineffective cerebral tissue perfusion", True),
                     ("risk for unilateral neglect", False), ("acute confusion", False), seed="u7c1-d0"),
            dropdown(("left middle cerebral artery thromboembolism", True), ("a ruptured cerebral aneurysm", False),
                     ("hypertensive encephalopathy", False), ("carotid artery dissection", False), seed="u7c1-d1"),
            dropdown(("neurogenic shock", False), ("intracerebral hemorrhage", True),
                     ("watershed infarction", False), ("autonomic dysreflexia", False), seed="u7c1-d2"),
        ],
    },
    "explanation": rationale(
        "<b>Ineffective cerebral tissue perfusion:</b> the priority is to restore blood flow to the <b>ischemic penumbra</b>, the reversibly "
        "injured brain tissue around the infarct core, before it dies. Impaired verbal communication is real but is a consequence of the "
        "ischemia, not the priority.",
        "<b>Left MCA thromboembolism:</b> the non-contrast CT rules out hemorrhage and shows early left MCA ischemia, and the CT angiogram shows "
        "the clot in the left M1 segment. With untreated atrial fibrillation, the clot most likely came from the heart. A ruptured aneurysm "
        "would show blood on CT; there is no sign of hypertensive encephalopathy or dissection.",
        "<b>Intracerebral hemorrhage:</b> he is within 4.5 hours of last known well (0800) and has no contraindication on the laboratory "
        "results (glucose 7.7 mmol/L, platelets 245 × 10⁹/L, INR 1.0). His BP of 196/106 mm Hg must be lowered below 185/110 mm Hg before "
        "the fibrinolytic is started, because a high BP greatly increases the risk of hemorrhagic transformation. Lowering it too far or too "
        "fast could instead cause watershed infarction; neurogenic shock and autonomic dysreflexia are complications of spinal cord injury.",
        "<b>Large-vessel occlusion:</b> because the CT angiogram shows a proximal MCA occlusion, the client is also a candidate for "
        "endovascular thrombectomy, which is offered in addition to thrombolysis."),
})

# ---------------------------------------------------------------- Screen 4 (generate solutions): matrix indicated / contraindicated
C.notes("ord", "Provider Orders",
    ("0940", "Client is a candidate for IV thrombolysis.<br>"
     "Alteplase 0.9 mg/kg IV (weight 82 kg): total dose 74 mg. Give 7.4 mg (10%) IV bolus over 1 minute, then 66.6 mg (90%) by infusion "
     "over 60 minutes.<br>"
     "Neurointerventional team consulted for endovascular thrombectomy."))
s4 = screen(4, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Provider Orders.",
    "stem": "The nurse plans care for the client before and during the alteplase infusion. For each intervention, click to specify whether "
            "it is <b>indicated</b> or <b>contraindicated</b>.",
    "matrix": matrix_mc("Intervention", ["Indicated", "Contraindicated"], [
        ("Insert an indwelling urinary catheter and a nasogastric tube 15 minutes after the alteplase bolus", 1),
        ("Administer prescribed IV labetalol to lower the BP below 185/110 mm Hg before starting alteplase", 0),
        ("Keep the client NPO until a bedside swallowing screen is passed", 0),
        ("Administer aspirin 325 mg with the alteplase infusion to prevent reocclusion", 1),
        ("Assess neurological status and vital signs every 15 minutes during the infusion and for 2 hours after it", 0),
        ("Insert two peripheral IV lines before starting the alteplase", 0),
    ]),
    "explanation": rationale(
        "<b>Indicated:</b>",
        "<b>Lower the BP first:</b> stroke guidelines (AHA/ASA and Canadian Stroke Best Practice Recommendations) require a BP below "
        "185/110 mm Hg before an IV fibrinolytic is given (labetalol, nicardipine or clevidipine), then below 180/105 mm Hg for 24 hours "
        "after it. (In Canada, tenecteplase 0.25 mg/kg as a single bolus is an accepted alternative to alteplase; the BP limits are the same.)",
        "<b>NPO until the swallowing screen:</b> dysphagia is common after stroke (this client has a weak cough), and aspiration pneumonia is "
        "a leading complication. Nothing is given by mouth, including medications, until a validated screen is passed.",
        "<b>Neurological checks and vital signs every 15 minutes</b> during the infusion and for 2 hours after it (then every 30 minutes for "
        "6 hours and every hour until 24 hours) detect bleeding, angioedema and BP above the limit early. A new headache, nausea, vomiting, "
        "a drop in level of consciousness or worsening weakness means stopping the infusion and calling the provider.",
        "<b>Two peripheral IV lines before the infusion:</b> needle sticks are done before thrombolysis, and a separate line lets "
        "antihypertensives or fluids run without interrupting the alteplase.",
        "<b>Contraindicated:</b>",
        "<b>Urinary catheter and nasogastric tube after the bolus:</b> invasive procedures during and after thrombolysis can cause bleeding "
        "that cannot be compressed. Guidelines say to delay them if the client can be safely managed without them (many protocols: for 24 "
        "hours); if one is truly needed, it is placed before the infusion starts.",
        "<b>Aspirin with alteplase:</b> antiplatelet agents and anticoagulants (aspirin, clopidogrel, heparin) are withheld for 24 hours "
        "after IV thrombolysis, until a follow-up CT shows no hemorrhage, because they greatly increase the risk of bleeding."),
})

# ---------------------------------------------------------------- Screen 5 (take action): select all
C.notes("nn", "Nurses' Notes",
    ("0950", "BP 176/98 mm Hg after labetalol 10 mg IV at 0945. Alteplase 7.4 mg IV bolus given at 0952, followed by the 60-minute "
     "infusion on a dedicated line. Neurological checks and vital signs every 15 minutes."),
    ("1015", "23 minutes into the infusion, the client suddenly becomes restless, groans, and clutches the left side of his head with his "
     "left hand. Does not open his eyes to voice; opens them to painful stimuli, localizes to painful stimuli, and makes incomprehensible "
     "sounds (Glasgow Coma Scale 9, was 14). Vomited 150 mL of clear fluid. Left pupil 6 mm and sluggish to light; right pupil 3 mm and "
     "brisk. Respirations irregular."))
C.vitals("1015", vs("", "56 beats/min, irregular", "12 breaths/min, irregular", "218/116 mm Hg", "93% on room air"))
s5 = screen(5, INTRO, C, {
    "type": "select_all",
    "preamble": "The nurse has reviewed the Nurses' Notes from 0950 and 1015 and the Vital Signs from 1015.",
    "stem": "Which actions should the nurse take <b>immediately</b>? <b>Select all that apply.</b>",
    "options": opts(
        ("Stop the alteplase infusion", True),
        ("Position the client supine with the head of the bed flat to maximize cerebral perfusion", False),
        ("Elevate the head of the bed to 30 degrees with the head and neck in a neutral, midline position", True),
        ("Prepare the client for an emergency non-contrast head CT", True),
        ("Notify the stroke team and anticipate orders for cryoprecipitate or tranexamic acid", True),
        ("Administer a bolus of 5% dextrose in water (D5W) IV to treat cerebral edema", False),
        ("Draw STAT blood work: CBC, fibrinogen, PT/INR, aPTT, and type and crossmatch", True),
        seed="u7c1-s5"),
    "explanation": rationale(
        "A sudden severe headache, vomiting, a drop in Glasgow Coma Scale score from 14 to 9, a dilated, sluggish left pupil, and Cushing's "
        "triad (BP 218/116 mm Hg with a widened pulse pressure, heart rate 56 beats/min, irregular respirations) during an alteplase infusion "
        "are the classic picture of <b>symptomatic intracerebral hemorrhage</b> (hemorrhagic transformation) with rising ICP and signs of "
        "herniation on the side of the stroke.",
        "<b>Stop the alteplase infusion:</b> the first action, to stop further fibrinolysis.",
        "<b>Head of the bed at 30 degrees, head and neck midline:</b> promotes venous drainage through the jugular veins, lowers ICP, and "
        "reduces aspiration risk while he is vomiting. Lying flat raises ICP and aspiration risk, so it is incorrect here.",
        "<b>Emergency non-contrast head CT, stroke team, STAT blood work:</b> suspected hemorrhage after thrombolysis needs immediate "
        "provider notification, a CT to confirm it, and a CBC, fibrinogen level, coagulation studies, and type and crossmatch. Reversal "
        "usually includes cryoprecipitate (10 units, to replace fibrinogen) or an antifibrinolytic (tranexamic acid or aminocaproic acid).",
        "<b>D5W is incorrect:</b> once the glucose is metabolized, D5W acts as free water (hypotonic). Free water moves into the brain and "
        "worsens cerebral edema and ICP. Isotonic 0.9% sodium chloride is used after brain injury."),
})

# ---------------------------------------------------------------- Screen 6 (evaluate outcomes): matrix effective / ineffective
C.notes("dx", "Diagnostic Results",
    ("1025", "<b>Repeat non-contrast head CT:</b> parenchymal hematoma (PH1) within the left MCA infarct, with surrounding edema and mild mass "
     "effect. No intraventricular extension."))
C.notes("nn", "Nurses' Notes",
    ("1030", "Alteplase stopped at 1016 (about 40 mg given). Cryoprecipitate 10 units and tranexamic acid 1 g IV given. Hypertonic saline "
     "and an IV antihypertensive infusion started as prescribed. Thrombectomy cancelled. Transferred to the neurological intensive care unit."),
    ("Day 7 0800", "Transferred from the neurological ICU to the stroke unit on Day 5. Neurologically stable for 72 hours; alert, follows "
     "commands. Residual right-sided weakness (right arm 3/5, right leg 4/5), right homonymous hemianopsia, and expressive aphasia that is "
     "slowly improving. Speech-language pathology swallowing assessment (Day 6): oropharyngeal dysphagia; soft diet with mildly thick "
     "liquids. Wife at the bedside, eager to help with his care. Rehabilitation plan of care in progress."))
C.vitals("Day 7 0800", vs("36.9° C", "78 beats/min, irregular", "16 breaths/min", "146/84 mm Hg", "96% on room air"))
s6 = screen(6, INTRO, C, {
    "type": "matrix_mc",
    "preamble": "The nurse has reviewed the Diagnostic Results from 1025, the Nurses' Notes from 1030 and Day 7 0800, and the Vital Signs "
                "from Day 7 0800.",
    "stem": "The nurse observes the unlicensed assistive personnel (UAP) and the client's wife caring for the client. For each action, "
            "click to specify whether it is <b>effective</b> or <b>ineffective</b> in carrying out the plan of care.",
    "matrix": matrix_mc("Observed Action", ["Effective", "Ineffective"], [
        ("The wife approaches the client from his left side and places the call light and his personal items within reach of his left hand", 0),
        ("The UAP offers the client thin liquids through a straw to help him swallow more easily", 1),
        ("The wife asks the client yes/no questions, gives him extra time to respond, and uses a picture communication board", 0),
        ("The UAP helps the client from the bed to the chair by pulling upward under his right arm and axilla", 1),
        ("During meals, the client sits upright at 90 degrees and the UAP reminds him to turn his head to the right to scan his whole tray", 0),
    ]),
    "explanation": rationale(
        "<b>Effective:</b>",
        "<b>Approaching from the left, call light at the left hand:</b> with a right homonymous hemianopsia and right-sided weakness, "
        "approaching from the intact (left) side avoids startling him, and he can see and reach the call light with his stronger hand.",
        "<b>Yes/no questions, extra time, picture board:</b> in expressive (Broca's) aphasia, comprehension is relatively preserved but "
        "speech production is impaired. Simple questions, not rushing or finishing his sentences, and a communication board reduce "
        "frustration.",
        "<b>Upright at 90 degrees, turning the head to the right to scan the tray:</b> sitting upright lowers aspiration risk, and teaching "
        "the client to turn his head toward the blind field (visual scanning) compensates for the hemianopsia so he sees all his food.",
        "<b>Ineffective:</b>",
        "<b>Thin liquids through a straw:</b> the swallowing assessment prescribed mildly thick liquids, because thin liquids are the easiest "
        "to aspirate. Straws send liquid quickly to the back of the throat before the swallow is triggered, which further raises the risk of "
        "aspiration.",
        "<b>Pulling under the weak arm:</b> pulling on a weak or flaccid arm can cause shoulder (glenohumeral) subluxation and brachial plexus "
        "injury. A gait belt is used, and the weak arm is supported (sling or pillow)."),
})

REVIEW = [
    "- Converted from your PDF \"Unfolding NGN Case Study: Acute Ischemic Stroke\" with the corrections you approved on 2 Nov 2026.",
    "- Screen 6: repeat CT changed to a PH1 parenchymal hematoma (was HI1), neuro ICU, update on Day 7 (was 48 hours); right arm 3/5.",
    "- Added: weight 82 kg, written-out alteplase dose (74 mg), CT angiography (left M1 occlusion), creatinine, thrombectomy referral.",
    "- Screen 1: vital signs added to the passage; BP 198/108 and the irregular pulse are correct phrases; RLE strength 4/5.",
    "- Screen 2: stem rewritten; row 5 now 'Diaphoresis, tremor, and hunger'; new row 6 (declining LOC with a dilated pupil).",
    "- Screen 4: new row (neuro checks every 15 minutes); softer wording on catheter/NG timing; tenecteplase note.",
    "- Screen 6: SLP dysphagia assessment added to the notes; row 3 is done by the wife.",
    "- Clinician review: recovery course after a symptomatic PH1 bleed with herniation signs; dysphagia diet wording.",
]

case = {
    "id": ID,
    "title": TITLE,
    "course": "NURS 1017",
    "unit": UNIT,
    "topic": UNIT,
    "disorder": UNIT,
    "description": "68-year-old male client with atrial fibrillation who stopped apixaban presents with sudden expressive aphasia and right-sided "
                   "weakness (left MCA ischemic stroke); thrombolysis eligibility, BP control, care during alteplase, symptomatic "
                   "intracerebral hemorrhage during the infusion, and rehabilitation safety (dysphagia, hemianopsia, aphasia, transfers).",
    "authorReview": {
        "note": "Your case study, converted by Claude on 2 Nov 2026; please review before using it with students:\n" + "\n".join(REVIEW),
        "flaggedAt": "2026-11-02",
    },
    "screens": [s1, s2, s3, s4, s5, s6],
}

out = os.path.join(HERE, f"{ID}_NURS_1017_Unit_7_Case_Study_1.json")
with open(out, "w") as f:
    json.dump(case, f, indent=2, ensure_ascii=False)
print("wrote", out)
