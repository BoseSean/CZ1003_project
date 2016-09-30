import requests
import sqlite3

# If any confiruration needed such as token, password or API_key, please define in config.py
# The following command will automaticly import default_config.py if there
# is no config.py.
try:
    from config import
except ImportError:
    from default_config import *


class Airlines_reminder(object):

    def __init__(self, ):
        # Initialize the data needed. For now, do not need to handle the convertion between
        # readable name and standard code needed for api.
        # For example:
        #   Singapore -- SG,
        #   China -- 86
        #   John F Kennedy International Airport -- JFK
        #   23/09/2016 -- 2016-09-23
        # We will furthur decide how to handle them, for now just assume all
        # input are standard.
        self.db_conn = sqlite3.connect('db.sqlite3')
        self.cursor = db_conn.cursor()

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

    def updata_data(self, data_set, in_and_out_cities):
        out_date = data_set[0]['Outbound_Departure'][1:11]
        In_date = data_set[0]['Outbound_Departure'][1:11]
        origin_place = in_and_out_cities[0]
        dest_place = in_and_out_cities[1]

        create_cmd = ('CREATE IF NOT EXIST ? '
                        '('
                            'Price int, ' 
                            'in_city varchar(25), '
                            'out_city varchar(25), ' 
                            'Outbound_Departure char(19), ' 
                            'Outbound_Arrival char(19), ' 
                            'Outbound_Carriers varchar(20), '
                            'Inbound_Departure char(19), '
                            'Inbound_Arrival char(19), '
                            'Inbound_Carriers varchar(20), '
                            'BookingLink varchar(1500)'
                        ')'
                    )
        
        self.cursor(create_cmd, (out_date,))
        self.cursor('DELETE FROM ? WHERE ?',
                    (out_date, origin_place, dest_place))
        for flight in data_set:
            self.('INSERT INTO ? ()')

# You could regard the following part as testing which will run only if
# you execuate itself.
if __name__ == "__main__":
    from pprint import pprint
    inst = Airlines_reminder()
    pprint(inst.get_data())
    print("Seem to be working well.")
