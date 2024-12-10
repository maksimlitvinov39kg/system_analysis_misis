import json
import numpy as np

def generate_rankings(structure):
    rankings = {}
    for idx, item in enumerate(structure):
        if isinstance(item, list):
            for elem in item:
                rankings[elem] = idx
        else:
            rankings[item] = idx
    return rankings

def create_matrix(rankings):
    matrix_size = len(rankings)
    matrix = []
    for i in range(1, matrix_size + 1):
        row = [1 if rankings[key] >= rankings[i] else 0 for key in rankings]
        matrix.append(row)
    return matrix

def calculate_kernel(matrix_a, matrix_b):
    matrix_a, matrix_b = np.array(matrix_a), np.array(matrix_b)
    product_ab = matrix_a * matrix_b
    product_ab_transpose = matrix_a.T * matrix_b.T
    kernel_matrix = np.logical_or(product_ab, product_ab_transpose)
    return kernel_matrix

def main(input_a, input_b):
    rankings_a = generate_rankings(input_a)
    rankings_b = generate_rankings(input_b)

    matrix_a = create_matrix(rankings_a)
    matrix_b = create_matrix(rankings_b)

    kernel = calculate_kernel(matrix_a, matrix_b)
    print(kernel)


data_a = [1, [2, 3], 4, [5, 6, 7], 8, 9, 10]
data_b = [[1, 2], [3, 4, 5], 6, 7, 9, [8, 10]]

main(data_a, data_b)
