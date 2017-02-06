# import pytest
# from django.core.cache import cache as dc


# not_travis = os.getenv('CI', '') != 'true'

# @pytest.mark.django_db

# @pytest.mark.
def test_get_url(cache, django_cache):
    # is cache and Django cahce the same?
    assert django_cache.get('key', None) is None
    django_cache.set('key', 1) == 1
    assert django_cache.get('key', None) == 1

    from core.tasks import get
    html, info = get("https://google.com")
    assert info['cached']
    # assert False
    # assert dc.get('key', None) == 1

    #
    # html, info = get("https://google.com")
    # print(html, info)
    # assert html is not None
    # assert info['cached']
