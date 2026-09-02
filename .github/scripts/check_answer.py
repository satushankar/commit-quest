#!/usr/bin/env python3
"""Compare a submitted answer against the stored hash and write the verdict.

The answer hash and its salt come from repository secrets, never from a file in
this repository, so nobody can pull the answer out of the history.

Everything in result.json originates from a pull request, so it is treated as
hostile input: values are sanitised before they become workflow outputs, and
the multi-line delimiter is random so a crafted value cannot close it early and
inject an output of its own.
"""

import hashlib
import json
import os
import re
import secrets
import sys

DEADLINE = os.environ.get("DEADLINE", "")
CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def out(key, value):
    """Write a workflow output, safely.

    Single-line values are stripped of newlines entirely. Multi-line values get
    a random delimiter, which is what stops a crafted filename or answer from
    closing the heredoc and setting outputs of its own (verdict=pass, say).
    """
    value = CONTROL.sub(" ", str(value))
    path = os.environ["GITHUB_OUTPUT"]
    with open(path, "a") as handle:
        if "\n" in value:
            delimiter = "EOF_%s" % secrets.token_hex(16)
            while delimiter in value:
                delimiter = "EOF_%s" % secrets.token_hex(16)
            handle.write("%s<<%s\n%s\n%s\n" % (key, delimiter, value, delimiter))
        else:
            handle.write("%s=%s\n" % (key, value))


def main():
    with open("result.json") as handle:
        result = json.load(handle)

    # Shape checks. A malformed artifact means something is wrong upstream, and
    # the safe response is to refuse rather than to guess.
    author = str(result.get("author", ""))
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})", author):
        print("refusing: implausible author %r" % author, file=sys.stderr)
        return 1

    try:
        pr = int(result.get("pr"))
    except (TypeError, ValueError):
        print("refusing: bad pull request number", file=sys.stderr)
        return 1
    if pr <= 0:
        print("refusing: bad pull request number", file=sys.stderr)
        return 1

    head_sha = str(result.get("head_sha", ""))
    if not re.fullmatch(r"[0-9a-f]{40}", head_sha):
        print("refusing: bad head sha", file=sys.stderr)
        return 1

    opened_at = str(result.get("opened_at", ""))[:32]
    late = bool(DEADLINE and opened_at and opened_at > DEADLINE)

    out("pr", pr)
    out("author", author)
    out("head_sha", head_sha)
    out("opened_at", opened_at)
    out("late", "yes" if late else "no")

    if result.get("status") != "parsed":
        out("verdict", "fail")
        out("message",
            "Not quite - this pull request is not shaped right yet.\n\n"
            + str(result.get("reason", ""))[:1000]
            + "\n\nFix it, commit, and push to the same branch. This same pull "
              "request gets checked again automatically. No need to open a new one.")
        return 0

    salt = os.environ.get("FINAL_SALT", "")
    expected = os.environ.get("FINAL_ANSWER_HASH", "").strip().lower()
    if not expected:
        print("FINAL_ANSWER_HASH is not set", file=sys.stderr)
        return 1

    given = str(result.get("answer", "")).strip().lower()[:200]
    digest = hashlib.sha256((given + salt).encode("utf-8")).hexdigest()

    # Constant-time comparison. The hash is not a password, but there is no
    # reason to leak timing on it either.
    if not secrets.compare_digest(digest, expected):
        out("verdict", "fail")
        out("message",
            "That answer is not the one.\n\n"
            "The file is in the right place and the format is fine, so you are "
            "close - it is the answer itself that is wrong. Check for typos, and "
            "check you are submitting what stage 7 gave you rather than an "
            "earlier stage key.\n\n"
            "Fix the file, commit, push to the same branch, and this pull "
            "request gets re-checked.")
        return 0

    note = ""
    if late:
        note = ("\n\nThis came in after the deadline, so it is recorded but it "
                "does not place in the rankings.")

    out("verdict", "pass")
    out("message",
        "Correct. That is the whole quest.\n\n"
        "@%s - you just dug through a repository's history, recovered a deleted "
        "file, and opened a pull request against somebody else's project. That "
        "last part is a real open source contribution, and it is on your GitHub "
        "profile now.\n\nMerging this. Well played.%s" % (author, note))
    return 0


if __name__ == "__main__":
    sys.exit(main())
