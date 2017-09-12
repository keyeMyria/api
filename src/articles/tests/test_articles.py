# import pytest
from .factories import ArticleFactory


# @pytest.mark.host('ege')
def test_urls_as_admin(admin_client, settings):
    r = admin_client.get('/articles/0/non-existent')
    assert r.status_code == 404

    a = ArticleFactory()
    assert a.revision_count == 0

    # redirect to the correct slug
    r = admin_client.get('/articles/{}/asd'.format(a.id))
    assert r.status_code == 302

    # ok
    r = admin_client.get('/articles/{}/{}'.format(a.id, a.slug))
    assert r.status_code == 200
