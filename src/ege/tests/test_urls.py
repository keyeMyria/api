import pytest


@pytest.mark.urls('ege.urls')
def test_urls_as_admin(admin_client, settings):
    urls = ['/']
    for url in urls:
        r = admin_client.get(url)
        assert r.status_code == 200

    # admin user is already logged in,
    # so /login url must redirect
    r = admin_client.get(settings.LOGIN_URL)
    assert r.status_code == 302


# @pytest.mark.skip(reason='not published yet')
@pytest.mark.urls('ege.urls')
def test_urls_as_anon(client, settings, db):
    urls = ['/', settings.LOGIN_URL]
    for url in urls:
        r = client.get(url)
        assert r.status_code == 200
