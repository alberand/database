#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pprint
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# This list define package structure. Thus, in which order data are arranged.
# Empty fields doesn't appear in data structure. They are just skipped, also as
# non defined fields.
pkg_structure = [
        'module_id',
        'date',
        'time',
        'lattitude',
        'longitude',
        'course',
        'gps_altitude',
        'speed',
        'temperature',
        'pressure',
        'unknown_1',
        'unknown_2'
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
        'lattitude':    str,
        'longitude':    str,
        'course':       float,
        'gps_altitude': float,
        'speed':        float,
        'temperature':  int,
        'pressure':     int,
        'unknown_1':    int,
        'unknown_2':    int
}

def parse(string):
    '''
    This function receive string which represent data package sent by logger.
    Then this string is parased into separate elements. Those data are added 
    to resulting dictionary.
    Args:
        str: package string in the next format: @02;;;...;;;1;06#
    Returns:
        Dictionary with names and converted data.
    '''
    if not string:
        return None

    # Check if receive complete string
    if string[0] != '@' or string[-1] != '#':
        logger.error('Sorry, string is not complete. String: {}'.format(string))
        return None
    
    # Get rid of package characters and split data into list
    raw_data = string[1:-1].split(';')
    # Remove empty positions
    data_list = list(filter(None, raw_data))

    # Parse and convert data
    result = dict()
    for i, name in enumerate(pkg_structure):
        try:
            result[name] = handlers[name](data_list[i])
        except ValueError:
            logger.error('There is wrong data or handler. This sample skipped.')
            return None

    return result

if __name__ == '__main__':
    test_list = [
        "@02;30.07.16;17:55:37.9;5007.84276N;01425.11099E;0.0;338.8;0.0;280;97847;;;;;;;;1;06#",
        "@02;30.07.16;17:55:41.9;5007.84266N;01425.11084E;0.0;339.1;0.0;280;97849;;;;;;;;1;06#",
        "@02;30.07.16;17:55:46.9;5007.84262N;01425.11075E;0.0;339.3;0.0;280;97849;;;;;;;;1;06#",
        "@02;30.07.16;17:55:52.9;5007.84260N;01425.11066E;0.0;339.4;0.0;281;97851;;;;;;;;1;06#",
        "@02;30.07.16;17:55:56.9;5007.84259N;01425.11061E;0.0;339.5;0.0;281;97851;;;;;;;;1;06#",
        "@02;30.07.16;17:56:01.9;5007.84257N;01425.11057E;0.0;339.6;0.0;281;97850;;;;;;;;1;06#",
        "@02;30.07.16;17:56:06.9;5007.84253N;01425.11054E;0.0;339.6;0.0;281;97845;;;;;;;;1;06#",
        "@02;30.07.16;17:56:11.9;5007.84247N;01425.11052E;0.0;339.6;0.0;281;97850;;;;;;;;1;06#",
        "@02;30.07.16;17:56:16.9;5007.84241N;01425.11048E;0.0;339.7;0.0;282;97840;;;;;;;;1;06#",
        "@02;30.07.16;17:56:21.9;5007.84237N;01425.11044E;0.0;339.7;0.0;282;97846;;;;;;;;1;06#",
        "@02;30.07.16;17:56:26.9;5007.84232N;01425.11041E;0.0;339.7;0.0;282;97853;;;;;;;;1;06#",
        "@02;30.07.16;17:56:31.9;5007.84228N;01425.11038E;0.0;339.8;0.0;282;97849;;;;;;;;1;06#",
        "@02;30.07.16;17:56:36.9;5007.84227N;01425.11034E;0.0;339.9;0.0;282;97852;;;;;;;;1;06#",
        "@02;30.07.16;17:56:41.9;5007.84225N;01425.11030E;0.0;340.0;0.0;283;97850;;;;;;;;1;06#",
        "@02;30.07.16;17:56:46.9;5007.84223N;01425.11026E;0.0;340.1;0.0;283;97839;;;;;;;;1;06#",
        "@02;30.07.16;17:56:51.9;5007.84218N;01425.11021E;0.0;340.1;0.0;283;97845;;;;;;;;1;06#",
        "@02;30.07.16;17:56:56.9;5007.84218N;01425.11018E;0.0;340.2;0.0;283;97843;;;;;;;;1;07#",
        "@02;30.07.16;17:57:01.9;5007.84220N;01425.11014E;0.0;340.4;0.0;284;97847;;;;;;;;1;07#",
        "@02;30.07.16;17:57:06.9;5007.84223N;01425.11007E;0.0;340.5;0.0;284;97842;;;;;;;;1;07#",
        "@02;30.07.16;17:57:11.9;5007.84226N;01425.11002E;0.0;340.7;0.0;284;97852;;;;;;;;1;07#",
        "@02;30.07.16;17:57:16.9;5007.84228N;01425.10999E;0.0;340.7;0.0;284;97858;;;;;;;;1;07#",
        "@02;30.07.16;17:57:21.9;5007.84227N;01425.10997E;0.0;340.7;0.0;285;97846;;;;;;;;1;07#",
        "@02;30.07.16;17:57:26.9;5007.84224N;01425.10995E;0.0;340.8;0.0;285;97841;;;;;;;;1;07#",
        "@02;30.07.16;17:57:31.9;5007.84220N;01425.10994E;0.0;340.8;0.0;285;97856;;;;;;;;1;07#",
        "@02;30.07.16;17:57:36.9;5007.84216N;01425.10992E;0.0;340.8;0.0;285;97850;;;;;;;;1;07#",
        "@02;30.07.16;17:57:41.9;5007.84213N;01425.10989E;0.0;340.8;0.0;286;97851;;;;;;;;1;07#",
        "@02;30.07.16;17:57:46.9;5007.84212N;01425.10985E;0.0;340.9;0.0;286;97849;;;;;;;;1;07#",
        "@02;30.07.16;17:57:51.9;5007.84212N;01425.10981E;0.0;340.9;0.0;286;97849;;;;;;;;1;07#"
    ]

    for line in test_list:
        pprint.pprint(parse(line))
