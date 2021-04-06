#%% imports

import numpy as np
from sympy import *
from sympy.calculus.util import continuous_domain
import pandas as pd
import copy


init_printing(use_unicode=True)

#%%funcoes

class Ponto:
    def __init__(self,x, fx, tipo):
        self.x = x
        self.fx = fx
        self.tipo = tipo

    def __lt__(self, other):
        return self.x < other.x

def acha_intervalo_newton(f, symbol):
    f_ = diff(f)
    f__ = diff(f_)
    _inf = limit(f,symbol,-oo).evalf()
    Pontos = []
    Pontos.append(Ponto(-oo, _inf,'- infinito: '))
    inf_mais = limit(f,symbol,+oo).evalf()
    Pontos.append(Ponto(oo, inf_mais,'+ infinito: '))

    f_zeros = solve(f_)

    for zero in f_zeros:
        if str(type(zero)) != "<class 'sympy.core.add.Add'>":
            fvalue = f.subs(symbol, zero.evalf())
            if fvalue < 0:
                Pontos.append(Ponto(zero.evalf(), fvalue,'minimo local: '))
            else:
                Pontos.append(Ponto(zero.evalf(), fvalue,'maximo local: '))

    f__zeros = solve(f__)
    for zero in f__zeros:
        if str(type(zero)) != "<class 'sympy.core.add.Add'>":
            fvalue = f.subs(symbol, zero.evalf())
            Pontos.append(Ponto(zero.evalf(), fvalue, 'mudanca concav: '))
    df = pd.DataFrame(columns=['Tipo','x','f(x)'])
    Pontos.sort()
    for i, ponto in enumerate(Pontos):
        df.loc[i, 'x'] = ponto.x
        df.loc[i, 'f(x)'] = ponto.fx
        df.loc[i, 'Tipo'] = ponto.tipo

    return df

def visual_check(f,interval,symbol):
    plot(f, (symbol, interval.args[0], interval.args[1]))
    inp = input('Vazio para confirmar')
    if inp == '':
        return True
    else:
        return False

def check_continuity(f, interval, symbol, visual=False):
    cont_domain = continuous_domain(f,symbol,interval)
    if visual:
        check = visual_check(f,interval,symbol)
        if not check:
            raise NameError('Aborted at visual check')
    if len(cont_domain.args) == 1:
        return True
    elif type(cont_domain) == type(Interval(0,1)):
        return True
    else:
        return False

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
    return possiveis_sem_complex

def check_bolz(f, intervalo, symbol):
    t0 = float(intervalo.args[0])
    t1 = float(intervalo.args[1])
    boz = f.subs(symbol,t0)*f.subs(symbol,t1) < 0
    return boz

def check_monotonia(f, intervalo, symbol):
    f_ = diff(f)
    maximos = check_maximum(f_,intervalo, symbol)
    f_max = np.max(maximos)
    f_mim = np.min(maximos)
    if f_max * f_mim > 0:
        if f_max > 0:
            return True, 1
        else:
            return True, -1
    else:
        return False, False

def muda_concav(f,intervalo):
    f_ = diff(f)
    f__ = diff(f_)
    sols = solve(f__)
    for sol in sols:
        if sol in intervalo:
            return False
    return True

def acha_intervalo_aprx_suc(phi):
    ''' Da uma dica pra achar o intervalo'''
    phi_ = diff(phi)
    sol1 = solve(phi_)
    sol0 = solve(phi_ + 1)
    sol2 = solve(phi_ - 1)

    if len(sol1) != len(sol0) or len(sol0) != len(sol2):
        print(sol0)
        print(sol1)
        print(sol2)
    else:
        for i in range(len(sol0)):
            print(sol0[i].evalf(), '|', sol1[i].evalf(), '|', sol2[i].evalf())

def check_intervalo_aprx_suc(f,phi, symbol, intervalo):
    '''Verifica se o intervalo serve'''
    t0 = float(intervalo.args[0])
    t1 = float(intervalo.args[1])
    fcond = f.subs(symbol,t0)*f.subs(symbol,t1) < 0
    phi_ = abs(diff(phi))
    phi_cond = phi_.subs(symbol,t0) < 1 and phi_.subs(symbol,t1) < 1
    if not phi_cond:
        print('Intervalo invalido, modulo de phi_ nao eh menor que 1')
    if not fcond:
        print('raizes tao do msm lado, cade bolzano???')
    if fcond and phi_cond:
        print('Intervalo valido')
    return fcond and phi_cond

class aproximacoes_sucessivas:
    ''''Classe para executar todas as variacoes de aproximacoes sucessivas'''
    def __init__(self,f, phi,intervalo, erro, symbol, visual = False):
        self.erro = erro
        self.phi = phi
        self.phi_ = diff(phi)
        self.intervalo = intervalo
        self.symbol = symbol
        self.visual = visual
        self.f = f

        inter_check = check_intervalo_aprx_suc(f, phi, symbol, intervalo)
        if not inter_check:
            print('intervalo incorreto')

        condicoes_basicas = self.__verifica_condicoes()
        if not condicoes_basicas:
            print('condicoes basicas nao são suficientes pelo(s) motivo(s) acima')

        convergente_em_phi = self.__converg_phi()
        if not convergente_em_phi:
            print('Não podemos garantir convergencia em phi, pelo(s) motivo(s) acima')

        self.x0 = self.__escolhe_x0()
        self.iters = 100
        self.df = pd.DataFrame()

#################################################################################################
#metodo monotonic
    def exec_monotonic(self):
        print()
        print('Exececutando monotonic')
        phi = self.phi
        intervalo = self.intervalo
        symbol = self.symbol
        mono = check_monotonia(phi,intervalo,symbol)
        if mono[1] < 0:
            print('Metodo invalido, sequencia nao monotonica')
            return
        column1, column2 = self.monotonic_type()

        self.df[column1] = np.nan
        self.df[column2] = np.nan
        self.df.loc[0, column2] = self.meio_intervalo
        self.resps = [self.x0]
        self.iters_ = 0
        self.iters = 100
        self.__recursi(column1,column2,'monotonic_criteria')

    def monotonic_criteria(self):
        if np.abs(self.resps[-1] - self.resps[-2]) < 2*self.erro:
            return True

    def monotonic_type(self):
        symbol = self.symbol
        phi = self.phi
        resps = self.resps
        resp = float(phi.subs(symbol , resps[-1]))
        resps.append(resp)
        self.sinal = (resps[-1]-resps[-2])
        self.sinal = self.sinal/abs(self.sinal)
        if self.sinal > 0:
            print('monotonica crescente')
            return 'Xn_Mono_cres', 'Erro_Xn_Mono_cres'
        else:
            print('monotonica decrescente')
            return 'Xn_Mono_decres', 'Erro_Xn_Mono_decres'


