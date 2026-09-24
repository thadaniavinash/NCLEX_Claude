"""One-time fix: select-all and trend questions listed every correct option first,
so students could score by picking the top options. Shuffle their options into a
fixed (seeded, reproducible) order that no longer starts with all the correct
answers, and relabel rationale markers that pointed at option positions.

Rationale markers such as "(1)" were written to follow the options in order, but
not always one-to-one, so each marker's option(s) were mapped by hand below
(original option numbers). They are rewritten as "(Option N)" with the new numbers.
"""
import random
import re

import bank

# (item id, screen step) -> {marker: [original option numbers it describes]}
MARKERS = {
    ("case_1782360000001", 1): {1: [1], 2: [2], 3: [3], 4: [4]},
    ("case_1782360000001", 4): {1: [1], 2: [2], 3: [3], 4: [4], 5: [5]},
    ("case_1782360000002", 1): {1: [1], 2: [2], 3: [3]},
    ("case_1782360000002", 4): {1: [1], 2: [2], 3: [3], 4: [4]},
    ("case_1782360000003", 1): {1: [1], 2: [2], 3: [3], 4: [4]},
    ("case_1782360000003", 4): {1: [1], 2: [2], 3: [3], 4: [4]},
    ("case_1782370000001", 4): {1: [1], 2: [2], 3: [3, 4], 4: [5]},
    ("case_1782370000002", 1): {1: [1], 2: [2], 3: [3], 4: [4]},
    ("case_1782370000002", 4): {1: [1], 2: [2], 3: [3], 4: [4], 5: [5]},
    ("case_1782370000003", 1): {1: [2, 3], 2: [1, 5], 3: [4], 4: [6]},
    ("case_1782370000003", 4): {1: [1], 2: [2], 3: [3], 4: [4], 5: [5]},
    ("case_1782380000001", 4): {1: [1], 2: [2], 3: [3], 4: [4]},
    ("case_1782380000002", 1): {1: [1], 2: [2, 3]},
    ("case_1782380000002", 4): {1: [1], 2: [2, 3], 3: [4], 4: [5]},
    ("case_1782380000003", 1): {1: [1, 3], 2: [1], 3: [2], 4: [4]},
    ("case_1782380000003", 4): {1: [1], 2: [2], 3: [3], 4: [4]},
    ("case_1782380000004", 1): {1: [1], 2: [2], 3: [3], 4: [4], 5: [5]},
    ("case_1782380000004", 4): {1: [1], 2: [2], 3: [3], 4: [4], 5: [5]},
    ("case_1782380000005", 4): {1: [1], 2: [2], 3: [3], 4: [4], 5: [5]},
    ("case_1782390000001", 4): {1: [1], 2: [2], 3: [3], 4: [4]},
    ("case_1782390000002", 4): {1: [1], 2: [2], 3: [3], 4: [4]},
    ("case_1782390000003", 1): {1: [1], 2: [2], 3: [3], 4: [4]},
    ("case_1782390000003", 4): {1: [1], 2: [2], 3: [3], 4: [4]},
    ("case_1782390000004", 1): {1: [4], 2: [1], 3: [2], 4: [3]},
    ("case_1782390000004", 4): {1: [1], 2: [2], 3: [3], 4: [4]},
    ("case_1782390000005", 4): {1: [1], 2: [2], 3: [3], 4: [4]},
}

# Rationales numbered by topic ("1. Impetigo ...") rather than "(1)": heading -> options.
HEADINGS = {
    ("case_1782390000002", 1): {1: [1, 4], 2: [2, 3], 3: [5, 6]},
}


def label(numbers):
    n = sorted(numbers)
    if len(n) == 1:
        return f"Option {n[0]}"
    if len(n) == 2:
        return f"Options {n[0]} and {n[1]}"
    return "Options " + ", ".join(map(str, n[:-1])) + f", and {n[-1]}"


def correct_first(options):
    flags = [o["correct"] for o in options]
    k = sum(flags)
    return k > 0 and all(flags[:k])


def shuffled_order(options, seed):
    order = list(range(len(options)))
    rng = random.Random(seed)
    while True:
        rng.shuffle(order)
        if not correct_first([options[i] for i in order]):
            return order


def main():
    cases, standalone = bank.load()
    changed = relabeled = 0
    for item in cases + standalone:
        for screen in item["screens"]:
            q = screen["question"]
            if q.get("type") not in ("select_all", "trend") or not correct_first(q.get("options", [])):
                continue
            key = (item["id"], screen["step"])
            order = shuffled_order(q["options"], f"{item['id']}:{screen['step']}:options")
            new_number = {old + 1: new + 1 for new, old in enumerate(order)}
            q["options"] = [q["options"][i] for i in order]
            changed += 1

            text = q.get("explanation", "")
            markers = MARKERS.get(key, {})
            found = sorted(int(m) for m in re.findall(r"\((\d)\)", text))
            assert found == sorted(markers), f"{key}: markers {found} not mapped {sorted(markers)}"
            for m, olds in markers.items():
                text = text.replace(f"({m})", f"\x00{m}\x00", 1)
            for m, olds in markers.items():
                text = text.replace(f"\x00{m}\x00", f"({label(new_number[o] for o in olds)})")
            for m, olds in HEADINGS.get(key, {}).items():
                text, n = re.subn(rf"(^|<br>){m}\. ", rf"\g<1>({label(new_number[o] for o in olds)}) ", text, count=1)
                assert n == 1, f"{key}: heading {m} not found"
            if markers or key in HEADINGS:
                relabeled += 1
            q["explanation"] = text
    bank.save(cases, standalone)
    print(f"shuffled {changed} questions, relabeled {relabeled} rationales")


if __name__ == "__main__":
    main()
