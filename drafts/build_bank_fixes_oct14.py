"""Bank clean-up of 14 October 2026 (user request). Writes, for the Supabase workflow:

- drafts/bank_fixes_oct14_patch.json   `patch`: per-screen and per-field changes (before/after)
- drafts/bank_remove_oct14.json        `remove`: the two duplicates and the stroke bow-tie case
- drafts/standalone_1783070000010_...json  `add`: the stroke bow-tie as a stand-alone question

What it does:
1. University of Maryland CS3-CS21: resolves the open review notes (drafts/umd_review/CS<nn>.json) as
   well as possible (chart values, orders, answer keys and their rationales), makes the case studies
   available to students, and records what was changed in `authorReview` (a note only the author
   sees in the studio, "Needs your review"). CS2's one open note goes into its review note too.
2. "Case Study 2" (NURS 1017 Unit 11, DKA) and "Case Study 1" (NURS 1021 Unit 2, heart failure) get
   titles and descriptions (and the heart-failure case its missing drop-down choices), with notes.
3. Answer order: every option list and drop-down whose correct answer is listed first is put in a
   random order (any position may come out correct, first included: the user wants answers randomly
   distributed, not a rule). A drag-and-drop word bank keeps one order for all its blanks. "(Option N)"
   references in rationales are renumbered. Seeded, so the output is reproducible.
4. Removes "New Case Study" and "NCSBN Case Study 2" (duplicates of NURS 1021 Unit 3 Case Study 1 and
   Unit 6 Case Study 2) and moves the Unit 7 stroke bow-tie from the case studies to the stand-alones.
"""
import copy
import json
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'tools'))
import bank  # noqa: E402

TODAY = '2026-10-14'
cases, standalone = bank.load()
ORIG = {c['id']: copy.deepcopy(c) for c in cases}
BY = {c['id']: c for c in cases}
NOTES = {}
U = 'case_17907768000'


def strings(obj, fn):
    """Applies fn to every string inside obj (in place); returns the number of changes fn reports."""
    total = 0
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str):
                new, n = fn(v)
                obj[k] = new
                total += n
            else:
                total += strings(v, fn)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, str):
                new, n = fn(v)
                obj[i] = new
                total += n
            else:
                total += strings(v, fn)
    return total


def R(cid, old, new, n=None):
    """Replaces text everywhere in the item (chart, questions, rationales)."""
    count = strings(BY[cid]['screens'], lambda s: (s.replace(old, new), s.count(old)))
    if not count or (n is not None and count != n):
        raise SystemExit(f'{cid}: {old!r} found {count} times (expected {n or "1+"})')
    return count


def RX(cid, pattern, repl, n=None):
    rx = re.compile(pattern)
    count = strings(BY[cid]['screens'], lambda s: rx.subn(repl, s))
    if not count or (n is not None and count != n):
        raise SystemExit(f'{cid}: /{pattern}/ matched {count} times (expected {n or "1+"})')


def RX0(cid, pattern, repl):
    """Like RX, but finding nothing is fine (for text that appears in some forms only)."""
    rx = re.compile(pattern)
    return strings(BY[cid]['screens'], lambda s: rx.subn(repl, s))


def Q(cid, s):
    return BY[cid]['screens'][s - 1]['question']


def OPT(cid, s, old, new=None, correct=None):
    opts = [o for o in Q(cid, s)['options'] if o['text'] == old]
    if len(opts) != 1:
        raise SystemExit(f'{cid} S{s}: option {old!r} not found')
    if new is not None:
        opts[0]['text'] = new
    if correct is not None:
        opts[0]['correct'] = correct


def ROW(cid, s, old, new=None, key=None):
    q = Q(cid, s)
    rows = [r for r in q['matrix']['rows'] if r.get('text') == old]
    if len(rows) != 1:
        raise SystemExit(f'{cid} S{s}: row {old!r} not found')
    r = rows[0]
    if new is not None:
        r['text'] = new
    if key is not None:
        if q['type'] == 'matrix_mr':
            r['correctIndices'] = list(key)
            r['correctIndex'] = key[0]
        else:
            r['correctIndex'] = key
            if 'correctIndices' in r:
                r['correctIndices'] = [key]


def DD(cid, s, b, old, new=None, correct=None):
    opts = [o for o in Q(cid, s)['cloze']['dropdowns'][b]['options'] if o['text'] == old]
    if len(opts) != 1:
        raise SystemExit(f'{cid} S{s} blank {b}: {old!r} not found')
    if new is not None:
        opts[0]['text'] = new
    if correct is not None:
        opts[0]['correct'] = correct


def EXP(cid, s, old, new):
    """Replaces text in one rationale; spaces in `old` also match <br> line breaks."""
    q = Q(cid, s)
    if old in q['explanation']:
        q['explanation'] = q['explanation'].replace(old, new)
        return
    rx = re.compile(r'(?:\s|<br>)+'.join(re.escape(w) for w in old.split(' ')))
    if not rx.search(q['explanation']):
        raise SystemExit(f'{cid} S{s} rationale: {old!r} not found')
    q['explanation'] = rx.sub(lambda m: new, q['explanation'], count=1)


def EXP_ADD(cid, s, text):
    q = Q(cid, s)
    q['explanation'] = q['explanation'].rstrip() + ' ' + text


def NOTE(cid, *lines):
    NOTES.setdefault(cid, []).extend(lines)


def note_on_row(cid, label, old_value, new_value, n=None):
    """Changes a lab/vital table cell: the value cell right after the row label `label`."""
    RX(cid, r'(' + re.escape(label) + r'.*?</td><td[^>]*>)' + re.escape(old_value) + r'(</td>)', r'\g<1>' + new_value + r'\2', n)


# ======================================================================= Maryland fixes
# CS2 Tuberculosis: no content change; its open note goes to the review note.
NOTE('case_1790769567553', 'Isoniazid is shown as 300 mg PO daily (the source said 1000 mg, above the maximum). Confirm the regimen and dose.')

