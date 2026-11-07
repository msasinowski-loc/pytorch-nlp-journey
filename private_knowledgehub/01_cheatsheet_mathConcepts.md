# Math Concepts Cheatsheet
### pytorch-nlp-journey · msasinowski-loc
> **How to use in Notion:** Each `##` section is a toggle block. Use Ctrl/Cmd+F to search across all sections. Tags in `[brackets]` are searchable keywords.
> Built the way I learned each concept: picture first, words second, formula last.

---

## 📋 Table of Contents

- [Bayes' theorem — the essence](#-bayes-theorem--the-essence)
- [Element-wise `*` vs matrix product `@` — the two rules](#-element-wise--vs-matrix-product---the-two-rules)

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

### Bayes' formula from the givens only — derived 2026-11-07

I got there in two moves. First write the answer with the variables I **built**, then swap each one for the **givens** it came from.

**Move 1 — the tree, as a formula** (80 out of 125):
```
P_error_if_flag = P_flag_and_error / P_flag          # 0.08 / 0.125 = 0.64
```

**Move 2 — replace each built variable with its givens:**
- Numerator: `P_flag_and_error` = one path down the tree → **multiply** → `P_flag_if_error * P_prior_error`
- Denominator: `P_flag` = **two routes added**, each route one path → **multiply inside, add between**

```
P_error_if_flag = (P_flag_if_error * P_prior_error) /
                  (P_flag_if_error * P_prior_error + P_flag_if_noError * P_prior_noError)
# 0.08 / (0.08 + 0.045) = 0.08 / 0.125 = 0.64
```

**The shape to remember:** the numerator shows up again as the first part of the denominator.
**My route ÷ all routes.**

```
                              P(flag | error) · P(error)
P(error | flag) =  ─────────────────────────────────────────────────────
                   P(flag | error) · P(error) + P(flag | no error) · P(no error)
```

**Slips I made on the way (and the check that catches each one):**

| Slip | What I wrote | Check that catches it |
|---|---|---|
| `_if_` on top instead of `_and_` | `P_flag_if_error / P_flag` | gives **6.4** — a probability can't exceed 1 → same-universe rule |
| A false-alarm piece in the numerator | `P_flag_if_error + P_flag_and_noError` | look at the tree: false alarms aren't "really an error" |
| Only one route in the denominator | `(... ) / (false-alarm route)` | `P_flag` always has **two** routes — the error route is missing |
| A built variable × a given, again | `P_flag_and_noError * P_prior_noError` | the 0.9 is already inside `_and_` — counted twice |
| Adding where it should multiply | `P_flag_if_noError + P_prior_noError` | run the numbers: 0.95 ≠ 0.125 |
| Capital letter in a name | `P_Prior_error` | Python is case-sensitive — that's a different, undefined variable |

**The habit that caught most of them:** plug the numbers in and see whether the denominator gives 0.125 and the answer 0.64.

*Python note:* no brackets needed around each product inside the denominator — `*` happens before `+`. Same precedence idea as `|` binding tighter than `==` in Pandas masks.

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
*Updated: 2026-11-07 — formula derived from the givens; slips and checks recorded*

---

## ✖️ Element-wise `*` vs matrix product `@` — the two rules
`[numpy] [broadcasting] [matmul] [dot product] [element-wise] [shapes] [weighted word count] [CAT]`

**The question I kept tripping on:** "we're doing matrix multiplication here — so why are the shape rules different?"
**The answer:** `*` is **not** matrix multiplication. In NumPy, `*` is *never* the matrix product. Two operators, two rules.

| Symbol | Name | What it does | Shape rule |
|---|---|---|---|
| `*` | **element-wise** | each cell × its **matching** cell — no sums | **broadcasting** — align from the **right** |
| `@` = `np.dot` = `np.matmul` | **matrix product** | each result cell = a **row · column** dot product — multiply **and sum** | **dot** — the **inner** pair must match |

**Why it's confusing:** in written maths, "A × B" or "AB" usually means the matrix product. NumPy chose `*` for element-wise and `@` for matrix product. **In code, `*` means cell by cell.**

**Same inputs, different results:**

```
A = [[1, 2],    B = [[10, 20],
     [3, 4]]         [30, 40]]

A * B  (element-wise)        A @ B  (matrix product)
[[1×10, 2×20],               [[1×10 + 2×30,  1×20 + 2×40],
 [3×30, 4×40]]                [3×10 + 4×30,  3×20 + 4×40]]
= [[10,  40],                = [[ 70, 100],
   [90, 160]]                   [150, 220]]
```

---

### Rule 1 — broadcasting (for `*`, `+`, `-`, `/`)

1. Write the shapes **right-aligned**
2. If one is shorter, **pad it on the left with 1** — *not 0* (a size-0 axis would mean "no elements at all")
3. Each column pair must be **equal, or one of them must be 1**
4. A size-**1** axis **stretches** to match — virtually, no data is copied
5. Anything else → error. One failing pair is enough.

**What broadcasting can't do:** turn a 3 into a 4. Only a **1** stretches. (5,) can't become (5, 2) either — that would need values that don't exist.

### Rule 2 — the dot rule (for `@`, `np.dot`)

1. **Order matters** — write the shapes in the order of the call
2. The **inner** pair must match: **last** dim of the first ↔ **first** dim of the second
3. The matched dims **cancel**; the **outer** dims survive into the result
4. `(m × n) @ (n × p) → (m × p)`
5. A 1D array's single dim is both its first and last — so a `(3,)` can sit on either side

---

### Worked through: the file discounts

```python
counts   = np.array([[1200,  850,  930, 400],
                     [ 300,  310,  290, 150],
                     [2100, 1980, 2050, 900]])   # (3, 4): files × languages
discount = np.array([1.0, 0.9, 0.8])            # (3,): one per file
```

**Goal A — scale each file's row by its discount → element-wise `*`**

```
counts    :  3  4
discount  :  1  3      ← padded on the left with 1
             ✅ ❌     4 vs 3: not equal, neither is 1 → error
```

Fix: the 3 discounts describe the 3 **files**, so the 3 goes on the **rows** axis → **(3, 1)**

```
counts       :  3  4
discount_2d  :  3  1
                ✅ ✅    3 = 3, and the 1 stretches across the 4 languages → result (3, 4)
```

```python
discount_2d = discount[:, np.newaxis]   # (3,) → (3, 1); same as discount.reshape(3, 1)
counts * discount_2d                    # (3, 4): each row scaled by its own file's discount
```

`np.newaxis` lives in NumPy (not a method on the array) and goes **inside the index brackets** — its **position** decides where the new size-1 axis lands:
- `v[np.newaxis, :]` → new axis **first** → `(1, n)`
- `v[:, np.newaxis]` → new axis **last** → `(n, 1)`

**Goal B — weighted total per language → dot product**

```
np.dot(discount, counts)
discount  (3,)      ← last dim:  3
counts    (3, 4)    ← first dim: 3     inner 3s cancel → result (4,)
```

Each element = Σ over files of (discount × count) for one language. French = 1.0×1200 + 0.9×300 + 0.8×2100.

**Why `*` needed the reshape but `np.dot` didn't:** broadcasting aligns from the **right**, so the plain (3,) landed against the 4 languages. The dot rule matches the **inner** dims, so with `discount` first, its 3 met the 3 files directly.

---

### CAT link — weighted word count is a dot product

`np.dot(weights, counts)` = **weighted word count**: raw words × weights, summed. Same arithmetic a memoQ/Trados analysis uses to turn raw words into billable words for a quote.
- **Shared:** a weighted total is weights · counts
- **Differs:** in a CAT analysis the weights belong to **match bands** (100%, 95–99, 85–94, …), not to **files** — so the weights vector would line up against a band axis. Same math; different axis.

---

### Slips I made on the way

| Slip | Fix |
|---|---|
| Wrote `(3,4) @ (1,3)` for a `*` operation | `*` → broadcasting; `@` → dot. Don't mix the symbols |
| Padded the short shape with **0** | Pad with **1** |
| Wanted to stretch the 3 into a 4 | Only a **1** stretches; move the 3 to the axis it describes instead |
| Applied the "outer must match" idea to `*` | Inner/outer is the **dot** rule only |
| Said the dot rule checks the **outer** dims | The **inner** dims must match; the outer survive |
| Lined up `(3,4)` and `(3,)` for `np.dot(discount, counts)` | Keep the **call order**: `(3,)` first, then `(3,4)` |
| `discount.newaxis()` / `np,newaxis` | `discount[:, np.newaxis]` — NumPy attribute, inside the brackets, with a **dot** |

*Added: 2026-11-07 — re-entry carry-over: discount reshape, `*` vs `@`, weighted word counts*
