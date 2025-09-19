#!/usr/bin/env python3
"""Pretty-print all index.html files under the repository root.

Usage: python tools/pretty_index_html.py

This script uses BeautifulSoup4 to prettify HTML and preserves a leading <!DOCTYPE html> if present.
It will only overwrite files when the content actually changes.
"""
import sys
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
changed = []

for path in sorted(ROOT.rglob('index.html')):
    try:
        text = path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"SKIP {path} (read error: {e})")
        continue
    doctype = ''
    stripped = text.lstrip()
    if stripped.lower().startswith('<!doctype'):
        # keep the first line if it's the doctype
        first_line, _, rest = stripped.partition('\n')
        doctype = first_line.strip()
        html_in = rest
    else:
        html_in = text
    # Parse and prettify
    soup = BeautifulSoup(html_in, 'html.parser')
    pretty = soup.prettify()
    new_text = (doctype + '\n' if doctype else '') + pretty + '\n'
    # Normalize line endings
    new_text = new_text.replace('\r\n', '\n')
    if new_text != text.replace('\r\n','\n'):
        path.write_text(new_text, encoding='utf-8')
        changed.append(str(path))
        print(f"UPDATED {path}")
    else:
        print(f"UNCHANGED {path}")

print('\nSummary:')
print(f"Total files checked: {len(list(ROOT.rglob('index.html')))}")
print(f"Total updated: {len(changed)}")
if changed:
    for p in changed:
        print(' -', p)

if len(changed) == 0:
    sys.exit(0)
else:
    sys.exit(0)
