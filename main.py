#!/usr/bin/env python3
"""Write the dad-joke entry for Dad Joke Showdown.

The entry is a single dad joke of at most 200 characters. This
program assembles the joke from its parts, validates the result,
writes it to /output/entry.txt as UTF-8 with no trailing newline,
and reads it back for a byte-for-byte comparison.
"""

import os
import sys

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200

# The joke is built from its beats rather than stored as one
# literal: a setup about code telling a joke, the protocol named
# in the middle, and the two-part shrug that lands the punchline.
SETUP_HEAD = "My code told me a "
PROTOCOL = "UDP"
SETUP_TAIL = " joke "
DASH = "—"
PUNCH_A = " I didn't get it, "
PUNCH_B = "and it didn't care."
JOKE_PARTS = (SETUP_HEAD, PROTOCOL, SETUP_TAIL, DASH, PUNCH_A, PUNCH_B)


def assemble_joke() -> str:
    """Return the dad joke assembled from its parts."""
    return "".join(JOKE_PARTS)


def validate_joke(text: str) -> None:
    """Raise ValueError if the assembled joke breaks any rule."""
    if not text or not text.strip():
        raise ValueError("joke must not be empty or only whitespace")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(f"joke must be 1 to {MAX_CHARS} characters, got {len(text)}")
    if "\n" in text or "\r" in text:
        raise ValueError("joke must be a single line with no newline")
    if text != text.strip():
        raise ValueError("joke must not have leading or trailing whitespace")
    if "\t" in text:
        raise ValueError("joke must not contain a tab")
    if text.endswith(" ") or text.endswith("\n"):
        raise ValueError("joke must not end with whitespace")
    if not text.endswith("."):
        raise ValueError("joke must end with its punchline full stop")
    if PROTOCOL not in text:
        raise ValueError("joke must name the protocol it is about")
    # The punchline must stay in its two halves and in order: the
    # teller not getting it, then the joke not caring.
    rebuilt = SETUP_HEAD + PROTOCOL + SETUP_TAIL + DASH + PUNCH_A + PUNCH_B
    if text != rebuilt:
        raise ValueError("joke must match its assembled parts exactly")
    if text.index(PUNCH_A) > text.index(PUNCH_B):
        raise ValueError("punchline halves must stay in order")
    encoded = text.encode("utf-8")
    if encoded.decode("utf-8") != text:
        raise ValueError("joke must survive a UTF-8 round trip")
    if len(encoded) > MAX_CHARS * 4:
        raise ValueError("joke must fit the byte budget for its character limit")


def main() -> int:
    joke = assemble_joke()
    validate_joke(joke)

    payload = joke.encode("utf-8")
    out_dir = os.path.dirname(OUTPUT_PATH)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(OUTPUT_PATH, "wb") as fh:
        fh.write(payload)

    with open(OUTPUT_PATH, "rb") as fh:
        written = fh.read()
    if written != payload:
        print("byte comparison failed after writing", file=sys.stderr)
        return 1
    if written.decode("utf-8") != joke:
        print("round-trip text mismatch after writing", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
