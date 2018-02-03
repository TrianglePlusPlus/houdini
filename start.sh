#!/bin/bash

cd /home/thecorp/django/houdini/houdini

../virt_env/bin/gunicorn -w 8 -b 127.0.0.1:8080 --log-file /tmp/houdini.log -D houdini.wsgi:application
