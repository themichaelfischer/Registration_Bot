from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# TODO change to OOP
# class Register():
#     url

def setup_driver(URL):
    # gets rid of devtools message
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)
    driver.get(URL)
    return driver

def get_page(driver, program):
    driver.find_element(By.NAME, "all_search_form").click()
    driver.find_element(By.NAME, "KeywordSearch").send_keys(program)
    driver.find_element(By.XPATH, "//input[@type='submit']").click()

def get_login_info():
    f = open ("info.txt", "r")
    user = f.readline().strip()
    password = f.readline()
    f.close()
    return (user, password)

def login(user, password):
    driver.find_element(By.XPATH, "//a[@title='Click here to login.']").click()
    time.sleep(1)
    driver.find_element(By.NAME, "ClientBarcode").send_keys(user)
    driver.find_element(By.NAME, "AccountPIN").send_keys(password)
    driver.find_element(By.XPATH, "//input[@type='submit']").click()

def get_date():
    # TODO get current date
    # TODO choose corresponding date name + location
    return "Friday"

def select_course(day):
    parent = driver.find_element(By.XPATH, "//div[@id='activity-1-8635']")

    #TODO make this function cleaner
    parent.find_element(By.XPATH, "./child::*").click()
    time.sleep(1)
    # add button
    driver.find_element(By.XPATH, "//a[@class='ui-state-active ui-corner-all link-button ajax-request from-full-page focus-parent need-focus-pageobject']").click()



if __name__ == "__main__":
    url = "https://webreg.burnaby.ca/webreg/Activities/ActivitiesAdvSearch.asp"
    driver = setup_driver(url)

    user, password = get_login_info()
    login(user, password)

    get_page(driver, "volleyball")
    
    # TODO check for waitlist condition
    # TODO if add available some how....
    # TODO or try to find select_course function if not continue while loop


    


    time.sleep(1)
    try:
        select_course("tues")
    except:
        print("try again")

    time.sleep(5)

    # driver.refresh()
    # get_page(driver, "volleyball")
    # time.sleep(2)

    # try:
    #     select_course("tues")
    # except:
    #     print("try again")




    # time.sleep(2)


    driver.quit()