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
	pip3 install -r $BASE_DIR/requirements.txt
	deactivate
	mysql -uroot -proot -e "create database $2;"
	mysql -uroot -proot -e "create user '$3'@'localhost' identified by '$4';"
	mysql -uroot -proot -e "grant all privileges on $2 . * to '$3'@'localhost';"
	mysql -uroot -proot -e "flush privileges;"
	echo cd $BASE_DIR >> $HOME_DIR/.bashrc
	echo source $VIRT_ENV >> $HOME_DIR/.bashrc
else
	echo "Invalid number of arguments"
fi
