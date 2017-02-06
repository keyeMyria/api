import pytest


@pytest.mark.urls('pashinin.urls')
def test_urls_as_admin(admin_client):
    urls = ['/', '/contacts', '/faq', '/articles/']
    urls += ['/_/celery', '/_/nginx', '/_/updates']
    for url in urls:
        r = admin_client.get(url)
        assert r.status_code == 200

    # admin user is already logged in,
    # so /login url must redirect
    r = admin_client.get('/login')
    assert r.status_code == 302


@pytest.mark.urls('pashinin.urls')
def test_urls_as_anon(client):
    urls = ['/', '/contacts', '/faq', '/login', '/baumanka/']
    for url in urls:
        r = client.get(url)
        assert r.status_code == 200
