#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

def get_session_id(key):
    '''
    This function generate random number from some seed.
    Args:
        key: string or integer
    Returns:
        Random 5 places ingeger.
    '''
    random.seed(int(key))

    return random.randint(10000, 99999)

if __name__ == '__main__':
    print(get_session_id(1))
