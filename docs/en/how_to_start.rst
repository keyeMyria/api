How to start
************

Linux
=====

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


Windows
=======

.. warning::

   Docker for Windows runs on 64bit Windows 10 Pro, Enterprise and
   Education (1511 November update, Build 10586 or later). `And
   more... <https://docs.docker.com/docker-for-windows/install/#what-to-know-before-you-install>`_


Windows 10 64bit Pro or Enterprise
----------------------------------

#. Install following programs:
   Git, Git LFS, Github Desktop, Node, `Docker for Windows <https://store.docker.com/editions/community/docker-ce-desktop-windows?tab=description>`_
#. Run setup.exe.
#. In your browser go to http://example.org or http://localhost.

Windows 7
---------

Install `Docker Toolbox <https://www.docker.com/products/docker-toolbox>`_


Mac
===

Install Docker.
