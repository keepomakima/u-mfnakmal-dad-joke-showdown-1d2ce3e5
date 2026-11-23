#!/usr/bin/env python3
"""Dad Joke Showdown — make.fun entry v1.

A Python program that writes ONE dad joke to /output/entry.txt.

Stdlib only, no network, no fonts, no third-party imports: the grade
run happens in a bare Python 3.13 image, so this program must run with
`python3 -P -s` in a clean interpreter.

v1 joke (105 characters, 1 line): Dad loves the air fryer because it
is a little oven with a really big fan club. The pun turns on "fan"
(the fryer's fan / a fan club), lands on the first read, is fresh
(air fryer, not a recycled classic), and the punchline is the last
phrase — criteria 2, 3 and 4 of the judge's brief, in a father's
voice at the table (criteria 1 and 5).
"""

import os
from pathlib import Path

JOKE = "I asked Dad why he loves the air fryer. 'It's just a little oven,' he said, 'with a really big fan club.'"


def main() -> None:
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "entry.txt"
    # Atomic write: write to a temp file in the same directory, then
    # rename over entry.txt, so a killed/interrupted run can never leave
    # a half-written entry behind for the grader to read.
    tmp_path = output_path.with_suffix(".tmp")
    tmp_path.write_text(JOKE + "\n", encoding="utf-8")
    os.replace(tmp_path, output_path)
    # Read back and verify: the entry must be 1-200 Unicode code points
    # of non-whitespace text (the bounty gate), or the run fails loudly
    # instead of silently producing an invalid file.
    written = output_path.read_text(encoding="utf-8")
    if written != JOKE + "\n":
        raise SystemExit("FAIL: entry.txt content does not match the joke exactly")
    if not 1 <= len(written) <= 200:
        raise SystemExit(
            f"FAIL: entry.txt is {len(written)} characters, outside 1-200"
        )
    if not written.strip():
        raise SystemExit("FAIL: entry.txt must not be only whitespace")
    if written.count("\n") != 1:
        raise SystemExit("FAIL: entry.txt must be exactly one line")


if __name__ == "__main__":
    main()
