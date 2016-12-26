Install first:

```bash
sudo pip install Sphinx -U
```

Then in your docs dir:

```bash
sphinx-quickstart
...
...

make html
```


Add in conf.py:

```python
import os
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

...

html_theme_path = []
if not on_rtd:  # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
```
