#!/bin/bash

# There is no "python" command in a db container - so need to tell
# "django" container to run migrations

touch /var/www/project/tmp/run-migrations
