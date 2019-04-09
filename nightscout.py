#! /usr/bin/env python3

import requests
import json
import os
import time
import calendar


def set_config(args):

    # the order we want is file -> env -> flag with the last one taking the cake

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

def poll_nightscout(token, url):

    # stale results is the age at which results are no longer considered valid, they should still be reported
    # but we should do something to note that they are stale.
    # This is in minutes
    stale_time = 6

    headers = {
        "accept": "application/json",
    }

    response = requests.get(url, headers=headers)

    # Check the response code
    print(response.status_code)
    print(response.text)

    # Get the current timestamp in GMT
    current_time = calendar.timegm(time.gmtime())

    # parse the response
    current_results = json.loads(response.text)
    data_time_int = current_results[0]['date']
    data_time_str = str(data_time_int)
    data_time_str = data_time_str[:-3]
    data_time_int = int(data_time_str)

    # The number of minutes ago that the data was last checked
    last_check = (current_time - data_time_int) /60

    if last_check > stale_time:
        print("The data is %d minutes old and outside the requested freshness range" % last_check)
    else:
        print("The data is %d minutes old" % last_check)

    bg = current_results[0]['sgv']
    direction = current_results[0]['direction']

    return bg, direction
