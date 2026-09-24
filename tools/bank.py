"""Read and write cases-data.js, the app's single source of question data.

The file format matches what the app and server.js write:
  window.NCLEX_CASES = [...];\n\nwindow.NCLEX_STANDALONE = [...];\n
"""
import json
import os
import re

PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cases-data.js")
_PATTERN = re.compile(r"^window\.NCLEX_CASES = (.*);\n\nwindow\.NCLEX_STANDALONE = (.*);\n$", re.S)


def load():
    m = _PATTERN.match(open(PATH, encoding="utf-8").read())
    if not m:
        raise ValueError("cases-data.js is not in the expected format")
    return json.loads(m.group(1)), json.loads(m.group(2))


def dumps(cases, standalone):
    d = lambda v: json.dumps(v, indent=2, ensure_ascii=False)
    return f"window.NCLEX_CASES = {d(cases)};\n\nwindow.NCLEX_STANDALONE = {d(standalone)};\n"


def save(cases, standalone):
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(dumps(cases, standalone))
