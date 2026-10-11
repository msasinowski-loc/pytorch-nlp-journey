# Weekend Projects — pytorch-nlp-journey
### msasinowski-loc · localization × NLP/ML engineering

> One coding-only project per weekend, 30–90 minutes. Grounded in real localization work where possible. Each project either uses skills already in the KA or expands by one new tool/concept.

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

### Length Ratio QA Report — *2026-09-26*
**Goal:** Compute source/target length ratio per segment. Flag statistical outliers. Real MT quality signal used at LSPs.
**Data:** `parsed_tmx_raw_reference.csv` — 8,552 EN→ES-US segments, LIUNA project.
**Skills used:** Pandas, NumPy, standard deviation / z-score outlier detection.
**Output:** `lqa_length_ratio_report.csv` + summary stats.
**Status:** In progress this session.

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

### Near-duplicate detector
Find source segments that are very similar to each other using cosine similarity on word frequency vectors. Flags fuzzy matches in the TM — real coverage analysis tool.
**Skills needed:** NumPy cosine similarity (already at confidence 2), basic tokenisation.

### MT quality estimator (stretch)
Use length ratio + segment type + tag density as features to score each segment's translation quality without a reference. Outputs a risk score per segment.
**Skills needed:** Pandas feature engineering, basic scoring logic.

---

## 📁 Reference data

| File | Description |
|---|---|
| `parsed_tmx_raw_reference.csv` | Raw parser output — 8,552 EN→ES-US segments, LIUNA project, all noise intact |
| `sample_tm.tmx` | Synthetic 15-segment TMX used for initial testing |
