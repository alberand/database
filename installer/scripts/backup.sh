#!/bin/bash

echo "Enter ROOT password of the database (not user)."
mysqldump --single-transaction --flush-logs --master-data=2 --all-databases -u root -p > ../backups/all_databases.sql
