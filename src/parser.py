#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pprint
import logging

from utils import get_session_id
from config import pkg_structure, handlers, config

logger = logging.getLogger(__name__)

def parse(string):
    """
    This function receive raw string (package) in next format: 
        @ses_id;ses_time;pkg_type;;;;...;;;#
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

    # Check if receive complete string
    if string[0] != config['pkg_start'] or string[-1] != config['pkg_end']:
        logger.error('Sorry, string is not complete. String: {}'.format(string))
        return None
    
    # Get rid of package characters and split data into list
    raw_data = string[1:-1].split(config['pkg_delimeter'])
    # Remove empty positions
    data_list = list(filter(None, raw_data))

    # Parse and convert data
    result = dict()

    # Setup some specific fields
    result['ses_id'] = get_session_id(int(data_list[0]))
    result['type'] = data_list[2]
    result['original'] = string.rstrip()

    # We already used this fields so we need to delte them
    data_list.pop(0) # Delete session id
    data_list.pop(1) # Delete package type

    # Based on package type choose next parser.
    if result['type'] == 'T':
        result.update(parse_msg(data_list))
    elif result['type'] == 'D':
        result.update(parse_data(data_list))
    else:
        result = None

    return result


def parse_msg(data_list):
    result = dict()

    result['ses_time'] = str(data_list[0])
    result['msg'] = str(';'.join(data_list[1:]))

    return result

def parse_data(data_list):
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

    for i, name in enumerate(pkg_structure):
        try:
            if data_list[i] != 'x':
                result[name] = handlers[name](data_list[i])
            else:
                result[name] = 'NULL'

        except ValueError:
            # We don't want to loose data in any case so we save it to file
            logging.error('There is wrong data or handler. The sample skipped.')
            with open(config['corrupted_storage'], 'a+') as corrupted_storage:
                corrupted_storage.write(string + '\n')

            return None
        except TypeError:
            logging.error('Can\'t parse string. Possibly there is problem with '
                         ' some handler. Handler should be callable function.')
            with open(config['corrupted_storage'], 'a+') as corrupted_storage:
                corrupted_storage.write(string + '\n')

            return None
        except IndexError:
            result[name] = 'NULL'
            logging.error('There is IndexError, possibly package contains wrong'
                         ' number of field.')

    return result

if __name__ == '__main__':
    test_list = [
        '@010;00:00:00;T;Var. init.;SW:PaPa,0.2;HW:s12,SIM5320e,bastl#',
        '@010;00:00:00;T;Reset#',
        '@010;00:00:05;T;Init wait done.#',
        '@010;00:00:05;T;Modem init done.#',
        '@010;00:00:10;D;x;x;x;x;x;x;x;x;x;320;99486#',
        '@010;00:00:15;D;x;x;x;x;x;x;x;x;x;320;99473#',
        '@010;00:00:20;D;13.08.16;10:24:49.0;5004.340927N;01432.673110E;6.2;323.4;298.61;8;1;319;99479#',
        '@010;00:00:25;D;13.08.16;10:24:53.0;5004.349060N;01432.666529E;9.1;336.7;299.41;8;1;-1;-1#',
        '@010;00:00:26;T;GSM Process error.#',
    ]

    for line in test_list:
        pprint.pprint(parse(line))
