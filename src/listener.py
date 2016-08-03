#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import socket
import logging
import threading
from queue import Queue

from server import Server
from handler import RequestHandler
from config import config
from database import Database

logger = logging.getLogger(__name__)

class Listener(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        self.queue = Queue()
        self.running = True
        self.database = Database()

    def start(self):
        '''
        Run main loop for this thread
        '''

        logging.info('Creating server.')
        self.server = Server(
                (config['host'], config['port']),
                RequestHandler
        )
        # Add queue for communication with handlers
        self.server.queue = self.queue

        # Get ip and port
        ip, port = self.server.server_address

        logging.info('Server loop running in thread: {}'.format(self.name))
        logging.info('IP: {}, Port: {}'.format(ip, port))

        # Start server thread
        logging.info('Run server daemon.')
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        # Connect to database
        logging.info('Connect to database.')
        self.database.connect()

        # Start processing loop
        try:
            logging.info('Run loop for receiving data from server.')
            while self.running:
                if not self.queue.empty():
                    sample = self.queue.get()

                    # logging.info(sample)
                    self.database.insert(sample)

                time.sleep(0.001)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        '''
        Stop main loop in this thread.
        '''
        logging.info('Stop.')
        # Stop socket server
        self.server.shutdown()
        self.server.server_close()
        # Close database connection
        self.database.close()

