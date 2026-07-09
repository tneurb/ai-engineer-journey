def is_even(numbers):
    new_numbers = []
    for number in numbers:
        if number % 2==0:
            new_numbers.append(number)
            
    return new_numbers
print(is_even([1, 2, 3, 4, 5, 6]))
# should print [2, 4, 6]

# def is_even(numbers):
#    return [newnumber.append(number) for number in numbers if number%2==0]

def is_even(numbers):
    return [numbers for number in numbers if number%2==0]

def get_long_words(words): 
    return [word for word in words if len(word)>=4]
def summarise_words(words):
    return {word : len(word) for word in words}