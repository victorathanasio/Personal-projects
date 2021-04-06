# %%
from sympy import *
import pandas as pd
import numpy as np

init_printing(use_unicode=True)

# %%
x, y = symbols('x y')


def check_maximum(f, interval, symbol):
    possiveis_max = []
    borda1 = (f.subs(symbol, interval.args[0]).evalf())
    borda2 = (f.subs(symbol, interval.args[1]).evalf())

    possiveis_max.append(borda1)
    possiveis_max.append(borda2)
    f_ = diff(f)
    zeros = solve(f_)
    for zero in zeros:
        if str(type(zero)) == "<class 'sympy.core.add.Add'>":
            zero = zero.evalf()
        if zero in interval:
            possiveis_max.append(f.subs(symbol, zero).evalf())

    possiveis_sem_complex = []
    for ele in possiveis_max:
        if str(type(ele)) != "<class 'sympy.core.add.Add'>":
            possiveis_sem_complex.append(float(ele))
    return Matrix(possiveis_sem_complex)


def df_from_M(M, func=None, symb=symbols('x')):
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


class interpolador():
    def __init__(self, matrix, func=None, symb=symbols('x')):
        df = df_from_M(matrix, func, symb)
        self.df = df
        self.symb = symb
        min_ = df['x'].min()
        max_ = df['x'].max()
        Inter = Interval(min_, max_)
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
                    up *= (x - Rational(df.loc[j, 'x']))
                    down *= (Rational(df.loc[i, 'x']) - Rational(df.loc[j, 'x']))
            df.loc[i, 'Li(x)'] = simplify(up / down)
            p += (up / down) * Rational(df.loc[i, 'f(x)'])
            p = simplify(p)
        self.df = df
        self.p_lagr = p

    def newton(self):
        x = symbols('x')
        df = self.df
        xlist = df['x'].to_list()
        ylist = df['f(x)'].to_list()
        names = ['x', 'f(x)']
        n = len(xlist)
        arr = np.full((n, n - 1), Rational(0))
        arr_ = np.full((n, n + 1), Rational(0))
        for j in range(n):
            for i in range(n - j - 1):
                if i == 0:
                    names.append(f_newton(i, xlist[i:i + j + 2], ylist[i:i + j + 1]).name)
                arr[i, j] = Rational(f_newton(i, xlist[i:i + j + 2], ylist[i:i + j + 2]).acha_val())
        arr_[:, 2:] = arr
        arr_[:, 0:1] = np.array([xlist]).transpose()
        arr_[:, 1:2] = np.array([ylist]).transpose()
        df = pd.DataFrame(arr_, columns=[names])
        p_new = 0
        termo = 1
        for i in range(arr_.shape[1] - 1):
            p_new += Rational(arr_[0, i + 1]) * termo
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
                    Erro *= (x - Rational(df.loc[i, 'x']))
                except:
                    Erro *= (x - Rational(df.loc[i, 'x'].values[0]))
                func___ = diff(func___)
            # Erro = abs(Erro)
            Erro /= Rational(factorial(n + 1))
            maxi = max(abs(check_maximum(func___, Inter, x)))
            Erro *= maxi
            Erro = simplify(Erro) / 2
            self.Erro = Erro
            return Erro


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
        self.buffer = np.array([ylist, [0 for i in range(len(ylist))]]).transpose()
        self.list_ = xlist
        self.nivel = 0
        self.acha_val()

    def acha_val(self):
        while self.buffer.shape[0] > 1:
            self.nivel += 1
            xlist = self.xlist
            buffer = self.buffer
            for i in range(buffer.shape[0] - 1):
                buffer[i, 1] = (buffer[i + 1, 0] - buffer[i, 0]) / (xlist[i + self.nivel] - xlist[i])
            buffer = np.hstack([buffer[:-1, 1:], np.zeros(buffer[:-1, 1:].shape)])
            self.buffer = buffer
        self.val = self.buffer[0, 0]
        return self.val


class romberg:
    def __init__(self, Ts):
        h = symbols('h')
        cols = ['h', 'T(h)', 'S(h)', 'W(h)']
        df = pd.DataFrame(columns=cols)
        df['T(h)'] = Ts
        for i in range(df.shape[0]):
            df.loc[i, 'h'] = h
            h *= 1 / Rational(2)
            if i != df.shape[0] - 1:
                i += 1
                df.loc[i, 'S(h)'] = (4 * df.loc[i, 'T(h)'] - df.loc[i - 1, 'T(h)']) / Rational(3)
                df.loc[i, 'W(h)'] = (16 * df.loc[i, 'S(h)'] - df.loc[i - 1, 'S(h)']) / Rational(15)
        self.df = df


class gauss:
    def __init__(self, grau, Inter, func, symb=symbols('x')):
        x = symb
        t = symbols('t')
        cnj = {
            2: {
                0: 1,
                1: 1
            },
            3: {
                0: 0.5555555555555555555555,
                1: 0.8888888888888888888888,
                2: 0.5555555555555555555555
            },
            4: {
                0: 0.3478548451,
                1: 0.6521451549,
                2: 0.6521451549,
                3: 0.3478548451
            }
        }
        xnj = {
            2: {
                0: 0.5773502692,
                1: -0.5773502692
            },
            3: {
                0: 0.7745966692,
                1: 0,
                2: -0.7745966692
            },
            4: {
                0: 0.8611363116,
                1: 0.3399810436,
                2: -0.3399810436,
                3: -0.8611363116
            }
        }
        n = 0
        while 2 * n - 1 < grau:
            n += 1
        self.n = n
        res = 0
        a = Inter.args[0]
        b = Inter.args[1]
        var = ((b - a) * t + a + b) / 2

        var_ = diff(var, t)
        func = func.subs(x, var)
        for i in range(n):
            res += cnj[n][i] * func.subs(t, xnj[n][i])
        res *= var_
        self.res = res


