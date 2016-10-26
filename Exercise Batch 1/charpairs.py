import sys

user_input = sys.argv[1:]
print(user_input)

my_dict = {}
total_list = []

for i in range(len(user_input)):
    for j in range(len(user_input[i]) - 1):
        total_list.append(user_input[i][j:j + 2])
print(total_list)

for i in total_list:
    if i not in my_dict:
        my_dict[i] = 1
    else:
        my_dict[i] += 1
print(my_dict)

for key in sorted(my_dict):
    print(key, ":", my_dict[key], "occurrences")