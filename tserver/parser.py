#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import pprint
import logging

from utils import get_session_id
from config import pkg_structure, msg_structure, handlers, config

def is_valid_package(string):
    '''
    Check if it is valid package. Control if it's have starting and ending
    symbols.
    Args:
        string: string to check
    Returns:
        True is it is false otherwise.
    '''
    if string[0] != config['pkg_start'] or string[-1] != config['pkg_end']:
        return False
    return True

def parse(string):
    """
    This function receive raw string (package) in next format: 
        @ses_id;pkg_type;date;time;;...;;;#
    Parse this string and depending on package type call next function to parse
    left data fields.
    Args:
        string: String @;;;#
    Returns:
        Dictionary with parsed data and three fields named ses_id, type(package
        type), original (original string)
    """
    if not string:
        return None

    # Add original string to dict. Later it will be used to it to file.
    package = {
            'ses_id':   0,
            'type':     'E',
            'original': string.rstrip()
    }

    # Check if receive complete string
    if not is_valid_package(string):
        logging.error('Sorry, string is not complete. String: {}'.format(string))
        return package
    
    # Get rid of package characters and split data into list
    raw_data = string[1:-1].split(config['pkg_delimeter'])
    # Remove empty positions
    data_list = [i if i else 'x' for i in raw_data]

    # Setup some specific fields. This fields are common for all packages.
    try:
        package['device_id'] = int(data_list.pop(0))
        package['type'] = str(data_list.pop(0))
    except:
        # This is case if package really bad and hasn't some basic fields.
        logging.info('Fail to parse primary fields. Package is wrong.')
        return package

    # Based on package type choose next parser.
    if package['type'] == 'I':
        package['version'] = data_list.pop(0).split(':')[1]
    elif package['type'] == 'T':
        package.update(parse_data(data_list, msg_structure))
    elif package['type'] == 'D':
        package.update(parse_data(data_list, pkg_structure))
    else:
        logging.info('Unknown package type. Just save it to file.')

    return package

def parse_data(data_list, struct):
    '''
    This function receive string which represent data package sent by logger.
    Then this string is parsed into separate elements. Those data are added 
    to resulting dictionary.
    Args:
        str: package string in the next format: @;;;...;;;;#
    Returns:
        Dictionary with names and converted data.
    '''
    # Parse and convert data
    result = dict()

    for i, name in enumerate(struct):
        try:
            if data_list[i] != 'x':
                result[name] = handlers[name](data_list[i])
            else:
                result[name] = 'NULL'

        except ValueError:
            # We don't want to loose data in any case so we save it to file
            logging.error('There is wrong data or handler. The sample skipped.'
                          ' Item = {}, name of handler = {}'.format(
                data_list[i], name))
            result[name] = 'NULL'
        except TypeError:
            logging.error('Can\'t parse string. Possibly there is problem with '
                         ' some handler. Handler should be callable function.')
            result[name] = 'NULL'
        except IndexError:
            logging.error('There is IndexError, possibly package contains wrong'
                         ' number of field.')
            result[name] = 'NULL'

    return result

if __name__ == '__main__':
    test_list = [
        '@10;T;Var. init.;SW:PaPa,0.2;HW:s12,SIM5320e,bastl#',
        '@10;T;Reset#',
        # '@010;T;00:00:05;Init wait done.#',
        # '@010;T;00:00:05;Modem init done.#',
        # '@010;D;13.08.16;10:24:49.0;5004.340927N;01432.673110E;6.2;323.4;298.61;8;1;319;99479#',
        # '@010;D;x;x;x;x;x;x;x;x;x;320;99486#',
        # '@010;D;x;x;x;x;x;x;x;x;x;320;99473#',
        # '@010;D;x;#',
        # '@010;D;13.08.16;10:24:49.0;5004.340927N;01432.673110E;6.2;323.4;298.61;8;1;319;99479#',
        # '@010;D;13.08.16;10:24:53.0;5004.349060N;01432.666529E;9.1;336.7;299.41;8;1;-1;-1#',
        #'@010;D;13.08.16;10:24:53.0;5004.349060N;01432.666529E;9.1;336.7;299.41;8;1;3.4;;3G;1.0;2.0;3.0#',
        '@20;D;29.12.16;09:09:26.5;4948.93380N;1531.25368E;0.0;345.4;356.4;;;32;O2- CZ;4G;15;-16;-996#',
        # '@010;T;00:00:15;GSM Process error.#',
        # '@asdfasdfasdfasdfadsf#'
    ]

    for line in test_list:
        pprint.pprint(parse(line))
