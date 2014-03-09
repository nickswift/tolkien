#!/bin/sh

# Check for dependencies
if [ ! -f "/usr/local/bin/node" ] 
then
    echo "ERR: NodeJS not installed -- compiling Node"
fi
if [ ! -f "/usr/bin/python" ]
then 
    echo "ERR: Python not installed"
fi 
if [ ! -d "/etc/apache2" ]
then
    echo "ERR: Apache2x not installed"
fi 

# Create needed directories
if [ ! -d "/django/tolkien" ]
then
    if [ ! -d "/django" ]
    then
        sudo mkdir /django 
    fi 
    sudo mkdir /django/tolkien 
fi

# Install PIP/Django/Requirements if they don't exist
sudo apt-get install python-pip python-dev build-essential libapache2-mod-wsgi \
    mysql-server libmysqlclient-dev
sudo pip install -r ./backend/requirements.txt

# Move apache config into place and bring server down for maintenence
sudo rm -f /etc/apache2/sites-available/000-default.conf 
sudo cp ./config/000-default.conf /etc/apache2/sites-available
sudo service apache2 stop

# Move Django app into place
sudo rm -rf /django/tolkien/*
sudo cp -r ./backend/* /django/tolkien/

# Move frontend into place 
cd frontend
npm install 
bower install 
sudo grunt

sudo chmod -R 0755 ./build/
sudo rm -rf /var/www/*
sudo cp -r ./build/* /var/www/

# Restart server
sudo service apache2 start