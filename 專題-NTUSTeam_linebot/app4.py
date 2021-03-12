import random

import requests
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import sys
import imp
import time
from bs4 import BeautifulSoup
from selenium import webdriver

import json
# --------------------------------------------------
import httplib2
import os
import io

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from selenium.webdriver import ActionChains

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Python OCR'
FILE_ID = '11JjdhbBRHVqj8S6vQM93cxZIX82NsKmE'

# 取得憑證、認證、建立 Google 雲端硬碟 API 服務物件
credential_path = os.path.join("./", 'google-ocr-credential.json')
store = Storage(credential_path)
credentials = store.get()
if not credentials or credentials.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    flow.user_agent = APPLICATION_NAME
    credentials = tools.run(flow, store)
    print('憑證儲存於：' + credential_path)
http = credentials.authorize(httplib2.Http())
service = discovery.build('drive', 'v3', http=http)

# chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")
# --------------------------------------------------


app = Flask(__name__)

line_bot_api = LineBotApi(
    'eGsaOBECCTQbmauJgf0PLC2LbvWEke/WRuFXuS0/bvLGtuOPwIh9Yng8+i2y07TIds7hWBAOFzKAPF7Iz9Yx5IoY6Op6mp83F8EEi93EHwD+ARqseWvZMzEvRbHRUVHKbq94Sfbkje3Of16k5IfAcgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0134d5ce9f1b5f94f0be216fd9db7a31')

newlink = []
newimg = []
gamename = []
gametab = []
gameprice = []
tagsRanking = []

allPageNum = []
def GamesParser(flag):
    for flag in range(16):
        flag1 = flag + 1
        newlink.clear()
        newimg.clear()
        gamename.clear()
        gametab.clear()
        gameprice.clear()
        driver = webdriver.Chrome('C:\selenium_driver_chrome\chromedriver.exe')
        alltext = ""

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:49.0) Gecko/20100101 Firefox/49.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-TW,zh;q=0.5",
            "Accept-Encoding": "gzip",
            "Connection": "keep-alive",
            "Cookie": "browserid=1178180757615078361; steamCountry=TW%7Cec9ee54d7b0da8ca2bade64a4cec7061; sessionid=97b065f7fc4fc75643e86564; timezoneOffset=28800,0; _ga=GA1.2.30895296.1571386387; strResponsiveViewPrefs=desktop; bGameHighlightAutoplayDisabled=false; _gid=GA1.2.523639413.1575597766; Steam_Language=tchinese; birthtime=880992001; lastagecheckage=2-0-1998; recentapps=%7B%221191210%22%3A1575620845%2C%22710920%22%3A1575618403%2C%221199880%22%3A1575617070%2C%221174370%22%3A1575616963%2C%22760810%22%3A1575611064%2C%22976730%22%3A1575610993%2C%221064220%22%3A1575606891%2C%221173900%22%3A1575606798%2C%22349270%22%3A1575606795%2C%22846470%22%3A1575606763%7D; app_impressions=1016920@1_2300_4__201|790740@1_2300_4__43|1191210@1_2300_4__103|585710@1_2300_4__43|1189230@1_2300_4__103|1192610@1_2300_4__103|936490@1_2300_4__103|1176020@1_2300_4__103|1179720@1_2300_4__103|760810@1_2300_4__103|1174370@1_2300_4__103|1065950@1_2300_4__103|648800@1_2300_4__40|1159540@1_2300_4__103|1171310@1_2300_4__103|1158910@1_2300_4__103|1161270@1_2300_4__103|617290@1_2300_4__hub-specials|418240@1_2300_4__hub-specials|1016920@1_2300_4__hub-specials|1174370@1_2300_4__hub-specials|1097420@1_2300_4__103|1168430@1_2300_4__103|617290@1_2300_4__201|790740@1_2300_4__43|1191210@1_2300_4__103"
        }

        if flag1 == 1:
            r = requests.get('https://store.steampowered.com/explore/new/', headers=headers)
            DBid = "1ybwjFk0pxH9HGaQQqnQR6usYNJq0ObsE"
            DBname = "new"
        elif flag1 == 2:
            r = requests.get('https://store.steampowered.com/specials', headers=headers)
            DBid = "1utJrJhlgO_pAzgsTfIQsLra7uaA0AmA1"
            DBname = "discount"
        elif flag1 == 3:
            r = requests.get('https://store.steampowered.com/tags/zh-tw/%E4%BC%91%E9%96%92/', headers=headers)
            DBid = "1C1DcUfZTnpEU-wZs_LXSETjW-HZcYfoV"
            DBname = "leisure"
        elif flag1 == 4:
            r = requests.get('https://store.steampowered.com/tags/zh-tw/%E5%86%92%E9%9A%AA/', headers=headers)
            DBid = "1-7MTYcw8UNY6pc8J3h6fw_IAquJoOzjF"
            DBname = "adventure"
        elif flag1 == 5:
            r = requests.get('https://store.steampowered.com/tags/zh-tw/%E5%8B%95%E4%BD%9C/', headers=headers)
            DBid = "1U_iDoIiGRKeAheiz-zeEVDnF8VgSPkxV"
            DBname = "action"
        elif flag1 == 6:
            r = requests.get('https://store.steampowered.com/tags/zh-tw/%E6%A8%A1%E6%93%AC/', headers=headers)
            DBid = "1qtWM1Ccq-Fn6voP8hZhg0vQnNC9M1WzK"
            DBname = "simulation"
        elif flag1 == 7:
            r = requests.get(
                'https://store.steampowered.com/tags/zh-tw/%E5%A4%A7%E5%9E%8B%E5%A4%9A%E4%BA%BA%E9%80%A3%E7%B7%9A/',
                headers=headers)
            DBid = "1HjSsF9KAVILQY2uMBBMr7CNxIJ_FSLe4"
            DBname = "mmo"
        elif flag1 == 8:
            r = requests.get('https://store.steampowered.com/tags/zh-tw/%E7%AB%B6%E9%80%9F/', headers=headers)
            DBid = "1viu1iox7JXLxQ0jQ1WI7VSkVBCLi_1GT"
            DBname = "racing"
        elif flag1 == 9:
            r = requests.get('https://store.steampowered.com/tags/zh-tw/%E8%A7%92%E8%89%B2%E6%89%AE%E6%BC%94/',
                             headers=headers)
            DBid = "1y36dbhMefvpOOWy4-Ru3tF68Xvi_USgH"
            DBname = "rpg"
        elif flag1 == 10:
            r = requests.get('https://store.steampowered.com/genre/Early%20Access/', headers=headers)
            DBid = "1cEomzBHVcXpsAs6GjF12tbu-_Q9UBuKs"
            DBname = "before"
        elif flag1 == 11:
            r = requests.get('https://store.steampowered.com/tags/zh-tw/%E7%8D%A8%E7%AB%8B/', headers=headers)
            DBid = "18srb4dM7naJOZ3CSUnUiNvcXUVD1KTin"
            DBname = "independent"
        elif flag1 == 12:
            r = requests.get('https://store.steampowered.com/tags/zh-tw/%E7%AD%96%E7%95%A5/', headers=headers)
            DBid = "1hAu31KAe49kWfxIbVeODrIOgnBJCXdGZ"
            DBname = "strategy"
        elif flag1 == 13:
            r = requests.get('https://store.steampowered.com/tags/zh-tw/%E9%81%8B%E5%8B%95/', headers=headers)
            DBid = "1RInc3Wm1bu8V8oMq_vhATN_spJ3Vij-l"
            DBname = "sports"
        elif flag1 == 14:
            r = requests.get('https://store.steampowered.com/vr/', headers=headers)
            DBid = "1qMvvwXano3lac6LYfG_EvWu6jkbx37CX"
            DBname = "vr"
        elif flag1 == 15:
            r = requests.get('https://store.steampowered.com/updated/all/', headers=headers)
            DBid = "1E4eqTAj9buLXt5Qb58UaUYXvwU4EG4Dd"
            DBname = "lastup"
        elif flag1 == 16:
            r = requests.get('https://store.steampowered.com/genre/Free%20to%20Play/', headers=headers)
            DBid = "10Sm1QJjXhVWGgYF3MjF15wNbpIhfGwyk"
            DBname = "free"

        # 確認是否下載成功
        if r.status_code == requests.codes.ok:
            driver.get(r.url)
            # driver.get(r.url)
            # 以 BeautifulSoup 解析 HTML 程式碼
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            # print('This is html')
            # print(driver.page_source)

            # allPageNum = soup.find_all('span', class_='paged_items_paging_pagelink')
            try:
                allPageNumPre = soup.find('span', id='NewReleases_links')
                allPageNum = allPageNumPre.find_all('span', class_='paged_items_paging_pagelink')
                totalPages = int(allPageNum[len(allPageNum) - 1].text)
            except:
                totalPages = 2

            # name_counter = 1
            page = 1;
            print(totalPages)
            while page <= totalPages - 1:
                # if(page == 5):
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # names = soup.find_all('div', class_='tab_item_name', limit=15)
                links = soup.find_all('a', class_='tab_item', limit=15)
                imgs = soup.find_all('img', class_='tab_item_cap_img', limit=15)
                name = soup.find_all('div', class_='tab_item_name', limit=15)
                price = soup.find_all('a', class_='tab_item', limit=15)
                taball = soup.find_all('div', class_='tab_item_top_tags', limit=15)

                # gamerandom = random.sample(range(0, 15), 15)

                for i in range(15):
                    tab = taball[i].find_all('span', class_='top_tag')
                    newlink.append(links[i].get('href'))
                    newimg.append(imgs[i].get('src'))
                    gamename.append(name[i].text)
                    try:
                        if price[i].find('div', class_='discount_final_price').text != "免費遊玩":
                            gameprice.append(price[i].find('div', class_='discount_final_price').text)
                        else:
                            gameprice.append(price[i].find('div', class_='discount_final_price').text)
                    except:
                        gameprice.append("暫無")
                    str = ""
                    for j in tab:
                        str += ''.join(j.text)
                    gametab.append(str)
                    alltext = alltext + gamename[i + (page - 1)*15] + ";" + newimg[i + (page - 1)*15] + ";" + newlink[i + (page - 1)*15] + ";" + gameprice[i + (page - 1)*15] + ";" + gametab[i + (page - 1)*15] + "\n"

                try:
                    driver.find_element_by_id("NewReleases_btn_next").click()
                except:
                    print("只有一頁")
                page = page + 1
                time.sleep(2)  # 睡2秒让网页加载完再去读它的html代码
                links.clear()
                imgs.clear()
                name.clear()
                price.clear()
                taball.clear()
                # page = page + 1
                # driver.find_element_by_id("NewReleases_btn_next").click()
                # time.sleep(2)  # 睡2秒让网页加载完再去读它的html代码
            # print('this is button')
            # print(driver.find_elements_by_id('div#NewReleasesTable').pop)


            g = open(os.path.join("./gameDB/", DBname + '.txt'), 'w', encoding='utf-8')
            g.write(alltext)
            g.close()
            uploadFile(DBid, os.path.join("./gameDB/", DBname + '.txt'), 'text/txt')
            driver.quit()


