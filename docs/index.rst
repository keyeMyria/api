.. pashinin.com documentation master file, created by
   sphinx-quickstart on Mon Dec 26 16:56:52 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pashinin.com
============

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   static
   long-running-tasks
   tests


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



.. _core/tasks.py: https://github.com/pashinin-com/pashinin.com/blob/master/src/core/tasks.py
.. _travis_secret_settings: https://github.com/pashinin-com/pashinin.com/blob/master/configs/settings.py.mustache#L334
.. _travis.yml: https://github.com/pashinin-com/pashinin.com/blob/master/.travis.yml#L105-L106
