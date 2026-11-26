# Weekend Projects — pytorch-nlp-journey
### msasinowski-loc · localization × NLP/ML engineering

> One coding-only project per weekend, 30–90 minutes. Grounded in real localization work where possible. Each project either uses skills already in the KA or expands by one new tool/concept.

---

## 💡 Ideas for later

### i18n linter — *stand-alone project, inspired by an industry peer's post (seen 2026-11-21)*
**Source:** https://juliadiez.substack.com/p/i-turned-my-i18n-checklist-into-a
A command-line linter that scans an app's code and translation files and flags i18n bugs before they ship: hardcoded user-facing text, sentences glued together from pieces, hand-rolled plurals, keys missing from the source file, poor key names (a 0–100 naming score), placeholders translated or dropped (`{name}` → `{nom}`), missing plural forms per language.
**Why I want to build it:**
- **A linter is a kind of tool I've never built**: parsing code, rules, a report, a CI exit code.
- **A different tech stack**: the original runs on Node (`npx`) against React/Vue/Svelte/Flutter projects. Good exposure beyond Python and pandas.
- **An interview hook for more technical roles**: it sits right where localization expertise meets engineering.
**Head start:** the placeholder checker (OOP week, Nov 23–29) is a small version of its third layer, run on a TM instead of app files.
**Skills needed:** regex, file walking, JSON parsing, rule design, CLI arguments, CI basics; JavaScript/Node if built in the original stack.

### Segment type classifier
Categorise each segment into types using regex + word count rules:
- `placeholder_only` — segments containing only `‹#›`, `{}`, `{0}` etc.
- `tag_heavy` — segments where >50% of tokens are inline tags
- `ui_string` — short segments ≤ 3 words after cleaning
- `full_sentence` — >10 words, likely prose
- `number_only` — segments that are purely numeric

**Output:** enriched DataFrame with `segment_type` column + breakdown report.
**Skills needed:** regex, Pandas apply/map, value_counts.

### Near-duplicate detector → *now in progress (see below)*
Find source segments that are very similar to each other using cosine similarity on word frequency vectors. Flags fuzzy matches in the TM — real coverage analysis tool.
**Skills needed:** NumPy cosine similarity (see KA `FundMath-LinAlg-004` for current confidence — KA is the source of truth), basic tokenisation.

### MT quality estimator (stretch)
Use length ratio + segment type + tag density as features to score each segment's translation quality without a reference. Outputs a risk score per segment.
**Skills needed:** Pandas feature engineering, basic scoring logic.

---

## 🗓️ Up next: placeholder checker — *OOP week, 2026-11-23 to 11-29*
Decided 2026-11-21, for 9 days of 60 minutes (Nov 21–29):
- **Sat 21 – Sun 22:** detector M3–M4, to reach a clean pause point.
- **Mon 23 – Fri 27:** 20 min OOP theme, then 40 min building a placeholder checker as a **class** from day one.
- **Sat 28 – Sun 29:** finish it and run it on the full TM; Sunday is the teach-back and weekly check-in.
**Goal:** for each TM row, do the target's placeholders match the source's (`{}`, `{0}`, `‹#›`…)? Report mismatches.
**Bernoulli link:** "placeholders intact?" is a yes/no per row, so its mean is the TM's placeholder error rate.
**CAT link:** the tag/placeholder mismatch check in memoQ QA and Xbench.
**Data:** `parsed_tmx_raw_CleanedUp.csv` (source and target columns). Also unblocks the tabled `{}` decision in the detector.
**Folder:** `_sideProjects/01_ooo_Intro/`. **Status (2026-11-26):** v0.1, `Segment` class with `__init__`, `extract_placeholders(text)` and `placeholders_match()`; first mismatch found on a test row.

---

## 🔨 In progress

