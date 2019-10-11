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


class Automation:
    
    def __init__(self, username, password, hours):
        self.name = ''
        self.username = username
        self.password = password
        self.hours = 0
        self.number_of_segments, self.segment_hours = Automation.segments(self)
        self.time_period = ''

        Automation.selenium_script(self)

    def segments(self):
        """Takes the user submitted "hours worked" and divides it into chunks of 20 with a remainder.
        Returns the chunks in a list."""

        self.number_of_segments = math.ceil(self.hours / 20)
        self.segment_hours = []

        x = 0
        for i in range(self.number_of_segments):
            i # Removes 'problem' from IDE.
            x += 20
            if x <= self.hours:
                self.segment_hours.append(20)
            else:
                self.segment_hours.append(self.hours % 20)

        return self.number_of_segments, self.segment_hours

    def selenium_script(self):
        """This is the main script that runs the headless Chromedriver with Selenium. 
        It navigates through ULink using user given credentials. It travels to banner and opens up the user's timesheet.
        Then, it invokes segments() break up the user inputted "hours worked" into segments of 20 hours.
        It inputs the chunks of 20 and then submits the timesheet. Lastly, it sends an email to our manager and the sender."""

        start_time = time.time()

        # Browser Config
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('disable-gpu')
        options.add_argument('no-sandbox')
        capabilities = DesiredCapabilities().CHROME
        capabilities["pageLoadStrategy"] = "none"
        driver = webdriver.Chrome(desired_capabilities=capabilities, options=options)
        driver.set_window_size(1920, 1080)
        driver.set_page_load_timeout(10)
        wait = WebDriverWait(driver, 10)

        # Open Chrome
        driver.get('https://ulink.louisiana.edu')

        # ULink Login
        wait.until(EC.element_to_be_clickable((By.ID, 'username'))).send_keys(self.username)
        wait.until(EC.element_to_be_clickable((By.ID, 'password'))).send_keys(self.password)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]/div[4]/input'))).click()

        # Travel to Banner
        self.name = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/nav[2]/div[3]/div/div/div/div[1]/div/div/span[2]/div[2]/ul/li[3]/a/span/span'))).text
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="layout_33"]/a/span'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="portlet_56_INSTANCE_ZJ9sUpbDoQCa"]/div/div/div/div[1]/p/a'))).click()
        driver.switch_to.window(driver.window_handles[1])

        # Banner - Open Time Sheet
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id____UID5"]/div/div/div'))).click()

        # Banner - Collect Status
        banner_status = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="contentHolder"]/div[2]/table[1]/tbody/tr[5]/td/form/table[1]/tbody/tr[2]/td[4]/p'))).text

        # Banner - Collect Data
        self.time_period = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="contentHolder"]/div[2]/table[1]/tbody/tr[3]/td'))).text

        if banner_status != 0:
            print('Submitted!')
        else:
            # Banner - Enter Time Sheet Hours
            y = 7
            for i in range(self.number_of_segments):
                if i == 0:
                    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="contentHolder"]/div[2]/table[1]/tbody/tr[5]/td/form/table[1]/tbody/tr[2]/td[' + str(y) + ']/p/a'))).click()
                else:
                    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="contentHolder"]/div[2]/table[1]/tbody/tr[6]/td/form/table[1]/tbody/tr[2]/td[' + str(y) + ']/p/a'))).click()

                wait.until(EC.element_to_be_clickable((By.ID, 'hours_id'))).send_keys(str(self.segment_hours[i]))
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id____UID5"]/div/div/div'))).click()
                y += 1

            # Submit Time Sheet For Approval
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id____UID11"]/div/div/div'))).click()

        # Send Email
        if banner_status != 0:
            print('Sent Email!')
        else:
            Automation.send_mail(self, self.time_period)
        
        # Browser Config
        time.sleep(2)
        driver.quit()

        print(self.name)
        print("--- %s seconds ---" % (time.time() - start_time))

    def send_mail(self, time_period):
        """Send's an email with user provided and sends it to our manager while also 
        sending it back to the sender for confirmation."""

        port = 587  # For starttls
        smtp_server = "smtp.office365.com"
        sender_email = f"{self.username}@louisiana.edu"
        receiver_email = [credentials.RECIPIENT, sender_email]
        password = self.password

        message = f'Subject: {self.name} Time Sheet Entry\n\n{time_period}\n{self.hours} Hours\n\n{self.name}\n{self.username}'

        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)