#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import socket
import logging
import threading

logger = logging.getLogger(__name__)

class Device(threading.Thread):
    '''
    Class for emitating client instance. Just send some data to server.
    '''
    def __init__(self, ip, port, pkg_list):
        threading.Thread.__init__(self)
        self.running = True
        self.ip = ip
        self.port = port
        self.pkt_list = pkg_list

    def run(self):
        i = 0
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.ip, self.port))
            while i < len(self.pkt_list):
                sock.sendall(bytes(self.pkt_list[i], 'ascii'))
                i += 1

    def stop(self):
        self.running = False

if __name__ == '__main__':
    ip, port = '147.32.196.177', 5000
    # ip, port = '127.0.0.1', 5001
    a = Device(ip, port, False)
    # b = Device(ip, port, True)
    # c = Device(ip, port)

    a.start()
    # b.start()
    # c.start()

    # time.sleep(5)

    a.join()
    # b.join()
    # c.stop()

