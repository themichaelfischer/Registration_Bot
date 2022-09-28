from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

URL = "https://webreg.burnaby.ca/webreg/Activities/ActivitiesAdvSearch.asp"

# gets rid of devtools message
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)
driver.get(URL)

driver.find_element(By.NAME, "all_search_form").click()


filter = driver.find_element(By.NAME, "KeywordSearch")
filter.send_keys("volleyball")

driver.find_element(By.XPATH, "//input[@type='submit']").click()

time.sleep(5)