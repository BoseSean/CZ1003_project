from skyscanner.skyscanner import Flights
import json
from config import Skyscanner_Flight_APIKEY

MAX_FLIGHTS = 10


class Airlines():

    def __init__(self,
                 originplace,
                 destinationplace,
                 outbounddate,
                 inbounddate,
                 country='SG',
                 currency='SGD',
                 locale='en-GB',
                 adults=1):
        #  Get live information of flight
        self.flights_service = Flights(Skyscanner_Flight_APIKEY)
        # self.originplace = originplace
        # self.destinationplace = destinationplace
        # self.adults = adults
        self.all_result = self.flights_service.get_result(
            country=country,
            currency=currency,
            locale=locale,
            originplace=originplace,
            destinationplace=destinationplace,
            outbounddate=outbounddate,
            inbounddate=inbounddate,
            adults=adults).parsed

    def get_top(self):
        Flights = [{} for _ in range(MAX_FLIGHTS)]
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
                        Flights[counter] = FlightsLive
                        counter += 1
                    except IndexError:
                        break
                i += 1
            except IndexError:
                print(str(i) + " flights details has been listed")
                break
        return Flights
    #  Find respective OutboundLegId leg

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


if __name__ == "__main__":
    from pprint import pprint
    a = Airlines(
        originplace='SIN-sky',
        destinationplace='KHN-sky',
        outbounddate='2016-09-23',
        inbounddate='2016-10-04').get_top()
    pprint(a)
    print("Seem to be working well.")

    # # #  get agents (may delete later)
    # # FlightsLive['Agents'] = json.dumps(self.all_result['Itineraries'][i]["PricingOptions"][j]["Agents"][0])
    # #  get price
    # FlightsLive['Price'] = json.dumps(self.all_result['Itineraries'][i]["PricingOptions"][j]["Price"])
    # # # get OutboundLegId (may delete later)
    # # FlightsLive['OutboundLegId'] = json.dumps(self.all_result['Itineraries'][i]["OutboundLegId"])
    # #  get InboundLegId (may delete later)
    # # FlightsLive['InboundLegId'] = json.dumps(self.all_result['Itineraries'][i]["InboundLegId"])
    # FlightsLive['Outbound_Departure'] = json.dumps(self.all_result['Legs'][self.__outboundleg(self.all_result, i)]['Departure'])
    # FlightsLive['Outbound_Arrival'] = json.dumps(self.all_result['Legs'][self.__outboundleg(self.all_result, i)]['Arrival'])

#     # Process information
#     i = 0
#     while True:
#         FlightsLive = {}
#         try:
#             json.dumps(result['Itineraries'][i]["PricingOptions"])
#             j = 0
#             while True:
#                 try:
#                     #  get agents (may delete later)
#                     FlightsLive['Agents'] = json.dumps(result['Itineraries'][i]["PricingOptions"][j]["Agents"][0])
#                     #  get price
#                     FlightsLive['Price'] = json.dumps(result['Itineraries'][i]["PricingOptions"][j]["Price"])
#                     # get OutboundLegId (may delete later)
#                     FlightsLive['OutboundLegId'] = json.dumps(result['Itineraries'][i]["OutboundLegId"])
#                     #  get InboundLegId (may delete later)
#                     FlightsLive['InboundLegId'] = json.dumps(result['Itineraries'][i]["InboundLegId"])
#                     FlightsLive['Outbound_Departure'] = json.dumps(result['Legs'][outboundleg(result,i)]['Departure'])
#                     FlightsLive['Outbound_Arrival'] = json.dumps(result['Legs'][outboundleg(result, i)]['Arrival'])
#                     j += 1
#                     print(json.dumps(FlightsLive, indent = 4))
#                 except IndexError:
#                     break
#             i += 1
#         except IndexError:
#             print(str(i) + " flights details has been listed")
#             break
#     print("Program terminated.")
