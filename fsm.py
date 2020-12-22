from transitions.extensions import GraphMachine

from utils import send_text_message, send_menu, query_realtime_weather


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_weather_service(self, event):
        text = event.message.text
        return text.lower() == "天氣"
    
    def is_going_to_type_location(self, event):
        text = event.message.text
        return text.lower() == "即時天氣"
    '''
    def is_going_to_realtime_weather(self, event):
        text = event.message.text
        reply_token = event.reply_token
        send_text_message(reply_token, query_realtime_weather(text.lower()))
        return True
    '''
    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "go to state2"

    def on_enter_weather_service(self, event):
        print("I'm entering Weather Service")
        reply_token = event.reply_token
        send_menu(reply_token)
        return "OK"

    def on_exit_weather_service(self):
        print("Leaving Weather Service")

    def on_enter_type_location(self, event):
        print("I'm entering Type Location")

        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入縣市及行政區\n例如：台北市信義區")
        return "OK"

    def on_exit_type_location(self):
        print("Leaving Type Location")

    def on_enter_realtime_weather(self, event):
        print("I'm entering Realtime Weather")

        text = event.message.text
        reply_token = event.reply_token
        send_text_message(reply_token, query_realtime_weather(text.lower())
        return "OK"

    def on_exit_realtime_weather(self):
        print("Leaving Realtime Weather")

    def on_enter_state2(self, event):
        print("I'm entering state2")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state2")
        self.go_back()

    def on_exit_state2(self):
        print("Leaving state2")