# ---- CS3 Acute respiratory failure
c = U + '02'
R(c, 'Amoxicillin 500 mg IVPB every 12 hours', 'Piperacillin-tazobactam 4.5 g IVPB every 6 hours')
R(c, 'Gram-negative cocci', 'Gram-negative rods')
R(c, 'gram-negative cocci', 'gram-negative rods')
note_on_row(c, '<b>SaO<sub>2</sub></b><br>95&ndash;100%', '96%', '94%')
note_on_row(c, '<b>Lactate</b><br>0.5&ndash;2.2 mmol/L', '4.5 mmol/L', '2.4 mmol/L')
OPT(c, 1, 'Lactate 4.5 mmol/L', 'Lactate 2.4 mmol/L')
EXP(c, 1, 'The blood pressure is elevated but is not yet critical.',
    'The blood pressure is elevated but is not yet critical. The WBC count, the gram-negative rods in the blood culture and the mildly raised lactate point to infection; they need follow-up and treatment, but the failing gas exchange threatens life first.')
NOTE(c, 'IV amoxicillin (no IV form) replaced by piperacillin-tazobactam 4.5 g IVPB every 6 hours.',
     'Blood culture now "gram-negative rods" (was cocci).',
     'SaO₂ changed from 96% to 94% to fit the PaO₂ of 75 mm Hg.',
     'Lactate changed from 4.5 to 2.4 mmol/L (a lactate of 4.5 would have been one of the most urgent findings on screen 1); rationale sentence added.')

# ---- CS4 Breast cancer
c = U + '04'
ROW(c, 2, 'Sodium 148 mmol/L', 'Axillary lymph node removal 45 days ago', [1])
EXP(c, 2, 'Hypernatremia is not usually associated with cellulitis or DVT but could contribute to the swelling seen in lymphedema, and a low albumin level',
    'Removal of axillary lymph nodes interrupts lymph drainage from the arm and is the main risk factor for lymphedema after breast cancer surgery. A low albumin level')
OPT(c, 4, 'Amoxicillin PO', correct=False)
EXP(c, 4, 'Oral antibiotics such as amoxicillin are indicated to treat a possible infection that may have triggered the lymphedema.',
    'An antibiotic such as amoxicillin is not anticipated: the client is afebrile, and the arm has no redness or warmth, so no infection is suspected. Because she is neutropenic, she is watched closely for infection, and a fever is reported at once.')
R(c, 'Orders received for PO amoxicillin and acetaminophen,', 'Orders received for PO acetaminophen,')
R(c, 'PO acetaminophen and amoxicillin given', 'PO acetaminophen given')
R(c, 'Prescriptions include amoxicillin 500 mg PO twice daily for 10 days; ', 'Prescriptions include ')
RX(c, r'[Aa]cetaminophen 500 mg PO twice (a )?daily', 'acetaminophen 500 mg PO every 6 hours as needed for pain')
NOTE(c, 'Screen 2: the author\'s key kept (numbness/tingling → lymphedema and DVT; HR 104 → cellulitis only). Please confirm.',
     'Screen 2: the weak row "Sodium 148 mmol/L" is now "Axillary lymph node removal 45 days ago" (lymphedema).',
     'Screen 4: amoxicillin is now NOT anticipated (no signs of infection; neutropenic client); it was removed from the 1130 orders note and the discharge prescriptions.',
     'Discharge acetaminophen changed from twice daily to every 6 hours as needed.',
     'Screen 6 "ice bag = no understanding" kept (avoid temperature extremes on the affected arm). Please confirm.')

# ---- CS5 Burns
c = U + '05'
R(c, 'bilateral second- and third-degree burns to the front of the lower extremities',
  'second- and third-degree burns encircling both lower extremities (front and back)')
RX(c, r'(<td[^>]*>1320 mL/hr</td><td[^>]*>)1320 mL/hr(</td>)', r'\g<1>1584 mL/hr\2')
NOTE(c, 'Burns now encircle both legs (front and back), so 36% TBSA (and the 14,400 mL Parkland total) matches the Rule of Nines.',
     'Intake and output: the 2300 IV rate is now 1584 mL/hr (+20% for the 10 mL/hr urine output at 2200, per the titration order).',
     'Albumin order kept as "systolic BP < 80 or diastolic BP < 50". Please confirm "or" vs "and".')

# ---- CS6 STEMI
c = U + '06'
R(c, 'pulse oximetry reading 93% on room air', 'pulse oximetry reading 88% on room air')
R(c, 'Enoxaparin 100 mg SC', 'Enoxaparin 30 mg IV bolus, then 100 mg SC every 12 hours (1 mg/kg; maximum 100 mg for the first 2 doses)')
DD(c, 5, 0, 'enoxaparin 100 mg SC', 'enoxaparin 30 mg IV and 100 mg SC')
R(c, 'Started on unit chest pain protocol.', 'This hospital has no cardiac catheterization laboratory, so fibrinolysis is the reperfusion plan. Started on unit chest pain protocol.')
EXP(c, 3, 'The clot totally blocks the artery, and the blood supply to that part of the heart is lost.',
    'The clot totally blocks the artery, and the blood supply to that part of the heart is lost. It is the plaque that ruptures, not the artery, so the infarction is caused by a blockage of the coronary artery; spasm causes variant (Prinzmetal) angina.')
EXP_ADD(c, 5, 'Primary PCI within 90 minutes is preferred when a catheterization laboratory is available; this hospital has none, so the fibrinolytic is given within 30 minutes.')
NOTE(c, 'Room-air SpO₂ changed from 93% to 88%, so starting oxygen fits current ACS guidelines (oxygen when SpO₂ < 90%).',
     'Enoxaparin written as the fibrinolysis regimen (30 mg IV bolus, then 1 mg/kg SC, maximum 100 mg); drop-down choice updated.',
     'Added that the hospital has no catheterization lab, which explains fibrinolysis within 30 minutes.',
     'Screen 3 key "blockage" kept (the source had no key); rationale now explains plaque rupture vs blockage. Please confirm.',
     'The CS6 bow-tie (stand-alone, still hidden) still keys oxygen and aspirin wording; not changed.')

