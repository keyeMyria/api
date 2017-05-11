#!/bin/bash
(cd /var/www/project/src; python manage.py migrate --run-syncdb --settings=pashinin.settings)
(cd /var/www/project/src; python manage.py migrate --settings=pashinin.settings)
(cd /var/www/project/src; python manage.py loaddata --settings=pashinin.settings initial_data.json articles_examples.json ege_subjects.json)
