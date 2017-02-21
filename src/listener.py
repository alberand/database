#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
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

        logging.info('Creating server. {}:{}'.format(
                config['host'], config['port']))
        try:
            self.server = Server(
                (config['host'], config['port']),
                RequestHandler
            )
        except socket.error as e:
            logging.info('Error while creating server. {}'.format(e))
            sys.exit(2)
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
        if not self.database.connect():
            logging.error('Fail to connect to database. Exit.')
            self.stop()
            sys.exit(3)

        # Start processing loop
        try:
            logging.info('Running loop for receiving data from TCP-server.')

            while self.running:
                # Package received
                if not self.queue.empty():
                    pkg = self.queue.get()
                    
                    if pkg['type'] == 'E':
                        # Save package to file
                        self.save_pkg(pkg)
                    else:
                        if pkg['type'] == 'I':
                            self.create_new_session(pkg)

                        if self.assign_session_id(pkg):
                            # Data or message package
                            self.process_pkg(pkg)
                        else:
                            pkg['type'] = 'E'

                        # Save package to file
                        self.save_pkg(pkg)

                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop()

    def create_new_session(self, pkg):
        # Generate new session id
        session_id = get_session_id(int(pkg['device_id']))
        logging.info('Creating new session. New session id is {}.'.format(
            session_id))
        # Create session
        self.database.insert(['ses_id'], 
                {'ses_id': session_id}, 'sessions')
        # Update session for the current device. If doesn't
        # exists create.
        logging.info('Update session for the current device.' + \
                'If doesn\'t exists create.')
        self.database.update('connections', 
                ['ses_id', 'device_id'],
                {
                    'ses_id': session_id, 
                    'device_id': pkg['device_id']
                },
                'ses_id="{}"'.format(session_id)
        )

    def assign_session_id(self, pkg):
        '''
        Assign current session id to the package. Session id is selected from
        database. For every device id (first elemen of the package) attach
        current session id.
        Args:
            pkg: dict. Package.
        Returns:
            Package (dict) or None.
        '''
        if not pkg:
            return False
        ses_id = self.database.select(
                'connections', ['ses_id'], 
                {'device_id': pkg['device_id']}
        )

        if len(ses_id):
            pkg['ses_id'] = ses_id[0][0]
            return True

        return False

    def process_pkg(self, pkg):
        '''
        Save package to file and to database.
        Args:
            pkg: dict, with parsed data
        '''

        # Load package data to database
        if pkg['type'] == 'D':
            # There we need to change package structure a little bit.
            if not self.database.insert(expand_pkg_struct(), 
                    data_for_db(pkg), 'packages'):
                logging.info('Fail to load package to database.')
        elif pkg['type'] == 'T':
            if not self.database.insert(msg_structure, pkg, 'messages'):
                logging.info('Fail to load package to database.')
        elif pkg['type'] == 'I':
            pass
        else:
            logging.info('Unkonwn type of the packages. Skipping. Package '
                    'already saved.')


    def save_pkg(self, pkg):
        '''
        Saves package to session file.
        Args:
            pkg: dict, with parsed data
        '''
        if pkg['type'] == 'E':
            filename = config['corrupted_storage']
        else:
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

        sys.exit(0)

