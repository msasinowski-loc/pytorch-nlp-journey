# Session Protocol
### pytorch-nlp-journey · msasinowski-loc
> **How to use in Notion:** Each `##` becomes a toggle. The **Forge v2** section below is the live protocol from 2026-11-16. Everything under "Archive" is the earlier protocol, kept for reference; where the two disagree, Forge v2 wins.

---

## 🔥 Forge v2: the live protocol (from 2026-11-16)

**Master page:** The Forge (artifact "The Forge", anvil icon), https://claude.ai/artifact/Eej5tP9zXS1FTWCP5HqHDx. It replaces the pilot log and the old Forge page. Pilot sessions (Nov 12–15) and the pilot retro were carried over.

**Core principle:** *Explain it, or it isn't forged.* Speaking a concept out loud, in your own words, is the learning. Code and paper are how you get there.

### 1. Rhythm
| Day | Time | What |
|---|---|---|
| Mon–Fri | **20 min** | 5 recall + 12 new/apply + 3 explain aloud |
| Sat | **60 min** | 5 recall + 50 build + 5 log |
| Sun | **60 min** | 40 build + 10 teach-back + 10 weekly check-in |

- **7 of 7 days.** Weekly target: 5×20 + 2×60 = **220 min**.
- **Ember day:** if time is short, **5 minutes of recall** counts. The streak holds, nothing is penalised, and the sequence doesn't move (see 3).

