from selenium import webdriver
from flask import session
from config import config
import time, math, smtplib, ssl

class Auto:

    def __init__(self, username, password, hours_worked):
        self.name = None
        self.username = username.capitalize()
        self.password = password
        self.hours_worked = hours_worked
        self.number_of_segments = None
        self.segment_hours = None
        self.timesheet_period = None

        Auto.segments(self)
        Auto.script(self)

    def segments(self):
        """Takes the user submitted "hours worked" and divides it into chunks of 20 with a remainder.
        Returns the chunks in a list."""

        self.number_of_segments = math.ceil(self.hours_worked / 20)
        self.segment_hours = []

        x = 0
        for i in range(self.number_of_segments):
            i # Removes 'problem' from IDE.
            x += 20
            if x <= self.hours_worked:
                self.segment_hours.append(20)
            else:
                self.segment_hours.append(self.hours_worked % 20)

        print(self.number_of_segments, self.segment_hours)

    def script(self):
        """Opens Banner in a chrome browser and submits hours worked into the timesheet."""
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(options=options)

        # Open Banner
        driver.get('https://ssb-prod.ec.louisiana.edu/ssomanager/c/SSB?pkg=bwpktais.P_SelectTimeSheetRoll')

        # Log In To Banner
        driver.find_element_by_id('username').send_keys(self.username)
        driver.find_element_by_id('password').send_keys(self.password)
        driver.find_element_by_xpath('//input[@type="submit"]').click()

        try:
            wrong_password_alert = driver.find_element_by_xpath(f"//*[contains(text(), 'Authentication failed! Try again.')]").text
        except:
            wrong_password_alert = None

        if not wrong_password_alert:

            print ('running...')

            # Open Timesheet
            driver.find_element_by_id('id____UID5').click()

            # Get name
            full_name = driver.execute_script('return userDetails;')
            short_name = full_name.split()
            del short_name[1]
            self.name = ' '.join(short_name)
            print(self.name)

            # Enter Hours If Not Already Submitted
            banner_status = driver.find_element_by_xpath('//*[@id="contentHolder"]/div[2]/table[1]/tbody/tr[5]/td/form/table[1]/tbody/tr[2]/td[4]/p').text

            # Collect Timesheet Period
            timesheet_period = driver.find_element_by_xpath('//*[@id="contentHolder"]/div[2]/table[1]/tbody/tr[3]/td').text

            if (int(banner_status) == 0):
                for i in range(self.number_of_segments):
                    if i == 0:
                        driver.find_element_by_xpath(f'//*[@id="contentHolder"]/div[2]/table[1]/tbody/tr[5]/td/form/table[1]/tbody/tr[2]/td[{i + 7}]/p/a').click()
                    else:
                        driver.find_element_by_xpath(f'//*[@id="contentHolder"]/div[2]/table[1]/tbody/tr[6]/td/form/table[1]/tbody/tr[2]/td[{i + 7}]/p/a').click()
                    
                    driver.find_element_by_id('hours_id').send_keys(str(self.segment_hours[i]))
                    driver.find_element_by_xpath('//*[@id="id____UID5"]/div/div/div').click()

                # Submit Timesheet
                driver.find_element_by_xpath('//*[@id="id____UID11"]/div/div/div').click()

                # Send Email
                self.send_email(timesheet_period)
            else:
                print('Timesheet not submitted.')

            session['status'] = f"Thanks, {self.name.split(' ', 1)[0]}!"
        else:
            session['status'] = 'Wrong Password'

        # time.sleep(10000)
        driver.quit()


    def send_email(self, timesheet_period):
        """Send's an email with user provided and sends it to our manager while also 
        sending it back to the sender for confirmation."""

        port = 587  # For starttls
        smtp_server = "smtp.office365.com"
        sender_email = f"{self.username}@louisiana.edu"
        receiver_email = [config["recipient"], sender_email]
        password = self.password

        message = f'Subject: {self.name} Time Sheet Entry\n\n{timesheet_period}\n{self.hours_worked} Hours\n\n{self.name}\n{self.username}'

        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)