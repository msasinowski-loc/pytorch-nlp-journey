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

# Dot product — FM-LA-005
np.dot(a, b)                            # 3·1 + 4·0 = 3

# L2 norm — FM-LA-007
np.linalg.norm(a)                       # √(9+16) = 5
np.linalg.norm(a, ord=1)               # L1 norm (Manhattan) — FM-LA-006

# Cosine similarity — FM-LA-009
np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Matrix multiplication — FM-LA-003
M = np.array([[1, 2], [3, 4]])
N = np.array([[5, 6], [7, 8]])
M @ N                                   # preferred syntax
np.matmul(M, N)                         # explicit, same result

# Identity matrix — FM-LA-010
np.eye(3)                               # 3×3 I — neutral element of matmul
np.linalg.inv(M)                        # inverse — FM-LA-011
np.linalg.eig(M)                        # eigenvalues & eigenvectors — FM-LA-012
```

**Shape rule for matmul:** `(a×b) @ (b×c)` → `(a×c)`. Inner dims must match and disappear.
**@ vs *:** `@` is matrix multiplication, `*` is element-wise.

---

*Last updated: Day 3 — NumPy session complete*
*Next: Pandas · PyTorch tensors · OOP*
