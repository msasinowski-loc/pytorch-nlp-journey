import numpy as np

<<<<<<< HEAD
z = np.array([-5, -1, 0, 1, 5])

# 1. Implement σ(z) — one line, from memory

sigma = 1 / (1 + np.exp(-z))

# 2. Print result with scientific notation suppressed

np.set_printoptions(suppress=True)

print(sigma)

# 3. Compute the derivative of sigmoid at each point:
#    σ'(z) = σ(z) · (1 − σ(z))
#    Print it — where is the derivative largest?

derivative_of_sigma = sigma * (1 - sigma)
print(derivative_of_sigma)

# 4. In a comment: why does σ'(z) being small at extremes
#    cause the vanishing gradient problem?

# because in hidden layers the gradients multiply, eventually becoming too small to leave an impact
=======
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
>>>>>>> e8603d41f3c00b790f3d7a920fafe63517328230
