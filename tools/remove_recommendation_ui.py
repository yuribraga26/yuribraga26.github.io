#!/usr/bin/env python3
"""
Script to surgically remove recommendation upload/manual UI text and disable star rendering
in the built Next.js chunk for recommendations. Edits are literal substring replacements.
"""
from pathlib import Path
p = Path(r"c:\Users\ymabr\Personal\yuri-portfolio\_next\static\chunks\app\recommendations\page-41c1b54e17e532e3.js")
if not p.exists():
    print("File not found:", p)
    raise SystemExit(1)
text = p.read_text(encoding='utf-8')
replacements = [
    ("Upload Recommendation Letter", ""),
    ("Upload PDF, Word document, or image files of recommendation letters", ""),
    ("Add Recommendation Manually", ""),
    ("Enter recommendation details manually if you prefer not to upload a file", ""),
    ("e.rating&&", "false&&"),
]
changed = False
for old, new in replacements:
    if old in text:
        text = text.replace(old, new)
        changed = True
        print(f"Replaced: {old!r} -> {new!r}")
    else:
        print(f"Not found (skipped): {old!r}")
if changed:
    backup = p.with_suffix('.js.bak')
    p.rename(backup)
    p.write_text(text, encoding='utf-8')
    print("Updated file and created backup:", backup)
else:
    print("No changes made.")
