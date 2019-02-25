#!/bin/bash

git pull
export PIPENV_VENV_IN_PROJECT=True
pipenv install
yarn install
node_modules/.bin/gulp

pipenv run toja init-db
