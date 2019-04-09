#! /usr/bin/env python3

import requests
import json
import sys
import os

def set_config(args):

    # the order we want is file -> env -> flag with the last one taking the cake

    token = ""
    label = ""

    if args.lifx_token:
        token = args.lifx_token
    elif 'LIFX_TOKEN' in os.environ:
        if not os.environ['LIFX_TOKEN'] == "":
            token = os.environ['LIFX_TOKEN']
    else:
        print("A lifx token is required")
        # set some logging here instead of exiting
        sys.exit(2)

    if args.lifx_label:
        label = args.lifx_label
    elif 'LIFX_LABEL' in os.environ:
        if not os.environ['LIFX_LABEL'] == "":
            token = os.environ['LIFX_LABEL']
    else:
        print("A lifx label is required")
        # set some logging here instead of exiting
        sys.exit(2)

    return token, label


def debug_lifx():

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

def discover_lifx_devices(token):
    # Url to get a list of known devices for the auth token
    DEVICE_DISCOVERY_URL = "https://api.lifx.com/v1/lights/all"

    headers = {
    "Authorization": "Bearer %s" % token,
}

    response = requests.get(DEVICE_DISCOVERY_URL, headers=headers)

    # parse the response
    device_hash = json.loads(response.text)

    return device_hash

# TODO check for a valid token
# TODO check for bad json (maybe key error)
def trigger_lifx(label, token, color):
    debug = False

    # get a list of devices
    devices = discover_lifx_devices(token)
    device_id = ""

    # get the device is we want to trigger
    for d in devices:
        if d['label'] == label:
            device_id = d['id']

    # Url to call interact with a device
    DEVICE_USAGE_URL = "https://api.lifx.com/v1/lights/id:"

    device_url = DEVICE_USAGE_URL + device_id + '/state'

    headers = {
        "Authorization": "Bearer %s" % token,
    }

    # if debuging the devices, set a sample payload
    if debug:
        new_state = debug_lifx()
    else:
        new_state = {
            "power": "on",
            "brightness": 1,
            "color": color,
        }


    # update the device
    response = requests.put(device_url, data=new_state, headers=headers)
    # parse the response and status to make sure we did what we wanted to do
    print(response.status_code)
    print(response.text)
