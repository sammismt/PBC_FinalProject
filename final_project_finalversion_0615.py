# 爬蟲所需的function

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as Soup
import time
import pyautogui
import copy
# -*-coding: utf8-* -

# 使用Selenium開啟瀏覽器、動態爬取餐廳資訊
class WebDriver:
    
    # 設定存取餐廳資料的預設格式
    location_data = {}

    def __init__(self):
        self.location_data["name"] = "NA"
        self.location_data["rating"] = "NA"
        self.location_data["keyword"] = []
        self.location_data["opentime"] = [["星期一", "NA", "NA", "NA", "NA"],
            ["星期二", "NA", "NA", "NA", "NA"], ["星期三", "NA", "NA", "NA", "NA"],
            ["星期四", "NA", "NA", "NA", "NA"], ["星期五", "NA", "NA", "NA", "NA"],
            ["星期六", "NA", "NA", "NA", "NA"], ["星期日", "NA", "NA", "NA", "NA"]]
        self.location_data["review"] = []


    def open_browser(self, single_url):
        ‘’‘開啟瀏覽器’‘’
        s = Service(r"C:\\Users\\marina.hsieh\\Desktop\\chromedriver_win32\\chromedriver.exe")
        self.driver = webdriver.Chrome(service=s)
        self.driver.get(single_url)
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
    
    
    # exception: 找不到網頁物件（該地點沒有評分、地點名稱位置不同等）
    def get_location_name_rating(self):
        ‘’‘取得餐廳名稱與評分’‘’
        
        try:
            self.driver.implicitly_wait(10)
            name = self.driver.find_element(By.CLASS_NAME,
                                            value="DUwDvf.fontHeadlineLarge")
            self.location_data["name"] = name.text
        except:
            pass

        try:
            self.driver.implicitly_wait(10)
            rating = self.driver.find_element(By.CLASS_NAME,
                                              value="F7nice.mmu3tf")
            self.location_data["rating"] = rating.text
        except:
            pass


    # exception: 找不到網頁物件（該地點沒有簡介）
    def get_location_keyword(self):
        ‘’‘取得餐廳簡介關鍵字’‘’
        
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

        if keyword_exist == True:
            self.driver.implicitly_wait(30)
            back = self.driver.find_element(By.CLASS_NAME, "NmQc4.Hk4XGb")
            back.click()


    def scroll_down_for_location_opentime(self):
        ‘’‘頁面向下捲動’‘’
        
        self.driver.implicitly_wait(30)
        pyautogui.moveTo(430,850)
        pyautogui.scroll(-500)


    # exception: 沒有營業時間的選單
    def tap_open_location_opentime(self):
        ‘’‘點開營業時間選單’‘’
        
        try:
            self.driver.implicitly_wait(10)
            timebutton = self.driver.find_element(By.CLASS_NAME,
                                                  value="ZDu9vd")
            timebutton.click()
        except:
            pass

    # 全天休息: [星期幾, close, NA, NA, NA]
    # 中午沒休息: [星期幾, 營業時間, 打烊時間, NA, NA]
    # 中午有休息: [星期幾, 第一次營業時間, 第二次營業時間, 第一次打烊時間, 第二次打烊時間]
    # 24小時營業: [星期幾, 0000, 2400, NA, NA]
    # exception: 沒有營業時間的頁面 [星期幾, NA, NA, NA, NA]
    def get_location_opentime(self):
        ‘’‘取得餐廳營業時間’‘’
        
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
                    self.location_data["opentime"][0][1] = Monday[:2] \
                                                           + Monday[3:5]
                    self.location_data["opentime"][0][2] = Monday[6:8] \
                                                           + Monday[9:11]
                elif len(all_time_tidy[Monday_index]) >= 39:
                    Monday1 = ''
                    Monday1 = all_time_tidy[Monday_index][:11]
                    self.location_data["opentime"][0][1] = Monday1[:2] \
                                                           + Monday1[3:5]
                    self.location_data["opentime"][0][3] = Monday1[6:8] \
                                                           + Monday1[9:11]
                    Monday2 = ''
                    Monday2 = all_time_tidy[Monday_index][11:22]
                    self.location_data["opentime"][0][2] = Monday2[:2] \
                                                           + Monday2[3:5]
                    self.location_data["opentime"][0][4] = Monday2[6:8] \
                                                           + Monday2[9:11]
                else:
                    self.location_data["opentime"][0][1] = "close"
            else:
                self.location_data["opentime"][0][1] = "0000"
                self.location_data["opentime"][0][2] = "2400"

            if all_time_tidy[Tuesday_index][:7] != "24 小時營業":
                if len(all_time_tidy[Tuesday_index]) == 28:
                    Tuesday = ''
                    Tuesday = all_time_tidy[Tuesday_index][:11]
                    self.location_data["opentime"][1][1] = Tuesday[:2] \
                                                           + Tuesday[3:5]
                    self.location_data["opentime"][1][2] = Tuesday[6:8] \
                                                           + Tuesday[9:11]
                elif len(all_time_tidy[Tuesday_index]) >= 39:
                    Tuesday1 = ''
                    Tuesday1 = all_time_tidy[Tuesday_index][:11]
                    self.location_data["opentime"][1][1] = Tuesday1[:2] \
                                                           + Tuesday1[3:5]
                    self.location_data["opentime"][1][3] = Tuesday1[6:8] \
                                                           + Tuesday1[9:11]
                    Tuesday2 = ''
                    Tuesday2 = all_time_tidy[Tuesday_index][11:22]
                    self.location_data["opentime"][1][2] = Tuesday2[:2] \
                                                           + Tuesday2[3:5]
                    self.location_data["opentime"][1][4] = Tuesday2[6:8] \
                                                           + Tuesday2[9:11]
                else:
                    self.location_data["opentime"][1][1] = "close"
            else:
                self.location_data["opentime"][1][1] = "0000"
                self.location_data["opentime"][1][2] = "2400"

            if all_time_tidy[Wednesday_index][:7] != "24 小時營業":
                if len(all_time_tidy[Wednesday_index]) == 28:
                    Wednesday = ''
                    Wednesday = all_time_tidy[Wednesday_index][:11]
                    self.location_data["opentime"][2][1] = Wednesday[:2] \
                                                           + Wednesday[3:5]
                    self.location_data["opentime"][2][2] = Wednesday[6:8] \
                                                           + Wednesday[9:11]
                elif len(all_time_tidy[Wednesday_index]) >= 39:
                    Wednesday1 = ''
                    Wednesday1 = all_time_tidy[Wednesday_index][:11]
                    self.location_data["opentime"][2][1] = Wednesday1[:2] \
                                                           + Wednesday1[3:5]
                    self.location_data["opentime"][2][3] = Wednesday1[6:8] \
                                                           + Wednesday1[9:11]
                    Wednesday2 = ''
                    Wednesday2 = all_time_tidy[Wednesday_index][11:22]
                    self.location_data["opentime"][2][2] = Wednesday2[:2] \
                                                           + Wednesday2[3:5]
                    self.location_data["opentime"][2][4] = Wednesday2[6:8] \
                                                           + Wednesday2[9:11]
                else:
                    self.location_data["opentime"][2][1] = "close"
            else:
                self.location_data["opentime"][2][1] = "0000"
                self.location_data["opentime"][2][2] = "2400"

            if all_time_tidy[Thursday_index][:7] != "24 小時營業":
                if len(all_time_tidy[Thursday_index]) == 28:
                    Thursday = ''
                    Thursday = all_time_tidy[Thursday_index][:11]
                    self.location_data["opentime"][3][1] = Thursday[:2] \
                                                           + Thursday[3:5]
                    self.location_data["opentime"][3][2] = Thursday[6:8] \
                                                           + Thursday[9:11]
                elif len(all_time_tidy[Thursday_index]) >= 39:
                    Thursday1 = ''
                    Thursday1 = all_time_tidy[Thursday_index][:11]
                    self.location_data["opentime"][3][1] = Thursday1[:2] \
                                                           + Thursday1[3:5]
                    self.location_data["opentime"][3][3] = Thursday1[6:8] \
                                                           + Thursday1[9:11]
                    Thursday2 = ''
                    Thursday2 = all_time_tidy[Thursday_index][11:22]
                    self.location_data["opentime"][3][2] = Thursday2[:2] \
                                                           + Thursday2[3:5]
                    self.location_data["opentime"][3][4] = Thursday2[6:8] \
                                                           + Thursday2[9:11]
                else:
                    self.location_data["opentime"][3][1] = "close"
            else:
                self.location_data["opentime"][3][1] = "0000"
                self.location_data["opentime"][3][2] = "2400"

            if all_time_tidy[Friday_index][:7] != "24 小時營業":
                if len(all_time_tidy[Friday_index]) == 28:
                    Friday = ''
                    Friday = all_time_tidy[Friday_index][:11]
                    self.location_data["opentime"][4][1] = Friday[:2] \
                                                           + Friday[3:5]
                    self.location_data["opentime"][4][2] = Friday[6:8] \
                                                           + Friday[9:11]
                elif len(all_time_tidy[Friday_index]) >= 39:
                    Friday1 = ''
                    Friday1 = all_time_tidy[Friday_index][:11]
                    self.location_data["opentime"][4][1] = Friday1[:2] \
                                                           + Friday1[3:5]
                    self.location_data["opentime"][4][3] = Friday1[6:8] \
                                                           + Friday1[9:11]
                    Friday2 = ''
                    Friday2 = all_time_tidy[Friday_index][11:22]
                    self.location_data["opentime"][4][2] = Friday2[:2] \
                                                           + Friday2[3:5]
                    self.location_data["opentime"][4][4] = Friday2[6:8] \
                                                           + Friday2[9:11]
                else:
                    self.location_data["opentime"][4][1] = "close"
            else:
                self.location_data["opentime"][4][1] = "0000"
                self.location_data["opentime"][4][2] = "2400"

            if all_time_tidy[Saturday_index][:7] != "24 小時營業":
                if len(all_time_tidy[Saturday_index]) == 28:
                    Saturday = ''
                    Saturday = all_time_tidy[Saturday_index][:11]
                    self.location_data["opentime"][5][1] = Saturday[:2] \
                                                           + Saturday[3:5]
                    self.location_data["opentime"][5][2] = Saturday[6:8] \
                                                           + Saturday[9:11]
                elif len(all_time_tidy[Saturday_index]) >= 39:
                    Saturday1 = ''
                    Saturday1 = all_time_tidy[Saturday_index][:11]
                    self.location_data["opentime"][5][1] = Saturday1[:2] \
                                                           + Saturday1[3:5]
                    self.location_data["opentime"][5][3] = Saturday1[6:8] \
                                                           + Saturday1[9:11]
                    Saturday2 = ''
                    Saturday2 = all_time_tidy[Saturday_index][11:22]
                    self.location_data["opentime"][5][2] = Saturday2[:2] \
                                                           + Saturday2[3:5]
                    self.location_data["opentime"][5][4] = Saturday2[6:8] \
                                                           + Saturday2[9:11]
                else:
                    self.location_data["opentime"][5][1] = "close"
            else:
                self.location_data["opentime"][5][1] = "0000"
                self.location_data["opentime"][5][2] = "2400"
            
            if all_time_tidy[Sunday_index][:7] != "24 小時營業":
                if len(all_time_tidy[Sunday_index]) == 28:
                    Sunday = all_time_tidy[Sunday_index][:11]
                    self.location_data["opentime"][6][1] = Sunday[:2] \
                                                           + Sunday[3:5]
                    self.location_data["opentime"][6][2] = Sunday[6:8] \
                                                           + Sunday[9:11]
                elif len(all_time_tidy[Sunday_index]) >= 39:
                    Sunday1 = all_time_tidy[Sunday_index][:11]
                    self.location_data["opentime"][6][1] = Sunday1[:2] \
                                                           + Sunday1[3:5]
                    self.location_data["opentime"][6][3] = Sunday1[6:8] \
                                                           + Sunday1[9:11]
                    Sunday2 = all_time_tidy[Sunday_index][11:22]
                    self.location_data["opentime"][6][2] = Sunday2[:2] \
                                                           + Sunday2[3:5]
                    self.location_data["opentime"][6][4] = Sunday2[6:8] \
                                                           + Sunday2[9:11]
                else:
                    self.location_data["opentime"][6][1] = "close"
            else:
                self.location_data["opentime"][6][1] = "0000"
                self.location_data["opentime"][6][2] = "2400"

        except:
            pass


    def scroll_back_to_top(self):
        ‘’‘回到頁面頂端’‘’
        
        pyautogui.scroll(500)


    # exception: 沒有評論的選單
    def tap_open_location_comment(self):
        ‘’‘打開評論頁面’‘’
        
        try:
            self.driver.implicitly_wait(10)
            commentbutton = self.driver.find_element(By.CLASS_NAME,
                                                     value="DkEaL")
            commentbutton.click()
        except:
            pass


    def scroll_down_for_location_comment(self):
        ‘’‘向下卷動以加載評論’‘’

        time.sleep(5)
        for r in range(80):
            self.driver.implicitly_wait(300)
            pyautogui.scroll(-500)


    # exception: 沒有評論的頁面
    def get_location_comment(self):
        ‘’‘取得餐廳評論’‘’

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
        ‘’‘整合上方function進行爬蟲’‘’

        self.open_browser(single_url)
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


