from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as Soup
import time
import pyautogui
import copy
# -*-coding: utf8-* -

class WebDriver:

    location_data = {}


    def __init__(self):
        self.driver = webdriver.Chrome(executable_path = "C:\\Users\\marina.hsieh\\Desktop\\chromedriver_win32\\chromedriver.exe")
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()

        self.location_data["name"] = "NA"
        self.location_data["rating"] = "NA"
        self.location_data["keyword"] = "NA"
        self.location_data["opentime"] = [["星期一", "NA", "NA", "NA"], ["星期二", "NA", "NA", "NA"], ["星期三", "NA", "NA", "NA"], ["星期四", "NA", "NA", "NA"], ["星期五", "NA", "NA", "NA"], ["星期六", "NA", "NA", "NA"], ["星期日", "NA", "NA", "NA"]]
        self.location_data["review"] = []


    # exception: 找不到class
    def get_location_name_rating_keyword(self):
        self.driver.implicitly_wait(30)
        try:
            name = self.driver.find_element(By.CLASS_NAME, value="DUwDvf.fontHeadlineLarge")
            self.location_data["name"] = name.text
        except:
            self.location_data["name"] = "NA"

        try:
            rating = self.driver.find_element(By.CLASS_NAME, value="F7nice.mmu3tf")
            self.location_data["rating"] = rating.text
        except:
            self.location_data["rating"] = "NA"

        try:
            keyword = self.driver.find_element(By.CLASS_NAME, value="WeS02d.fontBodyMedium")
            self.location_data["keyword"] = keyword.text
        except:
            self.location_data["keyword"] = "NA"


    def scroll_down_for_location_opentime(self):
        self.driver.implicitly_wait(30)
        pyautogui.moveTo(430,700)
        pyautogui.scroll(-500)

    
    # exception: 沒有營業時間的選單
    def tap_open_location_opentime(self):
        try:
            self.driver.implicitly_wait(30)
            timebutton = self.driver.find_element(By.CLASS_NAME, value="ZDu9vd")
            timebutton.click()
        except:
            pass
    
    # 全天休息: [close, NA, NA, NA]
    # 中午沒休息: [星期幾, 營業時間, 打烊時間, NA, NA]
    # 中午有休息: [星期幾, 第一次營業時間, 第二次營業時間, 第一次打烊時間, 第二次打烊時間]
    # 24小時營業: [星期幾, 0000, 2400, NA, NA]
    # exception: 沒有營業時間的頁面
    def get_location_opentime(self):
        try:
            soup = Soup(self.driver.page_source,"lxml")
            all_time = soup.find_all(class_ = "mxowUb")
            
            all_time_tidy = []
            for time in all_time:
                all_time_tidy.append(time.text.strip())
            
            weekday_order = soup.find_all(class_ = "y0skZc")
            weekday_order_tidy = []
            for weekday in weekday_order:
                weekday_order_tidy.append(weekday.text.strip()[:3])
            Monday_index = weekday_order_tidy.index("星期一")
            Tuesday_index = weekday_order_tidy.index("星期二")
            Wednesday_index = weekday_order_tidy.index("星期三")
            Thursday_index = weekday_order_tidy.index("星期四")
            Friday_index = weekday_order_tidy.index("星期五")
            Saturday_index = weekday_order_tidy.index("星期六")
            Sunday_index = weekday_order_tidy.index("星期日")

            if all_time_tidy[Monday_index][:7] != "24 小時營業":
                if len(all_time_tidy[Monday_index]) == 28:
                    Monday = ''
                    Monday = all_time_tidy[Monday_index][:11]
                    self.location_data["opentime"][0][0] = Monday[:2] + Monday[3:5]
                    self.location_data["opentime"][0][1] = Monday[6:8] + Monday[9:11]
                elif len(all_time_tidy[Monday_index]) == 39:
                    Monday1 = ''
                    Monday1 = all_time_tidy[Monday_index][:11]
                    self.location_data["opentime"][0][0] = Monday1[:2] + Monday1[3:5]
                    self.location_data["opentime"][0][2] = Monday1[6:8] + Monday1[9:11]
                    Monday2 = ''
                    Monday2 = all_time_tidy[Monday_index][11:22]
                    self.location_data["opentime"][0][1] = Monday2[:2] + Monday2[3:5]
                    self.location_data["opentime"][0][3] = Monday2[6:8] + Monday2[9:11]
                else:
                    self.location_data["opentime"][0][0] = "close"
            else:
                self.location_data["opentime"][0][0] = "0000"
                self.location_data["opentime"][0][1] = "2500"

            if all_time_tidy[Tuesday_index][:7] != "24 小時營業":
                if len(all_time_tidy[Tuesday_index]) == 28:
                    Tuesday = ''
                    Tuesday = all_time_tidy[Tuesday_index][:11]
                    self.location_data["opentime"][1][0] = Tuesday[:2] + Tuesday[3:5]
                    self.location_data["opentime"][1][1] = Tuesday[6:8] + Tuesday[9:11]
                elif len(all_time_tidy[Tuesday_index]) == 39:
                    Tuesday1 = ''
                    Tuesday1 = all_time_tidy[Tuesday_index][:11]
                    self.location_data["opentime"][1][0] = Tuesday1[:2] + Tuesday1[3:5]
                    self.location_data["opentime"][1][2] = Tuesday1[6:8] + Tuesday1[9:11]
                    Tuesday2 = ''
                    Tuesday2 = all_time_tidy[Tuesday_index][11:22]
                    self.location_data["opentime"][1][1] = Tuesday2[:2] + Tuesday2[3:5]
                    self.location_data["opentime"][1][3] = Tuesday2[6:8] + Tuesday2[9:11]
                else:
                    self.location_data["opentime"][1][0] = "close"
            else:
                self.location_data["opentime"][1][0] = "0000"
                self.location_data["opentime"][1][1] = "2500"

            if all_time_tidy[Wednesday_index][:7] != "24 小時營業":
                if len(all_time_tidy[Wednesday_index]) == 28:
                    Wednesday = ''
                    Wednesday = all_time_tidy[Wednesday_index][:11]
                    self.location_data["opentime"][2][0] = Wednesday[:2] + Wednesday[3:5]
                    self.location_data["opentime"][2][1] = Wednesday[6:8] + Wednesday[9:11]
                elif len(all_time_tidy[Wednesday_index]) == 39:
                    Wednesday1 = ''
                    Wednesday1 = all_time_tidy[Wednesday_index][:11]
                    self.location_data["opentime"][2][0] = Wednesday1[:2] + Wednesday1[3:5]
                    self.location_data["opentime"][2][2] = Wednesday1[6:8] + Wednesday1[9:11]
                    Wednesday2 = ''
                    Wednesday2 = all_time_tidy[Wednesday_index][11:22]
                    self.location_data["opentime"][2][1] = Wednesday2[:2] + Wednesday2[3:5]
                    self.location_data["opentime"][2][3] = Wednesday2[6:8] + Wednesday2[9:11]
                else:
                    self.location_data["opentime"][2][0] = "close"
            else:
                self.location_data["opentime"][2][0] = "0000"
                self.location_data["opentime"][2][1] = "2500"

            if all_time_tidy[Thursday_index][:7] != "24 小時營業":
                if len(all_time_tidy[Thursday_index]) == 28:
                    Thursday = ''
                    Thursday = all_time_tidy[Thursday_index][:11]
                    self.location_data["opentime"][3][0] = Thursday[:2] + Thursday[3:5]
                    self.location_data["opentime"][3][1] = Thursday[6:8] + Thursday[9:11]
                elif len(all_time_tidy[Thursday_index]) == 39:
                    Thursday1 = ''
                    Thursday1 = all_time_tidy[Thursday_index][:11]
                    self.location_data["opentime"][3][0] = Thursday1[:2] + Thursday1[3:5]
                    self.location_data["opentime"][3][2] = Thursday1[6:8] + Thursday1[9:11]
                    Thursday2 = ''
                    Thursday2 = all_time_tidy[Thursday_index][11:22]
                    self.location_data["opentime"][3][1] = Thursday2[:2] + Thursday2[3:5]
                    self.location_data["opentime"][3][3] = Thursday2[6:8] + Thursday2[9:11]
                else:
                    self.location_data["opentime"][3][0] = "close"
            else:
                self.location_data["opentime"][3][0] = "0000"
                self.location_data["opentime"][3][1] = "2500"

            if all_time_tidy[Friday_index][:7] != "24 小時營業":
                if len(all_time_tidy[Friday_index]) == 28:
                    Friday = ''
                    Friday = all_time_tidy[Friday_index][:11]
                    self.location_data["opentime"][4][0] = Friday[:2] + Friday[3:5]
                    self.location_data["opentime"][4][1] = Friday[6:8] + Friday[9:11]
                elif len(all_time_tidy[Friday_index]) == 39:
                    Friday1 = ''
                    Friday1 = all_time_tidy[Friday_index][:11]
                    self.location_data["opentime"][4][0] = Friday1[:2] + Friday1[3:5]
                    self.location_data["opentime"][4][2] = Friday1[6:8] + Friday1[9:11]
                    Friday2 = ''
                    Friday2 = all_time_tidy[Friday_index][11:22]
                    self.location_data["opentime"][4][1] = Friday2[:2] + Friday2[3:5]
                    self.location_data["opentime"][4][3] = Friday2[6:8] + Friday2[9:11]
                else:
                    self.location_data["opentime"][4][0] = "close"
            else:
                self.location_data["opentime"][4][0] = "0000"
                self.location_data["opentime"][4][1] = "2500"

            if all_time_tidy[Saturday_index][:7] != "24 小時營業":
                if len(all_time_tidy[Saturday_index]) == 28:
                    Saturday = ''
                    Saturday = all_time_tidy[Saturday_index][:11]
                    self.location_data["opentime"][5][0] = Saturday[:2] + Saturday[3:5]
                    self.location_data["opentime"][5][1] = Saturday[6:8] + Saturday[9:11]
                elif len(all_time_tidy[Saturday_index]) == 39:
                    Saturday1 = ''
                    Saturday1 = all_time_tidy[Saturday_index][:11]
                    self.location_data["opentime"][5][0] = Saturday1[:2] + Saturday1[3:5]
                    self.location_data["opentime"][5][2] = Saturday1[6:8] + Saturday1[9:11]
                    Saturday2 = ''
                    Saturday2 = all_time_tidy[Saturday_index][11:22]
                    self.location_data["opentime"][5][1] = Saturday2[:2] + Saturday2[3:5]
                    self.location_data["opentime"][5][3] = Saturday2[6:8] + Saturday2[9:11]
                else:
                    self.location_data["opentime"][5][0] = "close"
            else:
                self.location_data["opentime"][5][0] = "0000"
                self.location_data["opentime"][5][1] = "2500"
            
            if all_time_tidy[Sunday_index][:7] != "24 小時營業":
                if len(all_time_tidy[Sunday_index]) == 28:
                    Sunday = all_time_tidy[Sunday_index][:11]
                    self.location_data["opentime"][6][0] = Sunday[:2] + Sunday[3:5]
                    self.location_data["opentime"][6][1] = Sunday[6:8] + Sunday[9:11]
                elif len(all_time_tidy[Sunday_index]) == 39:
                    Sunday1 = all_time_tidy[Sunday_index][:11]
                    self.location_data["opentime"][6][0] = Sunday1[:2] + Sunday1[3:5]
                    self.location_data["opentime"][6][2] = Sunday1[6:8] + Sunday1[9:11]
                    Sunday2 = all_time_tidy[Sunday_index][11:22]
                    self.location_data["opentime"][6][1] = Sunday2[:2] + Sunday2[3:5]
                    self.location_data["opentime"][6][3] = Sunday1[6:8] + Sunday1[9:11]
                else:
                    self.location_data["opentime"][6][0] = "close"
            else:
                self.location_data["opentime"][6][0] = "0000"
                self.location_data["opentime"][6][1] = "2500"
            
        except:
            for r in range(7):
                self.location_data["opentime"][r][0] = "NA"
                self.location_data["opentime"][r][1] = "NA"


    def scroll_back_to_top(self):
        pyautogui.scroll(500)

    
    # exception: 沒有評論的選單
    def tap_open_location_comment(self):
        try:
            self.driver.implicitly_wait(30)
            commentbutton = self.driver.find_element(By.CLASS_NAME, value="DkEaL")
            commentbutton.click()
        except:
            pass


    def scroll_down_for_location_comment(self):
        for r in range(200):
            pyautogui.scroll(-500)
        self.driver.implicitly_wait(300)


    # exception: 沒有評論的頁面
    def get_location_comment(self):
        try:
            soup = Soup(self.driver.page_source,"lxml")
            all_reviews = soup.find_all(class_ = 'wiI7pd')
            all_reviews_tidy = []
            for review in all_reviews:
                all_reviews_tidy.append(review.text.strip())
            for r in range(40):
                if len(all_reviews_tidy) >= r:
                    self.location_data["review"].append(all_reviews_tidy[r])
                else:
                    self.location_data["review"].append("NA")
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


