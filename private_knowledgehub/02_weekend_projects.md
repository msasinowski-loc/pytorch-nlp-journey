# Weekend Projects — pytorch-nlp-journey
### msasinowski-loc · localization × NLP/ML engineering

> One coding-only project per weekend, 30–90 minutes. Grounded in real localization work where possible. Each project either uses skills already in the KA or expands by one new tool/concept.

---

## 🔨 In progress

### Near-duplicate detector — *weekend of 2026-10-24*
**Goal:** Find near-duplicate source segments inside one TM (internal fuzzy matches), score them with cosine similarity on word-count vectors, and report them in CAT-style match bands (100 / 95–99 / 85–94 / 75–84).
**CAT link:** Same idea as memoQ's homogeneity analysis (segments compared within the document, not against a TM). Differences: memoQ runs in document order and uses proprietary scoring; this tool scores all pairs at once with transparent cosine, which ignores word order. Not imitating memoQ for now.
**Data:** `parsed_tmx_raw_CleanedUp.csv` (regexes applied); `parsed_tmx_raw.csv` kept untouched as reference. 8,552 segments, EN→ES-US, LIUNA project.
**File:** `weekend_projects/weekend5_SimilarityFinder.py` (header docstring with version log, v0.3)

**Milestones**

| # | Milestone | Status |
|---|---|---|
| M1 | Load, clean, sample 500 | ✅ closed 2026-11-08 (v0.2) |
| M2 | Vocabulary (word → column index) | 🟡 started 2026-11-14 (v0.3): decisions made, `tokenise()` built |
| M3 | Count matrix A, shape (N, V) | ⬜ |
| M4 | Similarity matrix `A @ A.T`, normalised to cosine | ⬜ |
| M5 | Pair extraction: upper triangle, threshold | ⬜ |
| M6 | Report: sorted CSV and counts per match band | ⬜ |

**Progress check (2026-10-25)**
- Scoped M1–M6. Wrote the header docstring: purpose, CAT comparison, key maths, design decisions, version log.
- Chose the CleanedUp dataset, because leftover tag codes would otherwise become "words" in the bag-of-words.
- Loaded the data: `(8552, 5)`.
- Built the empty-source mask once and reused it: NaN **or** whitespace-only (`.str.strip() == ''`). It finds **42 empty rows**.
- Prediction vs result: predicted about 214 extra rows (a 2.5% rate from a 40-row look at the raw file); got 42 in total. The miss is probably down to the small sample and the tag-heavy file opening.

**Progress check (2026-10-31)**
- Refactored the mask into two named halves, a NaN test and a whitespace test, with the combined mask built from those two names.
- Wrote the removal line: `dataset_no_empty_segments = dataset[~is_empty_source_combined]`.
- Prediction recorded, not yet tested: about 42 from the NaN test and very few from whitespace, because `read_csv` turns empty fields into NaN.
- Paused here: the split counts (summing each half-mask) haven't been run yet.
- No session between 2026-11-01 and 2026-11-06 (unplanned break).

**Progress check (2026-11-07/08): M1 closed**
- Split counts: **42 NaN, 0 whitespace**. The prediction held: `read_csv` turns empty fields into NaN by default.
- The whitespace test stays as defensive code. It caught nothing today, but a field containing only spaces would *not* become NaN.
- Removal checked against the prediction: 8,552 − 42 = **8,510 rows**, `(8510, 5)`.
- Sampled **500 rows** with `random_state=42`, so results stay reproducible across sessions and machines. The sample keeps the original row labels.
- Source column turned into a list of length 500.
- Found the **real reason for removing empty segments**: an all-zero word-count vector has L2 norm 0, which puts a 0 in the cosine denominator in M4. NumPy quietly returns NaN, and that NaN spreads into every pair involving the segment.
- Version log v0.2 written. The header title now matches the file.

**Progress check (2026-11-14): M2 started** (first project session of the Forge pilot)
- M1 leftovers done: the `source_len` TODO is in Design decisions, and the typo is fixed.
- M2 decisions recorded in the header, each with its why:
  - **Case:** all lowercase. Accepted risk: an all-caps acronym that spells a word (SHIP vs "ship").
  - **Punctuation:** stripped. Low risk, and simpler. Side effect: `{` and `}` go too.
  - **`{}` placeholders:** tabled until there are real examples to assess.
  - **Placeholder-only segments:** filtered out of scoring, because they would become zero vectors. Counting and reporting them is still a TODO.
  - **Exact duplicates:** reported as repetitions, deduplicated on **raw text** (case and punctuation can carry meaning) and **before sampling** (true repetition counts for the whole TM).
  - **Bands:** 100 / 95–99 / 85–94 / 75–84, mirroring CAT.
- Pipeline redrawn: load → remove empty → dedupe raw text (count repetitions) → sample 500 → tokenise → filter `[]` (count) → vocabulary → M3.
- Built `tokenizer(text)`: regex `[^\w\s]` → space, then lowercase, then `.split()`. All four test predictions checked out, apart from one:
  - `"{} Underground Utilities {}"` → `['underground', 'utilities']`
  - `"Before using a pile driver…"` → `['before', 'using', 'a', 'pile', 'driver']`
  - The long "MUST be avoided" segment → clean lowercase words
  - `"‹#›"` → **`[]`**. Predicted `['   ']`. `.split()` with no arguments drops empty pieces, so whitespace-only text gives an empty list. That's the signature of a placeholder-only segment, and `if not tokens` is the filter test.
- Known limitation recorded: bag-of-words breaks compounds ("pile driver", "hard hat"). Future enhancement: n-grams, which would also partly address the word-order blind spot.