# ---- CS7 Compartment syndrome
c = U + '07'
R(c, 'RR 29 breaths/min', 'RR 20 breaths/min')
OPT(c, 5, 'Obtain vital signs every hour for 4 hours', 'Obtain vital signs every 15 minutes for 2 hours', correct=False)
EXP(c, 5, 'Measuring and documenting vital signs, intake and output, and height and weight may be done by the UAP,',
    'Measuring intake and output and documenting height and weight may be done by the UAP,')
EXP_ADD(c, 5, 'The vital signs every 15 minutes stay with the nurse: the client has been hypotensive (BP 82/44 mm Hg) and is unstable, so each set must be interpreted together with the neurovascular checks.')
EXP_ADD(c, 6, 'A limb that is now cold with an absent pulse is a serious decline even though the pain is less: pain relief together with loss of the pulse can mean ongoing ischemia, so the nurse notifies the provider immediately.')
NOTE(c, 'Screen 5: the vital-signs task now matches the STAT order (every 15 minutes) and is not delegated (unstable client).',
     'Screen 6: rationale now flags the cold, pulseless limb as urgent.',
     'RR 29 at 0830 changed to 20 (likely typo).',
     'Screen 6 colour keyed Improved (flow sheet N at 1245); the CS7 trend (stand-alone) shows pale (P) for the same time. Please confirm.')

# ---- CS8 COPD I
c = U + '08'
R(c, ' Clubbing noted in all digits bilaterally.', '')
OPT(c, 1, 'Bilateral digital clubbing', 'Barrel chest appearance')
EXP(c, 1, 'Digital clubbing reflects chronic hypoxemia,', 'A barrel chest reflects long-standing hyperinflation,')
ROW(c, 2, 'Digital clubbing', 'Green-tinged sputum', [1, 2])
EXP(c, 2, 'Clinical manifestations of COPD include dyspnea, cough, an increased anteroposterior diameter (barrel chest), digital clubbing, and expiratory wheezing. A barrel chest and digital clubbing are not manifestations of pneumonia, asthma, or pulmonary embolism.',
    'Clinical manifestations of COPD include dyspnea, cough, an increased anteroposterior diameter (barrel chest), and expiratory wheezing. A barrel chest is not a manifestation of pneumonia, asthma, or pulmonary embolism. Green (purulent) sputum fits a bacterial COPD exacerbation or pneumonia. Digital clubbing is not a feature of COPD itself; it suggests another cause, such as lung cancer.')
R(c, 'Provider notified. IV started.', 'Provider notified. Oxygen 1 L/min by nasal cannula started, titrated to a pulse oximetry reading of 88&ndash;92%. IV started.')
RX(c, r'(<td[^>]*>90% on room air</td><td[^>]*>)88% on room air(</td>)', r'\g<1>88% on 2 L/min NC\2')
OPT(c, 4, 'Nursing: Encourage client use of incentive spirometer', correct=False)
EXP(c, 4, 'A high-Fowler&rsquo;s position and the incentive spirometer maximize lung expansion and improve ventilatory effort.',
    'A high-Fowler&rsquo;s position maximizes lung expansion and eases the work of breathing. An incentive spirometer is not effective while the client is in severe respiratory distress; airway clearance is reconsidered once the exacerbation settles.')
R(c, '500 mg PO once, as needed for moderate to severe back pain', '500 mg PO every 6 hours as needed for mild pain or fever')
NOTE(c, 'Digital clubbing removed from the chart (not a feature of COPD); screen 1 option is now "Barrel chest appearance" and the screen 2 row is now "Green-tinged sputum" (COPD and pneumonia).',
     'Low-flow oxygen (1 L/min, target 88–92%) now starts at 1015; the 1045 reading is 88% on 2 L/min.',
     'Screen 4: incentive spirometer is now NOT included during the acute exacerbation.',
     'Acetaminophen order changed to every 6 hours as needed for mild pain or fever (the client had no back pain).')

# ---- CS9 COPD II
c = U + '09'
ROW(c, 2, 'Clubbing in fingers', key=1)
EXP(c, 2, 'Clubbing of the fingers is a sign of long-term hypoxia, and the PaCO',
    'Clubbing of the fingers is not a feature of COPD itself; it suggests another cause, such as lung cancer or bronchiectasis, and should be reported. The PaCO')
R(c, 'salmeterol/fluticasone 25/250 dry powder inhaler', 'fluticasone/salmeterol 250/50 mcg dry powder inhaler')
R(c, 'Levofloxacin 500 mg PO daily.', 'Levofloxacin 750 mg PO daily for 5 days.')
R(c, 'Roflumilast 500 mcg PO daily.', 'Roflumilast 250 mcg PO daily for 4 weeks, then 500 mcg daily.')
NOTE(c, 'Screen 2: clubbing is now keyed "Not associated with COPD", with an explanation.',
     'Inhaler written as fluticasone/salmeterol 250/50 mcg dry powder inhaler.',
     'Discharge: levofloxacin 750 mg daily for 5 days; roflumilast started at 250 mcg for 4 weeks.')

