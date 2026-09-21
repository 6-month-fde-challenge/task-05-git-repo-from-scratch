# GIT_WORKFLOW.md — the complete captured session

This is the **real, unedited terminal transcript** of building this repository from an
empty folder. Every command below was actually run, in this order, and every block of
output was captured from that run — `git init`, `git status`, `git add`, `git commit`,
`git log`, `git diff` and the `.gitignore` proof. Nothing here is illustrative or
invented: the SHAs printed below are the SHAs that are in this repository's history, and
you can check them yourself with `git log --oneline`.

The project was built up **in stages on purpose**: one small, self-contained group of
modules per commit. That is what makes `git status` and `git diff` show something
genuinely interesting at each step, instead of one giant "add everything" commit.

Environment: Windows 11, Git Bash, `git version 2.55.0.windows.3`, `Python 3.12.10`.

---

## Step 1 — `git init`

**What it does:** creates the `.git` directory — the object database, the index and
`HEAD` — which turns an ordinary folder into a Git repository.

**Why it is required:** without it there is no repository at all, and no other Git
command in this document can run. `-b main` sets the initial branch name to `main` up
front, so the default branch on GitHub matches from the very first push.

```console
$ git init -b main
Initialized empty Git repository in C:/Users/asus/Desktop/work/6-month-fde-challenge/03_git_and_git_hub/task-05-git-repo-from-scratch/.git/
```

Identity was then configured so that every commit is attributable:

```console
$ git config user.name "veerandra7"
$ git config user.email "veerandra.data@gmail.com"
```

---

## Step 2 — Commit 1: `.gitignore` and `.env.example`

The very first commit is the ignore policy. Doing this first means no junk file —
`__pycache__/`, a `.env`, a virtualenv — can ever be accidentally staged later.

### `git status` **before** `git add` — the two files are untracked

**What it does:** shows which files Git is tracking, which changes are staged for the
next commit, and which files it has never seen (untracked).

**Why it is required:** it is the "where am I" command. You run it before staging to see
what is new, and again after staging to confirm exactly what the next commit will
contain.

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

### `git add` — move the files into the staging area

**What it does:** copies the current content of the named files into the index (the
staging area).

**Why it is required:** Git does not commit your working directory, it commits the
index. `git add` is how you choose precisely which changes go into the next commit —
that is what makes small, meaningful commits possible at all.

```console
$ git add .gitignore .env.example
```

### `git status` **after** `git add` — the same two files are now staged

Note how the wording changes from "Untracked files" to "Changes to be committed". This
before/after pair is the clearest demonstration of what staging actually does.

```console
$ git status
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   .env.example
        new file:   .gitignore
```

### `git commit`

**What it does:** writes whatever is in the index into a permanent, immutable snapshot
with a message, an author and a parent, then moves the branch pointer to it.

**Why it is required:** it is the unit of history. Every commit is a point you can
return to, compare against, or hand to a reviewer.

```console
$ git commit -m "Initialise repository with .gitignore and environment template"
[main (root-commit) b84494c] Initialise repository with .gitignore and environment template
 2 files changed, 24 insertions(+)
 create mode 100644 .env.example
 create mode 100644 .gitignore
```

`(root-commit)` confirms this is the first commit in the repository — it has no parent.

---

## Step 3 — Commit 2: `config.py` and `input_variables.py`

```console
$ git status --short
?? config.py
?? input_variables.py
```

`--short` is the compact form of the same report: `??` means untracked, `A` staged as
added, `M` modified. Useful once you know what the long form is telling you.

```console
$ git add config.py input_variables.py
```

### `git diff --staged` — review exactly what is about to be committed

**What it does:** shows the difference between the staging area and the last commit
(`HEAD`) — that is, the precise content of the commit you are about to make.

**Why it is required:** it is the last check before history becomes permanent. Here it
proves the new `config.py` reads the API key from the environment rather than importing
a secret file.

```console
$ git diff --staged
diff --git a/config.py b/config.py
new file mode 100644
index 0000000..773a377
--- /dev/null
+++ b/config.py
@@ -0,0 +1,15 @@
+"""Configuration for the calculator project.
+
+The API key is read from the API_KEY environment variable. A harmless demo
+value is used as a fallback so that a fresh clone of this repository runs
+without any setup.
+
+This module replaces the old `secrets.py`. The previous version was listed in
+.gitignore, so it never reached GitHub and `from secrets import api_key`
+silently resolved to Python's standard-library `secrets` module, which does not
+define `api_key`. That made the program crash on a fresh clone.
+"""
+
+import os
+
+api_key = os.getenv("API_KEY", "demo-api-key-not-a-real-secret")
diff --git a/input_variables.py b/input_variables.py
new file mode 100644
index 0000000..c5d2a21
--- /dev/null
+++ b/input_variables.py
@@ -0,0 +1,17 @@
+"""Collect the two numbers the calculator works with.
+
+input() is wrapped so the project also runs non-interactively (for example when
+a reviewer pipes no stdin), instead of crashing with EOFError.
+"""
+
+
+def read_number(prompt, default):
+    try:
+        return int(input(prompt))
+    except (EOFError, ValueError):
+        print("   -> no input available, using default:", default)
+        return default
+
+
+a = read_number("Enter a number 1 : ", 10)
+b = read_number("Enter a number 2 : ", 5)
```

