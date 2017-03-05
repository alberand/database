# Telemetry data collecting server and web-interface

This repository contains scripts, programs and other materials for the project 
developed in CAST team at Czech Technical University.

The purpose of this application is to collect telemetry data from devices
(GPS-tracker, mobile etc.) and save them for further usage. Two type of data
storage are used MySQL database and *.txt* files.

Application is also delivered with a HTTP-server based on Django framework.
This interface allows display data on the interactive map and download collected
files. 

## Installation guide

You should get two files. This installation guide and _tserver-*.deb_
package.

1. Install *.deb* package by running following commands.

```sh
    sudo dpkg -i tserver.deb
    sudo apt-get install -f
```

First command will fail and generate required list of dependencies. Second
command will install all needed packages and main package.

While installation if MY SQL-server is not installed you will be asked for MY SQL
root password.

2. After successful installation you can create new configuration file. You can
   find template configuration file at `/opt/tserver/bin`. There will be file
   named `config`. Copy it somewhere to home folder and change it as you need.

```sh
    cp /opt/tserver/bin/config ~/config.ini
```

Pay attention to fields `port`. If chosen port will already in use server will 
fail to start.

## Usage

Prepared configuration file can be used to run, backup and delete all data of 
the server (database, text-files).

To run server use following command:

```sh
    tserver -s config.ini
```

This will run collecting server. Now you can send data to address specified in
configuration file.


To see all possible commands run:

```sh
    tserver -h
```

### Notes
For now it is impossible to automatically run web-interface. Also it can be run
only for one server simultaneously. 

Run GUI server:

1. Go to source directory:

```sh
    cd /opt/tserver/src/gui
```

2. Run following program:

```
python3 ./manage.py runserver 8000
```

Web-interface will be available at address of your machine with port 8000. For
example: 192.168.0.1:8000
