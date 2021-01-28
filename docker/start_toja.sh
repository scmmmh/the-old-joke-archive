#!/bin/bash

# Setup the database
toja -c /etc/toja/production.ini init-db
while [ $? -ne 0 ]
do
    sleep 10
    toja -c /etc/toja/production.ini init-db
done

# Run the background tasks
TOJA_CONFIGURATION_URI=/etc/toja/production.ini dramatiq --processes 1 toja.tasks &

# Run the web application
pserve /etc/toja/production.ini
