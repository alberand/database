#!/usr/bin/env python
# -*- coding: utf-8 -*-

#==============================================================================
# Script for clearing or dropping tables in database.
#==============================================================================

import sys

import mysql.connector
from mysql.connector import errorcode

from config import config

if __name__ == '__main__':
    print('{0:=^80}'.format(''))
    print('{0: ^80}'.format('Clear script.'))
    print('{0:=^80}'.format(''))
    # Get database name
    DB_NAME = config['mysql_db']
    print('This script clear tables or drop tables if you specify \'drop\''
          'argument. Packages are cleared/dropped in the next order: packages,'
          ' messages, sessions.')
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

    cnx.database = DB_NAME    

    # Create tables described in TABLES dictonary
    queries_cl = {
            'packages': 'DELETE FROM packages;', 
            'messages': 'DELETE FROM messages;', 
            'sessions': 'DELETE FROM sessions;',
    }

    queries_dp = {
            'packages': 'DROP TABLE packages;', 
            'messages': 'DROP TABLE messages;', 
            'sessions': 'DROP TABLE sessions;',
    }

    for name in ['packages', 'messages', 'sessions']:
        try:
            if 'drop' not in sys.argv:
                print("Clearing table '{}': ".format(name), end='')
                cursor.execute(queries_cl[name])
            else:
                print("Dropping table '{}': ".format(name), end='')
                cursor.execute(queries_dp[name])
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")

    cnx.commit()
    # Close connection and database
    cursor.close()
    cnx.close()

    print('{0:=^80}'.format(''))
