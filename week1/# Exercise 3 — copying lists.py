# Exercise 3 — copying lists
original = [1, 2, 3, 4, 5]

# Method 1 — .copy()
copy1 = original.copy()

# Method 2 — list()
copy2 = list(original)

# Method 3 — slice
copy3 = original[:]

# Modify each copy
copy1.append(10)
copy2.append(20)
copy3.append(30)

print("original:", original)
print("copy1:   ", copy1)
print("copy2:   ", copy2)
print("copy3:   ", copy3)