### Near-duplicate detector — *weekend of 2026-10-24*
**Goal:** Find near-duplicate source segments inside one TM (internal fuzzy matches), score them with cosine similarity on word-count vectors, and report them in CAT-style match bands (100 / 95–99 / 85–94 / 75–84).
**CAT link:** Same idea as memoQ's homogeneity analysis (segments compared within the document, not against a TM). Differences: memoQ runs in document order and uses proprietary scoring; this tool scores all pairs at once with transparent cosine, which ignores word order. Not imitating memoQ for now.
**Data:** `parsed_tmx_raw_CleanedUp.csv` (regexes applied); `parsed_tmx_raw.csv` kept untouched as reference. 8,552 segments, EN→ES-US, LIUNA project.
**Folder:** `week3-9_SimilarityFinder/` (renamed 2026-11-26; script `weekend5_SimilarityFinder.py`, header docstring with version log, v0.4)

**Milestones**

| # | Milestone | Status |
|---|---|---|
| M1 | Load, clean, sample 500 | ✅ closed 2026-11-08 (v0.2) |
| M2 | Vocabulary (word → column index) | ✅ closed 2026-11-15 (v0.4) |
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

**Progress check (2026-11-15): M2 closed** (v0.4)
- Dedupe moved before sampling: **2,243 repetitions** found in the 8,510 non-empty rows, leaving 6,267 unique rows.
- Top repeats: "{} Instructions {} :" (77), "During this activity you will:" (52), "CONTINUE" (46), "Complete the content above before moving on." (45), "{} {} Task 2 {} {} :" (32). Evidence for stripping `{}`.
- Vocabulary dict on the 500-row sample: **V = 1,863** (predicted about 1,750). **0** empty token lists.
- Mask renamed to `is_duplicate_source`.
- Week 1 (Bernoulli) found the share of repetitions: `is_duplicate_source.mean()` ≈ 0.26.

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
- **Paragraph-level TM units (found 2026-11-25):** `A.max()` = 27 turned out to be "the" ×27 in one TM unit that holds a whole paragraph (~10 sentences, formwork instructions). Not a code bug: the fill loop was verified (`A.sum()` = 7,175 = independent token count). The TM mixes sentence-level and paragraph-level units. Effect on M4: long units get large vector lengths, and function words like "the" dominate their vectors, so unrelated segments can look similar. **Decision: finish M1–M6 as is and accept this as a known limitation**, so the project doesn't keep growing. Future fixes, in order of likely value: stop-word removal or TF-IDF (Week 4 theme); flag or split over-long units (segmentation).

**Next steps** (as of 2026-11-14)
1. **Move dedupe into M1:** deduplicate on raw text after removing empty sources and before `.sample()`, and keep a repetition count.
2. **The `[]` filter:** tokenise the sample, separate out segments with no tokens, and count them.
3. **The vocabulary dict:** each unique token → a column index (0, 1, 2…). Predict roughly how many unique words 500 segments will give, then print the size and 10 entries.
4. **M3:** the count matrix A, shape (N, V).
5. **Tabled code-review findings (2026-11-14):** none break the current output.
   - ⚠️ `import regex as re` is the third-party package, so the script fails on a machine without it. The built-in `re` is enough. Fix before the next run on the rig.
   - Docstring `Finder \ near_…`: `\ ` is an invalid escape, and Python 3.12+ warns.
   - `tokenizer()` raises `TypeError` on NaN: keep the empty-row removal before tokenising, and add a comment saying so.
   - Header tidy-up: the duplicate `DESIGN DECISIONS` heading; the cut-off placeholder TODO ("0 billable…"); a fuller why for dedupe; update M1's pipeline line (now load → remove empty → dedupe → sample).
   - Naming: `tokenizer` vs `tokenise()` in the log.
   - KA list: add `Ph1-Python-012`, `Ph1-Python-003`, `Ph1-Loc-002`.
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

## 📁 Reference data

| File | Description |
|---|---|
| `parsed_tmx_raw_reference.csv` | Raw parser output — 8,552 EN→ES-US segments, LIUNA project, all noise intact |
| `sample_tm.tmx` | Synthetic 15-segment TMX used for initial testing |
| `parsed_tmx_raw.csv` | Parser output before regex cleanup; untouched reference for the near-duplicate detector |
| `parsed_tmx_raw_CleanedUp.csv` | Same data with the cleanup regexes applied; input for the near-duplicate detector |
