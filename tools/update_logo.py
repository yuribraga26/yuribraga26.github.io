#!/usr/bin/env python3
"""
Replace occurrences of 'carefuse_logo.png' with 'YB_logo.png' in HTML/TXT files
across the workspace, excluding the `carefuse/` directory and `backups/`.

Creates a backup for each changed file named <filename>.yb-logo.bak

Usage: run this script from anywhere; it resolves the repo root relative to the
script location.
"""
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {"carefuse", "backups"}
EXTS = {".html", ".htm", ".txt"}
OLD = "carefuse_logo.png"
NEW = "YB_logo.png"


def should_skip(path: Path) -> bool:
    parts = {p.lower() for p in path.parts}
    if parts & SKIP_DIRS:
        return True
    return False


def main():
    changed = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # allow skipping entire directories early
        rel = Path(dirpath).relative_to(ROOT)
        if should_skip(rel):
            continue
        for fn in filenames:
            p = Path(dirpath) / fn
            if p.suffix.lower() not in EXTS:
                continue
            # skip backup files
            if p.name.endswith('.yb-logo.bak') or '.next-runtime.bak' in p.name or p.name.endswith('.bak'):
                continue
            try:
                text = p.read_text(encoding='utf-8')
            except Exception:
                # skip files we can't read as utf-8
                continue
            if OLD in text:
                backup = p.with_name(p.name + '.yb-logo.bak')
                if not backup.exists():
                    backup.write_text(text, encoding='utf-8')
                newtext = text.replace(OLD, NEW)
                p.write_text(newtext, encoding='utf-8')
                changed.append(str(p.relative_to(ROOT)))

    if changed:
        print("Updated files (backups written with .yb-logo.bak):")
        for c in changed:
            print(" -", c)
    else:
        print("No files needed updating.")


if __name__ == '__main__':
    main()
