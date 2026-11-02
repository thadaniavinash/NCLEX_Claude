"""Writes an answer key with full rationales from Unit 7 case study JSON files.

Usage: python3 drafts/build_unit7_answer_key.py [first last out.md]   (default: cases 2-6 -> NURS_1017_Unit_7_Answer_Key.md)
"""
import glob, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = {1: "Recognize", 2: "Analyze", 3: "Prioritize hypotheses", 4: "Generate solutions", 5: "Take action",
         6: "Evaluate outcomes"}  # clinical judgment steps (labels without the word "cues")


def text(h):
    h = re.sub(r"<br\s*/?>", "\n", h or "")
    h = re.sub(r"</?b>", "**", h)
    h = re.sub(r"</?i>", "*", h)
    h = re.sub(r"<sup>(.*?)</sup>", r"^\1", h)
    h = re.sub(r"<sub>(.*?)</sub>", r"\1", h)
    h = re.sub(r"<[^>]+>", "", h)
    return html.unescape(h).strip()


def answers(q):
    t = q["type"]
    out = []
    if t in ("select_all", "multiple_choice", "select_n", "trend"):
        for i, o in enumerate(q["options"], 1):
            out.append(f"{i}. {'**✓** ' if o['correct'] else ''}{o['text']}")
    elif t in ("matrix_mc", "matrix_mr"):
        cols = q["matrix"]["columns"]
        for r in q["matrix"]["rows"]:
            idx = r["correctIndices"] if t == "matrix_mr" else [r["correctIndex"]]
            out.append(f"- {r['text']} → **{', '.join(cols[i] for i in idx)}**")
    elif t in ("dropdown_cloze", "dyad", "triad"):
        sent = q["cloze"]["text"]
        for i, d in enumerate(q["cloze"]["dropdowns"]):
            right = next(o["text"] for o in d["options"] if o["correct"])
            others = "; ".join(o["text"] for o in d["options"] if not o["correct"])
            sent = sent.replace(f"[[drop{i}]]", f"**[{right}]**")
            out.append(f"- Drop-down {i + 1}: **{right}** (other choices: {others})")
        out.insert(0, sent + "\n")
    elif t in ("highlight", "highlight_2"):
        for tab in q["highlightTabs"]:
            for m in re.finditer(r"\{([^{|}]+)(\|correct)?\}", tab["content"]):
                out.append(f"- [{tab['title']}] {'**✓** ' if m.group(2) else ''}{text(m.group(1))}")
    elif t == "bowtie":
        for label, key in (("Condition", "bowtieConditions"), ("Actions", "bowtieActions"), ("Parameters", "bowtieParams")):
            out.append(f"- {label}: " + "; ".join(("**✓ " + o["text"] + "**") if o["correct"] else o["text"] for o in q[key]))
    elif t == "ordered_response":
        out += [f"{i}. {s}" for i, s in enumerate(q["orderedOptions"], 1)]
    return "\n".join(out)


FIRST, LAST, OUT = (int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]) if len(sys.argv) > 3 else (2, 6, "NURS_1017_Unit_7_Answer_Key.md")
md = [f"# NURS 1017 Unit 7 Case Studies {FIRST}–{LAST}: Answer Key", "",
      "Written on 2 Nov 2026 for the Unit 7 (Neurological Disorders) learning outcomes. ✓ marks a correct answer. "
      "Each case also carries a “Needs your review” note in the studio.", ""]
files = [glob.glob(os.path.join(HERE, f"case_178241{n:07d}_*.json"))[0] for n in range(FIRST, LAST + 1)]
for f in files:
    c = json.load(open(f))
    md += [f"## {c['title']}", "", c["description"], "", "**Notes for review:**", "", c["authorReview"]["note"].split("\n", 1)[1], ""]
    for i, s in enumerate(c["screens"], 1):
        q = s["question"]
        md += [f"### Screen {i}: {STEPS[s['step']]} ({q['type']})", ""]
        if q.get("preamble"):
            md += [f"*{text(q['preamble'])}*", ""]
        md += [text(q["stem"]), "", answers(q), "", "**Rationale**", "", text(q["explanation"]).replace("\n\n", "\n\n"), ""]
out = os.path.join(HERE, OUT)
open(out, "w").write("\n".join(md))
print("wrote", out)
