#!/usr/bin/env python
# -*- coding: utf-8 -*-

#==============================================================================
# Script for initialization database.
#==============================================================================

import mysql.connector
from mysql.connector import errorcode

from config import config
from sql.tables import TABLES

def create_database(cursor):
    '''
    Create database if it doesn't exist.
    Args:
        cursor: mysql cursor
    '''
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except MySQLdb.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

if __name__ == '__main__':
    print('{0:=^80}'.format(''))
    print('{0: ^80}'.format('Inital script.'))
    print('{0:=^80}'.format(''))
    # Get database name
    DB_NAME = config['mysql_db']
    print(
    'This script try connect to database, in case database doesn\'t exist '
    'create new one. Then script create tables with predefined structure. '
    'This script is need to be used once before starting socket application. '
    'If tables already exist script skip them and continue. If tables are need'
    'to be changed you should change them by hands because this script can\'t '
    'change existing database or tables.')
    print('{0: ^80}'.format(''))
    print('Used database name:  {}'.format(DB_NAME))
    print('Used name:           {}'.format(config['mysql_user']))
    print('Used password:       {}'.format(config['mysql_pass']))
    print('{0:=^80}'.format(''))

    # Open connection to MySQL server and get cursor
    cnx = mysql.connector.connect(
            host=config['mysql_host'], 
            user=config['mysql_user'], 
            password=config['mysql_pass'])
    cursor = cnx.cursor()

    # Try to connect to database. If doesn't exist create one.
    try:
        cnx.database = DB_NAME    
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)

    # Create tables described in TABLES dictonary
    for name, ddl in TABLES.items():
        try:
            print("Creating table '{}': ".format(name), end='')
            cursor.execute(ddl)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    # Close connection and database
    cursor.close()
    cnx.close()

    print('{0:=^80}'.format(''))