# 演算法所需的function


def open_or_not(opentime_list, day, time_var):
    # 判斷該時段是否有營業 (營業時間的list, 想要去的時間的list)
    index = 0
    for x in range(7):
        if day in opentime_list[index][0] == True:
            index == x
    if opentime_list[index][1] != "NA": 
        if opentime_list[index][1] == "close":
            # 當天沒有營業
            return False
        elif opentime_list[index][1] != "close":
            if opentime_list[index][3] == opentime_list[index][4] == "NA":
                # 中間沒有休息:星期幾，營業時間，打烊時間，NA，NA
                if int(opentime_list[index][1]) < time_var \
                   < int(opentime_list[index][2]):
                    return True
                else:
                    return False
            elif (opentime_list[index][3] != "NA" and
                  opentime_list[index][4] != "NA"):
                # 中間有休息:
                # 星期幾，第一次營業時間，第二次營業時間，第一次打烊時間，第二次打烊時間
                if int(opentime_list[index][1]) < time_var \
                   < int(opentime_list[index][3]) or 
                   int(opentime_list[index][2]) < time_var \
                   < int(opentime_list[index][4]):
                    return True
                else:
                    return False

    elif opentime_list[index][1] == opentime_list[index][2] \
         == opentime_list[index][3] == opentime_list[index][4] == "NA":
        return False


