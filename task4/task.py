import numpy as np
from math import log2

matrix = np.array([
    [20, 15, 10, 5],
    [30, 20, 15, 10],
    [25, 25, 20, 15],
    [20, 20, 25, 20],
    [15, 15, 30, 25]
])

total_sum = np.sum(matrix)
joint_prob = matrix / total_sum
marginal_prob_X = np.sum(joint_prob, axis=1)
marginal_prob_Y = np.sum(joint_prob, axis=0)

def entropy(prob_matrix):
    H = 0
    for row in prob_matrix:
        for p in row:
            if p > 0:
                H -= p * log2(p)
    return H

H_XY = entropy(joint_prob)
H_X = -np.sum([p * log2(p) for p in marginal_prob_X if p > 0])
H_Y = -np.sum([p * log2(p) for p in marginal_prob_Y if p > 0])

I_XY = H_X + H_Y - H_XY

print(f"Количество информации I(X, Y): {I_XY:.2f}")
print(f"Энтропия совместного события H(XY): {H_XY:.2f}")