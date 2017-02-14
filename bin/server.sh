#/!/bin/bash

#==============================================================================
# Script for running socket server with specified configuration file.
#==============================================================================

# DIRRECTORY="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# DIRECTORY=$(echo $(pwd) )
# Application directory
DIRECTORY="$( cd "$( dirname "$0" )/../" && pwd )"
# File with list of created servers
SERVERS_LIST="/tmp/servers_list"
touch $SERVERS_LIST

# Help message
#==============================================================================
function help(){
    echo -e "This script is used to manipulate Telemetry data servers. It
allows spawn, terminate TCP-servers, backup and clear data after them."
    echo -e "\t-h show this help text"
    echo -e "\t-s config: Spawn server with specified configuration."
    # echo -e "\t-t config: Terminate server."
    echo -e "\t-b config: Backup server's data storage and database."
    echo -e "\t-c config: Clear server's data storage and database."
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

# Runs server
#==============================================================================
function run(){
    # Run server
    cd $DIRECTORY/src/
    nohup python3 main.py $1 > /dev/null 2>&1 &
    PID=$!

    if [ $? -eq 0 ]; then
        # Success
        echo "Server is succesfully run in background. PID:" $PID
        append_to_servers_list ${CONFIG['server_name']} ${CONFIG['port']} $PID
        return 1
    else
        # Fail
        echo "Fail to run server."
        return 0
    fi
}

# Backup function
#==============================================================================
function backup(){
    head "Start backup for ${CONFIG['mysql_db']} on host ${CONFIG['mysql_host']}."

    # Create file
    filename=$DIRECTORY"/backups/${CONFIG['mysql_db']}.sql"
	# Check if file already exists
    if [ -f $filename ]; then
        error "File already exists!"
		confirm
		if [ $? -eq 1 ]; then
			return 1
		fi
    fi
    mkdir -p "$(dirname "$filename")" && touch "$filename"
    echo "Database backup will be stored in $filename."

    # Backup database
    mysqldump --single-transaction --flush-logs --master-data=2 \
    -h"${CONFIG['mysql_host']}" -u"${CONFIG['mysql_user']}" \
    -p"${CONFIG['mysql_pass']}" --databases "${CONFIG['mysql_db']}" > $filename

    if [ $? -eq 0 ]; then
        success "Succsess."
        # Success
        return 0
    else
        error "Fail."
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
 echo -ne "${BLUE}"
 printf '%*s' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =
 echo -e ${1}
 printf '%*s' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =
 echo -e "${NC}"
}

function info(){
 echo -e "${BLUE}${1}${NC}"
}

function success(){
 echo -e "${GREEN}${1}${NC}"
}

function error(){
 echo -ne "${RED}"
 printf '%*s' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =
 echo -e ${1}
 printf '%*s' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =
 echo -e "${NC}"
}

function append_to_servers_list(){
    echo "Name: $1. Port: $2. PID: $3" >> $SERVERS_LIST
}

function list_all_open_server(){
    error "BE CAREFUL!!! This list can be wrong and doesn't have actual
    information. There is posibillity that it is not your server and you can 
    kill wrong process. Check what process you want to kill before doing it."
    echo "To stop server type following command. 'kill PID'"

    # TMP file used for server list cleaning
    TMP=$(mktemp)
    # Delete already killed servers
    while IFS='' read -r line || [[ -n "$line" ]]; do
        PID=$(echo $line | cut -d' ' -f6)

        ps -p $PID > /dev/null
        if [[ $? -ne 0 ]]
        then
            awk "!/$PID/" $SERVERS_LIST > $TMP && mv $TMP $SERVERS_LIST
        fi
    done < $SERVERS_LIST

    head "List of servers:"
    cat $SERVERS_LIST
}

function confirm() {
    read -r -p "${1:-Are you sure? [y/N]} " response
    case "$response" in
        [yY][eE][sS]|[yY]) 
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}


#==============================================================================
# Main
#==============================================================================

while [[ $# -gt 0 ]]; do
    # Get command
    arg="$1"
    # Parse arguments
    #==========================================================================
    case $arg in
        -s|--spawn)
            head "Spawning server."
            config="$( cd "$(dirname "$2")" && pwd )""/$(basename $2)"
            # Execute configuration script
            eval "$(cat $config | $DIRECTORY/bin/ini2arr.py)"

            run $config
            shift
            ;;
        -c|--clear)
            head "Clear server's data."
            remove_server $mysql_db $mysql_user $mysql_pass $host $catalog_name 
            if [ $? -eq 0 ]; then
                success "Server's data were successfully removed from the 
                         machine."
            else
                error "Fail to remove server's data."
            fi
            shift
            ;;
        -b|--backup)
            config="$( cd "$(dirname "$2")" && pwd )""/$(basename $2)"
            # Execute configuration script
            eval "$(cat $config | $DIRECTORY/bin/ini2arr.py)"

            backup
            if [ $? -eq 0 ]; then
                success "Succesfully backup whole database."
            else
                error "Fail to back up database.";
            fi
            shift
            ;;
        -l|--list)
            list_all_open_server
            shift
            ;;
        *)
            help
            exit 1
            ;;
    esac
    shift
done
