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
        self.timeout = 3
        self.request.setblocking(True)
        self.request.settimeout(3)

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

        except socket.error as e:
            logging.info('Connection dropped. Error: {}'.format(e))

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
        byte = self.request.recv(1, socket.MSG_WAITALL) 
        if byte:
            symbol = str(byte, self.coding)
            string = string + symbol

        while byte and symbol != config['pkg_end']:
            byte = self.request.recv(1) 
            if not byte:
                break

            symbol = str(byte, self.coding)
            string = string + symbol

        logging.debug('Received string: {}'.format(string))

        return string

