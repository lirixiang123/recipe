from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--headless')
chromedriver = r"C:\Users\86132\AppData\Local\Google\Chrome\Application\chromedriver.exe"
browser=webdriver.Chrome(chromedriver,chrome_options=chrome_options)
try:
    url = 'https://music.163.com/#/search/m/?s=%E9%A3%9E&type=1'
    browser.get(url)
    browser.switch_to.frame('g_iframe')
    input=browser.find_element_by_id('m-search-input')
    print(input)
    #
finally:
    browser.close()
