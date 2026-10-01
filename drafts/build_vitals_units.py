"""Builds drafts/vitals_units_patch.json: writes temperatures and vital-sign units the way the NCLEX does
(user request, October 2026), across every case study and stand-alone question.

1. Temperatures everywhere (chart tabs, stems, options, rationales, highlight passages): the degree sign
   right after the number, then a space and the scale: "38.2°C", "38.2 °C", "38.2&deg; C" -> "38.2° C";
   the same for Fahrenheit ("101.2° F"). A table cell in a temperature row reading "36.5 C" also gets the
   degree sign.
2. Vital-sign rows of tables in chart tabs (row labelled T/Temp/Temperature, P/HR/Pulse/Heart rate,
   RR/Respiratory rate, BP/Blood pressure, SpO2/Pulse oximetry/Oxygen saturation; laboratory tables are
   skipped): a value cell holding just the number gets its unit (P "112 beats/min", RR "24 breaths/min",
   BP "142/88 mm Hg", SpO2 "94%"); "bpm" becomes "beats/min" in pulse rows and "breaths/min" in
   respiratory rows, "/min" in respiratory rows becomes "breaths/min", and "mmHg" becomes "mm Hg".
   Anything else in a cell (words, ranges with other text, "on room air") is kept as it is.

3. Units in running text anywhere (added at the user's request, 1 Oct 2026): see fix_text_units.

Only the text changes; markup and styles are kept, and every screen gets the same change, so the chart
carry-forward rule still holds. Apply with the Supabase workflow's `patch` action.

Usage: python3 drafts/build_vitals_units.py [--summary] [--skip <item id> ...]  (skip items being edited in the studio)
"""
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools"))
import bank  # noqa: E402

# ---- 1. Temperatures ----
DEG = r"(?:°|&deg;|º|&#176;|&#xB0;)"
TEMP = re.compile(r"(\d{2,3}(?:\.\d+)?)[ \t ]*(?:&nbsp;)?" + DEG + r"[ \t ]*(?:&nbsp;)?([CF])\b")


def fix_temperatures(s):
    return TEMP.sub(r"\1° \2", s)


# ---- 2. Vital-sign rows ----
TABLE = re.compile(r"<table[\s\S]*?</table>", re.I)
ROW = re.compile(r"(<tr[^>]*>)([\s\S]*?)(</tr>)", re.I)
CELL = re.compile(r"(<t([hd])\b[^>]*>)([\s\S]*?)(</t[hd]>)", re.I)


def text_of(h):
    t = re.sub(r"<[^>]+>", "", h)
    t = t.replace("&nbsp;", " ").replace("&deg;", "°").replace("&amp;", "&")
    return re.sub(r"[\s ]+", " ", t).strip()


def vital_kind(label_html):
    l = text_of(label_html).lower().rstrip(":. ")
    if re.search(r"spo\s*2|sp\s*o\s*2|pulse ox|oxygen sat|o2 sat", l):
        return "spo2"
    l = re.sub(r"\s*\(.*\)$", "", l).strip()
    if re.fullmatch(r"t|temp|temperature", l):
        return "t"
    if re.fullmatch(r"bp|b/p|blood pressure|nibp", l):
        return "bp"
    if re.fullmatch(r"rr|r|resp|resps|respirations|respiratory rate|respiration rate", l):
        return "rr"
    if re.fullmatch(r"p|hr|pulse|pulse rate|heart rate|apical pulse|radial pulse", l):
        return "p"
    return None


def is_lab_table(table_html):
    first = CELL.search(table_html)
    return bool(first) and bool(re.search(r"laboratory|lab test|reference range", text_of(first.group(3)), re.I))


def append_after_last_number(cell_html, unit):
    nums = list(re.finditer(r"\d+(?:\.\d+)?", cell_html))
    m = nums[-1]
    return cell_html[:m.end()] + unit + cell_html[m.end():]


