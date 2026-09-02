#!/usr/bin/env python3
"""Decoder for Commit Quest.

Usage:

    python3 tools/decode.py .quest/stage2.enc <answer>

On Windows, if python3 is not recognised, use py instead:

    py tools/decode.py .quest/stage2.enc <answer>

Nothing to install. If you have Python 3, you have everything this needs.
"""

import base64
import hashlib
import sys

MAGIC = b"COMMITQUEST/v1"


def keystream(key, length):
    key_bytes = key.strip().lower().encode("utf-8")
    out = bytearray()
    counter = 0
    while len(out) < length:
        out += hashlib.sha256(key_bytes + b"|" + str(counter).encode()).digest()
        counter += 1
    return bytes(out[:length])


def xor(data, key):
    return bytes(a ^ b for a, b in zip(data, keystream(key, len(data))))


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 tools/decode.py <file.enc> <answer>")
        return 2

    path, answer = sys.argv[1], sys.argv[2]

    try:
        with open(path) as handle:
            blob = handle.read()
    except FileNotFoundError:
        print("No file at %s" % path)
        print("Check the path. If you are on a branch other than main, run")
        print("'git checkout main' first - the quest files only live on main.")
        return 1

    try:
        raw = base64.b64decode("".join(blob.split()))
    except Exception:
        print("That file is not a quest file.")
        return 1

    body = xor(raw, answer)

    if not body.startswith(MAGIC + b"\n"):
        print("Wrong key. That is not the answer.")
        print("Re-read the clue. Answers are single lowercase words unless the")
        print("clue says otherwise, and spelling counts.")
        return 1

    print(body[len(MAGIC) + 1:].decode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
