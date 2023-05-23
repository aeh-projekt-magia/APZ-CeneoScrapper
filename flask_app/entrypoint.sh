#!/bin/bash

echo "Waiting for postgres to start..."
#TBD postgres healthcheck
#while ! nc -z users-db 5432; do
#  sleep 0.1
#done
#
#echo "Postgres started"

python manage.py run --host=0.0.0.0