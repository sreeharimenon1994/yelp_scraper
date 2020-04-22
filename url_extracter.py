from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time

chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--disable-application-cache')

# use for headless option
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument('log-level=3')


driver_path = 'drivers\\chromedriver.exe'
main_url = 'https://www.yelp.co.uk'
# main_url = 'https://www.yelp.co.uk/search?cflt=restaurants&find_loc=Warsaw'

f = open("test_depth_2.txt", "a")
class Scraper():

    def scroll(self):
        try:
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(self.scroll_wait)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
        except:
            print('js failed....')

    def load_web_page(self, u):
        self.driver.get(u)
        self.scroll()

    def url_checker(self, url):
        flag = True
        if self.domain in url:
            if any(sub in url for sub in self.url_filter_string):
                flag = False
        else:
            flag = False
        return flag

    def url_extracter(self):
        tmp_url_set = set()
        all_urls = self.driver.find_elements_by_xpath('//a')
        for x in all_urls:
            all_url_ext = x.get_attribute("href")
            if all_url_ext:
                if self.url_checker(all_url_ext):
                    tmp_url_set.add(all_url_ext)
        return list(tmp_url_set)

    def depth_runner(self, url, depth):
        if depth <= self.max_depth:
            self.load_web_page(url)
            url_ext = self.url_extracter()
            for x in url_ext:
                if x not in self.complete_url_set:
                    print(depth, x)
                    f.write(x+"\n")
                    self.complete_url_set.add(x)
                    self.depth_runner(x, depth+1)

    def depth_runner_init(self, url, depth):
        self.load_web_page(url)
        tmp = self.url_extracter()
        for x in tmp:
            if self.domain in x:
                print(depth, x)
                self.depth_runner(x, depth+1)

    def __init__(self, main_url):
        super(Scraper, self).__init__()
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=driver_path)
        self.driver.maximize_window()
        # self.clear_cache()
        self.max_depth = 2
        self.scroll_wait = 0.25
        self.complete_url_set = set()
        self.domain = "yelp.co.uk"
        self.url_filter_string = ["/biz_photos/", "/biz_redir", "/biz_user_photos", "/writeareview", "/not_recommended_reviews" "/menu", "/guidelines", "/user_details", "/biz_attribute", "/signup", "/login", "/event", "/careers", "/questions", "/talk", "/support", "/mobile", "/advertise", "/map", "/topic", "/static"]
        self.url_accept_string = ["/search", "/biz/", "/colletion"]
        self.depth_runner_init(main_url, 0)
        self.driver.quit()

start_time = time.time()
test = Scraper(main_url)
print("--- minutes ---" ,(time.time() - start_time)/60)

complete = test.complete_url_set

df = pd.DataFrame(list(complete), columns=["Url"])
df.to_csv('urls.csv', index=False)
print('file saved...')
