from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import pickle
from selenium.webdriver.common.by import By
from random import randint
import threading
import concurrent.futures


class InstagramBot():
    def __init__(self, email, password):
        self.browser = webdriver.Chrome('chromedriver.exe')
        self.email = email
        self.password = password

    def signIn(self):
        self.browser.get('https://www.instagram.com/accounts/login/')
        time.sleep(2)
        emailInput = self.browser.find_elements_by_css_selector('form input')[0]
        passwordInput = self.browser.find_elements_by_css_selector('form input')[1]
        emailInput.send_keys(self.email)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(2)
        buton_not_now = self.browser.find_elements_by_css_selector('button')[-1]
        buton_not_now.click()

        time.sleep(0.5)

    def get_page(self, link):
        self.browser.get(link)
        time.sleep(1)

    def comment(self, com):
        element = self.browser.find_element_by_css_selector('textarea')
        element.click()
        time.sleep(2)
        element = self.browser.find_element_by_css_selector('textarea')
        element.send_keys(com)
        time.sleep(2)
        element = self.browser.find_element_by_css_selector('textarea')
        element.send_keys(Keys.ENTER)
        time.sleep(2)
        element = self.browser.find_element_by_css_selector('textarea')
        element.send_keys(Keys.ENTER)
        time.sleep(2)
        element = self.browser.find_element_by_css_selector('textarea')
        element.send_keys(Keys.ENTER)
        time.sleep(2)
        element = self.browser.find_element_by_css_selector('textarea')
        element.send_keys(Keys.ENTER)
        time.sleep(2)


def Bot_comment(L):
    bot = L[0]
    comment = L[1]
    link = 'https://www.instagram.com/p/B7hX92Fgj1f/'
    bot.get_page(link)
    bot.comment(comment)
    bot.get_page('https://www.instagram.com/cristiano/')
    bot.get_page('https://www.instagram.com/victorathanasio/')
    bot.get_page(link)


def main():
    # comments
    com = 'instas.txt'
    arq = open(com, 'r')
    com = arq.readlines()
    arq.close()

    # accounts
    bots = []
    bots.append(['victorathanasio@usp.br', 'pum12022518'])check
    bots.append(['victor.athanasio@polijunior.com.br', 'pum12022518'])not
    bots.append(['victorathanasio@icloud.com', 'Pum12022518'])check
    bots.append(['victor_alexandre_2000@hotmail.com', 'Pum12022518'])check
    bots.append(['victorathanasio', 'Givilata_12022518'])check

    for a in range(len(bots)):
        bots[a] = [InstagramBot(bots[a][0], bots[a][1]), '']
        bots[a][0].signIn()
        save_cookies(bots[a], bots[a].email + '.txt')


def save_cookies(driver, name):
    pickle.dump(driver.get_cookies(), open(name, "wb"))


def load_cookies(driver, name, url=None):
    cookies = pickle.load(open(name, "rb"))
    driver.delete_all_cookies()
    # have to be on a page before you can add any cookies, any page - does not matter which
    driver.get("https://google.com" if url is None else url)
    for cookie in cookies:
        if 'expiry' in cookie:
            del cookie['expiry']
        driver.add_cookie(cookie)

    # #parameters
    # days = 7
    # quanti = 200
    # times = 24*60*60/quanti
    # times = times//1
    # i = 1
    # start_time = time.time()
    #
    # #loop
    # for a in range(1,quanti*days+1):
    #     for bot in bots:
    #         bot[1] = com[randint(0, len(com))]
    #
    #     with concurrent.futures.ThreadPoolExecutor(max_workers=len(bots)) as executor:
    #         executor.map(Bot_comment, bots)
    #
    #
    #     elapsed_time = time.time() - start_time
    #     print(i, elapsed_time)
    #     i += 1
    #     t = randint(0,2*times)
    #
    #
    #     print('esperando '+ str(t)+ ' segundos')
    #     time.sleep(t)


main()