#################################################################################################
#metodo alternado
    def exec_alternado(self):
        print()
        print('Exececutando alternado')
        phi = self.phi
        intervalo = self.intervalo
        symbol = self.symbol
        mono = check_monotonia(phi,intervalo,symbol)
        if mono[1] > 0:
            print('Método invalido, sequencia nao alternada')
            return False
        if not self.M/(1-self.M) > 1:
            print('parada invalida, M/(1-M) < 1')
            return False
        column1, column2 = 'Xn_Alternado', 'Erro_Xn_Alternado'
        self.df[column1] = np.nan
        self.df[column2] = np.nan
        self.df.loc[0, column2] = self.meio_intervalo
        self.resps = [self.x0]
        self.iters_ = 0
        self.iters = 100
        self.__recursi(column1, column2, 'alternado_criteria')

    def alternado_criteria(self):
        if np.abs(self.resps[-1] - self.resps[-2]) < self.erro:
            return True
        else:
            return False

#################################################################################################
#metodo parada (I)
    def exec_parada_I(self):
        print()
        print('Exececutando parada I')
        if self.M >=1:
            print('Metodo invalido, M = {} > 1'.format(self.M))
            return
        if not self.M/(1-self.M) < 1:
            print('metodo invalido, M/(1-M) > 1')
            return
        column1, column2 = 'Xn_Parada_I', 'Erro_Xn_Parada_I'
        self.df[column1] = np.nan
        self.df[column2] = np.nan
        self.df.loc[0, column2] = self.meio_intervalo
        self.resps = [self.x0]
        self.iters_ = 0
        self.iters = 100
        self.__recursi(column1, column2, 'parada_I_criteria')

    def parada_I_criteria(self):
        M = self.M
        if (M/(1-M))*np.abs(self.resps[-1] - self.resps[-2]) < self.erro:
            return True

#################################################################################################
#metodo padrao
    def exec_padrao(self):
        print()
        print('Exececutando padrao')
        n = self.numero_de_passos()
        column1, column2 = 'Xn_Padrao', 'Erro_Xn_Padrao'
        self.df[column1] = np.nan
        self.df[column2] = np.nan
        self.df.loc[0, column2] = self.meio_intervalo
        self.resps = [self.x0]
        self.iters_ = 0
        self.iters = n
        print('Serao , ', n, ' iteracoes')
        self.__recursi(column1, column2, 'padrao_criteria')


    def padrao_criteria(self):
        if self.iters <= 0:
            return True


    def numero_de_passos(self):
        c = float(self.meio_intervalo)
        M = float(self.M)
        erro = self.erro
        n = np.ceil(np.log(erro/c)/np.log(M))
        return n


################################################################################################
#funcs auxiliares
    def __escolhe_x0(self):
        intervalo = self.intervalo
        symbol = self.symbol
        phi = self.phi

        a = intervalo.args[0]
        b = intervalo.args[1]
        c = float((a+b)/2)
        phi_de_c = float(phi.subs(symbol, c))
        if phi_de_c < c:
            x0 = a
        if phi_de_c > c:
            x0 = b
        if phi_de_c == c:
            x0 = c
        self.meio_intervalo = (b-a)/2
        return float(x0)

    def __verifica_condicoes(self):
        phi = self.phi
        f = self.f
        symbol = self.symbol
        intervalo = self.intervalo

        phicontinua = check_continuity(phi, intervalo, symbol, self.visual)
        fcontinua = check_continuity(f, intervalo, symbol, self.visual)
        fmonotonica = check_monotonia(f, intervalo, symbol)[0]
        fbolz = check_bolz(f, intervalo, symbol)

        if not phicontinua:
            print('Phi não continua no intervalo')
        if not fcontinua:
            print('f não continua no intervalo')
        if not fmonotonica:
            print('f não monotonica no intervalo')
        if not fbolz:
            print('f não satifaz bolzano')
        return phicontinua and fcontinua and fmonotonica and fbolz


    def __converg_phi(self):
        intervalo = self.intervalo
        symbol = self.symbol
        phi = self.phi
        phi_ = self.phi_
        visual = self.visual
        phicontinua = check_continuity(phi,intervalo,symbol,visual)
        phi_continua = check_continuity(phi_,intervalo,symbol,visual)
        phi_max = np.max(np.abs(np.array(check_maximum(phi_,intervalo,symbol))))
        phiarr = np.array(check_maximum(phi,intervalo,symbol))
        phimax = np.max(phiarr)
        phimim = np.min(phiarr)
        self.M = float(phi_max)
        phimax_intervalo = True
        phimin_intervalo = True
        phi_maxmod = True
        if not phicontinua:
            print('Phi não é continua no intervalo')
        if not phi_continua:
            print("Phi' não é continua no intervalo")
        if phimax >= intervalo.args[1]:
            phimax_intervalo = False
            print('Nao podemos garantir que Xn+1 estara no intervalo Phimax <= Intmax'
                  ' = {:.2f} < {:.2f}'.format(float(phimax),float(intervalo.args[1])))
        if phimim <= intervalo.args[0]:
            phimin_intervalo = False
            print('Nao podemos garantir que Xn+1 estara no intervalo Phimin'
                  ' <= Intmin = {:.2f} < {:.2f}'.format(float(phimim),float(intervalo.args[0])))
        if phi_max >= 1:
            phi_maxmod = False
            print('Nao podemos mostrar que Phi é uma n-contração, |Phi_| = {} >= 1'.format(phi_max))
        return phicontinua and phi_continua and phimax_intervalo and phimin_intervalo and phi_maxmod

    def exec(self):
        self.exec_padrao()#tanto faz
        self.exec_alternado()
        self.exec_parada_I()
        self.exec_monotonic()#xn+1


    def __calc_erro(self, column):
        M = self.M
        if column == 'Erro_Xn_Padrao':
            return np.abs(self.resps[-2]-self.resps[-1])*(M/(1-M))
        if column == 'Erro_Xn_Alternado':
            return np.abs(self.resps[-2]-self.resps[-1])
        if column == 'Erro_Xn_Parada_I':
            return (M/(1-M))*np.abs(self.resps[-1] - self.resps[-2])
        if column == 'Erro_Xn_Mono_cres' or column == 'Erro_Xn_Mono_decres':
            return np.abs(self.resps[-1] - self.resps[-2])

    def __recursi(self, column1, columns2, stop_criteria):
        symbol = self.symbol
        phi = self.phi
        resps = self.resps
        resp = float(phi.subs(symbol , resps[-1]))
        resps.append(resp)

        self.df.loc[self.iters_ , column1] = resps[-2]
        self.iters_ += 1
        self.df.loc[self.iters_ , column1] = resp
        self.df.loc[self.iters_ , columns2] = self.__calc_erro(columns2)
        self.iters -= 1
        validation = getattr(self, stop_criteria)
        result = validation()
        if result:
            print('Metodo '+ column1 + ' achou')
            print()
            if stop_criteria == 'monotonic_criteria':
                self.df.loc[self.iters_ , column1] = np.nan
                self.df.loc[self.iters_ , columns2] = np.nan
            return True
        elif self.iters == 0:
            print('esgotou iteracoes')
            print()
            return False
        else:
            self.__recursi(column1, columns2, stop_criteria)

