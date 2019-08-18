from selenium import webdriver
import time
import credentials

driver = webdriver.Chrome()

def auto():
    driver.get('https://ulink.louisiana.edu')
    driver.find_element_by_id('username').send_keys(credentials.USERNAME)
    driver.find_element_by_id('password').send_keys(credentials.PASSWORD)
    driver.find_element_by_xpath('//*[@id="loginForm"]/div[4]/input').click()
    driver.find_element_by_class_name('body').send_keys(ESCAPE)
    driver.find_element_by_xpath('//*[@id="layout_33"]/a').click()
    
    time.sleep(15)
    driver.close()

#---main---
auto()