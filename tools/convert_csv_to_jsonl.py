#!/usr/bin/env python3
"""Minimal CSV to JSONL converter."""

import csv
import json
import sys
from pathlib import Path


def csv_to_jsonl(csv_file: str, jsonl_file: str = None):
    """Convert CSV to JSONL."""
    csv_path = Path(csv_file)

    if not csv_path.exists():
        print(f"Error: File not found: {csv_file}")
        return False

    jsonl_file = jsonl_file or csv_path.with_suffix(".jsonl")

    try:
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            data = list(reader)

        with open(jsonl_file, "w") as f:
            for row in data:
                f.write(json.dumps(row) + "\n")

        print(f"✓ Converted {len(data)} rows to {jsonl_file}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_csv_to_jsonl.py <input.csv> [output.jsonl]")
        sys.exit(1)

    csv_to_jsonl(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
