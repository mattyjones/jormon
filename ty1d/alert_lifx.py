#! /usr/bin/env python3

import requests
import json


def debug_lifx(id):

	# an array of statuses to go through for debugging purposes
    # https://api.developer.lifx.com/docs/set-state
    status = [
        {"power": "on", "brightness": 1, "color": "white"},
        {"power": "on", "brightness": 1, "color": "red"},
        {"power": "on", "brightness": 1, "color": "orange"},
        {"power": "on", "brightness": 1, "color": "yellow"},
        {"power": "on", "brightness": 1, "color": "green"},
        {"power": "off"}
    ]

    return status

def discover_lifx_devices():

    headers = {
    "Authorization": "Bearer %s" % TOKEN,
}

    response = requests.get(DEVICE_DISCOVERY_URL, headers=headers)

    # parse the response
    device_hash = json.loads(response.text)

    return device_hash

def trigger_lifx(id):

    device_url = DEVICE_USAGE_URL + id + '/state'

    headers = {
        "Authorization": "Bearer %s" % TOKEN,
    }

    # if debuging the devices, set a sample payload
    if debug:
        new_status = debug_lifx(id)
    else:
        new_status = {
            "power": "on",
            "brightness": 1,
        }

    for s in new_status:
        s2 = json.dumps(s)

        response = requests.put(device_url, data=s2, headers=headers)
