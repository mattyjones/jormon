#! /usr/bin/env python3

import requests
import json
import os

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

    return token, url

def poll_nightscout(token, url):

    headers = {
        "accept": "application/json",
    }

    response = requests.get(url, headers=headers)

    # Check the response code
    print(response.status_code)
    print(response.text)

    # parse the response
    current_results = json.loads(response.text)

    # How do we account for stale results?
    bg = current_results[0]['sgv']
    direction = current_results[0]['direction']

    return bg, direction
