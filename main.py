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
import math

def auto():
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "none"
    driver = webdriver.Chrome(desired_capabilities=caps)
    driver.set_page_load_timeout(10)
    wait = WebDriverWait(driver, 10)

    # Open Chrome
    driver.get('https://ulink.louisiana.edu')

    # ULink Login
    wait.until(EC.element_to_be_clickable((By.ID, 'username'))).send_keys(credentials.USERNAME)
    wait.until(EC.element_to_be_clickable((By.ID, 'password'))).send_keys(credentials.PASSWORD)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]/div[4]/input'))).click()

    # Travel to Banner
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="layout_33"]/a/span'))).click()
    # window_before = driver.window_handles[0]      COMMENTED BECAUSE IM NOT SURE IT'S IMPORTANT
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="portlet_56_INSTANCE_ZJ9sUpbDoQCa"]/div/div/div/div[1]/p/a'))).click()
    window_after = driver.window_handles[1]
    driver.switch_to.window(window_after)

    # Banner - Open Time Sheet
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id____UID5"]/div/div/div'))).click()

    y = 6
    for i in range(number_of_segments):
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="contentHolder"]/div[2]/table[1]/tbody/tr[5]/td/form/table[1]/tbody/tr[2]/td[' + str(y) + ']/p/a'))).click()
        y += 1

    time.sleep(10)
    driver.quit()

def segments(HOURS):
    number_of_segments = math.ceil(HOURS / 20)
    segment_hours = []

    x = 0
    for i in range(number_of_segments):
        x += 20
        if x <= HOURS:
            segment_hours.append(20)
        else:
            segment_hours.append(HOURS % 20)
    
    return segment_hours, number_of_segments

#---main---
# HOURS = int(input('Enter hours worked: '))
HOURS = credentials.HOURS
segment_hours, number_of_segments = segments(HOURS)

auto()

# Hour Segment Initial Click:
#//*[@id="contentHolder"]/div[2]/table[1]/tbody/tr[5]/td/form/table[1]/tbody/tr[2]/td[6]/p/a
#//*[@id="contentHolder"]/div[2]/table[1]/tbody/tr[5]/td/form/table[1]/tbody/tr[2]/td[7]/p/a

