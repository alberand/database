#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import socket
import logging
import threading

from client import Device
from packages import sessions_list

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    # Configure test properties
    ip, port = '127.0.0.1', 5000
    # Order: normal, bad, miss, multiple
    _set = sessions_list[0]
    # Clients number should be > 0
    clients_number = 1

    # Test section
    clients_list = list()
    for i in range(clients_number):
        client = Device(ip, port, _set)

        client.start()
        clients_list.apeend(client)

    # Waiting for all clients to finish
    for client in clients_list:
        client.join()
