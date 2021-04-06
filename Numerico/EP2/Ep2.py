#%%
#Lui Damianci Ferreira - 10770579
#Victor A. C. Athanasio - 9784401


from Testes import *



#%%

def main():
    ''''Interface com o usuario'''
    teste = input('Insira o teste que deseja fazer ("a", "b", "c" ou "d", deixe em branco para todos)')
    if teste.lower() == 'a':
        TesteA()
    elif teste.lower() == 'b':
        TesteB()
    else:
        N = int(input('Insira N: '))
        if teste.lower() == 'c':
            TesteC(N)
        elif teste.lower() == 'd':
            TesteD(N)
        elif teste.lower() == '':
            TodosTestes()

main()

#%%



