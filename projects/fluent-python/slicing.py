# Slice object
s = 'bicycle'
print(s[::3])
print(s[::-1])

# Using + and * with Sequences
l = [1, 2, 3]
print(l * 5)

print(5 * 'abcd')

my_list = [[]] * 3
print(my_list)

# Building Lists of Lists
board = [['_'] * 3 for i in range(3)]
print(board)
board[1][2] = 'X'
print(board)

board = []
for i in range(3):
    row = ['_'] * 3
    board.append(row)
print(board)

# Bytecode for the expression s[a] += b
import dis
dis.dis('s[a] += b')