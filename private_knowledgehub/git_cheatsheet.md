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

# optional
git status
# compares branches

# 3. Stage all changes
git add .

# it stages everything — new files and modified files — from the current directory downward. 
# this will catch all the changes, no need to be explicit about a particular file in the directory


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

*Last updated: Day 1 — pytorch-nlp-journey*
