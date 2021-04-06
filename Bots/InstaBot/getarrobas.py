from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class getinstas():
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
        time.sleep(3)
        btn_segui = self.browser.find_elements_by_class_name('sqdOP')[2]
        print(btn_segui.text)
        print(btn_segui.tag_name)
        btn_segui.click()
        
        scr1 = self.browser.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]')
        for a in range(100):
            self.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scr1)
        time.sleep(20)

atha = getinstas('victorathanasio@icloud.com','pum12022518')
atha.signIn()
atha.get_page('https://www.instagram.com/p/B5iI4Sag0qQ/')