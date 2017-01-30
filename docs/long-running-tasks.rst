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

   In [1]: from ege.tasks import get_inf

   In [2]: t = get_inf.delay()
   Out[2]: t = <AsyncResult: 63b5705e-bf52-41d8-b9e4-930471a2738b>

   In [3]: t.state
   Out[3]: 'PENDING'

   In [4]: t.ready()
   Out[4]: False


Django Channels
---------------

Another way (simple and fast) to run long-running tasks, but no
guarantee if failed.


.. _core/tasks.py: https://github.com/pashinin-com/pashinin.com/blob/master/src/core/tasks.py
