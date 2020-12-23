from transitions.extensions import GraphMachine

from utils import send_text_message, send_menu, query_realtime_weather


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_weather_service(self, event):
        text = event.message.text
        return text.lower() == "天氣"
    
    def is_going_to_search_realtime(self, event):
        text = event.message.text
        return text.lower() == "即時天氣"

    def is_going_to_search_forecast(self, event):
        text = event.message.text
        return text.lower() == "天氣預報"

    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "go to state2"

    def on_enter_weather_service(self, event):
        print("I'm entering Weather Service")
        reply_token = event.reply_token
        send_menu(reply_token)
        return "OK"

    def on_enter_search_realtime(self, event):
        print("I'm entering Search Realtime")
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入縣市以及行政區\n(例如：台南市中西區)")
        return "OK"

    def on_enter_search_forecast(self, event):
        print("I'm entering Search Forecast")
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入縣市以及行政區\n(例如：台南市中西區)")
        return "OK"  

    def on_enter_realtime_weather(self, event):
        print("I'm entering Realtime Weather")
        text = event.message.text
        reply_token = event.reply_token
        send_text_message(reply_token,  query_realtime_weather(text))
        self.go_back()

    def on_enter_weather_forecast(self, event):
        print("I'm entering Weather Forecast")
        text = event.message.text 
        reply_token = event.reply_token
        send_text_message(reply_token, "預報結果")
        self.go_back()

    def on_enter_state2(self, event):
        print("I'm entering state2")

        reply_token = event.reply_token
        send_text_message(reply_token, "Test in state2 123123")
        self.go_back()

    def on_exit_state2(self):
        print("Leaving state2")
