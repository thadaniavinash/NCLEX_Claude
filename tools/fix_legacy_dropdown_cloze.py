"""One-time fix: convert drop-down questions stored in the legacy `dropdown_cloze`
shape ({sentences, dropdowns[{id, options: [str], correctIndex}]}) into the `cloze`
shape the player and editor read ({text with [[dropN]], dropdowns[{placeholder,
options: [{text, correct}]}]}).

Every legacy question had its correct answer as the first option, so the options
are shuffled into a fixed (seeded, reproducible) order during conversion.
"""
import random
import re
import sys

import bank


def convert(q, seed):
    legacy = q.pop("dropdown_cloze")
    order = {d["id"]: i for i, d in enumerate(legacy["dropdowns"])}
    text = " ".join(s.strip() for s in legacy["sentences"])
    text = re.sub(r"\[(\w+)\]", lambda m: f"[[drop{order[m.group(1)]}]]" if m.group(1) in order else m.group(0), text)

    rng = random.Random(seed)
    dropdowns = []
    for d in legacy["dropdowns"]:
        options = [{"text": t, "correct": i == d["correctIndex"]} for i, t in enumerate(d["options"])]
        rng.shuffle(options)
        dropdowns.append({"placeholder": "Select...", "options": options})
    q["cloze"] = {"text": text, "dropdowns": dropdowns}


def main():
    cases, standalone = bank.load()
    converted = 0
    for item in cases + standalone:
        for screen in item["screens"]:
            q = screen["question"]
            if "dropdown_cloze" in q and "cloze" not in q:
                convert(q, f"{item['id']}:{screen['step']}")
                converted += 1
    bank.save(cases, standalone)
    print(f"converted {converted} questions")


if __name__ == "__main__":
    sys.exit(main())
