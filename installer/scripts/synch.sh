#!/bin/bash

# This script synchronize local 'database'-project directory and remote
# directory on the server.

host="147.32.196.177"
user="database"

rsync -vrah --exclude 'src/config.py' --exclude 'src/logging.log' ../../database $user@$host:/home/database/
