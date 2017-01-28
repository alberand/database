#!/bin/python3

#==============================================================================
# This script opens bash scripts with some predefined variables. Parse this file
# and then update json configuration file used by server program for
# configuration.
#==============================================================================

import sys
import json
from pprint import pprint

# Json template for server config
template = {
    "server_name": "server",
    "corrupted_storage": "./data/corrupted_data.txt",
    "data_storage": "./data/server",
    "host": "localhost",
    "ini_end": "#",
    "ini_start": "P",
    "mysql_db": "db",
    "mysql_host": "localhost",
    "mysql_pass": "pass",
    "mysql_user": "user",
    "pkg_delimeter": ";",
    "pkg_end": "#",
    "pkg_start": "@",
    "port": 5000,
    "txt_end": "\r",
    "txt_start": "T"
}

# Server configuration file
if len(sys.argv) > 1:
    tmp_server_config = sys.argv[1]
    # Bash configuration
    bash_config = sys.argv[2]
else:
    print('Server configuration file is not specified.', file=sys.stderr)
    sys.exit(1)

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
            if field[0] == 'port':
                field[1] = int(field[1])

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
new_config = template
with open(tmp_server_config, 'r+') as tmp_server_config:
    for field in fields_to_update:
        new_config[field] = new_values[field]

    new_config['data_storage'] = './data/{}'.format(new_values['catalog_name'])

    tmp_server_config.seek(0)
    tmp_server_config.write(json.dumps(new_config, indent=4, sort_keys=True))
    tmp_server_config.truncate()
