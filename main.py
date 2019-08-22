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
    driver.set_page_load_timeout(10)
    wait = WebDriverWait(driver, 10)

    driver.get('https://ulink.louisiana.edu')

    wait.until(EC.element_to_be_clickable((By.ID, 'username'))).send_keys(credentials.USERNAME)

    wait.until(EC.element_to_be_clickable((By.ID, 'password'))).send_keys(credentials.PASSWORD)

    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]/div[4]/input'))).click()

    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="layout_33"]/a/span'))).click()

    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="portlet_56_INSTANCE_ZJ9sUpbDoQCa"]/div/div/div/div[1]/p/a'))).click()

    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id____UID5"]/div/div/div'))).click()

    time.sleep(15)
    driver.quit()

#---main---
auto()

#//*[@id="id____UID5"]/div/div/div