# ---- CS10 DVT II
c = U + '10'
R(c, 'Right pedal pulse weak, palpable.', 'Right pedal pulse 2+, palpable.')
OPT(c, 1, 'Right pedal pulse weak', 'Right pedal pulse 2+', correct=False)
Q(c, 1)['limit'] = 3
R(c, 'Select the <b>4</b> findings', 'Select the <b>3</b> findings', n=None) if 'Select the <b>4</b> findings' in Q(c, 1)['stem'] else R(c, 'Select the 4 findings', 'Select the 3 findings')
EXP(c, 1, 'pedal edema, calf pain, warmth of the right calf, and a weak pedal pulse.', 'pedal edema, calf pain, and warmth of the right calf. The pedal pulse is normal: DVT obstructs a vein, so it does not usually weaken the arterial pulse.')
ROW(c, 2, 'Decreased pedal pulse', 'Fever', [2])
EXP(c, 2, 'A decreased pedal pulse is most suggestive of DVT.', 'Fever suggests infection. A DVT does not usually decrease the pedal pulse, because it blocks a vein, not an artery.')
R(c, 'Positive motion and sensation in the R lower extremity.', 'Positive motion and sensation in the R lower extremity. Weight 80 kg (176 lb).')
R(c, 'Activity: strict bedrest.', 'Activity: bedrest until the heparin infusion has started, then ambulate as tolerated.')
R(c, '<br>Place compression stockings on bilateral lower extremities.', '')
ROW(c, 4, 'Compression stockings to bilateral lower extremities', 'Sequential compression device on the right leg', 1)
ROW(c, 4, 'Ambulate client 3 times a day', 'Ambulate as tolerated once anticoagulation has started', 0)
EXP(c, 4, 'Compression stockings and elevation of the right lower extremity are indicated. Ambulation is contraindicated until anticoagulation has begun, because of the risk of dislodging the thrombus.',
    'Elevation of the right lower extremity is indicated. Current guidelines support walking as tolerated once anticoagulation has started; it does not increase the risk of pulmonary embolism. A sequential compression device is not applied to a leg with an acute DVT, because squeezing the leg could dislodge the thrombus.')
ROW(c, 5, 'Strict bedrest', 'Bedrest until the heparin infusion has started')
ROW(c, 5, 'Place compression stockings on lower extremities', 'Weigh the client', 0)
EXP(c, 5, 'Strict bedrest is implemented immediately, as ordered.', 'Bedrest is implemented immediately, as ordered, and the client is weighed right away because the heparin bolus and infusion are dosed by weight.')
EXP(c, 5, ' Compression stockings will likely need to be obtained from supply and can be applied before the end of the shift.', '')
NOTE(c, 'Pedal pulse is now 2+ (a weak pulse is not a DVT sign); screen 1 is now "select 3"; the screen 2 row "Decreased pedal pulse" is now "Fever" (infection).',
     'Bedrest only until heparin starts; screen 4 keys walking as tolerated once anticoagulated as indicated (CHEST/ASH).',
     'Compression stockings removed from the orders; screen 4 row is now a sequential compression device on the DVT leg (contraindicated); screen 5 row is now "Weigh the client" (immediately).',
     'Weight 80 kg added for the weight-based heparin.',
     'Screen 2 row labels were rebuilt from the source rationale (the source table was blank). Please confirm.')

# ---- CS11 ESRD and peritoneal dialysis
c = U + '11'
ROW(c, 4, 'Vancomycin IV', 'Vancomycin IV as the only antibiotic')
EXP(c, 4, 'Vancomycin is not effective against gram-negative organisms.',
    'Empiric treatment of peritoneal dialysis peritonitis covers both gram-positive and gram-negative organisms until cultures return; vancomycin alone does not treat the gram-negative rods seen on the Gram stain.')
EXP(c, 4, 'Enoxaparin is cleared by the kidneys, so it accumulates in ESRD and increases the risk of bleeding.',
    'Enoxaparin is cleared by the kidneys, so it accumulates in ESRD and increases the risk of bleeding; when anticoagulation is needed, unfractionated heparin is preferred.')
R(c, 'an LPN', 'a practical nurse (LPN/RPN)')
Q(c, 5)['matrix']['columns'] = ['RN' if x == 'RN' else ('LPN/RPN' if x == 'LPN' else x) for x in Q(c, 5)['matrix']['columns']]
EXP(c, 5, 'The LPN performs', 'The practical nurse (LPN/RPN) performs')
EXP(c, 5, 'The LPN cannot', 'The practical nurse cannot')
RX(c, r'<b>WBC count, dialysate</b><br>Few', '<b>WBC count, dialysate</b><br>&lt; 100 &times; 10<sup>6</sup>/L (&lt; 100 cells/&micro;L)')
RX(c, r'<b>Polymorphonuclear cells, dialysate</b><br>Few', '<b>Polymorphonuclear cells, dialysate</b><br>&lt; 50%')
NOTE(c, 'Screen 4 row is now "Vancomycin IV as the only antibiotic" (not appropriate); rationale explains empiric gram-positive and gram-negative coverage.',
     'Enoxaparin rationale now says unfractionated heparin is preferred in ESRD.',
     'Delegation uses "practical nurse (LPN/RPN)"; keys follow the source. Please confirm against Ontario scope.',
     'Dialysate reference ranges added (WBC < 100 cells/µL, neutrophils < 50%).',
     'Screen 6 "exit site open to air = does not understand" kept; practice varies once the site is healed. Please confirm with your program.')

# ---- CS12 GERD
c = U + '12'
R(c, 'Morphine 2 mg and ondansetron 4 mg given IV.', 'Pantoprazole 40 mg and ondansetron 4 mg given IV. 12-lead ECG: normal sinus rhythm. Troponin within normal limits.')
R(c, 'Administer morphine 2 mg IV STAT.', 'Administer pantoprazole 40 mg IV STAT.')
R(c, 'Schedule follow-up with gastroenterologist.', 'Schedule follow-up with gastroenterologist.</p><p>7. 12-lead ECG and troponin STAT.</p><p>8. Replace potassium per protocol if below 3.5 mmol/L.')
OPT(c, 4, 'Administer analgesics', 'Administer a proton pump inhibitor')
EXP(c, 4, 'The client&rsquo;s pain, nausea, and vomiting should be treated,', 'The client&rsquo;s nausea and vomiting should be treated, and the reflux pain is treated by reducing stomach acid with a proton pump inhibitor (opioids are not used for reflux pain),')
EXP_ADD(c, 1, 'Because the client has had intermittent chest pain, a cardiac cause is still ruled out with an ECG and troponin, which are ordered at 0415.')
R(c, 'Taught client about diet,', 'Potassium replacement started per protocol. Taught client about diet,')
NOTE(c, 'An ECG and troponin are now ordered and documented as normal, so chest pain is ruled out before GERD is diagnosed.',
     'Morphine replaced by pantoprazole 40 mg IV; screen 4 option "Administer analgesics" is now "Administer a proton pump inhibitor".',
     'Potassium replacement ordered and started for K 3.0 mmol/L.')

