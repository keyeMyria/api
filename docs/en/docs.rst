Documentation
*************

Documentation is written in ReStructured (.rst) format in 2 languages: english and russian.

.. note::

   RST format is used in many projects of different size. So this is
   really worth learning. Official help on .rst fromat is `here
   <http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html>`_.

To compile docs from .rst format to HTML install Sphinx, enter directory
with docs and run :code:`make html`:

.. code-block:: bash

   # install Sphinx
   sudo pip install sphinx sphinx_rtd_theme

   # compile docs to HTML
   cd docs/en
   make html

   Running Sphinx v1.6.3
   loading translations [en]... done
   loading pickled environment... done
   building [mo]: targets for 0 po files that are out of date
   building [html]: targets for 0 source files that are out of date
   updating environment: 0 added, 0 changed, 0 removed
   looking for now-outdated files... none found
   no targets are out of date.
   build succeeded.

   Build finished. The HTML pages are in _build/html.


Then open :code:`/docs/en/_build/html/index.html`
