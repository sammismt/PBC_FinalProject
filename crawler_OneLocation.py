#!/usr/bin/env python
# coding: utf-8

# In[270]:


import pyautogui


# In[271]:


# import modules
# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup
import time
import json


# In[272]:


# test data
test_keyword = '宜蘭 景點'
chrome_path = Service('/Users/yangyujie/Desktop/python hw/final_project/chromedriver')
googlemap = 'https://www.google.com.tw/maps/@23.546162,120.6402133,8z?hl=zh-TW'
result = []
location_link = []


# In[273]:


# 打開google並輸入關鍵字

driver = webdriver.Chrome(service=chrome_path)
driver.get(googlemap)  # 前往googlemap
driver.maximize_window()

driver.implicitly_wait(20)  # 隱含等待，若後續出現問題可改為明確等待

searchbox = driver.find_element(By.ID, "searchboxinput")  # 輸入關鍵字
searchbox.send_keys(test_keyword)

search_btn = driver.find_element(By.ID, "searchbox-searchbutton")  # 按下搜尋
search_btn.click()


# In[274]:


time.sleep(10)

pyautogui.moveTo(200,400)

for i in range(5):
    pyautogui.scroll(-5000)
    time.sleep(2)


#scroll_el = driver.find_element(By.CLASS_NAME, "m6QErb DxyBCb kA9KIf dS8AEf ecceSd")

#ActionChains(driver).move_by_offset(200,200).perform()
#win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -448)
#js="var q=document.documentElement.scrollTop=10000"
#driver.execute_script(js) 


# In[275]:


# 取得網頁原始碼
time.sleep(15)
soup = BeautifulSoup(driver.page_source,"lxml")


# In[276]:


# 獲取所有地點的超連結，備用
location_link = []
test_link = soup.find_all('a', class_='hfpxzc')  # 注意以class查詢需使用class_
#print(test_link)
i = 0
for link in test_link:
    location_link.append([i,link.get('href')])
    i += 1
print(location_link)
print(len(location_link))  # 如果有21個代表第一個是廣告要記得踢掉


# In[277]:


# 可以抓全部的地點名，備用
loc_name = soup.find_all(class_='qBF1Pd fontHeadlineSmall')
#print(loc_name[0].text)


# In[278]:


# 方法一： 尋找連結位置，在有21個地點的情況下，跳過第一個廣告（不確定廣告是否只出現在第一個）並點開地點
# 方法二：用之前存起來的超連結直接前往地點頁面，好處是可以先把所有地點的連結都整理好再一個一個去
target_loc_link = driver.find_elements(By.CLASS_NAME, "hfpxzc")  # 找到所有地點的位置

#if len(target_loc_link) == 21:  # 有廣告
    #target_loc_link[1].click()
#else:
    #target_loc_link[4].click()

# print(len(target_loc_link))
# print(target_loc_link)

# 方法二
driver.get(location_link[4][1])

soup_single_loc = BeautifulSoup(driver.page_source,"lxml")


# In[290]:


# 抓取地名，加入result清單（空格待清理）
result = []

# 為了分段測試先直接用網址比較快
driver.get(location_link[4][1])

single_loc_name = soup_single_loc.find(class_='DUwDvf fontHeadlineLarge')
# print(single_loc_name)
result.append(single_loc_name.text)
print(result)


# In[291]:


# 抓取評分，加入result清單（空格待清理）

# 為了分段測試先直接用網址比較快
driver.get(location_link[4][1])

single_loc_rating = soup_single_loc.find(class_='F7nice')
result.append(float(single_loc_rating.text))
print(result)


# In[292]:


# 抓取google關鍵字，加入result清單（空格待清理）仍需要處理沒有此item的問題

# 為了分段測試先直接用網址比較快
driver.get(location_link[4][1])
time.sleep(2)

result.append([])

# 前往簡介，仍需要處理沒有此item的問題
summary_btn = driver.find_element(By.CLASS_NAME, "w5XdTb")
summary_btn.click()
time.sleep(3)

# 取得此新頁面原始碼
soup_summary = BeautifulSoup(driver.page_source,"lxml")

# 取得最上方文字簡介
key_sum = soup_summary.find(class_='HlvSq')
result[2].append(key_sum.text)

# 取得無障礙程度、等其他類別之關鍵字
key_access = soup_summary.find_all(class_='hpLkke')
for key in key_access:
    result[2].append(key.text)

print(result)

# 返回
driver.get(location_link[4][1])


# In[293]:


# 抓取營業時間，加入result清單（空格待清理）仍需要處理沒有此item的問題
result.append([['日'],['一'],['二'],['三'],['四'],['五'],['六']])

# 為了分段測試先直接用網址比較快
driver.get(location_link[4][1])
time.sleep(2)

# 點開營業時間
open_btn = driver.find_element(By.CLASS_NAME, "OMl5r.hH0dDd.jBYmhd")
open_btn.click()
time.sleep(3)

# 取得此新頁面原始碼
soup_open = BeautifulSoup(driver.page_source,"lxml")

# 取得所有營業時間
open_time = soup_open.find_all(class_='G8aQO')

# 取得營業時間的文字
text_open_time = []
for i in range(len(open_time)):
    text_open_time.append(open_time[i].text)
# 將營業時間整理後放入result
for i in range(len(text_open_time)):
    print("round" + str(i))
    if ('–' in text_open_time[i]) == True:
        time_split = text_open_time[i].split('–')
        # print(time_split)

        result[3][i].append(time_split[0])
        result[3][i].append(time_split[1])
     
        
print(result)
# print(text_open_time)


# In[294]:


# 抓取評論，加入result清單（空格待清理）仍需要處理沒有此item的問題
result.append([])

# 為了分段測試先直接用網址比較快
driver.get(location_link[4][1])
time.sleep(4)

#pyautogui.moveTo(200,400)

#for i in range(1):
    #pyautogui.scroll(-90)
    #time.sleep(2)

# 打開評論頁面
comment_btn = driver.find_element(By.CLASS_NAME, "DkEaL")
comment_btn.click()
time.sleep(3)

#向下滑加載
pyautogui.moveTo(200,400)
for i in range(2):
    pyautogui.scroll(-200)
    time.sleep(2)

# 取得此新頁面原始碼
soup_comment = BeautifulSoup(driver.page_source,"lxml")

all_comments = soup_comment.find_all(class_='wiI7pd')

for c in all_comments:
    result[4].append(c.text)
    print(c.text)

print(len(all_comments))
print(result)