class euler1l:
    def __init__(self, x0, y0, h, func):
        x, y = symbols('x y')
        xlist = []
        ylist = []
        xlist.append(x0)
        ylist.append(y0)
        for i in range(1, 11):
            ylist.append(ylist[-1] + h * func.subs(x, xlist[-1]).subs(y, ylist[-1]))
            xlist.append(xlist[-1] + h)
        df = pd.DataFrame()
        df['x'] = xlist
        df['y'] = ylist
        self.df = df
        self.xs = xlist
        self.ys = ylist


class eulermod:
    def __init__(self, x0, y0, h, func):
        x, y = symbols('x y')
        xlist = []
        ylist = []
        xlist.append(x0)
        ylist.append(y0)
        for i in range(1, 10):
            ylist.append(ylist[-1] + (h / 2) * (
                        func.subs(x, xlist[-1]).subs(y, ylist[-1]) + func.subs(x, xlist[-1] + h).subs(y, ylist[
                    -1] + h * func.subs(x, xlist[-1]).subs(y, ylist[-1]))))
            xlist.append(xlist[-1] + h)
        df = pd.DataFrame()
        df['x'] = xlist
        df['y'] = ylist
        self.df = df
        self.xs = xlist
        self.ys = ylist


class eulerM:
    def __init__(self, x0, y0, h, coef):
        xlist = []
        ylist = []
        xlist.append(x0)
        ylist.append(y0)
        dlist = []
        for i in range(1, 11):
            dlist.append(ylist[-1] * coef)
            ylist.append(ylist[-1] + h * dlist[-1])
            xlist.append(xlist[-1] + h)
        df = pd.DataFrame()
        df['x'] = xlist
        df['y'] = ylist
        self.df = df
        self.xs = xlist
        self.ys = ylist


# %% Q2
print('-----------------------------------------------------')
print('Q2')
A = [5 / Rational(6), -3 / Rational(2)]
Y0 = [6, -9]
h = 1 / Rational(17)

X0 = [0, 0]
a0 = eulerM(X0[0], Y0[0], h, A[0])
n1 = a0.ys[2]

a1 = eulerM(X0[1], Y0[1], h, A[1])
n2 = a1.ys[2]

print('Resp', n1 + n2)

erros = []

for i in range(2):
    segderi = Y0[i] * A[i] ** 2 * exp(A[i] * x)
    Msegderi = max(abs(check_maximum(segderi, Interval(0, 1), x)))
    L = abs(A[i])
    erro = h * Msegderi / (2 * L) * (exp(L * 1) - 1)
    erros.append(erro.evalf())
print(erros)

# %% Q3
print('-----------------------------------------------------')
print('Q3')

y0 = symbols('y0')
func = y * x ** (-2)
x0 = 1 / Rational(5)
xf = 3 / Rational(10)
yf = -27 / Rational(8)
h = (xf - x0) / 2

a = euler1l(x0, y0, h, func)
y0_ = solve(a.df.loc[2, 'y'] - yf)[0]
print(y0_)
a = eulermod(x0, y0_, h, func)
print(a.df.loc[2, 'y'])

# %% Q4
print('-----------------------------------------------------')
print('Q4')
a = symbols('a')
M = Matrix([
    [-2, -1, 0, 1],
])
sube = 1 / Rational(2)
x = symbols('x')
a = interpolador(M, (Rational(3) / Rational(2)) ** x)

a.newton()
print('Primeira linha df\n', a.df)

print('Fracao', a.p_new.subs(x, Rational(sube)))

print('Debaixo', max(abs(check_maximum(a.Erro(), Interval(M[0], M[-1]), x))) * 10)

# %% Q5
print('-----------------------------------------------------')
print('Q5')

x = symbols('x')
func = Rational(1) / (Rational(16) / Rational(7) * x + Rational(6) / Rational(5))
Inter = Interval(8 / 3, 49 / 18)
func__ = func
pprint(func)
for i in range(3):
    func__ = diff(func__)
check_maximum(func__, Inter, x) / (factorial(3))

# %% Q6
print('-----------------------------------------------------')
print('Q6')
h, fa, fb, fx1, fx2, fx3 = symbols('h fa fb fx1, fx2, fx3')

resps = [Rational(5) / 2, Rational(5) / 3, Rational(493) / 336]
a = 1 / Rational(2)

Eq1e = (fa + fb) * h
Eq1d = 2 * a * resps[0]

Eq2e = h * (fa + fb) + h * 2 * fx2
Eq2d = 4 * a * resps[1]

Eq3e = h * (fa + fb) + h * (+ 2 * fx1 + 2 * fx2 + 2 * fx3)
Eq3d = 8 * a * resps[2]

Eq3e *= 2
Eq3d *= 2

Eq3e += - Eq2e
Eq3d += - Eq2d

Eq3e *= 1 / Rational(6)
Eq3d *= 1 / Rational(6)

Eq3e = simplify(Eq3e)
pprint(Eq3d)
a = romberg(resps)
a.df

# %%Q7
print('-----------------------------------------------------')
print('Q7')
x = symbols('x')
Inter = Interval(-3, 7)
M = Matrix([
    [-3, 2, 7],
    [2 / 5, -2, 4 / 9]
])

b = interpolador(M)
b.lagrange()
func = b.p_lagr
grau = 2

a = gauss(grau, Inter, func)
print(a.res)
t = symbols('t')
a = Inter.args[0]
b = Inter.args[1]
var = (2 * x - a - b) / (b - a)
var_ = diff(var, t)
Legendre = t ** 3 - (3 / 5) * t
print(solve(Legendre.subs(t, var)))
