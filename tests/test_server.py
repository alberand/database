#!/bin/python

import os
import sys
import threading
import socketserver

# sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/src"))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from client import Client
from tserver.server import Server
from tserver.handler import RequestHandler

def test_hello():
    assert 2 == 2

def test_run_server():
    ip = '127.0.0.1'
    port = 5000
    s = Server((ip, port), RequestHandler)
    t = threading.Thread(target=s.acquire)
    t.start()

    s.shutdown()
    t.join()

def test_client_send():
    ip = '127.0.0.1'
    port = 5000
    s = Server((ip, port), RequestHandler)
    t = threading.Thread(target=s.acquire)
    t.start()

    client = Client(ip, port)
    client.start()
    client.send('Hello world')
    client.stop()

    client.join()

    s.shutdown()
    t.join()
