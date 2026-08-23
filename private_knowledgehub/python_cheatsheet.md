# Python & NumPy Cheatsheet
### pytorch-nlp-journey · msasinowski-loc
> **How to use in Notion:** Each `##` section is a toggle block. Use Ctrl/Cmd+F to search across all sections. Tags in `[brackets]` are searchable keywords.

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

**The rule:** align shapes from the right. Any dimension of size 1 stretches to match the other.

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

**Shape rule for matmul:** `(a×b) @ (b×c)` → `(a×c)`. Inner dims must match and disappear.
**@ vs *:** `@` is matrix multiplication, `*` is element-wise.

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

# Inspection
df.shape          # (3, 3) — rows, cols
df.dtypes         # column types — strings show as 'object'
df.head()         # first 5 rows
df.isnull().sum() # count missing per column

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
df.groupby('language')['segments'].sum()    # sum per group
df.groupby('language')['segments'].count()  # count non-null per group

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
