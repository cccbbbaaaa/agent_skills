#!/usr/bin/env python3
"""Check whether an XML Prompt Contract contains core sections."""

import argparse
import re
import sys
from pathlib import Path


REQUIRED_TAGS = [
    "background",
    "role",
    "task",
    "input_schema",
    "requirements",
    "output_schema",
    "examples",
    "edge_cases",
    "current_input",
]


def count_tag(text, tag):
    pattern = rf"<{tag}(?:\s[^>]*)?>.*?</{tag}>"
    return len(re.findall(pattern, text, flags=re.DOTALL))


def main():
    parser = argparse.ArgumentParser(description="Validate core tags in an XML Prompt Contract.")
    parser.add_argument("path", help="Path to a prompt markdown, txt, or xml file")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2

    text = path.read_text(encoding="utf-8")
    errors = []
    warnings = []

    if "<prompt_contract" not in text:
        errors.append("missing <prompt_contract> root tag")

    for tag in REQUIRED_TAGS:
        count = count_tag(text, tag)
        if count == 0:
            errors.append(f"missing <{tag}>...</{tag}>")
        elif tag == "current_input" and count > 1:
            warnings.append("multiple <current_input> sections found; batch prompts should process one item at a time")

    if re.search(r"```(?:json|markdown|md)?", text):
        warnings.append("prompt contains fenced code blocks; ensure the model is told not to output fenced blocks")

    if "{{CURRENT_INPUT_JSON}}" not in text and "<current_input>" in text:
        warnings.append("consider using {{CURRENT_INPUT_JSON}} as the replacement placeholder")

    print(f"errors={len(errors)}")
    print(f"warnings={len(warnings)}")

    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARNING: {message}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
