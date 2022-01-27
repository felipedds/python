# List comprehensions
list_of_numbers = [x for x in range(10)]
print(list_of_numbers)

# Nested list comprehensions
list_nested = [[x, y] for x in range(10) for y in range(10)]
print(list_nested)

# Nested list comprehensions with three multiple
list_three_multiple = [x for x in range(100) if x % 3 == 0]
print(list_three_multiple)

x = 1
y = 1
z = 2
n = 3

list_comprehension = list([i, j, k] for i in range(x+1) for j in range(y+1) for k in range(z+1) if (i + j + k) != n)
print(list_comprehension)