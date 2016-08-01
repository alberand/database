#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import socket
import threading
import socketserver

# log_filename = 'handlers_log.log'
# logging.basicConfig(filename=log_filename, level=logging.DEBUG)

class RequestHandler(socketserver.BaseRequestHandler):
    '''
    This class is used to proceed requests by clients. In this case its receive
    data and sends it further to parsing and saving to database.
    '''
    logging.info('Request Handler creadted.')

    def handle(self):
        data = str(self.request.recv(1024), 'utf-8')
        while data != 'quit':
            c_thread = threading.current_thread()

            logging.info('{}: {}'.format(c_thread.name, data))
            # self.request.sendall(bytes('asdg;jaklsdjf', 'utf-8'))

            data = str(self.request.recv(1024), 'utf-8')

