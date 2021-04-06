#%%
import time
global simu
times = time.time()
import numpy as np
from numba import njit, stencil
# import cupy as np
from Numerico_poli_2020 import Simu

global simu
simu = Simu.simu


#%%
@njit(parallel=True)
def calcula_matrix_euler(matrix, DeltaX, DeltaT):
    # matrix[1:-1, 1] = matrix[1:-1, 0] + DeltaT * (
    #             (matrix[0:-2, 0] - 2 * matrix[1:-1, 0] + matrix[2:, 0]) / square(DeltaX) + fvector[1:-1])
    for i in range(matrix.shape[1] - 1):
        matrix[1:-1, i + 1:i + 2] = calcula_column_euler(matrix[:, i:i + 2], DeltaX, DeltaT)
    return matrix


@stencil
def _calcula_column_euler(x, DeltaX, DeltaT):
    # print(columns)
    return x[0, -1] + DeltaT * (
            (x[-1, -1] - 2 * x[0, -1] + x[1, -1]) / (DeltaX * DeltaX) + x[0, 0])
    # Snd[i][0] = Fst[i][0] + DeltaT * ((Fst[i - 1][0] - 2 * Fst[i][0] + Fst[i + 1][0]) / square(DeltaX) + fvector[i])


@njit(parallel=True)
def calcula_column_euler(columns, DeltaX, DeltaT):
    return _calcula_column_euler(columns, DeltaX, DeltaT, out=columns)[1:-1, 1:2]


# @njit()
# def calcula_column_euler(matrix, DeltaX, DeltaT):
#     return matrix[1:-1, 0:1] + DeltaT * (
#                 (matrix[0:-2, 0:1] - 2 * matrix[1:-1, 0:1] + matrix[2:, 0:1]) / square(DeltaX) + matrix[1:-1, 0:1])


@stencil()
def _sum(x):
    return x[0, -1] + x[0, 0]


@njit(parallel=True)
def sum(x):
    return _sum(x)


@njit()
def matrix_serializer(matrix, tspace, mod):
    final_matrix = matrix[:, 0:1]
    final_tspace = tspace[0:1]
    for i in range(mod, len(tspace), mod):
        final_tspace = np.concatenate((final_tspace, tspace[i:i + 1]))
        final_matrix = np.column_stack((final_matrix, matrix[:, i:i + 1]))
    return final_tspace, final_matrix


@njit()
def square(x):
    return x ** 2


@njit()
def ldl_decomposition(A, L, D):
    # A 2 vectors, fst represents the diagonal, the second, de subdiagonal (Nx2)
    # L empty array that will represent the subdiagonal of matrix L (N-1x2)
    # D empty array that will represent the diagonal of matrix D
    n = A[0].shape[0]
    A = (A[0, 0], A[1, 0])
    for i in range(n):
        D[i] = A[0] - square(L[i - 1]) * D[i - 1]
        if not i + 1 == n:
            L[i] = A[1] / D[i]


@njit(parallel=True)
def forward_solution(L, f):
    # returns X
    for i in range(1, f.shape[0]):
        f[i] = f[i] - L[i - 1] * f[i - 1]


@njit(parallel=True)
def diagonal_solution(D, x):
    # return Y
    return x / D


@njit(parallel=True)
def backward_solution(L, y):
    for i in range(-2, -y.shape[0] - 1, -1):
        # returns U
        y[i] -= L[i + 1] * y[i + 1]


@njit()
def solve_ldl(L, D, put):
    # put is the right side of the system, and for memory allocation reasons, is also the output
    forward_solution(L, put)
    put = diagonal_solution(D, put)
    backward_solution(L, put)
    return put


@njit(parallel=True)
def calcula_matrix_implicit_euler(L, D, Matrix):
    for i in range(Matrix.shape[1] - 1):
        Matrix[1:-1, i + 1:i + 2] = solve_ldl(L, D, Matrix[1:-1, i:i + 1] + Matrix[1:-1, i + 1:i + 2])


@njit(parallel=True)
def calcula_matrix_implicit_nicolson(L, D, Matrix, lambd):
    for i in range(Matrix.shape[1] - 1):
        Matrix[1:-1, i + 1:i + 2] = solve_ldl(L, D, calcula_right_side_nicolson(Matrix[:, i:i + 2], lambd))


@njit(parallel=True)
def calcula_right_side_nicolson(columns, lambd):
    return _calcula_right_side_nicolson(columns, lambd)[1:-1, 1:]


@stencil()
def _calcula_right_side_nicolson(x, lambd):
    return x[0, 0] + ((lambd / 2) * x[-1, -1]) + ((lambd / 2) * x[1, -1]) + ((1 - lambd) * x[0, -1])
