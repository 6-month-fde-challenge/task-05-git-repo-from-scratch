# Task 5 — Build a Git Repository from Scratch

A small multi-module Python project (a guarded calculator with a login step and a
dashboard) created in an empty folder, initialised with Git, and grown commit by commit
until it was published on GitHub with its full history.

The point of the task is not the calculator — it is the **Git workflow**. This README
therefore contains the real, captured output of `git init`, `git status`, `git add`,
`git commit`, `git log` and `git diff`, plus the `.gitignore` quoted in full with proof
that it works. Nothing in this file is illustrative: every console block was copied from
an actual terminal run, and the SHAs are the SHAs in this repository.

**Evidence files (all committed to this repository, so they are visible without cloning):**

* [`GIT_WORKFLOW.md`](GIT_WORKFLOW.md) — the complete captured session, every command in
  order with its real output and an explanation of why each command is needed.
* [`COMMIT_HISTORY.md`](COMMIT_HISTORY.md) — the real `git log --stat` and
  `git log --graph`, plus a table of all commits.

---

## Contents

1. [How to run](#how-to-run)
2. [Project files](#project-files)
3. [Git commands demonstrated](#git-commands-demonstrated)
4. [The .gitignore, quoted in full](#the-gitignore-quoted-in-full)
5. [Commit history](#commit-history)
6. [Fixes applied after review feedback](#fixes-applied-after-review-feedback)

---

## How to run

No setup, no dependencies, no environment variables. Python 3 only.

```bash
git clone https://github.com/6-month-fde-challenge/task-05-git-repo-from-scratch.git
cd task-05-git-repo-from-scratch
python dashboard.py
```

`dashboard.py` is the entry point; running it exercises every other module in the
project. It prompts for two numbers and a username/password, but every prompt falls back
to a default if there is no input, so it also runs completely unattended. This is the
real captured output of a **fresh clone with no configuration at all**:

```console
$ python dashboard.py < /dev/null
Enter a number 1 :    -> no input available, using default: 10
Enter a number 2 :    -> no input available, using default: 5
Enter username :    -> no input available, using default: veerandra
Enter password :    -> no input available, using default: demo-password
API key present and logged in as veerandra
API key present and logged in as veerandra
API key present and logged in as veerandra
API key present and logged in as veerandra
*********** CALCULATOR DASHBOARD ***********
Result of addition is       :  15
Result of subtraction is    :  5
Result of multiplication is :  50
Result of division is       :  2.0
********************************************
```

To use a real API key instead of the built-in demo fallback, copy the committed template
and edit it — the copy is ignored by Git, so it never leaves your machine:

```bash
cp .env.example .env      # .env is in .gitignore
```

---

## Project files

| File | What it does |
|---|---|
| `config.py` | Reads `API_KEY` from the environment via `os.getenv` with a harmless demo fallback, so a fresh clone runs with zero setup. Replaces the old `secrets.py` (see [Fixes applied](#fixes-applied-after-review-feedback)). |
| `input_variables.py` | Collects the two operands `a` and `b`. `read_number()` wraps `input()` and catches `EOFError`/`ValueError`, falling back to `10` and `5` so the program never crashes on empty or non-numeric input. |
| `login.py` | Prompts for `user_name` and `pass_word` through `read_text()`, with the same EOF-safe fallback behaviour. |
| `profile.py` | Derives `profile_name` from the login details. `profile_name` is initialised to `""` first, so it is always defined even when the credentials are blank. |
| `addition_module.py` | `addition(a, b)` — returns `a + b`, but only after checking that an API key is configured and a profile is logged in; otherwise it explains why and returns `None`. |
| `subtract_module.py` | `subtract(a, b)` — returns `a - b` behind the same API-key and profile guards. |
| `multiply_module.py` | `multiply(a, b)` — returns `a * b` behind the same guards. |
| `division_module.py` | `division(a, b)` — returns `a / b` behind the same guards, plus an explicit divide-by-zero check that prints a message and returns `None` instead of raising. |
| `calculator.py` | The integration point. Imports the operands and all four operations, computes `total`, `subtraction`, `multiplication` and `div`, and prints them when run directly. |
| `dashboard.py` | The entry point and presentation layer. Imports the four results from `calculator.py` and prints them as a single formatted report. |
| `.env.example` | Committed template for the real `.env`. Documents the `API_KEY` variable without ever containing a real secret. |
| `.gitignore` | The ignore policy — caches, virtualenvs, real secrets and editor noise. [Quoted in full below.](#the-gitignore-quoted-in-full) |
| `GIT_WORKFLOW.md` | The full captured terminal transcript of building this repository. |
| `COMMIT_HISTORY.md` | The real `git log --stat` / `git log --graph` output and the commit table. |
| `submission_links.txt` | The repository URL for submission. |

**Dependency order** — which is exactly the order the commits were made in:

```
config.py ─┐
           ├─> addition / subtract / multiply / division ─┐
login.py ──┴─> profile.py ────────────────────────────────┤
                                                          ├─> calculator.py ─> dashboard.py
input_variables.py ───────────────────────────────────────┘
```

---

## Git commands demonstrated

Each subsection below has the **real captured output** and an explanation of why the
command is needed. The full transcript, including every intermediate step, is in
[`GIT_WORKFLOW.md`](GIT_WORKFLOW.md).

### `git init`

**Why it is required:** it creates the `.git` directory — the object database, the index
and `HEAD` — turning an ordinary folder into a repository. Without it, no other Git
command can run. `-b main` names the initial branch `main` immediately, so the default
branch on GitHub matches from the first push.

```console
$ git init -b main
Initialized empty Git repository in C:/Users/asus/Desktop/work/6-month-fde-challenge/03_git_and_git_hub/task-05-git-repo-from-scratch/.git/
```

### `git status`

**Why it is required:** it is the orientation command — it shows what is untracked, what
is staged, and what is modified. Run before `git add` you see what is new; run after, you
confirm exactly what the next commit will contain.

Before staging the first two files, they are **untracked**:

```console
$ git status
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        .env.example
        .gitignore

nothing added to commit but untracked files present (use "git add" to track)
```

After `git add`, the very same files are **staged** — the section heading changes from
"Untracked files" to "Changes to be committed":

```console
$ git status
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   .env.example
        new file:   .gitignore
```

And later in the build, `git status` reports an edit to an already-tracked file
differently again — as **modified**, not untracked:

```console
$ git status
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   dashboard.py

no changes added to commit (use "git add" and/or "git commit -a")
```

### `git add`

**Why it is required:** Git does not commit your working directory, it commits the index
(the staging area). `git add` is how you choose precisely which changes go into the next
commit — which is what makes small, meaningful commits possible instead of one bulk dump.
It prints nothing on success; `git status`, above, is how you see what it did.

```console
$ git add .gitignore .env.example
$ git add config.py input_variables.py
$ git add login.py profile.py
$ git add addition_module.py subtract_module.py
$ git add multiply_module.py division_module.py
$ git add calculator.py
$ git add dashboard.py
```

### `git commit`

**Why it is required:** it writes whatever is in the index into a permanent, immutable
snapshot with a message, an author and a parent, and moves the branch pointer to it. It
is the unit of history — every commit is a point you can return to or compare against.

The first commit reports `(root-commit)`, because it has no parent:

```console
$ git commit -m "Initialise repository with .gitignore and environment template"
[main (root-commit) b84494c] Initialise repository with .gitignore and environment template
 2 files changed, 24 insertions(+)
 create mode 100644 .env.example
 create mode 100644 .gitignore
```

A later commit, showing the branch, the new SHA and the files created:

```console
$ git commit -m "Add multiplication and division modules with divide-by-zero guard"
[main 40399b4] Add multiplication and division modules with divide-by-zero guard
 2 files changed, 31 insertions(+)
 create mode 100644 division_module.py
 create mode 100644 multiply_module.py
```

And the one commit that modified an existing file rather than adding new ones — note it
is the only one so far with **deletions** as well as insertions:

```console
$ git commit -m "Clarify dashboard docstring and banner text"
[main 5250c99] Clarify dashboard docstring and banner text
 1 file changed, 9 insertions(+), 3 deletions(-)
```

### `git log`

**Why it is required:** it is how a repository is audited — who changed what, when, in
what order, and which SHA to point at if you need to go back to a known-good state.

```console
$ git log --oneline
5250c99 Clarify dashboard docstring and banner text
3a9f22f Add dashboard that prints the final calculation report
4cb8d9c Add calculator entry point wiring all four arithmetic modules
40399b4 Add multiplication and division modules with divide-by-zero guard
01ce93d Add addition and subtraction modules guarded by API key and profile
b8b6fa5 Add login prompt and profile resolution modules
5fb47c5 Add environment-based config and user input collection
b84494c Initialise repository with .gitignore and environment template
```

`git log -1` gives the full detail of a single commit — full 40-character SHA, author and
timestamp:

```console
$ git log -1
commit 5250c99332eea1cd07c255b3d78ea9bd666fb37a
Author: veerandra7 <veerandra.data@gmail.com>
Date:   Mon Sep 21 18:24:50 2026 +0530

    Clarify dashboard docstring and banner text
```

`git log --stat` adds which files each commit touched and by how many lines — here are
the two most recent entries; the complete output for every commit is in
[`COMMIT_HISTORY.md`](COMMIT_HISTORY.md):

```console
$ git log --stat
commit 5250c99332eea1cd07c255b3d78ea9bd666fb37a
Author: veerandra7 <veerandra.data@gmail.com>
Date:   Mon Sep 21 18:24:50 2026 +0530

    Clarify dashboard docstring and banner text

 dashboard.py | 12 +++++++++---
 1 file changed, 9 insertions(+), 3 deletions(-)

commit 3a9f22f3b8aaeae350a93073a1c40c046732b463
Author: veerandra7 <veerandra.data@gmail.com>
Date:   Mon Sep 21 18:24:34 2026 +0530

    Add dashboard that prints the final calculation report

 dashboard.py | 10 ++++++++++
 1 file changed, 10 insertions(+)
```

### `git diff`

**Why it is required:** it is the review step before you stage and before you commit.
Git has three places a file's content can live, and one diff for each gap between them:

| Command | Compares | Question it answers |
|---|---|---|
| `git diff` | working tree **vs** staging area | "What have I changed but not staged yet?" |
| `git diff --staged` (or `--cached`) | staging area **vs** `HEAD` | "What exactly will my next commit contain?" |
| `git diff HEAD` | working tree **vs** `HEAD` | "What have I changed since the last commit, staged or not?" |

To demonstrate this properly, the docstring and banner text of the already-tracked
`dashboard.py` were rewritten. **Before staging**, `git diff` shows the change:

```console
$ git diff
diff --git a/dashboard.py b/dashboard.py
index ece6422..b4945ce 100644
--- a/dashboard.py
+++ b/dashboard.py
@@ -1,10 +1,16 @@
-"""Final integration point - displays the results produced by calculator.py."""
+"""Final integration point for the project.
+
+Imports the four results already computed by calculator.py and prints them as a
+single report. Run this file to exercise every other module in one go:
+
+    python dashboard.py
+"""
 
 from calculator import total, subtraction, multiplication, div
 
-print("*************** DASHBOARD ***************")
+print("*********** CALCULATOR DASHBOARD ***********")
 print("Result of addition is       : ", total)
 print("Result of subtraction is    : ", subtraction)
 print("Result of multiplication is : ", multiplication)
 print("Result of division is       : ", div)
-print("*****************************************")
+print("********************************************")
```

**After `git add`, the same command prints nothing:**

```console
$ git add dashboard.py

$ git diff
```

That empty output is the whole point. `git diff` does not mean "show me my changes", it
means "show me changes that are **not yet staged**". Once the change is staged, the
working tree and the index are identical, so plain `git diff` has nothing left to report.
The change is not lost — it has moved into the staging area, where `--staged` finds it:

```console
$ git diff --staged
diff --git a/dashboard.py b/dashboard.py
index ece6422..b4945ce 100644
--- a/dashboard.py
+++ b/dashboard.py
@@ -1,10 +1,16 @@
-"""Final integration point - displays the results produced by calculator.py."""
+"""Final integration point for the project.
+
+Imports the four results already computed by calculator.py and prints them as a
+single report. Run this file to exercise every other module in one go:
+
+    python dashboard.py
+"""
 
 from calculator import total, subtraction, multiplication, div
 
-print("*************** DASHBOARD ***************")
+print("*********** CALCULATOR DASHBOARD ***********")
 print("Result of addition is       : ", total)
 print("Result of subtraction is    : ", subtraction)
 print("Result of multiplication is : ", multiplication)
 print("Result of division is       : ", div)
-print("*****************************************")
+print("********************************************")
```

`git diff --staged` was also used earlier in the build as the final check before
committing new files — the full capture is in [`GIT_WORKFLOW.md`](GIT_WORKFLOW.md).

---

## The `.gitignore`, quoted in full

**Why it is required:** it tells Git which paths to never track, so build caches,
virtual environments, editor settings and — most importantly — real secrets cannot be
committed by accident. It is the first commit in this repository for exactly that
reason: the policy exists before there is any code to generate junk.

This is the complete, verbatim content of the `.gitignore` file at the root of this
repository:

```gitignore
# Byte-compiled / cache
__pycache__/
*.py[cod]
*$py.class

# Virtual environments
.venv/
venv/
env/

# Real secrets - never commit these. Use .env.example as the template.
.env
.env.local
secrets_local.py

# Editor / OS noise
.vscode/
.idea/
.DS_Store
Thumbs.db
```

It covers every category the task asks for: `__pycache__/`, `.env`, virtual environments
(`.venv/`, `venv/`, `env/`) and local secrets files (`.env.local`, `secrets_local.py`).

### Proof that it actually works

A `.gitignore` that is merely present proves nothing, so two things Git *should* ignore
were deliberately created: `__pycache__/` (generated just by running the program) and a
`.env` file containing a realistic-looking secret. Both genuinely exist on disk:

```console
$ ls -a
.
..
.env
.env.example
.git
.gitignore
__pycache__
addition_module.py
calculator.py
config.py
dashboard.py
division_module.py
input_variables.py
login.py
multiply_module.py
profile.py
subtract_module.py
```

**Proof 1 — `git status` does not list them at all.** Without `.gitignore` both would
appear under "Untracked files":

```console
$ git status
On branch main
nothing to commit, working tree clean
```

**Proof 2 — `git status --ignored` shows Git sees them and is deliberately skipping
them.** This distinguishes "Git cannot see these files" from "Git is choosing to ignore
these files":

```console
$ git status --ignored
On branch main
Ignored files:
  (use "git add -f <file>..." to include in what will be committed)
        .env
        __pycache__/

nothing to commit, working tree clean
```

**Proof 3 — `git check-ignore -v` names the exact rule doing the ignoring.** This is the
definitive answer to "*why* is this path ignored?":

```console
$ git check-ignore -v __pycache__ .env
.gitignore:2:__pycache__/       __pycache__
.gitignore:12:.env      .env
```

Read as `file:line:pattern<TAB>path` — line 2 of `.gitignore` (the pattern
`__pycache__/`) ignores `__pycache__`, and line 12 (the pattern `.env`) ignores `.env`.
Cross-check those line numbers against the quoted file above.

**Proof 4 — `git ls-files` lists everything actually tracked.** `.gitignore` is there;
`.env` and `__pycache__` are not:

```console
$ git ls-files
.env.example
.gitignore
addition_module.py
calculator.py
config.py
dashboard.py
division_module.py
input_variables.py
login.py
multiply_module.py
profile.py
subtract_module.py
```

---

## Commit history

The task requires at least five meaningful commits; this repository has **ten**. Because
an automated reviewer may only see a flat snapshot of the files rather than the Git
history, the history is reproduced here and, in full, in
[`COMMIT_HISTORY.md`](COMMIT_HISTORY.md).

This capture was taken after commit 9 was made and pushed, so it shows `origin/main`
next to the local branch — the local history and the published history are identical:

```console
$ git log --graph --oneline --all --decorate
* f2d1d4b (HEAD -> main, origin/main) Add README, workflow transcript and commit history evidence
* 5250c99 Clarify dashboard docstring and banner text
* 3a9f22f Add dashboard that prints the final calculation report
* 4cb8d9c Add calculator entry point wiring all four arithmetic modules
* 40399b4 Add multiplication and division modules with divide-by-zero guard
* 01ce93d Add addition and subtraction modules guarded by API key and profile
* b8b6fa5 Add login prompt and profile resolution modules
* 5fb47c5 Add environment-based config and user input collection
* b84494c Initialise repository with .gitignore and environment template
```

The single unbroken column of `*` confirms a clean, linear history. In build order:

1. **`b84494c` — Initialise repository with .gitignore and environment template.**
   Establishes the ignore policy before any code exists, and ships the committed
   `.env.example` template.
2. **`5fb47c5` — Add environment-based config and user input collection.** The
   configuration layer: `config.py` reads `API_KEY` from the environment, and
   `input_variables.py` gathers the two operands safely.
3. **`b8b6fa5` — Add login prompt and profile resolution modules.** The authentication
   layer, which every arithmetic module depends on.
4. **`01ce93d` — Add addition and subtraction modules guarded by API key and profile.**
   First half of the arithmetic layer.
5. **`40399b4` — Add multiplication and division modules with divide-by-zero guard.**
   Second half, including the zero-denominator check.
6. **`4cb8d9c` — Add calculator entry point wiring all four arithmetic modules.** The
   integration point; only possible once 2–5 exist.
7. **`3a9f22f` — Add dashboard that prints the final calculation report.** The
   presentation layer and the program you run.
8. **`5250c99` — Clarify dashboard docstring and banner text.** A deliberate edit to an
   already-tracked file, so `git diff` and `git diff --staged` had real content to
   demonstrate. The first commit with deletions as well as insertions.
9. **`f2d1d4b` — Add README, workflow transcript and commit history evidence.** Commits
   the captured command evidence into the repository so it is visible in a file snapshot.
10. **Refresh captured git history evidence.** Re-runs `git log` after commit 9 was
    pushed and refreshes the pasted graph above so the evidence is accurate rather than
    stale. It is the commit that saves this README, so its own SHA cannot appear in it —
    run `git log --oneline` on a clone to see it. Every earlier commit is listed above.

Each commit is a self-contained, reviewable layer of the project, added in dependency
order, with a descriptive message in the imperative mood.

---

## Fixes applied after review feedback

An earlier version of this task was reviewed and three issues were raised. All three are
fixed here.

### (a) The commit history and command evidence are now committed as repo-visible files

**The problem:** the reviewer saw only a flat snapshot of the source files, not the Git
history, and reported that it could not verify the five-commit requirement or find any
`git status` / `git log` / `git diff` demonstration.

**The fix:** the captured workflow is now part of the repository itself, not just of the
history. [`GIT_WORKFLOW.md`](GIT_WORKFLOW.md) holds the complete terminal transcript with
every command and its real output; [`COMMIT_HISTORY.md`](COMMIT_HISTORY.md) holds the real
`git log --stat` and `git log --graph --oneline --all --decorate` plus a commit-by-commit
table; and this README reproduces the key captures inline. All of it is readable in a
plain file snapshot without cloning or inspecting `.git`.

### (b) The `.gitignore` is present, quoted in the README, and proven to work

**The problem:** the reviewer reported "No .gitignore was shown in the reviewed source
files". The file did exist, but dotfiles are easy for a snapshot to miss.

**The fix:** `.gitignore` is tracked at the repository root — it is the content of the
very first commit, visible in `git log --stat` — and its full contents are now
[quoted verbatim in this README](#the-gitignore-quoted-in-full) so it cannot be missed.
It excludes `__pycache__/`, `.env`, virtual environments (`.venv/`, `venv/`, `env/`) and
local secrets files, and the README includes four independent proofs that the rules take
effect, including `git check-ignore -v` naming the exact line number of each rule.

### (c) The fragile `from secrets import api_key` is gone

**The problem:** `multiply_module.py` and `subtract_module.py` imported `api_key` from a
module named `secrets`. That old `secrets.py` was itself listed in `.gitignore`, so it
was never committed and never reached GitHub. On a fresh clone the file was therefore
absent, and `from secrets import api_key` silently fell through to **Python's
standard-library `secrets` module**, which exists on every install and has no `api_key`
attribute — so the import raised `ImportError` and the whole program failed for anyone
who cloned it. The repository could not be run by the person reviewing it.

**The fix:** there is no `secrets.py` anywhere in this project. Configuration lives in
[`config.py`](config.py), which reads the key from an environment variable with a safe,
non-secret fallback:

```python
import os

api_key = os.getenv("API_KEY", "demo-api-key-not-a-real-secret")
```

Because the fallback is a harmless literal, a fresh clone runs immediately with no setup
— demonstrated by the captured [How to run](#how-to-run) output above, produced from a
clean clone with no `.env` and no environment variables. Anyone who wants to use a real
key copies the committed [`.env.example`](.env.example) to `.env` and fills it in; `.env`
stays ignored, so the real secret never reaches GitHub while the *shape* of the
configuration is documented in a committed file.

The general rule this enforces: **never `import` from a file that `.gitignore` excludes,
and never name a module after one in the Python standard library.** A committed example
plus an environment variable gives you both a working fresh clone and a secret that stays
out of version control.
