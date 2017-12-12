import pytest


# @pytest.mark.urls('ege.urls')
@pytest.mark.host('ege')
def test_urls_as_admin(admin_client, settings):
    urls = [
        # '/'
    ]
    for url in urls:
        r = admin_client.get(url)
        assert r.status_code == 200

        # This is only in root domain, but we are testing ege.example.org here
        assert 'Программы на заказ' not in r.content.decode('utf8')

    # admin user is already logged in,
    # so /login url must redirect
    r = admin_client.get(settings.LOGIN_URL)
    assert r.status_code == 302


# @pytest.mark.skip(reason='not published yet')
@pytest.mark.host('ege')
def test_urls_as_anon(admin_client, settings, db):
    urls = [
        '/',
        # settings.LOGIN_URL,
        # '/subject-name/2017/'
        '/2017',
    ]

    from ege.models import Subject, Exam
    # from core import now
    assert Subject.objects.filter().count() == 0
    subject = Subject.objects.create(
        slug='subject-name',
        name='Subject',
        published=True,
    )
    Exam.objects.create(
        year=2017,
        subject=subject,
        published=True,
    )
    assert Subject.objects.filter().count() > 0
    assert Exam.objects.filter().count() > 0

    for url in urls:
        r = admin_client.get(url)
        # print(r.content)
        assert r.status_code == 200
