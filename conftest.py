import os
import pytest
import codecs


# def pytest_addoption(parser):
#     parser.addoption("-E", action="store", metavar="NAME",
#         help="only run tests matching the environment NAME.")

# def pytest_configure(config):
#     # register an additional marker
#     config.addinivalue_line("markers",
#         "env(name): mark test to run only on named environment")

def pytest_runtest_setup(item):
    ci = item.get_marker("ci")
    if ci is not None:
        if os.getenv('CI', '') != 'true':
            pytest.skip('Run it on CI system only')

    # app = item.get_marker("app")
    # if app is not None:
    #     dsm = os.getenv('DJANGO_SETTINGS_MODULE', '').split('.')[0]
    #     print(item)
    #     if dsm != 'true':
    #         pytest.skip('Run it on CI system only')
        # envname = envmarker.args[0]
        # if envname != item.config.getoption("-E"):
        #     pytest.skip("test requires env %r" % envname)


@pytest.fixture()
def admin_user(db, django_user_model, django_username_field):
    """A Django admin user.
    This uses an existing user with username "admin", or creates a new one with
    password "password".
    """
    UserModel = django_user_model
    username_field = django_username_field

    try:
        user = UserModel._default_manager.get(**{username_field: 'admin@example.org'})
    except UserModel.DoesNotExist:
        extra_fields = {}
        if username_field != 'username' and username_field != 'email':
            extra_fields[username_field] = 'admin'
        user = UserModel._default_manager.create_superuser(
            'admin@example.org', 'admin', 'password', **extra_fields)
        return user


@pytest.fixture()
def admin_client(db, admin_user):
    """A Django test client logged in as an admin user."""
    from django.test.client import Client

    client = Client()
    client.login(username=admin_user.email, password='password')
    return client


@pytest.fixture(autouse=True)
def django_cache(request, settings):
    """A Django test client logged in as an admin user."""
    from django.core.cache import cache
    from core.tasks import url_get_version
    cache.clear()
    d = os.path.dirname(str(request.fspath))
    assets = os.path.join(d, 'assets')
    if os.path.isdir(assets):
        for f in os.listdir(assets):
            filename = os.path.join(assets, f)
            if f.startswith('url_'):
                basename, ext = os.path.splitext(f)
                sha1 = basename.split('_')[1]
                key = 'url.get_'+sha1
                try:
                    with codecs.open(filename, 'r', 'utf-8') as f:
                        html = f.read()
                        # html = open(filename, 'r').read()
                except:
                    with codecs.open(filename, 'r', 'cp1251') as f:
                        html = f.read()

                cache.set(
                    key,
                    html,
                    version=url_get_version
                )
    # print(request.function.__name__)
    # print(request.fspath)
    return cache
