from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import re
from selenium.webdriver.common.action_chains import ActionChains

Visu = False


class sci_dir():
    def __init__(self, link, Number):
        # threading.Thread.__init__(self)
        self.Number = Number
        options = Options()
        global Visu
        options.add_argument("user-data-dir=selenium")
        options.headless = Visu
        options.add_argument("window-size=700,1000")
        self.browser = webdriver.Chrome('chromedriver.exe', options=options)
        self.browser.get(link)
        time.sleep(2)
        self.goal = Number
        total_articles = self.browser.find_elements_by_class_name('search-body-results-text')
        total_articles = float(total_articles[0].text.split()[0].replace(',', '.'))
        if total_articles < self.goal:
            self.goal = total_articles
            print('Only {} articles available'.format(total_articles))
        self.termo = self.browser.find_element_by_class_name('search-input-field').get_attribute('value')
        self.df = pd.DataFrame(
            columns=['Abstract', 'Authors', 'Keywords', 'Link', 'Periodic', 'Plataforma', 'Termo', 'Title', 'Year'])

    def _get_articles(self):
        fim = False
        while self.df.shape[0] < self.goal:
            print('sorting articles')
            temp = self.browser.find_elements_by_class_name('ResultItem')
            if len(temp) >= int(self.goal - self.df.shape[0]):
                temp = temp[:int(self.goal - self.df.shape[0])]
                fim = True
            for article in temp:
                row = self._get_article_preview(article)
                self.df = self.df.append(row, ignore_index=True)
            if not fim:
                self._next_page()
            time.sleep(1)

    def _next_page(self):
        next_btn = self.browser.find_elements_by_tag_name('span')
        next_btn = next_btn[-15:]
        result = 0
        for span in next_btn:
            if span.text == 'next':
                result = span
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            result.click()
        except:
            self._next_page()

    def _get_article_preview(self, article):
        try:
            Periodic = article.find_element_by_class_name('SubType').find_element_by_tag_name('span').text
            Link = article.find_element_by_tag_name('a').get_attribute('href')
        except:
            return self._get_article_preview(article)
        return {'Link': Link,
                'Periodic': Periodic}

    def _articles(self):
        i0 = self.df.index.values.tolist()[0]
        for i in self.df.index.values.tolist():
            self.browser.get(self.df['Link'][i])
            time.sleep(1)
            try:
                self.df['Abstract'][i] = self.browser.find_element_by_class_name('abstract').text
            except:
                self.df['Abstract'][i] = 'None'
            authors = self.browser.find_elements_by_class_name('author')
            Authors = ''
            for author in authors:
                if len(author.find_elements_by_class_name('surname')) > 0:
                    name = author.find_element_by_class_name('given-name').text
                    surname = author.find_element_by_class_name('surname').text
                    author = name + ' ' + surname + '; '
                    Authors += author
            self.df['Authors'][i] = Authors
            try:
                Keywords = ''
                keywords = self.browser.find_element_by_class_name('Keywords').find_element_by_tag_name(
                    'div').find_elements_by_tag_name('div')
                for keyword in keywords:
                    Keywords += keyword.text + '; '
            except:
                Keywords = 'None'
            self.df['Keywords'][i] = Keywords
            try:
                Title = self.browser.find_element_by_class_name('title-text').text
            except:
                Title = 'None'
            self.df['Title'][i] = Title
            try:
                year = self.browser.find_element_by_class_name('Publication')
                year = year.find_element_by_class_name('text-xs').text
                Year = re.findall("\d{4}", year)[0]
            except:
                year = self.browser.find_element_by_class_name('Publication').text
                Year = re.findall("\d{4}", year)[0]
            self.df['Year'][i] = Year
            print(i - i0 + 1, '/', self.df.shape[0])
        self.browser.quit()

    def run(self):
        self._get_articles()
        # self.browser.quit()
        self.df['Termo'] = self.termo
        self.df['Plataforma'] = 'Science Direct'
        self._articles()
        self.df['Relevancia'] = self.df.index
        if self.Number == 100:
            self.df['Ano_inicial'] = 2010
        else:
            self.df['Ano_inicial'] = 2018

