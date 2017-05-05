Auth
====

For Single Sing On (SSO) on **different domains** (not subdomains) use CAS.

CAS - https://wiki.jasig.org/display/CAS/Home

pip install django-mama-cas

When using **subdomains only** it's enough to just set 2 variables:

.. code-block:: python

   # Auth once on all subdomains
   SESSION_COOKIE_DOMAIN = '.'+DOMAIN   # dot! + domain
   SESSION_COOKIE_NAME = 'session'





Permissions
-----------

https://djangopackages.org/grids/g/perms/

django-guardian_ vs django-rules_.




.. _django-guardian: https://github.com/django-guardian/django-guardian
.. _django-rules: https://github.com/dfunckt/django-rules
