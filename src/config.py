#!/bin/python

import os
import json
import sys
from datetime import datetime

config_dir = os.path.dirname(os.path.abspath(__file__))

if len(sys.argv) < 2:
    logging.error('Please specify config name.')
    sys.exit(1)
else:
    config_name = sys.argv[1]

config = json.load(open(os.path.join(config_dir, config_name), 'r'))

# This list define package structure. Thus, in which order data are arranged.
# Empty fields doesn't appear in data structure. They are just skipped, also as
# non defined fields.
pkg_structure = [
        # 'ses_time',
        'date',
        'time',
        'latitude',
        'longitude',
        # 'course',
        # 'gps_altitude',
        # 'speed',
        # 'temperature',
        # 'pressure',
        # 'gps_state',
        # 'sat_num'
]

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
        'time_ms_out': lambda time: 
                                datetime.strptime(time, '%H:%M:%S').time(),
        'latitude':     lambda data: [float(data[:-1]), str(data[-1])],
        'longitude':    lambda data: [float(data[:-1]), str(data[-1])],
        'course':       float,
        'gps_altitude': float,
        'speed':        float,
        'temperature':  int,
        'pressure':     int,
        'gps_state':    int,
        'sat_num':      int
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
