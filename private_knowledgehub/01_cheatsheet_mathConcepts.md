# Math Concepts Cheatsheet
### pytorch-nlp-journey · msasinowski-loc
> **How to use in Notion:** Each `##` section is a toggle block. Use Ctrl/Cmd+F to search across all sections. Tags in `[brackets]` are searchable keywords.
> Built the way I learned each concept: picture first, words second, formula last.

---

## 📋 Table of Contents

- [Bayes' theorem — the essence](#-bayes-theorem--the-essence)

---

## 🎲 Bayes' theorem — the essence
`[probability] [bayes] [conditional] [prior] [likelihood] [posterior] [base rate] [tree] [QA] [false positive]`

**The question Bayes answers:** I saw some evidence. How likely is the thing I care about, *now that I've seen it*?

**The one-line idea:** the evidence **shrinks the universe** to only the cases where the evidence happened. Inside that mini universe, I just count again.

---

### Step 1 — Crutch 1: draw the tree with COUNTS (never start with the formula)

Scenario: an automated QA check on MT output.
- 10% of segments really contain an error
- If a segment **has** an error, the check flags it 80% of the time
- If it has **no** error, the check still flags it 5% of the time (false alarm)

Picture **1,000 segments** and fill in counts top-down:

```
                    1,000 segments
                   /              \
          100 error              900 no error
           /       \               /        \
    80 flagged   20 not       45 flagged   855 not
                 flagged                    flagged
```

**Check:** each pair of branches adds back up to the number above it.

---

### Step 2 — Crutch 2: the lookup table (symbol → variable → value)

Every past slip came from translating between a math symbol, a variable name and a number. This table is the bridge — fill it **before** any formula or code.

| Math symbol | In words | Variable | Value |
|---|---|---|---|
| P(error) | **prior** — share of segments with an error | `P_prior_error` | 0.1 |
| P(no error) | complement of the prior | `P_prior_noError` | 0.9 |
| P(flag \| error) | **likelihood** — the check catches a real error | `P_flag_if_error` | 0.8 |
| P(flag \| no error) | false alarm rate | `P_flag_if_noError` | 0.05 |
| P(flag ∩ error) | flagged **and** really an error | `P_flag_and_error` | 0.08 |
| P(flag ∩ no error) | flagged **and** no error (false alarm) | `P_flag_and_noError` | 0.045 |
| P(flag) | flagged, by either route | `P_flag` | 0.125 |
| P(error \| flag) | **posterior** — the answer | `P_error_if_flag` | 0.64 |

**Variable naming:** `_if_` mirrors `|`, `_and_` mirrors `∩`. No hyphens in names — Python reads `-` as minus.

---

### `|` vs `∩` — zoom in, or don't

| Symbol | Read it as | The universe I count in | Divide by |
|---|---|---|---|
| P(flag \| error) | flag **given** error | only the 100 error segments | the branch total (100) |
| P(flag ∩ error) | flag **and** error | all 1,000 segments | the grand total (1,000) |

Both point at the **same leaf** (80 flagged errors). Only the divisor changes.
- `|` = **zoom into a branch first**, then take its share
- `∩` = **never zoom**, count against everything

---

### Add or multiply?

| Situation | Operation | Why | Example |
|---|---|---|---|
| Walking **down one path** ("this AND THEN that") | **multiply** | take a share of a share | 0.1 × 0.8 = 0.08 → P(flag ∩ error) |
| Combining **separate routes** to the same outcome ("this OR that") | **add** | the routes never overlap — like counting people in two rooms | 0.08 + 0.045 = 0.125 → P(flag) |

- **Multiplication rule:** P(A ∩ B) = P(A | B) · P(B)
- **Law of total probability:** P(flag) = P(flag ∩ error) + P(flag ∩ no error)
- **Complement rule:** P(no error) = 1 − P(error) — the two branches always add to 1

---

### The mini universe — what Bayes actually does

"Given flagged" means: **throw away every segment that wasn't flagged.**

```
"given flagged" world = 80 flagged errors + 45 flagged non-errors = 125 segments
                        ↑ really an error   ↑ false alarm
```

- The 20 missed errors and the 855 clean passes **drop out** — they're outside the mini universe
- Inside it, count again: 80 out of 125 → **0.64**

P(error | flag) = P(flag ∩ error) / P(flag)

Dividing by P(flag) **rescales to the mini universe**, so its probabilities add up to 1 again. Same move as the conditional probability formula P(A | B) = P(A ∩ B) / P(B).

**Sanity check:** a probability can never exceed 1. If a division gives 6.4, the numerator and denominator were counted in **different universes** (e.g. an `_if_` value on top of an `_and_` value).

---

### Bayes' formula from the givens only

`[TODO — derive myself, then fill in]`
- Numerator: rebuild `P_flag_and_error` from two **given** values → `?`
- Denominator: expand `P_flag` into its two routes, each from two given values → `?`
- Keep numerator and denominator together with brackets — in Python `a + b / c` divides only `b`

```
P_error_if_flag = ( ? ) / ( ? )
```

---

### Why the answer is 64%, not 80% — the base rate

The check catches 80% of errors, yet a flagged segment is only 64% likely to be a real error.
- Errors are **rare** (10%), so the large clean group (900) produces enough false alarms (45) to dilute the true catches (80)
- Same check on a file where 50% of segments had errors → a much higher posterior
- **Gut vs. result:** my gut said "closer to 80%". The gap below 80% *is* the base rate effect.

**QA / CAT link:** a QA tool that "catches 80% of errors" can still flood linguists with false positives. The tool's accuracy is only half the story — **how rare the error type is** matters just as much.

**Spam-filter version (2026-10-12):** P(spam) = 0.3, P(free | spam) = 0.6, P(free | ham) = 0.05 → P(spam | free) = 180 / 215 ≈ 0.837. One word moved the belief from 30% to 84%. A Naive Bayes filter repeats this update for every word.

---

### Vocabulary

| Term | Meaning here |
|---|---|
| **Prior** | belief *before* the evidence — P(error) |
| **Likelihood** | how often the evidence shows up *if* the thing is true — P(flag \| error) |
| **Evidence** | how often the evidence shows up *at all* — P(flag) |
| **Posterior** | belief *after* the evidence — P(error \| flag) |
| **False positive / false alarm** | flagged, but no error (45) |
| **False negative / miss** | error, but not flagged (20) |

---

*Added: 2026-10-28 — Bayes' theorem restart with tree + lookup-table crutches*
