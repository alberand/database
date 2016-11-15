#!/bin/sh

database="loggersdb"
mysql_user="cast"
mysql_pass="castpass"


# Create file
touch "../backups/$database.sql"
filename="../backups/$database.sql"

# Backup database
mysqldump --single-transaction --flush-logs --master-data=2 -h "127.0.0.1" -u"$mysql_user" -p"$mysql_pass" --databases "$database" > $filename
