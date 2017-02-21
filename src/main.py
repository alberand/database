#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging.config

from listener import Listener

logging.config.fileConfig('logging.ini')

if __name__ == '__main__':
    if '-h' in sys.argv or '--help' in sys.argv:
        print('Run this file and as the first argument send name of the config'
              'file. For example: python main.py config.ini')

    if len(sys.argv) < 2:
        logging.error('Please specify config name.')
        sys.exit(1)

    listener = Listener()
    try:
        listener.start()
    except KeyboardInterrupt:
        logging.info('KeyboardInterrupt. Exiting...')
        listener.stop()
        listener.join()
