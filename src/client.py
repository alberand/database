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
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.running = True
        self.ip = ip
        self.port = port

    def run(self):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.ip, self.port))

            i = 0
            while self.running:
                sock.sendall(
                        bytes('#{} from thread {}'.format(
                            i, self.name), 'utf-8'))
                # print(sock.recv(1024))
                i += 1
                time.sleep(1)

            sock.sendall(bytes('quit', 'utf-8'))

    def stop(self):
        self.running = False

if __name__ == '__main__':
    ip, port = '127.0.0.1', 5000
    a = Device(ip, port)
    b = Device(ip, port)
    c = Device(ip, port)

    a.start()
    b.start()
    c.start()

    time.sleep(5)

    a.stop()
    b.stop()
    c.stop()

