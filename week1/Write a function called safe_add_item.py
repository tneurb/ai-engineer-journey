"""Write a function called safe_add_item(original_list, item) that:
— takes a list and an item
— adds the item to a COPY of the list (not the original)
— returns the new list
— the original list must stay unchanged

Then test it by calling it and printing both the original and the returned list."""

number_list = [1,2,3,4]
def safe_add_item(original_list, item):
    output_list = original_list.copy()
    output_list.append(item)
    return output_list

print(safe_add_item(number_list,5))
print(number_list)

def safe_add_item(original_list, item):
    new_list = original_list.copy()
    new_list.append(item)
    return new_list

# Test it
my_list = [1, 2, 3]
result = safe_add_item(my_list, 99)

print("original:", my_list)   # [1, 2, 3] — unchanged
print("result:  ", result)    # [1, 2, 3, 99]