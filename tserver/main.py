#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging.config

from config import config
from processor import Processor

logging.filename = os.path.abspath('../logs/{}_log'.format(config['server_name']))
logging.config.fileConfig(os.path.abspath('logging.ini'))

def start():
    if '-h' in sys.argv or '--help' in sys.argv:
        print('Run this file and as the first argument send name of the config'
              'file. For example: python main.py config.ini')

    if len(sys.argv) < 2:
        logging.error('Please specify config name.')
        sys.exit(1)

    listener = Processor()
    try:
        listener.start()
    except KeyboardInterrupt:
        logging.info('KeyboardInterrupt. Exiting...')
        listener.stop()
        listener.join()

if __name__ == '__main__':
    start()
