#爬蟲爬下來的list:[ [店名1, 評分1, [google 提供關鍵字1],營業時間1, [評論1]],[店名2, 評分2, 營業時間2, 評論2]]
import tkinter as tk

def open_or_not(opentime_list, day, time):
    # 判斷該時段是否有營業 (營業時間的list, 想要去的時間的list)
    for x in range(7):
        
        if opentime_list[x][0] == day:
            # 星期相同
            if int(opentime_list[x][1]) < time < int(opentime_list[x][2]):
                return True
            else:
                return False

def keyword_index(list_keyword, find_keyword):
    # 算關鍵字分數 (爬蟲爬到的list, 他想要找的關鍵字(最多三個!))
    points = 0

    for x in range(len(find_keyword)):
        
        if str(find_keyword[x]) in list_keyword == True:
            # 如果在爬到的list裡面找到他要的關鍵字 加一分
            points += 1
    
    if points == len(find_keyword):  #所有關鍵字都找到了
        return 12
    elif 0 < points < len(find_keyword):  #只找到部分關鍵字
        return 6
    elif points == 0:  #完全沒有符合的關鍵字
        return 0

def score_index(score):
    # 算評分分數:分數乘以2
    score = int(score) * 2
    return score

def goodwords_index(comment_list, goodwords_list):
    # 算正面字詞分數 (爬蟲爬到的list, 我們自己寫的正面字詞庫)
    points = 0

    for x in range(len(comment_list)):
        if points < 5:
            for y in range(len(comment_list[x])):
                if goodwords_list.count(str(comment_list[x][y])) == 1:
                    points += 0.1            
        elif points == 5:
            break
    
    return points

app = tk.Tk() 
ratingdic = {}  #放每一家店對應到的積分
rating_record = []  #記錄每家店的積分
shop = [["麥當勞", "4.3", ["外送", "內用"], [["二", "1200", "1900"], ["三", "1200", "1900"]], ["很好吃", "非常推薦"]]]  # 爬蟲下來的大大list
goodwords = ["推薦", "好吃"]  # 我們自己寫的正面辭庫
answer = []  # 要印出來的答案
keywords = []  #放keywords

def citybox_selected():
    for x in range(len(shop)):
        rate_index = 0
        if open_or_not(shop[x][3], day, time) == True:
            
            if len(keywords) != 0:
                for y in range(len(keywords)):
                    rate_index += keyword_index(shop[x][2], keywords[y])
            elif len(keywords) == 0:
                rate_index += 12
            rate_index += score_index(shop[x][1])
            rate_index += goodwords_index(shop[x][4], goodwords)
            ratingdic[str(shop[x][0])] = rate_index
            rating_record.append(rate_index)
        elif open_or_not(shop[x][3], day, time) == True:
            continue

    rate_index_sorted = sorted(rating_record, reverse = True)  #由高分到低分排列


    for x in range(restnum):
        add_index = rating_record.index(rate_index_sorted[y])
        answer.append(shop[add_index][0])
        rating_record[add_index] = 0

    for x in range(restnum - 1):
        print(answer[x], end = ",")
    print(answer[len(answer) - 1])

#     print(citybox.get())
#     print(entrydestination.get())
#     print((restnumbox.get), type(restnumbox.get()))
#     print(restkindbox.get())
#     print(entryfoodkind.get())
#     print(daybox.get())
#     print(timebox.get())
#     print(type(timebox.get()))
#     print(keyword1box.get())
#     print(keyword2box.get())
#     print(keyword3box.get())

from tkinter import ttk
labelcity = tk.Label(app,text = "請選擇您想搜尋的城市")
labelcity.grid(column=0, row=0, ipadx=5, pady=5, sticky=tk.W+tk.N)

citybox = ttk.Combobox(app, values=["台北市", "新北市","基隆市","桃園市","新竹縣","苗栗縣","台中市","彰化縣","雲林縣","嘉義縣","台南市","高雄市","屏東縣","台東縣","花蓮縣","宜蘭縣","南投縣","澎湖縣","連江縣"], state="readonly", width=10) 
citybox.grid(column=1, row=0, ipadx=5, pady=5, sticky=tk.W+tk.N)
citybox.current(0)

