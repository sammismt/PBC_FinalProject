#!/usr/bin/env python
# coding: utf-8

def get_keyword(self):
    key_result = []
    keyword_exist = False
    try:
        # 前往簡介
        summary_btn = self.driver.find_element(By.CLASS_NAME, "w5XdTb")
        summary_btn.click()
        time.sleep(3)
        
        # 取得此新頁面原始碼
        soup_summary = BeautifulSoup(self.driver.page_source,"lxml")
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
                key_result.append(key_access[i].text)
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
        self.driver.back()
