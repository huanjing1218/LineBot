import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ButtonsTemplate


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
            title='天氣服務',
            text='請點選需要的服務',
            actions=[
                MessageTemplateAction(
                    label='weather',
                    text='即時天氣'
                ),
                MessageTemplateAction(
                    label='forecast',
                    text='天氣預報'
                )
            ]
        )
    )
    line_bot_api.reply_message(reply_token, message)
    return "OK"

"""
def send_image_url(id, img_url):
    pass
def send_button_message(id, text, buttons):
    pass
"""
