#!/bin/bash
(cd /var/www/project/src; ./manage.py migrate --run-syncdb --settings=pashinin.settings)
(cd /var/www/project/src; ./manage.py migrate --settings=pashinin.settings)

#
