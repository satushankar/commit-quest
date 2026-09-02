# Commit Quest - start here

Read this whole page once before you touch anything. It takes two minutes and
will save you twenty.

## What this is

Six riddles are hidden in this repository's history. Solving one gives you a
word. That word unlocks the next riddle. The sixth unlocks the final task, which
is opening a Pull Request - your first real contribution on GitHub.

Solo event. Four days. No coding required.

## What you need

- **Git.** `git --version` should print something.
- **Python 3.** `python3 --version` should print something. On Windows try `py --version`.
- **A GitHub account.**

If any of those three fail, ask in the help channel. That is exactly what
mentors are for.

## Setting up

1. **Fork this repository.** Hit the Fork button, top right of this page. That
   gives you your own copy. Do not use "Use this template" - it will break your
   final submission, because a template copy cannot open a Pull Request back
   here.

2. **Clone your fork** to your machine:

   ```
   git clone https://github.com/<your-username>/commit-quest.git
   cd commit-quest
   ```

   Use the URL of *your* fork, with your username in it.

3. Start digging. The first clue is at the bottom of [README.md](README.md).

## Unlocking each stage

Every riddle answer is a single lowercase word unless the clue says otherwise.
Feed it to the decoder along with the stage file:

```
python3 tools/decode.py .quest/stage2.enc <your-answer>
```

Wrong answer, it says so and nothing breaks. Guess as many times as you like.

Note: the `.quest` and `tools` folders only exist on `main`. If you have checked
out an old branch or an old commit and the decoder says the file is missing, run
`git checkout main` and try again.

## Submitting

**Stages 1 to 6:** submit each answer through the form as you get it.

> Form: https://docs.google.com/forms/d/e/1FAIpQLSfUjKyO6nujNiBJRF26UZhkSqZjBFtxdCjqNcnOLNMlOjUFPQ/viewform

The form asks which commands you used. Answer it honestly - it is worth points,
and it is how we award the clean-process bonus.

**The final answer:** not through the form. Stage 6 unlocks instructions for
opening a Pull Request, and the Pull Request is your submission. A bot checks it
and comments back within a couple of minutes.

## Rules

- Do not post answers, keys, or the final phrase in any public channel. Escape
  room etiquette. Let people find things themselves.
- Mentors help with Git mechanics only ("how do I check out a branch"), never
  with riddle answers.
- One final Pull Request per person. Its timestamp settles the ranking.
- GitHub Desktop is fine if you prefer buttons to commands, but the clues assume
  the command line and you will have an easier time with it.

Scoring, timings and hint drops: [docs/RULES.md](docs/RULES.md)
Never used Git before: [docs/git-primer.md](docs/git-primer.md)

## If you get stuck

Getting stuck is the event. Sit with it for a bit. A hint drops every day at
noon in the help channel, and they get more explicit as the week goes on.

Nothing you can type will permanently break your fork. If it gets into a state
you do not understand, delete the folder, clone it again, and carry on.
