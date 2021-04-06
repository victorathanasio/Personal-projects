# %%

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from numpy import *

options = Options()
options.headless = False
options.add_argument('log-level=3')
browser = webdriver.Chrome('chromedriver.exe', options=options)
from sympy import *

# %%

sites = {
    'water': 'https://www.peacesoftware.de/einigewerte/wasser_dampf_e.html',
    'air': 'https://www.peacesoftware.de/einigewerte/luft_e.html',
    'r134a': 'http://www.peacesoftware.de/einigewerte/r134a_e.html',
    'nh3': 'https://www.peacesoftware.de/einigewerte/nh3_e.html',
    'co2': 'https://www.peacesoftware.de/einigewerte/co2_e.html'
}

forms = {
    'water': {'liq': 0,
              'gas': 1,
              'saturado': 2
              },

    'air': {'gas': 0
            },

    'r134a': {'gas': 0,
              'saturado': 1,
              },

    'nh3': {'gas': 0,
            'saturado': 1,
            },
    'co2': {'gas': 0,
            'saturado': 1,
            }
}

formspd = pd.DataFrame.from_dict(forms)
formspd = formspd.fillna('-')


# %%


# %%

class estado():
    '''
    Estado termodinamico
    '''

    def __init__(self, material, table, p=None, T=None):
        global browser
        self.browser = browser
        self.browser.get(sites[material])
        self._material = material
        self._table_name = table
        self._forms_id = forms[material][table]
        if p != None:
            self._p = p / 100
        else:
            self._p = None
        if T != None:
            self._T = T
        else:
            self._T = None
        self.wrong = False
        # try:
        #     data_frame = self._get_properties()
        # except:
        #     self.wrong = True
        #     print('Verifique se as condições dão na tabela selecionada')
        self._get_properties()
        self._p = p
        # print(self)

    def titulo_dada_propriedade(self, propriedade, propriedade_target):
        if not self._table_name == 'saturado':
            print('estado não saturado')
            return None
        propriedade_liq, propriedade_gas = satura_propriedade(propriedade, self._material)

        propriedade_gas = self.get_propriedade(propriedade_gas)

        propriedade_liq = self.get_propriedade(propriedade_liq)

        titulo = symbols('titulo')

        func = titulo * propriedade_gas + (1 - titulo) * propriedade_liq - propriedade_target
        titulo = solve(func, titulo)[0]
        self.propriedade_dado_titulo(titulo)

    def propriedade_dado_titulo(self, titulo):
        if not self._table_name == 'saturado':
            print('estado não saturado')
            return None
        propriedades = ['specific_volume', 'specific_enthalpy', 'specific_entropy']
        for propriedade in propriedades:
            propriedade_liq, propriedade_gas = satura_propriedade(propriedade, self._material)

            propriedade_gas = self.get_propriedade(propriedade_gas)

            propriedade_liq = self.get_propriedade(propriedade_liq)

            propriedade_value = titulo * propriedade_gas + (1 - titulo) * propriedade_liq

            self.set_propriedade(propriedade, propriedade_value)
        self.set_propriedade('titulo', titulo)
        return self.titulo

    def _get_properties(self):
        p = str(self._p)
        T = str(self._T)
        input_forms = self.browser.find_elements_by_tag_name('form')[self._forms_id]
        input_table = input_forms.find_element_by_tag_name('table')
        inputs = input_table.find_elements_by_tag_name('input')
        confirm_btn = input_forms.find_elements_by_tag_name('input')[-1]
        if p != 'None':
            inputs[0].send_keys(p)
        if T != 'None':
            inputs[1].send_keys(T)
        confirm_btn.click()
        data_frame = pd.read_html(self.browser.page_source, header=0)[1]
        data_frame = data_frame.fillna('None')
        data_frame['Properties'] = data_frame.apply(lambda x: set_properties(x.Property, x.Value, x.Unit), axis=1)

        property_list = data_frame['Properties'].tolist()

        counter = 0
        for property in property_list:
            a = property
            code = "self.{} = a[0].value".format(a[0].name)
            code = code.replace("'", "")
            # print(code)
            exec(code)
            if 'density' in a[0].name:
                if self._table_name != 'saturado':
                    specific_volume = 1 / a[0].value
                    self.specific_volume = specific_volume
                else:
                    if counter != 0:
                        specific_volume_liq, specific_volume_gas = satura_propriedade('specific_volume', self._material)
                        density_liq, density_gas = satura_propriedade('density', self._material)
                        specific_volume_liq_val = 1 / self.get_propriedade(density_liq)
                        specific_volume_gas_val = 1 / self.get_propriedade(density_gas)
                        self.set_propriedade(specific_volume_liq, specific_volume_liq_val)
                        self.set_propriedade(specific_volume_gas, specific_volume_gas_val)
                    counter += 1

        self.data_frame = data_frame
        self.data_frame = self.data_frame.drop('Properties', axis=1)

    def __str__(self):
        if not self.wrong:
            pressure = self.pressure
            temperature = self.temperature
            return 'Estado = {}, tabela: {}, Pressão = {} Kpa, Temperatura = {} Celsius'.format(self.medium,
                                                                                                self._table_name,
                                                                                                pressure,
                                                                                                temperature)
        else:
            return 'Tabela errada'

    def quit(self):
        self.browser.quit()

    def get_propriedade(self, propriedade):
        ldict = locals()
        code = 'propriedade = self.{}'.format(propriedade)
        exec(code, ldict)
        propriedade = ldict['propriedade']
        return propriedade

    def set_propriedade(self, propriedade, value):
        code = 'self.{} = {}'.format(propriedade, value)
        exec(code, locals())


