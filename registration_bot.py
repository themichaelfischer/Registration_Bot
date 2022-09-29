from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time

class Register():
    def __init__(self):
        self._url = "https://webreg.burnaby.ca/webreg/Activities/ActivitiesAdvSearch.asp"
        self._program = "volleyball"
        self._day = "Friday"
        self._info = "info.txt"
        self._cc_info = "cc_info.txt"
        self._user = ''
        self._password = ''
        self._card_number = ''
        self._cvv = ''
        self._exp_month = ''
        self._exp_year = ''
        self._driver = self.setup_driver()

    # Description: set's up selenium driver
    def setup_driver(self):
        # gets rid of devtools message
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)
        driver.get(self._url)
        return driver
        
    # Description: get login info from file
    def get_login_info(self):
        f = open (self._info, "r")
        self._user = f.readline().strip()
        self._password = f.readline()
        f.close()

    # Description: login to webpage
    def login(self):
        self._driver.find_element(By.XPATH, "//a[@title='Click here to login.']").click()
        time.sleep(1)
        self._driver.find_element(By.NAME, "ClientBarcode").send_keys(self._user)
        self._driver.find_element(By.NAME, "AccountPIN").send_keys(self._password)
        self._driver.find_element(By.XPATH, "//input[@type='submit']").click()

    # Description: Gets correct activity page
    def get_page(self, amount):
        self._driver.find_element(By.NAME, "all_search_form").click()
        self._driver.find_element(By.NAME, "KeywordSearch").send_keys(self._program)
        self._driver.find_element(By.XPATH, "//input[@type='submit']").click()
        time.sleep(amount)

    # Description: Gets current date to select date you wish to sign up for
    def get_date():
        # TODO get current date
        # TODO have corresponding date to "//div[@id='activity-1-####']"
        return "Friday"

    # Description: Selects the correct course
    def select_course(self):
        #TODO select based on current date
        parent = self._driver.find_element(By.XPATH, "//div[@id='activity-1-8614']")

        #TODO make this function cleaner as multiple clicks?
        parent.find_element(By.XPATH, "./child::*").click()
        time.sleep(0.5)

        # Add Element is unique so just need to refresh + try this until it works
        self._driver.find_element(By.XPATH, "//a[@class='ui-state-active ui-corner-all link-button ajax-request from-full-page focus-parent need-focus-pageobject']").click()
        time.sleep(1)

    # Description: Selects the correct person to sign up
    def select_person(self):
        self._driver.find_element(By.XPATH, "//select[@name='ClientID']").click()
        # TODO make this match a name instead
        time.sleep(0.5)
        self._driver.find_element(By.XPATH, "//option[@value='10382']").click()
        # TODO select correct person + go to credit card info
        time.sleep(0.5)

        self._driver.find_element(By.XPATH, "//input[@value='Go to Checkout']").click()

        time.sleep(1)

    # Description: Pays for course at checkout page
    def pay_for_course(self):
        self.get_card_info()
        print("Made it to sign up page")

        card_type = Select(self._driver.find_element(By.XPATH, "//select[@name='CardType']"))
        card_type.select_by_visible_text('VISA (web)')

        self._driver.find_element(By.XPATH, "//input[@name='CardNum']").send_keys(self._card_number)

        self._driver.find_element(By.XPATH, "//input[@name='CardSecurityCode']").send_keys(self._cvv)

        card_month = Select(self._driver.find_element(By.XPATH, "//select[@name='CardExpM']"))
        card_month.select_by_visible_text(self._exp_month)
        
        card_year = Select(self._driver.find_element(By.XPATH, "//select[@name='CardExpY']"))
        card_year.select_by_visible_text(self._exp_year)

        # TODO should run once this is un commented
        self._driver.find_element(By.XPATH, "//input[@name='ApplyPayment']").click()
        print("Signed up!")

    # Description: Get's card info from file
    def get_card_info(self):
        f = open(self._cc_info, "r")
        self._card_number = f.readline().strip()
        self._cvv = f.readline().strip()
        self._exp_month = f.readline().strip()
        self._exp_year = f.readline()

        f.close()

    # Description: Destructor which quits selenium driver
    # def __del__(self):
    #     self._driver.quit()

if __name__ == "__main__":
    course_available = False
    reg = Register()

    reg.get_login_info()
    reg.login()
    
    while (not course_available):
        reg.get_page(1)
        try:
            reg.select_course()
            course_available = True
        except:
            print("Not Yet Available")
            time.sleep(1)
            reg._driver.refresh()

    reg.select_person()
    reg.pay_for_course()
    