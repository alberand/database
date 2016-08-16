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
        self.buf = ''
        self.coding = 'utf-8'

    def handle(self):
        logging.info('Client with address {} connected.'.format(
            self.client_address))

        try:
            data = self.recv_package()

            while data:
                if data:
                    self.server.queue.put(data)
                data = self.recv_package()

            logging.info('Handler exiting.')
        except socket.error:
            logging.info('Connection dropped.')

    def recv_package(self):
        '''
        '''
        data = None

        data = self.read_package()
        data = parse(data)

        return data

    def read_package(self):
        '''
        Read package with starting symbol 'start_sym' until 'end_sym'.
        'start_sym' is just added to the start of a string.
        Args:
            start_sym: string, symbol
            end_sym: string, one symbol
        Returns:
            String, ended by 'end_sym'.
        '''
        string = ''
        symbol = ''

        while symbol != config['pkg_end']:
            symbol = str(self.request.recv(1), self.coding)
            string = string + symbol
            time.sleep(0.01)

        return string

