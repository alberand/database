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
        self.request.setblocking(True)

    def handle(self):
        logging.info('Client with address {} connected.'.format(
            self.client_address))

        try:
            while True:
                data = parse(self.read_package())
                if data:
                    self.server.queue.put(data)
                else:
                    break

            logging.info('Handler for client {} end working.'.format(
                self.client_address))

        except socket.error:
            logging.info('Connection dropped.')

    def read_package(self):
        '''
        Reads package enditing by config['pkg_end'] symbol.
        Returns:
            String, ended by 'pkg_end'.
        '''
        string = ''
        symbol = ''

        # Don't know why but if I put this construction only in cycle loop
        # continue executing forever. Like if socket was is non-blocking state.
        # byte = self.request.recv(1, socket.MSG_WAITALL) 

        while symbol != config['pkg_end']:
            byte = self.request.recv(1, socket.MSG_WAITALL) 
            symbol = str(byte, self.coding)
            string = string + symbol
            time.sleep(0.001)

        logging.info('Sending string: {}'.format(string))

        return string

