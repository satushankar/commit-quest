#!/usr/bin/env python3
"""Compare a submitted answer against the stored hash and write the verdict.

The answer hash and its salt come from repository secrets, never from a file in
this repository, so nobody can pull the answer out of the history.
"""

import hashlib
import json
import os
import sys

DEADLINE = os.environ.get("DEADLINE", "")


def out(key, value):
    with open(os.environ["GITHUB_OUTPUT"], "a") as handle:
        if "\n" in str(value):
            handle.write("%s<<__EOF__\n%s\n__EOF__\n" % (key, value))
        else:
            handle.write("%s=%s\n" % (key, value))


def main():
    with open("result.json") as handle:
        result = json.load(handle)

    author = result["author"]
    pr = result["pr"]
    opened_at = result.get("opened_at", "")
    late = bool(DEADLINE and opened_at and opened_at > DEADLINE)

    out("pr", pr)
    out("author", author)
    out("opened_at", opened_at)
    out("late", "yes" if late else "no")

    if result["status"] != "parsed":
        out("verdict", "fail")
        out("message",
            "Not quite - this pull request is not shaped right yet.\n\n"
            + result["reason"]
            + "\n\nFix it, commit, and push to the same branch. This same pull "
              "request gets checked again automatically. No need to open a new one.")
        return 0

    salt = os.environ.get("FINAL_SALT", "")
    expected = os.environ.get("FINAL_ANSWER_HASH", "").strip().lower()
    if not expected:
        print("FINAL_ANSWER_HASH is not set", file=sys.stderr)
        return 1

    given = result["answer"].strip().lower()
    digest = hashlib.sha256((given + salt).encode("utf-8")).hexdigest()

    if digest != expected:
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
