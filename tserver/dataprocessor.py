#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy

from .config import config, pkg_structure, db_fields

def expand_pkg_struct():
    '''
    Generate package structure with additional fields. Because we want 
    separate symbol in latitude and longitude we need to change 
    'pkg_structure.' Also because MySQL can't store microseconds we need to 
    use another column for this.
    We need to make copy of 'pkg_structure' because otherwise we will
    change global settings.
    Returns:
        List with additional fields on the end.
    '''
    return copy.copy(pkg_structure) + db_fields

def data_for_db(data, struct):
    '''
    Preapare data for inserting it to database. Because package structure is
    different than data saved in database we need to change dictionary with data
    before sending it to db.
    Args:
        data: dictionary with data
    '''
    if data['time'] != 'NULL':
        data['t_ms'] = data['time'].microsecond
    else:
        data['t_ms'] = 'NULL'

    if data['latitude'] != 'NULL':
        data['lat_pos'] = data['latitude'][1]
        data['latitude'] = data['latitude'][0]
    else:
        data['lat_pos'] = 'NULL'
        data['latitude'] = 'NULL'

    if data['longitude'] != 'NULL':
        data['lon_pos'] = data['longitude'][1]
        data['longitude'] = data['longitude'][0]
    else:
        data['lon_pos'] = 'NULL'
        data['longitude'] = 'NULL'

    result = (data[item] for item in struct)

    return result