def keyword_index(keywords_list, keywords):
    # 算關鍵字分數 (爬蟲爬到的list, 他想要找的關鍵字(最多三個!))
    points = 0

    for x in range(len(keywords)):
        for y in range(len(keywords_list)):
            if keywords_list[y] == str(keywords[x]):
                # 如果在爬到的list裡面找到他要的關鍵字 加一分
                points += 1

    if points == len(keywords):  # 所有關鍵字都找到了
        return 12
    elif 0 < points < len(keywords):  # 只找到部分關鍵字
        return 6
    elif points == 0:  # 完全沒有符合的關鍵字
        return 0


def score_index(score):
    # 算評分分數:分數乘以2
    if score == "NA":
        score = 0
    else:
        score = float(score) * 2
    return score


def goodwords_index(comment_list, goodwords_list):
    # 算正面字詞分數 (爬蟲爬到的list, 我們自己寫的正面字詞庫)
    points = 0
    for x in range(len(comment_list)):
        if points < 5:
            for y in range(len(goodwords_list)):
                if (goodwords_list[y] in str(comment_list[x])) == True:
                    points += (0.1) \
                              * str(comment_list[x]).count(goodwords_list[y])
        elif points == 5:
            break
    return points


def algorithm(final_result):
    city = city_box.get()  # 輸入縣市
    destination = destination_entry.get()  # 輸入更小範圍
    restnum = int(restnum_box.get())  # 輸入想要的店家數量
    restkind = restkind_box.get()  # 輸入餐廳種類 (咖啡廳、餐廳...)
    foodkind = foodkind_entry.get()  # 輸入食物種類
    day = day_box.get()  # 輸入要去的星期
    time_var = int(hr_box.get()+min_box.get())   # 輸入要去的時間點 格式:1830
    keyword1 = keyword1_box.get()  # 使用者輸入的關鍵字
    keyword2 = keyword2_box.get()
    keyword3 = keyword3_box.get()
    ratingdic = {}  # 放每一家店對應到的積分
    rating_record = []  #記錄每家店的積分
    shop = []  # 爬蟲下來的大大list
    goodwords_list = ["好吃", "氣氛好", "服務好", "交通方便", "划算", "美味", \
                      "CP值高", "很不錯", "很讚", "喜歡", "很好"]  # 自己寫的正面辭庫
    keywords = []  # 放使用者輸入的keywords
    answer = []  # 最後選到的店家的名稱
    output_index_list = []  # 放最後選到的店家的index
    output_list = []  # 輸出店家名稱、index

    # 使用者輸入的關鍵字
    if keyword1 != "無":
        keywords.append(keyword1)
    if keyword2 != "無":
        keywords.append(keyword2)
    if keyword3 != "無":
        keywords.append(keyword3)

    # 計算每個店家的分數
    for x in range(len(final_result)):
        rate_index = 0  # 店家的分數
        if open_or_not(final_result[x]["opentime"], day, time_var) == True and
           final_result[x]["name"] != "NA":
            if len(keywords) != 0:
                rate_index += keyword_index(final_result[x]["keyword"],
                                            keywords)
            elif len(keywords) == 0:
                rate_index += 12
            rate_index += score_index(final_result[x]["rating"])
            rate_index += goodwords_index(final_result[x]["review"],
                                          goodwords_list)
            ratingdic[str(final_result[x]["name"])] = rate_index
            rating_record.append(rate_index)
        elif open_or_not(final_result[x]["opentime"], day, time_var) == False:
            rating_record.append(-1)
            continue
    rate_index_sorted = sorted(rating_record, reverse = True)
    not_pass = rate_index_sorted.count(-1)  # 沒通過的店家數量
    passed = len(rate_index_sorted) - not_pass  # 通過的店家數量

    # 如果完全沒有店家通過
    if not_pass == len(rate_index_sorted):
        answer.append("無符合店家")
    # 如果通過的店家數量不足以輸出
    elif passed < restnum:
        for x in range(passed):
            add_index = rating_record.index(rate_index_sorted[x])
            answer.append(final_result[add_index]["name"])
            rating_record[add_index] = 0
            output_index_list.append(add_index)
        for y in range(restnum - passed):
            answer.append("無其他符合店家")
    # 如果通過的店家數量足以輸出
    elif passed >= restnum:
        for x in range(restnum):
            add_index = rating_record.index(rate_index_sorted[x])
            answer.append(final_result[add_index]["name"])
            rating_record[add_index] = 0
            output_index_list.append(add_index)

    output_list = [answer, output_index_list, rate_index_sorted,
                   not_pass, restnum]

    return output_list


