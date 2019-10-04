import credentials

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import smtplib, ssl

import time
import math

def selenium_script():
    """This is the main script that runs the headless Chromedriver with Selenium. 
    It navigates through ULink using user given credentials. It travels to banner and opens up the user's timesheet.
    Then, it invokes segments() break up the user inputted "hours worked" into segments of 20 hours.
    It inputs the chunks of 20 and then submits the timesheet. Lastly, it sends an email to our manager and the sender."""

    start_time = time.time()

    # Browser Config
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    capabilities = DesiredCapabilities().CHROME
    capabilities["pageLoadStrategy"] = "none"
    driver = webdriver.Chrome(desired_capabilities=capabilities, chrome_options=options)
    driver.set_window_size(1920, 1080)
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

    # Banner - Collect Status
    banner_status = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="contentHolder"]/div[2]/table[1]/tbody/tr[5]/td/form/table[1]/tbody/tr[2]/td[4]/p'))).text

    # Banner - Collect Data
    time_period = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="contentHolder"]/div[2]/table[1]/tbody/tr[3]/td'))).text

    if banner_status != 0:
        print('Submitted!')
    else:
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

        # Submit Time Sheet For Approval
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id____UID11"]/div/div/div'))).click()

    # Send Email
    if banner_status != 0:
        print('Sent Email!')
    else:
        send_mail(time_period)
    
    # Browser Config
    time.sleep(2)
    driver.quit()

    print("--- %s seconds ---" % (time.time() - start_time))

def segments():
    """Takes the user submitted "hours worked" and divides it into chunks of 20 with a remainder.
    Returns the chunks in a list."""

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

def send_mail(time_period):
    """Send's an email with user provided and sends it to our manager while also sending it back to the sender for confirmation."""

    port = 587  # For starttls
    smtp_server = "smtp.office365.com"
    sender_email = f"{credentials.USERNAME}@louisiana.edu"
    receiver_email = [credentials.RECIPIENT, sender_email]
    password = credentials.PASSWORD

    message = f'Subject: {credentials.NAME} Time Sheet Entry\n\n{time_period}\n{credentials.HOURS} Hours\n\n{credentials.NAME}\n{credentials.USERNAME}'

    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)