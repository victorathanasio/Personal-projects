
from sympy import *
import pandas as pd
import numpy as np
init_printing(use_unicode=True)

x, y = symbols('x y')

#%%
def check_maximum(f,interval,symbol):
    possiveis_max = []
    borda1 = (f.subs(symbol,interval.args[0]).evalf())
    borda2 = (f.subs(symbol,interval.args[1]).evalf())

    possiveis_max.append(borda1)
    possiveis_max.append(borda2)
    f_ = diff(f)
    zeros = solve(f_)
    for zero in zeros:
        if str(type(zero)) == "<class 'sympy.core.add.Add'>":
            zero = zero.evalf()
        if zero in interval:
            possiveis_max.append(f.subs(symbol,zero).evalf())

    possiveis_sem_complex = []
    for ele in possiveis_max:
        if str(type(ele)) != "<class 'sympy.core.add.Add'>":
            possiveis_sem_complex.append(float(ele))
    return Matrix(possiveis_sem_complex)

def df_from_M(M, func = None, symb = symbols('x')):
    x = symb
    M = transpose(M)
    M = np.array(M).astype(np.float64)
    try:
        df = pd.DataFrame(M, columns=['x', 'f(x)'])
    except:
        df = pd.DataFrame(M, columns=['x'])
        df['f(x)'] = ''
        for i in range(df.shape[0]):
            df.loc[i, 'f(x)'] = Rational(func.subs(x, Rational(df.loc[i, 'x'])))
    return df

class f_newton:
    def __init__(self, ind, xlist, ylist):
        n = len(xlist)
        xlist = [Rational(n) for n in xlist]
        ylist = [Rational(n) for n in ylist]
        self.n = n
        name = 'f['
        for i in range(n):
            name += 'x{},'.format(ind + i)
        name = name[:-1]
        name += ']'
        self.name = name
        self.xlist = xlist
        self.buffer = np.array([ylist,[0 for i in range(len(ylist))]]).transpose()
        self.list_ = xlist
        self.nivel = 0
        self.acha_val()

    def acha_val(self):
        while self.buffer.shape[0] >1:
            self.nivel += 1
            xlist = self.xlist
            buffer = self.buffer
            for i in range(buffer.shape[0]-1):
                buffer[i,1] = (buffer[i+1,0] - buffer[i,0])/(xlist[i+self.nivel]-xlist[i])
            buffer = np.hstack([buffer[:-1,1:],np.zeros(buffer[:-1,1:].shape)])
            self.buffer = buffer
        self.val = self.buffer[0,0]
        return self.val

class interpolador():
    def __init__(self, matrix, func=None,symb = symbols('x')):
        df = df_from_M(matrix, func, symb)
        self.df = df
        self.symb = symb
        min_ = df['x'].min()
        max_ = df['x'].max()
        Inter = Interval(min_,max_)
        self.min_ = min_
        self.max_ = max_
        self.Inter = Inter
        self.func = func

    def lagrange(self):
        df = self.df
        x = self.symb


        df['Li(x)'] = ''
        p = 0
        for i in range(df.shape[0]):
            up = 1
            down = 1
            for j in range(df.shape[0]):
                if i != j:
                    up *= (x-Rational(df.loc[j,'x']))
                    down *= (Rational(df.loc[i,'x'])-Rational(df.loc[j,'x']))
            df.loc[i, 'Li(x)'] = simplify(up/down)
            p += (up/down)*Rational(df.loc[i, 'f(x)'])
            p = simplify(p)
        self.df = df
        self.p_lagr = p

    def newton(self):
        x = symbols('x')
        df =  self.df
        xlist = df['x'].to_list()
        ylist = df['f(x)'].to_list()
        names = ['x','f(x)']
        n = len(xlist)
        arr = np.full((n,n-1), Rational(0))
        arr_ = np.full((n,n+1), Rational(0))
        for j in range(n):
            for i in range(n-j-1):
                if i == 0:
                    names.append(f_newton(i, xlist[i:i+j+2],ylist[i:i+j+1]).name)
                arr[i,j] = Rational(f_newton(i, xlist[i:i+j+2],ylist[i:i+j+2]).acha_val())
        arr_[:,2:] = arr
        arr_[:,0:1] = np.array([xlist]).transpose()
        arr_[:,1:2] = np.array([ylist]).transpose()
        df = pd.DataFrame(arr_, columns=[names])
        p_new = 0
        termo = 1
        for i in range(arr_.shape[1]-1):
            p_new += Rational(arr_[0,i+1])*termo
            termo *= (x - Rational(xlist[i]))
        self.df = df
        self.p_new = simplify(p_new)

    def Erro(self):
        x = symbols('x')
        func = self.func
        df = self.df
        Inter = self.Inter

        if func != None:
            Erro = 1
            n = df.shape[0]
            func___ = func
            for i in range(n):
                try:
                    Erro *= (x-Rational(df.loc[i,'x']))
                except:
                    Erro *= (x-Rational(df.loc[i,'x'].values[0]))
                func___ = diff(func___)
            # Erro = abs(Erro)
            Erro /= Rational(factorial(n+1))
            maxi = max(abs(check_maximum(func___,Inter, x)))
            Erro *= maxi
            Erro = simplify(Erro)/2
            self.Erro = Erro
            return Erro



print('-----------------------------------------------------')
print('Q4')
M = Matrix([
    [0, 1, 2, 3],
])
sube = 1/Rational(6) #Valor que deve ser substituido em X para obter a fração desejada
a = interpolador(M, (Rational(8)/Rational(5))**x)

a.newton()
print()
print('Primeira resposta é a primeira linha do dataframe abaixo.\n', a.df)
print()
print()
print('Fração que é a resposta da questão do meio:')
print()
pprint(a.p_new.subs(x,Rational(sube)))

print()
print()
b = a.Erro()
print('Erro no ponto x = 1/6:           ', abs(b.subs(x, sube))*10)
print('Majoramento do erro no intervalo:', max(abs(check_maximum(b, Interval(M[0], M[-1]), x)))*10 )



