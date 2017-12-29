import os
import json


def create_config(*args):
    return '\n'.join(args)


def render_config(filename, **kwargs):
    """
    Output filename is the same without .ext part:

    filename - a filename in /configs/ dir without "systemd-" prefix.

    Example:
      render_config('worker.service.jinja')

    """
    from core import get_git_root
    repo = get_git_root()
    filename_full = os.path.join(
        repo,
        'configs',
        'systemd-'+filename
    )

    data = json.load(open(os.path.join(
        repo,
        'configs',
        'tmp',
        'conf.json'
    )))
    data.update(kwargs)
    # print(data)
    from jinja2 import Environment
    with open(filename_full, 'r') as f:
        try:
            return Environment().from_string(f.read()).render(**data)
        except Exception:
            print('FAILED rendering: ', filename)
            raise


def test(**kwargs):
    print(render_config('worker.service.jinja', **kwargs))
