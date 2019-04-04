#! /usr/bin/python3

import pprint

# Internal Constants

# TOKEN is the api token needed by lifx
TOKEN = 'c5bb638f07930424c179ab001cc5e74db2a62e7f3aa50ebcb3843012d32dac6c'

# Url to get a list of known devices for the auth token
DEVICE_DISCOVERY_URL = "https://api.lifx.com/v1/lights/all"

# Url to call interact with a device
DEVICE_USAGE_URL = "https://api.lifx.com/v1/lights/id:"

debug = True

pp = pprint.PrettyPrinter(indent=4)