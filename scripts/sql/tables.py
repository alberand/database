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

# Tables with data loggers
TABLES['sessions'] =  (
    'CREATE TABLE `sessions` ('
    '    `ses_id` VARCHAR(11) NOT NULL,'                    # Session number
    '    `name`   VARCHAR(255) DEFAULT \'Default Name\','   # Session name
    '    PRIMARY KEY (`ses_id`)'
    ') ENGINE=InnoDB'
)

TABLES['connections'] = (
    'CREATE TABLE `connections` ('
    '    `device_id` INT(11) NOT NULL,'
    '    `ses_id` VARCHAR(11) NOT NULL,'                    # Session number
    '    PRIMARY KEY(`device_id`)'
    ') ENGINE=InnoDB'
)

# Tables with received packages
TABLES['packages'] =  (
    'CREATE TABLE `packages` ('
    '    `id` int(11) NOT NULL AUTO_INCREMENT,'     # Sample id
    '    `ses_id` VARCHAR(11) NOT NULL,'                # Session id
   #'    `module_id` INT(11) NULL,'                 # Module id
   #'    `ses_time` TIME NULL,'                     # Time
    '    `date` DATE NULL,'                         # Date
    '    `time` TIME NULL,'                         # Time
    '    `t_ms` INT(11) NULL,'                      # Time microseconds
    '    `latitude` FLOAT(10, 5) NULL,'             # Latitude
    '    `lat_pos` ENUM("N", "S") NULL,'            # Latitude point N/S
    '    `longitude` FLOAT(10, 5) NULL,'            # Longitude
    '    `lon_pos` ENUM("E", "W") NULL,'            # Longitude point E/W
    '    `course` FLOAT NULL,'                      # Course
    '    `gps_altitude` FLOAT(4, 1) NULL,'          # Gps altitude
    '    `speed` FLOAT NULL,'                       # Speed 
   #'    `temperature` INT(11) NULL,'               # Temperature 
   #'    `pressure` INT(11) NULL,'                  # Pressure
    '    `gps_state` INT(11) NULL,'                 # Is gps connected
    '    `sat_num` INT(11) NULL,'                   # Number of sattelites
    '    `gsm_sig_str` FLOAT NULL,'                 # GSM signal strength
    '    `net_provider` VARCHAR(20) NULL,'          # Network provider O2
    '    `network_type` VARCHAR(5) NULL,'           # Network type 2G, 3G...
    '    `x_acc` FLOAT NULL,'                       # X accelerometer
    '    `y_acc` FLOAT NULL,'                       # Y accelerometer
    '    `z_acc` FLOAT NULL,'                       # Z accelerometer
    '    FOREIGN KEY pkg_session(`ses_id`)'
    '        REFERENCES sessions(`ses_id`),'
    '    PRIMARY KEY (`id`)'
    ') ENGINE=InnoDB'

)

# Table with messages
TABLES['messages'] =  (
    'CREATE TABLE `messages` ('
    '    `id` int(11) NOT NULL AUTO_INCREMENT,'     # Message id
    '    `ses_id` VARCHAR(11) NOT NULL,'            # Session id
    '    `ses_time` TIME NULL,'                     # Time
    '    `msg` VARCHAR(255) NOT NULL,'              # Message
    '    FOREIGN KEY msg_session(`ses_id`)'
    '       REFERENCES sessions(`ses_id`),'
    '    PRIMARY KEY (`id`)'
    ') ENGINE=InnoDB'

)

# Table with filenames to store data
# TABLES['filenames'] =  (
    # 'CREATE TABLE `filenames` ('
    # '    `id` int(11) NOT NULL AUTO_INCREMENT,'         # File id
    # '    `ses_id` int(11) NOT NULL,'                    # Session id
    # '    `filename` VARCHAR(255) NOT NULL,'             # Filename
    # '    PRIMARY KEY (`id`)'
    # ') ENGINE=InnoDB'
# )
