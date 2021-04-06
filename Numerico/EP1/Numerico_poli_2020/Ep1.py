# %% imports
import time

times = time.time()
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from numba import vectorize, njit, stencil
# import cupy as np
import pandas as pd
import os

# %% Globals
global colorscale

colorscale = 'RdYlBu_r'

global renderer_engine
renderer_engine = 'iframe'

global export_format
export_format = 'png'

global simu

global metho

simulations = ['a_old', 'a', 'b', 'c']  # possibilidade = aold, a, b, c pode-se deixar como um input

global methods

methods = ['Euler', 'Crank-Nicolson',
           'Implicit euler']  # ['Euler', 'Implicit euler', 'Crank-Nicolson']  # possibilidades = Euler, Implicit euler, Crank-Nicolson


# %% main
def main():
    global image_path
    image_path = 'Data/' + simu + '/' + metho
    pandas_frame = standard_calculations()
    if metho != 'Euler':
        plot_implict_analysis(pandas_frame)
    else:
        plot_error_evolution(pandas_frame)
        plot_complexity_evolution(pandas_frame)


# %% create_dirs
def create_dirs():
    # checagem de arquivos para depositar os resultados
    if not os.path.exists('Data'):
        os.mkdir('Data')
    if not os.path.exists('Data/' + simu):
        os.mkdir('Data/' + simu)
    if not os.path.exists(image_path):
        os.mkdir(image_path)
    if not os.path.exists(image_path + '/heat_maps'):
        os.mkdir(image_path + '/heat_maps')
    if not os.path.exists(image_path + '/final_state'):
        os.mkdir(image_path + '/final_state')
    if not os.path.exists(image_path + '/analysis'):
        os.mkdir(image_path + '/analysis')
    if not os.path.exists(image_path + '/temporal_series'):
        os.mkdir(image_path + '/temporal_series')
    if hasattr(he_solver, 'exact_sol'):
        if not os.path.exists(image_path + '/hm_erro'):
            os.mkdir(image_path + '/hm_erro')


