"""NURS 1017 Unit 5 Case Studies 6, 7 and 8 (burns with inhalation injury, herpes zoster ophthalmicus,
erythrodermic psoriasis): option order, one highlight phrase, and expanded rationales with figures.
October 2026, at the user's request; applied with `tools/supabase.js patch`.

1. Answer order. The player shows options and drop-down choices in their stored order, and these
   cases listed correct answers first (for example, the five correct answers of a "select five" item
   were options 1-5). The orders below are fixed by hand, not random: no item starts with a correct
   answer, and correct answers are neither grouped nor strictly alternating. The drag-and-drop word
   bank (Case Study 7, screen 5) follows the first blank's order, so all its blanks get the same order.
   Answer keys are unchanged.
2. Case Study 6, screen 1: "Reports headache and nausea." is no longer part of the correct phrase
   "Oriented to person only; unsure of the time or place." (as in the source answer key, where it is
   not highlightable).
3. Rationales: rewritten as structured HTML (answer, why, why not, beyond-the-chapter notes) built on
   the source answer key, with figures. Diagrams are original (files/rationale/*.svg); photographs are
   from Wikimedia Commons under CC BY-SA or public domain, credited in each caption. Images live in the
   repository (served by GitHub Pages next to index.html), so the item data only holds their paths.
   Select-all/select-N rationales name options as "(Option N)" in the new order.

Writes drafts/integ_rationales_patch.json: [{row, id, path, before, after}].
"""
import copy
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'tools'))
import bank  # noqa: E402

C6, C7, C8 = 'case_1782390000006', 'case_1782390000007', 'case_1782390000008'
IMG = 'files/rationale/'

# ---------------------------------------------------------------- figures

PHOTOS = {
    # local file: (Commons file name, author, licence, licence URL)
    'burn-partial-thickness-hand.jpg': ('Hand2ndburn.jpg', 'Kronoman', 'CC BY-SA 3.0',
                                        'https://creativecommons.org/licenses/by-sa/3.0/'),
    'burn-full-thickness-foot.jpg': ('8-day-old-3rd-degree-burn.jpg', 'Craig0927', 'public domain', None),
    'zoster-chest-dermatome.jpg': ('Herpes zoster chest.png', 'Fisle', 'CC BY-SA 3.0',
                                   'https://creativecommons.org/licenses/by-sa/3.0/'),
    'zoster-cornea-fluorescein.jpg': ('HerpesZosterOpth.jpg', 'James Heilman, MD', 'CC BY-SA 4.0',
                                      'https://creativecommons.org/licenses/by-sa/4.0/'),
    'psoriasis-plaque.jpg': ('Psoriasis2010.JPG', 'James Heilman, MD', 'CC BY-SA 3.0',
                             'https://creativecommons.org/licenses/by-sa/3.0/'),
    'impetigo-honey-crust.jpg': ('Impetigo2020.jpg', 'James Heilman, MD', 'CC BY-SA 4.0',
                                 'https://creativecommons.org/licenses/by-sa/4.0/'),
}
PHOTOS_FILE = os.path.join(HERE, 'integ_photos.json')  # extra photos chosen after review
if os.path.exists(PHOTOS_FILE):
    with open(PHOTOS_FILE, encoding='utf-8') as f:
        for k, v in json.load(f).items():
            PHOTOS[k] = tuple(v) if v else None

LINK = 'target="_blank" rel="noopener"'


def figure(file, alt, caption):
    """A figure the browser serializes exactly as written (so the editor's open-and-save keeps it)."""
    src = IMG + file
    if not file.endswith('.svg'):  # photographs need a credit; diagrams (.svg) are original
        if not PHOTOS.get(file):
            raise SystemExit(f'No credit recorded for {file}')
        name, author, lic, lic_url = PHOTOS[file]
        page = 'https://commons.wikimedia.org/wiki/File:' + name.replace(' ', '_')
        lic_html = f'<a href="{lic_url}" {LINK}>{lic}</a>' if lic_url else lic
        credit = (f' Photo: {html.escape(author)}, <a href="{html.escape(page)}" {LINK}>Wikimedia Commons</a>, '
                  f'{lic_html}.')
    else:
        credit = ''
    return ('<figure style="margin: 12px 0; text-align: center;">'
            f'<a href="{src}" {LINK}><img src="{src}" alt="{html.escape(alt)}" style="max-width: 100%; '
            f'{"" if file.endswith(".svg") else "max-height: 320px; "}height: auto; border: 1px solid #e2e8f0; '
            'border-radius: 6px;"></a>'
            f'<figcaption style="font-size: 12px; color: #64748b; margin-top: 4px; text-align: left;">'
            f'{caption}{credit}</figcaption></figure>')


def head(text):
    return f'<p><b>{text}</b></p>'


def ul(*items):
    return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'


def beyond(text):
    return f'<p style="font-size: 12px; color: #64748b;"><i>Beyond the chapter: {text}</i></p>'


def p(text):
    return f'<p>{text}</p>'


# ---------------------------------------------------------------- option orders (old indices)

OPTION_ORDER = {
    (C7, 0): [2, 0, 7, 8, 4, 1, 9, 3, 6, 5],
    (C7, 3): [6, 2, 0, 8, 5, 4, 9, 7, 1, 3],
    (C8, 3): [7, 3, 0, 9, 5, 1, 10, 4, 6, 8, 2],
}
DROPDOWN_ORDER = {
    (C6, 2): [[1, 3, 0, 2], [3, 0, 1, 2], [2, 1, 3, 0], [1, 3, 0, 2]],
    (C6, 3): [None, None, None, [2, 1, 0, 3], None],
    (C7, 2): [[1, 3, 0, 2], [1, 0, 3, 2], [3, 1, 2, 0], [1, 0, 3, 2]],
    (C8, 1): [[1, 3, 0, 2], [2, 0, 3, 1], [2, 3, 1, 0], [2, 0, 3, 1], [2, 3, 0, 1]],
    (C8, 2): [[1, 3, 0, 2], [1, 0, 3, 2], [3, 1, 2, 0]],
}
WORD_BANK_ORDER = {(C7, 4): [5, 2, 7, 0, 9, 4, 1, 8, 3, 6]}


def opt_no(case_id, screen, old_index):
    """'(Option N)' for an option, numbered in its new position."""
    return f'(Option {OPTION_ORDER[(case_id, screen)].index(old_index) + 1})'


# ---------------------------------------------------------------- rationales

def o7(s, i):
    return opt_no(C7, s, i)


def o8(s, i):
    return opt_no(C8, s, i)


