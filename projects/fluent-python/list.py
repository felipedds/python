from array import array
from random import random

# Create an array of double-precision floats (typecode 'd')
floats = array('d', (random() for i in range(10 ** 7)))
print(floats[-1])

# Save the array to a binary file.
with open('floats.bin', 'wb') as fp:
    floats.tofile(fp)