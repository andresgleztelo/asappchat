#!/bin/bash
set -e -x

VERSION=2.8.21

# Download and install redis in home directory
cd ~
wget http://download.redis.io/releases/redis-$VERSION.tar.gz
tar xzf redis-$VERSION.tar.gz
cd redis-$VERSION
make

# Start the redis server in the background
src/redis-server --daemonize yes

# To invoke the command line for testing use:
# src/redis-cli

# To stop the redis server, send 'shutdown' to redis command line:
# src/redis-cli shutdown