class Newton:
    def __init__(self,f, symbol, intervalo, erro, visual = False):
        self.f = f
        f_ = diff(f)
        self.f_ = f_
        f__ = diff(f_)
        self.f__ = f__
        self.erro = erro
        self.visual = visual
        self.phi = symbol - f/(diff(f))
        self.phi_ = diff(self.phi)
        self.intervalo = intervalo
        self.symbol = symbol

        inter_check = self.__verifica_intervalo()
        if not inter_check:
            print('Intervalo contem irregularidades')

        self.x0 = self.__escolhex0()
        self.df = pd.DataFrame()


    def __verifica_intervalo(self):
        f = self.f
        intervalo = self.intervalo
        symbol = self.symbol

        bolz = check_bolz(f, intervalo, symbol)
        mono = check_monotonia(f, intervalo, symbol)[0]
        concav = muda_concav(f,intervalo)
        fcont = check_continuity(f,intervalo,symbol,self.visual)

        if not bolz:
            print('intervalo nao satisfaz bolzano')

        if not mono:
            print('Intervalo invalido, f nao e monotonica')

        if not concav:
            print('Intervalo invalido, f muda concavidade')

        if not fcont:
            print('Intervalo invalido, f n eh continua')


        return bolz and mono and concav and fcont

    def __escolhex0(self):
        f__ = self.f__
        f_ = self.f_
        symbol = self.symbol
        intervalo = self.intervalo
        a = intervalo.args[0]
        b = intervalo.args[1]
        c = (a+b)/2
        sinalf_ = f_.subs(symbol, c).evalf()
        sinalf__ = f__.subs(symbol, c).evalf()
        self.meio_intervalo = (b-a)/2

        if sinalf__*sinalf_ > 0:
            x0 = b
        if sinalf__*sinalf_ < 0:
            x0 = a
        return x0

    def __tipo_conv(self):
        phi = self.phi
        symbol = self.symbol
        phi_list = [self.x0, phi.subs(symbol,self.x0)]
        phi_list.append(phi.subs(symbol,phi_list[-1]))
        sinal1 = phi_list[1] - phi_list[0]
        sinal2 = phi_list[2] - phi_list[1]

        if sinal1*sinal2 > 0:
            self.tipo = 'monotonica'
            self.mono_tipo = self.__check_cres()
        else:
            print('Phi eh  oscilante')
            self.tipo = 'oscilante'
    #     phi = self.phi
    #     intervalo = self.intervalo
    #     symbol = self.symbol
    #
    #     mono = check_monotonia(phi, intervalo, symbol)
    #     if not mono[0]:
    #         print('phi_ troca de sinal no intervalo, n eh possivel determinar '
    #               'se a sequencia sera monotonica ou alternante')
    #         print()
    #         print('Fazendo que nem o prof, assumindo monotonica e andando com 2Erro')
    #         self.__estado_pelo_ponto()
    #
    #     elif mono[0]:
    #         if mono[1] > 0:
    #
    #         if mono[1] < 0:
    #
    #
    # def __estado_pelo_ponto(self):
    #     # phi_ = self.phi_
    #     # a = phi_.subs(self.symbol, self.x0).evalf()
    #     # if a > 0:
    #     self.tipo = 'monotonica'
    #     self.mono_tipo = self.__check_cres()
    #     # elif a < 0:
    #     #     print('Phi eh  oscilante')
    #     #     self.tipo = 'oscilante'


    def __check_cres(self):
        symbol = self.symbol
        phi = self.phi
        resps = [self.x0]
        resp = float(phi.subs(symbol , resps[-1]))
        resps.append(resp)
        self.sinal = (resps[-1]-resps[-2])
        self.sinal = self.sinal/abs(self.sinal)
        if self.sinal > 0:
            print('Phi eh monotonica crescente')
            return 'crescente'
        else:
            print('Phi eh monotonica decrescente')
            return 'decrescente'

    def exec(self):
        print()
        print('Exececutando Euler')
        self.sinal = 0

        self.__tipo_conv()
        self.df['Erro'] = np.nan
        self.df.loc[0,'Erro'] = self.meio_intervalo
        self.df['Xn'] = np.nan
        if self.tipo == 'oscilante':
            column2 = 'phi(Xn)'
            self.df.loc[0, 'Erro'] = self.meio_intervalo
        else:

            if self.mono_tipo == 'crescente':
                self.df['Xn + 2E'] = np.nan
                self.df['f(Xn + 2E)'] = np.nan
                column2 = 'phi(Xn+2E)'
            else:
                self.df['f(Xn - 2E)'] = np.nan
                column2 = 'phi(Xn-2E)'


        self.df[column2] = np.nan
        self.resps = [self.x0]
        self.iters_ = 0
        self.iters = 100
        self.__recursi(column2)
        self.__finalize()

    def __finalize(self):
        resps = self.resps
        if self.tipo == 'oscilante':
            _x_ = (resps[-1] + resps[-2])/2
            print('xbarra = {}'.format(_x_))
        elif self.mono_tipo == 'crescente':
            _x_ = (resps[-2] + self.erro)
            print('xbarra = {}'.format(_x_))
        else:
            _x_ = (resps[-2] - self.erro)
            print('xbarra = {}'.format(_x_))
        self.xbarra = _x_

    def __calc_erro(self):
        return abs(self.resps[-2]-self.resps[-1])/2

    def stop_criteria(self):
        if self.__calc_erro() < self.erro:
            return True
        else:
            return False

    def __recursi(self, columns2):
        symbol = self.symbol
        phi = self.phi
        resps = self.resps
        resp = float(phi.subs(symbol , resps[-1] + self.sinal*2*self.erro))
        resps.append(resp)
        result = self.stop_criteria()
        if result:
            print('Metodo de newton achou')
            print()
            return True
        elif self.iters == 0:
            print('esgotou iteracoes')
            print()
            return False
        else:
            self.df.loc[self.iters_ , 'Xn'] = resps[-2]

            if self.tipo == 'monotonica':
                if self.mono_tipo == 'crescente':
                    self.df.loc[self.iters_ ,'Xn + 2E'] = resps[-2] + 2*self.erro
                    self.df.loc[self.iters_ ,'f(Xn + 2E)'] = self.f.subs(self.symbol, resps[-2] + 2*self.erro).evalf()
                else:
                    self.df.loc[self.iters_ ,'Xn - 2E'] = resps[-2] - 2*self.erro
                    self.df.loc[self.iters_ ,'f(Xn - 2E)'] = self.f.subs(self.symbol, resps[-2] - 2*self.erro).evalf()

            self.df.loc[self.iters_ , columns2] = resps[-1]
            self.iters_ += 1
            self.df.loc[self.iters_ , 'Xn'] = resp
            self.df.loc[self.iters_ , 'Erro'] = self.__calc_erro()

            if self.tipo == 'monotonica':
                if self.mono_tipo == 'crescente':
                    self.df.loc[self.iters_ ,'Xn + 2E'] = resps[-1] + 2*self.erro
                    self.df.loc[self.iters_ ,'f(Xn + 2E)'] = self.f.subs(self.symbol, resps[-1] + 2*self.erro).evalf()
                else:
                    self.df.loc[self.iters_ ,'Xn - 2E'] = resps[-1] - 2*self.erro
                    self.df.loc[self.iters_ ,'f(Xn - 2E)'] = self.f.subs(self.symbol, resps[-1] - 2*self.erro).evalf()


            self.iters -= 1
            self.__recursi(columns2)

