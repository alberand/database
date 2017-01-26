Telemetry data collecting server and web-interface
===============================================================================
This repository contains scripts, programs and other materials for the project 
developed in CAST team at Czech Technical University.

The purpose of this application is to collect telemetry data from devices
(GPS-tracker, mobile etc.) and save them for further usage. Two type of data
storage are used MySQL database and *.txt* files.

Application is also delivered with a HTTP-server based on Django framework.
This interface allows display data on the interactive map and download collected
files. 

# How to run
Run collecting server:
1. Go to source directory
2. Run following command with specified configuration file:
```
python3 ./main.py config.json
```
This will run collecting server. Now you can send data to address specified in
configuration file.

Run GUI server:
1. Go to source directory. Then to the *gui* directory.
2. Run following program:
```
python3 ./manage.py runserver 8000
```
Web-interface will be available at address of your machine with port 8000.