# %% define he_solver (Heat Equation Solver)
class he_solver():
    def __init__(self, T, lambd, N, X=float(1)):
        self.T = T  # tempo analisado
        self.X = X  # comprimento da barra
        self.N = N  # Discretização em X
        self.lambd = lambd  # resolução
        self.DeltaX = X / N  # DeltaX
        self.N += 1
        self.xspace = np.vstack(np.linspace(X, 0, self.N))  # x space
        if not hasattr(self, 'exact_sol'):
            self.errorval = float(0)  # error when there is no exact sol
        # dict of attributes
        self.M = 0  # discretizacao em Y
        self.DeltaT = np.array(0)  # Delta T
        self.tspace = np.array(0)  # t space
        self.mod = 1  # module for image reduction when ploting
        self.matrix = np.array(0)  # Matrix usada para calcular as respostas
        self.time = 0.0  # tempo para o calculo da matrix
        self.exact_matrix = np.array(0)  # matrix com a resposta exata
        self.exact = np.array(0)  # exact solution in time T
        self.oursol = np.array(0)  # our solution in time T
        self.A = np.array(0)  # vector that represents matrix A
        self.L = np.array(0)  # vector that represents matrix L
        self.D = np.array(0)  # vector that represents the matrix D
        self.errorval = 0  # value of error
        create_dirs()

    def execute_euler(self):
        # inicial conditions for euler's method
        self.M = round(self.T / (self.lambd * (square(self.X / (self.N - 1)))))  # Discretização em T
        self.M += 1
        self.DeltaT = self.T / (self.M - 1)
        self._initialize_matrix_()
        self.mod = self.N  # Fator pelo qual é reduzida a malha da matrix antes da plotagem dos gráficos
        if self.N > 10:
            self.mod *= 2
        # execução do metodo própriamente dito
        self.time = time.time()
        self.matrix = calcula_matrix_euler(self.matrix, self.DeltaX, self.DeltaT)
        self.time = time.time() - self.time
        self._finalize_()  # executes he plotting routine

    def execute_implict_euler(self):
        self.time = time.time()
        self._implicit_()
        self.A = np.zeros((2, self.M - 2), dtype=float)  # vector that represents matrix A
        self.A[0, 0] = 1 + 2 * self.lambd
        self.A[1, 0] = -self.lambd
        self.L = np.zeros(self.M - 3, dtype=float)  # vector that represents matrix L
        self.D = np.zeros(self.M - 2, dtype=float)  # vector that represents the matrix D
        ldl_decomposition(self.A, self.L, self.D)
        self.D = np.vstack(self.D)
        calcula_matrix_implicit_euler(self.L, self.D, self.matrix)
        self.time = time.time() - self.time
        self._finalize_()  # executes he ploting routine

    def execute_crank_nicolson(self):
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
        self._finalize_()  # executes he ploting routine

    def _finalize_(self):
        serialized_tspace, serialized_matrix = matrix_serializer(self.matrix, self.tspace, self.mod)
        if hasattr(self, 'exact_sol'):
            serialized_exact_matrix = exact_sol(serialized_tspace, self.xspace)

            # error_matrix = self.matrix - serialized_exact_matrix
            # self.errorval = np.sum(np.absolute(self.matrix - serialized_exact_matrix)) / (error_matrix.shape[0] * error_matrix.shape[1])
            error_matrix = 0

            # serialized_tspace, serialized_exact_matrix = matrix_serializer(serialized_exact_matrix, self.tspace, self.mod)
            self._plot_(serialized_tspace, serialized_matrix, serialized_exact_matrix)
        else:
            self._plot_(serialized_tspace, serialized_matrix)
        self._plot_serie_temporal_()
        self._plot_final_state_()

    def _initialize_matrix_(self):
        self.tspace = np.linspace(0, self.T, self.M)
        self.matrix = f(self.tspace, self.xspace, self.DeltaX)  # inicia matrix que conterá todos os estados da
        # barra, por conveniencia e manejo de memória, seus valores iniciais correspondem aos valores de f,
        # dessa forma precisamos de uma matriz a menos
        self.f = np.copy(self.matrix[:, 0])
        if metho == 'Crank-Nicolson':
            self.matrix = sum(self.matrix)
            # self.matrix[0] = 2*g2(self.tspace)  # adds the right frontier to the matrix
            # self.matrix[-1] = 2*g1(self.tspace)  # adds the left frontier to the matrix
            # self.matrix[:, 0:1] = u0dex(self.xspace)  # sets the initial conditions on the bar
        self.matrix[0] = g2(self.tspace)  # adds the right frontier to the matrix
        self.matrix[-1] = g1(self.tspace)  # adds the left frontier to the matrix
        self.matrix[:, 0:1] = u0dex(self.xspace)  # sets the initial conditions on the bar
        if metho != 'Euler':
            self.matrix *= self.DeltaT
            self.matrix[1, 1:] += self.matrix[0, 1:] * self.lambd / self.DeltaT
            self.matrix[-2, 1:] += self.matrix[-1,
                                   1:] * self.lambd / self.DeltaT  # transformam os valores F de forma a ser facil o calculo do lado direito do sistema em qualquer instante
            if metho == 'Crank-Nicolson':
                self.matrix /= 2
            self.matrix[0] = g2(self.tspace)  # resets the right frontier to the matrix
            self.matrix[-1] = g1(self.tspace)  # resets the left frontier to the matrix
            self.matrix[:, 0:1] = u0dex(self.xspace)  # resets the initial conditions on the bar
        if metho == 'Euler':
            self.matrix[1:-1, 1:] = self.matrix[1:-1, 0:-1]
            self.matrix[1:-1, 1:2] = np.vstack(self.f[1:-1])

    def _implicit_(self):
        self.DeltaT = self.DeltaX
        self.lambd = round(self.DeltaT / square(self.DeltaX))
        self.M = self.N
        self._initialize_matrix_()

    def _plot_(self, tspace, matrix, exact_matrix=False):
        if hasattr(self, 'exact_sol'):
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=("Nossa solução", "Solução exata"),
                shared_xaxes=True, vertical_spacing=0.05)
            fig.add_trace(go.Heatmap(
                x=tspace,
                y=self.xspace.transpose()[0],
                z=matrix,
                coloraxis="coloraxis",
            ), 1, 1)
            fig.add_trace(go.Heatmap(
                x=tspace,
                y=self.xspace.transpose()[0],
                z=exact_matrix,
                coloraxis="coloraxis",
            ), 2, 1)
            error_matrix = matrix - exact_matrix
            self.errorval = np.sum(np.absolute(error_matrix)) / (error_matrix.shape[0] * error_matrix.shape[1])

            fig.update_layout(
                title="Evol. da temp na barra em função de t, lambda = {}, N = {}<br>Matrix shape: {}; Execution "
                      "time: {} secs;<br>mean_error = {}; Método: {}; simulation = {} ".format(
                    self.lambd, self.N - 1, self.matrix.shape, round(self.time, 3),
                    np.format_float_scientific(self.errorval, 3),
                    metho, simu),
                coloraxis=dict(colorscale=colorscale),
                height=900,
                width=900,
                margin=dict(t=150),
            )
            fig.write_image(image_path + "/heat_maps/l={},N={}.".format(self.lambd, self.N - 1) + export_format)
            fig = go.Figure(go.Heatmap(
                x=tspace,
                y=self.xspace.transpose()[0],
                z=error_matrix,
                coloraxis="coloraxis",
            ))
            fig.update_layout(
                title="Evol. do erro na barra em função de t, lambda = {}, N = {}<br>Matrix shape: {}; Execution "
                      "time: {} secs<br>mean_error = {}; Método = {}; simulation = {} ".format(
                    self.lambd, self.N - 1, self.matrix.shape, round(self.time, 3),
                    np.format_float_scientific(self.errorval, 3),
                    metho, simu),
                coloraxis=dict(colorscale=colorscale),
                height=900,
                width=900
            )
            fig.write_image(image_path + "/hm_erro/hmerro,l={},N={}.".format(self.lambd, self.N - 1) + export_format)

            fig = go.Figure()

            erro_final = error_matrix[:, -1:]
            fig.add_trace(go.Scatter(x=self.xspace.transpose()[0], y=erro_final.transpose()[0], mode='lines',
                                     name='Aproximated solution'))
            fig.update_layout(
                title="Erro da temperatura x posição na barra no instante T, lambda = {}, N ={}  <br>mean_error = {}; Método: {}; simulation = {}".format(
                    self.lambd, self.N - 1, np.format_float_scientific(self.errorval, 3), metho, simu),
                xaxis_title="Posição na barra",
                yaxis_title="Temperatura")
            # fig.show(renderer = renderer_engine)
            fig.write_image(image_path + "/final_state/erro,l={},N={}.".format(self.lambd, self.N - 1) + export_format)


        else:
            fig = go.Figure(go.Heatmap(
                x=tspace,
                y=self.xspace.transpose()[0],
                z=matrix,
                coloraxis="coloraxis",
            ))
            fig.update_layout(
                title="Evol. da temp na barra em função de t, lambda = {}, N = {}<br>Matrix shape: {}; Execution "
                      "time: {} secs;<br>Método: {}; simulation = {} ".format(
                    self.lambd, self.N - 1, self.matrix.shape, round(self.time, 3),
                    metho, simu),
                coloraxis=dict(colorscale=colorscale),
                height=900,
                width=900
            )
            fig.write_image(image_path + "/heat_maps/l={},N={}.".format(self.lambd, self.N - 1) + export_format)

    def _plot_final_state_(self):
        self.oursol = self.matrix[:, -1:]
        if not hasattr(self, 'exact_sol'):
            erro = 0
        else:
            erro = np.format_float_scientific(self.errorval, 3)
        fig = go.Figure()
        if hasattr(self, 'exact_sol'):
            self.exact = exact_sol(self.T, np.linspace(self.X, 0, 600))
            fig.add_trace(
                go.Scatter(x=np.linspace(self.X, 0, 600), y=self.exact,
                           mode='lines',
                           name='Exact solution'))
        fig.add_trace(go.Scatter(x=self.xspace.transpose()[0], y=self.oursol.transpose()[0], mode='lines',
                                 name='Aproximated solution'))
        fig.update_layout(
            title="Temperatura x posição na barra no instante T, lambda = {}, N = {}  <br>mean_error = {}; Método: {}; simulation = {}".format(
                self.lambd, self.N - 1, erro, metho, simu),
            xaxis_title="Posição na barra",
            yaxis_title="Temperatura")
        # fig.show(renderer = renderer_engine)
        fig.write_image(image_path + "/final_state/final,l={},N={}.".format(self.lambd, self.N - 1) + export_format)

    def _plot_serie_temporal_(self):
        t = 0
        fig = go.Figure()
        col = 0
        gap = int(self.M // (self.T / 0.1))

        while t <= self.T:
            if col >= self.matrix.shape[1]:
                col = self.matrix.shape[1] - 1
            fig.add_trace(
                go.Scatter(x=self.xspace.transpose()[0], y=self.matrix[:, col:col + 1].transpose()[0], mode='lines',
                           name='time = {} seconds'.format(round(t, 2))))
            col += gap
            col = int(col)
            t += 0.1
        fig.update_layout(
            title="Evol. da temp na barra em função de t, lambda = {}, N = {}<br>Método: {}, simulation = {}".format(
                self.lambd, self.N - 1, metho, simu),
            xaxis_title="Posição na barra",
            yaxis_title="Temperatura")
        fig.write_image(
            image_path + "/temporal_series/ts,l={},N={}.".format(self.lambd, self.N - 1) + export_format)


# %% standard_calculations
def standard_calculations():
    time1 = time.time()
    new_time = 0
    pandas_frame = pd.DataFrame(columns=['N', 'Lambda', 'Error', 'Time', 'Shape'])
    lambd = [0.25, 0.5, 0.51]
    Ns = [10, 20, 40, 80, 160, 320]
    # inicialize compiler
    a = he_solver(1, 0.5, 10)
    if metho == 'Euler':
        a.execute_euler()
    elif metho == 'Implicit euler':
        a.execute_implict_euler()
    elif metho == 'Crank-Nicolson':
        a.execute_crank_nicolson()

    for n in Ns:
        passei = 0
        for l in lambd:
            if passei == 0 or metho == 'Euler':
                if (n < 90) or (l == 0.25 or l == 0.5):
                    a = he_solver(1, l, n)
                    if metho == 'Euler':
                        a.execute_euler()
                    elif metho == 'Implicit euler':
                        a.execute_implict_euler()
                    elif metho == 'Crank-Nicolson':
                        a.execute_crank_nicolson()
                    pandas_frame = log(a, pandas_frame)
                    if new_time == 0:
                        new_time = time.time() - a.time - 0.9
                        print('initialize time = {}'.format(round(new_time - time1, 4)))
                    print(
                        'Simu= {}, Metho= {}, l = {}, N = {}, time elapsed = {}, calc_time = {}, plot_time = {}'.format(
                            simu, metho, a.lambd, n, round(
                                time.time() - time1, 4), round(a.time, 4),
                            round(time.time() - new_time - a.time, 4)))
                    new_time = time.time()
                    passei += 1
        print()
    pandas_frame.to_csv(image_path + '/DataFrame_' + simu + '_' + metho + '.csv', index=False, header=True)
    # print(pandas_frame)
    return pandas_frame


def log(hesolver, pandas_frame):
    pandas_frame = pandas_frame.append(
        {'N': hesolver.N - 1, 'Lambda': hesolver.lambd, 'Error': float(hesolver.errorval), 'Time': hesolver.time,
         'Shape': hesolver.matrix.shape[0] * hesolver.matrix.shape[1]}, ignore_index=True)
    return pandas_frame


# %% compiled functions
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


# %% plot_implict_analysis
def plot_implict_analysis(pandas_frame):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=pandas_frame['N'].to_list(),
                             y=pandas_frame['Error'].to_list(), mode='lines',
                             name='Erro'))
    fig.update_layout(
        title="Error in function of N, Método: {}; simulation = {}".format(metho, simu),
        xaxis_title="N",
        yaxis_title="Mean_error")
    # fig.show(renderer = renderer_engine)
    fig.write_image(image_path + "/analysis/error(N)." + export_format)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=pandas_frame['N'].to_list(),
                             y=pandas_frame['Time'].to_list(), mode='lines',
                             name='Erro'))
    fig.update_layout(
        title="Time in function of N, Método: {}; simulation = {}".format(metho, simu),
        xaxis_title="N",
        yaxis_title="Time")
    # fig.show(renderer = renderer_engine)
    fig.write_image(image_path + "/analysis/time(N)." + export_format)
    fig.update_layout(
        title="Time in function of N, Método: {}; simulation = {}<br>log scale ".format(metho, simu))
    fig.update_layout(yaxis_type="log", xaxis_type="log")
    fig.write_image(image_path + "/analysis/logtime(N)." + export_format)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=pandas_frame['N'].to_list(),
                             y=pandas_frame['Shape'].to_list(), mode='lines',
                             name='Erro'))
    fig.update_layout(
        title="Number of calculations (matrix size) in function of N, Método: {}; simulation = {}".format(metho,
                                                                                                          simu),
        xaxis_title="N",
        yaxis_title="Calculations (cells in the matrix)")
    # fig.show(renderer = renderer_engine)
    fig.write_image(image_path + "/analysis/Calculations(N)." + export_format)
    fig.update_layout(
        title="Number of calculations (matrix size) in function of N, Método: {}; simulation = {}<br>log scale ".format(
            metho, simu))
    fig.update_layout(yaxis_type="log", xaxis_type="log")
    fig.write_image(image_path + "/analysis/logCalculations(N)." + export_format)


