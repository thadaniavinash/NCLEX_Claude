"""Content fixes for the case studies (September 2026), applied with `tools/supabase.js patch`.

1. Question preambles. The player no longer marks chart tabs as New/Updated (the real NCLEX does not),
   so each case-study screen whose chart gained a tab or new entries says so in its preamble, e.g.
   "The nurse has reviewed the Nurses' Notes from 1130 and the Diagnostic Results." The sentence goes
   after any existing preamble text (whose "(see ... tab)" pointers are dropped as redundant).
   First screens, unchanged charts and preambles already written this way are left alone.
2. Chart and wording errors found while checking (see FIXES below).
3. HTML codes such as "&times;" typed into fields the player shows as plain text (option, matrix row
   and drop-down choice text) become the characters themselves.

Writes drafts/content_patch.json: [{row, id, title, path, before, after, why}]. tools/supabase.js patch
refuses the whole patch if any field no longer holds `before`, so edits made since are never lost.
"""
import html
import json
import os
import re
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
        6: R + 'Hospital Day 4 Flowsheet.',  # a highlight question: its own tab is the chart shown
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


SEE_TAB = re.compile(r'\s*\(see [^()]*?tab\)', re.I)
# Existing preambles whose wording needs the sentence placed inside rather than after.
REWORDED = {
    ('case_1781534070850', 2): 'On Tuesday morning, the campus clinic nurse reviews the clinic log and contacts the residence. '
                               'The nurse has reviewed the Epidemiologic Data. The cause of the illness has not been confirmed.',
}
ENTITY = re.compile(r'&(times|ge|le|deg|plusmn|micro|mdash|ndash|rarr|asymp|ne|nbsp);')
PLAIN_TEXT_KEYS = {'text', 'columns', 'firstColumnHeader', 'placeholder'}


def note_row(time, text):
    return (f'<p class="nurse-note-row"><span class="nurse-note-time">{time}:</span>'
            f'<span class="nurse-note-text">{text}</span></p>')


def tab_index(screen, title):
    return next(i for i, t in enumerate(screen['leftContent']['tabs']) if t['title'] == title)


def build():
    cases, standalone = bank.load()
    by_id = {c['id']: c for c in cases}
    patch = []

    def add(item, path, after, why, row='cases'):
        node = item
        for k in path:
            node = node[k] if not isinstance(node, dict) or k in node else None
            if node is None:
                break
        before = node
        if before == after:
            return
        patch.append({'row': row, 'id': item['id'], 'title': item['title'], 'path': path,
                      'before': before, 'after': after, 'why': why})

    # 1. Preambles
    for cid, screens in PREAMBLES.items():
        item = by_id[cid]
        for n, sentence in screens.items():
            before = item['screens'][n - 1]['question'].get('preamble') or ''
            if (cid, n) in REWORDED:
                after = REWORDED[(cid, n)]
            else:
                kept = SEE_TAB.sub('', before).strip()
                after = f'{kept} {sentence}' if kept else sentence
            add(item, ['screens', n - 1, 'question', 'preamble'], after, 'preamble')

    # 2. Chart and wording errors
    # NURS 1021 Unit 6 CS1: the CT results were timed 1100/1130, before the CT scans (1230, repeat at
    # 1415); the preamble already gave 1230 and 1445. The second entry's markup was also malformed.
    u6 = by_id['case_1781741217820']
    fixed = (note_row('1230', 'Acute gangrenous appendix with calcified appendicolith.') +
             note_row('1445', 'Free intraperitoneal fluid noted consistent with a ruptured appendix.'))
    for n in (5, 6):
        i = tab_index(u6['screens'][n - 1], 'Diagnostic Results')
        add(u6, ['screens', n - 1, 'leftContent', 'tabs', i, 'content'], fixed,
            'Diagnostic Results times 1100/1130 -> 1230/1445 (after the CT scans), tidy markup')

    # Case Study 2 (DKA): tab title typo; the introduction changed mid-case to "a client in the clinic..."
    # although the client is in hospital; the highlight question's tab holds the prescriptions.
    dka = by_id['case_1780489713691']
    for n, s in enumerate(dka['screens'], 1):
        for i, t in enumerate(s['leftContent']['tabs']):
            if t['title'] == "Nurses's Notes":
                add(dka, ['screens', n - 1, 'leftContent', 'tabs', i, 'title'], "Nurses' Notes", 'tab title typo')
        if n > 2:
            add(dka, ['screens', n - 1, 'leftContent', 'intro'], dka['screens'][0]['leftContent']['intro'],
                'introduction matches screens 1-2')
    add(dka, ['screens', 4, 'question', 'highlightTabs', 0, 'title'], 'Prescriptions',
        'the highlight tab holds the 0905 prescriptions')

    # Case Study 1 (heart failure): tabs vanished between screens (Nurses' Notes on screen 5, Lab Results on 6).
    hf = by_id['cardio-case-1']
    s4, s5, s6 = hf['screens'][3], hf['screens'][4], hf['screens'][5]
    notes4 = s4['leftContent']['tabs'][tab_index(s4, "Nurses' Notes")]
    labs5 = s5['leftContent']['tabs'][tab_index(s5, 'Lab Results')]
    add(hf, ['screens', 4, 'leftContent', 'tabs'],
        [s5['leftContent']['tabs'][0], dict(notes4, id=notes4['id'] + '_s5'), labs5],
        "keep the Nurses' Notes tab on screen 5")
    add(hf, ['screens', 5, 'leftContent', 'tabs'],
        s6['leftContent']['tabs'] + [dict(labs5, id=labs5['id'] + '_s6')], 'keep the Lab Results tab on screen 6')

    # New Case Study (78-year-old, pneumonia/sepsis): screen 6 stem was unfinished. Its matrix columns are
    # Improved / Not Changed / Worsened (as in NURS 1021 Unit 3 Case Study 1).
    ncs = by_id['case_1782159166328']
    add(ncs, ['screens', 5, 'question', 'stem'],
        "For each assessment finding, click to specify if the finding indicates that the client's condition has improved, not changed, or worsened.",
        'unfinished stem completed to match the matrix columns')

    # 3. HTML codes in plain-text fields
    def walk(item, row, node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                walk(item, row, v, path + [k])
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(item, row, v, path + [i])
        elif isinstance(node, str) and ENTITY.search(node):
            key = next(p for p in reversed(path) if isinstance(p, str))
            if key in PLAIN_TEXT_KEYS:
                add(item, path, ENTITY.sub(lambda m: html.unescape(m.group(0)), node), 'HTML code shown as text', row)
    for c in cases:
        walk(c, 'cases', c, [])
    for q in standalone:
        walk(q, 'standalone', q, [])
    return patch


def main():
    patch = build()
    out = os.path.join(HERE, 'content_patch.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(patch, f, indent=1, ensure_ascii=False)
    kinds = {}
    for p in patch:
        k = 'preamble' if p['why'] == 'preamble' else p['why']
        kinds[k] = kinds.get(k, 0) + 1
    print(f'{len(patch)} changes in {len({p["id"] for p in patch})} items -> {out}')
    for k, n in kinds.items():
        print(f'  {n:4}  {k}')


if __name__ == '__main__':
    main()