### 2. The daily recall opener (first 5 minutes, every day)
- **1-2-2 mix:** 1 question from yesterday, 2 from this week, 2 from 1–4 weeks ago.
- Plus **yesterday's mistakes**, asked again.
- Weekend version: three re-entry questions about the project (where were we, what was the last decision, what's next) plus last session's mistakes.
- **No cheatsheets during recall or KA reviews.** Cheatsheets are allowed and encouraged in build sessions.
- Bayes: drawing the tree is compulsory before the formula.
- **Code-reading drill (from 2026-11-25):** 1 of the 5 recall questions is a 3–5 line snippet where you predict the exact output. Topics: loops, indexing, dicts, list vs NumPy array, pandas masks, `=` vs `==`, function arguments. Snippets come from your own code and your recent slips. **Friday's Keep step is half code drills.** Reason: the week 1 check-in found theory more confident than code; coding basics feel like a shaky foundation.

### 3. The weekly sequence rolls on *sessions*, not dates
Each week has one theme. The theme is worked through seven steps, in order:

| # | Step | Kind | What happens |
|---|---|---|---|
| 1 | **Learn** | weekday | First contact, built through questions. Pen and paper and code together. |
| 2 | **Use** | weekday | One pen-and-paper problem and its code twin. Predict before you run. |
| 3 | **Test** | weekday | Edge cases, explained cold, without notes. Write one cheatsheet line yourself. |
| 4 | **Connect** | weekday | Where does the concept live in the near-duplicate detector? |
| 5 | **Keep** | weekday | 20 min of mixed spaced review across weeks. |
| 6 | **Build** | weekend | 60 min on the detector, using the theme where it fits. |
| 7 | **Teach-back** | weekend | Explain the week's theme start to finish; weekly check-in. |

**Rules for "what's next":**
- The page proposes the **first step not yet done this week** (Mon–Sun). Weekdays take the first undone weekday step; weekends take Build, and on Sunday Teach-back if it's still open.
- **A missed day doesn't skip a step.** If Tuesday is missed, Wednesday is "Use", not "Test".
- An **ember day** (recall only) is logged as such and doesn't advance the sequence.
- If all steps are done, weekdays fall back to Keep and weekends to Build/Teach-back.
- Steps not reached by Sunday are **not debt**. They show as "not reached" in the check-in, and the theme moves on with the calendar week. A step that matters can be picked up in a later Keep session.
- You can always override the proposal in the "What you did" field: the log records what actually happened.

### 4. The daily check-in (on the page)
Fields: **What you did** (step or ember day), **Minutes**, **Recall /5** (optional), **Explained aloud** (yes/no), **One line** (what you learned, or what to remember, in your own words).
- One record per day; logging again the same day updates it.
- Your one-liners become the raw material for recall questions and for Sunday's check-in.

### 5. Gamification logic (exact rules, for future recall)
- **Heat** (the forge mouth): this week's minutes ÷ this week's target. Cold iron <20% · Dull red ≥20% · Cherry red ≥40% · Orange heat ≥60% · Yellow heat ≥80% · **White heat ≥100%**. Pilot-week target was 195 (15-min weekdays); from Nov 16 it's 220.
- **Streak:** consecutive days with **≥5 min** logged, counting back from today (if today isn't logged yet, from yesterday). Starts at the pilot (Nov 12). An ember day keeps it alive.
- **Strikes per session** (only if minutes > 0):
  - base: weekday **1**, weekend **3**
  - **+1** if minutes ≥ the day's target (20 weekday / 60 weekend; 15 in the pilot)
  - **+1** if recall ≥ 4/5
  - **+1** if explained aloud
- **Ranks** by total strikes: Apprentice 0 · Journeyman 5 · Smith 15 · Master smith 35 · Forge master 70 · Grand master 120.
- **Seals:** First strike (any session) · Pilot graduate (all 4 pilot days) · Seven of seven (7-day streak) · White heat (a week at ≥100%) · Theme forged (all 7 steps in one week) · Teach-back (a Sunday check-in marked "Yes, clearly") · Month forged (28-day streak).
- **Month view:** Nov 9 – Dec 13. Dim dot = nothing, ember dot = 5+ min, bright dot = target met. Pilot days have a dashed border.

### 6. The Sunday check-in: on actuals, not the plan
The page fills in the facts automatically from the week's log: **days shown up / 7**, **minutes**, **steps done / 7**, and **steps not reached**. Then you answer three things:
1. **Teach-back:** could you explain the week's theme start to finish? (Yes, clearly / Partly / Not yet)
2. **What actually got done, and what stuck?**
3. **Keep or change for next week?**

Rules:
- The review covers **what was done**, never what was planned. Missed steps are information, not failure.
- **KA scores are set on Sunday only**, from the teach-back and the week's recall, and the KA CSV remains the single source of truth.
- **Open feedback item for the Nov 29 check-in:** Claude asks specifically whether the code-reading drill is helping, and whether to keep, change or drop it.
- Claude reads the week's log (the page's database) before the check-in.

### 7. The month: Nov 16 – Dec 13
| Week | Theme | Detector link |
|---|---|---|
| Nov 9–15 | Pilot week | M1 closed, M2 started |
| Nov 16–22 | Probability distributions: Bernoulli, Gaussian, mean and variance | M3–M4: count matrix and cosine scores, then the shape of the score distribution |
| Nov 23–29 | OOP: classes and methods | Refactor the detector into a `SimilarityFinder` class |
| Nov 30–Dec 6 | z-scores and outliers | M5–M6: thresholds, bands, unusual scores |
| Dec 7–13 | TF-IDF | Weight rare words above "the" and "continue" |

**Change, decided 2026-11-21:** time off gives 9 days of **60 min** (Nov 21–29). Sat 21–Sun 22: detector M3–M4. OOP week: the 20-minute theme sequence as usual, then 40 min building a **placeholder checker as a class** (instead of refactoring the detector, which becomes the second OOP exercise later). Weekday targets on the page stay at 20 min, so a 60-minute day simply counts as "target met". Details are in weekend_projects.md.

Each Sunday is a checkpoint. On Dec 13: a month retro, then decide the next month.

### 8. Standing rules (unchanged)
- Claude never gives code outright; Socratic, step by step. Two-stage review: ✅/❌ with a one-line hint first, the fix only if asked.
- Derive values yourself; Claude doesn't hand over constants you can compute.
- Unfamiliar function: `help()`, the docs, your cheatsheet. Exception: when short on time and you ask, Claude feeds it and updates the cheatsheet.
- In project work, Claude notes what shares concepts or maths with CAT tools (memoQ homogeneity) and what differs.
- Code keeps a header with a version log.
- You write the paper template; Claude reminds you only when a step looks skipped.
- Additive changes only: existing content and statuses are preserved.

### 9. How the Forge sits inside the grand picture
The Forge is the **short-horizon layer** (days, weeks, one month). It deliberately doesn't show the long-term assets, but it depends on them:

| Layer | Asset | Role | When the Forge uses it |
|---|---|---|---|
| Long term: *where am I on the path* | **pytorch-nlp-journey tracker** (https://claude.ai/artifact/1zDUp1JRnbJcJbu1avm65o) | Phases, topics, order | Choosing each month's themes; the Dec 13 retro picks the next month from the tracker's next open items. |
| Proficiency: *how well do I know each item* | **KA CSV** (single source of truth) + KA viewer (https://claude.ai/artifact/WjT1RDm5xK48Gu4RFjvfmH) | 0–3 score per item | **Daily recall** draws its "older weeks" questions from KA items at 1–2 and recently promoted items. **Sunday** scores are updated from the teach-back and the week's recall. **Themes** target KA gaps. |
| Short term: *what did I do today* | **The Forge** | Sessions, streak, sequence, weekly check-in | Every day. |

Flow, in one line: **tracker → month themes → weekly sequence → daily sessions → Sunday KA update → tracker progress → next month's themes.**

Rules:
- A new theme gets KA rows (score 0) when it starts, if they don't exist yet.
- Claude reads the KA CSV (and, monthly, the tracker) before Sunday check-ins and before planning a new month. The Forge log is evidence; the KA CSV stays the verdict.

---

# 🗄️ Archive: protocol before Forge v2 (kept for reference)


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

---

## 🎓 Teaching & confidence level principles

### Python teaching flow
When introducing new Python/Pandas/NumPy content:
1. Show the setup code, explain what it does
2. Ask the learner to **explain it back in their own words**
3. Ask for a **prediction before running** — what do you expect this to output and why?
4. Run the code and compare to prediction
5. Explain any gaps, then move to the next concept

This flow builds durable understanding — prediction forces active thinking, not passive reading.

### Confidence level definitions

| Level | Name | Meaning |
|---|---|---|
| 0 | Unseen | Not yet encountered |
| 1 | Fuzzy | Seen it, couldn't fully recall without help |
| 2 | Familiar | Can recall and apply with some effort — **expected steady state** |
| 3 | Mastery | Can recall fluently, explain to others, apply in novel contexts |

**Confidence 2 is the target for all content.** Progression from 2 → 3 is slow and deliberate.

### Warm-up item rules by confidence level

**Items at confidence 1 → 2:**
- Standard warm-up exercises — recall and apply the basic concept
- Move to 2 when: got it right on first attempt without hints

**Items at confidence 2 → 3:**
- Max 1–2 items per warm-up
- Challenge goes beyond basic recall — novel application, edge cases, explaining the why, connecting to upcoming content
- Move to 3 only when: demonstrated mastery unprompted
- Devalue back to 1 if: fundamental gap surfaces during the exercise

**Confidence 2 is not a stepping stone — it's the destination.** Most items will live at 2 for weeks before earning a 3.
