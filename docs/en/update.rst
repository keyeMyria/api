Update process
==============

Commit -> Github -> Travis

When travis build is OK Travis sends info to a webhook (see
travis.yml_). The hook URL is:


.. code-block:: text

   https://pashinin.com/_hooks/travis


Request is signed - so there is `a way
<https://docs.travis-ci.com/user/notifications#Verifying-Webhook-requests>`_
to check it is really Travis connecting to us.

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
