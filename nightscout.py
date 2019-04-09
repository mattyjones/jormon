#! /usr/bin/env python3

import requests
import json
import os
import time
import calendar
import sys


def set_config(args):

    # Configuration Order
    # 1. env
    # 2. flag
    token = ""
    url = ""

    if args.nightscout_token:
        token = args.nightscout_token
    elif 'NIGHTSCOUT_TOKEN' in os.environ:
        if not os.environ['NIGHTSCOUT_TOKEN'] == "":
            token = os.environ['NIGHTSCOUT_TOKEN']

    if args.nightscout_url:
        url = args.nightscout_url
    elif 'NIGHTSCOUT_URL' in os.environ:
        if not os.environ['NIGHTSCOUT_URL'] == "":
            token = os.environ['NIGHTSCOUT_URL']
    else:
        print("A nightscout url is needed")
        # set some logging here instead of exiting
        sys.exit(2)

    return token, url

def validate_data_freshness(data_time):

    # stale results is the age at which results are no longer considered valid, they should still be reported
    # but we should do something to note that they are stale.
    # This is in minutes
    stale_time = 6

    fresh = False

    # Get the current timestamp in GMT
    current_time = calendar.timegm(time.gmtime())

    data_time = data_time[:-3]
    data_time_int = int(data_time)

    # The number of minutes ago that the data was last checked
    last_check = (current_time - data_time_int) /60

    if last_check > stale_time:
        fresh = False
        # print("The data is %d minutes old and outside the requested freshness range" % last_check)
    else:
        fresh = True
        # print("The data is %d minutes old" % last_check)

    return fresh



def poll_nightscout(token, url):

    headers = {
        "accept": "application/json",
    }

    response = requests.get(url, headers=headers)

    # Check the response code

    if response.status_code != 200:
        # set some logging here instead of exiting
        # we should account for network instability as well and try a few times to get data
        sys.exit(2)

    # parse the response
    current_results = json.loads(response.text)
    fresh = validate_data_freshness(str(current_results[0]['date']))

    bg = current_results[0]['sgv']
    direction = current_results[0]['direction']

    print(fresh)

    return bg, direction, fresh
