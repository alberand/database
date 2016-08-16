#!/bin/python

from datetime import datetime

config = {
        # MySQL information
        # Host is usually localhost, if database is running on another machine
        # it should be change to address of that machine.
        'mysql_host':   'localhost',
        # User name
        'mysql_user':   'cast',
        # Password
        'mysql_pass':   'castpass',
        # Name of the DATABASE (not a table)
        'mysql_db':  'loggersdb',

        # Socket parameters
        'host': 'localhost',
        'port': 5000,

        # Files storage. Without slash (/) on the end.
        'data_storage': './data',

        # Name of file where will be saved all corrupted packages (which can't
        # be parsed).
        'corrupted_storage': './data/corrupted_data.txt',

        # Package symbols
        'pkg_start':        '@',
        'pkg_delimeter':    ';',
        'pkg_end':          '#',
        # Text package
        'txt_start':        'T',
        'txt_end':          '\r',
        # Init package
        'ini_start':        'P',
        'ini_end':          '#'
}

# This list define package structure. Thus, in which order data are arranged.
# Empty fields doesn't appear in data structure. They are just skipped, also as
# non defined fields.
pkg_structure = [
        'date',
        'time',
        'latitude',
        'longitude',
        'course',
        'gps_altitude',
        'speed',
        'temperature',
        'pressure',
        'gps_state',
        'sat_num'
]

# Messages package structure
msg_structure = [
        'msg',
        'ses_id',
]

# Initial package structure
init_structure = [
        '',
]

# This dictionary define data handlers. There is no need to keep right order.
# Handler should be pointer (object) to callable function not result of calling
# this function.
handlers = {
        # Name  # Handler
        'module_id':    int,
        'date':         lambda date: 
                                datetime.strptime(date, '%d.%m.%y').date(),
        'time':         lambda time: 
                                datetime.strptime(time, '%H:%M:%S.%f').time(),
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
