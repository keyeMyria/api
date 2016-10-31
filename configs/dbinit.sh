#!/bin/sh
until psql -h db -U "postgres" -c '\l'; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done
sleep 1
psql -h db -U postgres -c "CREATE USER pashinin WITH PASSWORD 'superpass';"
psql -h db -U postgres -c "CREATE DATABASE pashinin WITH OWNER pashinin;"
# psql -h db -U postgres -c "grant all privileges on database pashinin to pashinin;"
