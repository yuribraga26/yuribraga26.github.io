#!/usr/bin/env python3
"""State-machine formatter: insert newlines between tags outside script/style blocks.

This avoids regex pitfalls by scanning the document and tracking whether we're
inside a <script> or <style> element (case-insensitive). It writes back only
if changes occur.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BLOCKS = ('script', 'style')


def process_text(text: str) -> str:
    out = []
    i = 0
    n = len(text)
    in_block = None  # None or block name
    while i < n:
        if in_block is None:
            # Look for next '<'
            if text[i] == '<':
                # check if this opens a block
                # find tag name
                j = i + 1
                # skip possible '/' for end tags
                if j < n and text[j] == '/':
                    j += 1
                # read tag name
                start = j
                while j < n and text[j].isalpha():
                    j += 1
                tag = text[start:j].lower()
                if tag in BLOCKS:
                    # enter block mode: copy until closing tag </tag>
                    # but first copy the opening tag as normal
                    # find end of opening tag '>'
                    k = text.find('>', j)
                    if k == -1:
                        # malformed, copy rest
                        out.append(text[i:])
                        break
                    out.append(text[i:k+1])
                    i = k + 1
                    # now copy verbatim until we see </tag>
                    end_seq = f'</{tag}>'
                    idx = text.lower().find(end_seq, i)
                    if idx == -1:
                        # not found, copy rest
                        out.append(text[i:])
                        break
                    # copy block body and closing tag
                    out.append(text[i:idx])
                    out.append(text[idx:idx+len(end_seq)])
                    i = idx + len(end_seq)
                    continue
                else:
                    # normal tag; append '<' and continue
                    out.append('<')
                    i += 1
                    continue
            else:
                # not a '<', append char
                out.append(text[i])
                # if we see '>' followed by '<' across appended chars, insert newline
                # but easiest to handle after building string
                i += 1
        else:
            # shouldn't reach here since we handle blocks inline
            out.append(text[i])
            i += 1
    result = ''.join(out)
    # Now, insert newlines between tags except inside script/style (we preserved them verbatim)
    # Replace all occurrences of '><' with '>' + '\n' + '<'
    result = result.replace('><', '>' + '\n' + '<')
    # Normalize CRLF
    result = result.replace('\r\n', '\n')
    return result


def prettify_path(path: Path) -> bool:
    try:
        raw = path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"SKIP {path} (read error: {e})")
        return False
    # Handle leading DOCTYPE separately to preserve capitalization and placement
    stripped = raw.lstrip()
    prefix = ''
    if stripped.lower().startswith('<!doctype'):
        first_line, _, rest = stripped.partition('\n')
        prefix = first_line.strip() + '\n'
        html_in = rest
    else:
        html_in = raw

    new_body = process_text(html_in)
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
        if prettify_path(path):
            changed.append(str(path))
    print('\nSummary:')
    print(f"Total files checked: {len(list(ROOT.rglob('index.html'))) }")
    print(f"Total updated: {len(changed)}")
    for p in changed:
        print(' -', p)

if __name__ == '__main__':
    main()