# 視覺化input + 爬蟲爬到的店家資訊 --> 利用演算法計算評分


def search_by_selenium():

    # 使用者輸入的部分

    city = city_box.get()  #輸入縣市
    destination = destination_entry.get()  #輸入更小範圍
    restnum = int(restnum_box.get())  #輸入想要的店家數量
    restkind = restkind_box.get()  #輸入餐廳種類 (咖啡廳、餐廳...)
    foodkind = foodkind_entry.get()  #輸入食物種類
    day = day_box.get()  #輸入要去的星期
    time_var = int(hr_box.get()+min_box.get())   #輸入要去的時間點 格式:1830
    keyword1 = keyword1_box.get()  #輸入關鍵字
    keyword2 = keyword2_box.get()
    keyword3 = keyword3_box.get()
    location = city+destination
    location += restkind
    location += foodkind

    # 存取搜尋結果的所有店家連結
    s = Service(r"C:\\Users\\marina.hsieh\\Desktop\\chromedriver_win32\\chromedriver.exe")
    driver = webdriver.Chrome(service=s)
    google_map_url = "https://www.google.com.tw/maps/@23.546162,120.6402133,8z?hl=zh-TW"
    driver.get(google_map_url)  # 打開google map
    driver.implicitly_wait(30)
    driver.maximize_window()  # 最大化視窗
    driver.implicitly_wait(30)
    element = driver.find_element(By.CLASS_NAME,
                                  value = "tactile-searchbox-input")  # 定位搜尋框
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
        next_20_location_button = driver.find_element(By.XPATH,
                                                      value='//*[@id="ppdPk-Ej1Yeb-LgbsSe-tJiF1e"]')
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
    for r in range(min(5, len(url_list))):
        single_url = url_list[r]
        x = WebDriver()
        final_result.append(copy.deepcopy(x.scrape(single_url)))

    # 利用演算法計算評分
    answer_str = ''
    answer = algorithm(final_result)[0]
    output_index_list = algorithm(final_result)[1]
    rate_index_sorted = algorithm(final_result)[2]
    not_pass = algorithm(final_result)[3]
    restnum = algorithm(final_result)[4]
    if not_pass != len(rate_index_sorted):
        for i in range(restnum - 1):
            answer_str += answer[i]
            answer_str += '、'
        answer_str += answer[restnum - 1]
    # 如果完全沒有店家通過
    else:
        answer_str += answer[0]

    newwindow = tk.Toplevel(app)
    search_Button = tk.Button(newwindow,
                              text = '查詢！',
                              fg = '#8592A2',
                              width=10)
    result = '您的最佳選擇：{}'.format(answer_str)
    result_label = tk.Label(newwindow, text = result)
    result_label.pack()

    # 把挑選的店家的網頁開啟
    if not_pass != len(rate_index_sorted):
        try:
            global new_driver
            s = Service(r"C:\\Users\\marina.hsieh\\Desktop\\chromedriver_win32\\chromedriver.exe")
            new_driver = webdriver.Chrome(service=s)
            new_driver.maximize_window()
            for i in range(len(output_index_list)):
                if i == 0:
                    # 前往第x個地點的網址
                    new_driver.get(url_list[output_index_list[i]])
                    new_driver.implicitly_wait(20)
                else:
                    # 開一個新分頁
                    pyautogui.hotkey('ctrl', 't', interval=0.1)
                    # 前往新分頁
                    new_driver.switch_to.window(new_driver.window_handles[i])
                    new_driver.implicitly_wait(20)
                    new_driver.get(url_list[output_index_list[i]])
        except:
            pass
    else:
        pass


