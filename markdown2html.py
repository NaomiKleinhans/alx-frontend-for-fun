#!/usr/bin/python3
import sys
import re
import hashlib


def parse_md_to_html(md_line):
    # Headings
    heading_match = re.match(r'^(#{1,6}) (.+)', md_line)
    if heading_match:
        level = len(heading_match.group(1))
        content = heading_match.group(2)
        return f"<h{level}>{content}</h{level}>"

    # Unordered list
    if md_line.startswith("- "):
        return f"<ul><li>{md_line[2:].strip()}</li></ul>"

    # Ordered list
    if md_line.startswith("* "):
        return f"<ol><li>{md_line[2:].strip()}</li></ol>"

    # Bold and emphasis
    md_line = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', md_line)
    md_line = re.sub(r'__(.+?)__', r'<em>\1</em>', md_line)

    # MD5 and 'c' replacement
    md_line = re.sub(
        r'\[\[(.+?)\]\]', lambda x: hashlib.md5(x.group(1).encode()).hexdigest(), md_line)
    md_line = re.sub(
        r'\(\((.+?)\)\)', lambda x: x.group(1).replace("c", "").replace("C", ""), md_line)

    # Paragraph with line breaks
    if md_line:
        return f"<p>{md_line.replace('\n', '<br/>')}</p>"
    return ''


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    md_filename = sys.argv[1]
    html_filename = sys.argv[2]

    try:
        with open(md_filename, 'r') as md_file, open(html_filename, 'w') as html_file:
            for line in md_file:
                html_line = parse_md_to_html(line.strip())
                if html_line:
                    html_file.write(html_line + "\n")
    except FileNotFoundError:
        print(f"Missing {md_filename}", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)
