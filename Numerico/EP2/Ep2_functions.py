#Lui Damianci Ferreira - 10770579
#Victor A. C. Athanasio - 9784401

from Ep1 import *


####### Este arquivo cont'em os metodos desenvolvidos para o Ep2

# %% Item A

def create_us(plist, N):
    ''''Recebe uma lista de pontos e calcula os vetores U's correspondentes
    Recebe tambem o parametro N
    Devolve os vetores U dentro de um vetor maior, cada vetor U é um vetor coluna.
    '''
    ulist = []
    for p in plist:
        u = crank_nicolson(N, p).execute()[1:-1]  # slicing para retirada das bordas
        ulist.append(u)
    return np.array(ulist)


# %% Item B
@vectorize()
def _prod_interno(x, y):
    ''''Executa multiplicacao element_wise dentre 2 vetores'''
    return x * y


@njit(parallel=True)
def prod_interno(x, y):
    ''''Executa o produto interno entre 2 vetores'''
    vec = _prod_interno(x, y)
    vec = np.sum(vec)
    return vec


@njit(parallel=True)
def create_matrix_MMQ(uarray):
    ''''Funcao que cria a matriz do MMQ
    Ela basicamente executa os produtos internos corretos, na metade inferior da matrix
    soma a matrix com sua transposta, tirando vantagem da natureza simetrica do problema,
    para executar menos calculos.'''
    shape = uarray.shape[0]
    matrix = np.zeros((shape, shape))
    for i in range(shape):
        for j in range(shape):
            if j > i:
                matrix[i][j] = prod_interno(uarray[i], uarray[j])
    matrixt = matrix.transpose()
    matrix += matrixt
    for i in range(shape):
        matrix[i][i] = prod_interno(uarray[i], uarray[i])
    return matrix


@njit(parallel=True)
def create_right_side_MMQ(uarray, ut):
    ''''funcao que cria o lado direito do sistema MMQ, funciona de forma analoga
    a funcao que cria a matrix do sistema MMQ'''
    shape = uarray.shape[0]
    matrix = np.zeros(shape)
    for i in range(shape):
        matrix[i] = prod_interno(uarray[i], ut)
    return matrix


# %% ItemC
@njit()
def achaLxy(matrix, L, D, x, y):
    ''''Encontra o termo Lxy mais detalhes sobre este termo podem ser vistas no relatório'''
    Lxy = matrix[x, y]
    for k in range(x):
        Lxy -= D[k] * L[x, k] * L[y, k]
    return Lxy / D[y]


@njit()
def achaDz(matrix, L, D, z):
    ''''Encontra o termo Dz mais detalhes sobre este termo podem ser vistas no relatório'''
    Dz = matrix[z, z]
    for k in range(z):
        Dz -= D[k] * L[z, k] ** 2
    return Dz


@njit(parallel=True)
def LDLt(matrix):
    ''''Encontra as matrizes L e D, vale notar que D foi armazena em um vetor. Isso foi feito para eficiencia
    computacional, uma vez que a matriz D é esparsa '''
    size = matrix.shape[0]
    L = np.zeros((size, size))
    D = np.zeros(size)
    for i in range(size):
        D[i] = achaDz(matrix, L, D, i)
        L[i, i] = 1
        for k in range(i + 1, size):
            L[k, i] = achaLxy(matrix, L, D, k, i)
    return L, D


@njit(parallel=True)
def resolve_U(matrix, b):
    ''''Resolve sistemas superiores'''
    A = matrix
    x = np.zeros(b.shape[0])
    for j in range(A.shape[0] - 1, -1, -1):
        A_row = A[j, :]
        SUM = prod_interno(A_row, x)
        x[j] = b[j] - SUM
        x[j] = x[j] / A_row[j]
    return x


@njit(parallel=True)
def resolve_L(matrix, b):
    ''''Resolve sistemas inferiores'''
    A = matrix
    x = np.zeros(b.shape[0])
    for j in range(A.shape[0]):
        A_row = A[j, :]
        SUM = prod_interno(A_row, x)
        x[j] = b[j] - SUM
        x[j] = x[j] / A_row[j]
    return x


@njit(parallel=True)
def resolve_D(D, b):
    ''''Resolve sistemas diagonains'''
    return b / D


@njit()
def resolve_LDLt(L, D, b):
    ''''Aplica as resolucoes sucessivamente, para resolver um sistema LDLt'''
    b1 = resolve_L(L, b)
    b2 = resolve_D(D, b1)
    b3 = resolve_U(L.transpose(), b2)
    return b3


# %% Extras

def resolveMMQ(plist, N, uT):
    ''''Agrupa os metodos anteriores sob uma unica funcao'''
    uarray = create_us(plist, N)
    matrix = create_matrix_MMQ(uarray)
    b = create_right_side_MMQ(uarray, uT)
    L, D = LDLt(matrix)
    resp = resolve_LDLt(L, D, b)
    return resp, uarray


def read_text(N):
    ''''Le o arquivo de teste disponibilizado no moodle, e retorna o vetor U e a posição das fontes'''
    mod = 2048 // N

    f = open("teste.txt", "r")

    positions = f.readline().split()
    for i in range(len(positions)):
        positions[i] = float(positions[i])

    uT = f.read().splitlines()
    uT_serialized = []
    for i in range(len(uT)):
        if i % mod == 0:
            uT_serialized.append(float(uT[i]))

    f.close()

    return positions, np.array(uT_serialized)[1:-1].reshape((N - 1, 1))
