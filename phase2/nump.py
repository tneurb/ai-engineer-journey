import numpy as np

# Exercise 1 — basic dot product
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print("Dot product:", np.dot(a, b))
# Predict the answer yourself first, then run it
#  32


# Exercise 2 — identical vectors
a = np.array([2, 3])
b = np.array([2, 3])
print("Dot product (identical):", np.dot(a, b))
# What do you expect?
# 11


# Exercise 3 — opposite vectors
a = np.array([1, 1])
b = np.array([-1, -1])
print("Dot product (opposite):", np.dot(a, b))
# Predict: positive, negative, or zero?
#-2

# Exercise 4 — perpendicular vectors (unrelated directions)
a = np.array([1, 0])
b = np.array([0, 1])
print("Dot product (perpendicular):", np.dot(a, b))
# Predict: what happens when vectors point in "unrelated" directions?
#0

# Exercise 5 — vector length (norm)
a = np.array([3, 4])
print("Length of [3,4]:", np.linalg.norm(a))
# Hint: this is the Pythagorean theorem — 3² + 4² = 25, √25 = 5
#5

# Exercise 6 — write cosine_similarity yourself
def cosine_similarity(a, b):
    # fill this in using np.dot and np.linalg.norm
    return np.dot(a,b)/ (np.linalg.norm(a) * np.linalg.norm(b))
    

a = np.array([1, 1])
c = np.array([100, 100])  # same direction, different length
print("Cosine similarity (same direction, diff length):", cosine_similarity(a, c))
# Predict: should this be close to 1.0, 0.0, or -1.0?
#1

a = np.array([3, 4])
print("Length of [3,4]:", np.linalg.norm(a))
#5
b = np.array([6, 8])  # same direction as a, just doubled
print("Length of [6,8]:", np.linalg.norm(b))
#10
c = np.array([1, 0])
print("Length of [1,0]:", np.linalg.norm(c))
#1
