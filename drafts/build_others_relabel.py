"""Relabel the 23 "Others" case studies by course and unit (user request, 14 October 2026).

Labels follow the case study inventory (artifact "NGN Case Study Inventory"): each case goes to the
course and unit that fits its topic best; `topic` and `disorder` equal `unit`, as everywhere else.

Visibility, following the user's rule "make it available if there are no problems":
- University of Maryland CS2 (Tuberculosis) is shown to students: its only open review note
  (drafts/umd_review/CS02.json, isoniazid dose) is about an untested order already set to 300 mg.
- CS3-CS21 stay hidden: each has at least one open review note on an answer key or on content that
  conflicts with current practice (drafts/umd_review/CS<nn>.json).
- "New Case Study" and "NCSBN Case Study 2" are hidden (draft: true): they repeat NURS 1021 Unit 3
  Case Study 1 and NURS 1021 Unit 6 Case Study 2, so after relabelling students would meet each twice.
- "Case Study 1" (heart failure) is still not ready (a blank drop-down option on screen 3).

Writes drafts/others_relabel_patch.json: [{row, id, path, before, after}] for tools/supabase.js patch.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'tools'))
import bank  # noqa: E402

LABELS = {
    'cardio-case-1': ('NURS 1021', 'Unit 2 (Cardiovascular Disorders)'),
    'case_1782149061171': ('NURS 1021', 'Unit 6 (Gastrointestinal Disorders)'),
    'case_1782159166328': ('NURS 1021', 'Unit 3 (Respiratory Disorders)'),
    'case_1790769567553': ('NURS 1021', 'Unit 3 (Respiratory Disorders)'),         # CS2 tuberculosis
    'case_1790776800002': ('NURS 1021', 'Unit 3 (Respiratory Disorders)'),         # CS3 acute respiratory failure
    'case_1790776800004': ('NURS 1017', 'Unit 4 (Neoplasia)'),                     # CS4 breast cancer
    'case_1790776800005': ('NURS 1017', 'Unit 5 (Integumentary Disorders and Burns)'),  # CS5 burns
    'case_1790776800006': ('NURS 1021', 'Unit 2 (Cardiovascular Disorders)'),      # CS6 STEMI
    'case_1790776800007': ('NURS 1017', 'Unit 6 (Musculoskeletal Disorders)'),     # CS7 compartment syndrome
    'case_1790776800008': ('NURS 1021', 'Unit 3 (Respiratory Disorders)'),         # CS8 COPD I
    'case_1790776800009': ('NURS 1021', 'Unit 3 (Respiratory Disorders)'),         # CS9 COPD II
    'case_1790776800010': ('NURS 1021', 'Unit 1 (Blood Disorders)'),               # CS10 DVT II
    'case_1790776800011': ('NURS 1021', 'Unit 7 (Urinary Disorders)'),             # CS11 ESRD
    'case_1790776800012': ('NURS 1021', 'Unit 6 (Gastrointestinal Disorders)'),    # CS12 GERD
    'case_1790776800013': ('NURS 1021', 'Unit 2 (Cardiovascular Disorders)'),      # CS13 heart failure
    'case_1790776800014': ('NURS 1021', 'Unit 4 (Inflammation and Immune Disorders)'),  # CS14 HIV
    'case_1790776800015': ('NURS 1017', 'Unit 11 (Endocrine Disorders)'),          # CS15 DKA
    'case_1790776800016': ('NURS 1021', 'Unit 6 (Gastrointestinal Disorders)'),    # CS16 liver failure
    'case_1790776800017': ('NURS 1021', 'Unit 9 (Reproductive Disorders)'),        # CS17 prostate cancer
    'case_1790776800018': ('NURS 1017', 'Unit 6 (Musculoskeletal Disorders)'),     # CS18 spine surgery
    'case_1790776800019': ('NURS 1017', 'Unit 7 (Neurological Disorders)'),        # CS19 stroke
    'case_1790776800020': ('NURS 1021', 'Unit 3 (Respiratory Disorders)'),         # CS20 tension pneumothorax
    'case_1790776800021': ('NURS 1017', 'Unit 11 (Endocrine Disorders)'),          # CS21 thyroid storm
}
SHOW = ['case_1790769567553']
HIDE = ['case_1782149061171', 'case_1782159166328']


def main():
    cases, _ = bank.load()
    by_id = {c['id']: c for c in cases}
    others = {c['id'] for c in cases if c.get('course') == 'Others'}
    assert others == set(LABELS), sorted(others ^ set(LABELS))
    entries = []

    def add(cid, field, after):
        before = by_id[cid].get(field)
        if before != after:
            entries.append({'row': 'cases', 'id': cid, 'path': [field], 'before': before, 'after': after})

    for cid, (course, unit) in LABELS.items():
        add(cid, 'course', course)
        for field in ('unit', 'topic', 'disorder'):
            add(cid, field, unit)
    for cid in SHOW:
        assert by_id[cid].get('draft') is True
        add(cid, 'draft', False)
    for cid in HIDE:
        add(cid, 'draft', True)

    out = os.path.join(HERE, 'others_relabel_patch.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=1)
    print(f'{len(entries)} changes written to {os.path.relpath(out)}')


if __name__ == '__main__':
    main()