# 視覺化，呼叫以上的function


import tkinter as tk
app = tk.Tk() 
app.title('美食地圖')

from tkinter import ttk
city_label = tk.Label(app,text = "請選擇您想搜尋的城市", fg = '#8592A2',
                      width=30, anchor = 'w')
city_label.grid(column=0, row=0, ipadx=5, pady=5, sticky=tk.W+tk.N)

city_box = ttk.Combobox(app, values=["台北市", "新北市", "基隆市", "桃園市", "新竹縣",
                                     "苗栗縣", "台中市", "彰化縣", "雲林縣", "嘉義縣",
                                     "台南市", "高雄市", "屏東縣", "台東縣", "花蓮縣",
                                     "宜蘭縣", "南投縣", "澎湖縣", "連江縣"],
                        state="readonly", width=10) 
city_box.grid(column=1, row=0, ipadx=5, pady=5, sticky=tk.W+tk.N)
city_box.current(0)

destination_label = tk.Label(app, text = "請輸入更詳細的地區（如XX鄉、XX站）",
                             fg = '#7D6252', width=30, anchor = 'w')
destination_label.grid(column=0, row=1, ipadx=5, pady=5, sticky=tk.W+tk.N)
destination_entry = tk.Entry(app, width=10)
destination_entry.grid(column=1, row=1, padx=10, pady=5, sticky=tk.W+tk.N)

