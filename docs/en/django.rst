Django
******

Default admin user/password:

.. code-block:: text

   admin@example.org
   admin



Shell
=====

To enter Django shell (:code:`shell_plus` actually) enter:

.. code-block:: bash

   make shell

.. code-block:: bash

   <a lot of imports>
   ...
   Python 3.6.1 (default, Jun 17 2017, 06:29:46)
   Type 'copyright', 'credits' or 'license' for more information
   IPython 6.1.0 -- An enhanced Interactive Python. Type '?' for help.

   In [1]:


ORM tree models
===============

.. note::

   django-mptt or `django-treebeard
   <https://github.com/django-treebeard/django-treebeard>`_?

   django-treebeard can do more but django-mptt has a nicer API and better docs


When converting a model to a tree (while making a migration) set
:code:`level`, :code:`lft` and :code:`rght` to :code:`0`.

Then run :code:`manage.py shell` and run:

.. code-block:: bash

   Model.objects.rebuild()



Migrations
==========

.. code-block:: bash

   django.db.migrations.exceptions.InconsistentMigrationHistory:
   Migration core.0001_initial is applied before its dependency auth.0001_initial on database 'default'.

   select earliest from django_migrations;

.. code-block:: bash

   INSERT INTO django_migrations (app, name, applied) VALUES ('auth', '0001_initial', '2016-11-01 12:00:00');


Fixtures
========

Fixtures are example records that are inserted into a database.

.. warning::

   Fixtures may cause pain.

`factory_boy <https://github.com/FactoryBoy/factory_boy>`_ is a fixtures
replacement.


Create fixture
--------------

Go to or create `src/<app>/fixtures/<any_filename>.json`

.. code-block:: json

   [
       {
           "model": "articles.article",
           "pk": 1,
           "fields": {
               "title": "Introduction to Latex",
               "src": "https://www.youtube.com/watch?v=g6ez7sbaiWc",
               "added": "2016-10-30T13:19:37+00:00",
               "changed": "2016-10-30T13:19:37+00:00"
           }
       }
   ]


Load fixture
------------

Run :code:`make shell` and then:

.. code-block:: python

   call_command('loaddata', 'initial_data.json')

.. note::

   Some fixtures are loaded automatically when you start :code:`db`
   container. (See :code:`docker/db_init.sh` file)

..
   manage.py loaddata --settings=pashinin.settings initial_data.json


Model (objects) history
=======================

.. note::

   Need this for article history or any other object history.


`django-reversion <https://django-reversion.readthedocs.io/en/stable/commands.html>`_


Permissions
===========

.. warning::

   Using permissions in a database is kinda slow. Django default
   permission system is kinda shit (uses database, doesn't have
   row-level permissions).

django-guardian uses DB. django-rules uses functions (all in memory).

Rules will search for rules.py in each app when added autodiscover in
settings.py:

.. code-block:: python

   INSTALLED_APPS = (
       # ...
       'rules.apps.AutodiscoverRulesConfig',
   )


For a model set :code:`default_permissions` to empty tuple:

.. code-block:: python

   class UpToDateFile(AddedChanged):
       basename = models.CharField(max_length=200, blank=True, null=True)
       current_file = models.ForeignKey(File)
       # groups = models.ManyToManyField(Group)

       class Meta:
           default_permissions = ()  # Defaults to ('add', 'change', 'delete')




.. _django-guardian: https://github.com/django-guardian/django-guardian
.. _django-rules: https://github.com/dfunckt/django-rules
