from selenium import webdriver
import time
import credentials
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def auto():
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "none"
    driver = webdriver.Chrome(desired_capabilities=caps)
    # driver = webdriver.Chrome()
    driver.set_page_load_timeout(10)

    
    driver.get('https://ulink.louisiana.edu')
    time.sleep(5)
    driver.find_element_by_id('username').send_keys(credentials.USERNAME)
    driver.find_element_by_id('password').send_keys(credentials.PASSWORD)
    time.sleep(5)
    element = driver.find_element_by_xpath('//*[@id="loginForm"]/div[4]/input')
    time.sleep(5)
    element.click()


    time.sleep(10)
    driver.quit()

#---main---
auto()

#Time Entry Button XPATH:
#//*[@id="layout_33"]/a