#  ------License------
#  You must display the text “Powered by”, followed by the Skyscanner logo, as shown below
#  Powered by (Skyscanner Logo)
#  The whole element must link to Skyscanner.net.
#  You can choose exactly how and where to display this, but it should be obvious to end-users
#  when Skyscanner data has been used.

from skyscanner.skyscanner import Flights
import json
import datetime
# If any confiruration needed such as token, password or API_key, please define in config.py
# The following command will automaticly import default_config.py if there
# is no config.py.
# form Airlines_reminder import *
# import db
import sqlite3
try:
    from config import Skyscanner_Flight_APIKEY
except ImportError:
    from default_config import Skyscanner_Flight_APIKEY

MAX_FLIGHTS = 10


class Airlines():

    def __init__(self, args, bot, chat_id):
        # Initialize the data needed. For now, do not need to handle the convertion between
        # readable name and standard code needed for api.
        # For example:
        #   Singapore -- SG,
        #   China -- 86
        #   John F Kennedy International Airport -- JFK
        #   23/09/2016 -- 2016-09-23
        # We will furthur decide how to handle them, for now just assume all input
        # are standard.

        #  Get live information of flight
        self.bot = bot
        self.chat_id = chat_id

        self.status = False
        if self.__check_input(args):
            self.status = True
            self.flights_service = Flights(Skyscanner_Flight_APIKEY)

            originplace, destinationplace, adults, outbounddate, inbounddate = args
            country = "SG"
            currency = "SGD"
            locale = "en-GB"

            originplace = self.__get_citycode(originplace)
            destinationplace = self.__get_citycode(destinationplace)

            
            destinationplace = 'CGK'
            self.all_result = self.flights_service.get_result(
                country=country,
                currency=currency,
                locale=locale,
                originplace=originplace + "-iata",
                destinationplace=destinationplace + "-iata",
                outbounddate=outbounddate,
                inbounddate=inbounddate,
                adults=int(adults)).parsed
            import pdb; pdb.set_trace()
        self.response()

    def __check_input(self, args):
        def data_validate(date_text):
            try:
                datetime.datetime.strptime(date_text, '%Y-%m-%d')
            except ValueError:
                return True
            return False
        errors = [0, 0, 0, 0]
        originplace, destinationplace, adults, outbounddate, inbounddate = args
        originplace = self.__get_citycode(originplace)
        destinationplace = self.__get_citycode(destinationplace)
        if originplace == 'No result':
            errors[0] = 1
        if destinationplace == 'No result':
            errors[1] = 1
        if data_validate(outbounddate):
            errors[2] = 1
        if data_validate(inbounddate):
            errors[3] = 1

        if 1 in errors:
            tmp = {0: "Original place", 1: "Destination place",
                   2: "Departure time", 3: "Back time"}
            self.response([tmp[i] for i in range(4) if errors[i] == 1])
        else:
            return True

    def get_data(self):
        # TODO: This function should be returning the final usable data in a
        # dict.
        flights = [{} for _ in range(MAX_FLIGHTS)]
        i = 0
        counter = 0
        while True:
            FlightsLive = {}
            try:
                json.dumps(self.all_result['Itineraries'][i]["PricingOptions"])
                j = 0
                while True:
                    try:
                        #  get price
                        FlightsLive['Price'] = json.dumps(self.all_result['Itineraries'][
                                                          i]["PricingOptions"][j]["Price"])
                        # get OutboundLegId (may delete later)
                        # FlightsLive['OutboundLegId'] = json.dumps(self.all_result['Itineraries'][i]["OutboundLegId"])
                        FlightsLive['Outbound_Departure'] = json.dumps(
                            self.all_result['Legs'][self.__outboundleg(self.all_result, i)]['Departure'])
                        FlightsLive['Outbound_Arrival'] = json.dumps(
                            self.all_result['Legs'][self.__outboundleg(self.all_result, i)]['Arrival'])
                        FlightsLive['Outbound_Carriers'] = self.__findcarriers(json.dumps(self.all_result[
                                                                               'Legs'][self.__outboundleg(self.all_result, i)]['Carriers'][0]), self.all_result)
                        FlightsLive['Outbound_Stops'] = self.__findplaces(json.dumps(self.all_result[
                                                                          'Legs'][self.__outboundleg(self.all_result, i)]['Stops'][0]), self.all_result)
                        # get InboundLegId (may delete later)
                        # FlightsLive['InboundLegId'] = json.dumps(self.all_result['Itineraries'][i]["InboundLegId"])
                        FlightsLive['Inbound_Departure'] = json.dumps(
                            self.all_result['Legs'][self.__inboundleg(self.all_result, i)]['Departure'])
                        FlightsLive['Inbound_Arrival'] = json.dumps(
                            self.all_result['Legs'][self.__inboundleg(self.all_result, i)]['Arrival'])
                        FlightsLive['Inbound_Carriers'] = self.__findcarriers(json.dumps(
                            self.all_result['Legs'][self.__inboundleg(self.all_result, i)]['Carriers'][0]), self.all_result)
                        FlightsLive['Inbound_Stops'] = self.__findplaces(json.dumps(
                            self.all_result['Legs'][self.__inboundleg(self.all_result, i)]['Stops'][0]), self.all_result)
                        j += 1
                        flights[counter] = FlightsLive
                        counter += 1
                    except IndexError:
                        break
                i += 1
            except IndexError:
                # print(str(i) + " flights details has been listed")
                break
        # Airlines_reminder().updata_data(flights[0], db_conn)
        return flights

    def response(self, etc=None):

        if self.status:
            for flight in self.get_data():
                message_content = """<b>%s SGD</b>""" % (flight[
                    'Price'])
                self.bot.sendMessage(
                    self.chat_id,
                    message_content,
                    parse_mode="HTML")
        else:
            message_content = "Invalid"
            for i in etc:
                message_content += " " + i
            message_content += "."
            self.bot.sendMessage(
                self.chat_id,
                message_content)

        # if not type:
        #     for flight in self.get_data():
        #         message_content = """<b>%s SGD</b>""" % (flight[
        #             'Price'])
        #         self.bot.sendMessage(
        #             self.chat_id,
        #             message_content,
        #             parse_mode="HTML")
        # elif type == "error":
        #     message_content = "Invalid"
        #     for i in etc:
        #         message_content += " " + i
        #     message_content += "."
        #     self.bot.sendMessage(
        #         self.chat_id,
        #         message_content)

    # Other functions:
    # All other functions, except get_data(),
    # 1. should make name start with __
    # 2. should make self be the first parameter
    # for example:
    #
    # # Pre-process the data needed
    # def __pre_process(self, data):
    #   return ...

    # Save the data into the database to reduce the requests.
    # def __save_data(self):

    # Get city code
    def __get_citycode(self, city):
        db_conn = sqlite3.connect('db.sqlite3')
        cursor = db_conn.cursor()
        res = cursor.execute(
            'SELECT * FROM airport_info WHERE city=?', (city.lower(),)).fetchall()
        if res != []:
            return res[0][1]
        else:
            return 'No result'
        cursor.close()
        db_conn.close()

    # Find respective OutboundLegId leg
    def __outboundleg(self, all_result, i):
        k = 0
        while True:
            OutboundLegId = json.dumps(
                all_result['Itineraries'][i]["OutboundLegId"])
            Id = json.dumps(all_result['Legs'][k]['Id'])
            if Id == OutboundLegId:
                return k
                break
            else:
                k += 1

    # Find respective InboundLegId leg
    def __inboundleg(self, all_result, i):
        k = 0
        while True:
            InboundLegId = json.dumps(
                all_result['Itineraries'][i]["InboundLegId"])
            Id = json.dumps(all_result['Legs'][k]['Id'])
            if Id == InboundLegId:
                return k
                break
            else:
                k += 1

    # Get respective outbound SegmentsIds
    def __outsegments(self, all_result, i):
        k = 0
        while True:
            segmentids = json.dumps(all_result["Legs"][i]["SegmentIds"])
            Id = json.dumps(all_result['Legs'][k]['Id'])
            if Id == OutboundLegId:
                return k
                break
            else:
                k += 1

    # Find respective places
    def __findplaces(self, places, all_result):
        k = 0
        while True:
            if places == json.dumps(all_result['Places'][k]['Id']):
                places = json.dumps(all_result['Places'][k]['Name'])
                return places
                break
            else:
                k += 1

    # Find respective carriers
    def __findcarriers(self, carriers, all_result):
        k = 0
        while True:
            if carriers == json.dumps(all_result['Carriers'][k]['Id']):
                carriers = json.dumps(all_result['Carriers'][k]['Name'])
                return carriers
                break
            else:
                k += 1

# You could regard the following part as testing which will run only if
# you execute itself.
if __name__ == "__main__":
    from pprint import pprint
    a = Airlines(
        ['SIN-sky',
         'KHN-sky',
         '2016-09-23',
         '2016-10-29']).get_data()
    pprint(a)
    print("Seem to be working well.")
