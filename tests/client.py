#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import socket
import logging
import threading

logger = logging.getLogger(__name__)

class Client(threading.Thread):
    '''
    Class for emitating client instance. Just send some data to server.
    '''
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.running = True
        self.ip = ip
        self.port = port

        self.sock = None

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.ip, self.port))
            self.sock = sock
            while self.running:
                time.sleep(1)

    def send(self, data):
        self.sock.sendall(bytes(data, 'ascii'))

    def stop(self):
        self.running = False
