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
    ip, port = '147.32.196.177', 5000
    # Order: normal, bad, miss, multiple
    # _set = sessions_list[0]
    _set = load_session_from_file('data_4.txt')
    # Clients number should be > 0
    clients_number = 1

    # Test section
    clients_list = list()
    for i in range(clients_number):
        client = Device(ip, port, _set)

        client.start()
        clients_list.append(client)

    # Waiting for all clients to finish
    for client in clients_list:
        client.join()
