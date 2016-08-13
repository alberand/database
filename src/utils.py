#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

def get_session_id(key):
    random.seed(int(key))

    return random.randint(10000, 99999)
