#%%

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandasql as ps

#%%

# le excel
pesquisa = pd.read_excel('pesquisa_selenium.xlsx')
print('O formato da pesquisa quando entra é:', pesquisa.shape)
pesquisa = pesquisa[pesquisa['Authors'].notnull()]
pesquisa = pesquisa[pesquisa['Abstract'] != 'None']
pesquisa = pesquisa[pesquisa['Authors'] != 'None']
pesquisa = pesquisa[pesquisa['Keywords'] != 'None']
pesquisa = pesquisa.astype(str)
print('O formato da pesquisa após retirada de autores, abstracts e keywords nulos é:', pesquisa.shape)

pesquisa_sem_dupli = pesquisa.drop_duplicates(subset='Link', keep="first")
print('O formato da pesquisa após retirada de duplicatas:', pesquisa_sem_dupli.shape)


#%%

def contagem_modular(campo, df, separator):
    splited = df[campo].str.split(separator, expand=True)
    colum_form = splited[0]
    for a in range(1, len(splited.columns)):
        colum_form = pd.concat([colum_form, splited[a]])
    colum_form = colum_form.to_frame()
    colum_form = colum_form[colum_form[0] != 'None']
    colum_form = colum_form[colum_form[0] != ' ']
    colum_form = colum_form[colum_form[0] != '']
    colum_form = colum_form[colum_form[0].notnull()]
    colum_form[0] = colum_form[0].apply(Normalize)
    if campo == 'Keywords':
        colum_form[0] = colum_form[0].apply(low)
    colum_form_noreps = colum_form.drop_duplicates(keep="first")
    colum_form_noreps['Contagem'] = colum_form_noreps[0].map(colum_form[0].value_counts())
    return colum_form_noreps.sort_values(['Contagem'], ascending=[False])


def Normalize(x):
    for i in range(4):
        while x[0] == ' ':
            x = x[1:]
        while x[0] == ';':
            x = x[1:]
        while x[-1] == ' ':
            x = x[:-1]
        while x[-1] == ';':
            x = x[:-1]
    return x


def low(string):
    return string.lower()


#%%

analises = []

cont_autores = contagem_modular('Authors', pesquisa, ';')
cont_autores = cont_autores.rename(columns={0: 'Authors'})
cont_autores_sem_rep = contagem_modular('Authors', pesquisa_sem_dupli, ';')
cont_autores_sem_rep = cont_autores_sem_rep.rename(columns={0: 'Authors sem duplicatas'})

cont_Keywords = contagem_modular('Keywords', pesquisa, ';')
cont_Keywords = cont_Keywords.rename(columns={0: 'Keywords'})
cont_Keywords_sem_rep = contagem_modular('Keywords', pesquisa_sem_dupli, ';')
cont_Keywords_sem_rep = cont_Keywords_sem_rep.rename(columns={0: 'Keywords sem duplicatas'})

cont_Periodic = contagem_modular('Periodic', pesquisa, ';')
cont_Periodic = cont_Periodic.rename(columns={0: 'Periodic'})
cont_Periodic_sem_rep = contagem_modular('Periodic', pesquisa_sem_dupli, ';')
cont_Periodic_sem_rep = cont_Periodic_sem_rep.rename(columns={0: 'Periodic sem duplicatas'})

cont_Plataforma = contagem_modular('Plataforma', pesquisa, ';')
cont_Plataforma = cont_Plataforma.rename(columns={0: 'Plataforma'})
cont_Plataforma_sem_rep = contagem_modular('Plataforma', pesquisa_sem_dupli, ';')
cont_Plataforma_sem_rep = cont_Plataforma_sem_rep.rename(columns={0: 'Plataforma sem duplicatas'})

cont_Year = contagem_modular('Year', pesquisa, ';')
cont_Year = cont_Year.rename(columns={0: 'Year'})
cont_Year_sem_rep = contagem_modular('Year', pesquisa_sem_dupli, ';')
cont_Year_sem_rep = cont_Year_sem_rep.rename(columns={0: 'Year sem duplicatas'})

analises.append(cont_autores)
analises.append(cont_autores_sem_rep)
analises.append(cont_Keywords)
analises.append(cont_Keywords_sem_rep)
analises.append(cont_Periodic)
analises.append(cont_Periodic_sem_rep)
analises.append(cont_Plataforma)
analises.append(cont_Plataforma_sem_rep)
analises.append(cont_Year)
analises.append(cont_Year_sem_rep)

pesquisa_sem_dupli['Contagem'] = pesquisa_sem_dupli['Link'].map(pesquisa['Link'].value_counts())
pesquisa_sem_dupli = pesquisa_sem_dupli.sort_values(['Contagem'], ascending=[False])

#%% graficos

for df in analises[-2:]:
    name = df.columns[0]
    df.set_index(df.columns[0], inplace=True)
    df.sort_index(inplace=True)
    df = df.astype(int)
    df = df.rename(columns={'Year':'Ano'})
    df.index.name = df.index.name.replace('Year', 'Ano')
    a = df.plot.line(title='Artigos por ano', figsize=(12, 6))

    fig = a.get_figure()
    fig.savefig('wordcloud/' + name + 'pandas')


