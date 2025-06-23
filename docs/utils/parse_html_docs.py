#!/usr/bin/env python3
"""
Utility script to extract API documentation sections from raw HTML docs.

Usage:
  python parse_html_docs.py -i docs/raw__ReponseSpec.html -o docs/parsed_api_docs.html

Requirements:
  pip install beautifulsoup4
"""

import argparse
import sys

try:
    from bs4 import BeautifulSoup
except ImportError:
    sys.stderr.write("Error: beautifulsoup4 is required. Install with: pip install beautifulsoup4\n")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Extract API model sections from raw HTML docs"
    )
    parser.add_argument(
        "-i", "--input",
        default="docs/raw__ReponseSpec.html",
        help="Path to the raw HTML file (default: docs/raw__ReponseSpec.html)"
    )
    parser.add_argument(
        "-o", "--output",
        default="docs/parsed_api_docs.html",
        help="Path to the output file with extracted sections"
    )
    args = parser.parse_args()

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            html = f.read()
    except Exception as e:
        sys.stderr.write(f"Error reading input file '{args.input}': {e}\n")
        sys.exit(1)

    soup = BeautifulSoup(html, "html.parser")

    sections = []
    for section in soup.find_all("section", id=True):
        if section.find("table"):
            sections.append(section)

    if not sections:
        sys.stderr.write("No model sections found in the input HTML.\n")
        sys.exit(1)

    try:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write("<!DOCTYPE html>\n<html>\n<body>\n")
            for sec in sections:
                f.write(str(sec))
                f.write("\n")
            f.write("</body>\n</html>\n")
    except Exception as e:
        sys.stderr.write(f"Error writing output file '{args.output}': {e}\n")
        sys.exit(1)

    print(f"Extracted {len(sections)} section(s) to '{args.output}'")


if __name__ == "__main__":
    main()