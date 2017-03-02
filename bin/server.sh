#!/bin/bash

# TODO:
# - When check if there Mysql user or not there can be user with the same name
# but different password. Should check it in future
# - Backup data direcotry

#==============================================================================
# Script for running socket server with specified configuration file.
#==============================================================================

# Application directory
# DIRECTORY="$( cd "$( dirname "$0" )/../" && pwd )" # Doesn't work for links
DIRECTORY="$( dirname "$(readlink -f "$0")" )/../"
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
    echo -e "\t-b config: Backup server's data storage and database."
    echo -e "\t-c config: Clear server's data storage and database."
}

# Run function
#==============================================================================
function clear_server(){
    echo -e "If server is running exit. PID: $PID."
    # Get server PID
    PID=$(list_all_open_server | grep "${CONFIG['server_name']}" | \
        cut -d" " -f6)

    if [[ -z "${PID// }" ]]; then
        echo "Server is down. Continue."
    else
        is_process_running $PID 
        status=$?
        if [ "$status" -eq "1" ]; then
            echo "Server is running (in accordence to '$0 -l'). Exit."
            exit 1
        fi
    fi

    echo -e "Check if database specified in configuration file exist."
    is_db_exist
    status=$?

    if [ "$status" -eq "1" ]; then
        echo "Database '${CONFIG['mysql_db']}' doesn't exist."
    elif [ "$status" -eq "2" ]; then
        error "Can't access to database with user: ${CONFIG['mysql_user']}."
        exit 1
    else
        echo "Delteting database."
        # Run script which will drop database
        python3 $DIRECTORY/scripts/clear.py $1 "drop"
    fi

    echo "Check if data folder exists and remove it."
    if [ -d "$DIRECTORY/src/data/${CONFIG['server_name']}" ]; then
        echo "Remove $DIRECTORY/src/data/${CONFIG['server_name']}."
        rm -Rv $DIRECTORY/src/data/${CONFIG['server_name']}
    else
        echo "Directory doesn't exist."
    fi
}

# Runs server
#==============================================================================
function run(){
    echo -e "Check if MySQL user specified in configuration file exist. If not create it."
    read -sp "Enter root's MySQL password: " root_mysql_pass
    echo
    is_mysql_user_exists $root_mysql_pass
    status=$?

    if [ "$status" -eq "0" ]; then
        error "MySQL user '${CONFIG['mysql_user']}' doesn't exist. Create it."
        python3 $DIRECTORY/scripts/create_user.py $1 $root_mysql_pass
    elif [ "$status" -eq "2" ]; then
        error "Can't create user ${CONFIG['mysql_user']}"
        exit 1
    elif [ "$status" -eq "1" ]; then
        success "[OK]"
    fi

    echo -e "Check if database specified in configuration file exist. If not create it."
    is_db_exist
    status=$?

    # Create database if doesn't exist
    if [ "$status" -eq "1" ]; then
        error "Database '${CONFIG['mysql_db']}' doesn't exist. Create it."
        python3 $DIRECTORY/scripts/init.py $1
    elif [ "$status" -eq "2" ]; then
        error "Can't access to database with user: ${CONFIG['mysql_user']}."
        exit 1
    elif [ "$status" -eq "0" ]; then
        success "[OK]"
    fi

    # Create data direcctory if doen't exist
    data_dir=$DIRECTORY/src/data/${CONFIG['server_name']}
    mkdir -p $data_dir
    echo "Server's data directory: $data_dir."

    echo "Running server."
    cd $DIRECTORY/src/
    nohup python3 main.py $1 > /dev/null 2>&1 &
    PID=$!

    echo "Sleep for a 3 seconds. Wait if server didn't crash."
    # TODO: Not sure about this timeout. It should include attempt to create TCP
    # socket and connect to MySQL database. For now, if error occure it happens
    # immediately (and as I know there is no any timeouts).
    sleep 3

    # If process still exists => server is running.
    is_process_running $PID 
    status=$?
    if [ "$status" -eq "1" ]; then
        # Success
        success "[OK]"
        echo "Server is run in background. PID:" $PID
        append_to_servers_list ${CONFIG['server_name']} ${CONFIG['port']} $PID
        return 0
    else
        # Fail
        error "Fail to run server."
        return 1
    fi
}

