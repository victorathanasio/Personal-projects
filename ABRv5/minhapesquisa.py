# %%

from Classes import *
def main():
    # IoTDesignThinking = [
    #     # emerald
    #     #     ['https://www.emerald.com/insight/search?q=IoT+AND+%22Design+Thinking%22&fromYear=2010',100],
    #     #     ['https://www.emerald.com/insight/search?q=IoT+AND+%22Design+Thinking%22&fromYear=2018',50],
    #     # #sci_dir
    #     #     ['https://www.sciencedirect.com/search/advanced?qs=IoT%20AND%20%22Design%20Thinking%22',100],
    #     #     ['https://www.sciencedirect.com/search/advanced?qs=IoT%20AND%20%22Design%20Thinking%22&years=2020%2C2019%2C2018&lastSelectedFacet=years',50],
    #     # #tandf
    #     #     ['https://www.tandfonline.com/action/doSearch?AllField=IoT+AND+%22Design+Thinking%22&content=standard&target=default&queryID=37%2F3008444834&AfterYear=2010&BeforeYear=2020',100],
    #     #     ['https://www.tandfonline.com/action/doSearch?AllField=IoT+AND+%22Design+Thinking%22&content=standard&target=default&queryID=37%2F3008444834&AfterYear=2018&BeforeYear=2020',50],
    #     # #wiley
    #     #     ['https://onlinelibrary.wiley.com/action/doSearch?AllField=IoT+AND+%22Design+Thinking%22&content=articlesChapters&countTerms=true&target=default&AfterYear=2010&BeforeYear=2020',100],
    #     #     ['https://onlinelibrary.wiley.com/action/doSearch?AllField=IoT+AND+%22Design+Thinking%22&content=articlesChapters&countTerms=true&target=default&AfterYear=2018&BeforeYear=2020',50]
    #
    # ]
    # InternetofThingsDesignThinking = [
    #     # emerald
    #     #     ['https://www.emerald.com/insight/search?q=%22Internet+of+Things%22+AND+%22Design+Thinking%22&showAll=true',100],
    #     #     ['https://www.emerald.com/insight/search?q=%22Internet+of+Things%22+AND+%22Design+Thinking%22&showAll=true&fromYear=2018',50],
    #     # #sci_dir
    #     #     ['https://www.sciencedirect.com/search/advanced?qs=%22Internet%20of%20Things%22%20AND%20%22Design%20Thinking%22',100],
    #     #     ['https://www.sciencedirect.com/search/advanced?qs=%22Internet%20of%20Things%22%20AND%20%22Design%20Thinking%22&years=2020%2C2019%2C2018&lastSelectedFacet=years',50],
    #     # #tandf
    #     #     ['https://www.tandfonline.com/action/doSearch?AllField=%22Internet+of+Things%22+AND+%22Design+Thinking%22&content=standard&target=default&queryID=38%2F3008455012&AfterYear=2010&BeforeYear=2020',100],
    #     #     ['https://www.tandfonline.com/action/doSearch?AllField=%22Internet+of+Things%22+AND+%22Design+Thinking%22&AfterYear=2018&BeforeYear=2020',50],
    #     # #wiley
    #     #     ['https://onlinelibrary.wiley.com/action/doSearch?AllField=%22Internet+of+Things%22+AND+%22Design+Thinking%22&content=articlesChapters&countTerms=true&target=default&AfterYear=2010&BeforeYear=2020',100],
    #     #     ['https://onlinelibrary.wiley.com/action/doSearch?AllField=%22Internet+of+Things%22+AND+%22Design+Thinking%22&content=articlesChapters&countTerms=true&target=default&AfterYear=2018&BeforeYear=2020',50]
    #
    # ]
    # IoTUserCentricDesign = [
    #     # emerald
    #     # ['https://www.emerald.com/insight/search?q=%22IoT%22+AND+%22User+Centric+Design%22&showAll=true',100],
    #     # ['https://www.emerald.com/insight/search?q=%22IoT%22+AND+%22User+Centric+Design%22&showAll=true&fromYear=2018',50],
    #     # sci_dir
    #     #     ['https://www.sciencedirect.com/search/advanced?qs=%22IoT%22%20AND%20%22User%20Centric%20Design%22&years=2012%2C2013%2C2014%2C2015%2C2016%2C2017%2C2018%2C2019%2C2020&lastSelectedFacet=years',100],
    #     #     ['https://www.sciencedirect.com/search/advanced?qs=%22IoT%22%20AND%20%22User%20Centric%20Design%22&years=2018%2C2019%2C2020&lastSelectedFacet=years',50],
    #     # #tandf
    #     #     ['https://www.tandfonline.com/action/doSearch?AllField=IoT+AND+%22User+Centric+Design%22&AfterYear=2010&BeforeYear=2020',100],
    #     #     ['https://www.tandfonline.com/action/doSearch?AllField=%22IoT%22+AND+%22User+Centric+Design%22&AfterYear=2018&BeforeYear=2020',50],
    #     # #wiley
    #     #     ['https://onlinelibrary.wiley.com/action/doSearch?AllField=%22IoT%22+AND+%22User+Centric+Design%22',100],
    #     #     ['https://onlinelibrary.wiley.com/action/doSearch?AllField=%22IoT%22+AND+%22User+Centric+Design%22&content=articlesChapters&countTerms=true&target=default&AfterYear=2018&BeforeYear=2019',50]
    #
    # ]
    # IoTDesignMethodology = [
    #     # emerald
    #     #     ['https://www.emerald.com/insight/search?q=%22IoT%22+AND+%22Design+methodology%22&showAll=true&fromYear=2010',100],
    #     #     ['https://www.emerald.com/insight/search?q=%22IoT%22+AND+%22Design+methodology%22&showAll=true&fromYear=2018',50],
    #     # #sci_dir
    #     #     ['https://www.sciencedirect.com/search/advanced?qs=%22IoT%22%20AND%20%22Design%20methodology%22&lastSelectedFacet=years&years=2020%2C2019%2C2018%2C2017%2C2016%2C2015%2C2014%2C2013%2C2012%2C2011',100],
    #     #     ['https://www.sciencedirect.com/search/advanced?qs=%22IoT%22%20AND%20%22Design%20methodology%22&lastSelectedFacet=years&years=2020%2C2019%2C2018',50],
    #     # tandf
    #     #     ['https://www.tandfonline.com/action/doSearch?AllField=%22IoT%22+AND+%22Design+methodology%22&AfterYear=2010&BeforeYear=2020',100],
    #     #     ['https://www.tandfonline.com/action/doSearch?AllField=%22IoT%22+AND+%22Design+methodology%22&AfterYear=2018&BeforeYear=2020',50],
    #     # #wiley
    #     #     ['https://onlinelibrary.wiley.com/action/doSearch?AllField=%22IoT%22+AND+%22Design+methodology%22&content=articlesChapters&countTerms=true&target=default&AfterYear=2010&BeforeYear=2020',100],
    #     [
    #         'https://onlinelibrary.wiley.com/action/doSearch?field1=AllField&text1=%22IoT%22+AND+%22Design+methodology%22&Ppub=&AfterMonth=&AfterYear=2018&BeforeMonth=&BeforeYear=2020',
    #         50]
    #
    # ]
    # sites_list = IoTDesignThinking + InternetofThingsDesignThinking + IoTUserCentricDesign + IoTDesignMethodology
    continua = True
    sites_list = []
    while continua:
        site_ = input('Entre o site, deixe em branco para iniciar pesquisa')
        numero = input('Quantos artigos deseja?')
        if numero != '':
            numero = int(numero)
        if site_ == '':
            print('false')
            continua = False
        site_ = [site_, numero]
        sites_list.append(site_)
    sites_list = sites_list[:-1]
    i = 0
    for url in sites_list:
        print(url)
        i += 1
        print(
            '---------------------------------------------------------------------------------------------------------')
        print(i)
        print(
            '---------------------------------------------------------------------------------------------------------')
        site(url[0], url[1])


# %%

dfs = []


def site(link, Number):
    global dfs

    if 'tandfonline' in link:
        print('tandfonline')
        a = taylor(link, Number)
        a.run()
    elif 'emerald' in link:
        print('emerald')
        a = emerald(link, Number)
        a.run()
    elif 'sciencedirect' in link:
        print('sciencedirect')
        a = sci_dir(link, Number)
        a.run()
    elif 'wiley' in link:
        print('wiley')
        a = wiley(link, Number)
        a.run()
    dfs.append(a)


# %%

main()

# %%

save = dfs

# %%

dfs_for_real = []
for a in dfs:
    dfs_for_real.append(a.df)

df = pd.concat(dfs_for_real)
df.to_excel('pesquisa_selenium.xlsx', index=False)

import Tratamento_de_dados