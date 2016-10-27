import matplotlib.pyplot as plt
import sys

data = []
data_ma = []
with open(sys.argv[1], 'r') as infile:
    for line in infile:
        data.append(float(line.split()[1]))

with open(sys.argv[2], 'r') as infile:
    for line in infile:
        data_ma.append(float(line.split()[1]))

plt.plot(data, color='red', lw=2)
plt.plot(data_ma, color='black', lw=2)
plt.show()
