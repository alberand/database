#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

def NMEA_to_ll(lat, lon):
    '''
    Converts NMEA coordinates to decimal degree.
    Args:
        lat: float, latitude
        lon: float, longitude
    Returns:
        List with latitude and longitude.
    '''
    result = list()

    # Convert to strings
    lat, lon = (str(lat), str(lon))

    # Get degree
    for coord in (lat, lon):
        num = coord.split('.')
        # Last two numbers are minutes, but first 1 - 3 are degree
        int_part = num[0][0:len(num[0]) - 2]
        dd = float(int_part) + \
            float(num[0][len(num[0]) - 2:] + '.' + num[1])/60.0
        result.append(dd)

    return result 

def add_coords_to_json(json_str, coords):
    '''
    Add list of coordinates [lat, lon, alt] to prepared json structure.
    Args:
        json_str: json object.
        coords: list with three float numbers.
    Returns:
        Update json structure.
    '''
    json_str['features'][0]['geometry']['coordinates'].append(coords)

    return json_str


if __name__ == '__main__':
    from pprint import pprint

    print('='*80)
    print('{0:=^80}'.format('Test coords convertion from NMEA to dd formats.'))
    print('='*80)
    print('Initial coordinates: {} {}'.format(14.3924090, 50.0813583))
    print('Calculated coordinates: {} {}'.format(
        *NMEA_to_ll(1423.5445, 5004.8815)))

    print('='*80)
    print('{0:=^80}'.format('Test adding coords to data set.'))
    print('='*80)

    with open('./template.json', 'r') as _file:
        coords_set = json.loads(_file.read())

        updated_set = add_coords_to_json(coords_set, [123.0, 34.0, 42.0])

        pprint(updated_set['features'][0]['geometry']['coordinates'])

