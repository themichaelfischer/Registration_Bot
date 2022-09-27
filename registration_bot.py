#region imports
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
import smtplib
import time
#endregion

url = 'https://webreg.burnaby.ca/webreg/Activities/ActivitiesAdvSearch.asp'

driver=webdriver.Chrome("C:/Users/Work/chromedriver")
get=driver.get(url)
html=driver.page_source
soup=BeautifulSoup(html,'html.parser')



title = soup.find(title="Click here for advanced search").text.strip('\n')

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print(title)
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")

time.sleep(2)