class Bisseccao:
    def __init__(self,f, symbol, intervalo, erro, visual = False):
        self.f = f
        self.symbol = symbol
        self.intervalo = intervalo
        self.erro = erro
        self.visual = visual
        self.df = pd.DataFrame(columns=['a','c','b','erro'])

        self.numero_de_passos()
        self.iters = 0
        self.check_inter()
        self.c = 0

    def recursi(self):
        a = self.a
        b = self.b
        self.df.loc[self.iters, 'a'] = a
        self.df.loc[self.iters, 'b'] = b
        self.c = (self.a + self.b)/2
        c = self.c
        self.df.loc[self.iters, 'c'] = c
        self.df.loc[self.iters, 'erro'] = b-c
        f = self.f
        symbol = self.symbol
        if f.subs(symbol, a) * f.subs(symbol, c) < 0:
            self.b = c
        else:
            if f.subs(symbol, c) * f.subs(symbol, b) < 0:
                self.a = c
            else:
                self.xbarra = c
                return
        self.n -= 1
        self.iters += 1
        if self.n <= 0:
            return
        else:
            self.recursi()

    def exec(self):
        self.numero_de_passos()
        self.recursi()


    def numero_de_passos(self):
        intervalo = self.intervalo
        a = float(intervalo.args[0])
        b = float(intervalo.args[1])
        self.a = a
        self.b = b
        n = np.ceil(np.log2((b-a)/(2*self.erro)))
        self.n = n + 1

    def check_inter(self):
        fcont = check_continuity(self.f,self.intervalo,self.symbol,self.visual)

        if not fcont:
            print('Intervalo invalido, f nao eh continua')

        return fcont

class Secantes:
    def __init__(self, f , symbols, x, y, erro):
        ''''x e y sao valores iniciais, e os symbols tao na ordem obvia'''
        self.symbol1 = symbols[0]
        self.symbol2 = symbols[1]
        symbol1 = self.symbol1
        symbol2 = self.symbol2
        self.erro = erro
        self.f = f
        self.x0 = y
        self.x1 = x
        self.df = pd.DataFrame()

        self.phi = symbol1 - (f*(symbol1-symbol2)/(f-f.subs(symbol1,symbol2)))


    def exec(self):
        self.df['Xn'] = np.nan
        self.df['Erro'] = np.nan
        self.resps = [self.x0, self.x1]
        self.x = self.resps[1]
        self.y = self.resps[0]
        self.iters = 100
        self.iters_ = 1
        self.df.loc[0, 'Xn'] = self.x0
        self.df.loc[1, 'Xn'] = self.x1
        self.df.loc[1, 'Erro'] = abs(self.x1 - self.x0)
        self.recursi()

    def recursi(self):
        x = self.x
        y = self.y
        resps = self.resps
        symbol1 = self.symbol1
        symbol2 = self.symbol2
        phi = self.phi
        z = phi.subs(symbol1,x).subs(symbol2,y).evalf()
        resps.append(z)
        self.y = x
        self.x = z
        self.iters -= 1
        self.iters_ += 1
        self.df.loc[self.iters_, 'Erro'] = abs(resps[-1]- resps[-2])
        self.df.loc[self.iters_, 'Xn'] = z
        if abs(resps[-2]- resps[-1]) < self.erro:# and abs(resps[-2]- resps[-3]) < self.erro:
            print(self.iters_)
        if abs(self.f.subs(symbol1, resps[-1])) < self.erro:
            print('achou')
            return True
        elif self.iters <= 0:
            print('nao achou')
            return False
        else:
            return self.recursi()

def arredonda(x, R):
    if R is None:
        return x
    if x != 0:
        sinalx = x/abs(x)
        if sinalx < 0:
            x *= -1
        digs = 0
        if x > 1:
            sinal = 1
            while x > 1:
                x /= 10
                digs += 1
            digs -= R
        else:
            sinal = -1
            while x < 1:
                x *= 10
                digs += 1
            digs -= 1
            digs += R
            x/= 10
        x = x*10**R + 0.5000001
        x = x//1
        x = x*10**(digs*sinal)
        if sinalx < 0:
            x*=-1
        return x
    else:
        return 0

