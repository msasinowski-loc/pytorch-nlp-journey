import numpy as np

# Setup data: word counts for 3 files × 4 target languages (FR, ES, DE, PL).

counts = np.array([[1200,  850,  930, 400],
                   [ 300,  310,  290, 150],
                   [2100, 1980, 2050, 900]])

# a) all DE counts 3x1
answer_1a = counts[:, 2]
print(counts)
print (counts.ndim)
print (answer_1a.ndim)
print(answer_1a)

# b) 1x4
answer_1b = counts[1, :]

# c) 2x2
answer_1c = counts[:-2 :-2]



answer_2a = counts * np.array([0.12, 0.10, 0.14, 0.16
])

# answer_2b the problem here is with broadcasting - the counts array is 3x4
# while the volume discount is a 1d vector
# I know numpy will broadcast, which means it will make the 1d vector 3x4 for the purpose of multiplication
# which makes me thinkg it's okay to multiply as is


# answer_3a = counts * I dont know
# counts @ counts.T should give the same shape, it's transposition
# same for other direction
# but I forgot how to code .T

# single cell of counts @ counts.T represents.... dunno