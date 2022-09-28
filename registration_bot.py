from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class Register():
    def __init__(self):
        self._url = "https://webreg.burnaby.ca/webreg/Activities/ActivitiesAdvSearch.asp"
        self._program = "volleyball"
        self._day = "Friday"
        self._info = "info.txt"
        self._user = ''
        self._password = ''
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
        # TODO choose corresponding date name + location
        return "Friday"

    # Description: Selects the correct course
    def select_course(self):
        
        parent = self._driver.find_element(By.XPATH, "//div[@id='activity-1-8635']")

        #TODO make this function cleaner as multiple clicks?
        parent.find_element(By.XPATH, "./child::*").click()
        #TODO add sleep
        time.sleep(1)
        # add button
        self._driver.find_element(By.XPATH, "//a[@class='ui-state-active ui-corner-all link-button ajax-request from-full-page focus-parent need-focus-pageobject']").click()


    # Description: Selects the correct person to sign up
    def select_person(self):
        pass
        # TODO select correct person + go to credit card info

    # Description: Checks if course is available to add
    def check_course_availability(self):
        # change to while loop later
        for i in range(5):
            print(i)
            try:
                print("running")
                self.select_course()
                self.select_person()
                print("Course Available!")
                return True
            except:
                print("here")
                time.sleep(1)
                self._driver.refresh()
        return False

    # Description: Pays for course at checkout page
    def pay_for_course(self):
        print("Made it to sign up page")
        pass

    # Description: Destructor which quits selenium driver
    # def __del__(self):
    #     self._driver.quit()

if __name__ == "__main__":
    reg = Register()
    reg.get_login_info()
    reg.login()
    reg.get_page(1)

    # time.sleep(1)
    try:
        reg.select_course()
    except:
        print("failed ")
        # time.sleep(1)
        # reg._driver.refresh()
    
    time.sleep(2)

    # TODO check for waitlist condition
    # TODO if add available some how....
    # TODO or try to find select_course function if not continue while loop

    # TODO while loop, for while add not available.. can test on thur compared to friday which has add?
    # TODO also check when it has a waitlist, check when selecting course that title = 'ADD'

    # if (reg.check_course_availability == True):
    #     reg.pay_for_course()
    
    
