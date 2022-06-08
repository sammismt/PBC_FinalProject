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
        self.location_data["keyword"] = []
        self.location_data["opentime"] = [["星期一", "NA", "NA", "NA", "NA"], ["星期二", "NA", "NA", "NA", "NA"], ["星期三", "NA", "NA", "NA", "NA"], ["星期四", "NA", "NA", "NA", "NA"], ["星期五", "NA", "NA", "NA", "NA"], ["星期六", "NA", "NA", "NA", "NA"], ["星期日", "NA", "NA", "NA", "NA"]]
        self.location_data["review"] = []


    # exception: 找不到class
    def get_location_name_rating(self):
        try:
            self.driver.implicitly_wait(10)
            name = self.driver.find_element(By.CLASS_NAME, value="DUwDvf.fontHeadlineLarge")
            self.location_data["name"] = name.text
        except:
            pass

        try:
            self.driver.implicitly_wait(10)
            rating = self.driver.find_element(By.CLASS_NAME, value="F7nice.mmu3tf")
            self.location_data["rating"] = rating.text
        except:
            pass


    def get_location_keyword(self):
        key_result = []
        keyword_exist = False
        try:
            # 前往簡介
            summary_btn = self.driver.find_element(By.CLASS_NAME, "w5XdTb")
            summary_btn.click()
            time.sleep(3)

            # 取得此新頁面原始碼
            soup_summary = Soup(self.driver.page_source,"lxml")
            keyword_exist = True
            
            # 取得無障礙程度、等其他類別之關鍵字
            key_access = soup_summary.find_all(class_='hpLkke')

            # 將關鍵字的網頁原始碼轉為字串存入列表
            key_str = []
            for i in key_access:
                key_str.append(str(i))
                
            # 將不含有代表不提供此服務的class的關鍵字加入結果列表
            for i in range(len(key_str)):
                if ('WeoVJe' not in key_str[i]):
                    key_result.append(key_access[i].text.strip())
        except:
            pass

        try:
            # 取得最上方文字簡介
            key_sum = soup_summary.find(class_='HlvSq')
            key_result.append(key_sum.text)
        except:
            pass

        try:
            self.location_data["keyword"] = key_result
        except:
            pass

        # 這一句要改成前往當前網址或是寫巢狀的try-except block或設定一個TF變數
        if keyword_exist == True:
            self.driver.implicitly_wait(30)
            back = self.driver.find_element(By.CLASS_NAME, "NmQc4.Hk4XGb")
            back.click()


    def scroll_down_for_location_opentime(self):
        self.driver.implicitly_wait(30)
        pyautogui.moveTo(430,850)
        pyautogui.scroll(-500)

    
    # exception: 沒有營業時間的選單
    def tap_open_location_opentime(self):
        try:
            self.driver.implicitly_wait(10)
            timebutton = self.driver.find_element(By.CLASS_NAME, value="ZDu9vd")
            timebutton.click()
        except:
            pass
    
    # 全天休息: [星期幾, close, NA, NA, NA]
    # 中午沒休息: [星期幾, 營業時間, 打烊時間, NA, NA]
    # 中午有休息: [星期幾, 第一次營業時間, 第二次營業時間, 第一次打烊時間, 第二次打烊時間]
    # 24小時營業: [星期幾, 0000, 2400, NA, NA]
    # exception: 沒有營業時間的頁面 [星期幾, NA, NA, NA, NA]
    def get_location_opentime(self):
        try:
            self.driver.implicitly_wait(30)
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
                    self.location_data["opentime"][0][1] = Monday[:2] + Monday[3:5]
                    self.location_data["opentime"][0][2] = Monday[6:8] + Monday[9:11]
                elif len(all_time_tidy[Monday_index]) >= 39:
                    Monday1 = ''
                    Monday1 = all_time_tidy[Monday_index][:11]
                    self.location_data["opentime"][0][1] = Monday1[:2] + Monday1[3:5]
                    self.location_data["opentime"][0][3] = Monday1[6:8] + Monday1[9:11]
                    Monday2 = ''
                    Monday2 = all_time_tidy[Monday_index][11:22]
                    self.location_data["opentime"][0][2] = Monday2[:2] + Monday2[3:5]
                    self.location_data["opentime"][0][4] = Monday2[6:8] + Monday2[9:11]
                else:
                    self.location_data["opentime"][0][1] = "close"
            else:
                self.location_data["opentime"][0][1] = "0000"
                self.location_data["opentime"][0][2] = "2400"

            if all_time_tidy[Tuesday_index][:7] != "24 小時營業":
                if len(all_time_tidy[Tuesday_index]) == 28:
                    Tuesday = ''
                    Tuesday = all_time_tidy[Tuesday_index][:11]
                    self.location_data["opentime"][1][1] = Tuesday[:2] + Tuesday[3:5]
                    self.location_data["opentime"][1][2] = Tuesday[6:8] + Tuesday[9:11]
                elif len(all_time_tidy[Tuesday_index]) >= 39:
                    Tuesday1 = ''
                    Tuesday1 = all_time_tidy[Tuesday_index][:11]
                    self.location_data["opentime"][1][1] = Tuesday1[:2] + Tuesday1[3:5]
                    self.location_data["opentime"][1][3] = Tuesday1[6:8] + Tuesday1[9:11]
                    Tuesday2 = ''
                    Tuesday2 = all_time_tidy[Tuesday_index][11:22]
                    self.location_data["opentime"][1][2] = Tuesday2[:2] + Tuesday2[3:5]
                    self.location_data["opentime"][1][4] = Tuesday2[6:8] + Tuesday2[9:11]
                else:
                    self.location_data["opentime"][1][1] = "close"
            else:
                self.location_data["opentime"][1][1] = "0000"
                self.location_data["opentime"][1][2] = "2400"

            if all_time_tidy[Wednesday_index][:7] != "24 小時營業":
                if len(all_time_tidy[Wednesday_index]) == 28:
                    Wednesday = ''
                    Wednesday = all_time_tidy[Wednesday_index][:11]
                    self.location_data["opentime"][2][1] = Wednesday[:2] + Wednesday[3:5]
                    self.location_data["opentime"][2][2] = Wednesday[6:8] + Wednesday[9:11]
                elif len(all_time_tidy[Wednesday_index]) >= 39:
                    Wednesday1 = ''
                    Wednesday1 = all_time_tidy[Wednesday_index][:11]
                    self.location_data["opentime"][2][1] = Wednesday1[:2] + Wednesday1[3:5]
                    self.location_data["opentime"][2][3] = Wednesday1[6:8] + Wednesday1[9:11]
                    Wednesday2 = ''
                    Wednesday2 = all_time_tidy[Wednesday_index][11:22]
                    self.location_data["opentime"][2][2] = Wednesday2[:2] + Wednesday2[3:5]
                    self.location_data["opentime"][2][4] = Wednesday2[6:8] + Wednesday2[9:11]
                else:
                    self.location_data["opentime"][2][1] = "close"
            else:
                self.location_data["opentime"][2][1] = "0000"
                self.location_data["opentime"][2][2] = "2400"

            if all_time_tidy[Thursday_index][:7] != "24 小時營業":
                if len(all_time_tidy[Thursday_index]) == 28:
                    Thursday = ''
                    Thursday = all_time_tidy[Thursday_index][:11]
                    self.location_data["opentime"][3][1] = Thursday[:2] + Thursday[3:5]
                    self.location_data["opentime"][3][2] = Thursday[6:8] + Thursday[9:11]
                elif len(all_time_tidy[Thursday_index]) >= 39:
                    Thursday1 = ''
                    Thursday1 = all_time_tidy[Thursday_index][:11]
                    self.location_data["opentime"][3][1] = Thursday1[:2] + Thursday1[3:5]
                    self.location_data["opentime"][3][3] = Thursday1[6:8] + Thursday1[9:11]
                    Thursday2 = ''
                    Thursday2 = all_time_tidy[Thursday_index][11:22]
                    self.location_data["opentime"][3][2] = Thursday2[:2] + Thursday2[3:5]
                    self.location_data["opentime"][3][4] = Thursday2[6:8] + Thursday2[9:11]
                else:
                    self.location_data["opentime"][3][1] = "close"
            else:
                self.location_data["opentime"][3][1] = "0000"
                self.location_data["opentime"][3][2] = "2400"

            if all_time_tidy[Friday_index][:7] != "24 小時營業":
                if len(all_time_tidy[Friday_index]) == 28:
                    Friday = ''
                    Friday = all_time_tidy[Friday_index][:11]
                    self.location_data["opentime"][4][1] = Friday[:2] + Friday[3:5]
                    self.location_data["opentime"][4][2] = Friday[6:8] + Friday[9:11]
                elif len(all_time_tidy[Friday_index]) >= 39:
                    Friday1 = ''
                    Friday1 = all_time_tidy[Friday_index][:11]
                    self.location_data["opentime"][4][1] = Friday1[:2] + Friday1[3:5]
                    self.location_data["opentime"][4][3] = Friday1[6:8] + Friday1[9:11]
                    Friday2 = ''
                    Friday2 = all_time_tidy[Friday_index][11:22]
                    self.location_data["opentime"][4][2] = Friday2[:2] + Friday2[3:5]
                    self.location_data["opentime"][4][4] = Friday2[6:8] + Friday2[9:11]
                else:
                    self.location_data["opentime"][4][1] = "close"
            else:
                self.location_data["opentime"][4][1] = "0000"
                self.location_data["opentime"][4][2] = "2400"

            if all_time_tidy[Saturday_index][:7] != "24 小時營業":
                if len(all_time_tidy[Saturday_index]) == 28:
                    Saturday = ''
                    Saturday = all_time_tidy[Saturday_index][:11]
                    self.location_data["opentime"][5][1] = Saturday[:2] + Saturday[3:5]
                    self.location_data["opentime"][5][2] = Saturday[6:8] + Saturday[9:11]
                elif len(all_time_tidy[Saturday_index]) >= 39:
                    Saturday1 = ''
                    Saturday1 = all_time_tidy[Saturday_index][:11]
                    self.location_data["opentime"][5][1] = Saturday1[:2] + Saturday1[3:5]
                    self.location_data["opentime"][5][3] = Saturday1[6:8] + Saturday1[9:11]
                    Saturday2 = ''
                    Saturday2 = all_time_tidy[Saturday_index][11:22]
                    self.location_data["opentime"][5][2] = Saturday2[:2] + Saturday2[3:5]
                    self.location_data["opentime"][5][4] = Saturday2[6:8] + Saturday2[9:11]
                else:
                    self.location_data["opentime"][5][1] = "close"
            else:
                self.location_data["opentime"][5][1] = "0000"
                self.location_data["opentime"][5][2] = "2400"
            
            if all_time_tidy[Sunday_index][:7] != "24 小時營業":
                if len(all_time_tidy[Sunday_index]) == 28:
                    Sunday = all_time_tidy[Sunday_index][:11]
                    self.location_data["opentime"][6][1] = Sunday[:2] + Sunday[3:5]
                    self.location_data["opentime"][6][2] = Sunday[6:8] + Sunday[9:11]
                elif len(all_time_tidy[Sunday_index]) >= 39:
                    Sunday1 = all_time_tidy[Sunday_index][:11]
                    self.location_data["opentime"][6][1] = Sunday1[:2] + Sunday1[3:5]
                    self.location_data["opentime"][6][3] = Sunday1[6:8] + Sunday1[9:11]
                    Sunday2 = all_time_tidy[Sunday_index][11:22]
                    self.location_data["opentime"][6][2] = Sunday2[:2] + Sunday2[3:5]
                    self.location_data["opentime"][6][4] = Sunday2[6:8] + Sunday2[9:11]
                else:
                    self.location_data["opentime"][6][1] = "close"
            else:
                self.location_data["opentime"][6][1] = "0000"
                self.location_data["opentime"][6][2] = "2400"
            
        except:
            pass


    def scroll_back_to_top(self):
        pyautogui.scroll(500)

    
    # exception: 沒有評論的選單
    def tap_open_location_comment(self):
        try:
            self.driver.implicitly_wait(10)
            commentbutton = self.driver.find_element(By.CLASS_NAME, value="DkEaL")
            commentbutton.click()
        except:
            pass


    def scroll_down_for_location_comment(self):
        time.sleep(5)
        for r in range(80):
            self.driver.implicitly_wait(300)
            pyautogui.scroll(-500)


    # exception: 沒有評論的頁面
    def get_location_comment(self):
        try:
            self.driver.implicitly_wait(30)
            soup = Soup(self.driver.page_source,"lxml")
            all_reviews = soup.find_all(class_ = 'wiI7pd')
            all_reviews_tidy = []
            for review in all_reviews:
                all_reviews_tidy.append(review.text.strip())
            # range可以調整要擷取的留言數目
            for r in range(40):
                if len(all_reviews_tidy) >= r + 1:
                    self.location_data["review"].append(all_reviews_tidy[r])
                else:
                    self.location_data["review"].append("NA")
        except:
            for r in range(40):
                self.location_data["review"].append("NA")


    def scrape(self, single_url):
        self.driver.get(single_url)
        self.get_location_name_rating()
        self.get_location_keyword()
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
pyautogui.moveTo(430,850)
for r in range(30):
    pyautogui.scroll(-500)

