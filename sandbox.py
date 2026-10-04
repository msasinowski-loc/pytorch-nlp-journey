import numpy as np

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