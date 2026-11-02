"""Writes drafts/NURS_1017_Unit_7_Answer_Key.md (answer key with full rationales) from the Unit 7 case study JSON files."""
import glob, html, json, os, re

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
    elif t == "ordered_response":
        out += [f"{i}. {s}" for i, s in enumerate(q["orderedOptions"], 1)]
    return "\n".join(out)


md = ["# NURS 1017 Unit 7 Case Studies 2–6: Answer Key", "",
      "Drafts written on 2 Nov 2026 for the Unit 7 (Neurological Disorders) learning outcomes. ✓ marks a correct answer. "
      "Each case also carries a “Needs your review” note in the studio.", ""]
for f in sorted(glob.glob(os.path.join(HERE, "case_178241000000[2-9]_*.json"))):
    c = json.load(open(f))
    md += [f"## {c['title']}", "", c["description"], "", "**Notes for review:**", "", c["authorReview"]["note"].split("\n", 1)[1], ""]
    for i, s in enumerate(c["screens"], 1):
        q = s["question"]
        md += [f"### Screen {i}: {STEPS[s['step']]} ({q['type']})", ""]
        if q.get("preamble"):
            md += [f"*{text(q['preamble'])}*", ""]
        md += [text(q["stem"]), "", answers(q), "", "**Rationale**", "", text(q["explanation"]).replace("\n\n", "\n\n"), ""]
out = os.path.join(HERE, "NURS_1017_Unit_7_Answer_Key.md")
open(out, "w").write("\n".join(md))
print("wrote", out)
