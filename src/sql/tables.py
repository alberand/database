#!/usr/bin/env python
# -*- coding: utf-8 -*-

#==============================================================================
# Description of tables to create.
# Attention to quotes. This is python quotes ' and this is mysql quotes `
#==============================================================================

# ENGINE says what engine MySQL is using to store data. InnoDB is default, for
# example CSV will store all data in CSV format, Blackhole will return always
# return empty set etc.

TABLES = dict()

TABLES['logger'] =  (
    'CREATE TABLE `logger` ('
    '    `smp_no` int(11) NOT NULL AUTO_INCREMENT,'     # Sample number
    '    `module_id` INT(11) NOT NULL,'                 # Module id
    '    `date` DATE NOT NULL,'                         # Date
    '    `time` TIME NOT NULL,'                         # Time
    '    `t_ms` INT(11) NOT NULL,'                      # Time microseconds
    '    `latitude` FLOAT(10, 5) NOT NULL,'            # Latitude
    '    `lat_pos` ENUM("N", "S") NOT NULL,'            # Latitude point N/S
    '    `longitude` FLOAT(10, 5) NOT NULL,'           # Longitude
    '    `lon_pos` ENUM("E", "W") NOT NULL,'            # Longitude point E/W
    '    `course` FLOAT NOT NULL,'              # Course
    '    `gps_altitude` FLOAT(4, 1) NOT NULL,'        # Gps altitude
    '    `speed` FLOAT NOT NULL,'               # Speed 
    '    `temperature` INT(11) NOT NULL,'               # Temperature 
    '    `pressure` INT(11) NOT NULL,'                  # Pressure
    '    `unknown_1` INT(11) NOT NULL,'                 # 
    '    `unknown_2` INT(11) NOT NULL,'                 # 
    '    PRIMARY KEY (`smp_no`)'
    ') ENGINE=InnoDB'

)
