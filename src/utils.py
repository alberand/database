#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

def get_session_id(key):
    random.seed(int(key))

    return random.randint(10000, 99999)

if __name__ == '__main__':
    print(get_session_id(1))
