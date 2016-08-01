#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import threading
import socketserver

logger = logging.getLogger(__name__)

class Server(socketserver.ThreadingMixIn, socketserver.TCPServer):
    '''
    This class is responsible for receiving and handling all request by clients.
    '''
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # Much faster rebinding
    allow_reuse_address = True
