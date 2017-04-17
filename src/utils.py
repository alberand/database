#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random

from hashids import Hashids

def get_session_id(key=None):
    '''
    This function generate random number from some seed.
    Args:
        key: string or integer
    Returns:
        Random 5 places ingeger.
    '''
    hashids = Hashids(min_length=8, salt=str(random.randint(0, 1000)))

    return hashids.encode(key)

if __name__ == '__main__':
    print(get_session_id(2))
