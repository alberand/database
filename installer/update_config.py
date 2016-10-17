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
server_config = './src/config.json'

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

# Fields to update in json file
fields_to_update = [
        'host',
        'port',
        'mysql_user',
        'mysql_pass',
        'mysql_db'
]

# Open and parse bash config
with open(bash_config, 'r') as _config:
    new_values = parse(_config)

# Open and save new values to json config
with open(server_config, 'r+') as _json_config:
    new_config = json.load(_json_config)
    for field in fields_to_update:
        if field == 'port':
            new_config[field] = int(new_values[field])
        new_config[field] = new_values[field]

    _json_config.seek(0)
    _json_config.write(json.dumps(new_config, indent=4, sort_keys=True))
    _json_config.truncate()


