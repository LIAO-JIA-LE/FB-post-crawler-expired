from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time,json,csv,re,urllib,os
from webdriver_manager.chrome import ChromeDriverManager

#設定目標網址
group_url = "https://www.facebook.com/login/?next=https%3A%2F%2Fwww.facebook.com%2Fgroups%2F960251008444061"

try:
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  #在背景執行
    # driver = webdriver.Chrome() #設定開啟Chrome，執行擋在同一目錄下不用指定路徑
    
    service = Service(ChromeDriverManager().install())  # 確保 chromedriver 路逕正确
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(60) #設定載入超過60秒提示超時錯誤
    driver.get(group_url)    #要讀取的網址

    #自動登入
    username = driver.find_element(By.ID,"email") #尋找輸入帳號的欄位
    password = driver.find_element(By.ID,"pass") #密碼的欄位
    username.send_keys("") #輸入的帳號
    password.send_keys("") #輸入的密碼
    driver.find_element(By.ID,"loginbutton").click() #根據ID尋找loginbutton並點擊

    SCROLL_PAUSE_TIME = 5  # 設定滾動間隔時間（秒）
    SCROLL_TIMES = 3  # 設定滾動的次數

    #執行模擬滾動效果
    for _ in range(SCROLL_TIMES):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #間隔停止 防反爬蟲
        time.sleep(SCROLL_PAUSE_TIME)

    #擷取當前畫面html
    soup = BeautifulSoup(driver.page_source,'html.parser')

    #所有的貼文
    data_list = soup.find_all('div','x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z')
    #變數
    all_data = []
    dnum = 1
    
    #將貼文逐一讀取保存資料
    for data in data_list:
        post_data =[]
        fnum = 1
        post_url = ""
        photo_url = []

        #作者
        author = data.find("a","x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f").find("strong").get_text()
        
        #時間
        datetime = data.find("a","x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm").text
        
        #圖片網址
        img_list = data.find_all('div','x6ikm8r x10wlt62 x10l6tqk')
        dname = "pic_" + str(dnum)

        #判斷並建立資料夾
        if not os.path.exists(dname):
            os.makedirs(dname)
        #儲存每張圖片
        img_data = []
        for img in img_list:
            fname = str(fnum) + ".jpg"
            is_photo = re.search(r'photo',img.find('a')['href'])
            if is_photo is not None :
                img_url = img.find('img')['src']
                urllib.request.urlretrieve(img_url, os.path.join(dname, fname))
                img.append(img.find('img')['src'])
                #儲存在陣列
                img_data.append(img_url)
            fnum += 1

            #貼文網址
            photo_url.append(img.find("a")["href"])
        
        #從圖片的網址進入在找該貼文的網址(走小路)
        #自動進入在儲存圖片時順便抓的圖片網址
        driver.get(photo_url[0])
        #等待內容產生
        time.sleep(1)
        #再將當前頁面的解析保存
        photo_soup = BeautifulSoup(driver.page_source,'html.parser')
        #定位唯一的class
        photo_div = photo_soup.find("div","x9f619 x1n2onr6 x1ja2u2z x78zum5 x2lah0s x1qughib x6s0dn4 xozqiw3 x1q0g3np x1pi30zi x1swvt13 xsag5q8 xz9dl7a xcud41i x139jcc6 x4vbgl9 x1rdy4ex")
        #定位貼文網址的超連結並擷取href
        post_url = photo_div.find("a","x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f")["href"]
        print(post_url)


        #進入詳細貼文
        driver.get(post_url)
        #等待內容產生
        time.sleep(3)
        #再將當前頁面的解析保存
        post_soup = BeautifulSoup(driver.page_source,'html.parser')
        #貼文內文
        posts = post_soup.find("div","x1iorvi4 x1pi30zi x1l90r2v x1swvt13")

        #保存所有資訊以便後去儲存成csv,json
        all_data.append({
            'author': author,
            'datetime': datetime,
            'url': post_url,
            'content':posts.get_text(),
            'img':img_data
            })
        #資料夾名稱變數
        dnum+=1
    
    # 將貼文內容存儲到JSON檔案中
    with open("fb_post.json", "w", encoding="utf-8") as json_file:
        json.dump(all_data, json_file, ensure_ascii=False, indent=4)

    # 將貼文內容存儲到CSV檔案中
    with open("fb_post.csv", "w", newline="",encoding="utf-8-sig") as csv_file:
        csv_writer = csv.DictWriter(csv_file,fieldnames=["author","datetime","url","content","img"])
        csv_writer.writeheader()
        for data in all_data:
            csv_writer.writerow(data)

    # print("貼文內容已成功儲存到 fb_posts.json 和 fb_posts.csv 檔案中。")
    
finally:
    driver.quit() #關閉瀏覽器