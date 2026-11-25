#!/usr/bin/env python3
"""Have You Tried Turning It Off? -- a make.fun program/v1 entry.

Writes one funny line -- a hopeless tech support agent's reply to a
desperate customer -- to entry.txt in the output directory.

Pure Python standard library. Deterministic: the same bytes on every
run. No network, no clock, no randomness, and it never chmods anything.
"""

import os
import sys

LINE = (
    "Turn it off, wait ten seconds, turn it back on. "
    "If it still won't start, we'll restart me instead "
    "— it works on most of our agents."
)


def check_line(line):
    """Mirror the bounty gate: UTF-8 text of 1 to 199 characters,
    not only white space. Raises ValueError on a line that would fail.
    """
    if not 1 <= len(line) <= 199:
        raise ValueError("line must be 1..199 characters")
    if not line.strip():
        raise ValueError("line must not be only white space")


def candidate_paths():
    """Output paths for entry.txt, best first, de-duplicated:

    1. $MAKEFUN_OUTPUT_DIR/entry.txt -- where the grader looks;
    2. /output/entry.txt -- the harness default;
    3. entry.txt beside this script -- a last resort for local runs.
    """
    paths = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        paths.append(os.path.join(env_dir, "entry.txt"))
    paths.append(os.path.join("/output", "entry.txt"))
    here = os.path.dirname(os.path.abspath(__file__))
    paths.append(os.path.join(here, "entry.txt"))
    seen = set()
    unique = []
    for path in paths:
        if path not in seen:
            seen.add(path)
            unique.append(path)
    return unique


def write_entry():
    """Write LINE to the first candidate path that accepts it.

    Every path is tried in order and an OSError on one path never
    stops the next from being tried. Returns the path written, or
    None when every candidate failed.
    """
    data = LINE.encode("utf-8")
    for target in candidate_paths():
        try:
            with open(target, "wb") as fh:
                fh.write(data)
        except OSError:
            continue
        return target
    return None


def main():
    check_line(LINE)
    written = write_entry()
    if written is None:
        print("error: could not write entry.txt anywhere", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