def GamesParser_bestseller():
    newlink.clear()
    newimg.clear()
    gamename.clear()
    gametab.clear()
    gameprice.clear()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:49.0) Gecko/20100101 Firefox/49.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-TW,zh;q=0.5",
        "Accept-Encoding": "gzip",
        "Connection": "keep-alive",
        "Cookie": "browserid=1178180757615078361; steamCountry=TW%7Cec9ee54d7b0da8ca2bade64a4cec7061; sessionid=97b065f7fc4fc75643e86564; timezoneOffset=28800,0; _ga=GA1.2.30895296.1571386387; strResponsiveViewPrefs=desktop; bGameHighlightAutoplayDisabled=false; _gid=GA1.2.523639413.1575597766; Steam_Language=tchinese; birthtime=880992001; lastagecheckage=2-0-1998; recentapps=%7B%221191210%22%3A1575620845%2C%22710920%22%3A1575618403%2C%221199880%22%3A1575617070%2C%221174370%22%3A1575616963%2C%22760810%22%3A1575611064%2C%22976730%22%3A1575610993%2C%221064220%22%3A1575606891%2C%221173900%22%3A1575606798%2C%22349270%22%3A1575606795%2C%22846470%22%3A1575606763%7D; app_impressions=1016920@1_2300_4__201|790740@1_2300_4__43|1191210@1_2300_4__103|585710@1_2300_4__43|1189230@1_2300_4__103|1192610@1_2300_4__103|936490@1_2300_4__103|1176020@1_2300_4__103|1179720@1_2300_4__103|760810@1_2300_4__103|1174370@1_2300_4__103|1065950@1_2300_4__103|648800@1_2300_4__40|1159540@1_2300_4__103|1171310@1_2300_4__103|1158910@1_2300_4__103|1161270@1_2300_4__103|617290@1_2300_4__hub-specials|418240@1_2300_4__hub-specials|1016920@1_2300_4__hub-specials|1174370@1_2300_4__hub-specials|1097420@1_2300_4__103|1168430@1_2300_4__103|617290@1_2300_4__201|790740@1_2300_4__43|1191210@1_2300_4__103"
    }

    r = requests.get('https://store.steampowered.com/search/?filter=topsellers&ignore_preferences=1', headers=headers)

    # 確認是否下載成功
    if r.status_code == requests.codes.ok:

        # 以 BeautifulSoup 解析 HTML 程式碼
        soup = BeautifulSoup(r.text, 'html.parser')

        # 以 CSS 的 class 抓出各類遊戲資訊

        # 可能links要改用href的方式抓
        links = soup.find_all('a', class_='search_result_row', limit=50)
        imgs = soup.find_all('div', class_='col search_capsule', limit=50)
        name = soup.find_all('span', class_='title', limit=50)

        appLinks = []
        appImgs = []
        appName = []

        for i in range(50):
            link = links[i].get('href')
            if 'app' in link:
                appLinks.append(links[i])
                appImgs.append(imgs[i])
                appName.append(name[i])

        gamerandom = random.sample(range(0, len(appLinks)), 10)

        for i in range(10):
            price = None
            newlink.append(appLinks[gamerandom[i]].get('href'))
            newimg.append(appImgs[gamerandom[i]].find('img').get('src'))
            gamename.append(appName[gamerandom[i]].text)

            r2 = requests.get(newlink[i], headers=headers)
            # 確認是否下載成功
            if r2.status_code == requests.codes.ok:
                # 以 BeautifulSoup 解析 HTML 程式碼
                soup2 = BeautifulSoup(r2.text, 'html.parser')

                price = soup2.find('div', class_='game_purchase_price price')
                if price != None:
                    gameprice.append(price.text.strip('\r').strip('\n').strip('\t') + " (美金)")
                else:
                    price = soup2.find('div', class_='discount_final_price')
                    if price != None:
                        gameprice.append(price.text.strip('\r').strip('\n').strip('\t') + " (美金)")
                    else:
                        gameprice.append("月費遊戲")

                tag = soup2.find_all('a', class_='app_tag', limit=5)
                str = ""
                for j in tag:
                    if j != tag[len(tag)-1]:
                        str += ''.join(j.text.strip('\r').strip('\n').strip('\t') + ', ')
                    else:
                        str += ''.join(j.text.strip('\r').strip('\n').strip('\t'))
                gametab.append(str)


