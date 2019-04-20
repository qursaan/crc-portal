#!/usr/bin/env bash

cd ..
# to remove all previous build files
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

python3 manage.py makemigrations
python3 manage.py migrate
#python manage.py createsuperuser --email admin@qursaan.com --username admin