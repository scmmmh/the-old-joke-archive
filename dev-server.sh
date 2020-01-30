#!/bin/bash

if [ $1 = "server" ]
then
    pserve --reload development.ini
fi

if [ $1 = "dramatiq" ]
then
    TOJA_CONFIGURATION_URI=development.ini dramatiq --processes 1 --watch src/toja/tasks toja.tasks
fi
