import os

import requests
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from bs4 import BeautifulSoup

import selenium
import selenium.webdriver as webdriver

app = Flask(__name__)

line_bot_api = LineBotApi('eGsaOBECCTQbmauJgf0PLC2LbvWEke/WRuFXuS0/bvLGtuOPwIh9Yng8+i2y07TIds7hWBAOFzKAPF7Iz9Yx5IoY6Op6mp83F8EEi93EHwD+ARqseWvZMzEvRbHRUVHKbq94Sfbkje3Of16k5IfAcgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0134d5ce9f1b5f94f0be216fd9db7a31')

def Discount():
    game = ""
    # 下載 Yahoo 首頁內容

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), chrome_options=chrome_options)

    url = 'https://store.steampowered.com/search/'
    driver.get(url)
    driver.refresh()

    pagesource = driver.page_source
    soup = BeautifulSoup(pagesource)


    # 以 CSS 的 class 抓出各類頭條新聞
    stories = soup.find_all('span', class_='title')
    for s in stories:
       # 新聞標題
        game = game +  "標題：" + s.text + "\n"
        # 新聞網址
       # print("網址：" + s.get('href'))
    return game
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
        text1 = "歡迎使用NTUSteam!!!~~~\n按(分類按鈕)\n\t即可檢視遊戲類別\n"
        texta = "------------\n"
        text2 = "按下欲查詢類別按鈕或輸入(#類別名稱)\n範例:#動作\n\t即可查看該類別遊戲(隨機5個)\n"
        text3 = "按(下殺特賣按鈕)\n\t即可檢視目前含有折扣之遊戲\n"
        text4 = "按(新發售按鈕)\n\t即可觀看目前新發售之遊戲\n"
        text5 = "輸入(#遊戲名稱)\n\t即會顯示該遊戲相關介紹\n"
        text6 = "按(推薦清單按鈕)\n\t即會根據您喜歡的遊戲類別進行推薦\n"
        text7 = "輸入(+遊戲名稱)\n\t即會把遊戲加入我的最愛中\n"
        text8 = "按(我的最愛按鈕)\n\t即可查看我的最愛清單中您所加入的遊戲"

        message = text1 + text2 + text3 + text4 + text5 + text6 + text7 + text8
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))

        # line_bot_api.reply_message(
        #    event.reply_token,
        #    TextSendMessage(text=event.message.text))


    elif message == "#特惠":

        a = Discount()

        line_bot_api.reply_message(event.reply_token, TextSendMessage(a))


if __name__ == "__main__":
    app.run()