def fix_value(kind, h):
    t = text_of(h)
    if not t:
        return h
    if kind == "t":
        if re.fullmatch(r"(2[5-9]|3\d|4[0-5])(\.\d+)?\s*C", t):
            return re.sub(r"(\d)\s*C\b", r"\1° C", h)
        return h
    if kind == "p":
        if re.fullmatch(r"\d{2,3}", t):
            return append_after_last_number(h, " beats/min")
        h = re.sub(r"\bbpm\b", "beats/min", h)
        return re.sub(r"(\d)\s*/\s*min\b", r"\1 beats/min", h)
    if kind == "rr":
        if re.fullmatch(r"\d{1,3}", t):
            return append_after_last_number(h, " breaths/min")
        h = re.sub(r"\bbpm\b", "breaths/min", h)
        return re.sub(r"(\d)\s*/\s*min\b", r"\1 breaths/min", h)
    if kind == "bp":
        if re.fullmatch(r"\d{2,3}\s*/\s*\d{2,3}", t):
            return append_after_last_number(h, " mm Hg")
        return re.sub(r"\bmmHg\b", "mm Hg", h)
    if kind == "spo2":
        if re.fullmatch(r"\d{2,3}", t):
            return append_after_last_number(h, "%")
        return h
    return h


def fix_vitals_tables(html, changes):
    def fix_table(tm):
        table = tm.group(0)
        if is_lab_table(table):
            return table

        def fix_row(rm):
            cells = list(CELL.finditer(rm.group(2)))
            if len(cells) < 2:
                return rm.group(0)
            kind = vital_kind(cells[0].group(3))
            if not kind:
                return rm.group(0)
            body, out, pos = rm.group(2), [], 0
            for c in cells[1:]:
                if c.group(2).lower() != "d":
                    continue
                new = fix_value(kind, c.group(3))
                if new != c.group(3):
                    changes[kind].append((text_of(c.group(3)), text_of(new)))
                out.append(body[pos:c.start(3)] + new)
                pos = c.end(3)
            out.append(body[pos:])
            return rm.group(1) + "".join(out) + rm.group(3)

        return ROW.sub(fix_row, table)

    return TABLE.sub(fix_table, html)


# ---- 3. Units in running text (notes, rationales, stems, options, passages, any cell) ----
# "mmHg" -> "mm Hg"; "88 bpm" -> "88 beats/min" (or "breaths/min" after a respiratory label);
# "122/min" -> beats/min or breaths/min when a label just before says which; a labelled vital sign
# with no unit gets one: "P 128" / "HR 72" / "pulse 88" / "heart rate of 104" -> beats/min,
# "RR 30" / "respiratory rate of 24" / "respirations 18" -> breaths/min, "BP 88/60" / "blood pressure
# 154/96" -> mm Hg (ranges such as "HR 100–120" get the unit after the range). "P" alone counts only
# in a list of vital signs (RR or BP within the same stretch of text).
SEP = r"(?:\s+(?:of|is|was|at|to|from|now|remains|increased to|decreased to)\s+|\s*:\s*|\s+)"
RANGE = r"(?:\s*(?:–|-|to)\s*\d{2,3})?"
P_LABEL = r"\b(?:HR|[Pp]ulse(?: rate)?|[Hh]eart rate|[Aa]pical pulse|[Rr]adial pulse)"
RR_LABEL = r"\b(?:RR|[Rr]espiratory rate|[Rr]espirations|[Rr]esp(?:iratory)? rate)"
BP_LABEL = r"\b(?:BP|B/P|[Bb]lood pressure)"
NO_UNIT = r"(?!\s*(?:beats|breaths|[Bb][Pp][Mm]|/|%|mm|\.\d|[–-]\s*\d|\d|s\b|x\b|×|times|°))"
BRACE_END = r"(?=[\s,;.)|}<]|$)"


def _ctx(s, start):
    return re.sub(r"<[^>]+>", " ", s[max(0, start - 40):start]).lower()