class Property():
    '''
    Classe auxiliar
    '''

    def __init__(self, name, value, unit):
        self.name = name
        self.value = value
        self.unit = unit

    def __str__(self):
        if self.unit != 'None':
            return '{} = {} {}'.format(self.name, self.value, self.unit)
        else:
            return '{} = {}'.format(self.name, self.value)


def set_properties(property, Value, Unit):
    if str(Unit) == 'nan':
        Unit = 'None'
    name = property.replace(':', '')
    name = name.replace(" ", '_')
    name = name.replace("-", '_').lower()
    name = name.replace("_(calculated)", '')
    name = name.replace("boiling_", '')

    if name[-1] == '_':
        name = name[:-1]
    try:
        value = float(Value)
    except:
        value = Value
    unit = Unit.replace('[', '')
    unit = unit.replace(']', '')

    return [Property(name, value, unit)]


def busca_estado(property, target, variable, initial_state, delta=200, iters=100, precision=0.99999, dir=1,
                 proporcionalidade=1):
    '''Dado um estado inicial, variando a pressao ou a temperatura, ele encontra outro estado, baseado numa segunda propriedade'''
    if iters < 0:
        print('Não achou')
        return None
    ldict = locals()
    try:
        p = float(initial_state._p)
    except:
        p = None
    try:
        T = float(initial_state._T)
    except:
        T = None
    material = initial_state._material
    table = initial_state._table_name
    code = 'atual = initial_state.{}'.format(property)
    exec(code, ldict)
    atual = ldict['atual']
    if iters == 100:
        if variable == 'T':
            T += 5
        if variable == 'p':
            p += 5
        next_state = estado(material, table, p, T)
        ldict = locals()
        code = 'next = next_state.{}'.format(property)
        exec(code, ldict)
        next = ldict['next']
        proporcionalidade = (next - atual) / abs(next - atual)

    real_dir = dir * proporcionalidade
    if variable == 'T':
        T += delta * real_dir
    if variable == 'p':
        p += delta * real_dir
    try:
        next_state = estado(material, table, p, T)
        ldict = locals()
        code = 'next = next_state.{}'.format(property)
        exec(code, ldict)
        next = ldict['next']
        if (next - target) * proporcionalidade * real_dir > 0:
            dir *= -1
            delta /= 2
        if abs(next - target) < 1 - precision:
            return next_state
        else:
            return busca_estado(property, target, variable, next_state, delta=delta, iters=iters - 1,
                                precision=precision,
                                dir=dir, proporcionalidade=proporcionalidade)
    except:
        return busca_estado(property, target, variable, initial_state, delta=delta / 2, iters=iters - 1,
                            precision=precision,
                            dir=dir, proporcionalidade=proporcionalidade)


