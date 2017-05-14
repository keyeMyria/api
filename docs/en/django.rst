Django
======

ORM tree models (django-mptt)
-----------------------------

See another project: https://github.com/django-treebeard/django-treebeard

When converting a model to a tree (creating a migration) set `level`, 'lft' and 'rght' to 0.

Then enter 'manage.py shell' and run

Model.objects.rebuild()


.. _django-guardian: https://github.com/django-guardian/django-guardian
.. _django-rules: https://github.com/dfunckt/django-rules
