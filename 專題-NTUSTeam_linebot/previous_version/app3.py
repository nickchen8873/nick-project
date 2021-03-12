import httplib2
import os
import io

import requests
from apiclient import discovery
from bs4 import BeautifulSoup
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

import json

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Python OCR'

# 取得憑證、認證、建立 Google 雲端硬碟 API 服務物件
credential_path = os.path.join("./", 'google-ocr-credential.json')
store = Storage(credential_path)
credentials = store.get()
if not credentials or credentials.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    flow.user_agent = APPLICATION_NAME
    if flags:
        credentials = tools.run_flow(flow, store, flags)
    else:  # Needed only for compatibility with Python 2.6
        credentials = tools.run(flow, store)
    print('憑證儲存於：' + credential_path)
http = credentials.authorize(httplib2.Http())
service = discovery.build('drive', 'v3', http=http)


def main():
    # uploadFile('database.txt', 'text/txt')
    # downloadFile('11JjdhbBRHVqj8S6vQM93cxZIX82NsKmE', 'database.txt')
    # par(1212830)
    jsonopen()


def uploadFile(filepath, mimetype):
    '''file_metadata = {'name': filename}
    media = MediaFileUpload(filepath,
                            mimetype=mimetype)
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    print('File ID: %s' % file.get('id'))'''
    # File's new content.
    media_body = MediaFileUpload(
        filepath, mimetype=mimetype, resumable=True)

    # Send the request to the API.
    service.files().update(
        fileId='11JjdhbBRHVqj8S6vQM93cxZIX82NsKmE',
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


def par(r):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:49.0) Gecko/20100101 Firefox/49.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'Accept-Language': 'zh-TW,zh;q=0.5',
        "Accept-Encoding": "gzip",
        "Connection": "keep-alive",
        "Cookie": "browserid=1178180757615078361; steamCountry=TW%7Cec9ee54d7b0da8ca2bade64a4cec7061; sessionid=97b065f7fc4fc75643e86564; timezoneOffset=28800,0; _ga=GA1.2.30895296.1571386387; strResponsiveViewPrefs=desktop; bGameHighlightAutoplayDisabled=false; _gid=GA1.2.523639413.1575597766; Steam_Language=tchinese; birthtime=880992001; lastagecheckage=2-0-1998; recentapps=%7B%221191210%22%3A1575620845%2C%22710920%22%3A1575618403%2C%221199880%22%3A1575617070%2C%221174370%22%3A1575616963%2C%22760810%22%3A1575611064%2C%22976730%22%3A1575610993%2C%221064220%22%3A1575606891%2C%221173900%22%3A1575606798%2C%22349270%22%3A1575606795%2C%22846470%22%3A1575606763%7D; app_impressions=1016920@1_2300_4__201|790740@1_2300_4__43|1191210@1_2300_4__103|585710@1_2300_4__43|1189230@1_2300_4__103|1192610@1_2300_4__103|936490@1_2300_4__103|1176020@1_2300_4__103|1179720@1_2300_4__103|760810@1_2300_4__103|1174370@1_2300_4__103|1065950@1_2300_4__103|648800@1_2300_4__40|1159540@1_2300_4__103|1171310@1_2300_4__103|1158910@1_2300_4__103|1161270@1_2300_4__103|617290@1_2300_4__hub-specials|418240@1_2300_4__hub-specials|1016920@1_2300_4__hub-specials|1174370@1_2300_4__hub-specials|1097420@1_2300_4__103|1168430@1_2300_4__103|617290@1_2300_4__201|790740@1_2300_4__43|1191210@1_2300_4__103"
    }
    r = requests.get('https://steamcommunity.com/app/' + str(r) + '/reviews/?filterLanguage=tchinese', headers=headers)
    # 確認是否下載成功
    if r.status_code == requests.codes.ok:
        # 以 BeautifulSoup 解析 HTML 程式碼
        soup = BeautifulSoup(r.text, 'html.parser')
        # print(r.text)

        # 以 CSS 的 class 抓出各類頭條新聞
        reviews = soup.find_all('div', class_='apphub_Card modalContentLink interactable')
        for review in reviews:
            nick = review.find('div', class_='apphub_CardContentAuthorBlock tall').text
            content = review.find('div', class_='apphub_CardTextContent')
            title = review.find('div', class_='title').text
            hour = review.find('div', class_='hours').text.split(' ')[1].split(' ')[0]
            comment = review.find('div', {'class': 'apphub_CardTextContent'}).text
            print(nick.split('此')[0].split('\n')[6], title, '遊玩時數' + hour,
                  comment.strip('\t').split('日')[1].split('\n')[1].strip('\t'))


def par2():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:49.0) Gecko/20100101 Firefox/49.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'Accept-Language': 'zh-TW,zh;q=0.5',
        "Accept-Encoding": "gzip",
        "Connection": "keep-alive",
        "Cookie": "browserid=1178180757615078361; steamCountry=TW%7Cec9ee54d7b0da8ca2bade64a4cec7061; sessionid=97b065f7fc4fc75643e86564; timezoneOffset=28800,0; _ga=GA1.2.30895296.1571386387; strResponsiveViewPrefs=desktop; bGameHighlightAutoplayDisabled=false; _gid=GA1.2.523639413.1575597766; Steam_Language=tchinese; birthtime=880992001; lastagecheckage=2-0-1998; recentapps=%7B%221191210%22%3A1575620845%2C%22710920%22%3A1575618403%2C%221199880%22%3A1575617070%2C%221174370%22%3A1575616963%2C%22760810%22%3A1575611064%2C%22976730%22%3A1575610993%2C%221064220%22%3A1575606891%2C%221173900%22%3A1575606798%2C%22349270%22%3A1575606795%2C%22846470%22%3A1575606763%7D; app_impressions=1016920@1_2300_4__201|790740@1_2300_4__43|1191210@1_2300_4__103|585710@1_2300_4__43|1189230@1_2300_4__103|1192610@1_2300_4__103|936490@1_2300_4__103|1176020@1_2300_4__103|1179720@1_2300_4__103|760810@1_2300_4__103|1174370@1_2300_4__103|1065950@1_2300_4__103|648800@1_2300_4__40|1159540@1_2300_4__103|1171310@1_2300_4__103|1158910@1_2300_4__103|1161270@1_2300_4__103|617290@1_2300_4__hub-specials|418240@1_2300_4__hub-specials|1016920@1_2300_4__hub-specials|1174370@1_2300_4__hub-specials|1097420@1_2300_4__103|1168430@1_2300_4__103|617290@1_2300_4__201|790740@1_2300_4__43|1191210@1_2300_4__103"
    }
    r = requests.get('https://store.steampowered.com/genre/Early%20Access/', headers=headers)
    # 確認是否下載成功
    if r.status_code == requests.codes.ok:
        # 以 BeautifulSoup 解析 HTML 程式碼
        soup = BeautifulSoup(r.text, 'html.parser')
        # print(r.text)

        # 以 CSS 的 class 抓出各類頭條新聞
        links = soup.find_all('a', class_='tab_item', limit=15)
        imgs = soup.find_all('img', class_='tab_item_cap_img', limit=15)
        name = soup.find_all('div', class_='tab_item_name', limit=15)
        price = soup.find_all('a', class_='tab_item', limit=15)
        taball = soup.find_all('div', class_='tab_item_top_tags', limit=15)

        for i in range(5):
            print(links[i].get('href'))


def jsonopen():
    with open(os.path.join("./", 'uid.json')) as f:
        result = json.load(f)
        print(result['glossary'])


if __name__ == '__main__':
    main()
