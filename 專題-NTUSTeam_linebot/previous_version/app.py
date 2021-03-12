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

def GamesParser(flag):
    newlink.clear()
    newimg.clear()
    gamename.clear()
    gametab.clear()
    gameprice.clear()


    if flag == 1:
        dbname = "new"
    elif flag == 2:
        dbname = "discount"
    elif flag == 3:
        dbname = "leisure"
    elif flag == 4:
        dbname = "adventure"
    elif flag == 5:
        dbname = "action"
    elif flag == 6:
        dbname = "simulation"
    elif flag == 7:
        dbname = "mmo"
    elif flag == 8:
        dbname = "racing"
    elif flag == 9:
        dbname = "rpg"
    elif flag == 10:
        dbname = "before"
    elif flag == 11:
        dbname = "independent"
    elif flag == 12:
        dbname = "strategy"
    elif flag == 13:
        dbname = "sports"
    elif flag == 14:
        dbname = "vr"
    elif flag == 15:
        dbname = "lastup"
    elif flag == 16:
        dbname = "free"

    g = open(os.path.join(dbname + '.txt'), 'r', encoding='utf-8')

    links = []
    imgs = []
    name = []
    price = []
    taball = []
    for line in g:
        line2 = line.split(';')
        if 'app' in line2[2]:
            name.append(line2[0])
            imgs.append(line2[1])
            links.append(line2[2])
            price.append(line2[3])
            taball.append(line2[4])

    gamerandom = random.sample(range(0, len(name)), 10)
    for i in range(10):
        newlink.append(links[gamerandom[i]])
        newimg.append(imgs[gamerandom[i]])
        gamename.append(name[gamerandom[i]])
        gameprice.append(price[gamerandom[i]])
        gametab.append(taball[gamerandom[i]])
    print(newlink)


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

    r = requests.get('https://store.steampowered.com/search/?sort_by=_ASC&filter=topsellers', headers=headers)

    if r.status_code == requests.codes.ok:

        soup = BeautifulSoup(r.text, 'html.parser')
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
            if r2.status_code == requests.codes.ok:
                # 以 BeautifulSoup 解析 HTML 程式碼
                soup2 = BeautifulSoup(r2.text, 'html.parser')

                price = soup2.find('div', class_='game_purchase_price price')
                if price != None:
                    gameprice.append(price.text.strip('\r').strip('\n').strip('\t'))
                else:
                    price = soup2.find('div', class_='discount_final_price')
                    if price != None:
                        gameprice.append(price.text.strip('\r').strip('\n').strip('\t'))
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

        print(gamename)
        print(gameprice)
        print(gametab)
        print(newimg)
        print(newlink)


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
                    gameprice.append(price[gamerandom[i]].find('div', class_='discount_final_price').text)
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

        carousel = CarouselContainer()

        bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                spacing='xl',
                contents=[
                    BoxComponent(
                        layout='baseline',
                        spacing='xl',
                        contents=[
                            IconComponent(size='lg', url='https://i.imgur.com/ih2H7fI.png'),
                            TextComponent(text='歡迎使用NTUSteam!!!~~~', color='#000000', align='center', weight='bold',
                                          size='lg'),
                        ]
                    ),
                    SeparatorComponent(color='#666666'),
                    TextComponent(
                        text="以下為此項產品使用說明,",
                        color='#2F4F4F',
                        size='md',
                    ),
                    TextComponent(
                        text="針對每項功能詳細介紹(#為指令):",
                        color='#2F4F4F',
                        size='md',
                    ),
                    BoxComponent(
                        layout='horizontal',
                        contents=[
                            SpacerComponent(size='sm'),
                            BoxComponent(
                                layout='vertical',
                                contents=[
                                    TextComponent(
                                        spacing='sm',
                                        text='#推薦清單',
                                        color='#6A5ACD',
                                        size='sm',
                                    ),
                                    TextComponent(
                                        spacing='sm',
                                        text='#下殺特賣',
                                        align='end',
                                        color='#6A5ACD',
                                        size='sm',
                                    ),
                                    TextComponent(
                                        spacing='sm',
                                        text='#遊戲分類',
                                        color='#6A5ACD',
                                        size='sm',
                                    ),
                                    TextComponent(
                                        spacing='sm',
                                        text='#我的最愛',
                                        align='end',
                                        color='#6A5ACD',
                                        size='sm',
                                    ),
                                    TextComponent(
                                        spacing='sm',
                                        text='#新發售',
                                        color='#6A5ACD',
                                        size='sm',
                                    ),
                                    TextComponent(
                                        spacing='sm',
                                        text='其他指令',
                                        align='end',
                                        color='#6A5ACD',
                                        size='sm',
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
        )

        carousel.contents.append(bubble)

        bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                spacing='xl',
                contents=[
                    BoxComponent(
                        layout='baseline',
                        spacing='xl',
                        contents=[
                            IconComponent(size='lg', url='https://i.imgur.com/ih2H7fI.png'),
                        ]
                    ),
                   TextComponent(text='#推薦清單', color='#000000', align='center', size='lg'),
                    BoxComponent(
                        layout='horizontal',
                        contents=[
                            SpacerComponent(size='sm'),
                            BoxComponent(
                                layout='vertical',
                                contents=[
                                    SeparatorComponent(color='#666666'),  # 上面水平線
                                    TextComponent(
                                        text='即會根據您喜歡的遊戲類別,',
                                        color='#696969',
                                        size='md'
                                    ),
                                    TextComponent(
                                        text='針對瀏覽率高的類別進行推薦',
                                        color='#696969',
                                        size='md'
                                    ),
                                ]
                            ),
                        ]
                    ),
                    TextComponent(text='--------------------------------', color='#000000', align='center', size='lg'),
                    TextComponent(text='#下殺特賣', color='#000000', align='center', size='lg'),
                    BoxComponent(
                        layout='horizontal',
                        contents=[
                            SpacerComponent(size='sm'),
                            BoxComponent(
                                layout='vertical',
                                contents=[
                                    SeparatorComponent(color='#666666'),
                                    TextComponent(
                                        text='即可檢視當日或最近折扣中,',
                                        color='#696969',
                                        size='md'
                                    ),
                                    TextComponent(
                                        text='顯示出優惠的遊戲資訊',
                                        color='#696969',
                                        size='md'
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
        )

        carousel.contents.append(bubble)

        bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                spacing='xl',
                contents=[
                    BoxComponent(
                        layout='baseline',
                        spacing='xl',
                        contents=[
                            IconComponent(size='lg', url='https://i.imgur.com/ih2H7fI.png'),
                        ]
                    ),
                    TextComponent(text='#遊戲分類', color='#000000', align='center', size='lg'),
                    BoxComponent(
                        layout='horizontal',
                        contents=[
                            SpacerComponent(size='sm'),
                            BoxComponent(
                                layout='vertical',
                                contents=[
                                    SeparatorComponent(color='#666666'),  # 上面水平線
                                    TextComponent(
                                        text='查看有關該類別的遊戲,(隨機5個)',
                                        color='#708090',
                                        size='md'
                                    ),
                                    TextComponent(
                                        text='例如:#策略 #運動 #即將發行 #角色扮演...',
                                        color='#8B3626',
                                        size='sm'
                                    ),
                                ]
                            ),
                        ]
                    ),
                    TextComponent(text='--------------------------------', color='#000000', align='center', size='lg'),
                    TextComponent(text='#我的最愛', color='#000000', align='center', size='lg'),
                    BoxComponent(
                        layout='horizontal',
                        contents=[
                            SpacerComponent(size='sm'),
                            BoxComponent(
                                layout='vertical',
                                contents=[
                                    SeparatorComponent(color='#666666'),
                                    TextComponent(
                                        text='可將喜歡的遊戲,加入至其中,且可查看',
                                        color='#708090',
                                        size='sm'
                                    ),
                                    TextComponent(
                                        text='[我的最愛]清單中所加入的遊戲',
                                        color='#708090',
                                        size='sm'
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
        )

        carousel.contents.append(bubble)

        bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                spacing='xl',
                contents=[
                    BoxComponent(
                        layout='baseline',
                        spacing='xl',
                        contents=[
                            IconComponent(size='lg', url='https://i.imgur.com/ih2H7fI.png'),
                        ]
                    ),
                    TextComponent(text='#新發售', color='#000000', align='center', size='lg'),
                    BoxComponent(
                        layout='horizontal',
                        contents=[
                            SpacerComponent(size='sm'),
                            BoxComponent(
                                layout='vertical',
                                contents=[
                                    SeparatorComponent(color='#666666'),  # 上面水平線
                                    TextComponent(
                                        text='即可觀看近期新推出之遊戲,',
                                        color='#BEBEBE',
                                        size='md'
                                    ),
                                    TextComponent(
                                        text='讓您能馬上得知遊戲的最新消息',
                                        color='#BEBEBE',
                                        size='md'
                                    ),
                                ]
                            ),
                        ]
                    ),
                    TextComponent(text='--------------------------------', color='#000000', align='center', size='lg'),
                    TextComponent(text='其他指令', color='#000000', align='center', size='lg'),
                    BoxComponent(
                        layout='horizontal',
                        contents=[
                            SpacerComponent(size='sm'),
                            BoxComponent(
                                layout='vertical',
                                contents=[
                                    SeparatorComponent(color='#666666'),  # 上面水平線
                                    TextComponent(
                                        text='1.^遊戲ID : 加入/移除我的最愛',
                                        color='#BEBEBE',
                                        size='md'
                                    ),
                                    TextComponent(
                                        text='2.#查詢@遊戲名稱 : 搜尋遊戲ID',
                                        color='#BEBEBE',
                                        size='md'
                                    ),
                                    TextComponent(
                                        text='3.#隨機推薦 : 隨機推薦遊戲',
                                        color='#BEBEBE',
                                        size='md'
                                    ),
                                ]
                            ),
                        ]
                    ),

                ]
            ),
        )

        carousel.contents.append(bubble)

        bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                spacing='xl',
                contents=[
                    BoxComponent(
                        layout='baseline',
                        spacing='xl',
                        contents=[
                            IconComponent(size='lg', url='https://i.imgur.com/ih2H7fI.png'),
                        ]
                    ),
                    TextComponent(text='首先~', color='#000000', align='center', size='lg'),
                    TextComponent(text='感謝您的支持與鼓勵!', color='#000000', align='center', size='lg'),
                    TextComponent(text='希望此產品能夠幫助您!', color='#000000', align='center', size='lg'),
                    TextComponent(text='祝您使用起來開心快樂!', color='#000000', align='center', size='lg'),
                    TextComponent(text='最後~', color='#000000', align='center', size='lg'),
                    TextComponent(text='請給予我們評論與指教!', color='#000000', align='center', size='lg'),
                ]
            ),
        )

        carousel.contents.append(bubble)

        message = FlexSendMessage(alt_text="請輸入#分類(你要找的)", contents=carousel)
        line_bot_api.reply_message(event.reply_token, message)

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

    elif message == "#休閒" or message == "#冒險" or message == "#動作" or message == "#模擬" or message == "#大型多人連線" or message == "#競速" or message == "#角色扮演" or message == "#搶先體驗" or message == "#獨立" or message == "#策略" or message == "#運動" or message == "#虛擬實境" or message == "#最近更新" or message == "#即將發行" or message == "#暢銷商品" or message == "#免費遊玩" or message == "#新發售" or message == "#下殺特賣" or message == "#推薦清單" or message == "#隨機推薦":
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
        elif message == "#推薦清單":
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

        carousel = CarouselContainer()
        for i in range(10):
            bubble = BubbleContainer(
                direction='ltr',
                header=BoxComponent(
                    layout='vertical',
                    contents=[
                        TextComponent(text=title, weight='bold', size='xl'),
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
                                            text=index,
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
                        BoxComponent(
                            layout='horizontal',
                            spacing='sm',
                            contents=[
                                SpacerComponent(size='sm'),
                                ImageComponent(
                                    url=newimg[i],
                                    size='full',
                                    aspect_ratio='20:13',
                                    aspect_mode='fit',
                                    action=URIAction(
                                        uri=newlink[i])
                                ),
                                SeparatorComponent(),
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
                                    '*' +
                                    newlink[i].split('https://store.steampowered.com/app/')[1].split('/')[
                                        0])),
                        ),
                        ButtonComponent(
                            height='sm',
                            action=MessageAction(label='加入/移除最愛', text=(
                                    '^' +
                                    newlink[i].split('https://store.steampowered.com/app/')[1].split('/')[
                                        0])),
                        ),
                    ],
                ),
            )

            carousel.contents.append(bubble)

        message = FlexSendMessage(alt_text="請輸入#分類(你要找的)", contents=carousel)
        line_bot_api.reply_message(event.reply_token, message)
        # print(gameprice)

    elif message.find('^') != -1:
        # json處理
        r = ('https://store.steampowered.com/app/' + message.split('^')[1] + '/')
        text = (r)
        with open(os.path.join("./", 'uid.json'), 'r') as readJ:
            iddict = json.load(readJ)
            readJ.close()
        with open(os.path.join("./", 'uid.json'), 'w') as f:
            # 儲存到資料庫
            if uid in iddict:
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
        output = ''
        cnt = 0
        if r.status_code == requests.codes.ok:
            soup = BeautifulSoup(r.text, 'html.parser')

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






    elif message == "#我的最愛":
        newlink.clear()
        newimg.clear()
        gamename.clear()
        gametab.clear()
        gameprice.clear()
        with open(os.path.join("./", 'uid.json'), 'r') as readJ:
            iddict = json.load(readJ)
            readJ.close()
        if uid in iddict:
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
                        num += 1
                        soup = BeautifulSoup(r.text, 'html.parser')
                        name = soup.find_all('div', class_='apphub_AppName', limit=1)
                        gamename.append(name[0].text)
                        price = soup.find('div', class_='game_purchase_price price')
                        if price != None:
                            gameprice.append(price.text.strip('\r').strip('\n').strip('\t'))
                        else:
                            price = soup.find('div', class_='discount_final_price')
                            if price != None:
                                gameprice.append(price.text.strip('\r').strip('\n').strip('\t'))
                            else:
                                gameprice.append("月費遊戲")
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
                        newlink.append(line.strip('\n'))
            g.close()

            if output == 'None':
                line_bot_api.reply_message(event.reply_token, TextSendMessage('我的最愛中沒有項目'))
            else:
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
                                        SpacerComponent(size='sm'),
                                        ImageComponent(
                                            url=newimg[i],
                                            size='full',
                                            aspect_ratio='20:13',
                                            aspect_mode='fit',
                                            action=URIAction(
                                                uri=newlink[i])
                                        ),
                                        SeparatorComponent(),
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
        if r.status_code == requests.codes.ok:
            soup = BeautifulSoup(r.text, 'html.parser')

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

    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage("指令輸入錯誤，請查看使用說明"))


# def sort_by_value(d):
#     items = d.items()
#     backitems = [[v[1], v[0]] for v in items]
#     backitems.sort()
#     return [backitems[i][1] for i in range(0, len(backitems))]


def game_recommend(uid):

    newlink.clear()
    newimg.clear()
    gamename.clear()
    gametab.clear()
    gameprice.clear()
    tagsRanking.clear()

    with open(os.path.join("./", 'uid.json'), 'r') as readJ:
        iddict = json.load(readJ)
        readJ.close()
    # 讀取從資料庫
    if uid in iddict:
        g = open(os.path.join("./", uid + '.txt'), 'r', encoding='utf-8')
        output = ''
        num = 0
        tags = dict()
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
                    for i in range(len(links)):
                        taglink = links[i].get('href')
                        if taglink in tags.keys():
                            tags[taglink] += 1
                        else:
                            tags[taglink] = 1
        g.close()

        if output == 'None':
            haveWishlist = False
            game_randomRecommed()

        else:
            dbname = ''

            haveWishlist = True
            keys = list(tags.keys())
            random.shuffle(keys)
            ranTags = dict([(key, tags[key]) for key in keys])
            tagsRanking.append(max(ranTags, key=ranTags.get))
            ranTags.pop(max(ranTags, key=ranTags.get))
            tagsRanking.append(max(ranTags, key=ranTags.get))
            ranTags.pop(max(ranTags, key=ranTags.get))
            tagsRanking.append(max(ranTags, key=ranTags.get))
            for i in range(3):
                if tagsRanking[i].split('?')[0] == "https://store.steampowered.com/tags/zh-tw/%E5%8B%95%E4%BD%9C/" or \
                        tagsRanking[i].split('?')[0] == "https://store.steampowered.com/tags/zh-tw/%E5%86%92%E9%9A%AA/" or \
                        tagsRanking[i].split('?')[0] == "https://store.steampowered.com/genre/Early%20Access/" or \
                        tagsRanking[i].split('?')[0] == "https://store.steampowered.com/specials#tab=TopSellers" or \
                        tagsRanking[i].split('?')[0] == "https://store.steampowered.com/tags/zh-tw/%E5%85%8D%E8%B2%BB/" or \
                        tagsRanking[i].split('?')[0] == "https://store.steampowered.com/tags/zh-tw/%E7%8D%A8%E7%AB%8B/" or \
                        tagsRanking[i].split('?')[0] == "https://store.steampowered.com/updated/all/" or \
                        tagsRanking[i].split('?')[0] == "https://store.steampowered.com/tags/zh-tw/%E4%BC%91%E9%96%92/" or \
                        tagsRanking[i].split('?')[0] == "https://store.steampowered.com/tags/zh-tw/%E5%A4%A7%E5%9E%8B%E5%A4%9A%E4%BA%BA%E9%80%A3%E7%B7%9A/" or \
                        tagsRanking[i].split('?')[0] == "https://store.steampowered.com/explore/new/" or \
                        tagsRanking[i].split('?')[0] == "https://store.steampowered.com/tags/zh-tw/%E7%AB%B6%E9%80%9F/" or \
                        tagsRanking[i].split('?')[0] == "https://store.steampowered.com/tags/zh-tw/%E8%A7%92%E8%89%B2%E6%89%AE%E6%BC%94/" or \
                        tagsRanking[i].split('?')[0] == "https://store.steampowered.com/tags/zh-tw/%E6%A8%A1%E6%93%AC/" or \
                        tagsRanking[i].split('?')[0] == "https://store.steampowered.com/tags/zh-tw/%E9%81%8B%E5%8B%95/" or \
                        tagsRanking[i].split('?')[0] == "https://store.steampowered.com/tags/zh-tw/%E7%AD%96%E7%95%A5/" or \
                        tagsRanking[i].split('?')[0] == "https://store.steampowered.com/vr/":

                    if tagsRanking[i].strip('\r').strip('\n').strip('\t').split('?')[0] == "https://store.steampowered.com/explore/new/":
                        dbname = "new"
                    elif tagsRanking[i].strip('\r').strip('\n').strip('\t').split('?')[0] == "https://store.steampowered.com/specials#tab=TopSellers":
                        dbname = "discount"
                    elif tagsRanking[i].strip('\r').strip('\n').strip('\t').split('?')[0] == "https://store.steampowered.com/tags/zh-tw/%E4%BC%91%E9%96%92/":
                        dbname = "leisure"
                    elif tagsRanking[i].strip('\r').strip('\n').strip('\t').split('?')[0] == "https://store.steampowered.com/tags/zh-tw/%E5%86%92%E9%9A%AA/":
                        dbname = "adventure"
                    elif tagsRanking[i].strip('\r').strip('\n').strip('\t').split('?')[0] == "https://store.steampowered.com/tags/zh-tw/%E5%8B%95%E4%BD%9C/":
                        dbname = "action"
                    elif tagsRanking[i].strip('\r').strip('\n').strip('\t').split('?')[0] == "https://store.steampowered.com/tags/zh-tw/%E6%A8%A1%E6%93%AC/":
                        dbname = "simulation"
                    elif tagsRanking[i].strip('\r').strip('\n').strip('\t').split('?')[0] == 'https://store.steampowered.com/tags/zh-tw/%E5%A4%A7%E5%9E%8B%E5%A4%9A%E4%BA%BA%E9%80%A3%E7%B7%9A/':
                        dbname = "mmo"
                    elif tagsRanking[i].strip('\r').strip('\n').strip('\t').split('?')[0] == 'https://store.steampowered.com/tags/zh-tw/%E7%AB%B6%E9%80%9F/':
                        dbname = "racing"
                    elif tagsRanking[i].strip('\r').strip('\n').strip('\t').split('?')[0] == "https://store.steampowered.com/tags/zh-tw/%E8%A7%92%E8%89%B2%E6%89%AE%E6%BC%94/":
                        dbname = "rpg"
                    elif tagsRanking[i].strip('\r').strip('\n').strip('\t').split('?')[0] == 'https://store.steampowered.com/genre/Early%20Access/':
                        dbname = "before"
                    elif tagsRanking[i].strip('\r').strip('\n').strip('\t').split('?')[0] == 'https://store.steampowered.com/tags/zh-tw/%E7%8D%A8%E7%AB%8B/':
                        dbname = "independent"
                    elif tagsRanking[i].strip('\r').strip('\n').strip('\t').split('?')[0] == 'https://store.steampowered.com/tags/zh-tw/%E7%AD%96%E7%95%A5/':
                        dbname = "strategy"
                    elif tagsRanking[i].strip('\r').strip('\n').strip('\t').split('?')[0] == 'https://store.steampowered.com/tags/zh-tw/%E9%81%8B%E5%8B%95/':
                        dbname = "sports"
                    elif tagsRanking[i].strip('\r').strip('\n').strip('\t').split('?')[0] == 'https://store.steampowered.com/vr/':
                        dbname = "vr"
                    elif tagsRanking[i].strip('\r').strip('\n').strip('\t').split('?')[0] == 'https://store.steampowered.com/updated/all/':
                        dbname = "lastup"
                    elif tagsRanking[i].strip('\r').strip('\n').strip('\t').split('?')[0] == 'https://store.steampowered.com/tags/zh-tw/%E5%85%8D%E8%B2%BB/':
                        dbname = "free"

                    g = open(os.path.join(dbname + '.txt'), 'r', encoding='utf-8')

                    links = []
                    imgs = []
                    name = []
                    price = []
                    taball = []
                    for line in g:
                        line2 = line.split(';')
                        name.append(line2[0])
                        imgs.append(line2[1])
                        links.append(line2[2])
                        price.append(line2[3])
                        taball.append(line2[4])

                    if i == 0:
                        gamerandom = random.sample(range(0, len(name)), 5)
                        for i in range(5):
                            newlink.append(links[gamerandom[i]])
                            newimg.append(imgs[gamerandom[i]])
                            gamename.append(name[gamerandom[i]])
                            gameprice.append(price[gamerandom[i]])
                            gametab.append(taball[gamerandom[i]])
                    elif i == 1:
                        gamerandom = random.sample(range(0, len(name)), 3)
                        for i in range(3):
                            newlink.append(links[gamerandom[i]])
                            newimg.append(imgs[gamerandom[i]])
                            gamename.append(name[gamerandom[i]])
                            gameprice.append(price[gamerandom[i]])
                            gametab.append(taball[gamerandom[i]])
                    else:
                        for i in range(2):
                            gamerandom = random.sample(range(0, len(name)), 2)
                            newlink.append(links[gamerandom[i]])
                            newimg.append(imgs[gamerandom[i]])
                            gamename.append(name[gamerandom[i]])
                            gameprice.append(price[gamerandom[i]])
                            gametab.append(taball[gamerandom[i]])

                else:
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
                                        price[gamerandom[j]].find('div', class_='discount_final_price').text)
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
                                        price[gamerandom[j]].find('div', class_='discount_final_price').text)
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
                                        price[gamerandom[j]].find('div', class_='discount_final_price').text)
                                except:
                                    gameprice.append(
                                        "免費遊玩")
                                str = ""
                                for k in tab:
                                    str += ''.join(k.text)
                                gametab.append(str)
    else:
        haveWishlist = False
        game_randomRecommed()
    return haveWishlist


def game_randomRecommed():
    newlink.clear()
    newimg.clear()
    gamename.clear()
    gametab.clear()
    gameprice.clear()
    tagsRanking.clear()

    tagrandom = random.sample(range(0, 17), 10)

    for i in range(10):
        if tagrandom[i] == 1:
            dbname = "new"
        elif tagrandom[i] == 2:
            dbname = "discount"
        elif tagrandom[i] == 3:
            dbname = "leisure"
        elif tagrandom[i] == 4:
            dbname = "adventure"
        elif tagrandom[i] == 5:
            dbname = "action"
        elif tagrandom[i] == 6:
            dbname = "simulation"
        elif tagrandom[i] == 7:
            dbname = "mmo"
        elif tagrandom[i] == 8:
            dbname = "racing"
        elif tagrandom[i] == 9:
            dbname = "rpg"
        elif tagrandom[i] == 10:
            dbname = "before"
        elif tagrandom[i] == 11:
            dbname = "independent"
        elif tagrandom[i] == 12:
            dbname = "strategy"
        elif tagrandom[i] == 13:
            dbname = "sports"
        elif tagrandom[i] == 14:
            dbname = "vr"
        elif tagrandom[i] == 15:
            dbname = "lastup"
        elif tagrandom[i] == 16:
            dbname = "free"

        g = open(os.path.join(dbname + '.txt'), 'r', encoding='utf-8')

        links = []
        imgs = []
        name = []
        price = []
        taball = []
        for line in g:
            line2 = line.split(';')
            name.append(line2[0])
            imgs.append(line2[1])
            links.append(line2[2])
            price.append(line2[3])
            taball.append(line2[4])

        gamerandom = random.sample(range(0, len(name)), 1)

        for i in range(1):
            newlink.append(links[gamerandom[i]])
            newimg.append(imgs[gamerandom[i]])
            gamename.append(name[gamerandom[i]])
            gameprice.append(price[gamerandom[i]])
            gametab.append(taball[gamerandom[i]])


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