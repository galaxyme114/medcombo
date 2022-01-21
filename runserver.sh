#!/bin/bash
cd /home/ubuntu/
source env-medcombo/bin/activate
cd /home/ubuntu/Medcombo/
python manage.py runserver 0.0.0.0:8000 --settings=medcombo.settings.test


