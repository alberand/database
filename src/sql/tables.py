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
    '    `latitude` FLOAT(11, 11) NOT NULL,'            # Latitude
    '    `lat_pos` ENUM("N", "S") NOT NULL,'            # Latitude point N/S
    '    `longitude` FLOAT(11, 11) NOT NULL,'           # Longitude
    '    `lon_pos` ENUM("E", "W") NOT NULL,'            # Longitude point E/W
    '    `course` FLOAT(11, 11) NOT NULL,'              # Speed
    '    `gps_altitude` FLOAT(11, 11) NOT NULL,'        # Gps altitude
    '    `temperature` INT(11) NOT NULL,'               # Temperature 
    '    `pressure` INT(11) NOT NULL,'                  # Pressure
    '    PRIMARY KEY (`smp_no`)'
    ') ENGINE=InnoDB'

)
