#Lui Damianci Ferreira - 10770579
#Victor A. C. Athanasio - 9784401
# %%
from Ep2_functions import *
import matplotlib.pyplot as plt
import pandas as pd
from itertools import cycle, islice

string = 'Resultados \n \n' #referente a criacao do apendice contendo resultados
counter = 0 #referente a criacao do apendice contendo resultados
gerar_text = False #referente a criacao do apendice contendo resultados
a = time.time() 

# %% Teste A

def TesteA():
    ''''Executa teste A'''
    Name = 'Teste A'
    N = 128
    plist = [0.35]
    uarray = create_us(plist, N)
    uT = 7 * uarray[0]
    resp, uarray = resolveMMQ(plist, N, uT)
    exata = np.array([7])
    Erro = finalize(Name, resp, uT, uarray, N, exata, plist)
    return resp, Erro, exata, plist


# %% Teste B


def TesteB():
    ''''Executa teste B'''
    Name = 'Teste B'
    N = 128
    plist = [0.15, 0.3, 0.7, 0.8]
    uarray = create_us(plist, N)
    uT = 2.3 * uarray[0] + 3.7 * uarray[1] + 0.3 * uarray[2] + 4.2 * uarray[3]
    resp, uarray = resolveMMQ(plist, N, uT)
    exata = np.array([2.3, 3.7, 0.3, 4.2])
    Erro = finalize(Name, resp, uT, uarray, N, exata, plist)
    return resp, Erro, exata, plist


# %% TesteC


def TesteC(N):
    ''''Executa teste C'''
    Name = 'Teste C, N = {}'.format(N)
    plist, uT = read_text(N)
    resp, uarray = resolveMMQ(plist, N, uT)
    exata = np.array([1, 5, 2, 1.5, 2.2, 3.1, 0.6, 1.3, 3.9, 0.5])
    Erro = finalize(Name, resp, uT, uarray, N, exata, plist)
    return resp, Erro, exata, plist


# %%

def TesteD(N):
    ''''Executa teste D'''
    Name = 'Teste D, N = {}'.format(N)
    plist, uT = read_text(N)
    multipliers = np.random.random(N - 1)
    multipliers -= 0.5
    multipliers *= 2
    multipliers *= 0.01
    multipliers += 1
    multipliers = multipliers.reshape(N - 1, 1)
    uT = uT * multipliers
    resp, uarray = resolveMMQ(plist, N, uT)
    exata = np.array([1, 5, 2, 1.5, 2.2, 3.1, 0.6, 1.3, 3.9, 0.5])
    Erro = finalize(Name, resp, uT, uarray, N, exata, plist)
    return resp, Erro, exata, plist


# %%
def TodosTestes():
    ''''Executa todos os testes'''
    TesteA()
    TesteB()
    Ns = [128, 256, 512, 1024, 2048]

    respsc = []
    Errosc = []
    for n in Ns:
        resp, Erro, exatac, plistc = TesteC(n)
        respsc.append(resp)
        Errosc.append(Erro)

    plot_serie_barra('TesteC', respsc, exatac, plistc)

    respsD = []
    ErrosD = []
    for n in Ns:
        resp, Erro, exatad, plistd = TesteD(n)
        respsD.append(resp)
        ErrosD.append(Erro)

    plot_serie_barra('TesteD', respsD, exatad, plistd)
    plot_serie_erro(ErrosD, Errosc)


# %% Graficos
def finalize(Name, resp, uT, uarray, N, exata, plist):
    ''''Imprime os resultados e executa as analises de cada teste'''
    print_resp(Name, resp)
    sol = our_sol(resp, uarray)
    Erro = Erro_quadratico(N, sol, uT)
    plot_exataXsol(Name, uT, sol, Erro)
    plot_barra(Name, resp, exata, plist)
    return Erro


def print_resp(Name, resp):
    ''''Imprime respostas do teste de forma bonita e organizada'''
    global string
    global counter
    print('---------------------------------------------------------------------------------------')
    print(Name, ':')
    if counter % 2 == 0:
        string += r'\begin{multicols}{2}' + '\n' #referente a criacao do apendice contendo resultados
    string += r'\noindent\rule{\linewidth}{0.4pt}' + '\n' #referente a criacao do apendice contendo resultados

    string += Name + ':' + '\n \n' #referente a criacao do apendice contendo resultados
    df = pd.DataFrame(columns=['', 'Ak'])
    for i in range(resp.shape[0]):
        df.loc[i, ''] = 'a{} = '.format(i + 1)
        df.loc[i, 'Ak'] = resp[i]
        print('a{} = {}'.format(i + 1, resp[i]))
        string += 'a{} = {}'.format(i + 1, resp[i]) + '\n \n' #referente a criacao do apendice contendo resultados
    string = string[:-2] #referente a criacao do apendice contendo resultados
    string += r'\\'  #referente a criacao do apendice contendo resultados
    df = df.set_index('').dropna()
    print()
    string += '\n'#referente a criacao do apendice contendo resultados

def our_sol(resp, uarray):
    ''''Calcula o vetor solucao baseado nas intensidades do MMQ'''
    sol = np.zeros((uarray.shape[1], 1))
    for i in range(resp.shape[0]):
        sol += resp[i] * uarray[i]
    return sol