**Learned along the way**
- The `.str` accessor bridges a Series to string methods.
- `''` is a present (empty) string, not null, so `.isnull()` never catches it.
- Each condition joined with `|` needs its own brackets, because `|` binds tighter than `==`.
- Attributes are read without brackets (`.shape`, `.T`); methods are called with them (`.head()`, `.reshape()`).
- Anchor predictions on a sample, and be wary of non-random samples.
- A prediction can be a calculation, not a guess: work out the expected value, then check that the code matches it.
- Summing a boolean mask counts its True values.
- `.sample(n, random_state)` keeps the original index; `.tolist()` turns a Series into a list. Both are now in the cheatsheet.
- NaN doesn't create wrong scores, it makes pairs disappear: any comparison with NaN is False, and any average that includes NaN becomes NaN.
- `regex=True` belongs to pandas' `.str.replace`. On a plain string, use `re.sub(pattern, repl, text)`, and assign the result, because strings can't be changed in place.
- Write regex patterns as raw strings (`r'...'`) so that `\w` reaches the regex untouched.
- Replace punctuation with a **space**, not nothing, so that `end-to-end` becomes three words.

**Open findings**
- **`source_len` is stale:** empty sources still show `source_len = 3`, so it was computed before the cleanup. Recompute it after cleaning, or don't rely on it. *Recorded as a `[TODO]` in the header on 2026-11-14.*
- ✅ ~~NaN vs whitespace hypothesis~~: confirmed, 42 NaN and 0 whitespace.
- **`{}` placeholders:** tabled. Check real examples once the core build works.

**Next steps** (as of 2026-11-14)
1. **Move dedupe into M1:** deduplicate on raw text after removing empty sources and before `.sample()`, and keep a repetition count.
2. **The `[]` filter:** tokenise the sample, separate out segments with no tokens, and count them.
3. **The vocabulary dict:** each unique token → a column index (0, 1, 2…). Predict roughly how many unique words 500 segments will give, then print the size and 10 entries.
4. **M3:** the count matrix A, shape (N, V).
5. **End of queue:** replace the two hardcoded machine paths with a `pathlib` path relative to the script. First make the data folder names match (`tmxes_processed` on the rig vs `tmx_processed` on the laptop). Exercises KA `Ph1-Python-004b-Coding`.

---

## ✅ Completed

### TMX Parser v1 — *Week 1 weekend*
**Goal:** Parse a sample TMX file, extract source/target pairs into a DataFrame.
**Outcome:** Surfaced critical gaps in XML parsing and dict building. Deferred.
**Gap identified:** `Ph1-Loc-001-Coding` and `Ph1-Loc-002-Coding` added at confidence 0.

### TMX Parser v2 — *Week 2 weekends (multi-session)*
**Goal:** Production-ready TMX parser that handles real work files.
**Outcome:** Parser reads `srclang` from header dynamically, uses `itertext()` for inline tags, strips MemoQ formatting codes via regex, outputs coverage stats via groupby.
**Files:** `week2_project_tmxParser/tmx_parser.py`
**Status:** Working on real production TMX (LIUNA, 8,552 segments EN→ES-US). Not yet pushed to GitHub.

### tm_cleaner.py scaffolding — *Week 2 weekends*
**Goal:** Standalone cleaning pipeline — detect problems, dispatch cleaning functions.
**Outcome:** Dispatch table pattern implemented. `detect_inline_tags()` working. `strip_unescaped_tags()` implemented. Curly placeholders, escaped tags, hash placeholders detected.
**Files:** `week2_project_tmxParser/tm_cleaner.py`
**Status:** In progress — cleaning functions need completing.

### Length Ratio QA Report v1 — *2026-09-26*
**Goal:** Compute source/target length ratio per segment. Flag statistical outliers. Real MT quality signal used at LSPs.
**Data:** `parsed_tmx_raw_reference.csv` — 8,552 EN→ES-US segments, LIUNA project.
**Skills used:** Pandas, NumPy, standard deviation / z-score outlier detection.
**Output:** `lqa_length_ratio_report.csv` + summary stats.
**Status:** v1 complete.

---

## 💡 Ideas for later

### Segment type classifier
Categorise each segment into types using regex + word count rules:
- `placeholder_only` — segments containing only `‹#›`, `{}`, `{0}` etc.
- `tag_heavy` — segments where >50% of tokens are inline tags
- `ui_string` — short segments ≤ 3 words after cleaning
- `full_sentence` — >10 words, likely prose
- `number_only` — segments that are purely numeric

**Output:** enriched DataFrame with `segment_type` column + breakdown report.
**Skills needed:** regex, Pandas apply/map, value_counts.

### Near-duplicate detector → *now in progress (see top)*
Find source segments that are very similar to each other using cosine similarity on word frequency vectors. Flags fuzzy matches in the TM — real coverage analysis tool.
**Skills needed:** NumPy cosine similarity (see KA `FundMath-LinAlg-004` for current confidence — KA is the source of truth), basic tokenisation.

### MT quality estimator (stretch)
Use length ratio + segment type + tag density as features to score each segment's translation quality without a reference. Outputs a risk score per segment.
**Skills needed:** Pandas feature engineering, basic scoring logic.

---

## 📁 Reference data

| File | Description |
|---|---|
| `parsed_tmx_raw_reference.csv` | Raw parser output — 8,552 EN→ES-US segments, LIUNA project, all noise intact |
| `sample_tm.tmx` | Synthetic 15-segment TMX used for initial testing |
| `parsed_tmx_raw.csv` | Parser output before regex cleanup; untouched reference for the near-duplicate detector |
| `parsed_tmx_raw_CleanedUp.csv` | Same data with the cleanup regexes applied; input for the near-duplicate detector |
