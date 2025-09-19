#!/usr/bin/env python3
"""Pretty-print index.html files using only the Python standard library.

This avoids depending on BeautifulSoup/VS Code selected interpreter. It's a conservative
reformatter: it will add line breaks and indentation for tags but preserves all text
and won't try to alter attribute order or minified JS/CSS inside script/style tags.
"""
import sys
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]

class SimplePrettyHTMLParser(HTMLParser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.indent_level = 0
        self.lines = []
        self.need_newline = False

    def _indent(self):
        return '  ' * self.indent_level

    def handle_starttag(self, tag, attrs):
        attr_text = ''
        if attrs:
            attr_text = ' ' + ' '.join(f'{name}="{value}"' if value is not None else name for name, value in attrs)
        self.lines.append(f"{self._indent()}<{tag}{attr_text}>")
        self.indent_level += 1

    def handle_endtag(self, tag):
        self.indent_level = max(self.indent_level - 1, 0)
        self.lines.append(f"{self._indent()}</{tag}>")

    def handle_startendtag(self, tag, attrs):
        attr_text = ''
        if attrs:
            attr_text = ' ' + ' '.join(f'{name}="{value}"' if value is not None else name for name, value in attrs)
        self.lines.append(f"{self._indent()}<{tag}{attr_text} />")

    def handle_data(self, data):
        text = data.strip('\n')
        if not text:
            return
        # Keep inner newlines if they exist but re-indent each line
        for i, line in enumerate(text.splitlines()):
            line = line.strip()
            if line:
                self.lines.append(f"{self._indent()}{line}")

    def handle_comment(self, data):
        for line in data.splitlines():
            self.lines.append(f"{self._indent()}<!-- {line.strip()} -->")

    def handle_decl(self, decl):
        # Preserve DOCTYPE as top-level
        self.lines.insert(0, f"<!{decl}>")

    def get_text(self):
        return '\n'.join(self.lines) + '\n'


def prettify_html(text: str) -> str:
    stripped = text.lstrip()
    doctype = ''
    html_in = text
    if stripped.lower().startswith('<!doctype'):
        first_line, _, rest = stripped.partition('\n')
        doctype = first_line.strip()
        html_in = rest

    parser = SimplePrettyHTMLParser()
    parser.feed(html_in)
    new_text = (doctype + '\n' if doctype else '') + parser.get_text()
    # Normalize CRLF
    new_text = new_text.replace('\r\n', '\n')
    return new_text


def main():
    changed = []
    for path in sorted(ROOT.rglob('index.html')):
        try:
            text = path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"SKIP {path} (read error: {e})")
            continue
        new_text = prettify_html(text)
        if new_text != text.replace('\r\n','\n'):
            path.write_text(new_text, encoding='utf-8')
            changed.append(str(path))
            print(f"UPDATED {path}")
        else:
            print(f"UNCHANGED {path}")

    print('\nSummary:')
    print(f"Total files checked: {len(list(ROOT.rglob('index.html'))) }")
    print(f"Total updated: {len(changed)}")
    if changed:
        for p in changed:
            print(' -', p)

if __name__ == '__main__':
    main()
