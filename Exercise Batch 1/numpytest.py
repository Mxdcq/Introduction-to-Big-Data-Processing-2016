import sys
import numpy as np

user_input = sys.argv[1:]

my_list = np.loadtxt(user_input[0])

print("Minimum:", np.amin(my_list))
print("Maximum:", np.amax(my_list))
print("Average:", np.average(my_list))
print("Median:", np.median(my_list))
print("Variance:", np.nanvar(my_list))