labelrestnum = tk.Label(app,text = "請選擇欲獲得的店家數量", fg = '#8592A2',
                        width=30, anchor = 'w')
labelrestnum.grid(column=0, row=2, ipadx=5, pady=5, sticky=tk.W+tk.N)

restnum_box = ttk.Combobox(app, values=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                           state="readonly", width=10) 
restnum_box.grid(column=1, row=2, ipadx=5, pady=5, sticky=tk.W+tk.N)
restnum_box.current(0)

restkind_label = tk.Label(app,text = "請選擇您想要的店家種類", fg = '#7D6252',
                          width=30, anchor = 'w')
restkind_label.grid(column=0, row=3, ipadx=5, pady=5, sticky=tk.W+tk.N)

restkind_box = ttk.Combobox(app, values=['餐廳','咖啡廳','小吃','不限'],
                            state="readonly", width=10) 
restkind_box.grid(column=1, row=3, ipadx=5, pady=5, sticky=tk.W+tk.N)
restkind_box.current(0)

foodkind_label = tk.Label(app, text = "請輸入您想吃哪一式料理，如泰式、義式、不限",
                          fg = '#8592A2', width=30, anchor = 'w')
foodkind_label.grid(column=0, row=4, ipadx=5, pady=5, sticky=tk.W+tk.N)
foodkind_entry = tk.Entry(app, width=10)
foodkind_entry.grid(column=1, row=4, padx=10, pady=5, sticky=tk.W+tk.N)