class emerald():
    def __init__(self, link, Number):
        # threading.Thread.__init__(self)
        options = Options()
        global Visu
        options.add_argument("user-data-dir=selenium")
        options.headless = Visu
        options.add_argument("window-size=1000,1100")
        self.browser = webdriver.Chrome('chromedriver.exe', options=options)
        self.browser.get(link)
        time.sleep(1)
        self.Number = Number
        self.goal = Number
        total_articles = self.browser.find_elements_by_class_name('intent_searchresultscount')
        total_articles = float(total_articles[0].text.split()[-1])
        if total_articles < self.goal:
            self.goal = total_articles
            print('Only {} articles available'.format(total_articles))
        self.termo = self.browser.find_element_by_class_name('intent_input_query').get_attribute('value')
        self.df = pd.DataFrame(
            columns=['Abstract', 'Authors', 'Keywords', 'Link', 'Periodic', 'Plataforma', 'Termo', 'Title', 'Year'])

    def _get_articles(self):
        fim = False
        while self.df.shape[0] < self.goal:
            print('sorting articles')
            temp = self.browser.find_elements_by_class_name('intent_search_result')
            if len(temp) >= (self.goal - self.df.shape[0]):
                temp = temp[:int(self.goal - self.df.shape[0])]
                fim = True
            for article in temp:
                row = self._get_article_preview(article)
                self.df = self.df.append(row, ignore_index=True)
            if not fim:
                self._next_page()
            time.sleep(1)

    def _next_page(self):

        next_btn = self.browser.find_elements_by_class_name('intent_next_page_link')
        next_btn = next_btn[-1]
        scroll_target = self.browser.find_elements_by_class_name('input-group-text')[-1]
        ActionChains(self.browser).move_to_element(scroll_target).perform()
        try:
            next_btn.click()
        except:
            self._next_page()

    def _get_article_preview(self, article):
        ActionChains(self.browser).move_to_element(article).perform()
        btn = article.find_element_by_class_name('intent_toggle_button')
        btn.click()
        Title = article.find_element_by_class_name('intent_title').text
        authors = article.find_element_by_class_name('my-3').text
        Authors = authors.replace(' and',';').replace(',',';')
        if authors == '':
            Authors = 'None'
        Periodic = article.find_element_by_class_name('intent_publication_title').text.split(',')[0]
        year = article.find_element_by_class_name('intent_publication_date').text
        Year = re.findall("\d{4}", year)[0]
        Abstract = article.find_element_by_class_name('intent_abstract').text
        if Abstract == '':
            Abstract = 'None'
        Link = article.find_element_by_class_name('intent_link').get_attribute('href')
        try:
            keywords = article.find_element_by_class_name('intent_keywords')
            keywords = keywords.find_elements_by_tag_name('li')
            Keywords = ''
            for keyword in keywords:
                Keywords += keyword.text + '; '
        except:
            Keywords = 'None'
        return {'Abstract': Abstract,
                'Authors': Authors,
                'Keywords': Keywords,
                'Link': Link,
                'Periodic': Periodic,
                'Title': Title,
                'Year':Year}

    def run(self):
        self._get_articles()
        self.browser.quit()
        self.df['Termo'] = self.termo
        self.df['Plataforma'] = 'Emerald'
        self.df['Relevancia'] = self.df.index
        self.browser.quit()
        if self.Number == 100:
            self.df['Ano_inicial'] = 2010
        else:
            self.df['Ano_inicial'] = 2018

