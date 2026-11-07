# Python & NumPy Cheatsheet
### pytorch-nlp-journey · msasinowski-loc
> **How to use in Notion:** Each `##` section is a toggle block. Use Ctrl/Cmd+F to search across all sections. Tags in `[brackets]` are searchable keywords.

---

## 📋 Table of Contents

- [NumPy — Arrays & Creation](#-numpy--arrays--creation)
- [NumPy — Indexing & Slicing](#-numpy--indexing--slicing)
- [NumPy — Vectorised Operations](#-numpy--vectorised-operations)
- [NumPy — Broadcasting](#-numpy--broadcasting)
- [NumPy — Matrix Operations](#-numpy--matrix-operations)
- [NumPy — Reshaping](#-numpy--reshaping)
- [NumPy — Reading shapes (the way I worked it out)](#-numpy--reading-shapes-the-way-i-worked-it-out)
- [Pandas — DataFrame basics](#-pandas--dataframe-basics)
- [XML parsing — ElementTree](#-xml-parsing--elementtree)
- [Pandas — Column Modification & String Cleaning](#-pandas--column-modification--string-cleaning)

---

## 🐍 NumPy — Arrays & Creation
`[numpy] [array] [creation] [zeros] [ones] [eye] [identity] [shape] [dtype]`

```python
import numpy as np

# From a list
v = np.array([1, 2, 3])          # 1D array / vector — shape (3,)
M = np.array([[1, 2], [3, 4]])    # 2D array / matrix — shape (2, 2)

# Constructors
np.zeros((2, 3))                  # 2×3 matrix of zeros
np.ones((3,))                     # vector of ones
np.eye(3)                         # 3×3 identity matrix (named after "I")
np.random.randn(4, 4)             # random normal values

# Inspection
v.shape                           # (3,) — tuple of dimensions
v.dtype                           # int64 / float64
v.ndim                            # number of dimensions
```

**Shape convention:** always (rows, columns) for 2D.
- `(3,)` — 1D, 3 elements, no concept of row/column yet
- `(3, 1)` — 2D column vector
- `(1, 3)` — 2D row vector
- `(2, 3)` — 2 rows, 3 columns

---

## 🐍 NumPy — Indexing & Slicing
`[numpy] [indexing] [slicing] [rows] [columns] [subset]`

```python
v = np.array([10, 20, 30, 40, 50])

v[0]          # first element → 10
v[-1]         # last element → 50
v[1:4]        # elements 1,2,3 → [20, 30, 40]
v[::2]        # every other → [10, 30, 50]

M = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])

M[0, :]       # first row → [1, 2, 3]
M[:, 1]       # second column → [2, 5, 8]   ← all rows, column index 1
M[1:, 1:]     # bottom-right 2×2 submatrix
```

**Mental model:** `M[row, col]` — row first, col second. `:` means "all".

---

## 🐍 NumPy — Vectorised Operations
`[numpy] [vectorised] [loops] [performance] [speed] [element-wise]`

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# All element-wise — no loops needed
a + b                   # [5, 7, 9]
a * b                   # [4, 10, 18]
a ** 2                  # [1, 4, 9]
np.sqrt(a)              # [1, 1.41, 1.73]

# Why: NumPy runs C/Fortran under the hood + contiguous memory + SIMD
# Rule: never loop over array elements — always find the NumPy call
```

**Speed benchmark (1M elements):**
- Python loop: ~0.14s
- NumPy: ~0.003s → ~50x faster

---

## 🐍 NumPy — Broadcasting
`[numpy] [broadcasting] [shapes] [dimensions] [expand]`

```python
a = np.array([1, 2, 3])          # shape (3,)
M = np.array([[1, 2, 3],
              [4, 5, 6]])         # shape (2, 3)

M + a         # (3,) treated as (1,3), broadcast across rows → (2,3)
              # [[2,4,6], [5,7,9]]

col = np.array([[10], [20]])      # shape (2, 1)
M + col       # (2,1) broadcast across columns → (2,3)
              # [[11,12,13], [24,25,26]]
```

**The rule:** align shapes from the right. Pad the shorter shape on the **left with 1** (not 0). Each pair must be **equal, or one of them 1**. A size-1 dimension stretches to match the other; anything else is an error.
**Full worked example (file discounts, `(3,)` → `(3, 1)`) and the `*` vs `@` comparison:** see `math_concepts_cheatsheet.md`, section "Element-wise `*` vs matrix product `@`".

| Operation | Shapes | Result |
|---|---|---|
| `M + scalar` | (2,3) + () | (2,3) |
| `M + row vec` | (2,3) + (3,) | (2,3) |
| `M + col vec` | (2,3) + (2,1) | (2,3) |

**Not the same as matrix multiplication** — broadcasting is always addition/element-wise, never dot product.

---

## 🐍 NumPy — Matrix Operations
`[numpy] [matrix] [dot product] [matmul] [norm] [cosine similarity] [linear algebra]`

```python
a = np.array([3, 4])
b = np.array([1, 0])

# Dot product — FundMath-LinAlg-005
np.dot(a, b)                            # 3·1 + 4·0 = 3

# L2 norm — FundMath-LinAlg-007
np.linalg.norm(a)                       # √(9+16) = 5
np.linalg.norm(a, ord=1)               # L1 norm (Manhattan) — FundMath-LinAlg-006

# Cosine similarity — FundMath-LinAlg-009
np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Matrix multiplication — FundMath-LinAlg-003
M = np.array([[1, 2], [3, 4]])
N = np.array([[5, 6], [7, 8]])
M @ N                                   # preferred syntax
np.matmul(M, N)                         # explicit, same result

# Identity matrix — FundMath-LinAlg-010
np.eye(3)                               # 3×3 I — neutral element of matmul
np.linalg.inv(M)                        # inverse — FundMath-LinAlg-011
np.linalg.eig(M)                        # eigenvalues & eigenvectors — FundMath-LinAlg-012
```

**Shape rule for matmul:** `(a×b) @ (b×c)` → `(a×c)`. Inner dims must match and disappear. **Order matters** — write the shapes in the order of the call.
**@ vs *:** `@` is matrix multiplication, `*` is element-wise. In code, `*` is *never* the matrix product — even though written maths often uses "×" for it.
**`A @ A.T` vs `A.T @ A`:** the outer dims survive, so `(2,3) @ (3,2)` → `(2,2)` compares **rows** with rows; `(3,2) @ (2,3)` → `(3,3)` compares **columns** with columns. Each cell `[i, j]` of `A @ A.T` is the dot product of row i with row j — a similarity matrix (not yet normalised). The diagonal holds each row's squared length.

---

## 🐍 NumPy — Reshaping
`[numpy] [reshape] [flatten] [newaxis] [dimensions] [shape] [word embedding] [batch]`

```python
a = np.arange(12)              # [0, 1, 2, ... 11] — shape (12,)

# reshape — total elements must stay the same
a.reshape(3, 4)                # → (3, 4)
a.reshape(4, -1)               # → (4, 3)  — -1 means "compute this dim for me"
a.reshape(2, 2, 3)             # → (2, 2, 3) — 3D, works too

# flatten — collapse any shape back to 1D
a.reshape(3, 4).flatten()      # → (12,)

# newaxis — insert a size-1 dimension without moving data
v = np.array([1, 2, 3])       # shape (3,)
v[np.newaxis, :]               # → (1, 3)  row vector
v[:, np.newaxis]               # → (3, 1)  column vector
```

**The key insight:** no data is copied — reshaping just changes the lens NumPy uses to read the same memory block.

**Word embedding example:**
```python
# "cat" as a 4-dim embedding
cat = np.array([0.2, 0.8, 0.1, 0.5])   # (4,)  — ambiguous
cat[np.newaxis, :]                        # (1, 4) — explicitly one word, 4 features
cat[:, np.newaxis]                        # (4, 1) — column vector for matmul

# batch of 3 words
batch = np.array([[0.2, 0.8, 0.1, 0.5],
                  [0.9, 0.1, 0.3, 0.2],
                  [0.1, 0.9, 0.8, 0.3]])  # (3, 4) — 3 words × 4 dims
```

**When to use newaxis:** when broadcasting needs explicit row/col distinction, or when PyTorch expects a batch dimension and your array is 1D.

| Shape | Meaning |
|---|---|
| `(768,)` | ambiguous flat vector |
| `(1, 768)` | one word embedding, batch-ready |
| `(768, 1)` | column vector for matmul |
| `(32, 768)` | batch of 32 embeddings |

---

## 🐍 NumPy — Reading shapes (the way I worked it out)
`[numpy] [shape] [ndim] [axis] [1D vs 2D] [row vs column] [transpose] [stack] [indexing] [slice]`

**The question I kept asking:** is `(5,)` the same as `(1, 5)`? **No** — and most of my shape slips came from treating them as the same.

### Read the brackets — the layout on the page doesn't matter
1. **Bracket depth = number of axes (`ndim`).** Count the `[` before the first number.
2. **Items at each level = the shape**, outer level first.

| Written as | Depth | Outer holds | Inner holds | Shape |
|---|---|---|---|---|
| `[4, 5]` | 1 | 2 numbers | — | `(2,)` |
| `[[4, 5]]` | 2 | 1 list | 2 numbers | `(1, 2)` |
| `[[4], [5]]` | 2 | 2 lists | 1 number each | `(2, 1)` |
| `[[1, 2], [3, 4]]` | 2 | 2 lists | 2 numbers each | `(2, 2)` |

Commas at the outer level separate **rows**. Line breaks are only for humans.

### `(n,)` vs `(1, n)` vs `(n, 1)`

```
      (2,)                   (1, 2)                  (2, 1)
  1 axis, length 2       2 axes: 1 row × 2 cols   2 axes: 2 rows × 1 col

    ┌───┬───┐               ┌───┬───┐                 ┌───┐
    │ 7 │ 8 │               │ 7 │ 8 │                 │ 7 │
    └───┴───┘               └───┴───┘                 ├───┤
  a line — no rows,       a grid that happens         │ 8 │
  no columns              to have one row             └───┘
                                                    a grid that happens
                                                    to have one column
```

| | `(2,)` | `(1, 2)` | `(2, 1)` |
|---|---|---|---|
| `.ndim` | 1 | 2 | 2 |
| Index one value | `x[0]` | `x[0, 0]` | `x[0, 0]` |
| `.T` | **no change** | → `(2, 1)` | → `(1, 2)` |

- **Don't call `(n,)` "1×n"** — "1×n" means two axes. A 1D array has a **length**, not rows and columns.
- **`.ndim` = how many numbers are in the shape.** `(5,)` → 1, `(1, 5)` → 2, `(2, 3, 4)` → 3. The values never change ndim — only the count does.
- **`.T` swaps axes that exist — it never creates one.** On a 1D array it's a valid no-op.
- **Axis size** = how many positions along that direction. `np.newaxis` always adds a size-**1** axis, so no data is created or copied.

### Building the same single-row grid three ways
```python
v = np.array([1, 2, 3, 4, 5])     # (5,), ndim 1
v.reshape(1, 5)                    # (1, 5), ndim 2
v[np.newaxis, :]                   # (1, 5), ndim 2 — new axis in slot 1
np.array([[1, 2, 3, 4, 5]])        # (1, 5), ndim 2 — outer holds 1 list of 5
v[:, np.newaxis]                   # (5, 1) — new axis in slot 2
```

### Integer vs slice when indexing
**An integer removes that axis; a slice keeps it.**
```python
counts.shape          # (3, 4)
counts[1, :]          # (4,)   — integer 1 drops the row axis
counts[1:2, :]        # (1, 4) — slice 1:2 keeps it (stops *before* 2 → one row)
counts[-2:, -2:]      # (2, 2) — slices on both axes keep both
```
To test a shape prediction, print **`.shape`**, not the values — the values can look identical.

### Stack vs concatenate vs add
| Operation | Two `(5,)` vectors become | What happens |
|---|---|---|
| `np.stack([a, b])` | `(2, 5)` | each vector becomes a **row**; a new axis appears; **no arithmetic** |
| `np.concatenate([a, b])` | `(10,)` | joined end-to-end; still one axis |
| `a + b` | `(5,)` | element-wise arithmetic |

`np.stack` takes **one** argument holding all the arrays (a list). `np.stack(a, b)` fails — Python reads `b` as the `axis` option.

### Comparing arrays
`a == b` compares **cell by cell** and returns an array of True/False. For one answer: `(a == b).all()`, or `np.allclose(a, b)` for floats (tolerates rounding).

### Attribute vs method
- **Read** without brackets (attributes): `.shape`, `.ndim`, `.T`
- **Call** with brackets (methods): `.head()`, `.reshape(1, 5)`, `.all()`, `.sum()`
- `df.shape()` → `TypeError: 'tuple' object is not callable` — the tuple is the shape itself

*Added: 2026-11-07 — shapes refresher from the bench sessions of 2026-10-20 to 2026-10-27*

---

*Last updated: Day 4 — NumPy reshaping complete*
*Next: Pandas · PyTorch tensors · OOP*

---

## 🐍 Pandas — DataFrame basics
`[pandas] [dataframe] [series] [read_csv] [loc] [iloc] [filter] [groupby] [missing] [nan]`

```python
import pandas as pd
import numpy as np

# Create DataFrame from dict
df = pd.DataFrame({
    'language':  ['English', 'French', 'German'],
    'segments':  [1200, 850, 930],
    'coverage':  [1.0, 0.85, None]       # None → NaN automatically
})

# Load from file
df = pd.read_csv('file.csv')                          # basic read
df = pd.read_csv('file.csv', encoding='utf-8-sig')    # handle BOM (Excel exports)
df = pd.read_csv('file.csv', index_col=0)             # use first column as index

# Inspection
df.shape          # (3, 3) — rows, cols
df.dtypes         # column types — strings show as 'object'
df.head()         # first 5 rows
df.head(10)       # first N rows
df.columns.tolist()  # list of column names
df.isnull().sum() # count missing per column

# Display options — useful when terminal truncates output
pd.set_option('display.max_columns', None)   # show all columns
pd.set_option('display.max_colwidth', None)  # show full cell content
pd.reset_option('display.max_columns')       # reset to default

# Column and row access
df['language']           # single column → Series
df[['language', 'segments']]  # multiple columns → DataFrame
df.loc[1]                # row by index label
df.loc[1, 'segments']    # specific cell by label
df.iloc[1]               # row by integer position
df.iloc[1, 0]            # cell by integer position

# Filtering
df[df['segments'] > 900]             # boolean filter
df[df['coverage'].isnull()]          # rows with missing values
df[~df['coverage'].isnull()]         # rows without missing values

# Add computed column
df['pct'] = df['coverage'] * 100

# Groupby
df.groupby('language')['segments'].sum()         # sum per group
df.groupby('language')['segments'].count()        # count non-null per group
df.groupby('language')['segments'].mean()         # mean per group, nulls ignored

# Multiple aggregations at once
df.groupby('language').agg({
    'source': 'count',     # same as .count() — pass as string or function
    'target': 'count',
    'tgt_len': 'mean'
})
# Other agg options: 'sum', 'min', 'max', 'std', 'first', 'last'
# Pass np.mean etc. instead of string for custom functions

# Count non-null values as 0/1 (useful for coverage %)
df['translated'] = df['target'].notna().astype(int)
# notna() → True/False per row, astype(int) → 1/0
# Then groupby().sum() gives count of translated segments
# Note: astype(int) crashes if NaNs present — use 'Int64' (capital I) for nullable int

# Coverage pattern
total = df.groupby('language')['source'].count()
translated = df.groupby('language')['target'].count()
coverage = translated / total * 100

# Missing values
df.isnull()              # boolean mask of missing values
df.dropna()              # drop rows with any NaN
df.fillna(0)             # replace NaN with 0
df.loc[1, 'coverage'] = np.nan   # manually set a missing value
```

**loc vs iloc:**
- `loc` — label-based (use index labels and column names)
- `iloc` — integer-based (use position numbers, 0-indexed)
- Matters when index isn't 0,1,2,3 — e.g. after filtering

---

## 🐍 XML parsing — ElementTree
`[xml] [elementtree] [tmx] [xliff] [parse] [findall] [attrib] [localization]`

```python
import xml.etree.ElementTree as ET

# ── XML element anatomy ───────────────────────────────────────
# <book id="1" rating="5">Deep Learning</book>
#  ↑ tag name  ↑ attributes (dict)      ↑ .text (string)
#
# <book id="1" rating="5">   → element with 2 attributes, no text
# <title>Deep Learning</title> → element with 0 attributes, has text
# <year></year>               → element with 0 attributes, .text = None
#
# Attributes live INSIDE the opening tag.
# Text content lives BETWEEN opening and closing tags.
# Child elements also live between tags — but as nested XML.

# Load from file vs string
tree = ET.parse('file.tmx')        # parse a file → ElementTree object
root = tree.getroot()               # get root element
root = ET.fromstring(xml_string)    # parse a string directly → root element

# find() vs findall()
root.find('book')                   # first match only — like regex non-greedy stop
root.findall('book')                # ALL matches → list
root.findall('body/tu')             # path navigation — all <tu> inside <body>
tu.findall('tuv')                   # all <tuv> inside a <tu>
tuv.find('seg')                     # first <seg> inside a <tuv>

# Read attributes — always two separate steps
element.attrib                      # full dict of ALL attributes
element.attrib['id']                # one specific attribute by key
# Never use find("book id") — path syntax is tag names only, not tag+attribute

# Read text content
seg.text                            # string content, or None if empty
seg.text or ''                      # handle None safely
seg.text if seg is not None and seg.text else None   # full safe pattern

# Namespace handling (TMX uses xml: namespace)
XML_LANG = '{http://www.w3.org/XML/1998/namespace}lang'
lang = tuv.attrib[XML_LANG]         # 'en-US', 'fr-FR', etc.

# TMX parsing pattern
segments = []
for tu in root.findall('body/tu'):
    source = None
    target = None
    target_lang = None
    for tuv in tu.findall('tuv'):
        lang = tuv.attrib[XML_LANG]
        seg = tuv.find('seg')
        text = seg.text if seg is not None and seg.text else None
        if lang == 'en-US':
            source = text
        else:
            target = text
            target_lang = lang
    segments.append({
        'source': source,
        'target': target,
        'target_lang': target_lang,
        'source_len': len(source.split()) if source else 0,
        'target_len': len(target.split()) if target else 0,
    })

df = pd.DataFrame(segments)
```

**File path note:**
- Never hardcode absolute paths in shared code
- Relative paths work if you `cd` into the project dir first
- For robust scripts: `os.path.join(os.path.dirname(__file__), 'file.tmx')`

---

*Last updated: Day 7 — XML element anatomy and find vs findall clarified*
*Next: PyTorch tensors · OOP · TMX parser project*

---

## 🐼 Pandas — Column Modification & String Cleaning
`[pandas] [column] [str] [replace] [strip] [regex] [vectorized] [apply] [cleaning]`

```python
# ── Modify a column in place ──────────────────────────────────────
df['column'] = df['column'].any_modification_here

# Same variable for source and target — overwrites in place
cleaned_df['source'] = cleaned_df['source'].str.replace(' +', ' ', regex=True).str.strip()
cleaned_df['target'] = cleaned_df['target'].str.replace(' +', ' ', regex=True).str.strip()
```

**The `.str.` accessor** — bridges from a Pandas Series to string methods.
You must use it before any string method (`str.replace`, `str.strip`, `str.contains`, etc.).
Without it, Pandas doesn't know you want string operations.

**Vectorized vs apply:**

| | Vectorized (`str.replace`, `str.strip`, math ops) | `apply(fn)` |
|---|---|---|
| How it runs | C loop under the hood — fast | Python loop — slower |
| When to use | Standard string/math transformations | Custom per-row logic |
| Example | `.str.replace(' +', ' ', regex=True)` | `.apply(lambda x: my_function(x))` |

**Chaining** — each method returns a Series, so you can keep chaining:
```python
df['col'].str.replace(pattern, replacement, regex=True).str.strip().str.lower()
```

**Common string methods:**

```python
df['col'].str.replace(r'<[^>]+>', '', regex=True)   # strip HTML/inline tags
df['col'].str.replace(' +', ' ', regex=True)         # collapse multiple spaces
df['col'].str.strip()                                 # remove leading/trailing spaces
df['col'].str.contains(pattern, na=False)             # boolean mask — use na=False to handle NaN
df['col'].str.lower()                                 # lowercase
df['col'].str.split(' ')                              # split into list
```

**Note:** always pass `regex=True` to `str.replace()` when using a pattern — without it Pandas
may warn or treat the pattern as a literal string.

*Added: 2026-10-11 — column modification, vectorized ops, str accessor, apply*
