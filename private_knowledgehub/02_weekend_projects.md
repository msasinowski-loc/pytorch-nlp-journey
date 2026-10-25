# Weekend Projects — pytorch-nlp-journey
### msasinowski-loc · localization × NLP/ML engineering

> One coding-only project per weekend, 30–90 minutes. Grounded in real localization work where possible. Each project either uses skills already in the KA or expands by one new tool/concept.

---

## 🔨 In progress

### Near-duplicate detector — *weekend of 2026-10-24*
**Goal:** Find near-duplicate source segments inside one TM (internal fuzzy matches), score them with cosine similarity on word-count vectors, and report them in CAT-style match bands (100 / 95–99 / 85–94 / 75–84).
**CAT link:** Same idea as memoQ's homogeneity analysis (segments compared within the document, not against a TM). Differences: memoQ runs in document order and uses proprietary scoring; this tool scores all pairs at once with transparent cosine, which ignores word order. Not imitating memoQ for now.
**Data:** `parsed_tmx_raw_CleanedUp.csv` (regexes applied); `parsed_tmx_raw.csv` kept untouched as reference. 8,552 segments, EN→ES-US, LIUNA project.
**File:** `weekend_projects/weekend5_SimilarityFinder.py` (header docstring with version log, v0.1)

**Milestones**

| # | Milestone | Status |
|---|---|---|
| M1 | Load, clean, sample 500 | 🟡 partly done |
| M2 | Vocabulary (word → column index) | ⬜ |
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

**Learned along the way**
- The `.str` accessor bridges a Series to string methods.
- `''` is a present (empty) string, not null, so `.isnull()` never catches it.
- Each condition joined with `|` needs its own brackets, because `|` binds tighter than `==`.
- Attributes are read without brackets (`.shape`, `.T`); methods are called with them (`.head()`, `.reshape()`).
- Anchor predictions on a sample, and be wary of non-random samples.

**Open findings**
- **`source_len` is stale:** empty sources still show `source_len = 3`, so it was computed before the cleanup. Recompute it after cleaning, or don't rely on it.
- **NaN vs whitespace:** all five rows inspected are NaN, not whitespace. Hypothesis to check: an empty string saved to CSV comes back as NaN through `read_csv`.

**Next steps**
1. Split the 42 into Test A (NaN) and Test B (whitespace) counts.
2. Write the removal line with `~is_empty_source`.
3. Take the 500-row sample with a fixed `random_state`, and turn the source column into a list.
4. Add the M1 entry to the version log and record the `source_len` finding as a TODO.
5. M2: make the tokenisation decisions: lowercase, punctuation, `{}` placeholders, placeholder-only segments (`‹#›`), and exact duplicates reported as repetitions.
6. **End of queue:** replace the two hardcoded machine paths with a `pathlib` path relative to the script. First make the data folder names match (`tmxes_processed` on the rig vs `tmx_processed` on the laptop). Exercises KA `Ph1-Python-004b-Coding`.

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
