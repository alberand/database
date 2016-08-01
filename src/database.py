#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import MySQLdb

from config import config

logger = logging.getLogger(__name__)

class Database:

    def __init__(self):
        self.db = None
        self.cursor = None

    def connect(self):
        '''
        Set up connection with database. All conenction parameters can be
        changed in configuration file 'config.py'.
        '''
        self.db = MySQLdb.connect(
                config['mysql_host'], config['mysql_user'], 
                config['mysql_pass'], config['loggers'])
        self.cursor = self.db.cursor()

    # def create_table(self, params):
        # query = 'CREATE TABLE {name}'.format(
                # name=params['name']         
        # )
        # self.cursor.excute(query)


    def send_query(self, query):
        '''
        Send query to database. If query empty or None returns None otherwise
        return result of query.
        '''
        result = None

        if query:
            result = self.cursor.execute(query)
        else:
            logger.info('Empty query. Do nothing.')

        return result

    def close(self):
        '''
        Close database.
        '''
        self.db.close()
