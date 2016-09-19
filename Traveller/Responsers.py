
class Keymap_responser(object):

    def __init__(self, mode):
        self.key_dict = {
            "ariline services":    KeyboardMarkup(keyboard=[
                [KeyboardButton(
                    text="Get current airline price", callback_data="Airline current")],
                [KeyboardButton(
                    text="Set airline price alert", callback_data="Airline alert")]
            ]),
        }
        self.keyboard = key_dict[mode]

class Usage_responser(object):
    """docstring for Usage_responser"""

    def __init__(self, mode):
        self.message_dict = {
            "Airline curren": " Start with / and seperate with, \n<origin place> \n<destination place> \n<adult passengers> \n<outbound date> \n<inbounddate>",
            "Airline alert": " Start with / and seperate with, \n<origin place> \n<destination place> \n<adult passengers> \n<outbound date> \n<inbounddate> \n<target price>",
        }
        self.message = self.message_dict[mode]

class Error_responser(object):
    """docstring for Error_responser"""
    def __init__(self, arg):
        pass
