#!/bin/bash
python3 manage.py makemigrations
python3 manage.py migrate
service apache2 restart
