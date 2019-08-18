from selenium import webdriver
import time
import credentials
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()

def auto():
    driver.get('https://ulink.louisiana.edu')
    driver.find_element_by_id('username').send_keys(credentials.USERNAME)
    driver.find_element_by_id('password').send_keys(credentials.PASSWORD)

    driver.find_element_by_xpath('//*[@id="loginForm"]/div[4]/input').click()
    driver.find_element_by_tag_name('body').send_keys("Keys.ESCAPE")

    driver.find_element_by_class_name('item6').click()
    
    time.sleep(5)
    driver.quit()

#---main---
auto()

#Time Entry Button XPATH:
#//*[@id="layout_33"]/a