PostgreSQL
**********

To start db container separately:

.. code-block:: bash

   export UID; docker-compose -f docker/docker-compose.yml up db


Docker container (dev)
======================

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

Upgrading to a new Postgres version
-----------------------------------

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


PostgreSQL high availability
============================

Choose the best way for HA from `table 1
<https://www.postgresql.org/docs/current/static/different-replication-solutions.html#HIGH-AVAILABILITY-MATRIX>`_
and `table 2
<https://wiki.postgresql.org/wiki/Replication,_Clustering,_and_Connection_Pooling>`_


Looks like I need logical replication (in Postgres 10) with multimaster
so that I could write to any node.

I think it's better to have multimaster config to be able to write to
any node right away than wait for some sentinels to reconfigure a cluster.

#. `Solution from Postgres Profeccional (slides)
<https://postgrespro.ru/media/2017/02/10/mmtsslides-161110113542.pdf>`_
#. `CitusDB <https://www.citusdata.com/>`_

Looks like Citus is for lots of small writes, reads at first place
(separate a BIG table on several nodes and do reads a lot faster). And
only then high availability and disaster recovery.


Citus
-----

`Documentation <https://docs.citusdata.com/en/latest/>`_

Citus looks great at first. It was made for sharding actually. How about
replication, HA and DR? For HA, any data that is written to a primary
database called the Writer is instantly replicated onto a secondary
database called the Reader in real-time, through a stream called a WAL
or Write-Ahead-Log.

So no multimaster.

Bucardo
-------

`Bucardo <https://wiki.postgresql.org/wiki/Bucardo>`_ requires a
dedicated database and runs as a Perl daemon that communicates with this
database and all other databases involved in the replication. Nuff said.


pgpool-II
---------

http://www.pgpool.net/docs/latest/en/html

pgpool-II

   Scalability: Yes (up to 128 DB nodes)
   Read Scaling: Yes
   Write Scaling: No (possible to have up to 128 DB nodes, but performance is 60-70% of plain PostgreSQL)
   Synchronous replication: Yes
   Triggers/procedures: Yes
   Parallel Query: Yes
   Failover/HA: Yes
   Online Provisioning: Yes


Patroni
-------

Patroni, repmgr. Не слишком удобны в использовании и иногда могут терять данные.



Stolon
------

`Stolon <https://github.com/sorintlab/stolon>`_. Newer and probably
better than Patroni. Written in Go. Uses Consul. Runs sentinels, watches
and changes masters/slaves.


Future
======

.. note::

   Should I stick to traditional SQL database like Postgres or use a
   NewSQL database like `CockroachDB
   <https://github.com/cockroachdb/cockroach>`_ or a noSQL database?
