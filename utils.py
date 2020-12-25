import os
import requests
import json

from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ButtonsTemplate, TemplateSendMessage, MessageTemplateAction, ImageSendMessage

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

load_dotenv()
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)

def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))
    return "OK"

def send_menu(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            title='天氣',
            text='請點選需要的服務',
            actions=[
                MessageTemplateAction(
                    label='即時天氣',
                    text='即時天氣'
                ),
                MessageTemplateAction(
                    label='天氣預報',
                    text='天氣預報'
                ),
                MessageTemplateAction(
                    label='雷達回波',
                    text='雷達回波'
                )
            ]
        )
    )
    line_bot_api.reply_message(reply_token, message)
    return "OK"

def check_weather(location):
    location = location.replace(' ', '')
    city = location[0:3]
    town = location[3:]
    city = city.replace('台', '臺')
    result = ''
    find = False

    website = ['https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0003-001?Authorization=CWB-56562D80-292A-4ED6-BA0C-F6B5A1B82538&format=JSON', 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0001-001?Authorization=CWB-56562D80-292A-4ED6-BA0C-F6B5A1B82538&format=JSON']
    for i in website:
        if find:
            break
        data = requests.get(i).json()
        data = data['records']['location']
        for j in data:
            if city == j['parameter'][0]['parameterValue'] and town == j['parameter'][2]['parameterValue']:
                result = j['parameter'][0]['parameterValue'] + j['parameter'][2]['parameterValue'] + '\n\n'
                time = j['time']['obsTime'].split(' ')
                result += '日期：' + time[0] + '\n'
                result += '時間：' + time[1] + '\n'
                result += '氣溫：' + j['weatherElement'][3]['elementValue'] + ' ℃\n'
                result += '濕度：' + str(round(float(j['weatherElement'][4]['elementValue']) * 100)) + ' %'
                find = True
                break

    if not find:
        result = '查無結果\n請確認輸入內容或輸入鄰近行政區'
    return result      

def check_forecast(location):
    location = location.replace(' ', '')
    city = location[0:3]
    town = location[3:]
    city = city.replace('台', '臺')
    result = ''
    taiwan = {'臺北市': '063', '新北市': '071', '基隆市': '051', '桃園市': '007', '新竹縣': '011', '新竹市': '055', '苗栗縣': '015', '臺中市': '075', '南投縣': '023', '彰化縣': '019', '雲林縣': '027', '嘉義縣': '031', '嘉義市': '059', '臺南市': '079', '高雄市': '067', '屏東縣': '035', '宜蘭縣': '003', '花蓮縣': '043', '臺東縣': '039', '澎湖縣': '047', '金門縣': '087', '連江縣': '083'}
    if city in taiwan:
        ID = taiwan.get(city)
        result += city + town + '　三天天氣預報'

        website = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-' + ID + '?Authorization=CWB-56562D80-292A-4ED6-BA0C-F6B5A1B82538&elementName=WeatherDescription'
        data = requests.get(website).json()
        data = data['records']['locations'][0]['location']
        find = False
        for i in range(len(data)):
            if town == data[i]['locationName']:
                print(len(data[i]['locationName']))
                data = data[i]['weatherElement'][0]['time']
                find = True
                break
        if find:
            for i in range(6):
                result += '\n\n' + data[i]['startTime'] + '~' + data[i]['endTime'][-8:]
                tmp = data[i]['elementValue'][0]['value'].split('。')
                for j in range(3):
                    result += '\n' + tmp[j]
        else:
            result = '查無結果\n請確認輸入內容'
    else:
        result = '查無結果\n請確認輸入內容'
    return result

def radar_echo(reply_token):
    options = Options()
    options.add_argument("--disable-notifications")
    chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
    chrome.get("https://www.cwb.gov.tw/V8/C/W/OBS_Radar.html")
    soup = BeautifulSoup(chrome.page_source, "html.parser")
    result = soup.find_all("img", {"alt": "雷達回波"})

    website = []
    for i in result:
        website.append('https://www.cwb.gov.tw' + str(i.get("src")))
    chrome.close()

    line_bot_api = LineBotApi(channel_access_token)
    message = ImageSendMessage(
            original_content_url = website[0],
            preview_image_url = website[0]
    )
    line_bot_api.reply_message(reply_token, message)
    return "OK"

"""
def send_button_message(id, text, buttons):
    pass
"""
