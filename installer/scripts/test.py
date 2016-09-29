#!/usr/bin/env python
# -*- coding: utf-8 -*-

#==============================================================================
# This script fill up database and send some testing packages to server. It is
# made for demonstration that everything work.
#==============================================================================

import time
import socket
import random
import threading
from random import randint


import mysql.connector

print('='*80)
print('This script fill up database and send some testing packages to server. '
      'It is made for demonstration that everything work.')
print('='*80)

def get_session_id(key):
    random.seed(int(key))

    return random.randint(10000, 99999)

config = {
    'mysql_db': 'loggersdb',
    'mysql_host': 'localhost',
    'mysql_user': 'cast',
    'mysql_pass': 'castpass',
    'server_ip': '127.0.0.1',
    'server_port': 5000,
}

sessions = [get_session_id(i) for i in range(5)]

test_list = "@02;30.07.16;17:57:51.9;5007.84212N;01425.10981E;{};340.9;{};286;97849;;;;;;;;1;{}#"


class Device(threading.Thread):
    '''
    Class for emitating client instance. Just send some data to server.
    '''
    def __init__(self, ip, port, session):
        threading.Thread.__init__(self)
        self.running = True
        self.ip = ip
        self.port = port
        self.session = session

    def run(self):
        i = 0
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.ip, self.port))
            while i < 20:
                random.seed()
                sock.sendall(
                    bytes(
                        test_list.format(
                            int(self.session),
                            float(i)/randint(1, 10),
                            i), 
                        'ascii')
                )
                i += 1
                # time.sleep(1)

    def stop(self):
        self.running = False

if __name__ == '__main__':
    # Insert sessions into database
    cnx = mysql.connector.connect(
            host=config['mysql_host'], 
            user=config['mysql_user'], 
            password=config['mysql_pass'],
            database=config['mysql_db'])
    cursor = cnx.cursor()

    for session in sessions:
        pass
        # cursor.execute('INSERT INTO sessions (ses_id) VALUES'
                # ' ({})'.format(session))

    # cnx.commit()
    cnx.close()

    ip, port = config['server_ip'], config['server_port']
    a = Device(ip, port, 0)
    b = Device(ip, port, 1)
    c = Device(ip, port, 2)
    d = Device(ip, port, 3)
    e = Device(ip, port, 4)

    a.start()
    b.start()
    c.start()
    d.start()
    e.start()

    a.join()
    b.join()
    c.join()
    d.join()
    e.join()

