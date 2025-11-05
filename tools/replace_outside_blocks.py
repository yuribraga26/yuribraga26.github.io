#!/usr/bin/env python3
"""Replace '><' with '>\n<' outside of script/style blocks using span tracking.

This is conservative and only touches text outside <script>...</script> and <style>...</style>.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BLOCK_RE = re.compile(r'(?i)(<script\b[^>]*?>.*?</script\s*>|<style\b[^>]*?>.*?</style\s*>)', re.DOTALL)


def process(text: str) -> str:
    out_parts = []
    last = 0
    for m in BLOCK_RE.finditer(text):
        start, end = m.span()
        # process outside block
        outside = text[last:start]
        outside = outside.replace('><', '>' + '\n' + '<')
        out_parts.append(outside)
        # append the block unchanged
        out_parts.append(text[start:end])
        last = end
    # tail
    tail = text[last:]
    tail = tail.replace('><', '>' + '\n' + '<')
    out_parts.append(tail)
    return ''.join(out_parts)


def prettify_file(path: Path) -> bool:
    try:
        raw = path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"SKIP {path} (read error: {e})")
        return False
    # Keep DOCTYPE line at top if present
    stripped = raw.lstrip()
    prefix = ''
    if stripped.lower().startswith('<!doctype'):
        first_line, _, rest = stripped.partition('\n')
        prefix = first_line.strip() + '\n'
        body = rest
    else:
        body = raw

    new_body = process(body)
    new_text = prefix + new_body
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
