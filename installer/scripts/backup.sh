#!/bin/sh

function help(){
    echo -e "Backup script for database.\n"
    echo -e "To run this script throw three arguments to it:\n"
    echo -e "\t./backup.sh database_name mysql_user mysql_pass\n"
}

# Get arguments
if [ $# -eq 3 ]; then
    database="$1"
    mysql_user="$2"
    mysql_pass="$3"
else
    help
    exit 1
fi

# Create file
touch "../backups/$database.sql"
filename="../backups/$database.sql"

# Backup database
mysqldump --single-transaction --flush-logs --master-data=2 -h "127.0.0.1" -u"$mysql_user" -p"$mysql_pass" --databases "$database" > $filename
