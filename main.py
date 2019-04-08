#! /usr/bin/env python3

# TODO pytdoc
# TODO pytest

import argparse

import lifx
import nightscout as ns

debug = False

parser = argparse.ArgumentParser( description='Configuration options')
# TODO add help messages and better docs
# TODO add some sort of config file
parser.add_argument('--lifx_label', type=str)
parser.add_argument('--lifx_token', type=str)
parser.add_argument('--nightscout_token', type=str)
parser.add_argument('--nightscout_url', type=str)

args = parser.parse_args()

lifx_token, lifx_label = lifx.set_config(args)
ns_token, ns_url = ns.set_config(args)


# print("LIFX Token: " + lifx_token)
# print("Nightscout Token: " + ns_token)
# print("Nightscout Url: " + ns_url)
# print("LIFX Label: " + lifx_label)

blood_sugar,direction = ns.poll_nightscout(ns_token, ns_url)

print("Blood Sugar: ", blood_sugar)
print("Direction: ", direction)

# how do we turn the light off when the condition goes away but respect the user
# something like if the light is on already then change the color for 30s then go back to the previous state
# if the light was off then turn it on to the correct color for 30s, then turn it back off (returning it to its previous state)
# TODO need to capture the current state of the device

color = 'white'
if blood_sugar < 60:
    color = 'red'
elif blood_sugar < 80:
    color = 'orange'
elif blood_sugar > 300:
    color = 'red'

# should just pass in a state
lifx.trigger_lifx(lifx_label, lifx_token, color)

