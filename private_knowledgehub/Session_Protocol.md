# Session Protocol
### pytorch-nlp-journey · msasinowski-loc
> **How to use in Notion:** Each `##` becomes a toggle. Follow in order at the start and end of every Claude session.

---

## 🟢 Session Start

### 1. Sync your machine
```powershell
cd pytorch-nlp-journey
git pull
```

### 2. Open your assets
Open these from `private_knowledgeHub/` in your browser:
- `learning_path_tracker.html` — check what's planned for today
- `KA_viewer.html` — review what's due for spaced repetition

### 3. Brief Claude
Paste this at the start of the conversation:

```
Here is my current KA CSV — please use this as the source of truth for my knowledge state:
[paste raw GitHub URL or CSV contents]

I'm on Day X. Today's goals are: [from tracker]
```

> **Raw GitHub URL format:**
> `https://raw.githubusercontent.com/msasinowski-loc/pytorch-nlp-journey/main/private_knowledgeHub/KA_knowledge_acquired.csv`

### 4. State your goal for the session
Be specific — "watch videos 4–5 and do NumPy reshaping" is better than "continue learning."

---

## 🔴 Session End

### 1. Download updated CSV
Claude will have updated confidence scores during the session. Download the latest `KA_knowledge_acquired.csv`.

### 2. Replace and push
```powershell
Copy-Item "$HOME\Downloads\KA_knowledge_acquired.csv" private_knowledgeHub\ -Force
git add private_knowledgeHub/KA_knowledge_acquired.csv
git commit -m "update KA confidence scores - Day X"
git push
```

### 3. Update the tracker
Check off completed tasks in `learning_path_tracker.html`. Note: tracker state is localStorage only — it does not sync via Git. This is a known limitation.

### 4. Note anything unresolved
If a concept didn't click, flag it here or in Notion before closing. Don't rely on memory across sessions.

---

## 📋 Quick Reference

| What | Where |
|---|---|
| Learning path tracker | `private_knowledgeHub/learning_path_tracker.html` |
| KA database (source of truth) | `private_knowledgeHub/KA_knowledge_acquired.csv` |
| KA viewer | `private_knowledgeHub/KA_viewer.html` |
| Python cheatsheet | `private_knowledgeHub/python_cheatsheet.md` |
| Git cheatsheet | `private_knowledgeHub/git_cheatsheet.md` |
| GitHub repo | `https://github.com/msasinowski-loc/pytorch-nlp-journey` |
| Raw CSV URL | `https://raw.githubusercontent.com/msasinowski-loc/pytorch-nlp-journey/main/private_knowledgeHub/KA_knowledge_acquired.csv` |

---

## 🧠 KA Confidence Scale

| Score | Meaning | SRS behaviour |
|---|---|---|
| 0 | Unseen — not encountered yet | Not scheduled |
| 1 | Fuzzy — seen it, couldn't fully recall | Review in 1 day |
| 2 | Familiar — got it with some effort | Review in ~3 days |
| 3 | Solid — recalled cleanly, could explain it | Review in ~7+ days |

> Scores are per angle: pen & paper (`-P`), Python (`-C`), theory (`-T`). Knowing something on paper doesn't mean you know it in code.

---

## 🔁 Two-Machine Sync Rules

- **Always `git pull` before starting work**
- **Always push the CSV at end of session**
- The CSV is the only file that changes regularly — other files change only when explicitly updated
- If you edit any asset locally (e.g. cheatsheet), push that file too before switching machines

---

*Last updated: Day 4 — GitHub sync complete*
