PostgreSQL
**********

To start db container separately:

.. code-block:: bash

   export UID; docker-compose -f docker/docker-compose.yml up db


Postgres in a Docker container (dev)
====================================

Postgres v10 is used currently in a docker container.

Django migrations
-----------------

Migrations run after you first start a database container. Postgres
container executes everything in
:code:`docker/docker-entrypoint-initdb.d` which is only touching a file
:code:`tmp/run-migrations`.

If this files exists :code:`make` will run migrations after containers
were started (and then remove :code:`tmp/run-migrations` file).

There is no way to do this in :code:`docker-entrypoint-initdb.d/...`
script because Postgres container does not have anything but Postgres,
even :code:`python` command.

Switching to a new Postgres version in a container
--------------------------------------------------

When writing in :code:`docker-compose.yml`

.. code-block:: yml

   db:
     image: postgres:<NEWER_VERSION>

container will not start with an error:

.. code-block:: text

    FATAL:  database files are incompatible with server
    DETAIL:  The data directory was initialized by PostgreSQL version 9.6, which is not compatible with this version 10.0.

In this case just recreate a database:

.. code-block:: bash

   make recreate-db

And start containers again:

.. code-block:: bash

   make
