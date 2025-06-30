#!/usr/bin/env python3
"""
Generate Pydantic models from parsed API documentation HTML.

Usage:
  python generate_models.py \
      -i docs/raw/parsed_api_docs.html \
      -o httpobjects_gen.py
"""

import re
import sys
import argparse

from bs4 import BeautifulSoup


def parse_type(raw: str) -> str:
    s = raw.strip()
    # Literal strings in quotes
    if s.startswith('"') and s.endswith('"'):
        val = s.strip('"')
        return f'Literal["{val}"]'
    # List of items
    m = re.match(r"list\s*\[\s*(.+?)\s*\]$", s, re.IGNORECASE)
    if m:
        inner = m.group(1)
        # Recursively parse inner type
        inner_type = parse_type(inner)
        return f"list[{inner_type}]"
    # Basic type mappings
    low = s.lower()
    if low in ("string", "str"):
        return "str"
    if low in ("integer", "int"):
        return "int"
    if low in ("number", "float"):
        return "float"
    if low in ("boolean", "bool"):
        return "bool"
    # Fallback to raw
    return s


def extract_models(
    soup: BeautifulSoup,
) -> list[tuple[str, str, list[tuple[str, str, bool, str]]]]:
    models: list[tuple[str, str, list[tuple[str, str, bool, str]]]] = []
    for section in soup.find_all("section", id=True):
        name = section.get("id") or ""
        # description text
        desc_el = section.find("div", class_="model-description")
        description = desc_el.get_text(strip=True) if desc_el else ""
        table = section.find("table")
        if not table:
            continue
        fields: list[tuple[str, str, bool, str]] = []
        rows = table.find_all("tr")
        for tr in rows[1:]:
            cols = tr.find_all("td")
            if len(cols) < 4:
                continue
            field = cols[0].get_text(strip=True)
            raw_type = cols[1].get_text(strip=True)
            required = cols[2].get_text(strip=True).lower() == "true"
            desc = cols[3].get_text(strip=True)
            ftype = parse_type(raw_type)
            fields.append((field, ftype, required, desc))
        models.append((name, description, fields))
    return models


def render_models(
    models: list[tuple[str, str, list[tuple[str, str, bool, str]]]],
) -> str:
    lines: list[str] = []
    imports: set[str] = {
        "from __future__ import annotations",
        "from pydantic import BaseModel",
    }
    # detect typing imports
    for _, _, fields in models:
        for _, ftype, required, _ in fields:
            if not required:
                imports.add("from typing import Optional")
            if "Literal[" in ftype:
                imports.add("from typing import Literal")
            if re.match(r"list\[", ftype):
                imports.add("from typing import List")
    # write imports
    for imp in sorted(imports):
        lines.append(imp)
    lines.append("")

    # render each model
    for name, description, fields in models:
        lines.append(f"class {name}(BaseModel):")
        if description:
            lines.append(f'    """{description}"""')
        if not fields:
            lines.append("    pass")
        for field, ftype, required, _ in fields:
            default = "" if required else " = None"
            lines.append(f"    {field}: {ftype}{default}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Pydantic models from parsed API docs HTML"
    )
    parser.add_argument(
        "-i",
        "--input",
        default="docs/raw/parsed_api_docs.html",
        help="Parsed HTML with API sections",
    )
    parser.add_argument(
        "-o", "--output", help="Output Python file (defaults to stdout)"
    )
    args = parser.parse_args()

    try:
        with open(args.input, encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
    except Exception as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        sys.exit(1)

    models = extract_models(soup)
    code = render_models(models)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(code)
        except Exception as e:
            print(f"Error writing output: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(code)


if __name__ == "__main__":
    main()
