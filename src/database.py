#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import mysql.connector

from config import config, pkg_structure, db_fields
from sql.queries import QUERIES

logger = logging.getLogger(__name__)

class Database:

    def __init__(self):
        self.cnx = None
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
            logger.info("Successful connection to database.")
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
        self.cursor = self.cnx.cursor()

    def insert(self, struct, data):
        '''
        Inserting data sample to table.
        Args:
            struct: data fields in database
            data: dictionary with parsed data
        '''
        # Generate quiery from data. For now table is static. But table should
        # be choosen based on data.
        query = QUERIES['insert'].format(
            'logger', ', '.join(struct), 
            ', '.join(['%({})s'.format(item) for item in struct])
        )

        try:
            self.cursor.execute(query, data)
            self.cnx.commit()
        except Exception as e:
            logging.info(e)
            self.cnx.rollback()


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
        logger.info("Closing database.")
        self.cnx.close()