location = input()

driver = webdriver.Chrome(executable_path = "C:\\Users\\marina.hsieh\\Desktop\\chromedriver_win32\\chromedriver.exe")
google_map_url = "https://www.google.com.tw/maps/@23.546162,120.6402133,8z?hl=zh-TW"
driver.get(google_map_url)  # 打開google map
driver.implicitly_wait(30)
driver.maximize_window()  # 最大化視窗
driver.implicitly_wait(30)
element = driver.find_element(By.CLASS_NAME, value = "tactile-searchbox-input")  # 定位搜尋框
driver.implicitly_wait(30)
element.send_keys(location)  # 傳入輸入字串
element.send_keys('\ue007')  # 按下enter

# 把20家餐廳的頁面展開
time.sleep(10)
pyautogui.moveTo(430,720)
for r in range(30):
    pyautogui.scroll(-500)

# 取得20家餐廳的連結，有時候一頁會有超過20家，下一頁的迴圈再處理
url_list = []
soup = Soup(driver.page_source,"lxml")
for link in soup.find_all(class_ = 'hfpxzc'):
    url_list.append(link.get('href'))

# 按下按鍵，到另外20家餐廳的頁面
next_20_location_button = driver.find_element(By.XPATH, value='//*[@id="ppdPk-Ej1Yeb-LgbsSe-tJiF1e"]')
next_20_location_button.click()

# 把另外10家餐廳的頁面展開
time.sleep(5)
for r in range(15):
    pyautogui.scroll(-500)

# 取得另外10家餐廳的連結
soup = Soup(driver.page_source,"lxml")
for link in soup.find_all(class_ = 'hfpxzc'):
    if len(url_list) < 30:
        url_list.append(link.get('href'))
    else:
        break

driver.quit()

# 跑迴圈，使用上方的函數爬每個店家
final_result = []
for r in range(2):
    single_url = url_list[r]
    x = WebDriver()
    final_result.append(copy.deepcopy(x.scrape(single_url)))
print(final_result)