#%% pizza charts

for df in analises[-4:-2]:
    name = df.columns[0]
    df.set_index(df.columns[0], inplace=True)
    df.sort_index(inplace=True)
    df = df.astype(int)
    a = df.plot.pie(title='Artigos por plataforma', y='Contagem', figsize=(10, 8), autopct='%1.1f%%',
                    shadow=True, startangle=90)
    fig = a.get_figure()
    fig.savefig('wordcloud/' + name + 'pandas')

#%%wordclouds

for df in analises:
    df.reset_index(inplace=True)
    try:
        df = df.drop(columns=['index'])
    except:
        pass
    tuples = [tuple(x) for x in df.values]
    wordcloud = WordCloud(width=900, height=400, max_words=100).generate_from_frequencies(dict(tuples))
    plt.figure(figsize=(20, 10))
    #plt.suptitle(df.columns[0], fontsize=25)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig('wordcloud/' + df.columns[0])

#%% artigos relevantes

# 2 vezes
cont_x = 1
# top 50
cont_top = 50
# autores que aparecem 2 vezes ou mais cont_aut
cont_aut = 2
cont_key = 6
pesquisa_sem_dupli['Contagem'] = pesquisa_sem_dupli['Contagem'].astype(int)
pesquisa_sem_dupli['Year'] = pesquisa_sem_dupli['Year'].astype(int)
pesquisa_sem_dupli['Relevancia'] = pesquisa_sem_dupli['Relevancia'].astype(int)
art_relevant = pesquisa_sem_dupli[pesquisa_sem_dupli['Contagem'] >= cont_x]


def checa_autor(autores):
    autores_list = autores.values
    saida = []
    for autores in autores_list:
        autores = autores.split(';')
        check = False
        for autor in autores:
            if autor != ' ':
                autor = Normalize(autor)
            row = cont_autores_sem_rep[cont_autores_sem_rep['Authors sem duplicatas'] == autor]
            try:
                contagem = row['Contagem'].values[0]
            except:
                contagem = 0
            if contagem >= cont_aut:
                check = True
        if check:
            saida.append(True)
        else:
            saida.append(False)
    return saida

def checa_key(key):
    keys_list = key.values
    saida = []
    for keys in keys_list:
        keys = keys.split(';')
        check = False
        for key in keys:
            if key != ' ':
                key = Normalize(key).lower()
            row = cont_Keywords_sem_rep[cont_Keywords_sem_rep['Keywords sem duplicatas'] == key]
            try:
                contagem = row['Contagem'].values[0]
            except:
                contagem = 0
            if contagem >= cont_key:
                check = True
        if check:
            saida.append(True)
        else:
            saida.append(False)
    return saida

art_relevant = art_relevant[art_relevant['Relevancia'] <= cont_top]
art_relevant = art_relevant[checa_autor(art_relevant['Authors'])]
art_relevant = art_relevant[checa_key(art_relevant['Keywords'])]

#%%



#%% Grafico de todos os termos juntos

pesquisa_sem_dupli['Termo'] = pesquisa_sem_dupli['Termo'].str.replace('anywhere','')
pesquisa_sem_dupli['Termo'] = pesquisa_sem_dupli['Termo'].str.replace('"','')
pesquisa_sem_dupli['Termo'] = pesquisa_sem_dupli['Termo'].apply(Normalize)



q1 = """SELECT Termo FROM pesquisa_sem_dupli GROUP BY Termo"""

termos = ps.sqldf(q1, locals())



dfs = []
for i in range(len(termos.Termo)):
    termo = termos.Termo[i]
    print(termo)
    q1 = """SELECT Year, Count(*) FROM pesquisa_sem_dupli WHERE Termo = '{}' GROUP BY Year""".format(termo)
    frame = ps.sqldf(q1, locals())
    frame = frame.rename(columns={'Count(*)': termo, 'Year':'Ano'})
    name = frame.columns[0]
    frame.set_index(frame.columns[0], inplace=True)
    frame.sort_index(inplace=True)
    dfs.append(frame)

# q1 = """SELECT Year , Count(*) FROM pesquisa_sem_dupli GROUP BY Year"""
# total = ps.sqldf(q1, locals())
# total = total.rename(columns={'Count(*)': 'Total'})
# name = total.columns[0]
# total.set_index(total.columns[0], inplace=True)
# total.sort_index(inplace=True)
# dfs.append(total)

df_master = dfs[0]
# df_master.loc[2012] = 0
# for i in range(4):
#     if i != 2:
#         df = dfs[i]
#         df_master[df.columns[-1]] = df[df.columns[-1]]
#         print(df.columns[-1])




df_master.sort_index(inplace=True)
a = df_master.plot.line(title=name, figsize=(12, 6))
fig = a.get_figure()
fig.savefig('wordcloud/time_series_termos')

#%%

