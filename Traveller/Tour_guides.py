import requests

# If any confiruration needed such as token, password or API_key, please define in config.py
# The following command will automaticly import default_config.py if there
# is no config.py.
try:
    from config import 
except ImportError:
    from default_config import *

class Tour_guide(object):

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
if __name__ == "__main__":
    from pprint import pprint
    inst = Tour_guide()
    pprint(inst.get_data())
    print("Seem to be working well.")
