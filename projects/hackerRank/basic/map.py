# Given the participants' score sheet for your University Sports Day, 
# you are required to find the runner-up score. 
# You are given N scores. Store them in a list and find the score of the runner-up.

n = int(input()) # 5
arr = list(map(int, input().split())) # 2 3 6 6 5

x = max(arr)
y = -100
for i in range(0, n):
    if arr[i] < x and arr[i] > y:
        y = arr[i]
print(y)

########################

'''
list_number = [7, 1, 2, 3, 2, 4, 5, 6, 3]
def square_number(x):
    return x**x

new_list = list(map(square_number, list_number))
max_value = max(new_list)
print(max_value)

while max_value == max(new_list):
    new_list.remove(max_value)
    new_list = sorted(new_list)
 
print(new_list[-1])
print(*new_list, sep=', ')
'''
