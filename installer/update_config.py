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
server_config = ['./src/config.py', './scripts/config.py']

# Parse function
def parse(_file):
    result = dict()

    for line in _file.readlines():
        if line[0] in ['#', '\n'] or not line:
            continue
        else:
            field = [item.rstrip() for item in line.split('=')]
            if field[1][0] == '"':
                field[1] = field[1][1:-1]

        result[field[0]] = field[1]

    return result

# with open(server_config, 'wr') as _server:

fields_to_update = [
        'host',
        'port',
        'mysql_user',
        'mysql_pass',
        'mysql_db'
]
with open(bash_config, 'r') as _config:
    pprint(parse(_config))

