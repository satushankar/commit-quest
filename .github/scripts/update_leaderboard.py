#!/usr/bin/env python3
"""Append one verified submission and regenerate the leaderboard page.

Nobody edits the leaderboard by hand. It is rebuilt from results.json every
time, so concurrent merges cannot corrupt it.
"""

import json
import os
import re
import sys

DATA = "leaderboard/results.json"
PAGE = "leaderboard/README.md"
SPEED_CUTOFF = "2026-09-06T15:30:00Z"  # 6 Sep, 9pm IST


def load():
    try:
        with open(DATA) as handle:
            return json.load(handle)
    except (FileNotFoundError, ValueError):
        return []


def main():
    entries = load()
    author = os.environ["ENTRY_AUTHOR"]

    # This value ends up in a committed file and a commit message. GitHub
    # usernames cannot contain anything exotic, so anything that does not look
    # like one means something upstream is wrong and we stop rather than write it.
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})", author):
        print("refusing to record implausible author %r" % author, file=sys.stderr)
        return 1

    if not any(e["author"] == author for e in entries):
        entries.append({
            "author": author,
            "pr": int(os.environ["ENTRY_PR"]),
            "opened_at": os.environ["ENTRY_OPENED_AT"],
            "late": os.environ.get("ENTRY_LATE", "no") == "yes",
        })

    entries.sort(key=lambda e: e["opened_at"])

    os.makedirs("leaderboard", exist_ok=True)
    with open(DATA, "w") as handle:
        json.dump(entries, handle, indent=2)
        handle.write("\n")

    lines = [
        "# Commit Quest - finishers",
        "",
        "Everyone who solved all six stages and landed a correct pull request,",
        "in the order they opened it. Updated automatically.",
        "",
        "| # | Who | Finished (UTC) | Speed bonus | PR |",
        "|---|---|---|---|---|",
    ]
    rank = 0
    for entry in entries:
        if entry.get("late"):
            place = "late"
        else:
            rank += 1
            place = str(rank)
        bonus = "no" if entry.get("late") else ("yes" if entry["opened_at"] <= SPEED_CUTOFF else "no")
        lines.append("| %s | @%s | %s | %s | #%d |" % (
            place, entry["author"], entry["opened_at"].replace("T", " ").replace("Z", ""),
            bonus, entry["pr"]))

    lines += ["", "%d finisher(s) so far." % len(entries), ""]

    with open(PAGE, "w") as handle:
        handle.write("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
