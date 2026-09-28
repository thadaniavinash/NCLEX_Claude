"""Question preambles that say what the nurse has reviewed since the previous screen.

The player no longer marks chart tabs as New/Updated (the real NCLEX does not), so each case-study
screen whose chart gained a tab or new entries states it in the question preamble instead, e.g.
"The nurse has reviewed the Nurses' Notes from 1130 and the Diagnostic Results."

Rule: on a screen whose chart changed, the sentence is added after any existing preamble text
('add'), or becomes the preamble when there was none ('set'). Screens that already use this form,
first screens and screens whose chart did not change are left alone. Only question.preamble changes.

Writes drafts/preamble_patch.json: [{id, title, screen (1-based), before, after}]. `before` is the
current preamble; tools/supabase.js patch-preambles refuses an entry whose preamble has changed since.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'tools'))
import bank  # noqa: E402

R = 'The nurse has reviewed the '
PREAMBLES = {
    # Case Study 1 (cardio, not yet visible to students)
    'cardio-case-1': {
        2: R + "Nurses' Notes from 0800.",
        3: R + "Nurses' Notes from 0815.",
        4: R + "Nurses' Notes from 0830.",
        5: R + 'Lab Results.',
        6: R + "Nurses' Notes from 1200.",
    },
    # Case Study 2 (DKA)
    'case_1780489713691': {
        4: R + 'Laboratory Results from 0900.',
        5: R + 'Prescriptions from 0905.',
    },
    # NURS 1017 Unit 1 Case Study 1
    'case_1781534070850': {
        2: R + 'Epidemiologic Data.',
        6: R + 'Follow-Up Data (After 7 Days).',
    },
    # NURS 1021 Unit 6 Case Study 1
    'case_1781741217820': {
        2: R + "Nurses' Notes from 1100.",
    },
    # NURS 1017 Unit 1 Case Study 2
    'case_1782350000001': {
        2: R + 'Clinical Assessment and Point-of-Care Testing.',
        6: R + 'Follow-Up Data (4 Weeks Later).',
    },
    # NURS 1017 Unit 1 Case Study 3
    'case_1782350000002': {
        2: R + 'Diagnostic and Laboratory Findings.',
        6: R + 'Follow-Up Assessment (6 Months Later).',
    },
    # NURS 1017 Unit 2 Case Studies 1-3
    'case_1782360000001': {
        2: R + 'Diagnostic Reports.',
        6: R + "Nurses' Notes from the 12-Month Follow-Up.",
    },
    'case_1782360000002': {
        2: R + 'Laboratory &amp; Pathology results.',
        6: R + "Nurses' Notes from the 4-Week Outpatient Follow-up.",
    },
    'case_1782360000003': {
        2: R + 'Laboratory &amp; Wound Assessment.',
        5: R + "Nurses' Notes from 1830 (Postoperative SICU).",
        6: R + "Nurses' Notes from Postoperative Day 4.",
    },
    # NURS 1017 Unit 3 Case Studies 1-4
    'case_1782370000001': {
        2: R + "Nurses' Notes from 1200 and the Diagnostic &amp; Genetic Reports.",
        3: R + "Nurses' Notes and Vital Signs from 1400 (DOL 1).",
        4: R + "Nurses' Notes from 1600 (DOL 1) and the Cardiology Consult Note.",
        5: R + "Nurses' Notes and Vital Signs from 0800 (DOL 2).",
        6: R + "Nurses' Notes from 1100 (DOL 3) and the Discharge Summary.",
    },
    'case_1782370000002': {
        2: R + "Nurses' Notes from 1030 and the Genetic &amp; Diagnostic Reports.",
        3: R + "Nurses' Notes from 1115 and the Punnett Probability Reference.",
        4: R + "Nurses' Notes from 1300 and the Care Pathways.",
        5: R + "Nurses' Notes from 1430.",
        6: R + "Nurses' Notes from 1530.",
    },
    'case_1782370000003': {
        2: R + "Nurses' Notes from 0900 and the Diagnostic &amp; Laboratory Reports.",
        3: R + "Nurses' Notes from 1100 and the Teratology Principles Chart.",
        4: R + "Nurses' Notes from 1300 and the Clinical Pathway.",
        5: R + "Nurses' Notes from 0800 (DOL 2) and the Vital Signs.",
        6: R + "Nurses' Notes from 1400 (DOL 3) and the Interprofessional Discharge Plan.",
    },
    'case_1782370000004': {
        2: R + "Nurses' Notes from 1400, the Laboratory Results, and the Genetic Testing Report.",
        3: R + "Nurses' Notes from 1000 and the Family Genetics.",
        4: R + "Nurses' Notes from 1100 and the Care Plan Orders.",
        5: R + "Nurses' Notes and Vital Signs from 1615.",
        6: R + "Nurses' Notes from 0930 and the Follow-Up Data.",
    },
    # NURS 1017 Unit 4 Case Studies 1-5
    'case_1782380000001': {
        2: R + "Nurses' Notes from 1130 and the Diagnostic &amp; Pathology Reports.",
        3: R + "Nurses' Notes from 1300 and the Surgical Consult Plan.",
        4: R + "Nurses' Notes from 1430.",
        5: R + "Nurses' Notes and Vital Signs from 0630.",
        6: R + "Nurses' Notes from 1400 and the Operative &amp; Pathology Summary.",
    },
    'case_1782380000002': {
        2: R + "Nurses' Notes from 1330 and the Diagnostic &amp; Endoscopy Reports.",
        3: R + "Nurses' Notes from 1500.",
        4: R + "Nurses' Notes from 1600.",
        5: R + "Nurses' Notes from 1000 (Pre-Admission).",
        6: R + "Nurses' Notes from 1130.",
    },
    'case_1782380000003': {
        2: R + "Nurses' Notes from 1300 and the Diagnostic &amp; Pathology Reports.",
        3: R + "Nurses' Notes from 1430.",
        4: R + "Nurses' Notes from 1600.",
        5: R + "Nurses' Notes from 0900 (Day 2).",
        6: R + "Nurses' Notes from 1400 (Day 3).",
    },
    'case_1782380000004': {
        2: R + "Nurses' Notes from 1030 and the Laboratory Reports.",
        3: R + "Nurses' Notes from 1100.",
        4: R + "Nurses' Notes from 1300 and the Clinical Care Protocol.",
        5: R + "Nurses' Notes and Vital Signs from 0800 (Day 2).",
        6: R + "Nurses' Notes from 1100 (Day 4).",
    },
    'case_1782380000005': {
        2: R + "Nurses' Notes from 0900 and the Laboratory &amp; Endocrine Reports.",
        3: R + "Nurses' Notes from 1000.",
        4: R + "Nurses' Notes from 1200.",
        5: R + "Nurses' Notes and Vital Signs from 0800 (Day 2).",
        6: R + "Nurses' Notes from 1300 (Day 3).",
    },
    # NURS 1017 Unit 5 Case Studies 1-8
    'case_1782390000001': {
        2: R + "Nurses' Notes from 1000 and the Dermatological Reference.",
        3: R + "Nurses' Notes from 1400 (4 days post-biopsy) and the Pathology Reports.",
        4: R + "Nurses' Notes from 1500.",
        5: R + "Nurses' Notes from 1000 (Post-Op Day 2).",
        6: R + "Nurses' Notes from 1100 (Post-Op Day 10).",
    },
    'case_1782390000002': {
        2: R + "Nurses' Notes from 1045 and the Infectious Disease Matrix.",
        3: R + "Nurses' Notes from 1130.",
        4: R + "Nurses' Notes from 1215.",
        5: R + "Nurses' Notes from 1300.",
        6: R + "Nurses' Notes from 1330.",
    },
    'case_1782390000003': {
        2: R + "Nurses' Notes from 1100 and the Laboratory &amp; Serology Reports.",
        3: R + "Nurses' Notes from 1300.",
        4: R + "Nurses' Notes from 1430.",
        5: R + "Nurses' Notes from 1530.",
        6: R + "Nurses' Notes from 1600.",
    },
    'case_1782390000004': {
        2: R + "Nurses' Notes and the Burn Assessment &amp; Labs from 0915.",
        3: R + "Nurses' Notes from 0930.",
        4: R + "Nurses' Notes from 1130 (Hour 3 Post-Injury).",
        5: R + "Nurses' Notes from 1445 (Hour 6 Post-Injury) and the Resuscitation Flow Sheet.",
        6: R + "Nurses' Notes from 1500 (Hour 30 Post-Burn).",
    },
    'case_1782390000005': {
        2: R + "Nurses' Notes from 1620 and the Burn Classification Reference.",
        3: R + "Nurses' Notes from 1000 (Post-Burn Day 3) and the Wound Healing Stages Reference.",
        4: R + "Nurses' Notes from 1330.",
        5: R + "Nurses' Notes from 1600 (Post-Op Day 1 / Post-Burn Day 8).",
        6: R + "Nurses' Notes from 1100 (Post-Burn Day 21).",
    },
    'case_1782390000006': {
        2: R + "Nurses' Notes from 0305.",
        4: R + "Nurses' Notes from 0340, the Laboratory Results from 0335, and the Provider Orders from 0340.",
        6: R + 'Progress Notes from Post-injury Day 5.',
    },
    'case_1782390000007': {
        2: R + "Nurses' Notes from 1030.",
        4: R + "Nurses' Notes from 1400 and the Provider Orders.",
        6: R + "Nurses' Notes from Hospital Day 4.",
    },
    'case_1782390000008': {
        2: R + "Nurses' Notes from 2140.",
        5: R + "Nurses' Notes from Hospital Day 3 and the Screening Results.",
        6: R + "Nurses' Notes from Hospital Day 7.",
    },
    # NURS 1021 Unit 1 Case Study 1
    'case_1786010000001': {
        3: R + "Nurses' Notes from 1055.",
        4: R + "Nurses' Notes from 1152.",
        5: R + "Nurses' Notes from 0700.",
        6: R + "Nurses' Notes from 0645.",
    },
    # NURS 1021 Unit 6 Case Study 3
    'case_1786060000003': {
        3: R + "Nurses' Notes from 0815.",
        4: R + 'Laboratory Tests.',
        6: R + "Nurses' Notes and the repeat Laboratory Tests from the Medical Unit.",
    },
}


def main():
    cases, _ = bank.load()
    by_id = {c['id']: c for c in cases}
    patch = []
    for cid, screens in PREAMBLES.items():
        item = by_id[cid]
        for n, sentence in screens.items():
            before = item['screens'][n - 1]['question'].get('preamble') or ''
            text = before.strip()
            after = f'{text} {sentence}' if text else sentence
            patch.append({'id': cid, 'title': item['title'], 'screen': n, 'before': before, 'after': after})
    out = os.path.join(HERE, 'preamble_patch.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(patch, f, indent=2, ensure_ascii=False)
    print(f'{len(patch)} preambles in {len({p["id"] for p in patch})} case studies -> {out}')


if __name__ == '__main__':
    main()
