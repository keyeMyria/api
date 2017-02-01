import pytest


@pytest.mark.django_db
def test_get_runs_one(settings):
    from .update import project_update
    # settings.CELERY_ALWAYS_EAGER = True
    result = project_update.delay('123456')
    assert result.successful()