def escalona_gauss(matrix, R, cond):
    matrix = copy.deepcopy(matrix)
    multipliers = zeros(matrix.shape[0], matrix.shape[1])
    swaps = []
    line = 0
    for a in range(matrix.cols - 1):
        # print()
        # print()
        # print('Interacao ', a)
        # print('Antes do swap')
        # pprint(matrix)
        if cond:
            line_ = 0
            refcol = copy.deepcopy(matrix.col(a)[line:])
            refcol = special_sort(refcol)
            while refcol != matrix.col(a)[line:]:
                colA = matrix.col(a)[line + line_:]
                Max = max(colA)
                Min = min(colA)
                if abs(Min) > abs(Max):
                    larger = Min
                else:
                    larger = Max
                indi = index(colA, larger) + line + line_
                if indi != line + line_:
                    matrix.row_swap(line + line_, indi)
                    swaps.append((line + line_, indi, 'Col ' + str(a)))
                line_ += 1

        # print('Depois do swap')
        # pprint(matrix)
        # print(swaps)
        colA = matrix.col(a)[line:]
        Pivot = float(colA[0])
        multis = colA[1:]#/Pivot
        if Pivot != 0:
            for i, multi in enumerate(multis):
                multis[i] = arredonda(multi/Pivot, R)
                multipliers[line + i + 1, a] = multis[i]
                Pivot_row = matrix.row(line)
                Target_row = matrix.row(line + i + 1)
                Result_row = Target_row - Pivot_row*multis[i]
                Result_row = Matrix([[arredonda(number, R) for number in Result_row]])
                # pprint(matrix)
                matrix.row_del(line + i + 1)
                # pprint(matrix)
                matrix = matrix.row_insert(line + i + 1, Result_row)
                # pprint(matrix)
                matrix[line + i + 1, a] = 0
        else:
            if cond:
                pass
            else:
                Max = max(colA)
                Min = min(colA)
                if abs(Max) < 0.0001 and abs(Min) < 0.0001:
                    pass
                else:
                    if abs(Min) > abs(Max):
                        larger = Min
                    else:
                        larger = Max
                    indi = index(colA, larger) + line
                    if indi != line :
                        matrix.row_swap(line , indi)
                        swaps.append((line , indi, 'Col ' + str(a)))

                    colA = matrix.col(a)[line:]
                    Pivot = float(colA[0])
                    multis = colA[1:]#/Pivot
                    for i, multi in enumerate(multis):
                        multis[i] = arredonda(multi/Pivot, R)
                        multipliers[line + i + 1, a] = multis[i]
                        Pivot_row = matrix.row(line)
                        Target_row = matrix.row(line + i + 1)
                        Result_row = Target_row - Pivot_row*multis[i]
                        Result_row = Matrix([[arredonda(number, R) for number in Result_row]])
                        # pprint(matrix)
                        matrix.row_del(line + i + 1)
                        # pprint(matrix)
                        matrix = matrix.row_insert(line + i + 1, Result_row)
                        # pprint(matrix)
                        matrix[line + i + 1, a] = 0


        line += 1
        # print('multiplicadore')
        # pprint(multis)
        # print('Apos CL')
        # pprint(matrix)
    return matrix, multipliers, matrix+multipliers, swaps

def special_sort(Orig_lis, Targ_lis = None, targ_size = -10):
    if targ_size < 0:
        Targ_lis = []
        targ_size = len(Orig_lis)
    Max = max(Orig_lis)
    Min = min(Orig_lis)
    if abs(Min) > abs(Max):
        larger = Min
    else:
        larger = Max
    Targ_lis.append(larger)
    Orig_lis.remove(larger)
    if len(Targ_lis) == targ_size:
        return Targ_lis
    else:
        return special_sort(Orig_lis, Targ_lis, targ_size)

def index(line,target):
    for i in range(len(line)):
        if line[i] == target:
            return i
    return 0

def resolve_U(matrix, b, R):
    matrix = copy.deepcopy(matrix)
    b = copy.deepcopy(b)
    A = matrix
    x = zeros(b.shape[0],1)
    var = symbols('var')
    for j in range(A.shape[0]-1, -1, -1):
        A_row = A[j,:]
        x[j] = var
        multi = A_row*x
        sol = arredonda(solve(multi[0]-b[j])[0],R)
        x[j] = sol
    return x

def resolve_L(matrix, b, R):
    matrix = copy.deepcopy(matrix)
    b = copy.deepcopy(b)
    A = matrix
    x = zeros(b.shape[0],1)
    var = symbols('var')
    for j in range(A.shape[0]):
        A_row = A[j,:]
        x[j] = var
        multi = A_row*x
        sol = arredonda(solve(multi[0]-b[j])[0],R)
        x[j] = sol
    return x

def executa_swaps(swaps, vector):
    vector = copy.deepcopy(vector)
    vector = copy.deepcopy(vector)
    if swaps == []:
        print('Nao houveram swaps')
        return 'Nao houveram swaps'
    lines = []
    for swap in swaps:
        lines.append(swap[0])
        lines.append(swap[1])
    maxline = max(lines)
    column = Matrix([i for i in range(1, maxline+2)])
    for swap in swaps:
        column.row_swap(swap[0], swap[1])
        vector.row_swap(swap[0], swap[1])
    return column, vector

def desexecuta_swaps(swaps, vector):
    swaps = copy.deepcopy(swaps)
    vector = copy.deepcopy(vector)
    vector = copy.deepcopy(vector)
    if swaps == []:
        print('Nao houveram swaps')
        return 'Nao houveram swaps'
    lines = []
    for swap in swaps:
        lines.append(swap[0])
        lines.append(swap[1])
    maxline = max(lines)
    column = Matrix([i for i in range(1, maxline+2)])
    swaps.reverse()
    for swap in swaps:
        column.row_swap(swap[1], swap[0])
        vector.row_swap(swap[1], swap[0])
    return column, vector

class gauss_elimi:
    def __init__(self, matrix_exted, R, condensa, erro):
        self.erro = erro
        self.matrix = copy.deepcopy(matrix_exted)
        self.b = self.matrix.col(-1)
        self.R = R
        self.iters = 15
        self.xs = []
        self.rs = []
        self.cs = []
        self.A, self.multipliers, self.A_escal_bonita, self.swaps = escalona_gauss(self.matrix, R, condensa)
        self.A_escal = copy.deepcopy(self.A)
        self.b_ = self.A.col(-1)
        self.A = self.A[:,:-1]
        self.matrix = self.matrix[:,:-1]
        self.iters_ = 0
        x0 = resolve_U(self.A, self.b_, R)
        self.xs.append(x0)
        self.erros = [np.nan]

    def recursi(self):
        self.iters -= 1

        r = copy.deepcopy(self.b - self.matrix*self.xs[-1])
        r = Matrix([[arredonda(number, self.R*2) for number in r]])
        r = r.transpose()
        self.rs.append(r)
        c = resolve_U(self.matrix, self.rs[-1], self.R)
        self.cs.append(c)
        x = c + self.xs[-1]
        x = Matrix([arredonda(number, self.R) for number in x])
        self.xs.append(x)
        self.iters_ += 1
        stop = self.stop_criteria()
        if stop:
            print('achou em {} iteracoes'.format(self.iters_))
            return True
        elif self.iters <= 0:
            print('nao achou')
            return True
        else:
            self.recursi()

    def stop_criteria(self):
        resps = self.xs
        vk = copy.deepcopy(resps[-1])
        vk_1 = copy.deepcopy(resps[-2])
        lista = []
        for i, x in enumerate(vk):
            if abs(vk[i]) > 0.00000001:
                v = abs(vk[i] - vk_1[i])/vk[i]
                lista.append(v)
            elif abs(vk[i]) <  0.00000001 and abs(vk_1[i]) <  0.00000001:
                lista.append(0)
            else:
                lista.append(1)
        var = max(lista).evalf()
        # print(lista)
        self.erros.append(var)
        if var < self.erro:
            return True
        else:
            return False