```console
$ git commit -m "Add environment-based config and user input collection"
[main 5fb47c5] Add environment-based config and user input collection
 2 files changed, 32 insertions(+)
 create mode 100644 config.py
 create mode 100644 input_variables.py
```

---

## Step 4 — Commit 3: `login.py` and `profile.py`

```console
$ git status --short
?? login.py
?? profile.py

$ git add login.py profile.py

$ git commit -m "Add login prompt and profile resolution modules"
[main b8b6fa5] Add login prompt and profile resolution modules
 2 files changed, 33 insertions(+)
 create mode 100644 login.py
 create mode 100644 profile.py
```

---

## Step 5 — Commit 4: `addition_module.py` and `subtract_module.py`

```console
$ git status --short
?? addition_module.py
?? subtract_module.py

$ git add addition_module.py subtract_module.py

$ git commit -m "Add addition and subtraction modules guarded by API key and profile"
[main 01ce93d] Add addition and subtraction modules guarded by API key and profile
 2 files changed, 28 insertions(+)
 create mode 100644 addition_module.py
 create mode 100644 subtract_module.py
```

---

## Step 6 — Commit 5: `multiply_module.py` and `division_module.py`

```console
$ git status --short
?? division_module.py
?? multiply_module.py

$ git add multiply_module.py division_module.py

$ git commit -m "Add multiplication and division modules with divide-by-zero guard"
[main 40399b4] Add multiplication and division modules with divide-by-zero guard
 2 files changed, 31 insertions(+)
 create mode 100644 division_module.py
 create mode 100644 multiply_module.py
```

---

## Step 7 — Commit 6: `calculator.py`

```console
$ git status --short
?? calculator.py

$ git add calculator.py

$ git commit -m "Add calculator entry point wiring all four arithmetic modules"
[main 4cb8d9c] Add calculator entry point wiring all four arithmetic modules
 1 file changed, 18 insertions(+)
 create mode 100644 calculator.py
```

---

## Step 8 — Commit 7: `dashboard.py`

```console
$ git status --short
?? dashboard.py

$ git add dashboard.py

$ git commit -m "Add dashboard that prints the final calculation report"
[main 3a9f22f] Add dashboard that prints the final calculation report
 1 file changed, 10 insertions(+)
 create mode 100644 dashboard.py
```

---

## Step 9 — Commit 8: a dedicated `git diff` demonstration

Up to this point every commit added brand-new files. To demonstrate `git diff` properly
we need a change to an **already tracked** file, so the docstring and the banner text in
`dashboard.py` were rewritten.

### `git status` now reports a modification, not an untracked file

```console
$ git status
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   dashboard.py

no changes added to commit (use "git add" and/or "git commit -a")
```

### `git diff` — working tree vs staging area (unstaged changes)

**What it does:** with no arguments, `git diff` compares the files on disk against the
staging area. It shows work you have done but have not yet staged.

**Why it is required:** it is the review step before you stage. `-` lines are what the
file used to say, `+` lines are what it says now.

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

### `git add`, then `git diff` again — and now it prints nothing

```console
$ git add dashboard.py

$ git diff
```

**That empty output is the whole point.** `git diff` does not mean "show me my changes",
it means "show me changes that are **not yet staged**". Once the change is staged, the
working tree and the index are identical, so plain `git diff` has nothing left to
report. Beginners routinely misread this empty output as "my changes are gone" — they
are not, they have simply moved into the staging area, where the next command finds them.

### `git diff --staged` — staging area vs `HEAD`

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

### The difference between the two, stated plainly

Git has three places the content of a file can live, and one diff command for each gap
between them:

| Command | Compares | Question it answers |
|---|---|---|
| `git diff` | working tree **vs** staging area | "What have I changed but not staged yet?" |
| `git diff --staged` (or `--cached`) | staging area **vs** `HEAD` | "What exactly will my next commit contain?" |
| `git diff HEAD` | working tree **vs** `HEAD` | "What have I changed since the last commit, staged or not?" |

The transcript above shows the first two on the *same* edit: before `git add`, `git diff`
shows the change and `git diff --staged` is empty; after `git add` the two swap over
exactly.

```console
$ git commit -m "Clarify dashboard docstring and banner text"
[main 5250c99] Clarify dashboard docstring and banner text
 1 file changed, 9 insertions(+), 3 deletions(-)
```

