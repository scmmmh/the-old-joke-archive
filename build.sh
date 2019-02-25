#!/bin/bash

if [ -f 'pre-build.sh' ]; then
   ./pre-build.sh
fi

git pull
#export PIPENV_VENV_IN_PROJECT=True
pipenv install
pipenv run pip install -e .

pipenv run toja init-db

if [ -f 'post-build.sh' ]; then
   ./post-build.sh
fi
