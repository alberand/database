#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging
import socket
import threading
import socketserver

from parser import parse
from config import config

# log_filename = 'handlers_log.log'
# logging.basicConfig(filename=log_filename, level=logging.DEBUG)

class RequestHandler(socketserver.BaseRequestHandler):
    '''
    This class is used to proceed requests by clients. In this case its receive
    data and sends it further to parsing and saving to database.
    '''

    def setup(self):
        # String buffer for receiving symbols
        self.coding = 'utf-8'
        self.timeout = 3
        self.request.setblocking(True)
        self.request.settimeout(3)

    def handle(self):
        logging.info('Client with address {} connected.'.format(
            self.client_address))

        try:
            while True:
                byte = self.request.recv(1) 
                if byte:
                    char = str(byte, self.coding)

                self.server.queue.put(char)

            logging.info('Handler for client {} end working.'.format(
                self.client_address))

        except socket.error as e:
            logging.info('Connection dropped. Error: {}'.format(e))