# ---- CS13 Heart failure
c = U + '13'
ROW(c, 6, 'Thirst', 'Worry about his health', 2)
EXP(c, 6, 'Thirst is not related to the heart failure and is keyed as unchanged.', 'He was anxious about his condition on day 1 and is worried now, so his worry is unchanged.')
note_on_row(c, '<b>Hemoglobin (Hgb)</b><br>Male: 130&ndash;180 g/L; Female: 120&ndash;160 g/L', '135 g/L', '115 g/L')
R(c, 'hydrochlorothiazide 25 mg PO twice a day', 'furosemide 40 mg PO twice a day')
R(c, 'hydrochlorothiazide', 'furosemide')
NOTE(c, 'Screen 6 row "Thirst" (no day-1 baseline) is now "Worry about his health" (unchanged).',
     'Hemoglobin changed from 135 to 115 g/L to fit the hematocrit of 0.346.',
     'Hydrochlorothiazide 25 mg twice daily replaced by furosemide 40 mg twice daily (loop diuretic).')

# ---- CS14 HIV with PCP
c = U + '14'
ROW(c, 4, 'Administer ibuprofen as needed for fever', 'Administer acetaminophen as needed for fever')
EXP_ADD(c, 4, 'Acetaminophen is used for the fever because the creatinine is raised, and NSAIDs such as ibuprofen can harm the kidneys. Because the client is hypoxemic, a corticosteroid (prednisone) is usually added to trimethoprim/sulfamethoxazole for moderate to severe PCP.')
note_on_row(c, '<b>Sodium</b><br>135&ndash;145 mmol/L', '148 mmol/L', '144 mmol/L')
EXP(c, 1, 'The hematocrit, platelets, and potassium are within normal limits.', 'The hematocrit, platelets, potassium, and sodium are within normal limits.')
NOTE(c, 'Screen 4: ibuprofen replaced by acetaminophen (raised creatinine); rationale mentions adjunct corticosteroids for hypoxemic PCP.',
     'Sodium changed from 148 to 144 mmol/L (it was not keyed as concerning).',
     'Screen 6 "I can stop wearing a mask when I feel better = no understanding" kept. Please confirm.')

# ---- CS15 DKA (type 2, SGLT2 inhibitor)
c = U + '15'
ROW(c, 4, 'Administer insulin glargine subcutaneously', key=2)
ROW(c, 4, 'Insert indwelling urinary catheter', key=2)
EXP(c, 4, 'DKA is treated with IV regular insulin, which can be titrated, not subcutaneous insulin glargine. Urine output can be measured with a urinal; an indwelling catheter adds infection risk in a client with diabetes.',
    'DKA is treated with IV regular insulin, which can be titrated; subcutaneous insulin glargine is not needed now (some protocols add it early, before the infusion is stopped). The client is voiding, so output can be measured with a urinal; an indwelling catheter is not needed now and adds infection risk.')
RX(c, r'(<td[^>]*>)89% on room air(</td>)', r'\g<1>95% on room air\2')
RX(c, r'(<td[^>]*>)92% on 2 L/min NC(</td>)', r'\g<1>95% on room air\2')
RX(c, r'(<td[^>]*>)94% on 2 L/min NC(</td>)', r'\g<1>96% on room air\2')
RX(c, r'(<td[^>]*>)95% on 2 L/min NC(</td>)', r'\g<1>96% on room air\2')
R(c, ' Oxygen 2 L/min by nasal cannula started.', '')
R(c, 'Sitagliptin/metformin 50 mg/1000 mg PO daily', 'Sitagliptin/metformin 50 mg/1000 mg PO twice daily')
EXP_ADD(c, 1, 'His medications include empagliflozin, an SGLT2 inhibitor that increases the risk of ketoacidosis in type 2 diabetes; it is important background, but it is not a finding that needs follow-up first.')
NOTE(c, 'Screen 4: insulin glargine and the indwelling catheter are now "Nonessential" (were contraindicated).',
     'Pulse oximetry is now normal on room air and no oxygen is started (the 89% was unexplained with clear lungs).',
     'Sitagliptin/metformin changed to twice daily; screen 1 rationale mentions empagliflozin as a DKA risk.',
     'The corrected blood gas (PaCO₂ 25, HCO₃⁻ 10), the KCl concentration (20 mmol/L) and the changed key "pursed-lip breathing = contraindicated" from the conversion still need your confirmation.')

# ---- CS16 Liver failure
c = U + '16'
ROW(c, 4, 'Administer acetaminophen 650 mg as needed for temperature above 101° F (38.3° C)', 'Administer ibuprofen 400 mg as needed for temperature above 101° F (38.3° C)')
EXP(c, 4, 'Acetaminophen (metabolized by the liver) and sedatives are contraindicated,',
    'Ibuprofen and other NSAIDs are contraindicated in cirrhosis (they increase the risk of bleeding and kidney injury; acetaminophen up to about 2 g a day is the preferred antipyretic), sedatives are contraindicated,')
ROW(c, 4, 'Point-of-care glucose every 6 hours', key=0)
EXP(c, 4, 'Glucose monitoring would not harm the client but is not necessary.',
    'Point-of-care glucose checks are indicated: the client is malnourished with alcohol use disorder, so his liver cannot make enough glucose, and his fasting glucose is already 3.9 mmol/L.')
