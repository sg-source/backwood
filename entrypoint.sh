#!/bin/bash

python ./src/manage.py makemigrations
python ./src/manage.py migrate
python ./src/manage.py loaddata ./data/db.json

if [ "$DJANGO_SUPERUSER_EMAIL" ]
then
    python ./src/manage.py createsuperuser \
    --noinput \
    --email $DJANGO_SUPERUSER_EMAIL \
    --firstname $DJANGO_SUPERUSER_FIRSTNAME

fi

$@