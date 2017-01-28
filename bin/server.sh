#/!/bin/bash

#==============================================================================
# Script for running socket server with specified configuration file.
#==============================================================================

# DIRRECTORY="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# DIRECTORY=$(echo $(pwd) )
DIRECTORY="$( cd "$( dirname "$0" )/../" && pwd )"

# Help message
#==============================================================================
function help(){
    echo -e "This script is used to manipulate Telemetry data servers. It
allows spawn, terminate TCP-servers, backup and clear data after them."
    echo -e "\t-h show this help text"
    echo -e "\t-r config: Spawn server with specified configuration."
    echo -e "\t-t config: Terminate server."
    echo -e "\t-b config: Backup server's data storage and database."
    echo -e "\t-d config: Clear server's data storage and database."
}

# Run function
#==============================================================================
function clear_server(){
    # Get arguments
    mysql_db="$1"
    mysql_user="$2"
    mysql_pass="$3"
    host="$4"
    catalog="$5"

    # Run script which will drop database
    python3 $DIRECTORY/scripts/clear.py $mysql_user $mysql_pass $mysql_db $host "drop"
    # TODO remove data catalog
}

# Run function
#==============================================================================
function run(){
    # Create tmp file
    tmpfile=$(mktemp)
    # Fill this file with JSON configuration created from bash config
    python3 $DIRECTORY/scripts/json_config_producer.py $tmpfile $1
    # Run server
    cd $DIRECTORY/src/
    exec python3 main.py $tmpfile
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


#==============================================================================
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
    config="$( cd "$(dirname "$2")" && pwd )""/$(basename $2)"
    # Execute configuration script
    # Run command
    case $arg in
        -c|--config)
            head "Config specified."
            run $config
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