def GamesParser_ComingSoon():
    newlink.clear()
    newimg.clear()
    gamename.clear()
    gametab.clear()
    gameprice.clear()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:49.0) Gecko/20100101 Firefox/49.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-TW,zh;q=0.5",
        "Accept-Encoding": "gzip",
        "Connection": "keep-alive",
        "Cookie": "browserid=1178180757615078361; steamCountry=TW%7Cec9ee54d7b0da8ca2bade64a4cec7061; sessionid=97b065f7fc4fc75643e86564; timezoneOffset=28800,0; _ga=GA1.2.30895296.1571386387; strResponsiveViewPrefs=desktop; bGameHighlightAutoplayDisabled=false; _gid=GA1.2.523639413.1575597766; Steam_Language=tchinese; birthtime=880992001; lastagecheckage=2-0-1998; recentapps=%7B%221191210%22%3A1575620845%2C%22710920%22%3A1575618403%2C%221199880%22%3A1575617070%2C%221174370%22%3A1575616963%2C%22760810%22%3A1575611064%2C%22976730%22%3A1575610993%2C%221064220%22%3A1575606891%2C%221173900%22%3A1575606798%2C%22349270%22%3A1575606795%2C%22846470%22%3A1575606763%7D; app_impressions=1016920@1_2300_4__201|790740@1_2300_4__43|1191210@1_2300_4__103|585710@1_2300_4__43|1189230@1_2300_4__103|1192610@1_2300_4__103|936490@1_2300_4__103|1176020@1_2300_4__103|1179720@1_2300_4__103|760810@1_2300_4__103|1174370@1_2300_4__103|1065950@1_2300_4__103|648800@1_2300_4__40|1159540@1_2300_4__103|1171310@1_2300_4__103|1158910@1_2300_4__103|1161270@1_2300_4__103|617290@1_2300_4__hub-specials|418240@1_2300_4__hub-specials|1016920@1_2300_4__hub-specials|1174370@1_2300_4__hub-specials|1097420@1_2300_4__103|1168430@1_2300_4__103|617290@1_2300_4__201|790740@1_2300_4__43|1191210@1_2300_4__103"
    }

    r = requests.get('https://store.steampowered.com/explore/upcoming/', headers=headers)

    # 確認是否下載成功
    if r.status_code == requests.codes.ok:

        # 以 BeautifulSoup 解析 HTML 程式碼
        soup = BeautifulSoup(r.text, 'html.parser')
        # print(r.text)

        # 以 CSS 的 class 抓出各類遊戲資訊
        links = soup.find_all('a', class_='tab_item', limit=15)
        imgs = soup.find_all('img', class_='tab_item_cap_img', limit=15)
        name = soup.find_all('div', class_='tab_item_name', limit=15)
        price = soup.find_all('a', class_='tab_item', limit=15)
        taball = soup.find_all('div', class_='tab_item_top_tags', limit=15)

        gamerandom = random.sample(range(0, 15), 10)

        for i in range(10):
            tab = taball[gamerandom[i]].find_all('span', class_='top_tag')
            newlink.append(links[gamerandom[i]].get('href'))
            newimg.append(imgs[gamerandom[i]].get('src'))
            gamename.append(name[gamerandom[i]].text)
            try:
                if price[gamerandom[i]].find('div', class_='discount_final_price').text != "免費遊玩":
                    gameprice.append(price[gamerandom[i]].find('div', class_='discount_final_price').text + " (美金)")
                else:
                    gameprice.append(price[gamerandom[i]].find('div', class_='discount_final_price').text)
            except:
                gameprice.append("暫無")
            str = ""
            for j in tab:
                print('this is j')
                print(j)
                str += ''.join(j.text)
            gametab.append(str)


