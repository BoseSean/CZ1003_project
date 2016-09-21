from time import gmtime, strftime, sleep
import telepot
from pprint import pprint

from Airbnbs import *
from Airlines import *
from Tour_guides import *
# from Responsers import *


import telepot.helper
from telepot.namedtuple import (
    InlineQueryResultArticle, InputTextMessageContent,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton)

from config import Telegram_TOKEN


def log(log_message, msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print("[", strftime("%Y-%m-%d %H:%M:%S", gmtime()), "]"
          "  ", log_message + ":", content_type, chat_type, chat_id, msg["from"]["first_name"])
    print("                            " + "-" + msg["text"])


def command_processor(msg):
    px = "/"
    separator = " "
    text = msg["text"]
    if text.startswith(px):
        splited_command = text[len(px):].split(separator)
        return splited_command
    return False


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    log("Message", msg)

    if content_type != "text":
        return
    try:
        content_type = msg["entities"][0]["type"]
        content = command_processor(msg)
    except KeyError:
        content_type = "text"
        content = msg["text"]

    if content_type == "text":
        if content == "airlines assistant":
            markup = ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text="Get current airline price")],
                [KeyboardButton(text="Set airline price alert")]
            ],
                one_time_keyboard=True)
            bot.sendMessage(
                chat_id, "Okay, which one do you want? \n Powered by <a href="Skyscanner.net/">Skyscanner</a> ", parse_mode="HTML" ,reply_markup=markup)

        elif content == "Get current airline price":
            bot.sendMessage(
                chat_id,
                "Start with /check and seperate with, \n<origin place> \n<destination place> \n<adult passengers> \n<outbound date> \n<inbounddate>",
            )

        elif content == "Set airline price alert":
            bot.sendMessage(
                chat_id,
                "Start with /alert and seperate with, \n<origin place> \n<destination place> \n<adult passengers> \n<outbound date> \n<inbounddate> \n<target price>",
            )
        else:
            markup = ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text="airlines assistant")],
            ],
                one_time_keyboard=True)
            bot.sendMessage(
                chat_id,
                "Hello, this is your travel assistant! What can I do for you?",
                reply_markup=markup
            )
    elif content_type == "bot_command":
        if content[0] == "check":
            Airlines(content[1:]).response(chat_id)
        # if content[0] == "alert":
        #     Airlines_Reminder

bot = telepot.Bot(Telegram_TOKEN)
# bot.message_loop(handle)
# pprint(bot.getUpdates())
bot.message_loop({"chat": on_chat_message})
# print ("Listening ...")
while 1:

    sleep(100)