RX(c, r'(<td[^>]*>)Metoprolol XL(</td><td[^>]*>)50 mg PO daily(</td>)', r'\g<1>Propranolol\g<2>20 mg PO twice daily\3')
R(c, 'Morning medications (metoprolol and spironolactone) given.', 'Morning medications (propranolol and spironolactone) given.')
NOTE(c, 'Screen 4: the acetaminophen row is now ibuprofen (contraindicated in cirrhosis); acetaminophen ≤ 2 g/day is preferred.',
     'Screen 4: point-of-care glucose is now Indicated (malnourished, glucose 3.9 mmol/L).',
     'Metoprolol XL replaced by propranolol 20 mg twice daily (nonselective beta-blocker for portal hypertension).',
     'No creatinine is charted; consider adding one.')

# ---- CS17 Prostatectomy with hemorrhagic shock
c = U + '17'
R(c, 'Ketorolac 30 mg IV push given.', 'Morphine 2 mg IV push given.')
R(c, 'Indwelling urinary catheter with continuous bladder irrigation draining clear, red-colored urine.', 'Indwelling urinary catheter draining light red urine.')
R(c, 'Irrigation rate increased.', 'Catheter patency checked.')
assert RX0(c, r'<p>Maintain traction on catheter</p>', '') + RX0(c, r'Maintain traction on catheter\s*', '') > 0
assert RX0(c, r'(<p>)?\{?Continuous bladder irrigation: titrate to keep urine pink to clear\}?(</p>)?\s*', '') > 0
R(c, 'The physician assesses the client, applies traction to the catheter, and writes orders.', 'The physician assesses the client and writes orders.')
EXP(c, 4, ' The catheter stays in place; the provider may apply traction to put pressure on bleeding sites.', ' The catheter stays in place to monitor the bleeding and the urine output.')
EXP(c, 5, 'The other orders (irrigation titration, blood work, reporting results, and a possible transfusion) follow.', 'The other orders (blood work, reporting results, and a possible transfusion) follow.')
EXP_ADD(c, 3, 'The neurologic finding (confusion) and the low oxygen saturation are effects of poor perfusion; the cardiovascular findings show the cause.')
NOTE(c, 'Ketorolac (an NSAID, in a bleeding client) replaced by morphine 2 mg IV.',
     'Continuous bladder irrigation and catheter traction removed (they belong to TURP, not robotic radical prostatectomy); the screen 5 highlight passage no longer lists them.',
     'Screen 3 key "cardiovascular assessment" kept (the source had no key); rationale strengthened. Please confirm.')

# ---- CS18 Spine surgery
c = U + '18'
OPT(c, 5, 'Check the surgical dressing in the mirror daily.', 'Have a family member check the surgical dressing daily.')
EXP(c, 5, 'The client should check the surgical dressing daily to monitor drainage.', 'A family member checks the dressing daily to monitor drainage, because a lumbar incision is hard to see.')
RX(c, r'(<td[^>]*>)Senna(</td><td[^>]*>)1 tablet PO twice daily(</td>)', r'\g<1>Docusate sodium\g<2>100 mg PO twice daily\3')
ROW(c, 4, 'Administer senna 1 tablet PO twice daily', 'Administer docusate sodium 100 mg PO twice daily')
EXP(c, 4, 'Senna prevents straining', 'Docusate, a stool softener, prevents straining')
NOTE(c, 'Screen 5: "check the dressing in the mirror" is now "have a family member check the dressing daily".',
     'Senna (a stimulant laxative) replaced by docusate (a stool softener), so the teaching about a stool softener is accurate.',
     'The CS18 bow-tie (stand-alone, still hidden) still places a wound infection on day 1–2; not changed.')

# ---- CS19 Stroke
c = U + '19'
R(c, 'Heart rate 99 beats/min', 'Heart rate 112 beats/min')
EXP(c, 1, 'and the heart rate and elevated blood pressure', 'and the raised heart rate (112 beats/min) and blood pressure')
note_on_row(c, '<b>Hematocrit (Hct)</b><br>Male: 0.42&ndash;0.52 L/L; Female: 0.35&ndash;0.47 L/L', '0.55 L/L', '0.40 L/L')
note_on_row(c, '<b>Platelet count</b><br>140&ndash;450 &times; 10<sup>9</sup>/L', '500 &times; 10<sup>9</sup>/L', '250 &times; 10<sup>9</sup>/L')
note_on_row(c, '<b>Prothrombin time (PT)</b><br>9.5&ndash;12 seconds', '13.5 seconds', '11 seconds')
R(c, 'apixaban at discharge discussed', 'antiplatelet therapy (aspirin) at discharge discussed')
ROW(c, 6, '“The physical therapist will determine my functional ability.”', '“Once I go home, I will not need any more therapy.”')
EXP(c, 6, 'The baseline assessment of the client&rsquo;s functional ability (motor, social, and cognitive) is completed by the nurse.',
    'Rehabilitation (physical, occupational, and speech therapy) usually continues after discharge, so the client will still need therapy at home.')
EXP(c, 6, 'she will take apixaban, an oral anticoagulant.', 'she will take an antiplatelet medication (aspirin).')
NOTE(c, 'Heart rate changed from 99 to 112 beats/min, so it is truly abnormal (it is keyed on screen 1).',
     'Unexplained labs normalized: Hct 0.40 L/L, platelets 250 × 10⁹/L, PT 11 seconds.',
     'Discharge apixaban (no atrial fibrillation) replaced by antiplatelet therapy (aspirin).',
     'Screen 6: the physical-therapist statement is now "I will not need any more therapy" (no understanding).',
     'The CS19 bow-tie (stand-alone, still hidden) keys oxygen with no SpO₂ charted; not changed.')

# ---- CS20 Tension pneumothorax
c = U + '20'
R(c, 'Chest X-ray obtained. Medicated with morphine.', 'Medicated with morphine.')
R(c, 'Fluctuations noted in the water seal chamber.', 'Fluctuations noted in the water seal chamber. Chest X-ray obtained after the chest tube was placed.')
OPT(c, 4, 'Obtain a STAT chest X-ray', 'Obtain a chest X-ray after the chest tube is placed')
EXP(c, 4, 'A chest X-ray is done before chest tube placement if time allows; otherwise it is obtained soon after.',
    'A tension pneumothorax is a clinical diagnosis: decompression is never delayed for an X-ray, which is done after the chest tube is placed to confirm its position and the re-expansion of the lung.')
