from scipy import stats

# get the context from .csv file
lines_one = [line.split(',') for line in open('tracks.csv')]
lines_two = [line.split(',') for line in open('cust.csv')]

my_dict = {}
my_dict_gender = {}
my_dict_mobile = {}
total_list = []
total_list_mobile = []

# put all the (custID, trackID) into a list
for i in range(len(lines_one)):
    total_list.append(lines_one[i][1:3])

# count
for i in total_list:
    if i[0] not in my_dict:
        my_dict[i[0]] = [i[1]]
    else:
        if i[1] not in my_dict[i[0]]:
            my_dict[i[0]] = my_dict[i[0]] + [i[1]]
        else:
            continue

# get the maximun tracks number
max_tracks = 0
for pair in my_dict:
    if len(my_dict[pair]) > max_tracks:
        max_tracks = len(my_dict[pair])
print(max_tracks, 'tracks are the maximun tracks listened by a single customer!')
print('----------')

# get the related customer ID
customer_list = []
for pair in my_dict:
    if len(my_dict[pair]) == max_tracks:
        customer_list.append(pair)
print('The customer ID of the person is ', customer_list)
print('----------')

# get the related customer' name
for i in lines_two[1:]:
    for j in customer_list:
        if int(j) == int(i[0]):
            print('His or her name is ', i[1])
print('----------')

# Welch's-test
# Men and women
men = []
women = []

for i in total_list:
    if i[0] not in my_dict_gender:
        my_dict_gender[i[0]] = 1
    else:
        my_dict_gender[i[0]] += 1

for key in my_dict_gender:
    if lines_two[int(key) + 1][2] == '0':
        men.append(int(my_dict_gender[key]))
    if lines_two[int(key) + 1][2] == '1':
        women.append(int(my_dict_gender[key]))

# mobile and non-mobile
mobile = []
non_mobile = []

# put all the (custID, mobile) into a list
for i in range(len(lines_one)):
    total_list_mobile.append((lines_one[i][1], lines_one[i][4]))

# count
for i in total_list_mobile:
    if i[0] not in my_dict_mobile:
        my_dict_mobile[i[0]] = [i[1]]
    else:
        my_dict_mobile[i[0]] = my_dict_mobile[i[0]] + [i[1]]

for key in my_dict_mobile:
    mobile.append(my_dict_mobile[key].count('1'))
    non_mobile.append(my_dict_mobile[key].count('0'))

print("Hypothesis: Men and women listen to on average as many tracks.")
print(stats.ttest_ind(men, women, equal_var=False))
print("Hypothesis: non_mobile users and mobile users listen to on average as many tracks.")
print(stats.ttest_rel(mobile, non_mobile))