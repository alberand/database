Programs for work with database
===============================================================================
This repository contains scripts, programs and other materials to work with
database for the CAST team in Czech Technical University.

Outlines
===============================================================================
    - A lot of data loggers connected via Ethernet to Linux server (Ubuntu)
    - The server listen to TCP/IP socket and receive data packages from those
      loggers.
    - Those packages parsed and saved to database.

TODO
===============================================================================
 - Save data to files if connection to database lost.
 - Maybe close connection to database if for a logng time there is no data
   coming.
 - Periodically backup database to remote server (FTP)
