# CZ1003_Traveller

This is a backend application for telegram bot which could provide useful information for Travellers, such as airlines discounts and airbnb around you.

## What does it do?

1. Track the price of air tickets for the trip around user’s preferred dates (user will be prompted to select one or more preferred dates) and notify the user through telegram when the price gets lower. The tracking will start at the moment user inputs necessary information.

2. List the accommodation information of AirBnb. The sequence of listing will be determined by the price and the overall review of each hostel (user will be prompted to enter more accurate destination).

3. List some of tour guides from certain websites (which we haven’t decided yet, but the website will be trustworthy).

4. Track the foreign exchange rate (if in need) and notify the user through telegram when the price gets lower. However, the bot will first analyse the past rates and let user know whether it is good to exchange currency as soon as possible.

5. User will be able to cancel any of above tracing and notification with immediate effect at any time.

## Usage


## Requirments

pyhton3
* [Ruquests](http://docs.python-requests.org/en/master/user/install/#install)
* [Telepot](http://telepot.readthedocs.io/en/latest/)
* [Beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)
* [skyscanner](https://github.com/Skyscanner/skyscanner-python-sdk)