labeldestination = tk.Label(app, text = "請輸入更詳細的地區（如XX鄉、XX站）")
labeldestination.grid(column=0, row=1, ipadx=5, pady=5, sticky=tk.W+tk.N)
entrydestination = tk.Entry(app, width=10)
entrydestination.grid(column=1, row=1, padx=10, pady=5, sticky=tk.W+tk.N)

labelrestnum = tk.Label(app,text = "請選擇欲獲得的店家數量")
labelrestnum.grid(column=0, row=2, ipadx=5, pady=5, sticky=tk.W+tk.N)

restnumbox = ttk.Combobox(app, values=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], state="readonly", width=10) 
restnumbox.grid(column=1, row=2, ipadx=5, pady=5, sticky=tk.W+tk.N)
restnumbox.current(0)

labelrestkind = tk.Label(app,text = "請選擇您想要的店家種類")
labelrestkind.grid(column=0, row=3, ipadx=5, pady=5, sticky=tk.W+tk.N)

restkindbox = ttk.Combobox(app, values=['餐廳','咖啡廳','小吃','不限'], state="readonly", width=10) 
restkindbox.grid(column=1, row=3, ipadx=5, pady=5, sticky=tk.W+tk.N)
restkindbox.current(0)

labelfoodkind = tk.Label(app, text = "請輸入您想吃哪一式料理，如泰式、義式、不限")
labelfoodkind.grid(column=0, row=4, ipadx=5, pady=5, sticky=tk.W+tk.N)
entryfoodkind = tk.Entry(app, width=10)
entryfoodkind.grid(column=1, row=4, padx=10, pady=5, sticky=tk.W+tk.N)

labelday = tk.Label(app,text = "請選擇您想要搜尋的日期")
labelday.grid(column=0, row=5, ipadx=5, pady=5, sticky=tk.W+tk.N)

daybox = ttk.Combobox(app, values=['一','二','三','四','五','六','日'], state="readonly", width=10) 
daybox.grid(column=1, row=5, ipadx=5, pady=5, sticky=tk.W+tk.N)
daybox.current(0)

labeltime = tk.Label(app,text = "請選擇您想要搜尋的時間（24小時制）")
labeltime.grid(column=0, row=6, ipadx=5, pady=5, sticky=tk.W+tk.N)

timebox = ttk.Combobox(app, values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24], state="readonly", width=10) 
timebox.grid(column=1, row=6, ipadx=5, pady=5, sticky=tk.W+tk.N)
timebox.current(0)

labeltime = tk.Label(app,text = "請選擇您想要搜尋的時間（24小時制）")
labeltime.grid(column=0, row=6, ipadx=5, pady=5, sticky=tk.W+tk.N)

timebox = ttk.Combobox(app, values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24], state="readonly", width=10) 
timebox.grid(column=1, row=6, ipadx=5, pady=5, sticky=tk.W+tk.N)
timebox.current(0)

labelkeyword = tk.Label(app,text = "請選擇您的用餐條件")
labelkeyword.grid(column=0, row=7, ipadx=5, pady=5, sticky=tk.W+tk.N)

keyword1box = ttk.Combobox(app, values=['無', '外送', '外帶', '內用', '啤酒', '早餐', '午餐', '晚餐', '洗手間', '適合兒童', '氣氛悠閒', '環境舒適', '適合團體', '接受訂位', '信用卡', '免下車服務', '員工會接受體溫測量', '需要測量體溫', '提供素食料理', '甜點', '提供免費WIFI', '無障礙座位', '無障礙入口', '無障礙停車場'], state="readonly", width=10) 
keyword1box.grid(column=1, row=7, ipadx=5, pady=5, sticky=tk.W+tk.N)
keyword1box.current(0)

keyword2box = ttk.Combobox(app, values=['無', '外送', '外帶', '內用', '啤酒', '早餐', '午餐', '晚餐', '洗手間', '適合兒童', '氣氛悠閒', '環境舒適', '適合團體', '接受訂位', '信用卡', '免下車服務', '員工會接受體溫測量', '需要測量體溫', '提供素食料理', '甜點', '提供免費WIFI', '無障礙座位', '無障礙入口', '無障礙停車場'], state="readonly", width=10) 
keyword2box.grid(column=2, row=7, ipadx=5, pady=5, sticky=tk.W+tk.N)
keyword2box.current(0)

