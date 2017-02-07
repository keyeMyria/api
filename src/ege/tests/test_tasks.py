import pytest
from core.tasks import get
from ..tasks import (
    fipi_bank_root_url,
    process_sections,
    ege_subjects_and_urls,
    get_subject_sections,
    # create_subjects
)


# @pytest.mark.skip(reason='for now')
@pytest.mark.django_db
def test_get_subjects():
    html, info = get(fipi_bank_root_url)
    assert info['cached']
    subject_and_urls = ege_subjects_and_urls()
    assert len(subject_and_urls) == 15

    # Start from "openlogin.php"
    # Then redirects to -> index.php
    url_start = 'http://85.142.162.119/os11/xmodules/qprint/openlogin.php'
    for subj, url in subject_and_urls:
        assert url.startswith(url_start)


# @pytest.mark.django_db
# @pytest.mark.skip(reason='for now')
def test_get_subj_sections():
    # sha1 = 495af68e22c84a528901d6cb44de8e3a98f5af0c
    russian_lng_url = 'http://85.142.162.119/os11/xmodules/qprint/' +\
                      'index.php?proj=AF0ED3F2557F8FFC4C06F80B6803FD26'

    html, info = get(russian_lng_url)
    assert info['cached']

    # В "Русском языке" 11 разделов
    res = get_subject_sections(russian_lng_url)
    assert len(res) == 11


def test_process_sections(settings):
    settings.CELERY_ALWAYS_EAGER = True
    # process_sections([
    #     # ('русский язык', 'http://85.142.162.119/os11/xmodules/qprint/' +
    #     #  'openlogin.php?proj=AF0ED3F2557F8FFC4C06F80B6803FD26')
    # ])
    sections = [
        ('Средства ИКТ', 'http://85.142.162.119/os11/xmodules/qprint/' +
         'index.php?theme_guid=9009f55c9341e311beed001fc68344c9&proj_guid' +
         '=B9ACA5BBB2E19E434CD6BEC25284C67F')
    ]
    for title, url in sections:
        html, info = get(url)
        assert info['cached']

    result = process_sections.delay(sections)
    assert result.successful()

    result = process_sections.delay(None)
    assert result.successful()


# разделы по предмету
# http://85.142.162.119/os11/xmodules/qprint/index.php?proj=B9ACA5BBB2E19E434CD6BEC25284C67F


# Средства ИКТ - первая страница с задачами
# fef2594a33094cb79f4765972a56f02412ce736d
# http://85.142.162.119/os11/xmodules/qprint/index.php?theme_guid=9009f55c9341e311beed001fc68344c9&proj_guid=B9ACA5BBB2E19E434CD6BEC25284C67F
