Testing
=======

I use `Travis <https://travis-ci.org/>`_ for automatic testing. All
things that Travis does are described in :code:`/.travis.yml` file.

Use pytest_. `pytest-django`_ is a plugin for pytest.

.. note::

   Test coverage helps to discover redundant code or code that is not
   tested. Current status:

   .. image:: https://coveralls.io/repos/github/pashinin-com/pashinin.com/badge.svg?branch=master
      :target: https://coveralls.io/github/pashinin-com/pashinin.com?branch=master


.. code-block:: python

   ...


.. _pytest: http://doc.pytest.org/en/latest/
.. _pytest-django: https://pytest-django.readthedocs.io/en/latest/
