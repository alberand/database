#!/usr/bin/python3

import sys
import configparser

config = configparser.ConfigParser()
config.readfp(sys.stdin)

for sec in config.sections():
    print("declare -A {}".format(sec))
    for key, val in config.items(sec):
        print('{}[{}]="{}"'.format(sec, key, val))