OPT(c, 4, 'Insert an indwelling urinary catheter', 'Prepare the client for a thoracentesis')
EXP(c, 4, 'An indwelling urinary catheter is not needed to treat the pneumothorax.', 'A thoracentesis drains fluid, not air, so it does not treat a pneumothorax.')
R(c, 'Muffled heart sounds.', 'Jugular veins distended.')
ROW(c, 2, 'Muffled heart sounds', 'Jugular venous distention', [1, 2])
EXP(c, 2, 'Muffled heart sounds occur with cardiac tamponade and may occur with a tension pneumothorax.',
    'Jugular venous distention occurs with both cardiac tamponade and tension pneumothorax, because both obstruct the return of blood to the heart.')
ROW(c, 5, 'Document chest tube drainage every shift', 'Measure and record chest tube drainage hourly at first')
R(c, 'Crackles heard in the right lung fields.', 'Breath sounds clear on the right.')
RX(c, r'(<td[^>]*>95% on 4 L/min nasal cannula</td><td[^>]*>)98% on room air(</td>)', r'\g<1>97% on 2 L/min nasal cannula\2')
EXP(c, 6, 'SpO 2 on room air', 'SpO 2 on less oxygen') if 'SpO 2 on room air' in Q(c, 6)['explanation'] else EXP(c, 6, 'on room air', 'on less oxygen')
NOTE(c, 'Chest X-ray moved to after decompression and chest tube; screen 4 option now "Obtain a chest X-ray after the chest tube is placed".',
     'Screen 4: the urinary catheter option is now "Prepare the client for a thoracentesis" (not anticipated).',
     'Muffled heart sounds (a tamponade sign) replaced by jugular venous distention in the chart and the screen 2 grid.',
     'Screen 5: drainage is measured hourly at first (was every shift); unexplained right-sided crackles removed; 1600 SpO₂ now 97% on 2 L/min.',
     'Screen 3 uses rationale scoring as in the source. The CS20 bow-tie (stand-alone, still hidden) still keys the chest X-ray as an action; not changed.')

# ---- CS21 Thyroid storm
c = U + '21'
RX(c, r'(Pulse Oximetry Reading \(SpO<sub>2</sub>\)</b></td><td[^>]*>)97% on room air', r'\g<1>92% on room air')
RX(c, r'(<td[^>]*>92% on room air</td><td[^>]*>)97% on room air', r'\g<1>92% on room air')
ROW(c, 6, 'Oxygenation', key=0)
EXP(c, 6, 'and oxygenation is stable (unchanged) with an SpO<sub>2</sub> of 97%.', 'and oxygenation has improved, from 92% on room air to 97% on 2 L/min of oxygen.')
note_on_row(c, '<b>Thyroid-stimulating hormone (TSH)</b><br>0.45&ndash;4.5 mU/L', '0.27 mU/L', '&lt; 0.01 mU/L')
R(c, '8. Methimazole 20 mg PO every 8 hours', '8. Methimazole 20 mg PO every 8 hours</p><p>9. Propranolol 60 mg PO every 4 hours')
R(c, 'Order received for oral methimazole.', 'Orders received for oral methimazole and propranolol.')
R(c, 'administration of oral methimazole and acetaminophen as ordered', 'administration of oral methimazole, propranolol, and acetaminophen as ordered')
Q(c, 4)['options'].append({'text': 'Oral propranolol', 'correct': True})
EXP(c, 4, 'An antithyroid medication such as methimazole is an expected therapy for thyroid storm.',
    'An antithyroid medication such as methimazole is an expected therapy for thyroid storm, and a beta-blocker (propranolol) controls the tachycardia and other adrenergic effects.')
NOTE(c, 'Room-air SpO₂ changed from 97% to 92% (0900, 0910) so oxygen is indicated; screen 6 now keys oxygenation as Improved.',
     'TSH changed from 0.27 to < 0.01 mU/L (suppressed, as expected in thyroid storm).',
     'Propranolol 60 mg PO every 4 hours added to the orders and as a correct option on screen 4.',
     'Screen 5 key (oxygen and the ECG first) still comes from the source rationale (its highlighting was unreadable). Please confirm.',
     'Methimazole kept (propylthiouracil is often preferred in thyroid storm).')

