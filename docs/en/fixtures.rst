Fixtures
========

Fixtures are example records that are inserted into a database.


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


.. _django-guardian: https://github.com/django-guardian/django-guardian
.. _django-rules: https://github.com/dfunckt/django-rules
