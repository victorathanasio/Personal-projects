#%% Ex1

efic_t = 0.78
efic_c = 0.72
efic_b = 0.48

Qe = 54 #kw

T = [None, None, None, None, None, None, None, None, None]
P = [None, None, None, None, None, None, None, None, None]
v = [None, None, None, None, None, None, None, None, None]
h = [None, None, None, None, None, None, None, None, None]
s = [None, None, None, None, None, None, None, None, None]
x = [None, None, None, None, None, None, None, None, None]

# P8 = 2 = 7 = 3


Tevap = -10

T[6] = Tevap
#estado6
estado6 = estado('r134a', 'saturado', T = T[6])
estado6.propriedade_dado_titulo(1) #vap saturado
P[6] = estado6.pressure * 100
v[6] = estado6.specific_volume
h[6] = estado6.specific_enthalpy
s[6] = estado6.specific_entropy
x[6] = estado6.titulo

#estado3
Tcond = 40
T[3] = Tcond

estado3 = estado('r134a', 'saturado', T = T[3])
estado3.propriedade_dado_titulo(0) #liq saturado
P[3] = estado3.pressure * 100
v[3] = estado3.specific_volume
h[3] = estado3.specific_enthalpy
s[3] = estado3.specific_entropy
x[3] = estado3.titulo

#estado1
T[1] = 95

estado1 = estado('r134a','saturado', T = T[1])
estado1.propriedade_dado_titulo(1)
P[1] = estado1.pressure * 100
v[1] = estado1.specific_volume
h[1] = estado1.specific_enthalpy
s[1] = estado1.specific_entropy
x[1] = estado1.titulo




#estado5
h[5] = h[3]
P[5] = P[6]

estado5 = check_saturado('r134a', 'specific_enthalpy', h[5], p=P[5])

if estado5[0]:
    estado5 = estado5[1]

T[5] = estado5.temperature
v[5] = estado5.specific_volume
h[5] = estado5.specific_enthalpy
s[5] = estado5.specific_entropy
x[5] = estado5.titulo

#estado7
P[7] = P[3]
h7 = symbols('h7')
estado7s = check_saturado('r134a', 'specific_entropy', s[6], p=P[7])

if not estado7s[0]:
    _estado7s = estado('r134a','gas', p=P[7], T = 50)
    estado7s = busca_estado('specific_entropy', s[6], 'T', _estado7s)

func = (estado7s.specific_enthalpy - h[6])/(h7 - h[6]) - efic_c

h7 = solve(func,h7)[0]

estado7 = busca_estado('specific_enthalpy', h7, 'T', _estado7s)

T[7] = estado7.temperature
v[7] = estado7.specific_volume
h[7] = estado7.specific_enthalpy
s[7] = estado7.specific_entropy


#estado2
P[2] = P[3]
h2 = symbols('h2')
estado2s = check_saturado('r134a', 'specific_entropy', s[1], p=P[2])

if estado2s[0]:
    estado2s = estado2s[1]

func = (h2 - h[1])/(estado2s.specific_enthalpy - h[1]) - efic_t

h2 = solve(func,h2)[0]

estado2 = estado('r134a','saturado', T = estado2s.temperature)
estado2.titulo_dada_propriedade('specific_enthalpy', h2)

T[2] = estado2.temperature
v[2] = estado2.specific_volume
h[2] = estado2.specific_enthalpy
s[2] = estado2.specific_entropy
x[2] = estado2.titulo


#estado8
P[8] = P[3]
trab_specific_evap = h[6] - h[5]
v_mass_evap = Qe/trab_specific_evap

v_mass_c = v_mass_evap
trab_specifc_compr = (h[7] - h[6])
trab_compr = trab_specifc_compr*v_mass_c

trab_t = -trab_compr

trab_specifc_t = (h[2] - h[1])
v_mass_t = trab_t/trab_specifc_t

h[8] = (v_mass_c*h[7] + v_mass_t*h[2])/(v_mass_c+v_mass_t)

estado8 = estado('r134a','saturado', p = P[8])
estado8.titulo_dada_propriedade('specific_enthalpy', h[8])
T[8] = estado8.temperature
v[8] = estado8.specific_volume
h[8] = estado8.specific_enthalpy
s[8] = estado8.specific_entropy
x[8] = estado8.titulo


#estado4

#trab imcompressivel
P[4] = P[1]
trab_specifc_b_ideal = (P[3] - P[4])*estado3.specific_volume

trab_specifc_b = trab_specifc_b_ideal/efic_b

h[4] = h[3] + abs(trab_specifc_b)

_estado4 = estado('r134a','gas', p = P[4], T = 40)
estado4 = busca_estado('specific_enthalpy',h[4],'T',_estado4)

T[4] = estado4.temperature
v[4] = estado4.specific_volume
h[4] = estado4.specific_enthalpy
s[4] = estado4.specific_entropy



for i in range(1,9):
    print('Temperature {} = {}'.format(i, T[i]))
print('--------------------------------')
for i in range(1,9):
    print('Pressure {} = {}'.format(i, P[i]))
print('--------------------------------')
for i in range(1,9):
    print('Specifc_vol {} = {}'.format(i, v[i]))
print('--------------------------------')
for i in range(1,9):
    print('Enthalpy {} = {}'.format(i, h[i]))
print('--------------------------------')
for i in range(1,9):
    print('Entropy {} = {}'.format(i, s[i]))
print('--------------------------------')
for i in range(1,9):
    print('Titulo {} = {}'.format(i, x[i]))

#%%
