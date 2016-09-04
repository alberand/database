#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

if __name__ == '__main__':
    print('Initial coordinates: {} {}'.format(14.3924090, 50.0813583))
    print('Calculated coordinates: {} {}'.format(
        *NMEA_to_ll(1423.5445, 5004.8815)))