class decomposicao_LU:
    def __init__(self, matrix, R, condensa, erro):
        self.erro = erro
        self.matrix = copy.deepcopy(matrix)
        self.b = self.matrix.col(-1)
        self.R = R
        self.U, self.L, self.A_escal_bonita, self.swaps = escalona_gauss(self.matrix, R, condensa)
        self.U = copy.deepcopy(self.U)
        self.b_ = self.U.col(-1)
        self.U = self.U[:,:-1]
        self.L = self.L[:,:-1]
        self.L += eye(self.L.shape[0])
        self.matrix = self.matrix[:,:-1]
        self.P = eye(self.L.shape[0])
        self.P = executa_swaps(self.swaps, self.P)[1]
        self.iters = 15
        self.xs = []
        self.rs = []
        self.cs = []
        self.iters_ = 0
        x0 = resolve_L(self.L, self.b, self.R)
        x0 = resolve_U(self.U, x0, self.R)
        self.xs.append(x0)
        self.erros = [np.nan]


    def recursi(self):
        self.iters -= 1
        #LU = PB
        r = self.P*copy.deepcopy(self.b - self.matrix*self.xs[-1])
        r = Matrix([[arredonda(number, self.R*2) for number in r]])
        r = r.transpose()
        self.rs.append(r)
        c = resolve_L(self.L, self.rs[-1], self.R)
        c = resolve_U(self.U, c,  self.R)
        self.cs.append(c)
        x = c + self.xs[-1]
        x = Matrix([arredonda(number, self.R) for number in x])
        self.xs.append(x)
        self.iters_ += 1
        stop = self.stop_criteria()
        if stop:
            print('achou em {} iteracoes'.format(self.iters_))
            return True
        elif self.iters <= 0:
            print('nao achou')
            return True
        else:
            self.recursi()

    def stop_criteria(self):
        resps = self.xs
        vk = copy.deepcopy(resps[-1])
        vk_1 = copy.deepcopy(resps[-2])
        lista = []
        for i, x in enumerate(vk):
            if abs(vk[i]) > 0.00000001:
                v = abs(vk[i] - vk_1[i])/vk[i]
                lista.append(v)
            elif abs(vk[i]) <  0.00000001 and abs(vk_1[i]) <  0.00000001:
                lista.append(0)
            else:
                lista.append(1)
        var = max(lista).evalf()
        # print(lista)
        self.erros.append(var)
        if var < self.erro:
            return True
        else:
            return False

# A = Matrix([
#     [4,1,0,1],
#     [1,4,1,1],
#     [0,1,4,1]
# ])
#
# a = decomposicao_LU(A,5,True,0.01)
#
# a.L

class jacobi:
    def __init__(self, matrix, R, erro, x0 = None):
        if x0 is None:
            x0 = zeros(matrix.shape[0],1)

        self.matrix = copy.deepcopy(matrix)
        self.b = self.matrix.col(-1)
        self.matrix = self.matrix[:,:-1]
        self.R = R
        self.erro = erro
        self.xs = [x0]
        self.iters_ = 0
        self.iters = 15
        self.criterios_conv()
        self.erros = [np.nan]
        self.errosk = [np.nan]

    def recursi(self):
        matrix = self.matrix
        b = self.b
        xk_1 = self.xs[-1]
        xk = zeros(matrix.shape[0],1)
        for i in range(len(xk)):
            somatorio = 0
            for j in range(len(xk)):
                if j != i:
                    somatorio += matrix[j,i]*xk_1[j]
            xk[i] = arredonda((b[i] - somatorio)/matrix[i, i], self.R)
        self.iters_ += 1
        self.iters -= 1
        self.xs.append(xk)
        stop = self.stop_criteria()
        if stop:
            print('achou em {} iteracoes'.format(self.iters_))
            return True
        elif self.iters <= 0:
            print('nao achou')
            return True
        else:
            self.recursi()


    def stop_criteria(self):
        resps = self.xs
        vk = copy.deepcopy(resps[-1])
        vk_1 = copy.deepcopy(resps[-2])
        lista = []
        for i, x in enumerate(vk):
            if abs(vk[i]) > 0.00000001:
                v = abs(vk[i] - vk_1[i])/vk[i]
                lista.append(v)
            elif abs(vk[i]) <  0.00000001 and abs(vk_1[i]) <  0.00000001:
                lista.append(0)
            else:
                lista.append(1)
        var = max(lista).evalf()
        M = self.M
        vec_dif = vk - vk_1
        max_error = max(abs(vec_dif))
        errok = (M)/(1-M)*max_error
        vec_dif = (self.xs[0] - self.xs[1])
        max_error = max(abs(vec_dif))
        erro = (M**(self.iters_+1))/(1-M)*max_error
        self.erros.append(erro)
        self.errosk.append(errok)

        if var < self.erro:
            return True
        else:
            return False

    def criterios_conv(self):
        matrix = self.matrix
        eig = matrix.eigenvals()
        size = matrix.shape[0]
        vals = []
        for val in eig:
            vals.append(val.evalf())
        maior = max(vals)
        self.Maior_eig = maior
        if maior > 1:
            print('Talvez n convirja, M = {} > 1'.format(maior))
        diag_domi = False
        diag_domi_num = []
        for i in range(size):
            soma_diag = 0
            for j in range(size):
                if i != j:
                    soma_diag += abs(matrix[i,j])
            if abs(matrix[i,i]) > soma_diag:
                diag_domi = True
                diag_domi_num.append(i)

        if not diag_domi:
            print('Talvez n convirja, Diagonal {} nao dominante',format(diag_domi_num))

        Alfa = ones(size,1)
        for j in range(size):
            somato = 0
            for i in range(size):
                if i != j:
                    somato += abs(matrix[j,i])
            Alfa[j] = arredonda(somato/matrix[j,j], self.R)
        self.Alfa = Alfa
        self.M = max(Alfa).evalf()

        if self.M > 1:
            print('Talvez n convirja, criterio das linhas, M = {} > 1'.format(self.M))

