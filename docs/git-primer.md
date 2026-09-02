# Git in fifteen minutes

Enough Git to play Commit Quest. No prior experience assumed.

## What Git actually is

Git is a time machine for a folder.

Every time you tell it to, Git takes a snapshot of your project and stores it
forever, along with a note about what changed and who did it. It never throws a
snapshot away. That is the entire idea, and it is why this hunt works: things
people deleted years ago are still in there.

**GitHub** is a website that hosts these folders so people can share them. Git
is the tool; GitHub is the place. They are not the same thing.

## The words

| Word | What it means |
|---|---|
| **repository** ("repo") | A folder Git is watching. |
| **commit** | One snapshot, plus a message explaining it. |
| **branch** | A parallel line of snapshots. `main` is the default one. |
| **tag** | A permanent label stuck on one particular commit. |
| **clone** | Download a repository to your machine. |
| **fork** | Make your own copy of somebody else's repository on GitHub. |
| **push** | Send your commits up to GitHub. |
| **pull request** ("PR") | Ask someone to take your changes into their repository. |

## Setup, once

Check it is installed:

```
git --version
```

Nothing? Install from https://git-scm.com/downloads

Tell Git who you are. This gets stamped on every commit you make:

```
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Use the email on your GitHub account, so your commits get linked to you.

## Fork, then clone

**Fork** on the repository page, top right. You now have your own copy at
`github.com/<your-username>/commit-quest`.

**Clone** it to your machine:

```
git clone https://github.com/<your-username>/commit-quest.git
cd commit-quest
```

Your username, not anyone else's. Everything below is run from inside that
folder.

## Looking around

```
git status
```

What is going on right now. When confused, run this first.

```
git log
```

Every commit, newest first: who, when, and the message. Press `q` to get out.

```
git log --oneline
```

The same thing, one line each. Much easier to scan.

## Moving through time

```
git branch -a
```

Every branch, including ones you have not looked at.

```
git checkout <branch-name>
```

Switch the folder's contents to that branch. Your files change on disk. This is
not destructive - `git checkout main` puts everything back.

```
git tag
git show <tag-name>
```

List the labels, then read one. Tags can carry a message of their own.

## Asking who and what

```
git blame <file>
```

For every line in a file, which commit last touched it and who wrote that
commit. It is not an accusation, it is just the word Git uses.

```
git diff <thing-a> <thing-b>
```

What changed between two points. Lines starting `-` were removed, lines starting
`+` were added. `-` lines are the interesting ones in this hunt.

```
git show <commit-hash>
```

Everything about one commit. You can also read a single file as it was at that
commit:

```
git show <commit-hash>:path/to/file
```

That works even if the file has since been deleted, which is the whole point.

## Making a change and getting it merged

This is the final stage, and the only part where you write anything.

```
git checkout -b my-branch-name
```

Make a new branch and switch to it. Never work directly on `main`.

Make or edit your file, then:

```
git add path/to/your/file
git commit -m "a message saying what you did"
```

`add` picks what goes in the snapshot. `commit` takes it.

```
git push origin my-branch-name
```

Sends the branch to your fork on GitHub.

Then go to your fork on GitHub. There will be a **Compare & pull request**
button. Click it. **Check that it is pointing at the original repository's
`main`**, not your own fork's main. Give it a title, open it.

That is a contribution. That is the whole thing people put on their CVs.

## Windows notes

`python3` may not be recognised. Try:

```
py tools/decode.py .quest/stage2.enc <answer>
```

Use Git Bash (installed with Git) rather than Command Prompt. The commands here
are written for it.

## Things that will worry you but are fine

**"detached HEAD"** - you checked out a commit rather than a branch. You have
not broken anything. `git checkout main` returns you to normal.

**An editor opened and you cannot escape** - it is probably Vim. Press `Esc`,
then type `:q!` and Enter. Use `git commit -m "message"` to avoid it entirely.

**You deleted or mangled files** - `git checkout main` then
`git checkout -- .` restores everything tracked.

**Total confusion** - delete the folder and clone again. You lose nothing that
matters.

## The ten commands this hunt needs

```
git clone <url>
git status
git log
git log --oneline
git branch -a
git checkout <branch>
git tag
git show <thing>
git blame <file>
git diff <a> <b>
```

Plus `add`, `commit`, `push` at the very end. That is it.