day_label = tk.Label(app,text = "請選擇您想要搜尋的日期", fg = '#7D6252',
                     width=30, anchor = 'w')
day_label.grid(column=0, row=5, ipadx=5, pady=5, sticky=tk.W+tk.N)

day_box = ttk.Combobox(app, values=['星期一', '星期二', '星期三', '星期四',
                                    '星期五', '星期六', '星期日'],
                       state="readonly", width=10) 
day_box.grid(column=1, row=5, ipadx=5, pady=5, sticky=tk.W+tk.N)
day_box.current(0)

time_label = tk.Label(app,text = "請選擇您想要搜尋的時間（24小時制）",
                      fg = '#8592A2', width=30, anchor = 'w')
time_label.grid(column=0, row=6, ipadx=5, pady=5, sticky=tk.W+tk.N)

hr_box = ttk.Combobox(app, values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                                   12, 13, 14, 15, 16, 17, 18, 19, 20,
                                   21, 22, 23, 24],
                      state="readonly", width=10) 
hr_box.grid(column=1, row=6, ipadx=5, pady=5, sticky=tk.W+tk.N)
hr_box.current(0)

min_box = ttk.Combobox(app, values=['00', '30'], state="readonly", width=10) 
min_box.grid(column=2, row=6, ipadx=5, pady=5, sticky=tk.W+tk.N)
min_box.current(0)

keyword_label = tk.Label(app,text = "請選擇您的用餐條件", fg = '#7D6252',
                         width=30, anchor = 'w')
keyword_label.grid(column=0, row=7, ipadx=5, pady=5, sticky=tk.W+tk.N)

keyword1_box = ttk.Combobox(app, values=['無', '外送', '外帶', '內用', '啤酒',
                                         '早餐', '午餐', '晚餐', '洗手間',
                                         '適合兒童', '氣氛悠閒', '環境舒適',
                                         '適合團體', '接受訂位', '信用卡',
                                         '免下車服務', '員工會接受體溫測量',
                                         '需要測量體溫', '提供素食料理', '甜點',
                                         '提供免費WIFI', '無障礙座位', '無障礙入口',
                                         '無障礙停車場'],
                            state="readonly", width=10) 
keyword1_box.grid(column=1, row=7, ipadx=5, pady=5, sticky=tk.W+tk.N)
keyword1_box.current(0)

keyword2_box = ttk.Combobox(app, values=['無', '外送', '外帶', '內用', '啤酒',
                                         '早餐', '午餐', '晚餐', '洗手間',
                                         '適合兒童', '氣氛悠閒', '環境舒適',
                                         '適合團體', '接受訂位', '信用卡',
                                         '免下車服務', '員工會接受體溫測量',
                                         '需要測量體溫', '提供素食料理', '甜點',
                                         '提供免費WIFI', '無障礙座位', '無障礙入口',
                                         '無障礙停車場'],
                            state="readonly", width=10) 
keyword2_box.grid(column=2, row=7, ipadx=5, pady=5, sticky=tk.W+tk.N)
keyword2_box.current(0)

keyword3_box = ttk.Combobox(app, values=['無', '外送', '外帶', '內用', '啤酒',
                                         '早餐', '午餐', '晚餐', '洗手間',
                                         '適合兒童', '氣氛悠閒', '環境舒適',
                                         '適合團體', '接受訂位', '信用卡',
                                         '免下車服務', '員工會接受體溫測量',
                                         '需要測量體溫', '提供素食料理', '甜點',
                                         '提供免費WIFI', '無障礙座位', '無障礙入口',
                                         '無障礙停車場'],
                            state="readonly", width=10) 
keyword3_box.grid(column=3, row=7, ipadx=5, pady=5, sticky=tk.W+tk.N)
keyword3_box.current(0)

search_Button = tk.Button(app, text = '查詢！', command = search_by_selenium,
                          fg = '#8592A2', width=10)

search_Button.grid(column=1, row=10, pady=10, sticky=tk.W+tk.S)

app.mainloop()
