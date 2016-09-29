#!/bin/bash

#==============================================================================
# This script is used for installing TCP-server + Web-interface on linux
# machine.
#==============================================================================

# Folder with sources
src_folder="./database"
# Running scripts (should be separated by spaces).
run_scripts="./run_server.sh ./run_web_interface.sh"
# Folder with .deb packages
pkg_folder="./packages"
# File with list of requered python-packages
list_of_pp="./requirements.txt"
# User name
user="database"
# User default password
password="castpass"
# MySQL user name
mysql_user="cast"
# MySQL user password
mysql_pass="castpass"

# Adds user
adduser $user
echo "# Custom users" >> /etc/sudoers
echo "$user ALL=(ALL:ALL) ALL" >> /etc/sudoers

# Login as new user
su - database

# Install system packages
apt-get install mysql-server
apt-get install python3
python3 get-pip.py

# Install python packages
pip3 install -r $list_of_pp

# Create MySQL user
echo "CREATE USER '$mysql_user'@'localhost' IDENTIFIED BY '$mysql_pass';" | mysql -uroot -p
# Create database and tables
python3 ./scripts/init.py
# Give mysql-user privileges
echo "GRANT ALL PRIVILEGES ON loggersdb.* TO '$mysql_user'@'localhost';" | mysql -uroot -p
echo "FLUSH PRIVILEGES;" | mysql -uroot -p

# Move source files to their places
cp -R "$src_folder" $HOME/database
# Move run files
for file in $run_scripts; do cp "$file" "$HOME/$file"; done
