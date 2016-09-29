#!/bin/bash

# Temporary script for running web interface for datbase.

cd /home/database/database/src/gui/
python3 ./manage.py runserver 147.32.196.177:8001
