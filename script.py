import credentials

import time
import math

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def selenium_script():
    # Browser Config
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "none"
    driver = webdriver.Chrome(desired_capabilities=caps, chrome_options=options)
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
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="portlet_56_INSTANCE_ZJ9sUpbDoQCa"]/div/div/div/div[1]/p/a'))).click()
    driver.switch_to.window(driver.window_handles[1])

    # Banner - Open Time Sheet
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id____UID5"]/div/div/div'))).click()

    # Banner - Enter Time Sheet Hours
    y = 7
    for i in range(credentials.number_of_segments):
        if i == 0:
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="contentHolder"]/div[2]/table[1]/tbody/tr[5]/td/form/table[1]/tbody/tr[2]/td[' + str(y) + ']/p/a'))).click()
        else:
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="contentHolder"]/div[2]/table[1]/tbody/tr[6]/td/form/table[1]/tbody/tr[2]/td[' + str(y) + ']/p/a'))).click()

        wait.until(EC.element_to_be_clickable((By.ID, 'hours_id'))).send_keys(str(credentials.segment_hours[i]))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id____UID5"]/div/div/div'))).click()
        y += 1

    # Banner - Collect Data
    time_period = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="contentHolder"]/div[2]/table[1]/tbody/tr[3]/td'))).text

    # Submit Time Sheet For Approval
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id____UID11"]/div/div/div'))).click()
    # print('Submitted!')

    # Outlook - Sign In
    driver.execute_script("window.open('https://www.google.com');")
    driver.switch_to.window(driver.window_handles[2])
    driver.get('https://outlook.com/louisiana.edu')
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="i0116"]'))).send_keys(credentials.USERNAME + '@louisiana.edu' + Keys.ENTER)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="i0118"]'))).send_keys(credentials.PASSWORD + Keys.ENTER)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="idSIButton9"]'))).click()

    # Outlook - Compose Email
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id__3"]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[3]/div[2]/div/div[3]/div[1]/div/div/div/div[1]/div[1]/div[1]/div[1]/div[1]/div/div/div/div/div[1]/div/div/input'))).send_keys(credentials.RECIPIENT)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[3]/div[2]/div/div[3]/div[1]/div/div/div/div[1]/div[1]/div[1]/div[1]/div[2]/button/div'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[3]/div[2]/div/div[3]/div[1]/div/div/div/div[1]/div[1]/div[1]/div[3]/div/div/div/div/div/div[1]/div/div/input'))).send_keys(credentials.USERNAME + '@louisiana.edu' + Keys.TAB)
    users_name = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="O365_MainLink_Me"]/div/div[1]/span'))).text

    # Outlook - Fill in email
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="subjectLine0"]'))).send_keys(users_name + ' Time Sheet Entry' + Keys.TAB)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[3]/div[2]/div/div[3]/div[1]/div/div/div/div[1]/div[2]/div'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[3]/div[2]/div/div[3]/div[1]/div/div/div/div[1]/div[2]/div'))).send_keys(
        time_period + '\n' +
        str(credentials.HOURS) + ' Hours' + '\n\n' +
        users_name + '\n' +
        str(credentials.USERNAME)
    )
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[3]/div[2]/div/div[3]/div[1]/div/div/div/div[1]/div[4]/div[2]/div[1]/button[1]/div'))).click()
    # print('Clicked send!')

    # Browser Config
    driver.quit()

def segments():
    credentials.number_of_segments = math.ceil(credentials.HOURS / 20)
    credentials.segment_hours = []

    x = 0
    for i in range(credentials.number_of_segments):
        i # Removes 'problem' from IDE.
        x += 20
        if x <= credentials.HOURS:
            credentials.segment_hours.append(20)
        else:
            credentials.segment_hours.append(credentials.HOURS % 20)