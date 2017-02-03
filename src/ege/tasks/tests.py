# import pytest
from . import process_sections


# @pytest.mark.django_db
def test_fipi_get(settings):
    process_sections([])
    # from .update import project_update
    # settings.CELERY_ALWAYS_EAGER = True
    # result = project_update.delay('123456')
    # assert result.successful()