@app.route("/")
def home():
    return 'home OK'


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text  # message from user
    uid = event.source.user_id  # user id

    if message == "#使用說明":

        text1 = "歡迎使用NTUSteam!!!~~~\n"
        text11 = "以下為功能介紹,並介紹如何使用此款產品:\n"
        text12 = "點擊(分類按鈕)\n\t即可檢視遊戲類別\n"
        texta = "------------------------------\n"
        text2 = "點擊欲查詢類別按鈕或(輸入#類別名稱)範例:#動作\n\t即可查看有關該類別的遊戲(隨機5個)\n"
        textb = "------------------------------\n"
        text3 = "點擊(下殺特賣按鈕)\n\t即可檢視目前折扣中之遊戲\n"
        textc = "------------------------------\n"
        text4 = "點擊(新發售按鈕)\n\t即可觀看目前新發售之遊戲\n"
        textd = "------------------------------\n"
        text5 = "點擊(#遊戲名稱)\n\t即會顯示該遊戲相關之介紹\n"
        texte = "------------------------------\n"
        text6 = "點擊(推薦清單按鈕)\n\t即會根據您喜歡的遊戲類別進行推薦\n"
        textf = "------------------------------\n"
        text7 = "點擊(+遊戲名稱)\n\t即會將遊戲加入到我的最愛\n"
        textg = "------------------------------\n"
        text8 = "點擊(我的最愛按鈕)\n\t即可查看我的最愛清單中您所加入的遊戲"

        message = text1 + text11 + text12 + texta + text2 + textb + text3 + textc + text4 + textd + text5 + texte + text6 + textf + text7 + textg + text8
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))

        # line_bot_api.reply_message(
        #    event.reply_token,
        #    TextSendMessage(text=event.message.text))



    elif message == "#分類":
        tab = ['最近更新', '即將發行', '暢銷商品', '免費遊玩', '大型多人連線', '競速', '角色扮演', '搶先體驗', '休閒', '冒險', '動作', '模擬', '獨立', '策略', '運動']
        carousel = CarouselContainer()
        for i in range(5):
            bubble = BubbleContainer(
                direction='ltr',
                footer=BoxComponent(
                    layout='vertical',
                    spacing='xs',
                    contents=[
                        ButtonComponent(
                            height='sm',
                            action=MessageAction(label=tab[(i * 3) - 2], text=('#' + tab[(i * 3) - 2])),
                        ),
                        ButtonComponent(
                            height='sm',
                            action=MessageAction(label=tab[(i * 3) - 1], text=('#' + tab[(i * 3) - 1])),
                        ),
                        ButtonComponent(
                            height='sm',
                            action=MessageAction(label=tab[(i * 3)], text=('#' + tab[(i * 3)])),
                        ),
                    ],
                ),
            )
            carousel.contents.append(bubble)
        bubble2 = BubbleContainer(
            direction='ltr',
            footer=BoxComponent(
                layout='vertical',
                spacing='xs',
                contents=[
                    ButtonComponent(
                        height='sm',
                        action=MessageAction(label='虛擬實境', text='#虛擬實境'),
                    ),
                ],
            ),
        )
        carousel.contents.append(bubble2)

        message = FlexSendMessage(alt_text="請輸入#分類(你要找的)", contents=carousel)
        line_bot_api.reply_message(event.reply_token, message)

    elif message == "#休閒" or message == "#冒險" or message == "#動作" or message == "#模擬" or message == "#大型多人連線" or message == "#競速" or message == "#角色扮演" or message == "#搶先體驗" or message == "#獨立" or message == "#策略" or message == "#運動" or message == "#虛擬實境" or message == "#最近更新" or message == "#即將發行" or message == "#暢銷商品" or message == "#免費遊玩" or message == "#新發售" or message == "#下殺特賣" or message == "#推薦" or message == "#隨機推薦":
        title = message.split('#')[1]
        index = title + "類遊戲"
        if message == "#休閒":
            GamesParser(3)
        elif message == "#冒險":
            GamesParser(4)
        elif message == "#動作":
            GamesParser(5)
        elif message == "#模擬":
            GamesParser(6)
        elif message == "#大型多人連線":
            GamesParser(7)
        elif message == "#競速":
            GamesParser(8)
        elif message == "#角色扮演":
            GamesParser(9)
        elif message == "#搶先體驗":
            GamesParser(10)
        elif message == "#獨立":
            GamesParser(11)
        elif message == "#策略":
            GamesParser(12)
        elif message == "#運動":
            GamesParser(13)
        elif message == "#虛擬實境":
            GamesParser(14)
        elif message == "#最近更新":
            GamesParser(15)
        elif message == "#即將發行":
            GamesParser_ComingSoon()
        elif message == "#暢銷商品":
            GamesParser_bestseller()
        elif message == "#免費遊玩":
            GamesParser(16)
        elif message == "#新發售":
            GamesParser(1)
            title = "新發售"
            index = "最新發行遊戲,快來體驗"
        elif message == "#下殺特賣":
            GamesParser(2)
            title = "下殺特賣"
            index = "要撿便宜都看這"
        elif message == "#推薦":
            if game_recommend(uid):
                title = "專屬推薦清單"
                index = "屬於你的專屬推薦"
            else:
                title = "隨機推薦清單"
                index = "由於我的最愛沒有東西，因此隨機推薦您一些遊戲"
        elif message == "#隨機推薦":
            title = "隨機推薦清單"
            index = "隨機推薦您一些遊戲"
            game_randomRecommed()

        # carousel = CarouselContainer()
        # for i in range(10):
        #     # try:
        #     print(newlink)
        #     bubble = BubbleContainer(
        #         direction='ltr',
        #         header=BoxComponent(
        #             layout='vertical',
        #             contents=[
        #                 # title
        #                 TextComponent(text=title, weight='bold', size='xl'),
        #                 # info
        #                 BoxComponent(
        #                     layout='vertical',
        #                     margin='lg',
        #                     spacing='sm',
        #                     contents=[
        #                         BoxComponent(
        #                             layout='baseline',
        #                             spacing='sm',
        #                             contents=[
        #                                 TextComponent(
        #                                     text=index,
        #                                     wrap=True,
        #                                     color='#666666',
        #                                     size='xs',
        #                                     flex=5
        #                                 )
        #                             ],
        #                         ),
        #                     ],
        #                 )
        #             ],
        #         ),
        #         body=BoxComponent(
        #             layout='vertical',
        #             spacing='xl',
        #             contents=[
        #                 # 遊戲模板
        #                 BoxComponent(
        #                     layout='horizontal',
        #                     spacing='sm',
        #                     contents=[
        #                         # callAction, separator, websiteAction
        #                         SpacerComponent(size='sm'),
        #                         # callAction
        #                         ImageComponent(
        #                             url=newimg[i],
        #                             size='full',
        #                             aspect_ratio='20:13',
        #                             aspect_mode='fit',
        #                             action=URIAction(
        #                                 uri=newlink[i])
        #                         ),
        #                         # separator
        #                         SeparatorComponent(),
        #                         # websiteAction
        #                         BoxComponent(
        #                             layout='vertical',
        #                             margin='md',
        #                             contents=[
        #                                 TextComponent(
        #                                     text=gamename[i],
        #                                     color='#F74018',
        #                                     size='sm'
        #                                 ),
        #
        #                                 SeparatorComponent(),
        #
        #                                 BoxComponent(
        #                                     layout='baseline',
        #                                     spacing='sm',
        #                                     contents=[
        #                                         TextComponent(
        #                                             text="遊戲價格:",
        #                                             color='#aaaaaa',
        #                                             size='xxs',
        #                                             flex=1)
        #                                     ],
        #                                 ),
        #                                 SeparatorComponent(),
        #
        #                                 BoxComponent(
        #                                     layout='baseline',
        #                                     spacing='sm',
        #                                     contents=[
        #                                         TextComponent(
        #                                             text=gameprice[i],
        #                                             wrap=True,
        #                                             color='#666666',
        #                                             size='xxs',
        #                                             action=URIAction(label='CALL', uri='tel:02-2368-0254'),
        #                                             flex=5
        #                                         )
        #                                     ],
        #                                 ),
        #                                 SeparatorComponent(),
        #
        #                                 BoxComponent(
        #                                     layout='baseline',
        #                                     spacing='sm',
        #                                     contents=[
        #                                         TextComponent(
        #                                             text="遊戲標籤:",
        #                                             color='#aaaaaa',
        #                                             size='xxs',
        #                                             flex=1
        #                                         )
        #                                     ],
        #                                 ),
        #                                 SeparatorComponent(),
        #
        #                                 BoxComponent(
        #                                     layout='baseline',
        #                                     spacing='sm',
        #                                     contents=[
        #                                         TextComponent(
        #                                             text=gametab[i],
        #                                             wrap=True,
        #                                             color='#666666',
        #                                             size='xxs',
        #                                             flex=5,
        #                                         ),
        #                                     ],
        #                                 ),
        #                             ]
        #                         ),
        #                     ]
        #                 ),
        #
        #             ]
        #         ),
        #         footer=BoxComponent(
        #             layout='vertical',
        #             spacing='xs',
        #             contents=[
        #                 ButtonComponent(
        #                     height='sm',
        #                     action=MessageAction(label='查看評論', text=(
        #                             '*' + newlink[i].split('https://store.steampowered.com/app/')[1].split('/')[
        #                         0])),
        #                 ),
        #                 ButtonComponent(
        #                     height='sm',
        #                     action=MessageAction(label='加入/移除最愛', text=(
        #                             '^' + newlink[i].split('https://store.steampowered.com/app/')[1].split('/')[
        #                         0])),
        #                 ),
        #             ],
        #         ),
        #     )
        #     # except:
        #
        #     carousel.contents.append(bubble)
        #
        # message = FlexSendMessage(alt_text="請輸入#分類(你要找的)", contents=carousel)
        # line_bot_api.reply_message(event.reply_token, message)
        # print(gameprice)

    elif message.find('^') != -1:
        # json處理
        r = ('https://store.steampowered.com/app/' + message.split('^')[1] + '/')
        text = (r)
        iddict = {}
        downloadFile('1C1AhkK_LeBZROLTH5EPEdGlfQBAj9oQ5', 'uid.json')
        with open(os.path.join("./", 'uid.json'), 'r') as readJ:
            iddict = json.load(readJ)
            readJ.close()
        with open(os.path.join("./", 'uid.json'), 'w') as f:
            # 儲存到資料庫
            if uid in iddict:
                downloadFile(iddict[uid], uid + '.txt')
                g = open(os.path.join("./", uid + '.txt'), 'r', encoding='utf-8')
                favo = ''
                for line in g:
                    favo += line
                g.close()
                if favo.find(r) != -1:
                    g = open(os.path.join("./", uid + '.txt'), 'w', encoding='utf-8')
                    favo = favo.replace((text + '\n'), "")
                    g.truncate()
                    if favo == '':
                        g.write(favo + 'None')
                    else:
                        g.write(favo)
                    line_bot_api.reply_message(event.reply_token, TextSendMessage('已將' + r + ' 從最愛中移除'))
                elif favo == 'None':
                    g = open(os.path.join("./", uid + '.txt'), 'w', encoding='utf-8')
                    g.truncate()
                    g.write(text + '\n')
                    line_bot_api.reply_message(event.reply_token, TextSendMessage('已新增' + r + ' 到最愛中'))
                else:
                    g = open(os.path.join("./", uid + '.txt'), 'a', encoding='utf-8')
                    g.write(text + '\n')
                    line_bot_api.reply_message(event.reply_token, TextSendMessage('已新增' + r + ' 到最愛中'))
                g.close()
                uploadFile(iddict[uid], os.path.join("./", uid + '.txt'), 'text/txt')
                result = json.dumps(iddict)
                f.write(result)
            else:
                g = open(os.path.join("./", uid + '.txt'), 'w', encoding='utf-8')
                g.write(text + '\n')
                g.close()
                line_bot_api.reply_message(event.reply_token, TextSendMessage('已新增' + r + ' 到最愛中'))
                uiddict = {uid: newFile(uid + '.txt', os.path.join("./", uid + '.txt'), 'text/txt')}
                iddict.update(uiddict)
                result = json.dumps(iddict)
                f.write(result)
            f.close()
            uploadFile('1C1AhkK_LeBZROLTH5EPEdGlfQBAj9oQ5', os.path.join("./", 'uid.json'), 'application/json')
            try:
                os.remove(os.path.join("./", uid + '.txt'))
                os.remove(os.path.join("./", 'uid.json'))
            except OSError as e:
                print(e)
            else:
                print("File is deleted successfully")


    elif message.find('*') != -1:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:49.0) Gecko/20100101 Firefox/49.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-TW,zh;q=0.5",
            "Accept-Encoding": "gzip",
            "Connection": "keep-alive",
            "Cookie": "browserid=1178180757615078361; steamCountry=TW%7Cec9ee54d7b0da8ca2bade64a4cec7061; sessionid=97b065f7fc4fc75643e86564; timezoneOffset=28800,0; _ga=GA1.2.30895296.1571386387; strResponsiveViewPrefs=desktop; bGameHighlightAutoplayDisabled=false; _gid=GA1.2.523639413.1575597766; Steam_Language=tchinese; birthtime=880992001; lastagecheckage=2-0-1998; recentapps=%7B%221191210%22%3A1575620845%2C%22710920%22%3A1575618403%2C%221199880%22%3A1575617070%2C%221174370%22%3A1575616963%2C%22760810%22%3A1575611064%2C%22976730%22%3A1575610993%2C%221064220%22%3A1575606891%2C%221173900%22%3A1575606798%2C%22349270%22%3A1575606795%2C%22846470%22%3A1575606763%7D; app_impressions=1016920@1_2300_4__201|790740@1_2300_4__43|1191210@1_2300_4__103|585710@1_2300_4__43|1189230@1_2300_4__103|1192610@1_2300_4__103|936490@1_2300_4__103|1176020@1_2300_4__103|1179720@1_2300_4__103|760810@1_2300_4__103|1174370@1_2300_4__103|1065950@1_2300_4__103|648800@1_2300_4__40|1159540@1_2300_4__103|1171310@1_2300_4__103|1158910@1_2300_4__103|1161270@1_2300_4__103|617290@1_2300_4__hub-specials|418240@1_2300_4__hub-specials|1016920@1_2300_4__hub-specials|1174370@1_2300_4__hub-specials|1097420@1_2300_4__103|1168430@1_2300_4__103|617290@1_2300_4__201|790740@1_2300_4__43|1191210@1_2300_4__103"
        }
        r = requests.get(
            'https://steamcommunity.com/app/' + message.split('*')[1] + '/reviews/?filterLanguage=tchinese',
            headers=headers)
        # 確認是否下載成功
        output = ''
        cnt = 0
        if r.status_code == requests.codes.ok:
            # 以 BeautifulSoup 解析 HTML 程式碼
            soup = BeautifulSoup(r.text, 'html.parser')
        # print(r.text)

        # 以 CSS 的 class 抓出各類遊戲資訊
        reviews = soup.find_all('div', class_='apphub_Card modalContentLink interactable')
        for review in reviews:
            nick = review.find('div', class_='apphub_CardContentAuthorBlock tall').text
        try:
            content = review.find('div', class_='apphub_CardTextContent')
            title = review.find('div', class_='title').text
            hour = review.find('div', class_='hours').text.split(' ')[1].split(' ')[0]
            comment = review.find('div', {'class': 'apphub_CardTextContent'}).text
            if cnt < 3:
                output += (nick.split('此')[0].split('\n')[6] + ' ' + title + ' ' + '遊玩時數' + hour + ' ' +
                           comment.strip('\t').split('日')[1].split('\n')[1].strip('\t') + '\n\n')
            cnt += 1
        except:
            output = '不好意思，此遊戲尚無任何中文評論'
        if output == '':
            output = '不好意思，此遊戲尚無任何中文評論'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(output))

        # --------------------------------------------------





    elif message == "#願望清單":
        iddict = {}
        newlink.clear()
        newimg.clear()
        gamename.clear()
        gametab.clear()
        gameprice.clear()
        downloadFile('1C1AhkK_LeBZROLTH5EPEdGlfQBAj9oQ5', 'uid.json')
        with open(os.path.join("./", 'uid.json'), 'r') as readJ:
            iddict = json.load(readJ)
            readJ.close()
        # 讀取從資料庫
        if uid in iddict:
            downloadFile(iddict[uid], uid + '.txt')
            g = open(os.path.join("./", uid + '.txt'), 'r', encoding='utf-8')
            output = ''
            num = 0
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:49.0) Gecko/20100101 Firefox/49.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "zh-TW,zh;q=0.5",
                "Accept-Encoding": "gzip",
                "Connection": "keep-alive",
                "Cookie": "browserid=1178180757615078361; steamCountry=TW%7Cec9ee54d7b0da8ca2bade64a4cec7061; sessionid=97b065f7fc4fc75643e86564; timezoneOffset=28800,0; _ga=GA1.2.30895296.1571386387; strResponsiveViewPrefs=desktop; bGameHighlightAutoplayDisabled=false; _gid=GA1.2.523639413.1575597766; Steam_Language=tchinese; birthtime=880992001; lastagecheckage=2-0-1998; recentapps=%7B%221191210%22%3A1575620845%2C%22710920%22%3A1575618403%2C%221199880%22%3A1575617070%2C%221174370%22%3A1575616963%2C%22760810%22%3A1575611064%2C%22976730%22%3A1575610993%2C%221064220%22%3A1575606891%2C%221173900%22%3A1575606798%2C%22349270%22%3A1575606795%2C%22846470%22%3A1575606763%7D; app_impressions=1016920@1_2300_4__201|790740@1_2300_4__43|1191210@1_2300_4__103|585710@1_2300_4__43|1189230@1_2300_4__103|1192610@1_2300_4__103|936490@1_2300_4__103|1176020@1_2300_4__103|1179720@1_2300_4__103|760810@1_2300_4__103|1174370@1_2300_4__103|1065950@1_2300_4__103|648800@1_2300_4__40|1159540@1_2300_4__103|1171310@1_2300_4__103|1158910@1_2300_4__103|1161270@1_2300_4__103|617290@1_2300_4__hub-specials|418240@1_2300_4__hub-specials|1016920@1_2300_4__hub-specials|1174370@1_2300_4__hub-specials|1097420@1_2300_4__103|1168430@1_2300_4__103|617290@1_2300_4__201|790740@1_2300_4__43|1191210@1_2300_4__103"
            }
            for line in g:
                if line == 'None':
                    output = 'None'
                else:
                    r = requests.get(line, headers=headers)
                    if r.status_code == requests.codes.ok:
                        # 以 BeautifulSoup 解析 HTML 程式碼
                        num += 1
                        soup = BeautifulSoup(r.text, 'html.parser')
                        name = soup.find_all('div', class_='apphub_AppName', limit=1)
                        gamename.append(name[0].text)
                        price = soup.find('div', class_='game_purchase_price price')
                        if price != None:
                            gameprice.append(price.text.strip('\r').strip('\n').strip('\t') + " (美金)")
                        else:
                            price = soup.find('div', class_='discount_final_price')
                            if price != None:
                                gameprice.append(price.text.strip('\r').strip('\n').strip('\t') + " (美金)")
                            else:
                                gameprice.append("月費遊戲")
                        # price = soup.find_all('div', class_='game_purchase_price price', limit=2)
                        # if len(price) == 0:
                        #     price = soup.find_all('div', class_='discount_final_price', limit=1)
                        # gameprice.append(price[0].text.strip('\r').strip('\n').strip('\t') + " (美金)")
                        img = soup.find_all('img', class_='game_header_image_full', limit=1)
                        newimg.append(img[0].get('src'))
                        tag = soup.find_all('a', class_='app_tag', limit=5)
                        str = ""
                        for j in tag:
                            if j != tag[len(tag) - 1]:
                                str += ''.join(j.text.strip('\r').strip('\n').strip('\t') + ', ')
                            else:
                                str += ''.join(j.text.strip('\r').strip('\n').strip('\t'))
                        gametab.append(str)
                        # gametab.append(tag[0].text.strip('\r').strip('\n').strip('\t'))
                        newlink.append(line.strip('\n'))
                        # output = output + name[0].text + "\n" + line
            g.close()

            if output == 'None':
                line_bot_api.reply_message(event.reply_token, TextSendMessage('我的最愛中沒有項目'))
            else:
                # line_bot_api.reply_message(event.reply_token, TextSendMessage(output))
                carousel = CarouselContainer()
                for i in range(num):
                    bubble = BubbleContainer(
                        direction='ltr',
                        header=BoxComponent(
                            layout='vertical',
                            contents=[
                                # title
                                TextComponent(text='我的最愛', weight='bold', size='xl'),
                                # info
                                BoxComponent(
                                    layout='vertical',
                                    margin='lg',
                                    spacing='sm',
                                    contents=[
                                        BoxComponent(
                                            layout='baseline',
                                            spacing='sm',
                                            contents=[
                                                TextComponent(
                                                    text='你的專屬備忘錄',
                                                    wrap=True,
                                                    color='#666666',
                                                    size='xs',
                                                    flex=5
                                                )
                                            ],
                                        ),
                                    ],
                                )
                            ],
                        ),
                        body=BoxComponent(
                            layout='vertical',
                            spacing='xl',
                            contents=[
                                # 遊戲模板
                                BoxComponent(
                                    layout='horizontal',
                                    spacing='sm',
                                    contents=[
                                        # callAction, separator, websiteAction
                                        SpacerComponent(size='sm'),
                                        # callAction
                                        ImageComponent(
                                            url=newimg[i],
                                            size='full',
                                            aspect_ratio='20:13',
                                            aspect_mode='fit',
                                            action=URIAction(
                                                uri=newlink[i])
                                        ),
                                        # separator
                                        SeparatorComponent(),
                                        # websiteAction
                                        BoxComponent(
                                            layout='vertical',
                                            margin='md',
                                            contents=[
                                                TextComponent(
                                                    text=gamename[i],
                                                    color='#F74018',
                                                    size='sm'
                                                ),

                                                SeparatorComponent(),

                                                BoxComponent(
                                                    layout='baseline',
                                                    spacing='sm',
                                                    contents=[
                                                        TextComponent(
                                                            text="遊戲價格:",
                                                            color='#aaaaaa',
                                                            size='xxs',
                                                            flex=1)
                                                    ],
                                                ),
                                                SeparatorComponent(),

                                                BoxComponent(
                                                    layout='baseline',
                                                    spacing='sm',
                                                    contents=[
                                                        TextComponent(
                                                            text=gameprice[i],
                                                            wrap=True,
                                                            color='#666666',
                                                            size='xxs',
                                                            action=URIAction(label='CALL', uri='tel:02-2368-0254'),
                                                            flex=5
                                                        )
                                                    ],
                                                ),
                                                SeparatorComponent(),

                                                BoxComponent(
                                                    layout='baseline',
                                                    spacing='sm',
                                                    contents=[
                                                        TextComponent(
                                                            text="遊戲標籤:",
                                                            color='#aaaaaa',
                                                            size='xxs',
                                                            flex=1
                                                        )
                                                    ],
                                                ),
                                                SeparatorComponent(),

                                                BoxComponent(
                                                    layout='baseline',
                                                    spacing='sm',
                                                    contents=[
                                                        TextComponent(
                                                            text=gametab[i],
                                                            wrap=True,
                                                            color='#666666',
                                                            size='xxs',
                                                            flex=5,
                                                        ),
                                                    ],
                                                ),
                                            ]
                                        ),
                                    ]
                                ),

                            ]
                        ),
                        footer=BoxComponent(
                            layout='vertical',
                            spacing='xs',
                            contents=[
                                ButtonComponent(
                                    height='sm',
                                    action=MessageAction(label='查看評論', text=(
                                            '*' + newlink[i].split('https://store.steampowered.com/app/')[1].split('/')[
                                        0])),
                                ),
                                ButtonComponent(
                                    height='sm',
                                    action=MessageAction(label='移除最愛', text=(
                                            '^' + newlink[i].split('https://store.steampowered.com/app/')[1].split('/')[
                                        0])),
                                ),
                            ],
                        ),
                    )
                    carousel.contents.append(bubble)
                message = FlexSendMessage(alt_text="請輸入#分類(你要找的)", contents=carousel)
                line_bot_api.reply_message(event.reply_token, message)
            try:
                os.remove(os.path.join("./", uid + '.txt'))
                os.remove(os.path.join("./", 'uid.json'))
            except OSError as e:
                print(e)
            else:
                print("File is deleted successfully")
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage('我的最愛中沒有項目'))

    elif message.find('#查詢') != -1:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:49.0) Gecko/20100101 Firefox/49.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-TW,zh;q=0.5",
            "Accept-Encoding": "gzip",
            "Connection": "keep-alive",
            "Cookie": "browserid=1178180757615078361; steamCountry=TW%7Cec9ee54d7b0da8ca2bade64a4cec7061; sessionid=97b065f7fc4fc75643e86564; timezoneOffset=28800,0; _ga=GA1.2.30895296.1571386387; strResponsiveViewPrefs=desktop; bGameHighlightAutoplayDisabled=false; _gid=GA1.2.523639413.1575597766; Steam_Language=tchinese; birthtime=880992001; lastagecheckage=2-0-1998; recentapps=%7B%221191210%22%3A1575620845%2C%22710920%22%3A1575618403%2C%221199880%22%3A1575617070%2C%221174370%22%3A1575616963%2C%22760810%22%3A1575611064%2C%22976730%22%3A1575610993%2C%221064220%22%3A1575606891%2C%221173900%22%3A1575606798%2C%22349270%22%3A1575606795%2C%22846470%22%3A1575606763%7D; app_impressions=1016920@1_2300_4__201|790740@1_2300_4__43|1191210@1_2300_4__103|585710@1_2300_4__43|1189230@1_2300_4__103|1192610@1_2300_4__103|936490@1_2300_4__103|1176020@1_2300_4__103|1179720@1_2300_4__103|760810@1_2300_4__103|1174370@1_2300_4__103|1065950@1_2300_4__103|648800@1_2300_4__40|1159540@1_2300_4__103|1171310@1_2300_4__103|1158910@1_2300_4__103|1161270@1_2300_4__103|617290@1_2300_4__hub-specials|418240@1_2300_4__hub-specials|1016920@1_2300_4__hub-specials|1174370@1_2300_4__hub-specials|1097420@1_2300_4__103|1168430@1_2300_4__103|617290@1_2300_4__201|790740@1_2300_4__43|1191210@1_2300_4__103"
        }
        r = requests.get('https://store.steampowered.com/search/?term=' + message.split('@')[1], headers=headers)
        # 確認是否下載成功
        if r.status_code == requests.codes.ok:
            # 以 BeautifulSoup 解析 HTML 程式碼
            soup = BeautifulSoup(r.text, 'html.parser')
            # print(r.text)

            # 以 CSS 的 class 抓出各類遊戲資訊
            try:
                name = soup.find_all('span', class_='title', limit=1)
                links = soup.find_all('a', class_='search_result_row ds_collapse_flag', limit=1)
                texts1 = name[0].text + '\n' + links[0].get(
                    'href') + '\n' + '-----------------------------------------------------------------------\n遊戲id:'
                texts2 = links[0].get('href').split('https://store.steampowered.com/app/')[1].split('/')[0]
                text_search = texts1 + texts2
            except:
                text_search = '請輸入正確名稱或英文\n例:#查詢@萊莎'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text_search))

