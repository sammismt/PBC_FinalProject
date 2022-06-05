from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as Soup
import time
import pyautogui

class WebDriver:

    location_data = {}


    def __init__(self):
        self.driver = webdriver.Chrome(executable_path = "C:\\Users\\marina.hsieh\\Desktop\\chromedriver_win32\\chromedriver.exe")
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        
        self.location_data["name"] = "NA"
        self.location_data["rating"] = "NA"
        self.location_data["keyword"] = "NA"
        self.location_data["opentime"] = {"Monday":"NA", "Tuesday":"NA", "Wednesday":"NA", "Thursday":"NA", "Friday":"NA", "Saturday":"NA", "Sunday":"NA"}
        self.location_data["review"] = []


    def get_location_name_rating_keyword(self):
        try:
            self.driver.implicitly_wait(30)
            name = self.driver.find_element(By.CLASS_NAME, value="DUwDvf.fontHeadlineLarge")
            rating = self.driver.find_element(By.CLASS_NAME, value="F7nice.mmu3tf")
            keyword = self.driver.find_element(By.CLASS_NAME, value="WeS02d.fontBodyMedium")
        except:
            pass
        try:
            self.location_data["name"] = name.text
            self.location_data["rating"] = rating.text
            self.location_data["keyword"] = keyword.text
        except:
            pass


    def scroll_down_for_location_opentime(self):
        self.driver.implicitly_wait(30)
        pyautogui.moveTo(430,646)
        pyautogui.scroll(-500)


    def tap_open_location_opentime(self):
        self.driver.implicitly_wait(30)
        timebutton = self.driver.find_element(By.CLASS_NAME, value="ZDu9vd")
        timebutton.click()


    def get_location_opentime(self):
        try:
            soup = Soup(self.driver.page_source,"lxml")
            all_time = soup.find_all(class_ = "mxowUb")
            self.location_data["opentime"]["Sunday"] = all_time[0].text.strip()[:11]
            self.location_data["opentime"]["Monday"] = all_time[1].text.strip()[:11]
            self.location_data["opentime"]["Tuesday"] = all_time[2].text.strip()[:11]
            self.location_data["opentime"]["Wednesday"] = all_time[3].text.strip()[:11]
            self.location_data["opentime"]["Thursday"] = all_time[4].text.strip()[:11]
            self.location_data["opentime"]["Friday"] = all_time[5].text.strip()[:11]
            self.location_data["opentime"]["Saturday"] = all_time[6].text.strip()[:11]
        except:
            pass


    def scroll_back_to_top(self):
        pyautogui.scroll(500)


    def tap_open_location_comment(self):
        self.driver.implicitly_wait(30)
        commentbutton = self.driver.find_element(By.CLASS_NAME, value="DkEaL")
        commentbutton.click()


    def scroll_down_for_location_comment(self):
        for r in range(200):
            pyautogui.scroll(-500)
        self.driver.implicitly_wait(300)


    def get_location_comment(self):
        try:
            soup = Soup(self.driver.page_source,"lxml")
            all_reviews = soup.find_all(class_ = 'wiI7pd')
            for r in range(20):
                self.location_data["review"].append(all_reviews[r].text)
        except:
            pass


    def scrape(self, single_url):
        self.driver.get(single_url)
        self.get_location_name_rating_keyword()
        self.scroll_down_for_location_opentime()
        self.tap_open_location_opentime()
        self.get_location_opentime()
        self.scroll_back_to_top()
        self.tap_open_location_comment()
        self.scroll_down_for_location_comment()
        self.get_location_comment()
        self.driver.quit()
        return(self.location_data)


location = input("縣市+地理區+餐廳類型: ")

# 打開google map
driver = webdriver.Chrome(executable_path = "C:\\Users\\marina.hsieh\\Desktop\\chromedriver_win32\\chromedriver.exe")
google_map_url = "https://www.google.com.tw/maps/@23.546162,120.6402133,8z?hl=zh-TW"
driver.get(google_map_url)

# 最大化視窗
driver.implicitly_wait(30)
driver.maximize_window()

# 定位搜尋框
driver.implicitly_wait(30)
element = driver.find_element(By.CLASS_NAME, value="tactile-searchbox-input")

# 傳入輸入字串
driver.implicitly_wait(30)
element.send_keys(location)

# 按下enter
element.send_keys('\ue007')

# 把20家餐廳的頁面展開
time.sleep(10)
pyautogui.moveTo(430,646)
for r in range(30):
    pyautogui.scroll(-500)

# 取得20家餐廳的連結
url_list = []
soup = Soup(driver.page_source,"lxml")
for link in soup.find_all(class_ = 'hfpxzc'):
    url_list.append(link.get('href'))

# 按下按鍵，到另外20家餐廳的頁面
next_20_location_button = driver.find_element(By.XPATH, value='//*[@id="ppdPk-Ej1Yeb-LgbsSe-tJiF1e"]')
next_20_location_button.click()

# 把另外20家餐廳的頁面展開
time.sleep(5)
for r in range(30):
    pyautogui.scroll(-500)

# 取得另外20家餐廳的連結
soup = Soup(driver.page_source,"lxml")
for link in soup.find_all(class_ = 'hfpxzc'):
    url_list.append(link.get('href'))

driver.quit()

# 接下來跑迴圈
final_result = []
single_url = url_list[0]
x = WebDriver()
final_result.append(x.scrape(single_url))
print(final_result)
# final_result = []
# for r in url_list:
    # x = WebDriver()
    # final_result.append(x.scrape(r))
# print(final_result)