class gauss_seidel:
    def __init__(self, matrix, R, erro, x0 = None):
        if x0 is None:
            x0 = zeros(matrix.shape[0],1)

        self.matrix = copy.deepcopy(matrix)
        self.b = self.matrix.col(-1)
        self.matrix = self.matrix[:,:-1]
        self.R = R
        self.erro = erro
        self.xs = [x0]
        self.iters_ = 0
        self.iters = 15
        self.criterios_conv()
        self.errosk = [np.nan]
        self.erros = [np.nan]

    def recursi(self):
        matrix = self.matrix
        b = self.b
        xk_1 = self.xs[-1]
        xk = zeros(matrix.shape[0],1)
        for i in range(len(xk)):
            somatorio = 0
            for j in range(len(xk)):
                if j != i:
                    if j < i:
                        somatorio += matrix[j,i]*xk[j]
                    else:
                        somatorio += matrix[j,i]*xk_1[j]
            xk[i] = arredonda((b[i] - somatorio)/matrix[i, i], self.R)
        self.iters_ += 1
        self.iters -= 1
        self.xs.append(xk)
        stop = self.stop_criteria()
        if stop:
            print('achou em {} iteracoes'.format(self.iters_))
            return True
        elif self.iters <= 0:
            print('nao achou')
            return True
        else:
            self.recursi()


    def stop_criteria(self):
        resps = self.xs
        vk = copy.deepcopy(resps[-1])
        vk_1 = copy.deepcopy(resps[-2])
        lista = []
        for i, x in enumerate(vk):
            if abs(vk[i]) > 0.00000001:
                v = abs(vk[i] - vk_1[i])/vk[i]
                lista.append(v)
            elif abs(vk[i]) <  0.00000001 and abs(vk_1[i]) <  0.00000001:
                lista.append(0)
            else:
                lista.append(1)
        var = max(lista).evalf()
        # print(lista)
        M = self.M
        vec_dif = vk - vk_1
        max_error = max(abs(vec_dif))
        errok = (M)/(1-M)*max_error
        vec_dif = (self.xs[0] - self.xs[1])
        max_error = max(abs(vec_dif))
        erro = (M**(self.iters_+1))/(1-M)*max_error
        self.erros.append(erro)
        self.errosk.append(errok)
        if var < self.erro:
            return True
        else:
            return False

    def criterios_conv(self):
        matrix = copy.deepcopy(self.matrix)
        eig = matrix.eigenvals()
        size = matrix.shape[0]
        vals = []
        for val in eig:
            vals.append(val.evalf())
        maior = max(vals)
        self.Maior_eig = maior
        if maior > 1:
            print('Talvez n convirja, raio espectral = {} > 1'.format(maior))
        diag_domi = False
        diag_domi_num = []
        for i in range(size):
            soma_diag = 0
            for j in range(size):
                if i != j:
                    soma_diag += abs(matrix[i,j])
            if abs(matrix[i,i]) > soma_diag:
                diag_domi = True
                diag_domi_num.append(i)

        if not diag_domi:
            print('Talvez n convirja, Diagonal {} nao dominante'.format(diag_domi_num))
        matrix = copy.deepcopy(self.matrix)
        Beta = ones(size,1)
        for j in range(size):
            somato = 0
            for i in range(size):
                if i != j:
                    somato += abs(Beta[i]*matrix[j,i])
            Beta[j] = arredonda(somato/matrix[j,j], self.R)
        self.Beta = Beta
        self.M = max(Beta).evalf()

        if self.M > 1:
            print('Talvez n convirja, sassenfeld, M = {} > 1'.format(self.M))

class Sor:
    def __init__(self, matrix, R, erro, w, x0 = None):
        if x0 is None:
            x0 = zeros(matrix.shape[0],1)
        self.w = w
        self.matrix = copy.deepcopy(matrix)
        self.b = self.matrix.col(-1)
        self.matrix = self.matrix[:,:-1]
        self.R = R
        self.erro = erro
        self.xs = [x0]
        self.iters_ = 0
        self.iters = 15
        self.criterios_conv()
        self.errosk = [np.nan]
        self.erros = [np.nan]

    def recursi(self):
        matrix = self.matrix
        b = self.b
        xk_1 = self.xs[-1]
        xk = zeros(matrix.shape[0],1)
        for i in range(len(xk)):
            somatorio = 0
            for j in range(len(xk)):
                if j != i:
                    if j < i:
                        somatorio += matrix[j,i]*xk[j]
                    else:
                        somatorio += matrix[j,i]*xk_1[j]
            xk[i] = arredonda( self.w * (b[i] - somatorio)/matrix[i, i] + (1-self.w)*xk_1[i] , self.R)
        self.iters_ += 1
        self.iters -= 1
        self.xs.append(xk)
        stop = self.stop_criteria()
        if stop:
            print('achou em {} iteracoes'.format(self.iters_))
            return True
        elif self.iters <= 0:
            print('nao achou')
            return True
        else:
            self.recursi()


    def stop_criteria(self):
        resps = self.xs
        vk = copy.deepcopy(resps[-1])
        vk_1 = copy.deepcopy(resps[-2])
        lista = []
        for i, x in enumerate(vk):
            if abs(vk[i]) > 0.00000001:
                v = abs(vk[i] - vk_1[i])/vk[i]
                lista.append(v)
            elif abs(vk[i]) <  0.00000001 and abs(vk_1[i]) <  0.00000001:
                lista.append(0)
            else:
                lista.append(1)
        var = max(lista).evalf()
        # print(lista)
        M = self.M
        vec_dif = vk - vk_1
        max_error = max(abs(vec_dif))
        errok = (M)/(1-M)*max_error
        vec_dif = (self.xs[0] - self.xs[1])
        max_error = max(abs(vec_dif))
        erro = (M**(self.iters_+1))/(1-M)*max_error
        self.erros.append(erro)
        self.errosk.append(errok)
        if var < self.erro:
            return True
        else:
            return False

    def criterios_conv(self):
        matrix = copy.deepcopy(self.matrix)
        eig = matrix.eigenvals()
        size = matrix.shape[0]
        vals = []
        for val in eig:
            vals.append(val.evalf())
        maior = max(vals)
        self.Maior_eig = maior
        if maior > 1:
            print('Talvez n convirja, raio espectral = {} > 1'.format(maior))
        diag_domi = False
        diag_domi_num = []
        for i in range(size):
            soma_diag = 0
            for j in range(size):
                if i != j:
                    soma_diag += abs(matrix[i,j])
            if abs(matrix[i,i]) > soma_diag:
                diag_domi = True
                diag_domi_num.append(i)

        if not diag_domi:
            print('Talvez n convirja, Diagonal {} nao dominante'.format(diag_domi_num))
        matrix = copy.deepcopy(self.matrix)
        Beta = ones(size,1)
        for j in range(size):
            somato = 0
            for i in range(size):
                if i != j:
                    somato += abs(Beta[i]*matrix[j,i])
            Beta[j] = arredonda(somato/matrix[j,j], self.R)
        self.Beta = Beta
        self.M = max(Beta).evalf()

        if self.M > 1:
            print('Talvez n convirja, sassenfeld, M = {} > 1'.format(self.M))

