from Numerico_poli_2020 import Simu
Simu.simu = 'a' # opções = a_old, a, b, c

from Numerico_poli_2020 import he_solver

#%%
a = he_solver.he_solver(1, 0.5, 3) # Parametros são T, lambda, N
a.execute_euler() # opções = execute_implict_euler, execute_crank_nicolson e execute_euler
# he_solver parameters are (T,lambda,N), be aware that if you are going to execute implicit methods, your lambda will be over writen