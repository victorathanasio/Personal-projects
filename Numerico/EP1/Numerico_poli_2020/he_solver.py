#%%
import time


times = time.time()
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from numba import vectorize, njit, stencil
# import cupy as np
import pandas as pd
import os
#%%


global colorscale

colorscale = 'RdYlBu_r'

global renderer_engine
renderer_engine = 'iframe'

global export_format
export_format = 'png'

from Numerico_poli_2020 import Simu
simu = Simu.simu

#%%
def create_dirs():
    global image_path
    image_path = 'Data/' + simu + '/' + metho
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

#%%
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


    def execute_euler(self):
        global metho
        metho = 'Euler'
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
        global metho
        'Implicit euler'
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
        global metho
        metho = 'Crank-Nicolson'
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
        create_dirs()
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
        print(
            'Simu= {}, Metho= {}, l = {}, N = {}, calc_time = {}'.format(
                simu, metho, self.lambd, self.N-1, round(self.time, 4)))

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
#%%
if 'a_old' == simu:
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


#%% conditions for part_a
if 'a' == simu:
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

# %% conditions for part1_b
if 'b' == simu:
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


# %% conditions for part1_c
if 'c' == simu:
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



#%%
from Numerico_poli_2020.EP1_functions import *
