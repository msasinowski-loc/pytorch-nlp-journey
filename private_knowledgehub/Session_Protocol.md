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
Tell Claude which days or tasks are complete — Claude will hard-code the checkboxes in the HTML file. Download the updated `learning_path_tracker.html` and push it to GitHub alongside the CSV.

> ⚠️ **Do not rely on clicking checkboxes in the browser** — tracker state saves to localStorage which is browser-only and does not sync via Git. The only way to sync tracker state across machines is to push an updated HTML file from Claude.

```powershell
Copy-Item "$HOME\Downloads\learning_path_tracker.html" private_knowledgehub\ -Force
git add private_knowledgehub/learning_path_tracker.html
git commit -m "update tracker - Day X complete"
git push
```

> 🔮 **Planned improvement (Phase 2):** rebuild tracker to read/write state from the CSV so sync is automatic. Until then, update via Claude.

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

*Last updated: Day 5 — tracker sync architecture clarified*

---

## 🌅 Daily Warm-up Protocol (weekdays only)

Run every weekday before starting new content. 15 minutes max.

### Structure — fixed every day
```
5 min  — 1 Theory item (confidence 1, related to today's theme if natural)
10 min — 3–4 items from the active angle (lowest confidence first)
```

### Angle rotation — alternates daily
```
Day 6  → Pen & Paper
Day 7  → Coding
Day 8  → Pen & Paper
...and so on
```

### Item selection rule
Filter KA for confidence 1 in the active angle. If ties, prioritise items most relevant to upcoming content. Never include items at confidence 0 (unseen) in the warm-up.

### Warm-up prompt for Claude
```
Today is Day X — [PnP / Coding] warm-up day.
Here is my KA CSV: [paste raw GitHub URL]
Please generate today's warm-up following the session protocol.
```

### What counts as a pass (→ confidence 2)
- Got the core answer right without needing to open the answer first
- Could explain it in plain language without prompting
- For Coding: wrote the syntax correctly on the first attempt

---

## 📋 Coding warm-up review protocol

When you submit code for review, Claude follows this two-stage process:

**Stage 1 — verdict only, no answers:**
Claude marks each item as ✅ correct or ❌ wrong, with a one-line hint at most.
No syntax fixes, no solutions shown yet.

**Stage 2 — fixes (only after you ask):**
After seeing which items are wrong, you attempt to fix them yourself first.
Then ask Claude for the corrections if still stuck.

This applies to all coding exercises during warm-up. For new content sessions the flow is more flexible.

---

## 🏗 Weekend Project Protocol

**Every weekend — one coding-only project, 30–60 minutes.**

No PnP, no theory. A single self-contained coding challenge that uses everything learned so far in a realistic scenario.

### Design principles
- Localization-adjacent where possible (TMX, XLIFF, bilingual data, MT evaluation)
- Uses NumPy + Pandas as the primary tools, adding new libraries as the curriculum progresses
- Produces something pushable to GitHub as a portfolio commit
- Walkthrough provided (milestones + tool hints) but no starter code

### First project attempted: Translation Memory Analyser
- Parse a TMX file with ElementTree
- Load into Pandas DataFrame
- Compute coverage stats per language, length ratio outliers, near-duplicate detection via cosine similarity
- **Outcome:** surfaced gaps in XML parsing and dict building → added as KA items Ph1-Loc-001 and Ph1-Loc-002
- **Status:** incomplete, retry when XML parsing and dict building reach confidence 2

### Weekend project prompt for Claude
```
It's the weekend. I have [X] minutes.
My current KA items at confidence 2+: [paste or link CSV]
Suggest a weekend coding project appropriate for my level.
```
