#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

lvl_to_degree = [
    360.0,
    180.0,
    90.0,
    45.0,
    22.5,
    11.25,
    5.625,
    2.813,
    1.406,
    0.703,
    0.352,
    0.176,
    0.088,
    0.044,
    0.022,
    0.011,
    0.005,
    0.003,
    0.001,
    0.0005,
]

route_template = '''
{
  "type": "FeatureCollection",
  "crs": {
      "type": "name",
      "properties": {
          "name": "EPSG:4326"
      }
  },
  "features": [
    {
      "type": "route",
      "geometry": {
        "type": "LineString",
        "coordinates": []
      }
    }
  ]
}
'''

def NMEA_to_dd(coord, is_long=False):
    '''
    Converts NMEA representation of coordinate to decimal degree form. 
    TODO: For now doesn't support E/W, S/N
    Args:
        coord: string or float number describing coordinate in NMEA form
    Returns:
        Float number representing coordinate.
    '''
    coord = str(coord)

    num = coord.split('.')
    if len(num[0]) < 5:
        num[0] = '{0:0>5}'.format(num[0])

    int_length = 3 if is_long else 2
    # Last two numbers are minutes, but first 1 - 3 are degree
    int_part = num[0][0:len(num[0]) - int_length]
    dd = float(int_part) + \
        float(num[0][len(num[0]) - int_length:] + '.' + num[1])/60.0

    return dd


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
        result.append(NMEA_to_dd(coord))

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

def find_coords_center(packages):
    if not packages:
        return json.dumps([0.0, 0.0])

    # Latitude id in the list.
    max_lat = max([pkg['latitude'] for pkg in packages])
    min_lat = min([pkg['latitude'] for pkg in packages])
    # Longitude id in the list.
    max_lon = max([pkg['longitude'] for pkg in packages])
    min_lon = min([pkg['longitude'] for pkg in packages])

    return json.dumps(NMEA_to_ll(min_lon + (max_lon - min_lon)/2, 
            min_lat + (max_lat - min_lat)/2))

def find_bounds(packages):
    '''
    Function for finding coordinates bounds for all points contained in
    list.
    Args:
        pkg_list: list of packages with points. See self.get_packages.
    Returns:
        List with two lists first one is latitude range [min, max] and
        second one longitude range [min, max].
    '''
    if not packages:
        return json.dumps([[-90.0, 90.0], [-180.0, 180.0]])
    # Latitude id in the list.
    max_lat = NMEA_to_dd(max([pkg['latitude'] for pkg in packages]))
    min_lat = NMEA_to_dd(min([pkg['latitude'] for pkg in packages]))
    # Longitude id in the list.
    max_lon = NMEA_to_dd(max([pkg['longitude'] for pkg in packages]))
    min_lon = NMEA_to_dd(min([pkg['longitude'] for pkg in packages]))

    return json.dumps([[min_lon, max_lon], [min_lat, max_lat]])

def json_route(packages):
    '''
    Generate GEOjson structure for displaying on map. Adds coordinates from
    every package to json structure.
    Args:
        pkg_list: list of packages with coordinates.
    Returns:
        String which represents json structure.
    '''
    data_set = json.loads(route_template)

    for pkg in packages:
        data_set = add_coords_to_json(data_set, 
                NMEA_to_ll(float(pkg['longitude']), float(pkg['latitude'])))

    replace_table = {ord('\''): '"', ord('"'): '\''}

    return str(data_set).replace('\'', '"') 

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

    print('='*80)
    print('{0:=^80}'.format('Test zeros coordinates.'))
    print('='*80)
    print('Initial coordinates: {} {}'.format(0.1, 0.1))
    print('Calculated coordinates: {} {}'.format(
        *NMEA_to_ll(0.1, 0.1)))

    print(NMEA_to_ll(4981.15186, 1553.55322))

