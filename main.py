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
    driver.switch_to.window(driver.window_handles[1])

    # Banner - Open Time Sheet
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id____UID5"]/div/div/div'))).click()

    # Banner - Enter Time Sheet Hours
    y = 6
    for i in range(number_of_segments):
        # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="contentHolder"]/div[2]/table[1]/tbody/tr[5]/td/form/table[1]/tbody/tr[2]/td[' + str(y) + ']/p/a'))).click().send_keys(segment_hours[i])
        print('//*[@id="contentHolder"]/div[2]/table[1]/tbody/tr[5]/td/form/table[1]/tbody/tr[2]/td[' + str(y) + ']/p/a')
        print(segment_hours[i])
        y += 1

    # Banner - Collect Data
    time_period = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="contentHolder"]/div[2]/table[1]/tbody/tr[3]/td'))).text
    print(time_period)

    # Outlook
    driver.execute_script("window.open('https://www.google.com');")
    driver.switch_to.window(driver.window_handles[2])
    driver.get('https://outlook.com/louisiana.edu')
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="i0116"]'))).send_keys(credentials.USERNAME + '@louisiana.edu' + Keys.ENTER)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="i0118"]'))).send_keys(credentials.PASSWORD + Keys.ENTER)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="idSIButton9"]'))).click()

    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id__3"]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[3]/div[2]/div/div[3]/div[1]/div/div/div/div[1]/div[1]/div[1]/div[1]/div[1]/div/div/div/div/div[1]/div/div/input'))).send_keys(credentials.RECIPIENT + Keys.TAB)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[3]/div[2]/div/div[3]/div[1]/div/div/div/div[1]/div[1]/div[1]/div[2]/div/div/div/div/div/div[1]/div/div/input'))).send_keys(credentials.USERNAME + '@louisiana.edu' + Keys.TAB)
    users_name = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="O365_MainLink_Me"]/div/div[1]/span'))).text

    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="subjectLine0"]'))).send_keys(users_name + ' Time Sheet Entry' + Keys.TAB)
    #//*[@id="app"]/div/div[2]/div/div/div[3]/div[2]/div/div[3]/div[1]/div/div/div/div[1]/div[2]/div/div
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[3]/div[2]/div/div[3]/div[1]/div/div/div/div[1]/div[2]/div/div'))).send_keys(
        time_period + '\n' +
        str(credentials.HOURS) + '\n\n' +
        users_name + '\n' +
        str(credentials.USERNAME)
    )



    time.sleep(1000)
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

# Time Period XPATH:
#//*[@id="contentHolder"]/div[2]/table[1]/tbody/tr[3]/td

