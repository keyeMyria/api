## Docs

### Links

```
`Link text <http://example.com/>`_
```

```
txt Linux_ txt.


.. _Linux: https://www.ubuntu.com/
```

### Headers

Start from anyone, usually `=`.

```
Header 1 (parts)
################

Header 2 (chapters)
*******************

Header 3 (sections)
===================

Header 4 (subsections)
----------------------

Header 5 (subsubsections)
^^^^^^^^^^^^^^^^^^^^^^^^^

Header 6 (paragraphs)
"""""""""""""""""""""
```

## Installation of Sphinx

Install first:

```bash
sudo pip install Sphinx -U
```

Then in your docs dir:

```bash
sphinx-quickstart
...
... <answer some questions>
...

make html
```


RTD theme: https://github.com/snide/sphinx_rtd_theme

```python
# import os
# on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

...

# if not on_rtd:  # only import and set the theme if we're building docs locally
import sphinx_rtd_theme
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
```
