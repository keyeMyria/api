#!/bin/sh

python manage.py migrate auth || echo "ok"
python manage.py migrate contenttypes || echo "ok"

# run syncdb only on first (empty) db
python manage.py migrate --run-syncdb || echo "ok"


# preforms migrations for auth and contenttypes contrib apps
# python manage.py migrate auth

# python manage.py makemigrations
python manage.py migrate
python manage.py loaddata --app core initial_data.json
