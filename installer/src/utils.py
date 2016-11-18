#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

def get_session_id(key=None):
    '''
    This function generate random number from some seed.
    Args:
        key: string or integer
    Returns:
        Random 5 places ingeger.
    '''
    if key:
        random.seed(int(key))
    else:
        random.seed(random.randint(0, 1000))

    return random.randint(10000, 99999)

if __name__ == '__main__':
    print(get_session_id())
