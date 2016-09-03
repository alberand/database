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
 - Maybe close connection to database if for a logng time there is no data
   coming.
 - Periodically backup database to remote server (FTP)
 - Handle case when client is closing connection without ending transmittion.
 - Creation random number from device id (import hashlib;
   hashlib.md5(b'').digest())
 - Parse packages
 - On web page open *.txt files in new tab
