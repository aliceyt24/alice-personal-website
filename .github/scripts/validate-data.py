#!/usr/bin/env python3
"""Check that every file in data/ is valid JSON.

Hugo refuses to build the whole site if any data file has a syntax error, so a
single stray comma or missing brace takes the site offline. Python's own error
messages are accurate but cryptic, so this reprints them with the offending
line, a caret under the exact spot, and a plain-English hint.

Run locally with:  python3 .github/scripts/validate-data.py
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data"

# Cryptic json module messages -> what actually went wrong, in plain English.
HINTS = (
    ("Expecting ',' delimiter",
     "An entry probably isn't closed. Each one looks like:\n"
     '          {  "summary": "..."  },\n'
     "      Check for a missing } at the end of the entry, or a missing comma between entries."),
    ("Expecting property name enclosed in double quotes",
     "There's likely a trailing comma after the last entry, or a key is missing its quotes."),
    ("Expecting value",
     "Usually a comma too many — check for a stray , just before the ] or }.\n"
     "      The last entry in the list must NOT have a comma after it."),
    ("Expecting ':' delimiter",
     'A key is missing its colon. Keys look like:  "summary": "..."'),
    ("Unterminated string",
     'A quote is missing. Every piece of text needs one at each end: "like this"'),
    # Python reports a missing closing quote this way when the text runs to a newline.
    ("Invalid control character",
     'A closing quote is missing. Every piece of text needs one at each end: "like this"'),
    ("Extra data",
     "There's content after the final ] — possibly a duplicated or stray closing bracket."),
)


def hint_for(message):
    for needle, advice in HINTS:
        if needle in message:
            return advice
    return None


def check(path):
    """Return True if path holds valid JSON, printing a readable report if not."""
    rel = path.relative_to(REPO_ROOT)
    text = path.read_text(encoding="utf-8")

    try:
        json.loads(text)
    except json.JSONDecodeError as err:
        print(f"\n  ✗ {rel} is not valid JSON")
        print(f"      Line {err.lineno}, column {err.colno}: {err.msg}\n")

        lines = text.splitlines()
        if 0 < err.lineno <= len(lines):
            line = lines[err.lineno - 1]
            # Long prose lines would wrap and misalign the caret, so show a
            # window around the error instead of the whole line.
            start = max(0, err.colno - 40)
            snippet = line[start:err.colno + 20]
            prefix = f"      {err.lineno} | "
            ellipsis = "..." if start > 0 else ""
            print(f"{prefix}{ellipsis}{snippet}")
            print(" " * (len(prefix) + len(ellipsis) + (err.colno - 1 - start)) + "^")

        advice = hint_for(err.msg)
        if advice:
            print(f"\n      Hint: {advice}")

        print(f"\n      Paste the file into https://jsonlint.com to find it visually.")
        return False

    print(f"  ✓ {rel}")
    return True


def main():
    if not DATA_DIR.is_dir():
        print(f"No data/ directory found at {DATA_DIR}", file=sys.stderr)
        return 1

    files = sorted(DATA_DIR.glob("*.json"))
    if not files:
        print("No JSON files in data/ — nothing to check.")
        return 0

    print(f"Checking {len(files)} data file(s)...\n")
    failed = [p for p in files if not check(p)]

    if failed:
        names = ", ".join(str(p.relative_to(REPO_ROOT)) for p in failed)
        print(f"\n{len(failed)} file(s) need fixing: {names}")
        print("The website will NOT update until this is corrected.")
        return 1

    print("\nAll data files are valid. The website will build.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
