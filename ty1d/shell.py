#! /usr/bin/env python3

import base
import sys
import argparse
import nightscout

def load_config(args):
    if args.debug:
        base.debug = True

    # if args.scan_binaries:
    #     base.scan_binaries = True

    # if not args.scan_tests:
    #     base.scan_binaries = False

    # if args.match_level != None:
    #     base.match_level = args.match_level
    
    # if args.signatures == "":
    #     signatures.load_signatures([])
    # else:
    #     signatures.load_signatures(args.signatures)

class ty1d(object):

    def __init__(self):
        parser = argparse.ArgumentParser(description="Find secrets where they shouldn't be", usage='''code_recon <command> [<args>]

In order to effectively find a needle in a haystack you need to know where the haystack is:
   local_path     Scan a local path for any secrets
   raw_text       Pipe in raw text or a binary file for scanning
''')
        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)

        getattr(self, args.command)()

    def management_console(self):
        parser = argparse.ArgumentParser(
            description='A whitespace seperated list of files or paths to scan')
        # TODO add help messages and better docs
        parser.add_argument('lifx_token', type=str) # currently a placeholder
        parser.add_argument('nightscout_token', type=str) # currently a placeholder
        parser.add_argument('lifx_label', type=str) # currently a placeholder

        args = parser.parse_args(sys.argv[2:])

        load_config(args)

        nightscout.poll_nightscout(args.nightscout_token)

