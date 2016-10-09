#!/bin/python3

#==============================================================================
# This script opens bash scripts with some predefined variables. Parse this file
# and then update json configuration file used by server program for
# configuration.
#==============================================================================

import json
from pprint import pprint

# Bash configuration
bash_config = './config.cfg'
# Server configuration file
server_config = './src/config.py'

# Parse function
def parse(_file):
    result = dict()

    for line in _file.readlines():
        if line[0] == '#':
            continue
        else:
            key, value = map(rstrip, line.split('='))

        result[key] = value

    return result

# with open(server_config, 'wr') as _server:
with open(bash_config, 'r') as _config:
    pprint(parse(_config))

