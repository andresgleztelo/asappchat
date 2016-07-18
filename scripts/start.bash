#!/bin/bash

PIDFILE=/var/log/uwsgi/uwsgi.pid

if [[ -f $PIDFILE ]]; then
    echo -n "Stopping uwsgi (`cat $PIDFILE`) "
    while kill -0 `cat $PIDFILE` 2>/dev/null; do
      kill -INT `cat $PIDFILE`
      sleep 1
      echo -n ". "
    done
    echo "Stopped"
    rm -f $PIDFILE
fi

num_processes=$(cat /home/ec2-user/conf/local_settings.py | grep NUM_UWSGI_PROCESSES | perl -ne 'if (/(\d+)/) { print "$1"; }')

DEFAULT_NUM_PROCESSES=10

echo -n "Starting uwsgi with ${num_processes:=$DEFAULT_NUM_PROCESSES} processes "
/usr/local/bin/uwsgi \
      --chdir=/home/ec2-user/asappchat \
      --module=asappchat.wsgi:application \
      --env DJANGO_SETTINGS_MODULE=asappchat.settings \
      --env DJANGO_CONF_DIR=/home/ec2-user/conf \
      --master \
      --socket=127.0.0.1:8000 \
      --processes=${num_processes:=$DEFAULT_NUM_PROCESSES} \
      --enable-threads \
      --single-interpreter \
      --daemonize=/var/log/uwsgi/backend.log \
      --pidfile=$PIDFILE
echo "(`cat $PIDFILE`)"
