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
        except mysql.connector.Error as err:
            # Handle some errors
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logger.error('Something is wrong with your user name'
                             ' or password')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logger.error("Database does not exist")
            else:
                logger.error(err)

    def insert(self, struct, data, table='packages'):
        '''
        Inserting data sample to table.
        Args:
            struct: list with data fields in database
            data: dictionary with parsed data
            table: string with name of the table where to insert data
        '''
        # Generate quiery from data. For now table is static. But table should
        # be choosen based on data.
        query = QUERIES['insert'].format(
            table, ', '.join(struct), 
            ', '.join(['"{}"'.format(data[item]) for item in struct])
        )

        try:
            self.cursor.execute(query)
            self.cnx.commit()
        except mysql.connector.Error as e:
            logging.info(e)
            self.cnx.rollback()

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
            self.cnx.rollback()

    def close(self):
        '''
        Close database.
        '''
        logger.info("Closing database.")
        # Don't know maybe there also can be error =)
        try:
            self.cnx.close()
        except mysql.connector.Error as e:
            logging.error('Error while closing database. \n{}'.format(e))
