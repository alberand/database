#!/bin/bash

#==============================================================================
# Script for running socket server with specified configuration file.
#==============================================================================

# Help message
#==============================================================================
function help(){
    echo -e "Help message."
}

# Run function
#==============================================================================
function remove_server(){
    # TODO need to drop whole database
    # Get arguments
    mysql_db="$1"
    mysql_user="$2"
    mysql_pass="$3"
    host="$4"
    catalog="$5"

    ./scripts/clear.py $mysql_user $mysql_pass $mysql_db $host "drop"
}

# Run function
#==============================================================================
function run(){
    echo "Run server."
}

# Backup function
#==============================================================================
function backup(){
    # Get arguments
    mysql_db="$1"
    mysql_user="$2"
    mysql_pass="$3"
    host="$4"

    # Create file
    filename="./backups/$mysql_db.sql"
    touch $filename
    info "Filename is $filename."

    # Backup database
    mysqldump --single-transaction --flush-logs --master-data=2 -h"$host" \
        -u"$mysql_user" -p"$mysql_pass" --databases "$mysql_db" > $filename

    if [ $? -eq 0 ]; then
        # Success
        return 0
    else
        # Fail
        return 1
    fi
}

#==============================================================================
# Utils
#==============================================================================
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'
function head(){
 echo -e "${BLUE}=============================================================================="
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


# Main
#==============================================================================

# echo $0
# echo $(basename $0)
# echo $(dirname $0)
# echo $(readlink -f $0)
# exit

while [[ $# -gt 0 ]]; do
    # Get command
    arg="$1"
    config="$2"
    # Execute configuration script
    source $config
    # Run command
    case $arg in
        -c|--config)
            head "Config specified."
            shift
            ;;
        -r|--remove)
            head "Remove server."
            remove_server $mysql_db $mysql_user $mysql_pass $host $catalog_name 
            if [ $? -eq 0 ]; then
                success "Server's data were successfully removed from the "\
"machine."
            else
                error "Fail to remove server's data."
            fi
            shift
            ;;
        -b|--backup)
            head "Backup server data."
            backup $mysql_db $mysql_user $mysql_pass $host
            if [ $? -eq 0 ]; then
                success "Succesfully backup whole database."
                msg="You should find file named the same as the name of the "\
"database with .sql format."
                echo -e "$msg";
            else
                error "Fail to back up database.";
            fi
            shift
            ;;
        *)
            help
            exit 1
            ;;
    esac
    shift
done

# cd /home/database/database/src/
# python3 ./main.py
