#!/usr/bin/env python
# -*- coding: utf-8 -*-

#==============================================================================
# Script for clearing or dropping tables in database.
#==============================================================================

import sys

import mysql.connector
from mysql.connector import errorcode

if __name__ == '__main__':
    # Parse arguments
    if len(sys.argv) < 4:
        print('Not enough arguments. Please specify arguments in the next '\
            'order: \n\tuser password database host')
        sys.exit(1)
    else:
        print(sys.argv)
        user        = sys.argv[1]
        password    = sys.argv[2]
        database    = sys.argv[3]
        host        = sys.argv[4]
        drop        = True if 'drop' in sys.argv else False

    print('{0:=^80}'.format(''))
    print('{0: ^80}'.format('Clear script.'))
    print('{0:=^80}'.format(''))
    # Get database name
    DB_NAME = database
    print('This script clear tables or drop tables if you specify \'drop\''
          'argument. Packages are cleared/dropped in the next order: packages,'
          ' messages, sessions.')
    print('{0: ^80}'.format(''))
    print('Used database name:  {}'.format(DB_NAME))
    print('Used name:           {}'.format(user))
    print('Used password:       {}'.format(password))
    print('{0:=^80}'.format(''))

    # Open connection to MySQL server and get cursor
    cnx = mysql.connector.connect(
            host=host, 
            user=user, 
            password=password)
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
            if not drop:
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