def interpolador_h_s_gas(h, s, estado_inicial, iters=100, precision=0.99999, delta=100):
    '''Dada uma entropia e uma entalpia de um gas super aquecido, econtra esse estado
    Só usar como last resource, n se deve saber nem temperatura nem pressao
    Util em ciclos rankine com eficiencia isoentropica diferente de 100 onde de um lado se tem ume turbina e do outro uma valvula
    '''
    material = estado_inicial._material
    table = estado_inicial._table_name
    p_atual = float(estado_inicial._p)
    T_atual = float(estado_inicial._T)
    estado00 = estado_inicial
    estado10 = estado(material, table, p_atual, T_atual + delta)
    estado11 = estado(material, table, p_atual + delta, T_atual + delta)
    estado01 = estado(material, table, p_atual + delta, T_atual)

    arr = array([[T_atual, '', T_atual + delta],
                 [estado00.specific_enthalpy, h, estado10.specific_enthalpy]])
    T_new = interpolacao(arr)

    arr = array([[estado00.specific_entropy, '', estado10.specific_entropy],
                 [T_atual, T_new, T_atual + delta]])
    S0 = interpolacao(arr)

    arr = array([[estado01.specific_entropy, '', estado11.specific_entropy],
                 [T_atual, T_new, T_atual + delta]])
    S1 = interpolacao(arr)

    arr = array([[p_atual, '', p_atual + delta],
                 [S0, s, S1]])
    p_new = interpolacao(arr)

    estado_new = estado(material, table, p_new, T_new)
    print(estado_new.specific_entropy)
    if abs(estado_new.specific_entropy - s) <= 1 - precision and abs(estado_new.specific_enthalpy - h) <= 1 - precision:
        return estado_new
    return interpolador_h_s_gas(h, s, estado_new, iters=iters - 1, precision=0.99999, delta=0.8 * delta)


def interpolacao(arr):
    # print(arr)
    fill_row, fill_column = where(arr == '')
    other_row = [i for i in range(arr.shape[0]) if i != fill_row][0]
    other_coluns = [i for i in range(arr.shape[1]) if i != fill_column]
    deltaUp = float(arr[other_row][fill_column][0]) - float(arr[other_row][other_coluns[0]])
    deltaDown = float(arr[other_row][other_coluns[1]]) - float(arr[other_row][other_coluns[0]])
    deltaN = float(arr[fill_row][0][other_coluns[1]]) - float(arr[fill_row][0][other_coluns[0]])
    return deltaUp / deltaDown * deltaN + float(arr[fill_row][0][other_coluns[0]])


def getIndexes(dfObj, value):
    ''' Get index positions of value in dataframe i.e. dfObj.'''

    listOfPos = list()
    # Get bool dataframe with True at positions where the given value exists
    result = dfObj.isin([value])
    # Get list of columns that contains the value
    seriesObj = result.any()
    columnNames = list(seriesObj[seriesObj == True].index)
    # Iterate over list of columns and fetch the rows indexes where value exists
    for col in columnNames:
        rows = list(result[col][result[col] == True].index)
        for row in rows:
            listOfPos.append((row, col))
    # Return a list of tuples indicating the positions of value in the dataframe
    return listOfPos[0]


def interpolador_h_s_liq(h, s, estado_inicial, iters=100, precision=0.99999, delta=100):
    '''Mesma coisa que o do gas, mas para liquidos'''
    material = estado_inicial._material
    table = estado_inicial._table_name
    p_atual = float(estado_inicial._p)
    T_atual = float(estado_inicial._T)
    estado00 = estado_inicial
    estado10 = estado(material, table, p_atual, T_atual + delta)
    estado11 = estado(material, table, p_atual + delta, T_atual + delta)
    estado01 = estado(material, table, p_atual + delta, T_atual)

    arr = array([[T_atual, '', T_atual + delta],
                 [estado00.specific_enthalpy, h, estado10.specific_enthalpy]])
    T_new = interpolacao(arr)

    # arr = array([[estado00.specific_entropy,'',estado10.specific_entropy],
    #         [T_atual, T_new,T_atual + delta]])
    # S0 = interpolacao(arr)
    #
    # arr = array([[estado01.specific_entropy,'',estado11.specific_entropy],
    #         [T_atual, T_new,T_atual + delta]])
    # S1 = interpolacao(arr)
    #
    # arr = array([[p_atual,'',p_atual + delta],
    #         [S0, s, S1]])
    # p_new = interpolacao(arr)

    estado_new = estado(material, table, p_atual, T_new)
    print('Temperatura agua comprimida')
    return estado_new._T


def satura_propriedade(propriedade, material):
    ''''devolve primeiro liq, dps gas'''
    if material == 'water':
        propriedade_liq = propriedade + '_water'
        propriedade_gas = propriedade + '_steam'
    else:
        propriedade_liq = propriedade + '_fluid'
        propriedade_gas = propriedade + '_gas'
    return propriedade_liq, propriedade_gas