# %% plot_error_evolution

def plot_error_evolution(pandas_frame):
    fig = go.Figure()
    for lambd in [0.25, 0.50]:
        fig.add_trace(go.Scatter(x=pandas_frame[pandas_frame['Lambda'] == lambd]['N'].to_list(),
                                 y=pandas_frame[pandas_frame['Lambda'] == lambd]['Error'].to_list(), mode='lines',
                                 name='Lambda {}'.format(lambd)))
    fig.update_layout(
        title="Error in function of N for each lambda<br>Método: {}; simulation = {}".format(metho, simu),
        xaxis_title="N",
        yaxis_title="Mean_error")
    # fig.show(renderer = renderer_engine)
    fig.write_image(image_path + "/analysis/error(N)." + export_format)
    fig = go.Figure()
    pandas_frame = pandas_frame[pandas_frame['Lambda'] != 0.51]
    for N in [10, 20, 40, 80, 160, 320]:
        fig.add_trace(go.Scatter(x=pandas_frame[pandas_frame['N'] == N]['Lambda'].to_list(),
                                 y=pandas_frame[pandas_frame['N'] == N]['Error'].to_list(), mode='lines',
                                 name='N {}'.format(N)))
    fig.update_layout(
        title="Error in function of lambda for each N<br>Método: {}; simulation = {}".format(metho, simu),
        xaxis_title="Lambda",
        yaxis_title="Mean_error")
    # fig.show(renderer = renderer_engine)
    fig.write_image(image_path + "/analysis/error(lamda)." + export_format)


