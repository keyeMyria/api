Authentication and Authorization
================================

Authentication
--------------

`JSON Web Tokens (JWT) <https://jwt.io>`_ are used for
authentication.

api/auth/jwt/ - obtain JWT here using POST request with payload: {email,
password}.

`django-rest-framework-jwt
<https://github.com/GetBlimp/django-rest-framework-jwt>`_ is responsible
for this (`docs
<http://getblimp.github.io/django-rest-framework-jwt/>`_). It relies on
https://pyjwt.readthedocs.io/en/latest/index.html

JWT is "bad" see https://paseto.io/


For Single Sing On (SSO) on **different domains** (not subdomains) use CAS.

CAS - https://wiki.jasig.org/display/CAS/Home

pip install django-mama-cas

When using **subdomains only** it's enough to just set 2 variables:

.. code-block:: python

   # Auth once on all subdomains
   SESSION_COOKIE_DOMAIN = '.'+DOMAIN   # dot! + domain
   SESSION_COOKIE_NAME = 'session'





Authorization (permissions)
---------------------------

https://djangopackages.org/grids/g/perms/

django-guardian_ vs django-rules_.




.. _django-guardian: https://github.com/django-guardian/django-guardian
.. _django-rules: https://github.com/dfunckt/django-rules