def Erro_quadratico(N, sol, uT):
    ''''Calcula erro quadrático'''
    global string
    global counter
    DeltaX = 1 / N
    Erro_ponto_a_ponto = uT - sol
    # vector *= vector
    # sum = np.sum(vector)
    # sum *= DeltaX
    # Erro = np.sqrt(sum) Esses passo podem ser substituidos por:
    Erro = prod_interno(Erro_ponto_a_ponto, Erro_ponto_a_ponto)
    Erro = np.sqrt(DeltaX*Erro)
    print('Erro quadrático: {}'.format(Erro))
    string += 'Erro quadrático: {}'.format(Erro) #referente a criacao do apendice contendo resultados
    print()
    string += '\n \n' #referente a criacao do apendice contendo resultados
    if counter % 2 == 1: #referente a criacao do apendice contendo resultados
        string = string[:-2] #referente a criacao do apendice contendo resultados
        string += r'\end{multicols}' + '\n \n' #referente a criacao do apendice contendo resultados
    counter += 1 #referente a criacao do apendice contendo resultados
    return Erro





def plot_exataXsol(Name, vector, sol, Erro):
    ''''Plota a solucao exata, nossa solucao e a diferenca entre ambas no instante T'''
    N = vector.shape[0] + 1
    xspace = np.linspace(0, 1, N + 1)[1:-1]

    plt.clf()
    plt.plot(xspace, vector)
    plt.plot(xspace, sol)
    plt.ylim(0, np.max(vector) + 0.15*np.max(vector))
    plt.xlim(0, 1)
    plt.legend(['Solução exata', 'Solução calculada'])
    plt.ylabel('Temperature')
    plt.xlabel('Position')
    plt.suptitle('Solução exata e calculada, ' + Name)
    plt.text(0.35, 0.5, 'Erro quadrático = {}'.format(np.format_float_scientific(Erro, 2)), dict(size=12))
    plt.savefig('{}.png'.format('plots/exataXcalculada' + Name))
    plt.show()

    plt.clf()
    plt.plot(xspace, vector - sol)
    plt.axhline(0, color='black', lw=1)
    plt.xlim(0, 1)
    plt.legend(['Erro'])
    plt.ylabel('Diference in temperature')
    plt.xlabel('Position')
    plt.suptitle('Diferença entre solução exata e calculada (erro ponto a ponto), ' + Name)
    plt.savefig('{}.png'.format('plots/erro' + Name))
    plt.show()


def plot_barra(Name, resp, exata, plist):
    ''''Plota grafico de barras representando as intensidades calculadas e as exatas'''
    plt.clf()


    fig = plt.figure(frameon=False)
    ax = fig.add_axes([0, 0, 1, 1])
    X = np.array(plist)
    espessura = 0.014
    ax.set_xlim(0, 1)
    ax.bar(X - espessura / 2, resp, width=espessura)
    fig.add_axes(ax)
    ax.bar(X + espessura / 2, exata, width=espessura)
    ax.legend(labels=['Intensidade calculada', 'Intensidade exata'])
    ax.set_title('Intensidade calculada e exata, {}'.format(Name))
    ax.set_xlabel('Posição na barra')
    ax.set_ylabel('')

    fig.add_axes(ax)
    fig.savefig('{}.png'.format('plots/barras' + Name), bbox_inches='tight', pad_inches=0)
    fig.show()


def plot_serie_barra(Name, resps, exata, plist):
    ''''Plota a evolucao da intensidade de cada fonte em funcao do refinamento da malha, plota tambem uma linha que
    contem a resposta exata '''
    width = 0.35
    matrix = resps[0]
    for i in range(1, len(resps)):
        matrix = np.vstack((matrix, resps[i]))
    for i in range(len(plist)):
        plt.clf()
        data = matrix[:, i:i + 1].reshape(5)
        data = pd.DataFrame({
            'Intensidade calculada': data,
            'Intensidade exata': np.ones(len(data)) * exata[i]
        })
        my_colors = list(
            islice(cycle(['darkturquoise', 'deepskyblue', 'darkcyan', 'lightseagreen', 'c']), None, len(data)))

        data['Intensidade calculada'].plot(kind='bar', width=width, color=my_colors,
                                           title='Evolução da intensidade com N, {}, P = {}'.format(Name, plist[i]), legend=True)

        data['Intensidade exata'].plot()
        ax = plt.gca()
        ax.set_xticklabels(('128', '256', '512', '1024', '2048'))
        # ax.set_xticklabels(('128', '256', '512'))
        ax.set_xlabel("N", fontsize=12)
        ax.set_ylabel("Intensidade da fonte", fontsize=12)
        ax.legend(labels=['Intensidade exata', 'Intensidade calculada'],  loc='lower left')
        # plt.show()
        plt.savefig('{}.png'.format('plots/barras_pp' + Name + 'P=' + str(plist[i])))


def plot_serie_erro(erroD, erroC):
    ''''Plota a evolucao do erro com o refinamento da malha'''
    xspace = np.array([128, 256, 512, 1024, 2048])
    plt.clf()
    plt.plot(xspace, erroD)
    plt.plot(xspace, erroC)
    plt.ylim(0, 0.12)
    plt.legend(['Erro Teste D', 'Erro Teste C'])
    plt.ylabel('Erro quadrático')
    plt.xlabel('N')
    plt.suptitle('Evolução do erro em função de N')
    plt.savefig('{}.png'.format('plots/erroXn'))
    plt.show()

if gerar_text: #referente a criacao do apendice contendo resultados
    ''''Apenas usada para gerar o apendice que vai para o relatorio'''
    TodosTestes() #referente a criacao do apendice contendo resultados

    f = open('Resultados.txt', 'w') #referente a criacao do apendice contendo resultados

    f.write(string) #referente a criacao do apendice contendo resultados

    f.close() #referente a criacao do apendice contendo resultados

    print('Tempo total de execução:',time.time() - a)