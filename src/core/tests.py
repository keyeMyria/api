import os
import functools
import pytest
from unittest import TestCase


@pytest.fixture(autouse=True)
def ci(request):
    if os.getenv('CI', '') != 'true':
        pytest.skip('Run it on CI system only')


def travis(func):
    """Decorator to run a function only if we are in Travis.

    @travis
    def func1():
        pass

    func1()  # will run only if in Travis build
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        res = None
        if os.getenv('CI', '') == 'true':
            res = func(*args, **kwargs)
        return res
    return wrapper


def test_with_client(client):
    response = client.get('/')
    assert response.status_code == 200
