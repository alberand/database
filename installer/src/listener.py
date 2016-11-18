#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import socket
import logging
import datetime
import threading
from queue import Queue
import mysql.connector

from server import Server
from handler import RequestHandler
from config import config, msg_structure
from utils import get_session_id
from database import Database
from dataprocessor import data_for_db, expand_pkg_struct

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
            logging.info('Running loop for receiving data from TCP-server.')

            while self.running:
                # Package received
                if not self.queue.empty():
                    pkg = self.queue.get()
                    
                    # if pkg['type'] == 'I':
                    if not self.is_session_created(pkg['ses_id']):
                        self.database.insert(
                                ['ses_id'], {'ses_id': pkg['ses_id']}, 
                                'sessions')

                    self.process_pkg(pkg)

                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop()

    def process_pkg(self, pkg):
        '''
        Save package to file and to database.
        Args:
            pkg: dict, with parsed data
        '''
        # Save package to file
        self.save_pkg(pkg)

        # Load package data to database
        if pkg['type'] == 'D':
            # There we need to change package structure a little bit.
            self.database.insert(expand_pkg_struct(), 
                    data_for_db(pkg), 'packages')
        elif pkg['type'] == 'T':
            self.database.insert(msg_structure, pkg, 'messages')
        else:
            logging.info('Unkonwn type of the packages. Skipping. Package '
                    'already saved.')


    def save_pkg(self, pkg):
        '''
        Saves package to session file.
        Args:
            pkg: dict, with parsed data
        '''
        filename = '{}/{}.txt'.format(config['data_storage'], pkg['ses_id'])

        # Create server's data directory if doesn't exist
        if not os.path.exists(config['data_storage']):
            os.makedirs(config['data_storage'])

        # Write package to file
        with open(filename, 'a+') as _file:
            _file.write(pkg['original'])
            _file.write('\n')

    def is_session_created(self, session):
        '''
        Check in database if session with this id already created or not.
        Args:
            session: string or integer
        Returns:
            True if created, otherwise False.
        '''
        status = self.database.select('sessions', ['ses_id'], 
                {'ses_id': session})

        return True if status else False

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

