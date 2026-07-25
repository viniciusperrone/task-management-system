#!/bin/bash

set -e

echo "Running migrations"
python manage.py migrate --noinput

echo "Starting Django"
exec "$@"