# %% plot_complexity_evolution
def plot_complexity_evolution(pandas_frame):
    fig = go.Figure()
    for lambd in [0.25, 0.50]:
        fig.add_trace(go.Scatter(x=pandas_frame[pandas_frame['Lambda'] == lambd]['N'].to_list(),
                                 y=pandas_frame[pandas_frame['Lambda'] == lambd]['Shape'].to_list(), mode='lines',
                                 name='Lambda {}'.format(lambd)))
    fig.update_layout(
        title="Number of calculations (matrix size) in function of N for each lambda <br>Método: {}; simulation = {}".format(
            metho, simu),
        xaxis_title="N",
        yaxis_title="Calculations (cells in the matrix)")
    # fig.show(renderer = renderer_engine)
    fig.write_image(image_path + "/analysis/calculations(N)." + export_format)
    fig.update_layout(
        title="Number of calculations (matrix size) in function of N for each lambda <br>log scale ")
    fig.update_layout(yaxis_type="log", xaxis_type="log")
    fig.write_image(image_path + "/analysis/log(calculations)(N)." + export_format)
    fig = go.Figure()
    for lambd in [0.25, 0.50]:
        fig.add_trace(go.Scatter(x=pandas_frame[pandas_frame['Lambda'] == lambd]['N'].to_list(),
                                 y=pandas_frame[pandas_frame['Lambda'] == lambd]['Time'].to_list(), mode='lines',
                                 name='Lambda {}'.format(lambd)))
    fig.update_layout(
        title="Time to calculate matrix in function of N for each lambda<br>Método: {}; simulation = {}".format(
            metho, simu),
        xaxis_title="N",
        yaxis_title="Time (seconds)")
    # fig.show(renderer = renderer_engine)
    fig.write_image(image_path + "/analysis/time(N)." + export_format)
    fig.update_layout(
        title="Time to calculate matrix in function of N for each lambda <br>log scale ")
    fig.update_layout(yaxis_type="log", xaxis_type="log")
    fig.write_image(image_path + "/analysis/logtime(N)." + export_format)