def sort_by_value(d):
    items = d.items()
    backitems = [[v[1], v[0]] for v in items]
    backitems.sort()
    return [backitems[i][1] for i in range(0, len(backitems))]

def game_recommend(uid):
    #---------------------------------------------------------------test
    iddict = {}
    newlink.clear()
    newimg.clear()
    gamename.clear()
    gametab.clear()
    gameprice.clear()
    tagsRanking.clear()
    downloadFile('1C1AhkK_LeBZROLTH5EPEdGlfQBAj9oQ5', 'uid.json')
    with open(os.path.join("./", 'uid.json'), 'r') as readJ:
        iddict = json.load(readJ)
        readJ.close()
    # 讀取從資料庫
    if uid in iddict:
        downloadFile(iddict[uid], uid + '.txt')
        g = open(os.path.join("./", uid + '.txt'), 'r', encoding='utf-8')
        output = ''
        num = 0
        tags = dict()
        ranTags = dict()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:49.0) Gecko/20100101 Firefox/49.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-TW,zh;q=0.5",
            "Accept-Encoding": "gzip",
            "Connection": "keep-alive",
            "Cookie": "browserid=1178180757615078361; steamCountry=TW%7Cec9ee54d7b0da8ca2bade64a4cec7061; sessionid=97b065f7fc4fc75643e86564; timezoneOffset=28800,0; _ga=GA1.2.30895296.1571386387; strResponsiveViewPrefs=desktop; bGameHighlightAutoplayDisabled=false; _gid=GA1.2.523639413.1575597766; Steam_Language=tchinese; birthtime=880992001; lastagecheckage=2-0-1998; recentapps=%7B%221191210%22%3A1575620845%2C%22710920%22%3A1575618403%2C%221199880%22%3A1575617070%2C%221174370%22%3A1575616963%2C%22760810%22%3A1575611064%2C%22976730%22%3A1575610993%2C%221064220%22%3A1575606891%2C%221173900%22%3A1575606798%2C%22349270%22%3A1575606795%2C%22846470%22%3A1575606763%7D; app_impressions=1016920@1_2300_4__201|790740@1_2300_4__43|1191210@1_2300_4__103|585710@1_2300_4__43|1189230@1_2300_4__103|1192610@1_2300_4__103|936490@1_2300_4__103|1176020@1_2300_4__103|1179720@1_2300_4__103|760810@1_2300_4__103|1174370@1_2300_4__103|1065950@1_2300_4__103|648800@1_2300_4__40|1159540@1_2300_4__103|1171310@1_2300_4__103|1158910@1_2300_4__103|1161270@1_2300_4__103|617290@1_2300_4__hub-specials|418240@1_2300_4__hub-specials|1016920@1_2300_4__hub-specials|1174370@1_2300_4__hub-specials|1097420@1_2300_4__103|1168430@1_2300_4__103|617290@1_2300_4__201|790740@1_2300_4__43|1191210@1_2300_4__103"
        }
        for line in g:
            if line == 'None':
                output = 'None'
            else:
                r = requests.get(line, headers=headers)
                if r.status_code == requests.codes.ok:
                    # 以 BeautifulSoup 解析 HTML 程式碼
                    num += 1
                    soup = BeautifulSoup(r.text, 'html.parser')
                    links = soup.find_all('a', class_='app_tag')
                    # tagrandom = random.sample(range(0, len(links)), len(links))
                    for i in range(len(links)):
                        # taglink = links[i].text.strip('\r').strip('\n').strip('\t')
                        taglink = links[i].get('href')
                        if taglink in tags.keys():
                            tags[taglink] += 1
                        else:
                            tags[taglink] = 1
                # if line == 'https://store.steampowered.com/app/1234520/':
                #     print(taglink)
        g.close()

        if output == 'None':
            haveWishlist = False
            tagrandom = random.sample(range(0, 11), 10)
            for i in range(10):
                if tagrandom[i] == 0:
                    # 休閒
                    r = requests.get('https://store.steampowered.com/tags/zh-tw/%E4%BC%91%E9%96%92/', headers=headers)
                elif tagrandom[i] == 1:
                    # 冒險
                    r = requests.get('https://store.steampowered.com/tags/zh-tw/%E5%86%92%E9%9A%AA/', headers=headers)
                elif tagrandom[i] == 2:
                    # 動作
                    r = requests.get('https://store.steampowered.com/tags/zh-tw/%E5%8B%95%E4%BD%9C/', headers=headers)
                elif tagrandom[i] == 3:
                    # 模擬
                    r = requests.get('https://store.steampowered.com/tags/zh-tw/%E6%A8%A1%E6%93%AC/', headers=headers)
                elif tagrandom[i] == 4:
                    # 大型多人連驗
                    r = requests.get(
                        'https://store.steampowered.com/tags/zh-tw/%E5%A4%A7%E5%9E%8B%E5%A4%9A%E4%BA%BA%E9%80%A3%E7%B7%9A/',
                        headers=headers)
                elif tagrandom[i] == 5:
                    # 競速
                    r = requests.get('https://store.steampowered.com/tags/zh-tw/%E7%AB%B6%E9%80%9F/', headers=headers)
                elif tagrandom[i] == 6:
                    # 角色扮演
                    r = requests.get(
                        'https://store.steampowered.com/tags/zh-tw/%E8%A7%92%E8%89%B2%E6%89%AE%E6%BC%94/',
                        headers=headers)
                elif tagrandom[i] == 7:
                    # 獨立
                    r = requests.get('https://store.steampowered.com/tags/zh-tw/%E7%8D%A8%E7%AB%8B/', headers=headers)
                elif tagrandom[i] == 8:
                    # 策略
                    r = requests.get('https://store.steampowered.com/tags/zh-tw/%E7%AD%96%E7%95%A5/', headers=headers)
                elif tagrandom[i] == 9:
                    # 運動
                    r = requests.get('https://store.steampowered.com/tags/zh-tw/%E9%81%8B%E5%8B%95/', headers=headers)
                elif tagrandom[i] == 10:
                    # 虛擬實境
                    r = requests.get('https://store.steampowered.com/vr/', headers=headers)
                if r.status_code == requests.codes.ok:

                    # 以 BeautifulSoup 解析 HTML 程式碼
                    soup = BeautifulSoup(r.text, 'html.parser')

                    # 以 CSS 的 class 抓出各類遊戲資訊
                    links = soup.find_all('a', class_='tab_item', limit=15)
                    imgs = soup.find_all('img', class_='tab_item_cap_img', limit=15)
                    name = soup.find_all('div', class_='tab_item_name', limit=15)
                    price = soup.find_all('a', class_='tab_item', limit=15)
                    taball = soup.find_all('div', class_='tab_item_top_tags', limit=15)

                    gamerandom = random.sample(range(0, 15), 1)

                    for i in range(1):
                        tab = taball[gamerandom[i]].find_all('span', class_='top_tag')
                        newlink.append(links[gamerandom[i]].get('href'))
                        newimg.append(imgs[gamerandom[i]].get('src'))
                        gamename.append(name[gamerandom[i]].text)
                        gameprice.append(
                            price[gamerandom[i]].find('div', class_='discount_final_price').text + " (美金)")
                        str = ""
                        for j in tab:
                            str += ''.join(j.text)
                        gametab.append(str)
        else:
            haveWishlist = True
            keys = list(tags.keys())
            random.shuffle(keys)
            ranTags = dict([(key, tags[key]) for key in keys])
            # print('this is ranTags')
            # print(ranTags)
            tagsRanking.append(max(ranTags, key=ranTags.get))
            ranTags.pop(max(ranTags, key=ranTags.get))
            tagsRanking.append(max(ranTags, key=ranTags.get))
            ranTags.pop(max(ranTags, key=ranTags.get))
            tagsRanking.append(max(ranTags, key=ranTags.get))
            # print('this is tagsRanking')
            # print(tagsRanking)
            for i in range(3):
                r = requests.get(tagsRanking[i], headers=headers)
                if r.status_code == requests.codes.ok:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    links = soup.find_all('a', class_='tab_item', limit=15)
                    imgs = soup.find_all('img', class_='tab_item_cap_img', limit=15)
                    name = soup.find_all('div', class_='tab_item_name', limit=15)
                    price = soup.find_all('a', class_='tab_item', limit=15)
                    taball = soup.find_all('div', class_='tab_item_top_tags', limit=15)
                    gamerandom = random.sample(range(0, 15), 5)
                    if i == 0:
                        for j in range(5):
                            tab = taball[gamerandom[j]].find_all('span', class_='top_tag')
                            newlink.append(links[gamerandom[j]].get('href'))
                            newimg.append(imgs[gamerandom[j]].get('src'))
                            gamename.append(name[gamerandom[j]].text)
                            try:
                                gameprice.append(
                                    price[gamerandom[j]].find('div', class_='discount_final_price').text + " (美金)")
                            except:
                                gameprice.append(
                                    "免費遊玩")
                            str = ""
                            for k in tab:
                                str += ''.join(k.text)
                            gametab.append(str)
                    elif i == 1:
                        for j in range(3):
                            tab = taball[gamerandom[j]].find_all('span', class_='top_tag')
                            newlink.append(links[gamerandom[j]].get('href'))
                            newimg.append(imgs[gamerandom[j]].get('src'))
                            gamename.append(name[gamerandom[j]].text)
                            try:
                                gameprice.append(
                                    price[gamerandom[j]].find('div', class_='discount_final_price').text + " (美金)")
                            except:
                                gameprice.append(
                                    "免費遊玩")
                            str = ""
                            for k in tab:
                                str += ''.join(k.text)
                            gametab.append(str)
                    else:
                        for j in range(2):
                            tab = taball[gamerandom[j]].find_all('span', class_='top_tag')
                            newlink.append(links[gamerandom[j]].get('href'))
                            newimg.append(imgs[gamerandom[j]].get('src'))
                            gamename.append(name[gamerandom[j]].text)
                            try:
                                gameprice.append(
                                    price[gamerandom[j]].find('div', class_='discount_final_price').text + " (美金)")
                            except:
                                gameprice.append(
                                    "免費遊玩")
                            str = ""
                            for k in tab:
                                str += ''.join(k.text)
                            gametab.append(str)
    return haveWishlist
            # if num > 3:
            #     numrandom = random.sample(range(0, num), 3)
            # else:
            #     k = 5-num

