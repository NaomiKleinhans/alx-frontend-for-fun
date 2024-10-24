#!/usr/bin/python3
"""
markdown2html.py: A script that converts Markdown to HTML.
Usage: ./markdown2html.py input.md output.html
"""
import sys
import os


def parse_line(line):
    """
    Convert a line of Markdown into its corresponding HTML.

    - Converts Markdown headings (#, ##, etc.) into <h1>, <h2>, ..., <h6>
    - Converts unordered list items (- item) into <li> within <ul>
    - Converts ordered list items (* item) into <li> within <ol>
    - Wraps any other text into <p> paragraphs

    Args:
        line (str): A line of Markdown text.
    
    Returns:
        str: The corresponding HTML string.
    """
    # Heading conversion
    if line.startswith('#'):
        heading_level = len(line.split(' ')[0])
        if heading_level > 6:
            heading_level = 6
        return f"<h{heading_level}>{line[heading_level+1:].strip()}</h{heading_level}>"

    # Unordered list item (- item)
    elif line.startswith('- '):
        return f"<li>{line[2:].strip()}</li>"

    # Ordered list item (* item)
    elif line.startswith('* '):
        return f"<li>{line[2:].strip()}</li>"

    # Paragraph (wrap in <p>)
    else:
        return f"<p>{line.strip()}</p>"


if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py input.md output.html", file=sys.stderr)
        sys.exit(1)

    markdown_file = sys.argv[1]  # Input Markdown file
    output_file = sys.argv[2]    # Output HTML file

    # Check if the Markdown file exists
    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    # Open the Markdown file and output HTML file
    with open(markdown_file, 'r') as md_file, open(output_file, 'w') as html_file:
        in_ul = False  # Track if we're inside an unordered list
        in_ol = False  # Track if we're inside an ordered list

        for line in md_file:
            # Handle unordered list (- item)
            if line.startswith('- '):
                if not in_ul:
                    html_file.write("<ul>\n")
                    in_ul = True
                html_file.write(parse_line(line) + '\n')

            # Handle ordered list (* item)
            elif line.startswith('* '):
                if not in_ol:
                    html_file.write("<ol>\n")
                    in_ol = True
                html_file.write(parse_line(line) + '\n')

            else:
                # Close the unordered list if one was open
                if in_ul:
                    html_file.write("</ul>\n")
                    in_ul = False

                # Close the ordered list if one was open
                if in_ol:
                    html_file.write("</ol>\n")
                    in_ol = False

                # Write paragraphs or headings
                html_file.write(parse_line(line) + '\n')

        # Ensure we close any open lists at the end of the file
        if in_ul:
            html_file.write("</ul>\n")
        if in_ol:
            html_file.write("</ol>\n")

    # Exit the script successfully
    sys.exit(0)
