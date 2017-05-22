#!/bin/bash
if [ "$#" -eq 4 ]; then
	HOME_DIR=/home/vagrant
	BASE_DIR=/home/thecorp/django/$1
	VIRT_ENV=$BASE_DIR/virt_env/bin/activate
	if [ ! -d $BASE_DIR/virt_env ]; then
		mkdir $BASE_DIR/virt_env
	fi
	virtualenv $BASE_DIR/virt_env --always-copy
	source $VIRT_ENV
	pip3 install --upgrade pip
	pip3 install -r $BASE_DIR/requirements.txt
	deactivate
	sudo -u postgres psql -c "create database $2;"
	sudo -u postgres psql -c "create user $3 with password '$4';"
	sudo -u postgres psql -c "alter role $3 set client_encoding to 'utf8';"
	sudo -u postgres psql -c "alter role $3 set timezone to 'UTC';"
	sudo -u postgres psql -c "grant all privileges on database $2 to $3;"
	echo cd $BASE_DIR >> $HOME_DIR/.bashrc
	echo source $VIRT_ENV >> $HOME_DIR/.bashrc
else
	echo "Invalid number of arguments"
fi
