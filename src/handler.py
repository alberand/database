#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

    def handle(self):
        logging.info('Client with address {} connected.'.format(
            self.client_address))

        data = self.read_package()

        # while data:

        parsed_data = parse(data)
        if parsed_data:
            self.server.queue.put(parsed_data)
        else:
            logging.error('Can\'t parse this string. Skipping. ' 
                          'String: \n\t{}'.format(data))

            # data = str(self.request.recv(1024), 'utf-8')

    def read_package(self):
        '''

        '''
        string = ''
        symbol = ''

        while symbol != config['pkg_end']:
            symbol = str(self.request.recv(1), 'utf-8')
            string = string + symbol

        return string

