#!/bin/bash

#==============================================================================
# This script is used for installing TCP-server + Web-interface on linux
# machine.
#==============================================================================

#******************
# SHOULD BE CHANGED
#******************
# Load configuration
source ./config.cfg
# User home directory
USER_HOME="/home/$user/"

# Folder with sources
src_folder="./src"
# Running scripts (should be separated by spaces).
run_scripts="run_server.sh run_web_interface.sh"
# Folder with .deb packages
pkg_folder="./packages"
# File with list of requered python-packages
list_of_pp="./requirements.txt"

#==============================================================================
# Utils
#==============================================================================
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'
function head(){
 echo -e "${GREEN}=============================================================================="
 echo -e "$1"
 echo -e "==============================================================================${NC}"
}

function info(){
 echo -e "${BLUE}$1${NC}"
}

function success(){
 echo -e "${GREEN}$1${NC}"
}

function error(){
 echo -e "${RED}=============================================================================="
 echo -e "$1"
 echo -e "==============================================================================${NC}"
}

#==============================================================================
# Initalize user
#==============================================================================
head "Creating user."
info "Adding user with name \"$user\""

# Adds user
id -u $user &>/dev/null
if [ $? -eq 1 ]; then 
 adduser --gecos "" $user
 echo "# Custom users" >> /etc/sudoers
 echo "$user ALL=(ALL:ALL) ALL" >> /etc/sudoers
 success "User added."
else
 info "User with this name already exists. So, use \"$user\"."
fi

#==============================================================================
# Install system packages
#==============================================================================
head "Installing linux packages."

fuser /var/lib/dpkg/lock &>/dev/null
if [ $? -eq 1 ]; then
  # Install mysql-server
  info "Installing mysql-server ..."
  yes | dpkg -s --force-confdef mysql-server &>/dev/null
  if [ $? -eq 1 ]; then
      apt-get install mysql-server
  fi
  info "Installing libmysqlclient-dev..."
  dpkg -s --force-confdef libmysqlclient-dev &>/dev/null
  if [ $? -eq 1 ]; then
      apt-get install libmysqlclient-dev
  fi
  # Install python3
  info "Installing python3 ..."
  dpkg -s --force-confdef python3 &>/dev/null
  if [ $? -eq 1 ]; then
      apt-get install python3
      success "Python3 installed."
  fi
  # Install python3-dev
  info "Installing python3-dev ..."
  dpkg -s --force-confdef python3-dev &>/dev/null
  if [ $? -eq 1 ]; then
      apt-get install python3-dev
      success "Python3 installed."
  fi
  # Install pip3
  info "Installing pip3 ..."
  which pip3 &>/dev/null
  if [ $? -eq 1 ]; then
      python3 get-pip.py
      success "pip3 installed."
  fi
else
  error "dpkg lock is locked. Can't install packages. Are you installing something?"
  exit 1
fi

#==============================================================================
# Update server configuration
#==============================================================================
python3 ./update_config.py

#==============================================================================
# Move sources
#==============================================================================
head "Moving source files."
# Create catalog
info "Creating " + "$USER_HOME/$catalog_name"
mkdir -p "$USER_HOME/$catalog_name"
# Move source files to their places
info "Copying source files ..."
cp -R "$src_folder" "$USER_HOME/$catalog_name"
# Move run files
for file in $run_scripts; do cp "$file" "$USER_HOME/$file"; done

#==============================================================================
# Change user right
#==============================================================================
chmod u+x "$USER_HOME/$catalog_name"
chmod -R ug+rw "$USER_HOME/$catalog_name"
chown -R $user:$user "$USER_HOME/$catalog_name"

#==============================================================================
# Add virtual environment
#==============================================================================
head "Adding virtual environment"
info "Installing virtualenv..."
wcich virtualenv &>/dev/null
if [ $? ]; then
    pip3 --no-cache-dir install virtualenv
fi

info "Creating new virtual environment for Python packages ..."
# Create virtual environment
virtualenv -p `which python3` "$USER_HOME/$catalog_name/$venv_name"
# Activate virtenv
source "$USER_HOME$venv_name"/bin/activate

#==============================================================================
# Install python packages from .deb
#==============================================================================
head "Installing linux packages from .deb files."
fuser /var/lib/dpkg/lock &>/dev/null
if [ $? -eq 1 ]; then
  info "Installing mysql-connector-python"
  dpkg -i "$pkg_folder/mysql-connector-python-py3_2.1.3-1ubuntu14.04_all.deb"
else
  error "dpkg lock is locked. Can't install packages. Are you installing something?"
  exit 1
fi

#==============================================================================
# Install python packages
#==============================================================================
head "Installing python packages ..."
pip3 --no-cache-dir install -r $list_of_pp

#==============================================================================
# Initialize database
#==============================================================================
head "Creating mysql user and mysql tables..."
# Create MySQL user
info "Creating creation user \"$mysql_user\" ..."
echo "CREATE USER '$mysql_user'@'localhost' IDENTIFIED BY '$mysql_pass';" | mysql -uroot -p
# Create database
echo "CREATE DATABASE $mysql_db" | mysql -uroot -p
# Give mysql-user privileges
echo "GRANT ALL PRIVILEGES ON $mysql_db.* TO '$mysql_user'@'localhost';" | mysql -uroot -p
echo "FLUSH PRIVILEGES;" | mysql -uroot -p

info "Creating tables and database ..."
# Create database and tables
python3 ./scripts/init.py
