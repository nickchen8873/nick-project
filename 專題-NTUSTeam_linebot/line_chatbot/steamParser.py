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

from bs4 import BeautifulSoup
from selenium import webdriver

import json

import datetime
import time
# --------------------------------------------------
import httplib2
import os
import io

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

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

def steamParser():
    print('begin time=')
    print(datetime.datetime.now())

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
            dbid = "1ybwjFk0pxH9HGaQQqnQR6usYNJq0ObsE"
            dbname = "new"
        elif flag1 == 2:
            r = requests.get('https://store.steampowered.com/specials', headers=headers)
            dbid = "1utJrJhlgO_pAzgsTfIQsLra7uaA0AmA1"
            dbname = "discount"
        elif flag1 == 3:
            r = requests.get('https://store.steampowered.com/tags/zh-tw/%E4%BC%91%E9%96%92/', headers=headers)
            dbid = "1C1DcUfZTnpEU-wZs_LXSETjW-HZcYfoV"
            dbname = "leisure"
        elif flag1 == 4:
            r = requests.get('https://store.steampowered.com/tags/zh-tw/%E5%86%92%E9%9A%AA/', headers=headers)
            dbid = "1-7MTYcw8UNY6pc8J3h6fw_IAquJoOzjF"
            dbname = "adventure"
        elif flag1 == 5:
            r = requests.get('https://store.steampowered.com/tags/zh-tw/%E5%8B%95%E4%BD%9C/', headers=headers)
            dbid = "1U_iDoIiGRKeAheiz-zeEVDnF8VgSPkxV"
            dbname = "action"
        elif flag1 == 6:
            r = requests.get('https://store.steampowered.com/tags/zh-tw/%E6%A8%A1%E6%93%AC/', headers=headers)
            dbid = "1qtWM1Ccq-Fn6voP8hZhg0vQnNC9M1WzK"
            dbname = "simulation"
        elif flag1 == 7:
            r = requests.get(
                'https://store.steampowered.com/tags/zh-tw/%E5%A4%A7%E5%9E%8B%E5%A4%9A%E4%BA%BA%E9%80%A3%E7%B7%9A/',
                headers=headers)
            dbid = "1HjSsF9KAVILQY2uMBBMr7CNxIJ_FSLe4"
            dbname = "mmo"
        elif flag1 == 8:
            r = requests.get('https://store.steampowered.com/tags/zh-tw/%E7%AB%B6%E9%80%9F/', headers=headers)
            dbid = "1viu1iox7JXLxQ0jQ1WI7VSkVBCLi_1GT"
            dbname = "racing"
        elif flag1 == 9:
            r = requests.get('https://store.steampowered.com/tags/zh-tw/%E8%A7%92%E8%89%B2%E6%89%AE%E6%BC%94/',
                             headers=headers)
            dbid = "1y36dbhMefvpOOWy4-Ru3tF68Xvi_USgH"
            dbname = "rpg"
        elif flag1 == 10:
            r = requests.get('https://store.steampowered.com/genre/Early%20Access/', headers=headers)
            dbid = "1cEomzBHVcXpsAs6GjF12tbu-_Q9UBuKs"
            dbname = "before"
        elif flag1 == 11:
            r = requests.get('https://store.steampowered.com/tags/zh-tw/%E7%8D%A8%E7%AB%8B/', headers=headers)
            dbid = "18srb4dM7naJOZ3CSUnUiNvcXUVD1KTin"
            dbname = "independent"
        elif flag1 == 12:
            r = requests.get('https://store.steampowered.com/tags/zh-tw/%E7%AD%96%E7%95%A5/', headers=headers)
            dbid = "1hAu31KAe49kWfxIbVeODrIOgnBJCXdGZ"
            dbname = "strategy"
        elif flag1 == 13:
            r = requests.get('https://store.steampowered.com/tags/zh-tw/%E9%81%8B%E5%8B%95/', headers=headers)
            dbid = "1RInc3Wm1bu8V8oMq_vhATN_spJ3Vij-l"
            dbname = "sports"
        elif flag1 == 14:
            r = requests.get('https://store.steampowered.com/vr/', headers=headers)
            dbid = "1qMvvwXano3lac6LYfG_EvWu6jkbx37CX"
            dbname = "vr"
        elif flag1 == 15:
            r = requests.get('https://store.steampowered.com/updated/all/', headers=headers)
            dbid = "1E4eqTAj9buLXt5Qb58UaUYXvwU4EG4Dd"
            dbname = "lastup"
        elif flag1 == 16:
            r = requests.get('https://store.steampowered.com/genre/Free%20to%20Play/', headers=headers)
            dbid = "10Sm1QJjXhVWGgYF3MjF15wNbpIhfGwyk"
            dbname = "free"

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

                if page == 1:
                    g = open(os.path.join(dbname + '.txt'), 'r', encoding='utf-8')
                    line1 = g.readline()
                    # print('line1=')
                    # print(line1)
                    game1 = line1.split(';')
                    print(dbname + '資料庫的第一筆遊戲 =' + game1[0])
                    if game1[0] != gamename[0]:
                        print('update time=')
                        print(datetime.datetime.now())
                    else:
                        print(dbname + '的遊戲還沒被更新')
                    g.close()
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


            g = open(os.path.join("./", dbname + '.txt'), 'w', encoding='utf-8')
            g.write(alltext)
            g.close()
            uploadFile(dbid, os.path.join("./", dbname + '.txt'), 'text/txt')
            driver.quit()
    print('end time=')
    print(datetime.datetime.now())

    iddict = {}
    with open(os.path.join("./", 'uid.json'), 'r') as readJ:
        iddict = json.load(readJ)
        readJ.close()
        for uid in iddict:
            uploadFile(iddict[uid], os.path.join("./", uid + '.txt'), 'text/txt')
        uploadFile('1C1AhkK_LeBZROLTH5EPEdGlfQBAj9oQ5', os.path.join("./", 'uid.json'), 'application/json')

def main():
    h = 3
    m = 1
    while True:
        now = datetime.datetime.now()
        print(now.hour, now.minute)
        if now.hour == h and now.minute == m:
            # m += 60
            # if m >= 60:
            #     h += 1
            #     m - 60
            # if h >= 24:
            #     h-24
            steamParser()
        time.sleep(60)


if __name__ == '__main__':
    main()