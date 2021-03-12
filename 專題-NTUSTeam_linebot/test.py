import requests
from bs4 import BeautifulSoup


def test():
    newlink = []
    newlink.clear()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:49.0) Gecko/20100101 Firefox/49.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-TW,zh;q=0.5",
        "Accept-Encoding": "gzip",
        "Connection": "keep-alive",
        "Cookie": "browserid=1178180757615078361; steamCountry=TW%7Cec9ee54d7b0da8ca2bade64a4cec7061; sessionid=97b065f7fc4fc75643e86564; timezoneOffset=28800,0; _ga=GA1.2.30895296.1571386387; strResponsiveViewPrefs=desktop; bGameHighlightAutoplayDisabled=false; _gid=GA1.2.523639413.1575597766; Steam_Language=tchinese; birthtime=880992001; lastagecheckage=2-0-1998; recentapps=%7B%221191210%22%3A1575620845%2C%22710920%22%3A1575618403%2C%221199880%22%3A1575617070%2C%221174370%22%3A1575616963%2C%22760810%22%3A1575611064%2C%22976730%22%3A1575610993%2C%221064220%22%3A1575606891%2C%221173900%22%3A1575606798%2C%22349270%22%3A1575606795%2C%22846470%22%3A1575606763%7D; app_impressions=1016920@1_2300_4__201|790740@1_2300_4__43|1191210@1_2300_4__103|585710@1_2300_4__43|1189230@1_2300_4__103|1192610@1_2300_4__103|936490@1_2300_4__103|1176020@1_2300_4__103|1179720@1_2300_4__103|760810@1_2300_4__103|1174370@1_2300_4__103|1065950@1_2300_4__103|648800@1_2300_4__40|1159540@1_2300_4__103|1171310@1_2300_4__103|1158910@1_2300_4__103|1161270@1_2300_4__103|617290@1_2300_4__hub-specials|418240@1_2300_4__hub-specials|1016920@1_2300_4__hub-specials|1174370@1_2300_4__hub-specials|1097420@1_2300_4__103|1168430@1_2300_4__103|617290@1_2300_4__201|790740@1_2300_4__43|1191210@1_2300_4__103"
    }
    r = requests.get('https://store.steampowered.com/search/?filter=topsellers', headers=headers)

    # 確認是否下載成功
    if r.status_code == requests.codes.ok:
        # 以 BeautifulSoup 解析 HTML 程式碼
        soup = BeautifulSoup(r.text, 'html.parser')
        # print(r.text)

        # 以 CSS 的 class 抓出各類頭條新聞

        # 可能links要改用href的方式抓
        links = soup.find_all('a', class_='search_result_row', limit=15)
        newlink.append(links[14].get('href'))
        #name = soup.find_all('span', class_='title', limit=15)
        print(newlink)
        #print(name)
        # imgs = soup.find_all('div', class_='col search_capsule', limit=15)
        # name = soup.find_all('span', class_='title', limit=15)
        # price = soup.find_all('div', class_='col search_price_discount_combined responsive_secondrow.', limit=1)
        # print(price[0].text.strip())
        # taball = soup.find_all('div', class_='tab_item_top_tags', limit=15)

        # print(links)


def main():
    test()


if __name__ == '__main__':
    main()
