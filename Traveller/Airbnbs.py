import requests

# If any confiruration needed such as token, password or API_key, please define in config.py
# The following command will automaticly import default_config.py if there
# is no config.py.
try:
    from config import *
except ImportError:
    from default_config import *
import urllib.request
from bs4 import BeautifulSoup


class Airbnbs(object):

    Max_rooms = 10

    def __init__(self, args, bot, chat_id):
        # Initialize the data needed. For now, do not need to handle the convertion between
        # readable name and standard code needed for api.
        # For example:
        #   Singapore -- SG,
        #   China -- 86
        #   John F Kennedy International Airport -- JFK
        #   23/09/2016 -- 2016-09-23
        # We will furthur decide how to handle them, for now just assume all
        # input are standard.
        self.bot = bot
        self.chat_id = chat_id

        location, checkin, checkout, guests = args
        #  format of date: dd-mm-yy

        self.url = 'https://www.airbnb.com.sg/s/' + location + '?guests=' + guests + '&checkin=' + \
                checkin + '&checkout=' + checkout + '&s_tag=sdz88HoP&allow_override%5B%5D='
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'
        self.opener = urllib.request.build_opener()
        self.opener.addheaders = [('User-Agent', self.user_agent)]

        try:
            self.request = urllib.request.Request(self.url)
            self.response_ = self.opener.open(self.request)
        except urllib.request.URLError as e:
            print (e.reason)
            print (e.code)
        else:
            self.soup = BeautifulSoup(self.response_.read(), "html.parser")

        self.response()


    def get_data(self):
        # TODO: This function should be returning the final usable data.

        # Other functions:
        # All other functions, except get_data(),
        # 1. should make name start with __
        # 2. should make self be the first parameter
        # for example:
        #
        # # Pre-process the data needed
        # def __pre_process(self, data):
        #   return ...

        # You could regard the following part as testing which will run only if
        # you execuate itself.
        i = 0
        counter = 0
        rooms = [{}]
        while True:
            self.RoomsLive = {}
            try:
                self.link = self.soup.find("span", class_="price-amount")
                self.RoomsLive['price'] = self.soup.find("span", class_="price-amount").string
                self.RoomsLive['roomID'] = self.get_room_id()
                rooms[counter] = self.RoomsLive
                counter += 1
                self.link = self.link.find_next("span", class_="price-amount")
                i += 1
            except IndexError:
                break
        return rooms


    def get_room_id(self):
        list_0 = str(self.link).split('.')
        for element in list_0:
            if element[0] == '$':
                room_id = element[1:]
        return room_id

    def response(self, etc=None):
        for rooms in self.get_data():
            message_content = 'https://www.airbnb.com.sg/rooms/' + self.RoomsLive['roomID'] + \
                    '?checkin=' + "23-10-2016" + '&checkout=' + "27-10-2016" + '&guests=' + "1"
            self.bot.sendMessage(
                    self.chat_id,
                    message_content,
                    parse_mode="HTML")

if __name__ == "__main__":
    from pprint import pprint
    inst = Airbnbs()
    pprint(inst.get_data())
    print("Seem to be working well.")
