#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import config
import logging.config

from listener import Listener

logging.config.fileConfig('logging.ini')

if __name__ == '__main__':

    if len(sys.argv) > 1:
        logging.info('Config file is specified.')

    listener = Listener()
    try:
        listener.start()
    except KeyboardInterrupt:
        logging.info('KeyboardInterrupt. Exiting...')
        listener.stop()
        listener.join()
