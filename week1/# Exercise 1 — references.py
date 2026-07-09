# Exercise 1 — references
x = [1, 2, 3]
#y = x          # y points to the SAME list as x
y = x.copy()
y.append(4)

print("x:", x)
print("y:", y)
print("Same object?", x is y)