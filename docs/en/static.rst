Javascript, CSS
===============

All common static files like javascript libraries are located under
`core/static`.

To minify a javascript file (fetch.js_ for example) use uglifyjs_:

.. code-block:: bash

   uglifyjs [input files] [options]

   uglifyjs -V
   uglify-js 2.4.20

   uglifyjs fetch.js > fetch2.0.2.min.js


Javascript libraries
--------------------

* Dropzone_ - file uploads, `core/static/dropzone/`

.. _dropzone: https://github.com/enyo/dropzone
.. _fetch.js: https://github.com/github/fetch
.. _uglifyjs: https://github.com/mishoo/UglifyJS2
