# Exercise 2 — immutable types
a = 10
b = a
b = b + 5      # creates a NEW value, doesn't change a

print("a:", a)
print("b:", b)
print("Same object?", a is b)

# Same with strings
s1 = "hello"
s2 = s1
s2 = s2 + " world"   # creates a NEW string

print("s1:", s1)
print("s2:", s2)
print("Same object?", s1 is s2)