# %% conditions for part1_aold
if 'a_old' in simulations:
    print('a_old')
    simu = 'a_old'


    @vectorize()
    def g1(t):
        return t * 0


    he_solver.g1 = g1


    @vectorize()
    def g2(t):
        return t * 0


    he_solver.g2 = g2


    @vectorize()
    def f(t, x, DeltaX):
        return (10 * square(x) * (x - 1)) - (60 * x * t) + (20 * t)


    he_solver.f = f


    @vectorize()
    def u0dex(x):
        # initial conditions in the bar
        return x * 0


    he_solver.u0dex = u0dex


    @vectorize()
    def exact_sol(t, x):
        return 10 * t * square(x) * (x - 1)


    he_solver.exact_sol = exact_sol
    for metho in methods:
        main()

#%% conditions for part_a
if 'a' in simulations:
    print('a')
    simu = 'a'


    @vectorize()
    def g1(t):
        return t * 0


    he_solver.g1 = g1


    @vectorize()
    def g2(t):
        return t * 0


    he_solver.g2 = g2


    @vectorize()
    def f(t, x, DeltaX):
        return 10 * np.cos(10*t) * square(x) * square(1 - x) - (np.sin(10*t) + 1)*(12*square(x) - 12 * x + 2)


    he_solver.f = f


    @vectorize()
    def u0dex(x):
        # initial conditions in the bar
        return square(x)*square(1-x)


    he_solver.u0dex = u0dex


    @vectorize()
    def exact_sol(t, x):
        return (1 + np.sin(10*t)) * square(x) * square(1-x)


    he_solver.exact_sol = exact_sol
    for metho in methods:
        main()

