from selenium import webdriver
import time
import credentials

driver = webdriver.Chrome()

def auto():
    driver.get('https://ulink.louisiana.edu')
    driver.find_element_by_id('username').send_keys(credentials.USERNAME)
    driver.find_element_by_id('password').send_keys(credentials.PASSWORD)
    driver.find_element_by_xpath('//*[@id="loginForm"]/div[4]/input').click()
    driver.get('https://ssb-prod.ec.louisiana.edu/ssomanager/c/SSB?pkg=bwpktais.P_SelectTimeSheetRoll')
    
    time.sleep(15)
    driver.quit()

#---main---
auto()