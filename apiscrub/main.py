#!/usr/bin/env python

'''
Scrubs an OpenAPI file for distribution.

Usage:
scrub --keep admin channels/openapi.yaml channels/admin.yaml

Resources in the OpenAPI file are marked with a string or list of tags. This
also works for examples!

- name: param1
  x-only: admin
'''

import argparse
import sys

from ruamel.yaml import YAML

from apiscrub import process


def run():
    # Handle args and process the files!
    parser = argparse.ArgumentParser()
    parser.add_argument('source', help='Source OpenAPI document')
    parser.add_argument(
        'destination', help='Destination for rendered OpenAPI output')

    parser.add_argument('-t', '--tag', default='x-only',
                        help='Object property tag name to check')
    parser.add_argument('-k', '--keep', default='',
                        help='Names to keep in the output')

    args = parser.parse_args()

    # Use the default (round-trip) settings.
    yaml = YAML()

    if args.source == '-':
        src = sys.stdin
    else:
        src = open(args.source)

    doc = yaml.load(src)
    process(args.tag, set(args.keep.split(',')), doc)

    if args.destination == '-':
        dest = sys.stdout
    else:
        dest = open(args.destination, 'w')

    yaml.dump(doc, dest)


if __name__ == '__main__':
    run()
