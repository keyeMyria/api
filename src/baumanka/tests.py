import pytest


# @pytest.mark.xfail(reason='no files')
@pytest.mark.urls('baumanka.urls')
def test_baumanka_urls(client, db, settings):
    good = [
        # '/',

        # '/contacts',
        # '/faq',
        # '/articles/'
    ]
    bad = [
        # '/IU2/',  # there are no files -> 404
        # '/IU2/sem1',  # there are no files -> 404
    ]
    # urls += [
    #     '/_/celery', '/_/nginx', '/_/updates',
    #     # '/_/django/corefiles/basefile/'
    #     '/students'
    # ]
    for url in good:
        r = client.get(url)
        # assert r.content == ''
        assert r.status_code == 200

    for url in bad:
        r = client.get(url)
        # assert r.content == ''
        assert r.status_code == 404
