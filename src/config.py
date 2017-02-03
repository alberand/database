#!/bin/python

import os
import sys
import json
import logging
import configparser
from datetime import datetime

logger = logging.getLogger(__name__)

config_dir = os.path.dirname(os.path.abspath(__file__))

# Get configuration file name which send as first argumen to the program
if len(sys.argv) < 2:
    logging.error('Please specify config name.')
    sys.exit(1)
else:
    config_name = sys.argv[1]

# config = json.load(open(os.path.join(config_dir, config_name), 'r'))
parser = configparser.ConfigParser()
parser.read(os.path.join(config_dir, config_name))
items = parser['CONFIG'].items()

config = dict(items)
config['port'] = int(config['port'])

config['pkg_delimeter'] = ';'
config['pkg_end'] = '#'
config['pkg_start'] = '@'
config['txt_end'] = '\r'
config['txt_start'] = 'T'
config['ini_end'] = "#"
config['ini_start'] = "P"
config['data_storage'] = './data/{}'.format(config['server_name'])

# This list define package structure. Thus, in which order data are arranged.
# Empty fields doesn't appear in data structure. They are just skipped, also as
# non defined fields.
current_pkg_version = '1c'
pkg_versions = {
        '1a':[
            # 'ses_time',
            'date',
            'time',
            'latitude',
            'longitude',
            'speed',
            'course',
            'gps_altitude',
            'sat_num',
            'gps_state',
            'gsm_sig_str'
        ],
        '1b':[
            # 'ses_time',
            'date',
            'time',
            'latitude',
            'longitude',
            'speed',
            'course',
            'gps_altitude',
            'sat_num',
            'gps_state',
            'gsm_sig_str',
            'net_provider',
            'network_type'
        ],
        '1c':[
            # 'ses_time',
            'date',
            'time',
            'latitude',
            'longitude',
            'speed',
            'course',
            'gps_altitude',
            'sat_num',
            'gps_state',
            'gsm_sig_str',
            'net_provider',
            'network_type',
            'x_acc',
            'y_acc',
            'z_acc'
        ]
}

pkg_structure = pkg_versions[current_pkg_version]

# Messages package structure
msg_structure = [
        'msg',
        'ses_time',
        'ses_id',
]

# This dictionary define data handlers. There is no need to keep right order.
# Handler should be pointer (object) to callable function not result of calling
# this function.
handlers = {
        # Name  # Handler
        'module_id':    int,
        'ses_time':     lambda time: 
                                datetime.strptime(time, '%H:%M:%S').time(),
        'date':         lambda date: 
                                datetime.strptime(date, '%d.%m.%y').date(),
        'time':         lambda time: 
                                datetime.strptime(time, '%H:%M:%S.%f').time(),
        'time_ms_out':  lambda time: 
                                datetime.strptime(time, '%H:%M:%S').time(),
        'latitude':     lambda data: [float(data[:-1]), str(data[-1])],
        'longitude':    lambda data: [float(data[:-1]), str(data[-1])],
        'course':       float,
        'gps_altitude': float,
        'speed':        float,
        'temperature':  int,
        'pressure':     int,
        'gps_state':    int,
        'gsm_sig_str':  float,
        'sat_num':      int,
        'net_provider': str,
        'network_type': str,
        'x_acc': float,
        'y_acc': float,
        'z_acc': float,
}

# Some elements in received packages can be divided in more data elements. For
# example 'time' field consist of hours, minutes, seconds and also microseconds.
# But MySQL can store only hours, minutes and seconds. So we need to create
# additional field for storing ms. This list contains those additional fields.
db_fields = [
        't_ms',
        'lat_pos',
        'lon_pos',
        'ses_id'
]
