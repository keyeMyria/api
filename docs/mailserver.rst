Mail server
===========

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Using Postfix, Dovecot.

Probably add a subdomain (like mail.example.org). Bind zones are here:

.. code-block:: text

   /etc/bind/example.org.zone

   ...
   mail  	        IN	A	10.254.239.1
   ...


SSL
---



DKIM
----

DKIM is not about encrypting messages. This is ensuring that message
(which tells it is from example.org) indeed is from example.org.

So we need a key associated with a domain and a signaute of each email
using this key.



SQL configuration
-----------------

dovecot-sql.conf - in this file we say Dovecot

.. code-block:: conf

   driver = pgsql
   connect = host=127.0.0.1 dbname=postfix user=<USER> password=<PASSWORD>
   default_pass_scheme = MD5-CRYPT
   password_query = SELECT username, domain, password FROM mailbox WHERE username = '%u' AND active = TRUE
   user_query = SELECT '/home/vmail/%d/%n' AS home, 'vmail' AS uid, 'vmail' AS gid FROM mailbox where username = '%u' AND active = TRUE


Password schemes: http://wiki2.dovecot.org/Authentication/PasswordSchemes

MD5-CRYPT: A weak but common scheme often used in /etc/shadow. The
encrypted password will start with $1$

.. code-block:: conf

    %u = entire user@domain
    %n = user part of user@domain (user)
    %d = domain part of user@domain  (domain)

Commonly used available substitutions (see
http://wiki2.dovecot.org/Variables for full list):


Add a mailbox
-------------

1. Generate a password with MD5-CRYPT (why MD5-CRYPT? where did I see
   this shit? PostfixAdmin?). A command below.
2. Run SQL code to insert a new mailbox to a database.



To generate password:

.. code-block:: bash

   doveadm pw -s SHA512-CRYPT
   Enter new password:        "123"
   Retype new password:
   {SHA512-CRYPT}$6$p1KVWudMvHMpqRbR$Jj9lmMXexNe1.XxI0RiNOg8rp/AdZ/0xlz4BpNziYVBQyDWruJMpVe5l5jRSdUHhEQdRcT0uDRa4mmRjc63MQ.

   doveadm pw -s MD5-CRYPT
   Enter new password:        "123"
   Retype new password:
   {MD5-CRYPT}$1$DMy.uluE$QX37sT2rsmSX/U6vYHGf/.


.. code-block:: sql

   INSERT INTO mailbox (username, password, maildir, domain, local_part) VALUES ('user@example.org', '$1$DMy.uluE$QX37sT2rsmSX/U6vYHGf/.', 'user@example.org/', 'example.org', 'user');


Remove mailbox
--------------

Just DELETE from a database table:

.. code-block:: sql

   DELETE from mailbox WHERE username='';


Sieve
-----

Sieve is a language for filtering e-mail messages (antispam
actions).

Create sieve file:

.. code-block:: bash

   mkdir -p /etc/dovecot/sieve
   touch /etc/dovecot/sieve/default.sieve

   # important!
   chown -R vmail /etc/dovecot/sieve

.. code-block:: bash

   require "fileinto";
   if header :contains "X-Spam-Flag" "YES" {
       fileinto "Junk";
   }

Dovecot mailboxes.conf:


.. code-block:: conf

   mailbox Junk {
     special_use = \Junk
     # auto = create
     auto = subscribe
   }

Dovecot lda.conf:


.. code-block:: conf

   protocol lda {
        postmaster_address = postmaster

        # default - commented:
        # mail_plugins = sieve
        mail_plugins = $mail_plugins sieve

        quota_full_tempfail = yes
        deliver_log_format = msgid=%m: %$
        rejection_reason = Your message to <%t> was automatically rejected:%n%r
   }


Edit /etc/dovecot/conf.d/90-sieve.conf:

.. code-block:: conf

   # point to your sieve config
   plugin {

      sieve = /etc/dovecot/sieve/default.sieve


http://sieve.info/
