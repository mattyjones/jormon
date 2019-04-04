#! /usr/bin/env python3

import requests
import json

def poll_nightscout(token):

    poll_url = "https://ty1d.herokuapp.com/api/v1/entries/sgv?count=1"

    headers = {
        "accept": "application/json",
    }

    response = requests.get(poll_url, headers=headers)

    print(response.status_code)

    # parse the response
    current_results = json.loads(response.text)

    # print(current_results[0].sgv)
    # print(current_results[0].direction)

    # How do we account for stale results?
    bg = current_results[0]['sgv']
    direction = current_results[0]['direction']


    return bg, direction
