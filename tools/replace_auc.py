#!/usr/bin/env python3
import sys
from pathlib import Path

# Files to update
files = [
    Path(__file__).resolve().parents[1] / 'carefuse' / 'index.html',
    Path(__file__).resolve().parents[1] / 'index.html',
    Path(__file__).resolve().parents[1] / 'carefuse' / 'index.txt',
    Path(__file__).resolve().parents[1] / 'index.txt',
]

replacements = [
    ('Achieved ~0.87 AUC with robust calibration techniques', 'Achieved ~0.93 AUC with robust calibration techniques'),
    ('Achieved ~0.87 AUC', 'Achieved ~0.93 AUC'),
    ('~0.87', '~0.93'),
    ('≈ 0.87', '≈ 0.93'),
    ('AUC ≈ 0.87', 'AUC ≈ 0.93'),
    ('AUC ≈0.87', 'AUC ≈0.93'),
    ('0.87 AUC', '0.93 AUC'),
]

changed = []
for fp in files:
    if not fp.exists():
        print(f"Missing: {fp}")
        continue
    text = fp.read_text(encoding='utf-8')
    original = text
    for a,b in replacements:
        text = text.replace(a,b)
    if text != original:
        fp.write_text(text, encoding='utf-8')
        changed.append(str(fp))
        print(f"Updated: {fp}")
    else:
        print(f"No changes for: {fp}")

print('\nSummary:')
print(f"Files changed: {len(changed)}")
for p in changed:
    print(' -', p)

if not changed:
    sys.exit(2)
else:
    sys.exit(0)
