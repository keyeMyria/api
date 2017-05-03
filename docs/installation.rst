Development process
###################

#. Register at Github_ and fork `my repository <https://github.com/pashinin-com/pashinin.com>`_.
#. Clone your new repo
#. Do changes
#. Make a pull request

`Docker`_ is used for containers.



Linux
-----

.. code-block:: bash

   # Read only (my repo):
   # git clone https://github.com/pashinin-com/pashinin.com.git

   # Write access (your repo)
   git clone git@github.com:<YOUR_NAME>/pashinin.com.git

   make         # start Docker images
   make tmux    # start Django server and Gulp

In your browser go to `http://example.org` or `http://localhost`.


Tmux
^^^^




Windows
-------

.. warning::

   Using Windows may lead to a suicide. Using Mac can cause gay population growth.

.. note::

   Docker for Windows runs on 64bit Windows 10 Pro, Enterprise and
   Education (1511 November update, Build 10586 or later). `And
   more... <https://docs.docker.com/docker-for-windows/install/#what-to-know-before-you-install>`_


.. _Docker: https://www.docker.com/
.. _Linux: https://www.ubuntu.com/
.. _Github: https://github.com
