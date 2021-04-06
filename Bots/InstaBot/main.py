from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from random import randint

class InstagramBot():
    def __init__(self, email, password):
        self.browser = webdriver.Chrome('chromedriver.exe')
        self.email = email
        self.password = password
    def signIn(self):
        self.browser.get('https://www.instagram.com/accounts/login/')
        time.sleep(3)
        emailInput = self.browser.find_elements_by_css_selector('form input')[0]
        passwordInput = self.browser.find_elements_by_css_selector('form input')[1]
        emailInput.send_keys(self.email)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(2)
        buton_not_now = self.browser.find_elements_by_css_selector('button')[-1]
        buton_not_now.click()

        time.sleep(3)
    def get_page(self,link):
        self.browser.get(link)
        time.sleep(1)
        
    def comment(self,com):
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

days = 10
quanti = 250
link = 'https://www.instagram.com/p/B5gW2CJF4J_/'
com = 'instas.txt'



times = 24*60*60/250
times = times//1
arq = open(com, 'r')
com = arq.readlines()
arq.close()

atha = InstagramBot('victor.athanasio@polijunior.com.br','pum12022518')
atha.signIn()
atha.get_page(link)

atha1 = InstagramBot('victorathanasio@usp.br','pum12022518')
atha1.signIn()
atha1.get_page(link)

start_time = time.time()
i = 1
for a in range(1,quanti*days+1):
    comment = com[randint(0, len(com))]
    comment1 = com[randint(0, len(com))]
    atha.comment(comment)
    atha1.comment(comment1)
    elapsed_time = time.time() - start_time
    print(i, elapsed_time)
    i += 1
    atha.get_page('https://www.instagram.com/cristiano/')
    atha.get_page('https://www.instagram.com/victorathanasio/')
    atha.get_page(link)
    atha1.get_page('https://www.instagram.com/cristiano/')
    atha1.get_page('https://www.instagram.com/victorathanasio/')
    atha1.get_page(link)
    t = randint(0,2*times)-25
    print('esperando '+ str(t)+ ' segundos')
    time.sleep(t)

    
    