RATIONALES = {
    # ---------------- Case Study 6: flame burns with suspected inhalation injury
    (C6, 0): ''.join([
        p('<b>Highlight these five findings:</b> oriented to person only; hoarse voice with a frequent cough; '
          'black-tinged sputum; singed nasal hairs and eyebrows with soot around the nose and mouth; and '
          'expiratory wheezes.'),
        figure('u5c6-inhalation-cues.svg', 'Diagram of a head, larynx, trachea and lungs with the inhalation injury cues labelled',
               "Smoke inhalation injury: D.R.'s cues from the face down to the lungs."),
        head('Why these findings'),
        ul('<b>Hoarse voice and frequent cough:</b> heat and smoke injure the larynx. Swelling there can progress '
           'within hours to stridor and complete airway obstruction, so hoarseness is a red-flag cue.',
           '<b>Black-tinged (carbonaceous) sputum:</b> soot in the sputum shows that smoke was inhaled below the '
           'vocal cords.',
           '<b>Singed nasal hairs and eyebrows; soot around the nose and mouth:</b> classic external signs of '
           'smoke and heat inhalation, especially after being trapped in an enclosed, smoke-filled room.',
           '<b>Expiratory wheezes:</b> bronchospasm and lower-airway irritation from inhaled smoke and chemicals.',
           '<b>Oriented to person only:</b> new confusion after smoke exposure suggests cerebral hypoxia from '
           'carbon monoxide (CO) and/or impaired gas exchange. It belongs to both Breathing and Disability in '
           'the ABCDE sequence.'),
        p('The headache and nausea in the same note are early signs of CO poisoning, explored in the next '
          'question.'),
        head('Why the other phrases are not airway cues'),
        ul('<b>Tearful, asking about his dog:</b> an expected emotional response. He will need support once he '
           'is stable.',
           '<b>Chest pain 9/10:</b> comes from the partial-thickness (second-degree) burn of the anterior trunk, '
           'which is very painful because nerve endings are exposed. It needs treatment, but it is not an airway '
           'cue.',
           '<b>Circumferential full-thickness burn of the right arm:</b> a circulation concern (risk of '
           'compartment syndrome). A circumferential full-thickness burn of the <i>chest</i> could restrict '
           'breathing; one of the arm cannot.',
           '<b>Ring and watch on the burned arm:</b> they must come off before swelling starts, but they do not '
           'signal airway risk.'),
        figure('burn-partial-thickness-hand.jpg', 'Photograph of a partial-thickness burn with a blister on the back of a hand',
               "A partial-thickness (second-degree) burn: red, moist and blistered, and very painful, like D.R.'s "
               'chest and abdomen.'),
    ]),
    (C6, 1): ''.join([
        head('Correct answers'),
        ul('Hoarse voice: upper airway (inhalation) injury',
           'Singed nasal hairs: upper airway (inhalation) injury',
           'Headache and nausea: carbon monoxide poisoning',
           'Oriented to person only: upper airway (inhalation) injury <b>and</b> carbon monoxide poisoning',
           'SpO<sub>2</sub> 98% despite new confusion: carbon monoxide poisoning',
           'HR 122 beats/min with BP 104/66 mm Hg: hypovolemia related to the burn',
           'Hematocrit 0.53 L/L (53%): hypovolemia related to the burn'),
        figure('u5c6-co-pulse-ox.svg', 'Diagram comparing oxyhemoglobin and carboxyhemoglobin, and a pulse oximeter reading with co-oximetry',
               'Why a normal pulse oximeter reading does not rule out carbon monoxide poisoning.'),
        head('Why'),
        ul('<b>Hoarse voice and singed nasal hairs:</b> direct evidence that hot gas and smoke reached the '
           'airway; swelling of the larynx causes the hoarseness.',
           '<b>Headache and nausea:</b> early, nonspecific symptoms of CO toxicity. CO binds hemoglobin about '
           '200 times more tightly than oxygen, so less oxygen reaches the tissues.',
           '<b>Oriented to person only:</b> both apply. Confusion can come from hypoxemia caused by airway and '
           'lung injury, and from tissue hypoxia caused by CO.',
           '<b>SpO<sub>2</sub> 98%:</b> falsely reassuring. A standard pulse oximeter cannot tell '
           'carboxyhemoglobin from oxyhemoglobin and counts both as saturated. The carboxyhemoglobin (COHb) '
           'level on the blood gas drawn at 0320 (pending) is needed.',
           '<b>HR 122 beats/min with BP 104/66 mm Hg:</b> burns over 20% TBSA trigger a systemic inflammatory '
           'response. Plasma leaks out of the capillaries, intravascular volume falls, and hypovolemic (burn) '
           'shock can follow. Tachycardia with a narrowing pulse pressure is compensation. Pain and anxiety '
           'contribute, but with a burn this large, volume loss is the main cause.',
           '<b>Hematocrit 53%:</b> hemoconcentration. Plasma leaves the vessels while red cells stay, so the '
           'hematocrit rises as intravascular volume falls. Hemoglobin and hematocrit are monitored for fluid '
           'status.'),
        beyond('CO physiology and pulse oximetry are standard content.'),
    ]),
    (C6, 2): ''.join([
        p('<b>Correct answer:</b> The client is at highest risk for <b>airway obstruction from upper airway '
          'edema</b> as evidenced by <b>the hoarse voice and black-tinged sputum</b>. Once this is addressed, '
          "the nurse should next focus on the client's risk for <b>hypovolemic shock</b> as evidenced by <b>HR "
          '122 beats/min, BP 104/66 mm Hg, and hematocrit 0.53 L/L</b>.'),
        figure('u5c6-abcde.svg', "ABCDE table applied to this client's findings",
               "ABCDE applied to D.R.: the airway comes first, circulation (burn shock) second."),
        head('Why'),
        ul('<b>Airway first:</b> the nurse prioritizes with ABCDE; for burns, airway, breathing and circulation '
           'come first, followed by fluid resuscitation. After smoke inhalation, impaired gas exchange takes '
           'priority over impaired skin integrity. Upper-airway edema worsens over hours, so recognizing it '
           'early allows a controlled intubation before the airway is lost.',
           '<b>Circulation next:</b> with about 27% TBSA of partial- and full-thickness burns, large fluid shifts '
           'are expected. Tachycardia, a low-normal blood pressure and hemoconcentration show the volume loss; '
           'IV access and fluid resuscitation are the top priorities after the airway.'),
        head('Why the other choices are lower priority'),
        ul('<b>Wound infection</b> develops over days, not in the first hours.',
           '<b>Hypothermia</b> (Exposure in ABCDE) is a real risk, but it is managed after airway, breathing and '
           'circulation.',
           '<b>Compartment syndrome of the right arm</b> threatens a limb and needs frequent checks, but a threat '
           'to the airway threatens life.',
           '<b>Impaired skin integrity, acute pain and disturbed body image</b> are real needs, but none outranks '
           'the airway or circulation. Impaired skin integrity is the usual priority for smaller burns; it is '
           'displaced when the airway, breathing or circulation is at risk.',
           '<b>The other evidence</b> (temperature 36.3° C, WBC 11.2 × 10<sup>9</sup>/L, blistered trunk, pain '
           '9/10, potassium 5.3 mmol/L from cell damage) needs monitoring but does not point to the most urgent '
           'risk.'),
    ]),
    (C6, 3): ''.join([
        p('<b>Correct answer:</b> 27%; 8,640 mL; 4,320 mL; timed from 0215 (time of injury); at least '
          '40 mL/h.'),
        figure('u5c6-rule-of-nines.svg', "Rule of Nines body chart, front and back, with this client's burns shaded",
               'Rule of Nines: only the partial- and full-thickness burns count.'),
        head('Step 1: the percentage of TBSA'),
        ul('Anterior trunk (chest and abdomen) 18% + the whole right arm, front 4.5% and back 4.5% = <b>27%</b>.',
           'The face is a superficial (first-degree) burn: red, dry, no blisters. Superficial burns are '
           '<b>not</b> counted in resuscitation calculations; adding the face gives the 31.5% distractor, and '
           '18% leaves out the arm.'),
        figure('u5c6-burn-depth.svg', 'Cross-section of skin showing superficial, partial-thickness and full-thickness burn depths',
               "Burn depth decides what counts: D.R.'s face, chest and abdomen, and right arm."),
        head('Step 2: the volumes and the clock'),
        ul('<b>8,640 mL:</b> Parkland formula, 4 mL × 80 kg × 27 = 8,640 mL of Ringer\'s lactate over 24 hours.',
           '<b>4,320 mL:</b> half is given in the first 8 hours; the other 4,320 mL over the next 16 hours.',
           '<b>Timed from 0215:</b> the 8-hour clock starts at the time of the burn, not at arrival, when the IV '
           'is started or when the order is written. The first half must be in by 1015; because time has '
           'already passed, the hourly rate must make up for it.',
           '<b>At least 40 mL/h:</b> the adult target is about 0.5 mL/kg/h (0.5 × 80 kg). Urine output is the '
           'key guide for titrating the infusion. Output well above 1 mL/kg/h (for example 100 to 160 mL/h) '
           'suggests over-resuscitation, which worsens edema.'),
        figure('u5c6-parkland-timeline.svg', 'Timeline from 0215 showing 4,320 mL in the first 8 hours and 4,320 mL over the next 16 hours',
               'The first half is due by 1015, 8 hours after the burn, whatever time the infusion starts.'),
        beyond('the Parkland formula and urine-output targets are standard burn-care practice (Parkland/Baxter; '
               'American Burn Association guidance, where current protocols often start at 2 to 4 mL/kg/%TBSA '
               'and titrate to urine output). The Rule of Nines is from the chapter.'),
    ]),
    (C6, 4): ''.join([
        head('Correct answers'),
        ul('<b>Indicated:</b> notify the provider immediately about the right-hand findings; remove the ring and '
           'watch; elevate the right arm above the heart; continue 100% oxygen by non-rebreather mask; cover the '
           'burns with clean, dry dressings or sheets and keep the room warm.',
           '<b>Contraindicated:</b> a snug elastic compression wrap; morphine intramuscularly; ice packs on the '
           'chest; sips of an electrolyte drink.',
           '<b>Nonessential:</b> teaching active range-of-motion exercises for the right hand.'),
        figure('u5c6-escharotomy.svg', 'Cross-sections of a burned arm showing stiff eschar, swelling underneath, and escharotomy incisions',
               'A circumferential full-thickness burn: the stiff eschar cannot stretch as the tissue swells.'),
        head('Why'),
        ul('<b>Notify the provider (indicated):</b> cool, pale fingers, capillary refill of 5 seconds, a faint '
           'pulse, numbness and tingling, and a tense forearm under a circumferential full-thickness burn signal '
           'impending compartment syndrome. The expected treatment is an escharotomy, an incision through the '
           'inelastic eschar.',
           '<b>Remove the ring and watch (indicated):</b> clothing and jewelry near the burn are removed; once '
           'edema develops, a ring or watch acts as a tourniquet.',
           '<b>Elevate the arm (indicated):</b> elevation above heart level limits edema formation.',
           '<b>Compression wrap (contraindicated):</b> anything constricting raises the compartment pressure that '
           'is already compromising perfusion.',
           '<b>100% oxygen (indicated):</b> the COHb of 19% confirms CO poisoning. High-flow oxygen shortens the '
           'half-life of carboxyhemoglobin (from about 4 to 6 hours on room air to about 1 to 1½ hours) and '
           'continues until the airway is secured and the COHb falls.',
           '<b>IM morphine (contraindicated):</b> during burn shock, muscle perfusion is poor, so IM absorption is '
           'unreliable: little early relief, then possible delayed, excessive absorption once perfusion returns. '
           'Opioids are given IV, as ordered.',
           '<b>Ice packs (contraindicated):</b> ice causes vasoconstriction that can deepen the injury, and over a '
           '27% TBSA burn it promotes hypothermia. Burns are cooled with room-temperature water or saline to stop '
           'the burning process, not with ice.',
           '<b>Electrolyte drink (contraindicated):</b> the client is NPO with a nasogastric tube ordered; '
           'intubation is imminent, and large burns commonly cause paralytic ileus. Resuscitation is IV.',
           '<b>Range-of-motion teaching (nonessential now):</b> important later, when physical and occupational '
           'therapy prevent contractures, but not during an airway emergency with a compromised arm.',
           '<b>Clean, dry coverage and a warm room (indicated):</b> protects the wounds from contamination and '
           'limits heat loss; hypothermia is a complication of severe burns.'),
        figure('burn-full-thickness-foot.jpg', 'Photograph of a full-thickness burn with dry, leathery, yellow-white eschar',
               'A full-thickness (third-degree) burn: dry, leathery eschar that does not blanch and has no '
               'sensation. Around a whole limb, this stiff eschar acts like a tourniquet as the tissue beneath '
               'swells.'),
        beyond('limb elevation, the CO half-life figures and IM absorption in shock are standard content.'),
    ]),
    (C6, 5): ''.join([
        head('Correct answers'),
        ul('<b>Effective:</b> urine output averaging 55 mL/h; right hand warm with capillary refill of 2 seconds '
           'and pulse 2+; SpO<sub>2</sub> 96% on 2 L/min with clear lungs and full sentences; pain 3/10 during the '
           'dressing change.',
           '<b>Not effective:</b> green-yellow, foul-smelling drainage with redness 2 cm beyond the wound edge; '
           'temperature 38.9° C with WBC 17.4 × 10<sup>9</sup>/L.'),
        head('Why'),
        ul('<b>Urine output 55 mL/h:</b> above the 40 mL/h (0.5 mL/kg/h) target, showing adequate renal '
           'perfusion after resuscitation.',
           '<b>Warm hand, brisk refill, palpable pulse:</b> meets the outcome of no signs of compartment syndrome '
           '(no swelling, no decreased pulses) after the escharotomy.',
           '<b>SpO<sub>2</sub> 96%, clear lungs, full sentences:</b> gas exchange and airway patency are restored '
           'after extubation.',
           '<b>Pain 3/10 during the dressing change:</b> analgesia given at least 30 minutes before burn care '
           'keeps pain tolerable before, during and after dressing changes.',
           '<b>Purulent, foul drainage with spreading redness:</b> yellow or green, foul-smelling drainage and '
           'increasing erythema are signs of burn-wound infection. The nurse notifies the provider (a wound '
           'culture and antimicrobials are likely).',
           '<b>Fever with WBC 17.4 × 10<sup>9</sup>/L:</b> the goal is a WBC within the normal range. Fever and '
           'leukocytosis with a purulent wound suggest infection and possible sepsis, so the nurse escalates '
           'promptly.'),
    ]),

    # ---------------- Case Study 7: herpes zoster ophthalmicus
    (C7, 0): ''.join([
        p(f'<b>Correct answers:</b> the vesicle on the tip of the nose {o7(0, 0)}, the left-eye redness, '
          f'sensitivity to light and blurred vision {o7(0, 1)}, methotrexate and prednisone {o7(0, 3)}, daytime '
          f'care of her 4-month-old grandson {o7(0, 4)}, and pain 8/10 that is worse with light touch {o7(0, 5)}.'),
        figure('zoster-ophthalmicus-face.jpg', 'Photograph of herpes zoster on one side of the forehead and upper eyelid',
               'Herpes zoster ophthalmicus (here in a child): vesicles and crusts over one side of the forehead '
               'and scalp with a swollen upper eyelid, stopping at the midline.'),
        head('Why these need immediate follow-up'),
        ul(f'<b>Vesicle on the tip of the nose {o7(0, 0)}:</b> the Hutchinson sign. The nasociliary branch of '
           'the ophthalmic (V1) division of the trigeminal nerve supplies both the tip of the nose and the eye, '
           'so eye involvement is likely. The provider is informed immediately of any facial lesion, especially '
           'near the eye or ear.',
           f'<b>Red eye, photophobia, blurred vision {o7(0, 1)}:</b> signs of ocular involvement (conjunctivitis, '
           'keratitis, uveitis) that can threaten sight and need urgent ophthalmology assessment.',
           f'<b>Methotrexate and prednisone {o7(0, 3)}:</b> immunosuppression raises the risk of severe, '
           'prolonged or disseminated zoster. It changes the treatment setting (IV antiviral), the isolation '
           'needed and the monitoring.',
           f'<b>Cares for a 4-month-old {o7(0, 4)}:</b> the infant is too young for varicella vaccination and '
           'could develop chickenpox from contact with lesion fluid. This needs immediate teaching and exposure '
           'planning.',
           f'<b>Pain 8/10 with allodynia {o7(0, 5)}:</b> zoster pain is often moderate to severe. Severe acute '
           'pain needs prompt treatment and is linked to a higher risk of postherpetic neuralgia.'),
        head('Why the others do not'),
        ul(f'<b>Lesions stop at the midline {o7(0, 2)} and grouped vesicles on a red base {o7(0, 8)}:</b> '
           'expected features of zoster: vesicular, dermatomal, on one side, never crossing the midline.',
           f'<b>Childhood chickenpox {o7(0, 6)}:</b> explains why zoster occurred (reactivation of latent '
           'varicella-zoster virus); no immediate action.',
           f'<b>Temperature 37.9° C {o7(0, 7)}:</b> low-grade fever and malaise fit the viral prodrome; continue '
           'to monitor.',
           f'<b>BP 146/84 mm Hg {o7(0, 9)}:</b> mildly elevated, likely from pain and stress; recheck after the '
           'pain is treated.'),
    ]),
    (C7, 1): ''.join([
        head('Correct answers'),
        ul('<b>Expected manifestation:</b> burning, tingling pain for 3 days before the rash; lesions limited to '
           'one side, stopping at the midline; low-grade fever and fatigue.',
           '<b>Suggests ocular involvement:</b> vesicle on the tip of the nose; photophobia and blurred vision in '
           'the left eye.',
           '<b>Increases the risk of severe disease:</b> daily prednisone and weekly methotrexate; age 72.'),
        figure('u5c7-trigeminal-hutchinson.svg', 'Face diagram with the V1, V2 and V3 trigeminal dermatomes on the left side and vesicles in V1 including the nose tip',
               "The three divisions of the trigeminal nerve. L.T.'s rash (forehead, scalp, upper eyelid, nose tip) "
               'is V1, the division that also supplies the eye.'),
        head('Why'),
        ul('<b>Prodromal burning pain:</b> a burning or tingling sensation where the rash appears several days '
           'later is the typical prodrome.',
           '<b>One side, stopping at the midline:</b> zoster follows a single dermatome (the area supplied by one '
           'nerve root) and does not cross the midline.',
           '<b>Low-grade fever and fatigue:</b> part of the prodrome (feeling unwell, fever).',
           '<b>Vesicle on the nose tip:</b> the Hutchinson sign. The nasociliary nerve supplies both the nose tip '
           'and the eye, so this strongly predicts eye involvement.',
           '<b>Photophobia and blurred vision:</b> suggest corneal or intraocular inflammation.',
           '<b>Prednisone and methotrexate:</b> suppress the cell-mediated immunity that normally keeps the virus '
           'dormant, raising the risk of dissemination and prolonged viral shedding.',
           '<b>Age 72:</b> zoster most often affects older adults, and age raises the risk of complications, '
           'including postherpetic neuralgia.'),
        figure('zoster-chest-dermatome.jpg', 'Photograph of herpes zoster in a band on one side of the chest',
               'The same pattern on the trunk: clusters of vesicles on a red base in a band along one dermatome, on '
               'one side only.'),
        beyond('the Hutchinson sign and the immunosuppression risk are standard content.'),
    ]),
    (C7, 2): ''.join([
        p("<b>Correct answer:</b> The nurse's priority is to prevent <b>permanent vision loss</b> because <b>the "
          'virus is affecting the ophthalmic division of the trigeminal nerve</b>. The nurse\'s immediate action '
          'should be to <b>notify the provider immediately so that urgent ophthalmology assessment can be '
          "arranged</b>. The nurse also recognizes the client's <b>acute pain</b> as a concurrent priority."),
        figure('u5c7-eye-risk.svg', 'Diagram of the eye labelling cornea, iris and uvea, conjunctiva, retina and optic nerve with zoster complications',
               'What herpes zoster ophthalmicus can damage, and the symptoms L.T. already has.'),
        head('Why'),
        ul('<b>Permanent vision loss:</b> herpes zoster ophthalmicus can cause keratitis, uveitis, glaucoma and '
           'vision loss. A threat of permanent loss of function takes priority over skin integrity; zoster on '
           'facial dermatomes can affect eyesight and hearing.',
           '<b>Ophthalmic (V1) division:</b> the forehead, scalp, upper eyelid and nose-tip lesions map to V1, '
           'which explains why the eye is at risk.',
           '<b>Notify the provider immediately:</b> facial lesions near the eye or ear are reported at once. '
           'Putting ointment in or near the eye or applying warm compresses without a prescription is outside the '
           "nurse's scope and could cause harm; waiting a week risks permanent damage.",
           '<b>Acute pain:</b> pain rated 8/10 with allodynia must be treated promptly; adequate pain control is a '
           'recognized priority in zoster care.'),
        head('Why the other choices do not fit'),
        ul('Secondary skin infection, scarring and hyperglycemia are possible later problems but not the most '
           'urgent threat. Her age, the vesicles and childhood chickenpox do not explain why the eye is at risk. '
           'Fluid volume excess, impaired gas exchange and hypothermia are not supported by the data.'),
        figure('zoster-cornea-fluorescein.jpg', 'Photograph of an eye stained with fluorescein under cobalt-blue light',
               'Eye involvement in herpes zoster ophthalmicus: fluorescein dye under cobalt-blue light shows damage '
               'to the corneal surface (keratitis). Only an eye examination can find this, hence the urgent '
               'referral.'),
    ]),
    (C7, 3): ''.join([
        p(f'<b>Correct answers:</b> airborne infection isolation room with airborne and contact precautions '
          f'{o7(3, 0)}, staff with documented immunity to varicella {o7(3, 1)}, acyclovir over at least 1 hour '
          f'with hydration and strict intake and output {o7(3, 2)}, left-eye assessment each shift {o7(3, 3)}, '
          f'and daily serum creatinine {o7(3, 4)}.'),
        figure('u5c7-acyclovir-kidney.svg', 'Diagram of acyclovir crystals blocking a kidney tubule, and a nursing safety checklist',
               'IV acyclovir can crystallize in the kidney tubules; slow infusion and good hydration prevent it.'),
        head('Why these five'),
        ul(f'<b>Airborne and contact precautions {o7(3, 0)}:</b> for localized zoster in an immunocompromised '
           'client, isolation guidance calls for airborne and contact precautions until disseminated infection '
           'is ruled out (matches the provider\'s order).',
           f'<b>Immune staff {o7(3, 1)}:</b> varicella-zoster virus spreads to people who are not immune; '
           'non-immune or pregnant staff should not provide care.',
           f'<b>Slow acyclovir infusion, hydration, intake and output {o7(3, 2)}:</b> IV acyclovir can precipitate '
           'as crystals in the renal tubules and cause acute kidney injury, especially with rapid infusion or '
           'dehydration.',
           f'<b>Eye assessment {o7(3, 3)}:</b> follows from the priority of preventing vision loss; worsening '
           'vision is reported promptly to ophthalmology.',
           f'<b>Daily creatinine {o7(3, 4)}:</b> detects acyclovir-related kidney injury early.'),
        head('Why not the others'),
        ul(f'<b>Baby visits with gown and gloves {o7(3, 5)}:</b> the 4-month-old is unvaccinated against '
           'varicella and the client is on airborne precautions; a gown and gloves do not protect the infant.',
           f'<b>Opening intact vesicles {o7(3, 6)}:</b> increases the risk of secondary bacterial infection and '
           'scarring.',
           f'<b>Mupirocin in the eye {o7(3, 7)}:</b> the order is for skin lesions only. Only ophthalmic '
           'preparations go in the eye.',
           f'<b>Holding prednisone {o7(3, 8)}:</b> stopping long-term corticosteroids abruptly risks adrenal '
           "insufficiency; the provider continued it, and any change needs a prescriber's order.",
           f'<b>Shingles vaccine now {o7(3, 9)}:</b> the vaccine prevents future episodes; it does not treat '
           'active zoster. Vaccination is discussed after recovery.'),
        beyond('isolation details follow CDC and Public Health Agency of Canada guidance; acyclovir nephrotoxicity '
               'is standard pharmacology.'),
    ]),
    (C7, 4): ''.join([
        p("<b>Correct answer:</b> Before entering the client's room, the nurse performs hand hygiene and dons a "
          "gown, gloves, and a <b>fit-tested N95 respirator</b>. The door to the client's room must remain "
          '<b>closed</b>. Before the client is transported to the eye clinic for her slit-lamp examination, the '
          'nurse places <b>a surgical mask on the client</b> and prepares her by <b>covering the skin lesions with '
          'a clean dressing</b>. After administering the prescribed oxycodone for pain rated 8/10, the nurse plans '
          'to <b>reassess pain within 60 minutes</b>.'),
        figure('u5c7-airborne-precautions.svg', 'Diagram of an airborne infection isolation room with a closed door, a nurse in N95 respirator, gown and gloves, and transport steps',
               'Airborne and contact precautions for L.T. until disseminated zoster is ruled out.'),
        head('Why'),
        ul('<b>Fit-tested N95 respirator:</b> airborne precautions require an N95 (or higher) respirator; a '
           'surgical mask does not filter airborne particles adequately.',
           '<b>Door closed:</b> an airborne infection isolation room keeps its negative pressure only while the '
           'door is closed. Leaving it open for observation defeats the room.',
           '<b>Surgical mask on the client:</b> during essential transport, the client wears a surgical mask to '
           'contain her respiratory secretions. An N95 is not placed on a client: it is designed to protect the '
           'wearer, and some have an exhalation valve.',
           '<b>Covering the skin lesions:</b> limits contact and airborne spread from vesicle fluid. Mupirocin '
           'is for skin lesions only, never the eye.',
           '<b>Reassess pain within 60 minutes:</b> reassessing within the drug\'s peak time (about 30 to 60 '
           'minutes for oral opioids, per agency policy) evaluates pain relief and sedation. Waiting until the '
           'next dose leaves uncontrolled pain unnoticed.'),
        beyond('transmission-based precaution details follow the CDC 2007 Guideline for Isolation Precautions; '
               'Public Health Agency of Canada guidance is consistent.'),
    ]),
    (C7, 5): ''.join([
        p('<b>Highlight these three findings:</b> serum creatinine 163 µmol/L (admission 78 µmol/L); intake '
          "1,600 mL with urine output 380 mL; and the statement “Once the scabs are gone, any burning that's "
          "left doesn't mean anything, so I won't bother anyone about it.”"),
        figure('u5c7-creatinine-trend.svg', 'Bar charts of creatinine rising from 78 to 163 micromoles per litre and urine output of 380 mL against at least 720 mL expected',
               'Hospital day 4: creatinine has more than doubled and the urine output is far below what her '
               'intake should produce.'),
        head('Why these need follow-up'),
        ul('<b>Creatinine more than doubled:</b> suggests acyclovir-associated acute kidney injury. The nurse '
           'notifies the provider promptly; the dose may need adjusting and hydration reviewed.',
           '<b>Urine output 380 mL in 24 hours:</b> oliguria (under about 400 mL/24 h, or under 0.5 mL/kg/h; '
           'for a 60-kg client, at least 720 mL/24 h is expected) despite an adequate intake supports kidney '
           'injury.',
           '<b>"Any burning that\'s left doesn\'t mean anything":</b> pain that persists after the rash heals may '
           'be postherpetic neuralgia, a treatable neurological complication that should be reported. The '
           'teaching needs reinforcing.'),
        head('Why the others show expected progress'),
        ul('Temperature 37.0° C, all lesions crusted with no new lesions, pain 3/10 and a stable eye: afebrile, '
           'no dissemination, pain controlled. Once all lesions are crusted, she is no longer considered '
           'infectious.',
           'Capillary glucose 7.4 mmol/L: acceptable for a client with diabetes taking prednisone.',
           'The vaccine and hand-hygiene statements are accurate. The recombinant (non-live) zoster vaccine is '
           'recommended after recovery, including for people who are immunocompromised (NACI; CDC).'),
        beyond('acyclovir nephrotoxicity and the vaccine recommendations are standard references.'),
    ]),

    # ---------------- Case Study 8: plaque psoriasis progressing to erythroderma
    (C8, 0): ''.join([
        p('<b>Highlight these nine findings:</b> temperature 35.6° C; heart rate 116/min; blood pressure 96/58 '
          'lying and 80/50 mm Hg standing with dizziness; 100 mL of dark amber urine in 8 hours; erythema with '
          'scaling over about 90% of the body; potassium 3.1 mmol/L; magnesium 0.62 mmol/L; creatinine 132 '
          'µmol/L (84 three months ago); albumin 26 g/L.'),
        figure('erythroderma.jpg', 'Photograph of generalized erythroderma',
               'Generalized exfoliative dermatitis (erythroderma), from a historical atlas: redness and scaling '
               'over almost the whole body surface.'),
        head('Why these findings'),
        ul('<b>Temperature 35.6° C:</b> impaired thermoregulation; inflamed, dilated skin over 90% of the body '
           'loses heat. The nurse monitors temperature and provides warming measures.',
           '<b>Tachycardia; hypotension with an orthostatic drop:</b> hemodynamic instability from fluid lost '
           'through the damaged skin. Hemodynamic stability is the priority in erythroderma.',
           '<b>100 mL of urine in 8 hours:</b> about 0.14 mL/kg/h in a 92-kg client: oliguria from hypovolemia.',
           '<b>Erythema over about 90% of the body:</b> meets the definition of generalized exfoliative '
           'dermatitis (erythroderma), a life-threatening condition managed in hospital.',
           '<b>Low potassium and magnesium:</b> both raise the risk of dysrhythmias and are replaced; heavy '
           'alcohol use contributes to low magnesium.',
           '<b>Creatinine up from 84 to 132 µmol/L:</b> suggests prerenal acute kidney injury from hypovolemia.',
           '<b>Albumin 26 g/L:</b> protein lost through the shedding, inflamed skin. Low oncotic pressure explains '
           'the ankle edema.'),
        head('Why the others are not urgent'),
        ul('<b>RR 18/min and SpO<sub>2</sub> 97%:</b> within normal limits.',
           '<b>Nail pitting and ridging:</b> a chronic finding of nail psoriasis.',
           '<b>ESR 48 mm/h:</b> elevated ESR is expected with psoriatic inflammation; monitor.',
           '<b>Hemoglobin 124 g/L:</b> mild anemia, which can occur in erythroderma; not immediately dangerous.',
           '<b>ALT 34 U/L:</b> normal, and a useful baseline before systemic therapy.'),
        figure('nail-pitting.jpg', 'Photograph of a fingernail with pitting from psoriasis',
               'Nail pitting in psoriasis: small depressions in the nail plate. A long-standing finding, not an '
               'emergency.'),
    ]),
    (C8, 1): ''.join([
        p("<b>Correct answer:</b> The client's hypotension and tachycardia are most likely caused by <b>fluid loss "
          'through the widely inflamed, shedding skin</b> as evidenced by <b>the orthostatic blood pressure drop, '
          'dry oral mucosa, and low, concentrated urine output</b>. His temperature of 35.6° C is most likely due '
          'to <b>heat loss through widespread, dilated skin blood vessels</b>. The bilateral ankle edema is most '
          'likely related to <b>a low serum albumin from protein loss through the skin</b>. The flare was most '
          'likely triggered by <b>stopping methotrexate, finishing a course of oral prednisone, heavy alcohol use, '
          'and stress</b>.'),
        figure('u5c8-skin-losses.svg', 'Diagram of a body with erythroderma losing water, heat, protein and electrolytes through the skin',
               "What J.M.'s skin is losing, and the findings that show it."),
        head('Why'),
        ul('<b>Fluid loss through the skin:</b> in erythroderma the skin barrier is almost completely absent, so '
           'fluid is lost continuously. The orthostatic drop, dry mucosa and low, concentrated urine confirm '
           'volume depletion. A normal SpO<sub>2</sub> and clear lungs argue against a cardiac cause, and there '
           'was no allergen exposure suggesting anaphylaxis. Nail pitting, the ESR and the SpO<sub>2</sub> do not '
           'show volume status.',
           '<b>Heat loss through dilated skin vessels:</b> inflamed, vasodilated skin over 90% of the body loses '
           'heat rapidly. He has not stopped drinking long enough for significant withdrawal, and alcohol '
           'withdrawal tends to raise temperature, not lower it.',
           '<b>Low albumin:</b> albumin 26 g/L shows protein lost through scaling and exudation. Low oncotic '
           'pressure lets fluid shift into the tissues even while he is intravascularly depleted. No IV fluids '
           'have been given yet, and nothing suggests heart failure or bilateral DVT.',
           '<b>Triggers:</b> stress and excessive alcohol are psoriasis triggers, and psoriasis is a contributing '
           'cause of erythroderma. Abruptly stopping systemic therapy and withdrawal of systemic corticosteroids '
           'are well-recognized triggers of erythrodermic flares. A streptococcal throat infection classically '
           'triggers guttate psoriasis, and detergents trigger contact dermatitis.'),
        beyond('methotrexate and corticosteroid withdrawal as triggers are standard dermatology content.'),
    ]),
    (C8, 2): ''.join([
        p('<b>Correct answer:</b> The priority nursing hypothesis at this time is <b>risk for hemodynamic '
          'instability related to fluid and electrolyte loss</b> because <b>the skin barrier is almost completely '
          "absent, allowing ongoing loss of fluid, protein, electrolytes, and heat</b>. Once this is addressed, the "
          "nurse's next priority is <b>impaired skin integrity</b>."),
        figure('u5c8-priority-shift.svg', 'Diagram comparing nursing priorities in plaque psoriasis and in erythroderma',
               'The key clinical-judgment shift in this case.'),
        head('Why'),
        ul('<b>Hemodynamic instability first:</b> for ordinary plaque psoriasis, impaired skin integrity is the '
           'priority. Once the disease becomes erythroderma, the priority shifts to hemodynamic stability because '
           'the skin barrier is almost completely absent.',
           '<b>Loss of the skin barrier:</b> this is the mechanism that makes erythroderma life-threatening. That '
           'psoriasis is autoimmune, that he stopped methotrexate and that the ESR is raised are all true, but '
           'they do not explain the immediate danger.',
           '<b>Impaired skin integrity next:</b> the next hypothesis in erythroderma. Body image, knowledge and '
           'coping are real needs (he is tearful and isolating) and are addressed once he is physiologically '
           'stable.'),
        figure('psoriasis-plaque.jpg', 'Photograph of a psoriasis plaque with silvery-white scale',
               'Typical plaque psoriasis: a well-defined red plaque with silvery-white scale, the form J.M. has had '
               'for 20 years. In erythroderma the redness and scaling cover almost the whole body.'),
    ]),
    (C8, 3): ''.join([
        p(f'<b>Correct answers:</b> IV isotonic fluids {o8(3, 0)}; potassium and magnesium replacement with '
          f'cardiac monitoring {o8(3, 1)}; warm room, warm blankets and frequent temperature checks {o8(3, 2)}; '
          f'strict intake and output and daily weight {o8(3, 3)}; lukewarm oatmeal soaks and a bland, oil-based '
          f'emollient {o8(3, 4)}; an oral antihistamine at bedtime {o8(3, 5)}; and alcohol-withdrawal monitoring '
          f'with a validated scale {o8(3, 6)}.'),
        figure('u5c8-skin-care.svg', 'Do and do-not lists for skin care in erythroderma',
               'Skin care when the barrier is gone: gentle, lukewarm, moisturizing.'),
        head('Why these'),
        ul(f'<b>IV isotonic fluids {o8(3, 0)}:</b> adequate hydration through IV fluid replacement maintains '
           'hemodynamic stability.',
           f'<b>Potassium and magnesium {o8(3, 1)}:</b> potassium, magnesium and calcium are replaced when '
           'indicated; low potassium and magnesium raise the risk of dysrhythmias, so cardiac monitoring is '
           'prudent.',
           f'<b>Warming {o8(3, 2)}:</b> frequent temperature checks with warming measures address impaired '
           'thermoregulation.',
           f'<b>Intake and output, daily weight {o8(3, 3)}:</b> track the response to fluid replacement and '
           'ongoing losses.',
           f'<b>Oatmeal soaks and emollient {o8(3, 4)}:</b> oatmeal baths soothe erythroderma and oil-based '
           'emollients help psoriasis; lukewarm water avoids more vasodilation and heat loss.',
           f'<b>Bedtime antihistamine {o8(3, 5)}:</b> oral antihistamines (for example diphenhydramine) relieve '
           'itching; bedtime dosing uses the sedating effect. Supervise getting up because of the orthostatic '
           'hypotension.',
           f'<b>Alcohol-withdrawal monitoring {o8(3, 6)}:</b> he drinks 6 to 8 beers a day; withdrawal can begin '
           '6 to 24 hours after the last drink and would worsen his hemodynamic instability.'),
        head('Why not the others'),
        ul(f'<b>Fluid restriction {o8(3, 7)}:</b> the edema comes from low albumin while he is intravascularly '
           'depleted; restricting fluids would worsen the hypotension and kidney injury.',
           f'<b>Coal tar on all reddened skin {o8(3, 8)}:</b> coal tar treats mild, localized psoriasis. On '
           'inflamed, broken skin over 90% of the body it irritates and can worsen erythroderma.',
           f'<b>Phototherapy {o8(3, 9)}:</b> used for stable psoriasis; ultraviolet light on acutely inflamed skin '
           'can aggravate erythroderma, and he is unstable.',
           f'<b>Hot water and scrubbing {o8(3, 10)}:</b> friction and heat further damage the fragile barrier, '
           'increase heat and fluid loss, and invite infection.'),
        beyond('alcohol-withdrawal monitoring and the coal tar contraindication in erythroderma are standard '
               'content.'),
    ]),
    (C8, 4): ''.join([
        head('Correct answers'),
        ul('<b>Indicated:</b> confirm the TB and hepatitis screening before the first infusion; monitor vital signs '
           'and watch for an infusion reaction; teach him to report fever, cough, night sweats or skin infection; '
           'refer to a social worker and a psoriasis support group or counselling; teach stress reduction and '
           'support his plan to cut down on alcohol.',
           '<b>Contraindicated:</b> advising overdue live vaccines now; explaining that infusions can stop once the '
           'skin clears; encouraging long, hot showers.'),
        figure('u5c8-infliximab-checklist.svg', 'Checklist for before, during and after an infliximab infusion',
               'Infliximab, a TNF inhibitor: what the nurse checks and teaches.'),
        head('Why'),
        ul('<b>TB and hepatitis screening:</b> with systemic and biologic therapy (infliximab is one), the nurse '
           'monitors for serious infections such as tuberculosis and hepatitis. TNF inhibitors can reactivate '
           'latent TB and hepatitis B, so negative screening is confirmed first.',
           '<b>Infusion reaction:</b> infliximab can cause fever, chills, dyspnea, hives or hypotension during or '
           'after the infusion.',
           '<b>Infection warning signs:</b> suppressed immunity makes infection more likely.',
           '<b>Live vaccines (contraindicated):</b> live vaccines are avoided during biologic immunosuppression; '
           'needed vaccines are given before therapy starts, per the prescriber.',
           '<b>Stopping once the skin clears (contraindicated):</b> psoriasis is chronic, with remissions and '
           'relapses; the nurse reinforces adherence. Stopping therapy is what caused this admission.',
           '<b>Social work and support group:</b> address the root cause of his non-adherence (lost drug coverage) '
           'and the psychosocial impact of his skin disease.',
           '<b>Stress and alcohol reduction:</b> stress and excessive alcohol are psoriasis triggers.',
           '<b>Long, hot showers (contraindicated):</b> heat and prolonged water exposure dry and irritate the skin '
           'and promote heat and fluid loss; lukewarm soaks followed by emollients are used instead.'),
        beyond('infusion reactions and live-vaccine precautions are standard pharmacology.'),
    ]),
    (C8, 5): ''.join([
        head('Correct answers'),
        ul('<b>Effective:</b> BP 124/78 mm Hg and HR 82 beats/min with no orthostatic change; temperature '
           '36.8° C; potassium 4.1 and magnesium 0.84 mmol/L; erythema down to about 40% with less peeling and '
           'itch 3/10; alcohol-withdrawal scores 0 to 2.',
           '<b>Not effective:</b> the honey-coloured crust with redness and warmth on the right shin; the plan to '
           'skip the next infusion.'),
        figure('impetigo-honey-crust.jpg', 'Photograph of honey-coloured crusts of impetigo on the chin',
               'Honey-coloured crusts: the typical look of impetigo, a superficial bacterial skin infection '
               '(Staphylococcus aureus or Streptococcus pyogenes). The same crust on J.M.\'s excoriation, with '
               'redness and warmth, signals secondary infection.'),
        head('Why'),
        ul('<b>Stable BP and HR:</b> meets the outcome of vital signs within normal limits without fluid '
           'imbalance.',
           '<b>Temperature 36.8° C:</b> thermoregulation restored.',
           '<b>Normal potassium and magnesium:</b> no electrolyte disturbance.',
           '<b>Less erythema, peeling and itch:</b> the skin is beginning to heal.',
           '<b>Honey-coloured crust with redness and warmth:</b> a classic sign of secondary bacterial infection; '
           'yellow crusts over excoriations signal infection. The nurse notifies the provider (topical mupirocin '
           'is commonly prescribed); infection risk is higher on a biologic.',
           '<b>Withdrawal scores 0 to 2:</b> withdrawal was prevented or managed.',
           '<b>"I\'ll just skip the next infusion":</b> the adherence teaching has not been understood. The nurse '
           'evaluates the education and reinforces continuing treatment.'),
    ]),
}

