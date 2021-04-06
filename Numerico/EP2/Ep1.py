#Lui Damianci Ferreira - 10770579
#Victor A. C. Athanasio - 9784401
# %% imports
import time
import numpy as np
from numba import vectorize, njit, stencil
#Este arquivo contém os métodos importados do EP1

# %% define he_solver (Heat Equation Solver)
class crank_nicolson:
    ''''Classe que resolve o problema de distribuicao de calor atraves do método de cranck nicolson'''
    def __init__(self, N, P, T=1, X=float(1)):
        self.P = P #Ponto
        self.T = T  # tempo analisado
        self.X = X  # comprimento da barra
        self.N = N  # Discretização em X
        self.DeltaX = X / N  # DeltaX
        self.N += 1
        self.xspace = np.vstack(np.linspace(X, 0, self.N))  # x space
        self.M = 0  # discretizacao em Y
        self.DeltaT = np.array(0)  # Delta T
        self.tspace = np.array(0)  # t space
        self.mod = 1  # module for image reduction when ploting
        self.matrix = np.array(0)  # Matrix usada para calcular as respostas
        self.time = 0.0  # tempo para o calculo da matrix
        self.u = np.array(0)  # our solution in time T
        self.A = np.array(0)  # vector that represents matrix A
        self.L = np.array(0)  # vector that represents matrix L
        self.D = np.array(0)  # vector that represents the matrix D

    def execute(self):
        self.time = time.time()
        self._implicit_()
        self.A = np.zeros((2, self.M - 2), dtype=float)  # vector that represents matrix A
        self.A[0, 0] = 1 + self.lambd
        self.A[1, 0] = -self.lambd / 2
        self.L = np.zeros(self.M - 3, dtype=float)  # vector that represents matrix L
        self.D = np.zeros(self.M - 2, dtype=float)  # vector that represents the matrix D
        ldl_decomposition(self.A, self.L, self.D)
        self.D = np.vstack(self.D)
        calcula_matrix_implicit_nicolson(self.L, self.D, self.matrix, self.lambd)
        self.time = time.time() - self.time
        self.u = np.flip(self.matrix[:, -1:])
        return self.u

    def _initialize_matrix_(self):
        self.tspace = np.linspace(0, self.T, self.M)
        self.matrix = f(self.tspace, self.xspace, self.DeltaX, self.P)  # inicia matrix que conterá todos os estados da
        # barra, por conveniencia e manejo de memória, seus valores iniciais correspondem aos valores de f,
        # dessa forma precisamos de uma matriz a menos
        self.f = np.copy(self.matrix[:, 0])
        self.matrix = sum(self.matrix)
        self.matrix[0] = g2(self.tspace)  # adds the right frontier to the matrix
        self.matrix[-1] = g1(self.tspace)  # adds the left frontier to the matrix
        self.matrix[:, 0:1] = u0dex(self.xspace)  # sets the initial conditions on the bar
        self.matrix *= self.DeltaT
        self.matrix[1, 1:] += self.matrix[0, 1:] * self.lambd / self.DeltaT
        self.matrix[-2, 1:] += self.matrix[-1,
                               1:] * self.lambd / self.DeltaT  # transformam os valores F de forma a ser facil o calculo do lado direito do sistema em qualquer instante
        self.matrix /= 2
        self.matrix[0] = g2(self.tspace)  # resets the right frontier to the matrix
        self.matrix[-1] = g1(self.tspace)  # resets the left frontier to the matrix
        self.matrix[:, 0:1] = u0dex(self.xspace)  # resets the initial conditions on the bar

    def _implicit_(self):
        self.DeltaT = self.DeltaX
        self.lambd = round(self.DeltaT / square(self.DeltaX))
        self.M = self.N
        self._initialize_matrix_()


@stencil()
def _sum(x):
    return x[0, -1] + x[0, 0]


@njit(parallel=True)
def sum(x):
    return _sum(x)


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
def calcula_matrix_implicit_nicolson(L, D, Matrix, lambd):
    for i in range(Matrix.shape[1] - 1):
        Matrix[1:-1, i + 1:i + 2] = solve_ldl(L, D, calcula_right_side_nicolson(Matrix[:, i:i + 2], lambd))


@njit(parallel=True)
def calcula_right_side_nicolson(columns, lambd):
    return _calcula_right_side_nicolson(columns, lambd)[1:-1, 1:]


@stencil()
def _calcula_right_side_nicolson(x, lambd):
    return x[0, 0] + ((lambd / 2) * x[-1, -1]) + ((lambd / 2) * x[1, -1]) + ((1 - lambd) * x[0, -1])

#%% Bordas
@vectorize()
def g1(t):
    return t * 0


crank_nicolson.g1 = g1


@vectorize()
def g2(t):
    return t * 0


crank_nicolson.g2 = g2


@vectorize()
def gh(x, DeltaX, p):
    if p - DeltaX / 2 - 0.00000000001 <= x <= p + DeltaX / 2 + 0.00000000001:
        return 1 / DeltaX
    else:
        return 0


@vectorize()
def f(t, x, DeltaX, P):
    return 10*(1 + np.cos(5*t)) * gh(x, DeltaX, P)


crank_nicolson.f = f


@vectorize()
def u0dex(x):
    # initial conditions in the bar
    return x * 0


crank_nicolson.u0dex = u0dex


