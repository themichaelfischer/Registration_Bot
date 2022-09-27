from selenium import webdriver

url = 'https://www.amazon.ca/beyerdynamic-Headphone-professional-recording-monitoring/dp/B0016MNAAI/ref=sr_1_1?crid=LUISCOZOGA5V&dchild=1&keywords=beyerdynamic+dt770+pro&qid=1612820522&sprefix=beyer,aps,229&sr=8-1'
browser = webdriver.Chrome()
browser.get(url)

browser.find_element_by_xpath('//*[@id="price_inside_buybox"]').click()
