import pytest
from . import (
    process_sections,
    ege_subjects_and_urls,
    create_subjects
)


@pytest.mark.skip(reason='for now')
@pytest.mark.django_db
def test_get_subjects():
    subject_and_urls = ege_subjects_and_urls()
    assert len(subject_and_urls) == 15


# @pytest.mark.django_db
@pytest.mark.skip(reason='for now')
def test_fipi_get():
    process_sections([])
    # from .update import project_update
    # settings.CELERY_ALWAYS_EAGER = True
    # result = project_update.delay('123456')
    # assert result.successful()


@pytest.mark.django_db
def test_create_subjects():
    create_subjects('Информатика')
    # TODO: test record slug
