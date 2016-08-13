#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging
import socket
import threading
import socketserver

from parser import parse_data, parse_msg, parse_init
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
                self.server.queue.put(data)
                logging.info(data)

                data = self.recv_package()
        except socket.error:
            logging.info('Connection dropped.')

    def recv_package(self):
        '''
        '''
        data = None
        # Read first symbol
        start = str(self.request.recv(1), self.coding)
        
        if start == config['pkg_start']:
            # Data package
            data = self.read_package(start_sym=start, end_sym=config['pkg_end'])
            data = parse_data(data)
        elif start == config['txt_start']:
            # Text package
            data = self.read_package(start_sym=start, end_sym=config['txt_end'])
            data = parse_msg(data)
        elif start == config['ini_start']:
            # Initial package
            data = self.read_package(start_sym=start, end_sym=config['ini_end'])
            data = parse_init(data)
        else:
            logging.info('No package with this starting symbol: {}'.format(
                start))
            logging.error('Can\'t parse this string. Skipping. ' 
                        'String: \n\t{}'.format(data))
            return start

        return data

    def read_package(self, start_sym, end_sym):
        '''
        Read package with starting symbol 'start_sym' until 'end_sym'.
        'start_sym' is just added to the start of a string.
        Args:
            start_sym: string, symbol
            end_sym: string, one symbol
        Returns:
            String, ended by 'end_sym'.
        '''
        string = symbol = start_sym

        while symbol != str(end_sym, self.coding):
            symbol = str(self.request.recv(1), self.coding)
            string = string + symbol

        return string