# %% conditions for part1_b
if 'b' in simulations:
    print('b')
    simu = 'b'


    @vectorize()
    def g1(t):
        return np.exp(t)


    he_solver.g1 = g1


    @vectorize()
    def g2(t):
        return np.exp(t - 1) * np.cos(5 * t)


    he_solver.g2 = g2


    @vectorize()
    def f(t, x, DeltaX):
        return -5 * np.exp(t - x) * ((x + 2 * t) * np.sin(5 * t * x) - 5 * square(t) * np.cos(5 * t * x))


    he_solver.f = f


    @vectorize()
    def u0dex(x):
        # initial conditions in the bar
        return np.exp(-x)


    he_solver.u0dex = u0dex


    @vectorize()
    def exact_sol(t, x):
        return np.exp(t - x) * np.cos(5 * t * x)


    he_solver.exact_sol = exact_sol

    for metho in methods:
        main()
# %% conditions for part1_c
if 'c' in simulations:
    print('c')
    simu = 'c'


    @vectorize()
    def g1(t):
        return t * 0


    he_solver.g1 = g1


    @vectorize()
    def g2(t):
        return t * 0


    he_solver.g2 = g2


    @vectorize()
    def gh(x, DeltaX):
        p = 0.25
        if p - DeltaX / 2 - 0.00000000001 <= x <= p + DeltaX / 2 + 0.00000000001:
            return 1 / DeltaX
        else:
            return 0


    @vectorize()
    def f(t, x, DeltaX):
        return 10000 * (1 - 2*square(t)) * gh(x, DeltaX)


    he_solver.f = f


    @vectorize()
    def u0dex(x):
        # initial conditions in the bar
        return np.exp(-x)


    he_solver.u0dex = u0dex

    if hasattr(he_solver, 'exact_sol'):
        delattr(he_solver, 'exact_sol')

    for metho in methods:
        main()

print('total time = ', time.time() - times)
