#!/usr/bin/env python3
"""
Clean Next.js client runtime artifacts from exported static HTML files.

What it does:
- Scans the workspace for .html and .txt files.
- If a file contains Next runtime artifacts (self.__next_f or /_next/static/chunks/),
  it creates a backup (<filename>.next-runtime.bak) if not present, then removes:
    * <script ... src="/_next/static/chunks/...">...</script>
    * <script ...>...__next_f... </script> (inline payloads)
    * Any <script src="/_next/static/chunks/webpack-...js" ...></script>
- Writes cleaned file and reports summary.

Safety:
- Makes a one-time backup per file before modification.
- Only removes script tags that match the patterns; leaves other inline scripts (like mobile-menu) intact.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAT_CHUNK_SRC = re.compile(r"<script[^>]+src=[\"']/?_next/static/chunks/[^\"']+[\"'][^>]*>\s*</script>\s*", re.IGNORECASE)
PAT_INLINE_NEXT = re.compile(r"<script[^>]*>.*?__next_f.*?</script>\s*", re.IGNORECASE | re.DOTALL)
PAT_WEBPACK_SRC = re.compile(r"<script[^>]+src=[\"']/?_next/static/chunks/webpack-[^\"']+[\"'][^>]*>\s*</script>\s*", re.IGNORECASE)

EXTS = {'.html', '.htm', '.txt'}

files_processed = 0
files_modified = 0

for p in ROOT.rglob('*'):
    if p.suffix.lower() not in EXTS:
        continue
    try:
        text = p.read_text(encoding='utf-8')
    except Exception:
        # skip binary or unreadable files
        continue

    if 'self.__next_f' not in text and '/_next/static/chunks' not in text and 'webpack-' not in text:
        continue

    files_processed += 1
    original = text

    # Create backup
    backup = p.with_suffix(p.suffix + '.next-runtime.bak')
    if not backup.exists():
        backup.write_text(original, encoding='utf-8')

    # Remove patterns
    cleaned = PAT_CHUNK_SRC.sub('', original)
    cleaned = PAT_WEBPACK_SRC.sub('', cleaned)
    cleaned = PAT_INLINE_NEXT.sub('', cleaned)

    # Also remove any standalone occurrences of (self.__next_f=self.__next_f||[]).push... left outside script tags
    cleaned = re.sub(r"\(self\.__next_f=self\.__next_f\|\|\[\]\)\.push\([^)]*\);?", '', cleaned, flags=re.IGNORECASE | re.DOTALL)

    # Trim trailing spaces/newlines introduced
    if cleaned != original:
        p.write_text(cleaned, encoding='utf-8')
        files_modified += 1
        print(f"Cleaned: {p.relative_to(ROOT)} (backup: {backup.name})")
    else:
        print(f"No change needed for: {p.relative_to(ROOT)}")

print('\nSummary:')
print(f'  Files scanned with artifacts: {files_processed}')
print(f'  Files modified: {files_modified}')

if files_modified == 0:
    print('No files needed modification.')
else:
    print('Next: re-run a grep for self.__next_f to verify.')

sys.exit(0)
