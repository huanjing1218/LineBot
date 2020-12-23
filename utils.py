import os
import requests
import json

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ButtonsTemplate, TemplateSendMessage, MessageTemplateAction


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

def query_realtime_weather(location):
    city = location[0:3]
    town = location[3:]
    city = city.replace('台', '臺')
    result = ''
    find = False

    end_point = ['https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0003-001?Authorization=CWB-56562D80-292A-4ED6-BA0C-F6B5A1B82538&format=JSON', 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0001-001?Authorization=CWB-56562D80-292A-4ED6-BA0C-F6B5A1B82538&format=JSON']
    for i in end_point:
        if find:
            break
        data = requests.get(end_point).json()
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
        result = '查無結果\n請確認輸入是否有誤或改輸入鄰近行政區'
    return result      

"""
def send_image_url(id, img_url):
    pass
def send_button_message(id, text, buttons):
    pass
"""