# Backup function
#==============================================================================
function backup(){
    head "Start backup for ${CONFIG['mysql_db']} on host ${CONFIG['mysql_host']}."

    echo "Check if database exist and user has access to it."
    is_db_exist
    status=$?

    if [ "$status" -eq "1" ]; then
        error "Database '${CONFIG['mysql_db']}' doesn't exist. Nothing to 
               backup."
        exit 1
    elif [ "$status" -eq "2" ]; then
        error "Can't access to database with user: ${CONFIG['mysql_user']}."
        exit 1
    fi


    echo "Create file to store backup."
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

    echo "Backup database."
    mysqldump --single-transaction --flush-logs --master-data=2 \
    -h"${CONFIG['mysql_host']}" -u"${CONFIG['mysql_user']}" \
    -p"${CONFIG['mysql_pass']}" --databases "${CONFIG['mysql_db']}" > $filename

    echo "Backup server's direcotry."
    if [ -d "$DIRECTORY/src/data/${CONFIG['server_name']}" ]; then
        cp -R $DIRECTORY/src/data/${CONFIG['server_name']} $DIRECTORY/backups/${CONFIG['server_name']}
        echo "Copy is saved to: $DIRECTORY/backups/${CONFIG['server_name']}"
    else
        echo -e "Server's directory $DIRECTORY/src/data/${CONFIG['server_name']}
        doesn't exist. Nothing to copy."
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
 # printf '%*s' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =
 echo -ne ${1}
 # printf '%*s' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =
 echo -e "${NC}"
}

function append_to_servers_list(){
    echo "Name: $1. Port: $2. PID: $3" >> $SERVERS_LIST
}

function list_all_open_server(){
    head "List of servers:"
    error "BE CAREFUL!!! This list can be wrong and doesn't have actual
    information. There is posibillity that it is not your server and you can 
    kill wrong process. Check what process you want to kill before doing it."
    echo -e "To stop server type following command. 'kill PID'"

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

    info "List of currently run PID:"
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

function is_db_exist(){
    RESULT=`mysql -u${CONFIG['mysql_user']} -p${CONFIG['mysql_pass']} \
    --skip-column-names -e "SHOW DATABASES LIKE '${CONFIG['mysql_db']}'"`
    # If fail to proceed (access denied)
    if [ $? -ne 0 ]; then
        return 2
    fi

    if [ "$RESULT" == "${CONFIG['mysql_db']}" ]; then
        # Exist
        return 0
    else
        # Doesn't exist
        return 1
    fi
}

###############################################################################
# Check if process with provided PID is running.
# Globals:
#   CONFIG: array with configurations.
# Arguments:
#   string: MySQL root password
# Returns:
#   Boolean. 1 exists.
###############################################################################
function is_mysql_user_exists(){
    mysql -uroot -p$1 -B -N -e 'use mysql; SELECT `user` FROM `user`;' |
    while read User; do
        if [[ "${CONFIG['mysql_user']}" == "$User" ]]; then
            # Exists
            return 1
        fi
    done
    
    # Doesn't exist
    return 0
}

###############################################################################
# Check if process with provided PID is running.
# Arguments:
#   int: PID of process
# Returns:
#   Boolean. 1 is running.
###############################################################################
function is_process_running(){
    # If process still exists => server is running.
    if ps -p $1 > /dev/null 
    then
        # Success
        return 1
    else
        # Fail
        return 0
    fi
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
            eval "$(cat $config | $DIRECTORY/scripts/ini2arr.py)"

            run $config
            shift
            ;;
        -c|--clear)
            config="$( cd "$(dirname "$2")" && pwd )""/$(basename $2)"
            # Execute configuration script
            eval "$(cat $config | $DIRECTORY/scripts/ini2arr.py)"

            clear_server $config
            if [ $? -eq 0 ]; then
                success "Server's data were successfully removed from the machine."
            else
                error "Fail to remove server's data."
            fi
            shift
            ;;
        -b|--backup)
            config="$( cd "$(dirname "$2")" && pwd )""/$(basename $2)"
            # Execute configuration script
            eval "$(cat $config | $DIRECTORY/scripts/ini2arr.py)"

            backup
            if [ $? -eq 0 ]; then
                success "Database is successfully backuped."
            else
                error "Fail to back up database.";
            fi
            shift
            ;;
        -l|--list)
            list_all_open_server
            shift
            ;;
        -t|--test)
            config="$( cd "$(dirname "$2")" && pwd )""/$(basename $2)"
            # Execute configuration script
            eval "$(cat $config | $DIRECTORY/scripts/ini2arr.py)"

            read -sp "Enter root's MySQL password:" root_mysql_pass
            echo
            is_mysql_user_exists $root_mysql_pass
            status=$?
            echo $status
            shift
            ;;
        *)
            help
            exit 1
            ;;
    esac
    shift
done
