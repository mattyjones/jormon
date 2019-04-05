#! /usr/bin/env python3

# TODO pytdoc
# TODO pytest

import argparse
import pprint

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

a,b = ns.poll_nightscout(ns_token, ns_url)

print("Blood Sugar: ", a)
print("Direction: ", b)

lifx.trigger_lifx(lifx_label, lifx_token)

