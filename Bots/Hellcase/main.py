# %%
import pickle
from selenium import webdriver

''''
Contas:
'atha.txt'

'''


# %%
class Hellcase():
    def __init__(self, account):
        self.chrome = webdriver.Chrome()
        load_cookies(self.chrome, account)

    def get_daily_hellcase(self):
        self.chrome.get("https://hellcase.com/en/dailyfree")
        getbtn = self.chrome.find_element_by_class_name('hellcase-btn-success')
        getbtn.click()

    def get_daily_key_drop(self):
        self.chrome.get("https://key-drop.pl/Codzienna_skrzynka")
        getbtn = self.chrome.find_element_by_class_name('js-loser-open-btn')
        getbtn.click()


# %%
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


# %%

meu = Hellcase('atha.txt')
meu.get_daily_hellcase()
# %%


# %%



