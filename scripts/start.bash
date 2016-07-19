#!/bin/bash

PIDFILE_1=/var/log/uwsgi/uwsgi_1.pid
PIDFILE_2=/var/log/uwsgi/uwsgi_2.pid

if [[ -f $PIDFILE_1 ]]; then
    echo -n "Stopping uwsgi instance 1(`cat $PIDFILE_1`) "
    while kill -0 `cat $PIDFILE_1` 2>/dev/null; do
      kill -INT `cat $PIDFILE_1`
      sleep 1
      echo -n ". "
    done
    echo "Stopped"
    rm -f $PIDFILE_1
fi
if [[ -f $PIDFILE_2 ]]; then
    echo -n "Stopping uwsgi instance 2 (`cat $PIDFILE_2`) "
    while kill -0 `cat $PIDFILE_2` 2>/dev/null; do
      kill -INT `cat $PIDFILE_2`
      sleep 1
      echo -n ". "
    done
    echo "Stopped"
    rm -f $PIDFILE_2
fi

num_processes=$(cat /home/ec2-user/conf/local_settings.py | grep NUM_UWSGI_PROCESSES | perl -ne 'if (/(\d+)/) { print "$1"; }')

DEFAULT_NUM_PROCESSES=2

echo -n "Starting uwsgi instance 1 with ${num_processes:=$DEFAULT_NUM_PROCESSES} processes "
/usr/local/bin/uwsgi \
      --chdir=/home/ec2-user/asappchat \
      --module=asappchat.wsgi_django:application \
      --env DJANGO_SETTINGS_MODULE=asappchat.settings \
      --env DJANGO_CONF_DIR=/home/ec2-user/conf \
      --master \
      --socket=127.0.0.1:8000 \
      --processes=${num_processes:=$DEFAULT_NUM_PROCESSES} \
      --enable-threads \
      --single-interpreter \
      --daemonize=/var/log/uwsgi/backend.log \
      --pidfile=$PIDFILE_1
echo "(`cat $PIDFILE_1`)"

echo -n "Starting uwsgi instance 2 with ${num_processes:=$DEFAULT_NUM_PROCESSES} processes "
/usr/local/bin/uwsgi \
      --chdir=/home/ec2-user/asappchat \
      --module=asappchat.wsgi_websocket:application \
      --env DJANGO_SETTINGS_MODULE=asappchat.settings \
      --env DJANGO_CONF_DIR=/home/ec2-user/conf \
      --master \
      --http-socket=127.0.0.1:8001 \
      --gevent 1000 \
      --http-websockets \
      --processes=${num_processes:=$DEFAULT_NUM_PROCESSES} \
      --enable-threads \
      --single-interpreter \
      --daemonize=/var/log/uwsgi/websocket.log \
      --pidfile=$PIDFILE_2
echo "(`cat $PIDFILE_2`)"
