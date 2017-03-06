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

You should get two files. _mysql-connector-python-*.deb_ and _tserver-*.deb_
packages.

1. Install *.deb* package by running following commands.

```sh
sudo dpkg -i mysql-connector-python-py3_2.1.3-1ubuntu14.04_all.deb
sudo dpkg -i tserver_1.0-1.deb
sudo apt-get install -f
```

First command install necessary package which is not in Ubuntu repository. 
Second command will fail and generate required list of dependencies. Last
command will install all needed packages and main package.

While installation if MySQL-server is not installed you will be asked for MySQL
root password.

## Usage
After successful installation you can create new configuration file. You should
find template configuration file at `/opt/tserver/bin`. There will be file
named `config`. Copy it somewhere to your home folder and change it as you need.

```sh
cp /opt/tserver/bin/config ~/config.ini
```

Pay attention to field `port`. If chosen port will be already in use server will 
fail to start.

Prepared configuration file can be used to run, backup and delete server. 
Deleting means that you can delete server's database and txt-files.

To run server use following command:

```sh
tserver -s config.ini
```

You will be ask for MySQL root password to check if there is specified MySQL
user or server needs to create it.

If specified database or MySQL user are not exist it will be automatically 
create. In the end of running process you will be informed about server status 
and see server PID. Process ID can be used to stop the server by using `kill`
command.

After successful running you can send data to address specified in 
configuration file. Manually data can be found in:

```
/opt/tserver/src/data/NAME_OF_SERVER/
``` 

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
