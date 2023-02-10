import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
import os

chrome_path = os.path.join(
    r'H:\pyproj\learn_python\my_py\pixiv\driver\chromedriver.exe'
)
chrome_options = Options()  # Headless　設定
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

option = ChromeOptions()  # Chromedriver の設定
option.add_experimental_option('excludeSwitches', ['enable-automation'])
bro = webdriver.Chrome(executable_path=chrome_path,
                       chrome_options=chrome_options, options=option)


def get_cookie(username, password) -> str:  # seleniumを使って、cookieをGET
    url = 'https://accounts.pixiv.net/login'

    bro.get(url)
    user_tag = bro.find_element(by=By.XPATH,
                                value='//fieldset[1]//input')
    user_tag.send_keys(username)
    time.sleep(random.choice([0.4, 0.5, 0.6, 0.7]))
    pass_tag = bro.find_element(by=By.XPATH,
                                value='//fieldset[2]//input')
    pass_tag.send_keys(password)
    time.sleep(random.choice([0.3, 0.4, 0.5, 0.6]))
    bro.find_element(by=By.XPATH,
                     value='//form//button').click()
    # wait = WebDriverWait(bro, 30)
    # wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="g-recaptcha-response-100000"]')))
    time.sleep(2.5)
    cookie_item = bro.get_cookies()  # Cookieを獲得
    cookie_str = ''

    for item_cookie in cookie_item:  # dict cookie
        item_str = item_cookie["name"] + "=" + item_cookie["value"] + ";"
        cookie_str += item_str
    bro.quit()
    return cookie_str
