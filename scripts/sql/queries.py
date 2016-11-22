#!/usr/bin/env python
# -*- coding: utf-8 -*-

#==============================================================================
# Definiton of SQL quieries for work with database.
#==============================================================================

# Table's fields and values should be listed by ,

QUERIES = dict()

QUERIES['insert'] =  (
    'INSERT INTO {} '
    '({}) '
    'VALUES ({})'
)

QUERIES['select'] =  (
    'SELECT {} '
    'FROM {} '
    'WHERE {}'
)

QUERIES['update'] =  (
    'UPDATE {} '
    'SET {} '
    'WHERE {}'
)
