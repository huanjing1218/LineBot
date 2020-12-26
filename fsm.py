from transitions.extensions import GraphMachine

from utils import send_text_message, send_menu, check_weather, check_forecast, radar_echo


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def choose_weather_service(self, event):
        text = event.message.text
        return text == "天氣"

    def on_enter_weather_service(self, event):
        print("I'm entering Weather Service")
        reply_token = event.reply_token
        send_menu(reply_token)
        return "OK"
    
    def is_going_to_check_weather(self, event):
        text = event.message.text
        return text == "即時天氣"
    
    def on_enter_check_weather(self, event):
        print("I'm entering Search Realtime")
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入縣市以及行政區\n(例如：台南市中西區)")
        return "OK"
    
    def on_enter_weather(self, event):
        print("I'm entering Weather")
        text = event.message.text
        reply_token = event.reply_token
        send_text_message(reply_token, check_weather(text))
        self.go_back()

    def is_going_to_check_forecast(self, event):
        text = event.message.text
        return text == "天氣預報"

    def on_enter_check_forecast(self, event):
        print("I'm entering Search Forecast")
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入縣市以及行政區\n(例如：台南市中西區)")
        return "OK"

    def on_enter_weather_forecast(self, event):
        print("I'm entering Weather Forecast")
        text = event.message.text 
        reply_token = event.reply_token
        send_text_message(reply_token, check_forecast(text))
        self.go_back()

    def is_going_to_radar_echo(self, event):
        text = event.message.text
        return text == "雷達回波"

    def on_enter_radar_echo(self, event):
        print("I'm entering Radar echo")
        reply_token = event.reply_token
        radar_echo(reply_token)
        self.go_back()

    def is_going_to_backUser(self, event):
        text = event.message.text
        text = text.replace(" ", "")
        func = ["即時天氣", "天氣預報", "雷達回波"]
        return not text in func

    def is_going_to_manual(self, event):
        text = event.message.text 
        text = text.replace(" ", "")
        return (text.lower() == "?" or text.lower() == "？" )

    def on_enter_manual(self, event):
        print("I'm entering Manual")
        reply_token = event.reply_token
        send_text_message(reply_token, "不知道怎麼使用嗎？\n輸入\"天氣\"試試看吧\U00100085 ")
        self.go_back()

