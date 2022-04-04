#!/bin/bash

cd /calisabor
export PYTHONPATH=/calisabor;$PYTHONPATH

python manage.py makemigrations
python manage.py migrate
python manage.py initadmin
python manage.py runserver 0.0.0.0:8080