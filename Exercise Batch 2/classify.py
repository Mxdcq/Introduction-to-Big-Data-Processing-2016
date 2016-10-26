# ming

from sklearn.linear_model import Perceptron
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

vertigo_train_np = np.loadtxt('vertigo_train.txt', dtype=int, delimiter=' ')
vertigo_train_np_data = vertigo_train_np[:, 1:]
vertigo_train_np_class = vertigo_train_np[:, 0]
# print(vertigo_train_np_data, vertigo_train_np_class)

vertigo_predict_np = np.loadtxt('vertigo_predict.txt', dtype=int, delimiter=' ')
vertigo_answers_np = np.loadtxt('vertigo_answers.txt', dtype=int, delimiter=' ')

p = Perceptron()
p.fit(vertigo_train_np_data, vertigo_train_np_class)
vertigo_predict_answers_p = p.predict(vertigo_predict_np[:, :])

total_correct_p = 0
for i in range(len(vertigo_answers_np)):
    if vertigo_answers_np[i] == vertigo_predict_answers_p[i]:
        total_correct_p += 1

# print(total_correct_p, len(vertigo_answers_np))
print("Perceptron: " + str(total_correct_p * 100 / len(vertigo_answers_np)) + "% correct")

manhattan = []
temp = 0
for i in range(len(vertigo_predict_np)):
    sum_min = 100000000
    for j in range(len(vertigo_train_np) - 1):
        sum = 0
        for k in range(5):
            sum += abs(vertigo_train_np[j][k+1] - vertigo_predict_np[i][k])
        if sum_min >= sum:
            sum_min = sum
            temp = vertigo_train_np[j][0]
    manhattan.append(temp)

total_correct_mine = 0
for i in range(len(vertigo_answers_np)):
    if vertigo_answers_np[i] == manhattan[i]:
        total_correct_mine += 1

print("Nearest neighbor: " + str(total_correct_mine * 100 / len(vertigo_answers_np)) + "% correct")

"""
k = KNeighborsClassifier(p=1)
k.fit(vertigo_train_np_data, vertigo_train_np_class)
vertigo_predict_answers_k = k.predict(vertigo_predict_np[:, :])

total_correct_k = 0
for i in range(len(vertigo_answers_np)):
    if vertigo_answers_np[i] == vertigo_predict_answers_k[i]:
        total_correct_k += 1

print("Another method: " + str(total_correct_k * 100 / len(vertigo_answers_np)) + "% correct")
"""