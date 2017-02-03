import pytest


# not_travis = os.getenv('CI', '') != 'true'

# @pytest.mark.django_db
@pytest.mark.ci
def test_deploy_project(settings):
    from .update import project_update
    settings.CELERY_ALWAYS_EAGER = True
    project_update.delay('123456')
    # assert result.successful()


# @pytest.mark.ci
# def test_get_url():
#     from . import get
#     html, info = get("https://google.com")
#     print(html, info)
#     assert html is not None
#     assert False
