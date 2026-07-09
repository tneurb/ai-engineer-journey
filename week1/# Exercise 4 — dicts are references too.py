# Exercise 4 — dicts are references too
user = {"name": "Alice", "score": 100}

# Wrong way — both point to same dict
user_copy = user
user_copy["score"] = 999

print("user:", user)
print("user_copy:", user_copy)
print("Same object?", user is user_copy)

print("---")

# Right way — use .copy()
user2 = {"name": "Bob", "score": 100}
user2_copy = user2.copy()
user2_copy["score"] = 999

print("user2:", user2)
print("user2_copy:", user2_copy)