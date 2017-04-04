import pytest


@pytest.mark.urls('pashinin.urls')
def test_urls_as_admin(admin_client):
    urls = ['/', '/contacts', '/faq', '/articles/']
    urls += ['/_/celery', '/_/nginx', '/_/updates',
             '/_/django/corefiles/file/']
    for url in urls:
        r = admin_client.get(url)
        assert r.status_code == 200


@pytest.mark.urls('pashinin.urls')
def test_urls_as_anon(client):
    urls = ['/', '/contacts', '/faq']
    for url in urls:
        r = client.get(url)
        assert r.status_code == 200


@pytest.mark.urls('pashinin.urls')
def test_login_logout(admin_client, settings):
    # admin user is already logged in,
    # so login url must redirect
    r = admin_client.get(settings.LOGIN_URL)
    assert r.status_code == 302

    # logout
    r = admin_client.get('/_/logout')
    assert r.status_code == 302

    # admin_client.login(username='admin@example.com', password='password')

    # try to log in again
    r = admin_client.post(settings.LOGIN_URL, {
        'username': 'admin@example.com',
        'password': 'password'
    })
    assert r.json() == {'code': 0}
    assert r.status_code == 200

    r = admin_client.get('/_/updates')
    assert r.status_code == 200
