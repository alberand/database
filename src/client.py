#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import socket
import logging
import threading

logger = logging.getLogger(__name__)

test_list = [
        # "@010;00:00:00;T;Var. init.;SW:PaPa,0.2;HW:s12,SIM5320e,bastl#",
        # "@010;00:00:00;T;Reset#",
        # "@010;00:00:05;T;Init wait done.#",
        # "@010;00:00:05;T;Modem init done.#",
        # "@010;00:00:10;D;x;x;x;x;x;x;x;x;x;320;99486#",
        # "@010;00:00:15;D;x;x;x;x;x;x;x;x;x;320;99473#",
        # "@010;00:00:20;D;13.08.16;10:24:49.0;5004.340927N;01432.673110E;6.2;323.4;298.61;8;1;319;99479#",
        # "@010;00:00:25;D;13.08.16;10:24:53.0;5004.349060N;01432.666529E;9.1;336.7;299.41;8;-1;-1#",
        # "@010;00:00:20;D;13.08.16;10:24:49.0;5004.340927N;01432.673110E;6.2;323.4;298.61;8;1;389;99479#",
        # "@010;00:00:20;D;13.08.16;10:24:49.0;5004.340927N;01432.673110E;6.2;323.4;298.61;8;1;388;99479#",
        # "@010;00:00:20;D;13.08.16;10:24:49.0;5004.340927N;01432.673110E;6.2;323.4;298.61;8;1;323;99479#",
        # "@010;00:00:20;D;13.08.16;10:24:49.0;5004.340927N;01432.673110E;6.2;323.4;298.61;8;1;333;99479#",
        # "@010;00:00:20;D;13.08.16;10:24:49.0;5004.340927N;01432.673110E;6.2;323.4;298.61;8;1;339;99479#",
        # "@010;00:00:20;D;13.08.16;10:24:49.0;5004.340927N;01432.673110E;6.2;323.4;298.61;8;1;349;99479#",
        # "@010;00:00:26;T;Some messages about device state.#",
        "@15.02.16;22:19:39.1;5006.061870N;01423.242035E;0.0;300.8;0#",
        "TestInfo@15.02.16;22:19:39.1;5006.061870N;01423.242035E;0.0;300.8;0#",
        "Info@15.02.16;22:19:39.1;5006.061870N;01423.242035E;0.0;300.8;0#",
        "@012;D;13.08.16;10:24:49.0;5004.340927N;01432.673110E;6.2;323.4;298.61;8;1;379;99479#",
        "@012;T;00:00:26;GSM Process error.#",
        "@012;D;13.08.16;10:24:49.0;;;N;01432.673110E;6.2;323.4;298.61;8;1;379;99479#",
        "@012;T;00:00:26;GSM Process error.#",
        "@012;D;13.08.16;10:24:49.0;5004.340927N;01432.673110E;6.2;323.4;298.61;8;1;379;99479#",
        "@012;T;00:00:26;GSM Process error.#",
        "@012;D;13.08.16;10:24:49.0;5004.340927N;01432.673110E;6.2;323.4;298.61;8;1;379;99479#",
        "@012;T;0:00:26;GSM Process error.#",
        "@012;D;x;x;x;x;x;x;x;x;x;320;99473#",
        "@012;00:00:15;#",
        "@asdfasdfasdfasdf#",
]

test_list_b = [
        "@004;T;00:00:00;Var. init.;SW:PaPa,0.2;HW:s12,SIM5320e,bastl#",
        "@004;T;00:00:00;Reset#",
        "@004;T;00:00:05;Init wait done.#",
        "@004;T;00:00:05;Modem init done.#",
        "@004;D;x;x;x;x;x;x;x;x;x;320;99486#",
        "@004;D;x;x;x;x;x;x;x;x;x;320;99473#",
        "@004;D;x;x;x;#",
]

class Device(threading.Thread):
    '''
    Class for emitating client instance. Just send some data to server.
    '''
    def __init__(self, ip, port, flag):
        threading.Thread.__init__(self)
        self.running = True
        self.ip = ip
        self.port = port
        self.flag = flag

    def run(self):
        i = 0
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.ip, self.port))
            if self.flag:
                _set = test_list_b
            else:
                _set = test_list
            while i < len(_set):
                sock.sendall(bytes(_set[i], 'ascii'))
                i += 1
                # time.sleep(1)

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