# art_relevant_latex = art_relevant[['Title','Link']]
#
# #%%
#
# art_relevant_latex.to_latex('principais.tex',column_format='p{8cm}p{13cm}',index=False,label='table:Principais',longtable=False, escape=False)

#%%



#%%

writer = pd.ExcelWriter('resultado_analise.xlsx', engine='xlsxwriter')
workbook = writer.book

worksheet = workbook.add_worksheet('Resultado consolidado')
writer.sheets['Resultado consolidado'] = worksheet
pesquisa_sem_dupli.to_excel(writer, sheet_name='Resultado consolidado', startrow=0, startcol=0, index=False)

worksheet = workbook.add_worksheet('Artigos mais relevantes')
writer.sheets['Artigos mais relevantes'] = worksheet
art_relevant.to_excel(writer, sheet_name='Artigos mais relevantes', startrow=0, startcol=0, index=False)


def escreve_contagens(cont, cont_sem_rep, analise):
    worksheet = workbook.add_worksheet(analise)
    writer.sheets[analise] = worksheet
    worksheet.write_string(0, 0, analise)
    cont.to_excel(writer, sheet_name=analise, startrow=1, startcol=0, index=False)

    worksheet.write_string(0, 3, analise + 'após exclusão dos artigos repetidos')
    cont_sem_rep.to_excel(writer, sheet_name=analise, startrow=1, startcol=3, index=False)


escreve_contagens(cont_autores, cont_autores_sem_rep, 'Contagem dos autores ')
escreve_contagens(cont_Keywords, cont_Keywords_sem_rep, 'Contagem dos keywords ')
escreve_contagens(cont_Periodic, cont_Periodic_sem_rep, 'Contagem por periodico ')
escreve_contagens(cont_Plataforma, cont_Plataforma_sem_rep, 'Contagem por plataforma ')
escreve_contagens(cont_Year, cont_Year_sem_rep, 'Contagem por ano ')
writer.save()


#%%

titles_mais_rel = pd.read_excel('Resultado_analise_final.xlsx')

#%%
titulos_list = titles_mais_rel['Titulos'].to_list()
q1 = """SELECT * FROM pesquisa_sem_dupli WHERE Title LIKE '%{}%'""".format(titulos_list[0][5:-5])
df =  ps.sqldf(q1, locals())


for titulo in titulos_list[1:]:
    q1 = """SELECT * FROM pesquisa_sem_dupli WHERE Title LIKE '%{}%'""".format(titulo[5:-5])
    art = ps.sqldf(q1, locals())
    df = df.append(art)
df = df.reset_index().drop(columns=['index'])
#%%
df_campos = pd.DataFrame()
df_campos['Título'] = df['Title']#,'Year','Authors']
df_campos['Autores'] = df['Authors']
df_campos['Ano'] = df['Year']


#%%

writer = pd.ExcelWriter('Resultado_analise_final.xlsx', engine='xlsxwriter')
workbook = writer.book

worksheet = workbook.add_worksheet('Titulos_principais')
writer.sheets['Titulos_principais'] = worksheet
titles_mais_rel.to_excel(writer, sheet_name='Titulos_principais', startrow=0, startcol=0, index=False)

worksheet = workbook.add_worksheet('Artigos_principais')
writer.sheets['Artigos_principais'] = worksheet
df.to_excel(writer, sheet_name='Artigos_principais', startrow=0, startcol=0, index=False)

worksheet = workbook.add_worksheet('Tabela')
writer.sheets['Tabela'] = worksheet
df_campos.to_excel(writer, sheet_name='Tabela', startrow=0, startcol=0, index=False)
writer.save()

#%%
ciations = []
labels = []

def create_bibtex(journal,authors,year,link,title):


    authors_ = ''
    authors = authors.split(';')
    for i in range(len(authors)):
        author = authors[i].split('.')
        for j in range(len(author)):
            author[j] = author[j].split()
            for k in range(len(author[j])):
                author[j][k] = Normalize(author[j][k])
        author_ = []
        for x in author:
            author_ += x
        if len(author_)>0:
            name = author_[-1]
            surnames = author_[:-1]
            surnames_ = ''
            for i in range(len(surnames)):
                surnames[i] = surnames[i][0] + '. '
                surnames_ += surnames[i]
            surnames_ = surnames_[:-1] + ';'
            name += ', '
            autor_ = name + surnames_
            authors_ += autor_
    authors_ = authors_[:-1].upper()
    label = authors_.split(',')[0]
    if label in labels:
        label += '2'
    if label in labels:
        label = label[:-1] + '3'


    citation = '''@article{{{},
    author={{{}}},
    title={{{}}},
    year={{{}}},
    url = {{{}}},
    journal = {{{}}},
    urlaccessdate={{junho de 2020}}}}
    '''.format(label, authors_, title, year,link,journal)
    ciations.append(citation)
    labels.append(label)


df.apply(lambda x: create_bibtex(x.Periodic , x.Authors, x.Year, x.Link, x.Title), axis=1)
#%%
for citation in ciations:
    print(citation)
#%%
notice = ''
for label in labels:
    notice += label + ', '

print(notice)


