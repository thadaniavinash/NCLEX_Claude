"""Stamp a fresh cache-busting version on every script and stylesheet in index.html.

Browsers cache style.css, cases-data.js and js/*.js. index.html loads them as
`file?v=<version>`; changing the version makes every visitor fetch the new files.
Run after changing any of them:  python3 tools/bump_version.py
"""
import datetime
import os
import re

INDEX = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "index.html")

version = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d%H%M%S")
html = open(INDEX, encoding="utf-8").read()
updated, count = re.subn(r'((?:src|href)="[^"?]+\.(?:js|css))\?v=[^"]*"', rf'\1?v={version}"', html)
open(INDEX, "w", encoding="utf-8").write(updated)
print(f"Stamped version {version} on {count} files in index.html")
