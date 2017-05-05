.. pashinin.com documentation master file, created by
   sphinx-quickstart on Mon Dec 26 16:56:52 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pashinin.com
************

How to start?
=============

#. Register at Github_ and fork `this repository <https://github.com/pashinin-com/pashinin.com>`_.
#. Clone your new repo to your PC (Mac and Win users - just use `Github Desktop <https://desktop.github.com/>`_)
#. Start development server
#. Do changes
#. Make a pull request or `report a problem <https://github.com/pashinin-com/pashinin.com/issues>`_

All this in detail should be below...


`Docker`_ is used for containers.



Linux
-----

Clone your new repo (replace :code:`<YOUR_NAME>` with your Github login):

.. code-block:: bash

   git clone git@github.com:<YOUR_NAME>/pashinin.com.git
   make         # start Docker images
   make tmux    # start Django server and Gulp

In your browser go to http://example.org or http://localhost.


Windows
-------

.. warning::

   Docker for Windows runs on 64bit Windows 10 Pro, Enterprise and
   Education (1511 November update, Build 10586 or later). `And
   more... <https://docs.docker.com/docker-for-windows/install/#what-to-know-before-you-install>`_

Windows 10 64bit Pro or Enterprise
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Install `Docker for Windows <https://store.docker.com/editions/community/docker-ce-desktop-windows?tab=description>`_
#. Run setup.exe.
#. In your browser go to http://example.org or http://localhost.

Windows 7
^^^^^^^^^

Install `Docker Toolbox <https://www.docker.com/products/docker-toolbox>`_


Mac
---

Install Docker.


Update process
--------------

Commit -> Github -> Travis

When travis build is OK Travis sends info to a webhook (see travis.yml_). URL is:


.. code-block:: text

   https://pashinin.com/_hooks/travis/<SECRET>


Secret part is defined in travis_secret_settings_ `settings.py` and is
for being sure only Travis can contact us. TODO: See `Travis notes about
making it secure
<https://docs.travis-ci.com/user/notifications#Verifying-Webhook-requests>`_.

..
   travis encrypt "<account>:<token>#channel"

Tasks that do update process are defined in `core/tasks.py`_ (clone
repo, create css, collect static, restart server). Code that runs an
update process:


.. code-block:: python

   project_update.delay(commit_sha1)


To run it manually:


.. code-block:: bash

   sudo -H -u www-data tmp/ve/bin/python ./src/manage.py shell


.. code-block:: text

   In [1]: from core.tasks import project_update
   In [2]: project_update("ef49782ef60d75b2a66f29ea236912a54c09a305")


Migrations
----------

.. code-block:: bash

   django.db.migrations.exceptions.InconsistentMigrationHistory:
   Migration core.0001_initial is applied before its dependency auth.0001_initial on database 'default'.

   select earliest from django_migrations;

.. code-block:: bash

   INSERT INTO django_migrations (app, name, applied) VALUES ('auth', '0001_initial', '2016-11-01 12:00:00');


What next?
==========

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   static
   long-running-tasks
   tests
   algo
   mailserver
   auth
   cache
   maildb-sql


.. _core/tasks.py: https://github.com/pashinin-com/pashinin.com/blob/master/src/core/tasks.py
.. _travis_secret_settings: https://github.com/pashinin-com/pashinin.com/blob/master/configs/settings.py.mustache#L334
.. _travis.yml: https://github.com/pashinin-com/pashinin.com/blob/master/.travis.yml#L105-L106
.. _Docker: https://www.docker.com/
.. _Linux: https://www.ubuntu.com/
.. _Github: https://github.com
