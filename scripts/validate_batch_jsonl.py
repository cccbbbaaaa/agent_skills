#!/usr/bin/env python3
"""Validate basic JSONL structure for LLM batch requests."""

import argparse
import json
import sys
from pathlib import Path


def validate_line(obj, line_no, seen_ids):
    errors = []
    warnings = []

    custom_id = obj.get("custom_id")
    if not custom_id:
        errors.append("missing custom_id")
    elif custom_id in seen_ids:
        errors.append(f"duplicate custom_id: {custom_id}")
    else:
        seen_ids.add(custom_id)

    if obj.get("method") != "POST":
        errors.append("method should be POST")

    if not obj.get("url"):
        errors.append("missing url")

    body = obj.get("body")
    if not isinstance(body, dict):
        errors.append("missing body object")
        return errors, warnings

    if not body.get("model"):
        errors.append("body missing model")

    if body.get("stream") is True:
        errors.append("batch requests should not use stream=true")

    if "temperature" in body and isinstance(body["temperature"], (int, float)) and body["temperature"] > 0.3:
        warnings.append("temperature > 0.3; risky for classification/extraction batch jobs")

    has_input = "input" in body
    has_messages = "messages" in body
    if not has_input and not has_messages:
        errors.append("body should contain input or messages")

    if "max_output_tokens" not in body and "max_tokens" not in body:
        warnings.append("missing max output token limit")

    return [f"line {line_no}: {e}" for e in errors], [f"line {line_no}: {w}" for w in warnings]


def main():
    parser = argparse.ArgumentParser(description="Validate LLM batch JSONL request files.")
    parser.add_argument("path", help="Path to a .jsonl batch request file")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2

    seen_ids = set()
    errors = []
    warnings = []
    total = 0

    with path.open("r", encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, 1):
            line = raw.strip()
            if not line:
                continue
            total += 1
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_no}: invalid JSON: {exc}")
                continue
            if not isinstance(obj, dict):
                errors.append(f"line {line_no}: top-level value must be an object")
                continue
            line_errors, line_warnings = validate_line(obj, line_no, seen_ids)
            errors.extend(line_errors)
            warnings.extend(line_warnings)

    print(f"checked_lines={total}")
    print(f"errors={len(errors)}")
    print(f"warnings={len(warnings)}")

    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARNING: {message}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