def check_saturado(material, propriedade, propriedade_value, p=None, T=None):
    ''' Dadu um estado saturado verifica se a propriedade analisada pode pertencer a ele'''
    propriedade_liq, propriedade_gas = satura_propriedade(propriedade, material)
    try:
        if p != None:
            possivel_estado = estado(material, 'saturado', p=p)
        if T != None:
            possivel_estado = estado(material, 'saturado', T=p)
        propriedade_liq = possivel_estado.get_propriedade(propriedade_liq)
        propriedade_gas = possivel_estado.get_propriedade(propriedade_gas)
        possivel_estado.titulo_dada_propriedade(propriedade, propriedade_value)
        if propriedade_gas < propriedade_value < propriedade_liq:
            return True, possivel_estado
        elif propriedade_gas > propriedade_value > propriedade_liq:
            return True, possivel_estado
        else:
            return False, False
    except:
        print('error')
        return False, False


def turbina(estado_antes_turbina, eficiencia, pressao_final):
    '''Dada uma turbina com uma eficiencia, se souber a pressao final, devolve o estado
    util em cogeracao rankine'''
    '''Retorna estado pos turbina e estado pos turbina isoentropica'''

    ''''Explicação do ex:
    Primeiro finge que a turbina é isoentropica, e encontra um estado auxiliar
    Verifica se vira vapor ou saturado (com base na entropia e pressao final) e ai encontra a entalpia
    Com a entalpia e a eficiencia, calcula a entalpia real
    Verifica se é saturado ou vapor (com base na entalpia e pressao final)
    Feito isso, se tem o estado.
    '''

    s_pre_turb = estado_antes_turbina.specific_entropy
    s_pos_turb_s = s_pre_turb
    h_pre_turb = estado_antes_turbina.specific_enthalpy
    material = estado_antes_turbina._material

    satureba1 = check_saturado(material, 'specific_entropy', s_pos_turb_s, p=pressao_final)
    if satureba1[0]:
        estado_pos_turbina_s = satureba1[1]
        estado_pos_turbina_s.propriedade_dado_titulo('specific_enthalpy', estado_pos_turbina_s.titulo)
    else:
        estado_pos_turbina_s_init = estado('water', 'gas', pressao_final, 500)
        estado_pos_turbina_s = busca_estado('specific_entropy', s_pos_turb_s, 'T', estado_pos_turbina_s_init)

    h_pos_turb_s = estado_pos_turbina_s.specific_enthalpy
    h_pos_turb = symbols('pos_turb')
    fun = (h_pre_turb - h_pos_turb) / (h_pre_turb - h_pos_turb_s) - eficiencia
    sol = solve(fun, h_pos_turb)
    h_pos_turb = sol[0]

    satureba2 = check_saturado(material, 'specific_enthalpy', h_pos_turb, p=pressao_final)
    if satureba2[0]:
        estado_pos_turbina = satureba2[1]
        estado_pos_turbina.propriedade_dado_titulo('specific_entropy', estado_pos_turbina.titulo)

    else:
        estado_pos_turbina_init = estado('water', 'gas', pressao_final, 500)
        estado_pos_turbina = busca_estado('specific_enthalpy', h_pos_turb, 'T', estado_pos_turbina_init)
    return estado_pos_turbina, estado_pos_turbina_s


def compressor(estado_antes_compressor, eficiencia, pressao_final, R):
    s_pre_compr = estado_antes_compressor.specific_entropy
    pressao_inicial = estado_antes_compressor._p
    s_pos_compr_s = s_pre_compr + R * log(pressao_final/pressao_inicial)
    h_pre_compr = estado_antes_compressor.specific_enthalpy


    estado_pos_compressor_s_init = estado('water', 'liq', pressao_final, 40)
    estado_pos_compressor_s = busca_estado('specific_entropy', s_pos_compr_s, 'T', estado_pos_compressor_s_init)

    h_pos_compr_s = estado_pos_compressor_s.specific_enthalpy
    h_pos_compr = symbols('pos_compr')
    fun = (h_pre_compr - h_pos_compr_s) / (h_pre_compr - h_pos_compr) - eficiencia
    sol = solve(fun, h_pos_compr)
    h_pos_compr = sol[0]


    estado_pos_compressor_init = estado('water', 'liq', pressao_final, 40)
    estado_pos_compressor = busca_estado('specific_enthalpy', h_pos_compr, 'T', estado_pos_compressor_init)
    return estado_pos_compressor, estado_pos_compressor_s

# def pros_iter(h4, efic, f_compr):
#     h3, h4s, s4sT, s3T = symbols('h3, h4s, s4sT, s3T')
#     func = (h3 - h4)/(h3 - h4s) - efic
#     Tpalpite = 1000
#
#     Estado3palp = estado('air', 'gas', f_compr*100, Tpalpite)
#
#     h3palp = Estado3palp.specific_enthalpy
#
#     h4spalp = solve(func.subs(h3, h3palp), h4s)
#
#     Estado4palp =
