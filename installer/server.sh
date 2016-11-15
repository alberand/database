#!/bin/bash

#==============================================================================
# Script for running socket server with specified configuration file.
#==============================================================================


while [[ $# -gt 0 ]]; do
    arg="$1"
    case $arg in
        -c|--config)
            echo "Config specified."
            config="$2"
            shift
            ;;
        -r|--remove)
            echo "Remove server."
            config="$2"
            shift
            ;;
        -b|--backup)
            echo "Backup server data."
            config="$2"
            shift
            ;;
        *)
            echo "Unknown parameter."
            exit 1
            ;;
    esac
    shift
done

# cd /home/database/database/src/
# python3 ./main.py