class MMQ_discri:
    def __init__(self, GS, symbol, Xvector, Yvector, R = None):
        ''''por funcao 1 dentro da GS, GS é uma lista de g's '''
        R = R
        symbol = symbol
        GS = GS
        GSvectors = []
        dim = len(GS)
        B = []
        for g in GS:
            gvector = []
            for X in Xvector:
                gvector.append(arredonda(g.subs(symbol,X).evalf(), R))
            gvector = Matrix(gvector)
            GSvectors.append(gvector)
            b = gvector.dot(Yvector)
            B.append(b)
        B = Matrix(B)

        matrix = zeros(dim)

        for i in range(dim):
            for j in range(dim):
                matrix[i,j] =  GSvectors[i].dot(GSvectors[j])
        self.matrix = matrix
        self.B = B
        self.sol = self.matrix.inverse_LU() * self.B
        Funcvecs = Matrix(GS)
        self.GS = Funcvecs
        self.sol_multiplied = self.sol.dot(Funcvecs)
        self.sol_multiplied_matrix = Funcvecs.multiply_elementwise(self.sol)

# funcao que nao 'e do tipo a *x + b, deve ser linearizada
# A linearizacao vai deixar algo do tipo F(f(x),x) = a_  *x + B_
# (ou seja, encontramos a_ e b_, tem que converter pro original de volta)
# Com esse F, temos que converter o Yvector, como no exemplo abaixo.
#
#
# Xvector = [2, 4, 6, 8, 10]
# Yvector = [51.34, 52.72, 40.60, 27.79, 17.84]
# x_, y_ = symbols('x* y*')
# F = log(y_/x_)
#
# convert_lienarizado(Xvector, Yvector, F, x_, y_)

def convert_lienarizado(Xvector, Yvector,F, symbolx,symboly):
    Y_vector = []
    for i in range(len(Xvector)):
        temp = F.subs({
            symbolx:Xvector[i],
            symboly:Yvector[i]
        }).evalf()
        Y_vector.append(temp)
    return Matrix(Y_vector)

# x = symbols('x')
#
# g0 = x*0 + 1
# g1 = x
# GS = [g0, g1]
# Xvector = [2, 4, 6, 8, 10]
# Yvector = [51.34, 52.72, 40.60, 27.79, 17.84]
# x_, y_ = symbols('x* y*')
# F = log(y_/x_)
#
# Yvector = convert_lienarizado(Xvector, Yvector, F, x_, y_)
#
# a = MMQ_discri(GS, x, Xvector, Yvector)
#
# print(solveset(log(400*x)-float(a.sol[0])))

class MMQ_conti:
    def __init__(self, GS, symbol, Func, intervalo, R = None):
        ''''por funcao 1 dentro da GS, GS é uma lista de g's '''
        inf = intervalo.args[0]
        sup = intervalo.args[1]
        symbol = symbol
        GS = GS
        dim = len(GS)
        B = []
        for g in GS:
            inte = Func * g
            b = integrate(inte,(symbol,inf,sup))
            b = b.evalf()
            B.append(b)

        B = Matrix(B)
        matrix = zeros(dim)
        for i in range(dim):
            for j in range(dim):
                inte = GS[i] *GS[j] #GSvectors[i].dot(GSvectors[j])
                prod = integrate(inte,(symbol,inf,sup))
                prod = prod.evalf()
                matrix[i,j] =  prod

        self.matrix = matrix
        self.B = B
        self.sol = self.matrix.inverse_LU() * self.B
        Funcvecs = Matrix(GS)
        self.GS = Funcvecs
        self.sol_multiplied = self.sol.dot(Funcvecs)
        self.sol_multiplied_matrix = Funcvecs.multiply_elementwise(self.sol)

# x = symbols('x')
# g0 = x*0 + 1
# g1 = x
# g2 = x**2 - 1/3
# g3 = x**3 - 3*x/5
#
#
# Func = exp(2*x) + exp(-2*x)
# GS = [g0, g1, g2, g3]
# intervalo = Interval(-0.5,0.5)
#
# a = MMQ_conti(GS, x, Func, intervalo)

class serie_harmonic:
    def __init__(self, ordem, symbol, Func, intervalo, R = None):
        ''''por funcao 1 dentro da GS, GS é uma lista de g's '''
        self.ordem = ordem
        inf = intervalo.args[0]
        sup = intervalo.args[1]
        self.symbol = symbol
        self.gera_gs()
        GS = self.GS
        dim = len(GS)
        B = []
        for g in GS:
            inte = Func * g
            b = integrate(inte,(symbol,inf,sup))
            b = b.evalf()
            B.append(b)

        B = Matrix(B)
        matrix = zeros(dim)
        for i in range(dim):
            for j in range(dim):
                inte = GS[i] *GS[j] #GSvectors[i].dot(GSvectors[j])
                prod = integrate(inte,(symbol,inf,sup))
                prod = prod.evalf()
                matrix[i,j] =  prod

        self.matrix = matrix
        self.B = B
        self.sol = self.matrix.inverse_LU() * self.B
        Funcvecs = Matrix(GS)
        self.GS = Funcvecs
        self.sol_multiplied = self.sol.dot(Funcvecs)
        self.sol_multiplied_matrix = Funcvecs.multiply_elementwise(self.sol)

    def gera_gs(self):
        ordem = self.ordem
        symbol = self.symbol
        a0 = symbol*0 + 1
        GS = [a0]
        for i in range(1, ordem + 1):
            g = cos(i*symbol)
            GS.append(g)
            g_ = sin(i*symbol)
            GS.append(g_)
        self.GS = GS

#Para converter intervalo funcao F
#Nos extremos tem que bater
# x(t) tal que x(fim inter novo) é igual F(fim inter antigo)



# x = symbols('x')
# Func = abs(abs(x)-1/4)
# intervalo = Interval(-1,1)
#
# a = serie_harmonic(3, x, Func, intervalo)
# a.sol_multiplied_matrix
#
# p1 = plot(Func,(x,-3,3), show=False)
# p2 = plot(cos(x),(x,-3,3), show=False)
# p1.append(p2[0])
# p1.show()

#%%


