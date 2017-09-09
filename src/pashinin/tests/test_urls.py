import pytest
from subprocess import Popen, PIPE


# alpine /etc/apk/repositories
@pytest.mark.skip(reason='alpine 3.4 is used, tidy is in 3.5')
@pytest.mark.urls('pashinin.urls')
def test_urls_tidy(admin_client):
    urls = ['/', '/contacts', '/faq', '/articles/']
    for url in urls:
        r = admin_client.get(url)
        # p1 = Popen(cmd1, stdout=PIPE)
        p = Popen(
            ['tidy', '-config', 'configs/tidy.conf'],
            stdin=PIPE,
            stdout=PIPE
        )
        # p.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
        output, err = p.communicate(input=r.content)
        assert p.returncode == 0


@pytest.mark.urls('pashinin.urls')
def test_urls_as_admin(admin_client):
    urls = ['/', '/contacts', '/faq', '/articles/']
    urls += [
        '/_/celery', '/_/nginx', '/_/updates',
        # '/_/django/corefiles/basefile/'
        '/students'
    ]
    for url in urls:
        r = admin_client.get(url)
        assert r.status_code == 200


@pytest.mark.urls('pashinin.urls')
def test_urls_as_anon(client, db):
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
    from core.models import User
    u = User.objects.filter()[0]
    assert User.objects.all().count() == 1
    assert u.email == 'admin@example.org'
    # assert u.is_superuser

    # try to log in again
    r = admin_client.post(settings.LOGIN_URL, {
        # these credentials are defined in /conftest.py file.
        # not any fixtures!
        'username': 'admin@example.org', 'password': 'password'
    })
    assert r.json() == {'code': 0}
    assert r.status_code == 200

    # non-existent user must fail
    r = admin_client.post(settings.LOGIN_URL, {
        'username': 'admin2', 'password': 'password2'
    })
    assert 'errors' in r.json()
    assert r.status_code == 200

    # Logged in admin should have access to Updates page
    r = admin_client.get('/_/updates')
    assert r.status_code == 200


@pytest.mark.urls('pashinin.urls')
def test_enroll_from_main_page(client, db):
    r = client.post('/', {
        'name': 'admin',
        'phone': '12345',
        'message': 'comment'
    })
    assert r.json() == {'code': 0}
    assert r.status_code == 200

    # should fail (no contact field)
    r = client.post('/', {
        'name': 'admin',
        'message': 'comment'
    })
    assert 'errors' in r.json()
    assert r.status_code == 200


@pytest.mark.urls('pashinin.urls')
def test_StudentsView_some_lessons(admin_client, db):
    from pashinin.models import Lesson
    from core import now
    assert Lesson.objects.filter().count() == 0
    Lesson.objects.create(
        status=0,
        start=now(),
        end=now()
    )
    assert Lesson.objects.filter().count() > 0
    r = admin_client.get('/students')
    assert r.status_code == 200
