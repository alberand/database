#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import mysql.connector

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
        try:
            self.cnx = mysql.connector.connect(
                host=config['mysql_host'], 
                user=config['mysql_user'], 
                password=config['mysql_pass'], 
                database=config['mysql_db'])
        except mysql.connector.Error as err:
            # Handle some errors
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logger.error('Something is wrong with your user name'
                             ' or password')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logger.error("Database does not exist")
            else:
                logger.error(err)

        # Get cursor (input point to database)
        self.curser = self.cnx.cursor()

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
