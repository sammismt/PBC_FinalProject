#!/usr/bin/env python
# coding: utf-8


# result_path 要從演算法的結果抓網址存成一個結果的list
result_path = [googlemap,googlemap,googlemap]


# service=的部分要改成自己電腦的路徑～
driver = webdriver.Chrome(service=chrome_path)
driver.maximize_window()

# result_path要記得改成實際上存網址的lst
for i in range(len(result_path)):
    if i == 0:
        driver.get(result_path[i])  # 前往第x個地點的網址
        driver.implicitly_wait(20)

    else:
        # 如果是windows系統，command 要改成ctrl
        pyautogui.hotkey('command', 't', interval=0.1)  # 開一個新分頁
        driver.switch_to.window(driver.window_handles[i])  # 前往新分頁
        driver.implicitly_wait(20)
        driver.get(result_path[i])



# In[ ]:




