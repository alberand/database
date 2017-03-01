#!/usr/bin/env python
# -*- coding: utf-8 -*-

#==============================================================================
# Script for creating MySQL user
#==============================================================================

import os
import sys
import mysql.connector
from mysql.connector import errorcode

sys.path.insert(1, '../src')

from config import config
from sql.tables import TABLES

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('There is not enough arguments.')
        print('Use following arguments:')
        print('\tpython {} config.ini MYSQL_ROOT_PASSWORD'.format(
            os.path.basename(__file__)))
        sys.exit(1)

    # Open connection to MySQL server and get cursor
    cnx = mysql.connector.connect(
            host=config['mysql_host'], 
            user='root', 
            password=sys.argv[2])
    cursor = cnx.cursor()

    # Create MySql user
    command = '''
    CREATE USER '{}'@'{}' IDENTIFIED BY '{}';
    GRANT ALL PRIVILEGES ON *.* TO '{}'@'{}';
    FLUSH PRIVILEGES;
    '''.format(config['mysql_user'], config['mysql_host'], config['mysql_pass'],
            config['mysql_user'], config['mysql_host'])

    try:
        print("Creating user '{}' identified by {}: ".format(
            config['mysql_user'], config['mysql_pass']), end='')
        cursor.execute(command, multi=True)
    except mysql.connector.Error as err:
            print(err.msg)
    else:
        print("OK")

    cnx.commit()

    # Close connection and database
    cursor.close()
    cnx.close()
