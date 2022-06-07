#爬蟲爬下來的list:[ [店名1, 評分1, [google 提供關鍵字1],營業時間1, [評論1]],[店名2, 評分2, 營業時間2, 評論2]]

def open_or_not(opentime_list, day, time):
    # 判斷該時段是否有營業 (營業時間的list, 想要去的時間的list)
    for x in range(7):
        
        if opentime_list[x][0] == day and opentime_list[x][1] != "close":
            # 星期相同
            if opentime_list[x][3] == opentime_list[x][4] == "NA":
                # 中午沒有休息:星期幾，營業時間，打烊時間，NA，NA
                if int(opentime_list[x][1]) < time < int(opentime_list[x][2]):
                    return True
                else:
                    return False
            elif opentime_list[x][3] != "NA" and opentime_list[x][4] != "NA":
                # 中午有休息:星期幾，第一次營業時間，第二次營業時間，第一次打烊時間，第二次打烊時間
                if int(opentime_list[x][1]) < time < int(opentime_list[x][3]) or int(opentime_list[x][2]) < time < int(opentime_list[x][4]):
                    return True
                else:
                    return False
        elif opentime_list[x][0] == day and opentime_list[x][1] == "close":
            return False
        else:
            continue

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
shop = []  # 爬蟲下來的大大list
goodwords = ["好吃", "氣氛好", "服務好", "交通方便", "划算", "美味", "CP值高"]  # 我們自己寫的正面辭庫
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

# ［{"name":"店家一","rating":"店家一評分","keyword":"店家一關鍵字","opentime":[], "review":["評論1", "評論2"..., "評論40"] } ... ]

for x in range(len(shop)):
    rate_index = 0
    if open_or_not(shop[x][0]["opentime"], day, time) == True:
        
        if len(keywords) != 0:
            for y in range(len(keywords)):
                rate_index += keyword_index(shop[x][0]["keyword"], keywords[y])
        elif len(keywords) == 0:
            rate_index += 12
        rate_index += score_index(shop[x][0]["rating"])
        rate_index += goodwords_index(shop[x][0]["review"], goodwords)
        ratingdic[str(shop[x][0]["name"])] = rate_index
        rating_record.append(rate_index)
    elif open_or_not(shop[x][0]["opentime"], day, time) == True:
        continue

rate_index_sorted = sorted(rating_record, reverse = True)  #由高分到低分排列


for x in range(restnum):
    add_index = rating_record.index(rate_index_sorted[y])
    answer.append(shop[add_index][0]["name"])
    rating_record[add_index] = 0

for x in range(restnum - 1):
    print(answer[x], end = ",")
print(answer[len(answer) - 1])
