Long running tasks
==================

Celery: Distributed Task Queue
------------------------------

A "heavy" way to run long-running tasks.

Any Django project (including this one) can have `tasks.py` file in apps
(ex. `core/tasks.py`). There are Celery tasks that

.. code-block:: bash

   make shell

.. code-block:: python

   In [1]: from ege.tasks import ege_subjects_and_urls
   In [2]: ege_subjects_and_urls()


Django Channels
---------------

Another way (simple and fast) to run long-running tasks, but no
guarantee if failed.


.. _core/tasks.py: https://github.com/pashinin-com/pashinin.com/blob/master/src/core/tasks.py
