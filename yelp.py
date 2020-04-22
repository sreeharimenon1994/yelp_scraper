from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

chrome_options = Options()
chrome_options.add_argument('log-level=3')
# use for headless option
chrome_options.add_argument("--headless")
# use it while using headless option
chrome_options.add_argument("--window-size=1920x1080")


driver_path = 'drivers\\chromedriver.exe'
url = 'https://www.yelp.co.uk/search?cflt=restaurants&find_loc=London' 

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=driver_path)
driver.maximize_window()

driver.get(url)
driver.implicitly_wait(1)

all_urls = driver.find_elements_by_xpath('//*[@id="wrap"]/div[3]/div[2]/div/div[1]/div[1]/div[2]/div[2]/ul//a')
url_set = set()
for x in all_urls:
    url_set.add(x.get_attribute("href").split('?')[0])

details = []
for x in url_set:
    if '/biz/' in x:
        print(x)
        driver.get(x)
        driver.implicitly_wait(.5)
        title = driver.find_elements_by_xpath('//h1')[0].text
        phone = driver.find_elements_by_xpath("//*[text()='Phone number']")
        if len(phone) > 0:
            phone = phone[0].find_element_by_xpath('..')
            phone = phone.find_elements_by_tag_name("p")
            if len(phone) == 2:
                phone = phone[1].text
        else:
            phone = ''

        address = driver.find_elements_by_xpath("//address")[1].text
        details.append([title, phone, address, x])

df = pd.DataFrame(details, columns=["Title", "Phone", "Address", "Url"])
df.to_csv('details.csv', index=False)
driver.quit()