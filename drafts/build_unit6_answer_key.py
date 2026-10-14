"""Writes drafts/NURS_1017_Unit_6_Answer_Key.md (answer key + full rationales) from the Unit 6 case JSON files."""
import glob, html, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = ["Recognize cues", "Analyze cues", "Prioritize hypotheses", "Generate solutions", "Take action", "Evaluate outcomes"]


def text(s):
    s = re.sub(r"<br\s*/?>", "\n", s or "")
    s = re.sub(r"</?b>", "**", s)
    s = re.sub(r"</?i>", "*", s)
    s = re.sub(r"<sup>(.*?)</sup>", r"^\1", s)
    s = re.sub(r"<sub>(.*?)</sub>", r"\1", s)
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def key(q):
    t = q["type"]
    if t in ("select_all", "select_n", "multiple_choice"):
        return [f"{i + 1}. {'✔' if o['correct'] else '✘'} {o['text']}" for i, o in enumerate(q["options"])]
    if t == "matrix_mc":
        cols = q["matrix"]["columns"]
        return [f"- {r['text']} → **{cols[r['correctIndex']]}**" for r in q["matrix"]["rows"]]
    if t == "matrix_mr":
        cols = q["matrix"]["columns"]
        return [f"- {r['text']} → **{', '.join(cols[i] for i in r['correctIndices'])}**" for r in q["matrix"]["rows"]]
    if t == "dropdown_cloze":
        out = [f"Sentence: {q['cloze']['text']}"]
        for i, d in enumerate(q["cloze"]["dropdowns"]):
            out.append(f"- drop{i}: **{next(o['text'] for o in d['options'] if o['correct'])}** "
                       f"(other choices: {'; '.join(o['text'] for o in d['options'] if not o['correct'])})")
        return out
    if t == "ordered_response":
        return [f"{i + 1}. {s}" for i, s in enumerate(q["orderedOptions"])]
    if t == "highlight":
        out = []
        for tab in q["highlightTabs"]:
            for m in re.finditer(r"\{([^{|}]+)(\|correct)?\}", tab["content"]):
                out.append(f"- {'✔' if m.group(2) else '✘'} {text(m.group(1))}")
        return out
    return ["(answer key not listed for this type)"]


lines = ["# NURS 1017 Unit 6 case studies: answer key and rationales", "",
         "Written October 2026. Each case carries an author-only “Needs your review” note in the studio.", ""]
for f in sorted(glob.glob(os.path.join(HERE, "case_17824000000*_NURS_1017_Unit_6_Case_Study_*.json"))):
    c = json.load(open(f))
    lines += [f"## {c['title']}", "", c["description"], ""]
    if c.get("authorReview"):
        lines += ["**Points to review:**", ""] + [f"- {x}" for x in c["authorReview"]["note"].split("\n")[1:]] + [""]
    for i, s in enumerate(c["screens"]):
        q = s["question"]
        lines += [f"### Screen {i + 1}: {STEPS[i]} ({q['type']})", ""]
        if q.get("preamble"):
            lines += [f"*{text(q['preamble'])}*", ""]
        lines += [text(q["stem"]), ""] + key(q) + ["", "**Rationale:**", ""] + [text(q["explanation"]), ""]
out = os.path.join(HERE, "NURS_1017_Unit_6_Answer_Key.md")
open(out, "w").write("\n".join(lines))
print("wrote", out)
