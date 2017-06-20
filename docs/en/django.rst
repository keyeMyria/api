Django
======

Shell
-----

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


ORM tree models (django-mptt)
-----------------------------

See another project: https://github.com/django-treebeard/django-treebeard

When converting a model to a tree (while making a migration) set
:code:`level`, :code:`lft` and :code:`rght` to :code:`0`.

Then run :code:`manage.py shell` and run:

.. code-block:: bash

   Model.objects.rebuild()



Migrations
----------

.. code-block:: bash

   django.db.migrations.exceptions.InconsistentMigrationHistory:
   Migration core.0001_initial is applied before its dependency auth.0001_initial on database 'default'.

   select earliest from django_migrations;

.. code-block:: bash

   INSERT INTO django_migrations (app, name, applied) VALUES ('auth', '0001_initial', '2016-11-01 12:00:00');



.. _django-guardian: https://github.com/django-guardian/django-guardian
.. _django-rules: https://github.com/dfunckt/django-rules
