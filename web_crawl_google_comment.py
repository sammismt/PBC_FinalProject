from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as Soup
import time

driver = webdriver.Chrome(executable_path = "C:\\Users\\marina.hsieh\\Desktop\\PBC_final project\\chromedriver_win32\\chromedriver.exe")
url = "https://www.google.com.tw/maps/@23.546162,120.6402133,8z?hl=zh-TW"
driver.get(url)

driver.implicitly_wait(30)
# 定位搜尋框
element = driver.find_element_by_class_name("searchboxinput")
driver.implicitly_wait(30)
# 傳入字串
element.send_keys("台北市大安區咖啡廳")
# press enter
element.send_keys('\ue007')

# 點進第一家店
driver.implicitly_wait(30)  # 讓他跑最長30秒
button = driver.find_element_by_xpath("/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[3]/div/a")
button.click()

# 點進評論頁面
driver.implicitly_wait(30)
commentbutton = driver.find_element_by_class_name("DkEaL")
commentbutton.click()

# 不知道為什麼沒辦法scroll down
# scrollable_div = driver.find_element_by_class_name('m6QErb.DxyBCb.kA9KIf.dS8AEf')
# driver.execute_script('arguments[0].scrollHeight', scrollable_div)

# 獲取網頁原始碼
soup = Soup(driver.page_source,"lxml")

# 獲取評論資料
all_reviews = soup.find_all(class_ = 'wiI7pd')
for ar in all_reviews:
    print(ar)

# 回到上一頁
driver.implicitly_wait(30)
backbutton = driver.find_element_by_class_name("VfPpkd-kBDsod")
backbutton.click()