This is the first commit that reports **deletions** as well as insertions
(`9 insertions(+), 3 deletions(-)`), because it modified a tracked file rather than
adding a new one.

---

## Step 10 — proving the `.gitignore` actually works

A `.gitignore` that is merely present proves nothing. So two things Git *should* ignore
were deliberately created:

1. `__pycache__/`, generated simply by running the program;
2. a `.env` file containing a realistic-looking secret value.

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

Both artefacts genuinely exist on disk afterwards:

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

### Proof 1 — `git status` does not list them at all

```console
$ git status
On branch main
nothing to commit, working tree clean
```

`.env` and `__pycache__/` are sitting right there in the folder, yet Git reports a clean
tree. Without `.gitignore`, both would appear under "Untracked files".

### Proof 2 — `git status --ignored` shows Git knows about them and is deliberately skipping them

**What it does:** the same status report, plus an explicit "Ignored files" section.

**Why it is required:** it distinguishes "Git cannot see these files" from "Git sees
these files and is choosing to ignore them" — only the second is what you want.

```console
$ git status --ignored
On branch main
Ignored files:
  (use "git add -f <file>..." to include in what will be committed)
        .env
        __pycache__/

nothing to commit, working tree clean
```

### Proof 3 — `git check-ignore -v` names the exact rule doing the ignoring

**What it does:** for each path, prints the file, the line number and the pattern that
caused that path to be ignored.

**Why it is required:** it is the definitive answer to "*why* is this file being
ignored?", and the strongest possible evidence that the rules are real and effective.

```console
$ git check-ignore -v __pycache__ .env
.gitignore:2:__pycache__/       __pycache__
.gitignore:12:.env      .env
```

Read that as `file:line:pattern<TAB>path` — line 2 of `.gitignore` (the pattern
`__pycache__/`) ignores `__pycache__`, and line 12 (the pattern `.env`) ignores `.env`.

---

## Step 11 — `git log`: reading the history back

**What it does:** walks the commit graph backwards from `HEAD` and prints each commit.

**Why it is required:** it is how a repository is audited — who changed what, when, in
what order, and which SHA to point at if you need to go back to a known-good state.

### `git log --oneline` — the summary

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

### `git log -1` — full detail for a single commit

```console
$ git log -1
commit 5250c99332eea1cd07c255b3d78ea9bd666fb37a
Author: veerandra7 <veerandra.data@gmail.com>
Date:   Mon Sep 21 18:24:50 2026 +0530

    Clarify dashboard docstring and banner text
```

### `git log --stat` and `git log --graph`

Both are captured in full, with their real output, in
[COMMIT_HISTORY.md](COMMIT_HISTORY.md).

### `git ls-files` — what is actually tracked

**What it does:** lists every path currently in the index.

**Why it is required:** it is the definitive answer to "what did I actually commit?".
Note that neither `.env` nor `__pycache__` appears, while `.gitignore` does.

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

## Step 12 — publishing to GitHub

**What it does:** creates the remote repository, registers it as `origin`, and uploads
the whole local history to it.

**Why it is required:** `git init` only ever made a *local* repository. Until it is
pushed, the entire history exists on one machine and nobody else can see it.

```console
$ gh repo create 6-month-fde-challenge/task-05-git-repo-from-scratch \
    --public -d "<description>" --source=. --remote=origin --push
```

`--source=.` publishes this folder, `--remote=origin` names the remote, and `--push`
sends `main` up immediately — so the complete commit history shown above is exactly what
lands on GitHub.

---

## Command reference — every command used, and why it is needed

| Command | Why it is required |
|---|---|
| `git init -b main` | Turns the folder into a repository; nothing else works without it. `-b main` fixes the default branch name from the start. |
| `git config user.name` / `user.email` | Stamps every commit with an author, so the history is attributable. |
| `git status` | Shows untracked / staged / modified state. The orientation command, run before and after every `git add`. |
| `git status --short` | Compact form of the same report, for quick checks. |
| `git status --ignored` | Adds an explicit list of ignored files — proves `.gitignore` is doing its job. |
| `git add <files>` | Stages exactly the changes you want in the next commit; what makes small, meaningful commits possible. |
| `git commit -m "..."` | Records the staged snapshot permanently, with a message and an author. |
| `git diff` | Working tree vs staging area — what you have changed but not staged. |
| `git diff --staged` | Staging area vs `HEAD` — exactly what the next commit will contain. |
| `git check-ignore -v` | Names the exact `.gitignore` line that is ignoring a given path. |
| `git log --oneline` | Compact, one-line-per-commit history. |
| `git log --stat` | History plus per-commit file-change statistics. |
| `git log --graph --oneline --all --decorate` | Draws the branch topology with refs (`HEAD`, `main`, `origin/main`) attached. |
| `git ls-files` | Lists everything actually tracked — confirms no secrets or caches were committed. |
| `gh repo create ... --push` | Creates the GitHub remote and pushes the full history to it. |
