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

            # Get cursor (input point to database)
            self.cursor = self.cnx.cursor()
            # Set session timeout as long as possible
            self.cursor.execute('SET GLOBAL wait_timeout=31536000')
            self.cnx.commit()
        except mysql.connector.Error as err:
            # Handle some errors
            if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                logger.error('Something is wrong with your user name'
                             ' or password')
                return False
            elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                logger.error("Database does not exist")
                return False
            else:
                logger.error(err)
                return False

        return True

    def insert(self, struct, data_set, table='packages'):
        '''
        Inserting data sample to table.
        Args:
            struct: list with data fields in database
            data_set: dictionary with parsed data
            table: string with name of the table where to insert data
        '''
        # Generate quiery from data. For now table is static. But table should
        # be choosen based on data.
        query = QUERIES['insert'].format(
            table, ', '.join(struct), 
            ', '.join(['%s' for item in struct])
        )

        # logging.error(query)
        # logging.error(data_set)

        try:
            self.cursor.executemany(query, data_set)
            return True
        except mysql.connector.Error as e:
            logging.info(e)
            logging.info('Query: {}.'.format(query))
            self.cnx.rollback()
            return False

    def select(self, table, fields, where):
        '''
        Selects 'fields' from 'table' where 'where'.
        Args:
            table: string, name of the table
            fields: list, name of the fields to return
            where: dict, where key is field name and value is value to 
                   determine which field to select
        '''
        # Generate conditions. For now only AND.
        conditions = ' AND '.join(
            ['{}={}'.format(key, value) for key, value in where.items()])

        # Generate query.
        query = QUERIES['select'].format(
                ', '.join(fields), table, conditions
        )

        try:
            self.cursor.execute(query)
            return [item for item in self.cursor]
        except mysql.connector.Error as e:
            logging.info(e)
            logging.info('Query: {}.'.format(query))
            self.cnx.rollback()
            return None

    def update(self, table, struct, fields, on_update):
        '''
        Update 'fields' from 'table' where 'where'. If item doesn't exist create
        it.
        Args:
            table: string, name of the table
            struct: list with columns names
            fields: dictionary where key is name of the field to update and
                value is a new value
            on_update: string. Used when element already exist in the database.
                See ON DUPLICATE KEY UPDATE.
        '''
        query = QUERIES['update'].format(
            table, 
            ', '.join(struct), 
            ', '.join(['"{}"'.format(fields[item]) for item in struct]),
            on_update
        )

        try:
            self.cursor.execute(query)
            return True
        except mysql.connector.Error as e:
            logging.info(e)
            logging.info('Query: {}.'.format(query))
            self.cnx.rollback()
            return False

    def commit(self):
        self.cnx.commit()

    def close(self):
        '''
        Close database.
        '''
        logger.info("Closing database.")
        # Don't know maybe there also can be error =)
        if self.cnx:
            try:
                self.cnx.close()
            except mysql.connector.Error as e:
                logging.error('Error while closing database. \n{}'.format(e))
