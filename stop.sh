#!/bin/bash
kill -9 `ps -aux | grep gunicorn | grep houdini.wsgi:application | awk '{ print $2 }'`
