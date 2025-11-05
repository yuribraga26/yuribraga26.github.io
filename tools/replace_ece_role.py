#!/usr/bin/env python3
from pathlib import Path

workspace = Path(__file__).resolve().parents[1]
files = [
    workspace / 'campus-involvement' / 'index.txt',
    workspace / 'campus-involvement' / 'index.html',
    workspace / 'images' / 'pasted_content.txt',
]
replacements = [
    ('Ambassador and Mentor', 'President and Mentor'),
    ('Ambassador and mentor', 'President and mentor'),
    ('Your role: Ambassador', 'Your role: President'),
]

for fp in files:
    if not fp.exists():
        print('Missing:', fp)
        continue
    text = fp.read_text(encoding='utf-8')
    orig = text
    for a,b in replacements:
        text = text.replace(a,b)
    if text != orig:
        fp.write_text(text, encoding='utf-8')
        print('Updated:', fp)
    else:
        print('No change:', fp)
