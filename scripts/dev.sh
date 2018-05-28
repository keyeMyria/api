#!/bin/bash
export UID;docker-compose run --service-ports django python manage.py runserver 0.0.0.0:8000