def fix_text_units(s):
    s = re.sub(r"\bmmHg\b", "mm Hg", s)
    s = re.sub(r"\bmm hg\b", "mm Hg", s)

    def bpm(m):
        resp = re.search(r"\b(rr|resp|respirations|respiratory)\b[^,;.]*$", _ctx(s, m.start()))
        return m.group(1) + (" breaths/min" if resp else " beats/min")
    s = re.sub(r"(\d)\s*bpm\b", bpm, s, flags=re.I)

    def per_min(m):
        c = _ctx(s, m.start())
        if re.search(r"\b(rr|resp|respirations|respiratory)\b[^,;.]*$", c):
            return m.group(1) + " breaths/min"
        if re.search(r"\b(hr|pulse|heart rate|apical)\b[^,;.]*$", c):
            return m.group(1) + " beats/min"
        return m.group(0)
    s = re.sub(r"(\d{2,3})\s*/\s*min\b", per_min, s)

    s = re.sub("(" + P_LABEL + SEP + r"\d{2,3}" + RANGE + r")\b" + NO_UNIT + BRACE_END, r"\1 beats/min", s)
    s = re.sub("(" + RR_LABEL + SEP + r"\d{1,2}" + RANGE + r")\b" + NO_UNIT + BRACE_END, r"\1 breaths/min", s)
    s = re.sub("(" + BP_LABEL + SEP + r"\d{2,3}/\d{2,3})\b(?!\s*(?:mm|/))" + BRACE_END, r"\1 mm Hg", s)

    # "P 92" only inside a list of vital signs (RR or BP nearby).
    def p_alone(m):
        around = re.sub(r"<[^>]+>", " ", s[max(0, m.start() - 60):m.end() + 60])
        return m.group(1) + " beats/min" if re.search(r"\b(RR|BP)\b", around) else m.group(0)
    s = re.sub(r"(\bP\s*:?\s+\d{2,3})\b" + NO_UNIT + BRACE_END, p_alone, s)
    return s


def walk(o, path=()):
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, path + (k,))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, path + (i,))


SKIP_KEYS = {"id", "questionImage", "image", "imageUrl", "src"}


def main():
    cases, standalone = bank.load()
    entries, changes, temps = [], collections.defaultdict(list), collections.Counter()
    skip = {a for i, a in enumerate(sys.argv) if i and sys.argv[i - 1] == "--skip"}
    for row, items in (("cases", cases), ("standalone", standalone)):
        for item in items:
            if item["id"] in skip:
                continue
            for path, s in walk(item.get("screens", []), ("screens",)):
                if not s or s.startswith("data:") or any(k in SKIP_KEYS for k in path if isinstance(k, str)):
                    continue
                # Leave embedded images (data: URLs inside src attributes) out of the temperature search.
                parts = re.split(r'(src="data:[^"]*")', s)
                new = "".join(p if p.startswith('src="data:') else fix_temperatures(p) for p in parts)
                for m in TEMP.finditer(s):
                    temps[re.sub(r"\d+(\.\d+)?", "N", m.group(0))] += 1
                if path[-1] == "content" and "tabs" in path:
                    new = fix_vitals_tables(new, changes)
                parts = re.split(r'(src="data:[^"]*")', new)
                new = "".join(p if p.startswith('src="data:') else fix_text_units(p) for p in parts)
                if new != s:
                    entries.append({"row": row, "id": item["id"], "path": list(path), "before": s, "after": new})
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vitals_units_patch.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=1, ensure_ascii=False)
    print(f"{len(entries)} fields in {len({e['id'] for e in entries})} items -> drafts/vitals_units_patch.json")
    print("Temperature forms rewritten:", dict(temps))
    for kind, lst in changes.items():
        c = collections.Counter((re.sub(r"\d+(\.\d+)?", "N", a), re.sub(r"\d+(\.\d+)?", "N", b)) for a, b in lst)
        print(f"{kind}: {len(lst)} cells", c.most_common(12) if "--summary" in sys.argv else "")


if __name__ == "__main__":
    main()
