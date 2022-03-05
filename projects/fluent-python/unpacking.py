# Unpacking sequences and iterables
import os

t = (20, 8)
print(divmod(*t))

# Unpacking is prefixing an argument with * when calling a function
quotient, remainder = divmod(*t)
print(quotient, remainder)

# Use of unpacking: allowing functions to return multiple values in a way that is convenient to the caller
_, filename = os.path.split('/home/felipe/Desktop/python/projects/fluent-python/vector.py')
print(filename)

a, b, *rest = range(5)
print(a, b, rest)