class wiley():
    def __init__(self, link, Number):
        # threading.Thread.__init__(self)
        options = Options()
        self.Number = Number
        global Visu
        options.add_argument("user-data-dir=selenium")
        options.headless = Visu
        options.add_argument("window-size=1500,800")
        self.browser = webdriver.Chrome('chromedriver.exe', options=options)
        self.browser.get(link)
        time.sleep(1)
        self.goal = Number
        total_articles = self.browser.find_elements_by_class_name('result__count')
        total_articles = float(total_articles[0].text.replace(',','.'))
        if total_articles < self.goal:
            self.goal = total_articles
            print('Only {} articles available'.format(total_articles))
        self.termo = self.browser.find_element_by_class_name('result__suffix').text.replace('"','')
        self.df = pd.DataFrame(
            columns=['Abstract', 'Authors', 'Keywords', 'Link', 'Periodic', 'Plataforma', 'Termo', 'Title', 'Year'])

    def _get_articles(self):
        fim = False
        while self.df.shape[0] < self.goal:
            print('sorting articles')
            temp = self.browser.find_elements_by_class_name('search__item')
            if len(temp) >= (self.goal - self.df.shape[0]):
                temp = temp[:int(self.goal - self.df.shape[0])]
                fim = True
            for article in temp:
                row = self._get_article_preview(article)
                self.df = self.df.append(row, ignore_index=True)
            if not fim:
                self._next_page()
            time.sleep(1)

    def _next_page(self):

        next_btn = self.browser.find_elements_by_class_name('pagination__btn--next')
        next_btn = next_btn[-1]
        ActionChains(self.browser).move_to_element(next_btn).perform()
        try:
            next_btn.click()
        except:
            self._next_page()

    def _get_article_preview(self, article):
        ActionChains(self.browser).move_to_element(article).perform()
        Title = article.find_element_by_class_name('publication_title').text
        authors = article.find_element_by_class_name('meta__authors')
        authors = authors.find_elements_by_class_name('publication_contrib_author')
        Authors = ''
        for author in authors:
            Authors += author.text + '; '
        if Authors == ';':
            Authors = 'None'
        Periodic = article.find_elements_by_class_name('publication_meta_serial')
        if len(Periodic) == 0:
            Periodic = article.find_elements_by_class_name('meta__serial')#. meta__serial
        if len(Periodic) != 0:
            Periodic = Periodic[0].text.split('|')[0]
        else:
            Periodic = 'None'
        year = article.find_element_by_class_name('meta__epubDate').text
        Year = re.findall("\d{4}", year)[0]
        # Abstract = article.find_element_by_class_name('intent_abstract').text
        # if Abstract == '':
        #     Abstract = 'None'
        Link = article.find_element_by_class_name('publication_title').get_attribute('href')
        # try:
        #     keywords = article.find_element_by_class_name('intent_keywords')
        #     keywords = keywords.find_elements_by_tag_name('li')
        #     Keywords = ''
        #     for keyword in keywords:
        #         Keywords += keyword.text + '; '
        # except:
        #     Keywords = 'None'

        return {'Authors': Authors,
                'Link': Link,
                'Periodic': Periodic,
                'Title': Title,
                'Year':Year}

    def _articles(self):
        i0 = self.df.index.values.tolist()[0]
        for i in self.df.index.values.tolist():
            self.browser.get(self.df['Link'][i])
            Abstract = self.browser.find_element_by_class_name('article__body').text
            if Abstract == '':
                Abstract = 'None'

            try:
                time.sleep(1)
                keywords = self.browser.find_element_by_class_name('keywords')
                keywords = keywords.find_elements_by_tag_name('li')
                Keywords = ''
                for keyword in keywords:
                    Keywords += keyword.text + '; '
            except:
                Keywords = 'None'

            print(i - i0 + 1, '/', self.df.shape[0])
            self.df['Abstract'][i] = Abstract
            self.df['Keywords'][i] = Keywords


    def run(self):
        self._get_articles()
        self._articles()
        self.df['Termo'] = self.termo
        self.df['Plataforma'] = 'Wiley'
        self.df['Relevancia'] = self.df.index
        self.browser.quit()
        if self.Number == 100:
            self.df['Ano_inicial'] = 2010
        else:
            self.df['Ano_inicial'] = 2018

