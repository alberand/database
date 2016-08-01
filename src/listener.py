#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import socket
import logging
import threading

from server import Server
from handler import RequestHandler
from config import config

logger = logging.getLogger(__name__)

class Listener(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        self.running = True

    def start(self):
        '''
        Run main loop for this thread
        '''

        self.server = Server(
                (config['host'], config['port']),
                RequestHandler
        )
        ip, port = self.server.server_address

        logging.info('Server loop running in thread: {}'.format(self.name))
        logging.info('IP: {}, Port: {}'.format(ip, port))

        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        try:
            while self.running:
                # logging.info('Listener running...')
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        '''
        Stop main loop in this thread.
        '''
        self.server.shutdown()
        self.server.server_close()

