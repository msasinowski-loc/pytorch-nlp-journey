import numpy as np

z = np.array([-3.0, -1.0, 0.0, 1.0, 3.0])

# 1. σ(z) — one line from memory

sigma = 1 / (1 + np.exp(-z))

# 2. Suppress scientific notation, print

np.set_printoptions(suppress=True)

# 3. σ'(z) = σ(z) · (1 − σ(z)) — one line, print

sigma_det = sigma * (1 - sigma)
print(sigma_det)

# 4. Flag where σ(z) > 0.7 — boolean array, then print flagged z values

flagged_mask = sigma > 0.7
print(z[flagged_mask])
        

# 5. Comment: what does np.exp() do and why is it needed?
