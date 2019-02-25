#!/bin/bash

git pull
export PIPENV_VENV_IN_PROJECT=True
pipenv install
pipenv run pip install -e .
yarn install
node_modules/.bin/gulp

pipenv run toja init-db
