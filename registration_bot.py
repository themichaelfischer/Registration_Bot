from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time
import threading

class Register():
    def __init__(self, text_file, test = False, dev = False):
        dt = datetime.now()
        self._test = test
        self._dev = dev
        self._url = "https://webreg.burnaby.ca/webreg/Activities/ActivitiesAdvSearch.asp"
        self._program = "volleyball"
        self._info = text_file
        self._cc_info = "cc_info.txt"
        self._user = ''
        self._password = ''
        self._name = ''
        self._card_number = ''
        self._cvv = ''
        self._exp_month = ''
        self._exp_year = ''
        self._driver = self.setup_driver()
        self._day = self.convert_week_day_to_string(dt.weekday())

        if self._dev:
            self._program = "basketball"
            self._day = "Tuesday"
        
    def print_name(self):
        return self._info

    def convert_week_day_to_string(self, weekday):
        if (weekday == 0): return "Monday"
        elif (weekday == 1): return "Tuesday"
        elif (weekday == 2): return "Wednesday"
        elif (weekday == 3): return "Thursday"
        elif (weekday == 4): return "Friday"
        elif (weekday == 5): return "Saturday"
        elif (weekday == 6): return "Sunday"

    def setup_driver(self):
        """Set's up Selenium Web-driver"""
        # gets rid of devtools message
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)
        driver.get(self._url)
        return driver
        
    def get_login_info(self):
        """ Get login info from file"""
        f = open (self._info, "r")
        self._user = f.readline().strip()
        self._password = f.readline().strip()
        self._name = "//option[contains(text(), '" + f.readline() + "')]"
        f.close()

    def login(self):
        """ Login to webpage"""
        self._driver.find_element(By.XPATH, "//a[@title='Click here to login.']").click()
        self._driver.implicitly_wait(0.5)
        self._driver.find_element(By.NAME, "ClientBarcode").send_keys(self._user)
        self._driver.find_element(By.NAME, "AccountPIN").send_keys(self._password)
        self._driver.find_element(By.XPATH, "//input[@type='submit']").click()

    def get_page(self):
        """ Gets correct activity page instantly"""
        dt = datetime.now()
        dt_hour = dt.hour
        dt_min = dt.minute
        delay = 0

        # check every 5 min until 8:52 then as fast as possible
        if dt_hour < 8:
            delay = 300
        elif dt_hour <= 8 and dt_min <= 53:
            delay = 300
        elif dt_hour <= 8 and dt_min <= 54:
            delay = 240
        elif dt_hour <= 8 and dt_min <= 55:
            delay = 180
        elif dt_hour <= 8 and dt_min <= 56:
            delay = 120
        elif dt_hour <= 8 and dt_min <= 57:
            delay = 60

        print(dt_hour)
        time.sleep(delay)
        self._driver.find_element(By.NAME, "all_search_form").click()
        self._driver.find_element(By.NAME, "KeywordSearch").send_keys(self._program)
        self._driver.find_element(By.XPATH, "//input[@type='submit']").click()

    def get_next_weeks_activity(self):
        activity_dropdown = ""

        if (self._dev):
            # activity_dropdown = "//div[@id='activity-1-8607']" # edmonds
            activity_dropdown = "//div[@id='activity-1-8613']" # bonsor basketball tuesday
            return self._driver.find_element(By.XPATH, activity_dropdown)

        if (self._test):
            self._day = "Tuesday"

        # if (self._day == "Tuesday"): activity_dropdown = "//div[@id='activity-1-8609']" # test table tennis

        if (self._day == "Tuesday"): activity_dropdown = "//div[@id='activity-1-8607']" # edmonds
        # if (self._day == "Tuesday"): activity_dropdown = "//div[@id='activity-1-8642']" # bonsor
        elif (self._day == "Thursday"): activity_dropdown = "//div[@id='activity-1-8614']" # edmonds
        elif (self._day == "Friday"): activity_dropdown = "//div[@id='activity-1-8634']" # bonsor
        elif (self._day == "Sunday"): activity_dropdown = "//div[@id='activity-1-8638']" # christine
        elif (self._day == "Monday"): activity_dropdown = "//div[@id='activity-1-8837']"
        elif (self._day == "Wednesday"): activity_dropdown = "//div[@id='activity-1-8837']"
        return self._driver.find_element(By.XPATH, activity_dropdown)

    def select_course(self):
        """ Selects the correct course"""
        print(self._day)
        self._driver.implicitly_wait(0.5)
        parent = self.get_next_weeks_activity()
        parent.find_element(By.XPATH, "./child::*").click()

        # Add Element is unique so just need to refresh + try this until it works
        self._driver.find_element(By.XPATH, "//a[@class='ui-state-active ui-corner-all link-button ajax-request from-full-page focus-parent need-focus-pageobject']").click()

    def select_person(self):
        """ Selects the correct person to sign up """
        self._driver.implicitly_wait(5)
        self._driver.find_element(By.XPATH, "//select[@name='ClientID']").click()
        self._driver.find_element(By.XPATH, self._name).click()

    def confirm_person(self):
        """ After all people have been selected wait 2 seconds (global) then confirm people"""
        self._driver.implicitly_wait(3)
        self._driver.find_element(By.XPATH, "//input[@value='Go to Checkout']").click()

    def pay_for_course(self):
        """ Pays for the course at checkout page """
        """ Try except block here too... or just remove this as don't need to"""
        time.sleep(2)
        self._driver.implicitly_wait(1)
        self.get_card_info()
        print("Made it to sign up page")

        card_type = Select(self._driver.find_element(By.XPATH, "//select[@name='CardType']"))
        card_type.select_by_visible_text('VISA (web)')

        # enable this line later
        self._driver.find_element(By.XPATH, "//input[@name='CardNum']").send_keys(self._card_number)

        self._driver.find_element(By.XPATH, "//input[@name='CardSecurityCode']").send_keys(self._cvv)

        card_month = Select(self._driver.find_element(By.XPATH, "//select[@name='CardExpM']"))
        card_month.select_by_visible_text(self._exp_month)
        
        card_year = Select(self._driver.find_element(By.XPATH, "//select[@name='CardExpY']"))
        card_year.select_by_visible_text(self._exp_year)
        
        # should run once uncommented
        if (self._test):
            print("click payment!")
        else:
            time.sleep(0.25)
            self._driver.find_element(By.XPATH, "//input[@name='ApplyPayment']").click()
        print("Signed up!")

    def get_card_info(self):
        """ Gets card info from file """
        f = open(self._cc_info, "r")
        self._card_number = f.readline().strip()
        self._cvv = f.readline().strip()
        self._exp_month = f.readline().strip()
        self._exp_year = f.readline()

        f.close()

def exectue_bot(bot):
    course_available = False
    # reg = Register(bot,True, True) # testing basketball
    # reg = Register(bot, True, False) # testing same day no buy
    reg = Register(bot,False, False) # actually buying
    reg.get_login_info()
    reg.login()
    
    start = time.time()
    while (not course_available):
        start = time.time()
        reg.get_page()
        try:
            reg.select_course()
            course_available = True
        except:
            ending = time.time()
            print(f"took: {ending - start}")
            print("Not Yet Available")
            reg._driver.refresh()
        

    reg.select_person()
    end = time.time()

    total_time = end - start
    print(f"Time to book {reg.print_name()}: {total_time}")

    # time.sleep(5)
    # reg.confirm_person()
    # reg.pay_for_course()
    time.sleep(300)

if __name__ == "__main__":
    threading.Thread(target=exectue_bot, args = ("michael.txt",)).start()
    threading.Thread(target=exectue_bot, args = ("arianne.txt",)).start()
    # threading.Thread(target=exectue_bot, args = ("daniel.txt",)).start()
    # threading.Thread(target=exectue_bot, args = ("kayla.txt",)).start()

    
    