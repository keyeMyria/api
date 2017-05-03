-- -*- mode: sql -*-
CREATE USER pashinin WITH PASSWORD 'superpass';
ALTER USER "pashinin" CREATEDB;
CREATE DATABASE pashinin WITH OWNER pashinin;
