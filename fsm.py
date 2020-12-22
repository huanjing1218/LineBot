from transitions.extensions import GraphMachine

from utils import send_text_message, send_menu


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_weather_service(self, event):
        text = event.message.text
        return text.lower() == "天氣"

    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "go to state2"

    def on_enter_weather_service(self, event):
        print("I'm entering Weather Service")

        reply_token = event.reply_token
        send_menu(reply_token)
        self.go_back()

    def on_exit_weather_service(self):
        print("Leaving Weather Service")

    def on_enter_state2(self, event):
        print("I'm entering state2")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state2")
        self.go_back()

    def on_exit_state2(self):
        print("Leaving state2")