UMD_FIXED = [U + n for n in ('02', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21')]

# ======================================================================= other case studies
c = 'case_1780489713691'
BY[c]['title'] = 'NURS 1017 Unit 11 Case Study 1'
BY[c]['description'] = ('A 20-year-old female client with weeks of polydipsia and polyuria who presents with vomiting and '
                        'drowsiness in diabetic ketoacidosis, from the emergency department through fluid resuscitation and insulin therapy.')
ROW(c, 2, 'Polyruria', 'Polyuria')
NOTE(c, 'Title made up: "NURS 1017 Unit 11 Case Study 1" (was "Case Study 2"), with a new description. Please check both.',
     'Screen 2 row typo "Polyruria" corrected.')

c = 'cardio-case-1'
BY[c]['title'] = 'NURS 1021 Unit 2 Case Study 1'
BY[c]['description'] = ('A 72-year-old male client in the emergency department in respiratory distress from acute heart failure '
                        'that progresses from the left to the right side, through diagnostics, medications, and discharge teaching.')
blank = Q(c, 3)['cloze']['dropdowns'][0]['options']
assert [o['text'] for o in blank] == ['', '', ''], blank
blank[0]['text'] = 'high-Fowler’s'
blank[1]['text'] = 'supine'
blank[2]['text'] = 'Trendelenburg'
EXP(c, 6, '1. Gaining 0.5 lbs overnight', 'Gaining 0.5 lb overnight')
EXP(c, 6, '2. Client should stop', 'The client should stop')
EXP(c, 6, '3. Heart failure clients', 'Clients with heart failure')
NOTE(c, 'Title "NURS 1021 Unit 2 Case Study 1" and description made up. Please check both.',
     'Screen 3: the first drop-down had three empty choices; now high-Fowler’s (correct, per the rationale), supine and Trendelenburg.',
     'Screen 6 rationale no longer numbers its points 1–3 (they looked like option numbers).')

# ======================================================================= random answer order
rng = random.Random(20261014)


def renumber(expl, mapping):
    def sub(m):
        word, first, rest = m.group(1), m.group(2), m.group(3)
        ren = lambda n: str(mapping.get(int(n) - 1, int(n) - 1) + 1)
        return f'{word} {ren(first)}' + re.sub(r'\d+', lambda d: ren(d.group(0)), rest)
    return re.sub(r'\b(Options?)\s+(\d+)((?:\s*(?:,|and|&amp;|or)\s*\d+)*)', sub, expl)


def shuffled(n):
    order = list(range(n))
    while True:
        rng.shuffle(order)
        if order != list(range(n)) or n < 2:
            return order


SKIP_SHUFFLE = {'case_1782149061171', 'case_1782159166328', 'case_1789577787012', 'case_1790621568594'}
shuffle_log = []
for cdata in cases:
    if cdata['id'] in SKIP_SHUFFLE:
        continue
    for s, screen in enumerate(cdata['screens'], 1):
        q = screen['question']
        t = q.get('type')
        if t in ('select_all', 'multiple_choice', 'select_n', 'trend') and q.get('options') and q['options'][0].get('correct') \
                and not all(o.get('correct') for o in q['options']):
            order = shuffled(len(q['options']))
            mapping = {old: new for new, old in enumerate(order)}
            q['options'] = [q['options'][i] for i in order]
            if q.get('explanation'):
                q['explanation'] = renumber(q['explanation'], mapping)
            shuffle_log.append((cdata['id'], s, 'options'))
        if t in ('dropdown_cloze', 'dyad', 'triad') and q.get('cloze'):
            for b, dd in enumerate(q['cloze']['dropdowns']):
                if dd['options'] and dd['options'][0].get('correct'):
                    order = shuffled(len(dd['options']))
                    dd['options'] = [dd['options'][i] for i in order]
                    shuffle_log.append((cdata['id'], s, f'blank {b + 1}'))
        if t == 'drag_drop_cloze' and q.get('cloze'):
            dds = q['cloze']['dropdowns']
            if dds and dds[0]['options'] and dds[0]['options'][0].get('correct'):
                n = len(dds[0]['options'])
                if all(len(d['options']) == n for d in dds) and len({tuple(o['text'] for o in d['options']) for d in dds}) == 1:
                    order = shuffled(n)
                    for d in dds:
                        d['options'] = [d['options'][i] for i in order]
                else:
                    for d in dds:
                        d['options'] = [d['options'][i] for i in shuffled(len(d['options']))]
                shuffle_log.append((cdata['id'], s, 'word bank'))

# ======================================================================= availability and review notes
for cid in UMD_FIXED:
    if BY[cid].get('draft'):
        BY[cid]['draft'] = False
for cid, lines in NOTES.items():
    BY[cid]['authorReview'] = {
        'note': 'Changed by Claude on 14 Oct 2026; please double-check:\n' + '\n'.join(lines),
        'flaggedAt': TODAY,
    }

# ======================================================================= outputs
REMOVE = [('case_1782149061171', 'NCSBN Case Study 2'), ('case_1782159166328', 'New Case Study'),
          ('case_1789577787012', 'NURS 1017 Unit 7 Bowtie 1: Ischemic Stroke with Atrial Fibrillation')]
entries = []
for cid, before in ORIG.items():
    if cid in dict(REMOVE):
        continue
    after = BY[cid]
    for i, (sb, sa) in enumerate(zip(before['screens'], after['screens'])):
        if sb != sa:
            entries.append({'row': 'cases', 'id': cid, 'path': ['screens', i], 'before': sb, 'after': sa})
    for field in ('title', 'description', 'draft', 'authorReview'):
        if before.get(field) != after.get(field):
            entries.append({'row': 'cases', 'id': cid, 'path': [field], 'before': before.get(field), 'after': after.get(field)})

with open(os.path.join(HERE, 'bank_fixes_oct14_patch.json'), 'w', encoding='utf-8') as f:
    json.dump(entries, f, ensure_ascii=False, indent=1)
with open(os.path.join(HERE, 'bank_remove_oct14.json'), 'w', encoding='utf-8') as f:
    json.dump([{'row': 'cases', 'id': i, 'title': t} for i, t in REMOVE], f, ensure_ascii=False, indent=1)

stroke = copy.deepcopy(ORIG['case_1789577787012'])
bowtie = {
    'id': 'standalone_1783070000010',
    'title': 'Unit 7 Stand-alone 10: Bowtie - Ischemic Stroke with Atrial Fibrillation',
    'course': stroke['course'], 'unit': stroke['unit'], 'topic': stroke['topic'], 'disorder': stroke['disorder'],
    'description': stroke['description'], 'availability': stroke.get('availability', 'all'),
    'isStandalone': True, 'updatedAt': TODAY + 'T12:00:00.000Z', 'screens': stroke['screens'],
}
bowtie_file = os.path.join(HERE, 'standalone_1783070000010_Unit_7_Stand_alone_10_Bowtie_Ischemic_Stroke_with_Atrial_Fibrillation.json')
with open(bowtie_file, 'w', encoding='utf-8') as f:
    json.dump(bowtie, f, ensure_ascii=False, indent=2)

print(f'{len(entries)} patch entries; {len(shuffle_log)} answer lists reshuffled in '
      f'{len({x[0] for x in shuffle_log})} case studies; review notes on {len(NOTES)} items; '
      f'{len(REMOVE)} to remove; stand-alone bow-tie written.')
