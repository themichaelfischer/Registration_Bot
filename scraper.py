#region imports
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
import smtplib
import time
#endregion

#region variables
#url = input("Enter url")
url = 'https://www.amazon.ca/0-5meter-Lead-Snowkids-Compatible-Ethernet-Function/dp/B0839CBWBR/ref=br_msw_pdt-4?_encoding=UTF8&smid=A3M67XBJECTJN0&pf_rd_m=A3DWYIK6Y9EEQB&pf_rd_s=&pf_rd_r=B0DJT26VPXYR82JWH3SP&pf_rd_t=36701&pf_rd_p=4500e888-b5b9-4e64-8bd4-fc15289d25f6&pf_rd_i=desktop'
target_price = 10.00
user_email = 'lodenmf@gmail.com'
#endregion

#region open_browser
driver=webdriver.Chrome("C:/Users/Work/chromedriver")
get=driver.get(url)
html=driver.page_source
soup=BeautifulSoup(html,'html.parser')
#endregion

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo() #establishes connection
    server.starttls() #encripts connection
    server.ehlo()

    server.login('mfischer3d@gmail.com', 'ugbarjbvfomqeygb')

    subject = "Price drop on: " + title
    body = f'{title} + \n \n Target Price: {target_price} \n Current Price: {current_price} \n \n Check the link: {url}'
    msg = f"Subject: {subject} \n\n{body}"

    server.sendmail( 'mfischer3d@gmail.com', user_email, msg )
    print("Email has been sent!")

    server.quit()

price = ''

if ('amazon.ca' in url):
    title=soup.find(id="productTitle").text.strip('\n')
    print(title)
    print (price)
    try: price = soup.find('span',id="priceblock_dealprice").text.strip('\n')
    except: pass
    try: price = soup.find('span',id="priceblock_saleprice").text.strip('\n')
    except: pass
    try: price = soup.find('span',id="priceblock_ourprice").text.strip('\n')
    except: pass
    current_price = float(price.split("CDN$\xa0")[-1])
    print(current_price)

elif ('bestbuy.ca' in url):
    title = soup.find("h1", class_="productName_3nyxM").text
    price = soup.find("div", class_="price_FHDfG large_3aP7Z").text

    price = price[:-2] + "." + price[-2:]
    current_price = float(price.split("$")[-1])


if (current_price <= target_price):
    send_mail()


