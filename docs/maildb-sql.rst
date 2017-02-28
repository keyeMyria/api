Mail server DB tables
=====================

.. code-block:: sql

   CREATE TABLE users (
       username VARCHAR(128) NOT NULL,
       domain VARCHAR(128) NOT NULL,
       password VARCHAR(64) NOT NULL,
       home VARCHAR(255) NOT NULL,
       uid INTEGER NOT NULL,
       gid INTEGER NOT NULL,
       active CHAR(1) DEFAULT 'Y' NOT NULL
   );
