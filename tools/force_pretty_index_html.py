#!/usr/bin/env python3
"""Force-pretty index.html by inserting newlines between tags while preserving <script>/<style> contents.

This is more aggressive but careful: it extracts script/style blocks first, replaces them with placeholders,
adds newlines between tags, then restores the original blocks unchanged.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SCRIPT_RE = re.compile(r"<script\b[^>]*?>.*?</script>", re.IGNORECASE | re.DOTALL)
STYLE_RE = re.compile(r"<style\b[^>]*?>.*?</style>", re.IGNORECASE | re.DOTALL)

PLACEHOLDER_SCRIPT = "@@SCRIPT_BLOCK_{idx}@@"
PLACEHOLDER_STYLE = "@@STYLE_BLOCK_{idx}@@"


def protect_blocks(text: str):
    scripts = {}
    styles = {}

    def script_sub(m):
        idx = len(scripts)
        key = PLACEHOLDER_SCRIPT.format(idx=idx)
        scripts[key] = m.group(0)
        return key

    def style_sub(m):
        idx = len(styles)
        key = PLACEHOLDER_STYLE.format(idx=idx)
        styles[key] = m.group(0)
        return key

    text = SCRIPT_RE.sub(script_sub, text)
    text = STYLE_RE.sub(style_sub, text)
    return text, scripts, styles


def restore_blocks(text: str, scripts: dict, styles: dict):
    # restore scripts then styles
    for k, v in scripts.items():
        text = text.replace(k, v)
    for k, v in styles.items():
        text = text.replace(k, v)
    return text


def insert_newlines_between_tags(text: str) -> str:
    # Simple pass: replace '><' with '>' + newline + '<'
    # Also ensure no multiple blank lines
    return text.replace('><', '>' + '\n' + '<')


def prettify_file(path: Path) -> bool:
    try:
        raw = path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"SKIP {path} (read error: {e})")
        return False

    stripped = raw.lstrip()
    prefix = ''
    if stripped.lower().startswith('<!doctype'):
        first_line, _, rest = stripped.partition('\n')
        prefix = first_line.strip() + '\n'
        html_in = rest
    else:
        html_in = raw

    protected, scripts, styles = protect_blocks(html_in)
    new_body = insert_newlines_between_tags(protected)
    new_body = restore_blocks(new_body, scripts, styles)

    new_text = prefix + new_body
    # Normalize to \n
    new_text = new_text.replace('\r\n', '\n')

    if new_text != raw.replace('\r\n', '\n'):
        path.write_text(new_text, encoding='utf-8')
        print(f"UPDATED {path}")
        return True
    else:
        print(f"UNCHANGED {path}")
        return False


def main():
    changed = []
    for path in sorted(ROOT.rglob('index.html')):
        if prettify_file(path):
            changed.append(str(path))

    print('\nSummary:')
    print(f"Total files checked: {len(list(ROOT.rglob('index.html'))) }")
    print(f"Total updated: {len(changed)}")
    for p in changed:
        print(' -', p)

if __name__ == '__main__':
    main()
