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
        self.setup()

        # Start processing loop
        try:
            logging.info('Waiting for clients...')

            counter = 0
            while self.running:
                # Package received
                pkg = self.queue.get(True)

                self.process_pkg(pkg)

                # Commit to database every 10 packages or if queue is empty
                if counter == config['to_commit_pkg_count'] or self.queue.qsize() == 0:
                    self.database.commit()
                    counter = 0

                counter += 1

        except KeyboardInterrupt:
            self.stop()

    def setup(self):
        '''
        Run TCP-server connects to database.
        Exceptions:
            Exit with code 2 if failed to create TCP-server
            Exit with code 3 if failed to connect to database
        '''
        logging.info('Creating server. {}:{}'.format(
                config['host'], config['port']))
        try:
            self.server = Server(
                (config['host'], config['port']),
                RequestHandler
            )
        except socket.error as e:
            logging.error('Error while creating server. {}'.format(e))
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
        logging.info('Connecting to database...')
        if not self.database.connect():
            logging.error('Fail to connect to database. Exit.')
            self.stop()
            sys.exit(3)

    def process_pkg(self, pkg):
        # Packages preprocessing
        if pkg['type'] == 'E':
            # Save package to file
            self.save_pkg(pkg)
        else:
            if pkg['type'] == 'I':
                self.create_new_session(pkg)

            if self.assign_session_id(pkg):
                # Data or message package
                self.insert_to_db(pkg)
            else:
                pkg['type'] = 'E'

            # Save package to file
            self.save_pkg(pkg)


    def create_new_session(self, pkg):
        # Generate new session id
        session_id = get_session_id(int(pkg['device_id']))
        logging.info('Creating new session. New session id is "{}".'.format(
            session_id))
        # Create session
        self.database.insert(['ses_id'], 
                [(session_id,), ], 'sessions')
        # Update session for the current device. If doesn't
        # exists create.
        logging.info('Update/Create session for the current device.')
        self.database.update('connections', 
                ['ses_id', 'device_id'],
                {
                    'ses_id': session_id, 
                    'device_id': pkg['device_id']
                },
                'ses_id="{}"'.format(session_id)
        )
        self.database.commit()

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
        else:
            logging.debug('Fail to find session assigned to device id {} .'.format(
                pkg['device_id']))

        return False

    def insert_to_db(self, pkg):
        '''
        Load package to database.
        Args:
            pkg: dict, with parsed data
        '''
        # Load package data to database
        if pkg['type'] == 'D':
            # There is need to change package structure
            if not self.database.insert(expand_pkg_struct(), 
                    [data_for_db(pkg, expand_pkg_struct())], 'packages'):
                logging.info('Fail to load package to database.')
        elif pkg['type'] == 'T':
            msg_s = msg_structure + ['ses_id']
            if not self.database.insert(msg_s, 
                    [[pkg[item] for item in msg_s],], 'messages'):
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
            filename = '{}/{}'.format(config['data_storage'], 
                                      config['corrupted_storage'])
        else:
            filename = '{}/{}.txt'.format(config['data_storage'], pkg['ses_id'])

        # Create server's data directory if doesn't exist
        try:
            if not os.path.exists(config['data_storage']):
                os.makedirs(config['data_storage'], 0o755)
        except OSError as exp:
            logging.error(('Fail to create data storage directory. Exception:'
                           '{}').format(exp))

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
