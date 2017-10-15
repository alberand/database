#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import threading

import config

logger = logging.getLogger(__name__)

class Source:

    def __init__(self, queue, name=None):
        self.queue = queue
        self.name = name if name else self.__hash__()

        self.source = None

    def init(self):
        if self.source is None:
            self.source = config['source']['class']()
        thread = threading.Thread(target=self.source.acquire)
        thread.daemon = True
        thread.start()

    def stop(self):
        self.source.stop()
