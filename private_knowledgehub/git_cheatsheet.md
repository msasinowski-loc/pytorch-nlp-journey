# Git Cheatsheet — pytorch-nlp-journey

> Notion tip: paste this page as-is. Each `##` becomes a toggle or heading depending on your view setting.

---

## 🛠 One-time setup

```bash
# Install Git → git-scm.com/download/win (Windows)
# Restart terminal after installing

git --version                          # verify install

git config --global user.name "msasinowski-loc"
git config --global user.email "your@email.com"
```

---

## 🚀 Starting a project (done once per machine)

```bash
# Clone an existing repo from GitHub
git clone https://github.com/msasinowski-loc/pytorch-nlp-journey.git

# Enter the folder
cd pytorch-nlp-journey
```

---

## 📅 Daily workflow

```bash
# 1. Before starting work — pull latest from GitHub
git pull

# 2. Do your work (edit files, write code)

# 3. Stage all changes
git add .

# 4. Commit with a message
git commit -m "what you did"

# 5. Push to GitHub
git push
```

> **Rule of thumb:** `pull` before you start, `push` when you finish.  
> Works across two machines automatically.

---

## 🔍 Checking status

```bash
git status                             # what's changed since last commit
git log --oneline                      # short history of commits
git diff                               # see exact line-by-line changes
```

---

## ↩️ Undoing things

```bash
# Discard changes to a file (before staging)
git restore filename.py

# Unstage a file (after git add, before commit)
git restore --staged filename.py

# Undo the last commit but keep your changes
git reset --soft HEAD~1
```

---

## 🌿 Branches (Phase 4 — not needed yet)

```bash
# Create and switch to a new branch
git checkout -b feature-name

# Switch between branches
git checkout main
git checkout feature-name

# Merge a branch into main
git checkout main
git merge feature-name

# Delete a branch after merging
git branch -d feature-name
```

---

## 🔁 Two-machine sync (your setup)

```bash
# Machine A — finish work
git add .
git commit -m "done for today"
git push

# Machine B — start work next session
git pull                               # gets everything Machine A pushed
```

> Both machines point to the same GitHub repo.  
> GitHub is the single source of truth.

---

## 📁 What the files mean

| File/Folder | What it is |
|---|---|
| `.git/` | Hidden folder — Git's internal database. Never touch it. |
| `.gitignore` | List of files Git should ignore (e.g. `__pycache__`, `.env`, large data files) |
| `README.md` | Your project's front page on GitHub |

---

## 🧹 Recommended .gitignore for this project

```
__pycache__/
*.pyc
.env
.ipynb_checkpoints/
*.csv
*.tmx
*.xliff
data/
models/
*.pt
*.bin
```

> Add this as `.gitignore` in your repo root. Keeps large files and secrets off GitHub.

---

## ⚡ Merge conflicts — what they are and how to fix them

A merge conflict happens when two machines edited the **same lines** of the same file. Git can't decide which version wins, so it stops and asks you to choose.

### When it happens
```bash
git pull
# AUTO-MERGING FAILED:
# CONFLICT (content): Merge conflict in private_knowledgehub/file.html
```

### What Git puts in the file
```
<<<<<<< HEAD
your local version of the line
=======
the remote version of the line (from GitHub)
>>>>>>> abc1234
```

### How to fix it — step by step
```bash
# Step 1 — open the conflicted file in VS Code
code private_knowledgehub/learning_path_tracker.html

# Step 2 — search for <<<<<<< in the file (Ctrl+F)
# You'll see the conflict markers — decide which version to keep

# Step 3 — delete the markers and everything you don't want
# Keep only the final clean version of the lines

# Step 4 — save the file, then mark it resolved
git add private_knowledgehub/learning_path_tracker.html

# Step 5 — commit and push
git commit -m "resolve merge conflict in tracker"
git push
```

### Which version to keep?
For the learning tracker: keep **your local version** (between `<<<<<<< HEAD` and `=======`) since it reflects your most recent session updates from Claude.

### How to avoid conflicts
```bash
# Always pull BEFORE making any changes
git pull        # ← do this first, every session, on every machine
```

> The root cause is always the same: both machines changed the same file without syncing first. `git pull` before starting work eliminates this.

---

## 💬 Good commit message format

```
verb + what you did (keep under 72 chars)

Examples:
  add TMX parser script
  fix groupby error in coverage analysis
  refactor parser as OOP class
  add unit tests for TMX reader
  train baseline classifier on FLORES data
```

---

*Last updated: Day 6 — merge conflict resolution added*