HIGHLIGHT_SPLIT = (
    C6, 0,
    '{Oriented to person only; unsure of the time or place. Reports headache and nausea.|correct}',
    '{Oriented to person only; unsure of the time or place.|correct} Reports headache and nausea.',
)


def reorder(lst, order):
    assert sorted(order) == list(range(len(lst))), order
    return [lst[i] for i in order]


def main():
    cases, _ = bank.load()
    by_id = {c['id']: c for c in cases}
    entries = []

    def add(case_id, path, before, after):
        if before != after:
            entries.append({'row': 'cases', 'id': case_id, 'path': path, 'before': before, 'after': after})

    for (cid, s), order in OPTION_ORDER.items():
        q = by_id[cid]['screens'][s]['question']
        new = reorder(q['options'], order)
        assert not new[0]['correct'], (cid, s)
        add(cid, ['screens', s, 'question', 'options'], q['options'], new)

    for (cid, s), orders in DROPDOWN_ORDER.items():
        q = by_id[cid]['screens'][s]['question']
        for b, order in enumerate(orders):
            if order is None:
                continue
            opts = q['cloze']['dropdowns'][b]['options']
            new = reorder(opts, order)
            assert not new[0]['correct'], (cid, s, b)
            add(cid, ['screens', s, 'question', 'cloze', 'dropdowns', b, 'options'], opts, new)

    for (cid, s), order in WORD_BANK_ORDER.items():
        q = by_id[cid]['screens'][s]['question']
        for b, dd in enumerate(q['cloze']['dropdowns']):
            new = reorder(dd['options'], order)
            add(cid, ['screens', s, 'question', 'cloze', 'dropdowns', b, 'options'], dd['options'], new)
        bank_words = [o['text'] for o in reorder(q['cloze']['dropdowns'][0]['options'], order)]
        answers = [next(o['text'] for o in dd['options'] if o['correct']) for dd in q['cloze']['dropdowns']]
        assert bank_words[0] not in answers[:1], 'first word in the bank answers blank 1'

    cid, s, old, new = HIGHLIGHT_SPLIT
    tab = by_id[cid]['screens'][s]['question']['highlightTabs'][0]
    assert tab['content'].count(old) == 1
    add(cid, ['screens', s, 'question', 'highlightTabs', 0, 'content'], tab['content'], tab['content'].replace(old, new))

    for (cid, s), text in RATIONALES.items():
        q = by_id[cid]['screens'][s]['question']
        assert '\n' not in text
        for src in re.findall(r'src="([^"]+)"', text):
            assert os.path.exists(os.path.join(HERE, '..', src)), f'missing image {src}'
        add(cid, ['screens', s, 'question', 'explanation'], q.get('explanation'), text)

    out = os.path.join(HERE, 'integ_rationales_patch.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=1)
    print(f'{len(entries)} changes written to {os.path.relpath(out)}')


if __name__ == '__main__':
    main()