keyword3box = ttk.Combobox(app, values=['無', '外送', '外帶', '內用', '啤酒', '早餐', '午餐', '晚餐', '洗手間', '適合兒童', '氣氛悠閒', '環境舒適', '適合團體', '接受訂位', '信用卡', '免下車服務', '員工會接受體溫測量', '需要測量體溫', '提供素食料理', '甜點', '提供免費WIFI', '無障礙座位', '無障礙入口', '無障礙停車場'], state="readonly", width=10) 
keyword3box.grid(column=3, row=7, ipadx=5, pady=5, sticky=tk.W+tk.N)
keyword3box.current(0)

resultButton = tk.Button(app, text = 'Get Result', command = citybox_selected)
resultButton.grid(column=0, row=10, pady=10, sticky=tk.W+tk.S)

app.mainloop()

def open_or_not(opentime_list, day, time):
    # 判斷該時段是否有營業 (營業時間的list, 想要去的時間的list)
    for x in range(7):
        
        if opentime_list[x][0] == day:
            # 星期相同
            if int(opentime_list[x][1]) < time < int(opentime_list[x][2]):
                return True
            else:
                return False

def keyword_index(list_keyword, find_keyword):
    # 算關鍵字分數 (爬蟲爬到的list, 他想要找的關鍵字(最多三個!))
    points = 0

    for x in range(len(find_keyword)):
        
        if str(find_keyword[x]) in list_keyword == True:
            # 如果在爬到的list裡面找到他要的關鍵字 加一分
            points += 1
    
    if points == len(find_keyword):  #所有關鍵字都找到了
        return 12
    elif 0 < points < len(find_keyword):  #只找到部分關鍵字
        return 6
    elif points == 0:  #完全沒有符合的關鍵字
        return 0

def score_index(score):
    # 算評分分數:分數乘以2
    score = int(score) * 2
    return score

def goodwords_index(comment_list, goodwords_list):
    # 算正面字詞分數 (爬蟲爬到的list, 我們自己寫的正面字詞庫)
    points = 0

    for x in range(len(comment_list)):
        if points < 5:
            for y in range(len(comment_list[x])):
                if goodwords_list.count(str(comment_list[x][y])) == 1:
                    points += 0.1            
        elif points == 5:
            break
    
    return points


ratingdic = {}  #放每一家店對應到的積分
rating_record = []  #記錄每家店的積分
shop = ["麥當勞", "4.3", ["外送", "內用"], [["二", "1200", "1900"], ["三", "1200", "1900"]], ["很好吃", "非常推薦"]]  # 爬蟲下來的大大list
goodwords = ["推薦", "好吃"]  # 我們自己寫的正面辭庫
answer = []  # 要印出來的答案
keywords = []  #放keywords
city = citybox.get()  #輸入縣市
destination = entrydestination.get()  #輸入更小範圍
restnum = int(restnumbox.get())  #輸入想要的店家數量
restkind = restkindbox.get()  #輸入餐廳種類 (咖啡廳、餐廳...)
foodkind = entryfoodkind.get()  #輸入食物種類
day = daybox.get()  #輸入要去的星期
time = timebox.get()  #輸入要去的時間點 格式:1830
keyword1 = keyword1box.get()  #輸入關鍵字
keyword2 = keyword2box.get()
keyword3 = keyword3box.get()
if keyword1 != "無":
    keywords.append(keyword1)
if keyword2 != "無":
    keywords.append(keyword2)
if keyword3 != "無":
    keywords.append(keyword3)

# [店名1, 評分1, [google 提供關鍵字1],[[星期, 開業, 歇業],....], [評論1]]

for x in range(len(shop)):
    rate_index = 0
    if open_or_not(shop[x][3], day, time) == True:
        
        if len(keywords) != 0:
            for y in range(len(keywords)):
                rate_index += keyword_index(shop[x][2], keywords[y])
        elif len(keywords) == 0:
            rate_index += 12
        rate_index += score_index(shop[x][1])
        rate_index += goodwords_index(shop[x][4], goodwords)
        ratingdic[str(shop[x][0])] = rate_index
        rating_record.append(rate_index)
    elif open_or_not(shop[x][3], day, time) == True:
        continue

rate_index_sorted = sorted(rating_record, reverse = True)  #由高分到低分排列


for x in range(restnum):
    add_index = rating_record.index(rate_index_sorted[y])
    answer.append(shop[add_index][0])
    rating_record[add_index] = 0

for x in range(restnum - 1):
    print(answer[x], end = ",")
print(answer[len(answer) - 1])