# 取得20家餐廳的連結，有時候一頁會有超過20家，下一頁的迴圈再處理
url_list = []
soup = Soup(driver.page_source,"lxml")
for link in soup.find_all(class_ = 'hfpxzc'):
    url_list.append(link.get('href'))

# exception: 沒有下一個頁面
try:
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
except:
    pass

driver.quit()

# 跑迴圈，使用WebDriver()爬每個店家
# range可以調整要記錄的店家數目
final_result = []
for r in range(min(3, len(url_list))):
    single_url = url_list[r]
    x = WebDriver()
    final_result.append(copy.deepcopy(x.scrape(single_url)))
print(final_result)

# 單一店家測試
# final_result = []
# single_url = "https://www.google.com.tw/maps/place/%E6%AD%90%E7%89%B9%E5%84%80-%E5%BA%9C%E5%89%8D%E5%BB%A3%E5%A0%B4%E5%9C%B0%E4%B8%8B%E5%81%9C%E8%BB%8A%E5%A0%B4/@25.0344484,121.5649372,17z/data=!3m1!5s0x3442abb0d8534e5d:0x689cf0dc56f48057!4m13!1m7!3m6!1s0x3442ab466de5b261:0xf0534b76480d390c!2sMiraWan!8m2!3d25.0344484!4d121.5671259!10e2!3m4!1s0x0:0x576dacd8165633b3!8m2!3d25.0359834!4d121.5630113?hl=zh-TW"
# x = WebDriver()
# final_result.append(x.scrape(single_url))
# print(final_result)

# 已測試項目:
# 1. 某個地點的餐廳頁面只有一頁
# 2. 店家連結不滿30個
# 3. 沒有keyword
# 4. 各種營業時間
# 5. 沒有營業時間的選單、頁面
# 6. 沒有評論的選單、頁面
# 7. 留言不足40則