def game_randomRecommed():
    newlink.clear()
    newimg.clear()
    gamename.clear()
    gametab.clear()
    gameprice.clear()
    tagsRanking.clear()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:49.0) Gecko/20100101 Firefox/49.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-TW,zh;q=0.5",
        "Accept-Encoding": "gzip",
        "Connection": "keep-alive",
        "Cookie": "browserid=1178180757615078361; steamCountry=TW%7Cec9ee54d7b0da8ca2bade64a4cec7061; sessionid=97b065f7fc4fc75643e86564; timezoneOffset=28800,0; _ga=GA1.2.30895296.1571386387; strResponsiveViewPrefs=desktop; bGameHighlightAutoplayDisabled=false; _gid=GA1.2.523639413.1575597766; Steam_Language=tchinese; birthtime=880992001; lastagecheckage=2-0-1998; recentapps=%7B%221191210%22%3A1575620845%2C%22710920%22%3A1575618403%2C%221199880%22%3A1575617070%2C%221174370%22%3A1575616963%2C%22760810%22%3A1575611064%2C%22976730%22%3A1575610993%2C%221064220%22%3A1575606891%2C%221173900%22%3A1575606798%2C%22349270%22%3A1575606795%2C%22846470%22%3A1575606763%7D; app_impressions=1016920@1_2300_4__201|790740@1_2300_4__43|1191210@1_2300_4__103|585710@1_2300_4__43|1189230@1_2300_4__103|1192610@1_2300_4__103|936490@1_2300_4__103|1176020@1_2300_4__103|1179720@1_2300_4__103|760810@1_2300_4__103|1174370@1_2300_4__103|1065950@1_2300_4__103|648800@1_2300_4__40|1159540@1_2300_4__103|1171310@1_2300_4__103|1158910@1_2300_4__103|1161270@1_2300_4__103|617290@1_2300_4__hub-specials|418240@1_2300_4__hub-specials|1016920@1_2300_4__hub-specials|1174370@1_2300_4__hub-specials|1097420@1_2300_4__103|1168430@1_2300_4__103|617290@1_2300_4__201|790740@1_2300_4__43|1191210@1_2300_4__103"
    }
    tagrandom = random.sample(range(0, 11), 10)
    for i in range(10):
        if tagrandom[i] == 0:
            # 休閒
            r = requests.get('https://store.steampowered.com/tags/zh-tw/%E4%BC%91%E9%96%92/', headers=headers)
        elif tagrandom[i] == 1:
            # 冒險
            r = requests.get('https://store.steampowered.com/tags/zh-tw/%E5%86%92%E9%9A%AA/', headers=headers)
        elif tagrandom[i] == 2:
            # 動作
            r = requests.get('https://store.steampowered.com/tags/zh-tw/%E5%8B%95%E4%BD%9C/', headers=headers)
        elif tagrandom[i] == 3:
            # 模擬
            r = requests.get('https://store.steampowered.com/tags/zh-tw/%E6%A8%A1%E6%93%AC/', headers=headers)
        elif tagrandom[i] == 4:
            # 大型多人連驗
            r = requests.get(
                'https://store.steampowered.com/tags/zh-tw/%E5%A4%A7%E5%9E%8B%E5%A4%9A%E4%BA%BA%E9%80%A3%E7%B7%9A/',
                headers=headers)
        elif tagrandom[i] == 5:
            # 競速
            r = requests.get('https://store.steampowered.com/tags/zh-tw/%E7%AB%B6%E9%80%9F/', headers=headers)
        elif tagrandom[i] == 6:
            # 角色扮演
            r = requests.get(
                'https://store.steampowered.com/tags/zh-tw/%E8%A7%92%E8%89%B2%E6%89%AE%E6%BC%94/',
                headers=headers)
        elif tagrandom[i] == 7:
            # 獨立
            r = requests.get('https://store.steampowered.com/tags/zh-tw/%E7%8D%A8%E7%AB%8B/', headers=headers)
        elif tagrandom[i] == 8:
            # 策略
            r = requests.get('https://store.steampowered.com/tags/zh-tw/%E7%AD%96%E7%95%A5/', headers=headers)
        elif tagrandom[i] == 9:
            # 運動
            r = requests.get('https://store.steampowered.com/tags/zh-tw/%E9%81%8B%E5%8B%95/', headers=headers)
        elif tagrandom[i] == 10:
            # 虛擬實境
            r = requests.get('https://store.steampowered.com/vr/', headers=headers)
        if r.status_code == requests.codes.ok:

            # 以 BeautifulSoup 解析 HTML 程式碼
            soup = BeautifulSoup(r.text, 'html.parser')

            # 以 CSS 的 class 抓出各類遊戲資訊
            links = soup.find_all('a', class_='tab_item', limit=15)
            imgs = soup.find_all('img', class_='tab_item_cap_img', limit=15)
            name = soup.find_all('div', class_='tab_item_name', limit=15)
            price = soup.find_all('a', class_='tab_item', limit=15)
            taball = soup.find_all('div', class_='tab_item_top_tags', limit=15)

            gamerandom = random.sample(range(0, 15), 1)

            for i in range(1):
                tab = taball[gamerandom[i]].find_all('span', class_='top_tag')
                newlink.append(links[gamerandom[i]].get('href'))
                newimg.append(imgs[gamerandom[i]].get('src'))
                gamename.append(name[gamerandom[i]].text)
                try:
                    gameprice.append(price[gamerandom[j]].find('div', class_='discount_final_price').text + " (美金)")
                except:
                    gameprice.append("免費遊玩")
                # gameprice.append(
                #     price[gamerandom[i]].find('div', class_='discount_final_price').text + " (美金)")
                str = ""
                for j in tab:
                    str += ''.join(j.text)
                gametab.append(str)

def uploadFile(file_id, filepath, mimetype):
    '''file_metadata = {'name': filename}
    media = MediaFileUpload(filepath,
                            mimetype=mimetype)
    file = service.files().create(body=file_metadata,
 search                                 media_body=media,
                                  fields='id').execute()
    print('File ID: %s' % file.get('id'))'''
    # File's new content.
    media_body = MediaFileUpload(
        filepath, mimetype=mimetype, resumable=True)

    # Send the request to the API.
    service.files().update(
        fileId=file_id,
        media_body=media_body).execute()


def downloadFile(file_id, filepath):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with io.open(filepath, 'wb') as f:
        fh.seek(0)
        f.write(fh.read())

    # --------------------------------------------------


def newFile(filename, filepath, mimetype):
    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath,
                            mimetype=mimetype)
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    return (file.get('id'))


if __name__ == "__main__":
    app.run()
