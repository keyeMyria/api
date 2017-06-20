How to start (Linux)
====================

Clone your new repo (replace :code:`<YOUR_NAME>` with your Github login):

.. code-block:: bash

   git clone git@github.com:<YOUR_NAME>/pashinin.com.git
   cd pashinin.com
   make         # start Docker images

In your browser go to http://example.org or http://localhost.


.. note::

   If you want to see an output of a Django debug server or Gulp process - attach to a
   container:

   .. code-block:: bash

      docker attach django   # see Django debug server output
      docker attach gulp     # see gulp process
