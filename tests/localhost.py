#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import socket
import pprint
import logging
import threading

from client import Device
from packages import sessions_list

logger = logging.getLogger(__name__)

def load_session_from_file(filename):
    result = list()
    with open(filename, 'r') as _file:
        for line in _file.readlines():
            result.append(line.rstrip('\n'))

    return result

if __name__ == '__main__':
    # Configure test properties
    ip, port = '127.0.0.1', 5000
    # Order: normal, bad, miss, multiple
    _set = load_session_from_file('data_2.txt')
    # Clients number should be > 0
    clients_number = 1

    # pprint.pprint(_set)
    # sys.exit()

    # Test section
    clients_list = list()
    for i in range(clients_number):
        client = Device(ip, port, _set)

        client.start()
        clients_list.append(client)

    # Waiting for all clients to finish
    for client in clients_list:
        client.join()