class taylor():
    def __init__(self, link, Number):
        # threading.Thread.__init__(self)
        options = Options()
        self.Number = Number
        global Visu
        options.add_argument("user-data-dir=selenium")
        options.headless = Visu
        options.add_argument("window-size=1500,800")
        self.browser = webdriver.Chrome('chromedriver.exe', options=options)
        self.browser.get(link)
        time.sleep(1)
        self.goal = Number
        total_articles = self.browser.find_elements_by_class_name('search-results')[0].find_elements_by_tag_name('strong')[-1]
        total_articles = float(total_articles.text.replace(',','.'))
        if total_articles < self.goal:
            self.goal = total_articles
            print('Only {} articles available'.format(total_articles))
        self.termo = self.browser.find_element_by_class_name('searchText').get_attribute('value')
        self.df = pd.DataFrame(
            columns=['Abstract', 'Authors', 'Keywords', 'Link', 'Periodic', 'Plataforma', 'Termo', 'Title', 'Year'])

    def _get_articles(self):
        fim = False
        while self.df.shape[0] < self.goal:
            print('sorting articles')
            temp = self.browser.find_elements_by_class_name('search-citation')
            if len(temp) >= (self.goal - self.df.shape[0]):
                temp = temp[:int(self.goal - self.df.shape[0])]
                fim = True
            for article in temp:
                row = self._get_article_preview(article)
                self.df = self.df.append(row, ignore_index=True)
            if not fim:
                self._next_page()
            time.sleep(1)

    def _next_page(self):

        next_btn = self.browser.find_elements_by_class_name('paginationArrowSymbol')
        next_btn = next_btn[-1]
        ActionChains(self.browser).move_to_element(next_btn).perform()
        try:
            next_btn.click()
            time.sleep(2)
        except:
            self._next_page()
            time.sleep(2)

    def _get_article_preview(self, article):
        ActionChains(self.browser).move_to_element(article).perform()
        Title = article.find_element_by_class_name('hlFld-Title').text
        authors = article.find_element_by_class_name('author').text
        Authors = authors.replace(' ,',';')
        Authors = authors.replace(',',';')
        Authors = Authors.replace(' &',';')
        # authors = authors.find_elements_by_class_name('publication_contrib_author')
        # Authors = ''
        # for author in authors:
        #     Authors += author.text + '; '
        if Authors == '':
            Authors = 'None'
        Periodic = article.find_elements_by_class_name('searchResultJournal')[0].text
        # if len(Periodic) == 0:
        #     Periodic = article.find_elements_by_class_name('meta__serial')#. meta__serial
        if Periodic == '':
            Periodic = 'None'
        year = article.find_element_by_class_name('publication-year').text
        Year = re.findall("\d{4}", year)[0]
        # Abstract = article.find_element_by_class_name('intent_abstract').text
        # if Abstract == '':
        #     Abstract = 'None'
        Link = article.find_element_by_class_name('nowrap').get_attribute('href')
        # try:
        #     keywords = article.find_element_by_class_name('intent_keywords')
        #     keywords = keywords.find_elements_by_tag_name('li')
        #     Keywords = ''
        #     for keyword in keywords:
        #         Keywords += keyword.text + '; '
        # except:
        #     Keywords = 'None'

        return {'Authors': Authors,
                'Link': Link,
                'Periodic': Periodic,
                'Title': Title,
                'Year':Year}

    def _articles(self):
        i0 = self.df.index.values.tolist()[0]
        for i in self.df.index.values.tolist():
            self.browser.get(self.df['Link'][i])
            time.sleep(1)
            Abstract = self.browser.find_element_by_class_name('hlFld-Abstract').text
            if Abstract == '':
                Abstract = 'None'

            try:
                time.sleep(1)
                keywords = self.browser.find_element_by_class_name('hlFld-KeywordText').text
                keywords = keywords.replace('Keywords: ', '')
                keywords = keywords.replace('KEYWORDS:', '')
                keywords = keywords.replace('Key Words:', '')
                Keywords = keywords.replace(',', ';')
            except:
                Keywords = 'None'

            print(i - i0 + 1, '/', self.df.shape[0])
            self.df['Abstract'][i] = Abstract
            self.df['Keywords'][i] = Keywords


    def run(self):
        self._get_articles()
        self._articles()
        self.df['Termo'] = self.termo
        self.df['Plataforma'] = 'Taylor and Francis'
        self.df['Relevancia'] = self.df.index
        self.browser.quit()
        if self.Number == 100:
            self.df['Ano_inicial'] = 2010
        else:
            self.df['Ano_inicial'] = 2018

