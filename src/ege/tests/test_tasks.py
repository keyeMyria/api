import lxml
import pytest
from core.tasks import get
from edu.models import Task
from ..tasks import (
    fipi_bank_root_url,
    process_sections,
    ege_subjects_and_urls,
    get_subject_sections,
    extract_tasks_from_url,
    process_tasks,
    tag_contents
    # create_subjects
)


# Средства ИКТ - первая страница с задачами
# fef2594a33094cb79f4765972a56f02412ce736d
url_ikt_first_page = 'http://85.142.162.119/os11/xmodules/qprint/index.php' +\
                     '?theme_guid=9009f55c9341e311beed001fc68344c9&' + \
                     'proj_guid=B9ACA5BBB2E19E434CD6BEC25284C67F'


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


def test_process_sections(settings, db):
    settings.CELERY_ALWAYS_EAGER = True
    # process_sections([
    #     # ('русский язык', 'http://85.142.162.119/os11/xmodules/qprint/' +
    #     #  'openlogin.php?proj=AF0ED3F2557F8FFC4C06F80B6803FD26')
    # ])
    sections = [
        ('Средства ИКТ', url_ikt_first_page)
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


def test_extract_tasks_from_url():
    """Извлечение задач со страницы.

    На 1 странице расположено 10 форм. В каждой - таблица с содержанием
    задачи. В форме также есть скрытое поле - GUID задачи.

    """
    html, info = get(url_ikt_first_page)
    assert info['cached']

    import lxml
    from lxml.cssselect import CSSSelector as S
    tree = lxml.html.fromstring(html)
    forms = S('form[name="checkform"]')(tree)

    # 10 задач на странице
    assert len(forms) == 10

    tasks = extract_tasks_from_url(url_ikt_first_page)
    # Должно совпадать - 10 задач из 10 форм
    assert len(tasks) == 10

    for guid, text in tasks:
        # guid должен быть строкой
        assert len(guid) > 10
        assert len(text) > 10
        assert isinstance(guid, str)


@pytest.mark.django_db
def test_process_tasks(settings):
    tasks = extract_tasks_from_url(url_ikt_first_page)
    settings.CELERY_ALWAYS_EAGER = True

    result = process_tasks.delay(tasks)
    assert result.successful()
    assert result.info == 10  # return value

    # There should be 10 added tasks by now
    tasks = Task.objects.filter()
    assert tasks.count() == 10

    # process old tasks
    # set 1 as old and see how many processed
    task = tasks.filter(text__icontains='Степаненко')[0]
    assert task.debug['v'] >= 2
    task.debug['v'] = 0
    task.save()
    result = process_tasks.delay()
    assert result.successful()
    assert result.info == 1

    task.refresh_from_db()
    # print(task.text)

    assert task.text != task.debug['html']
    # print(task.debug['html'])
    # assert task.text == ''

    # all done already
    result = process_tasks.delay()
    assert result.successful()
    assert result.info == 0


def test_html():
    html = """<p>p1<p> <table><tr><td>1</td></tr>
<tr><td>2 <b>b</b></td></tr>
</table> p2
"""
    tree = lxml.html.fromstring(html)
    # for el in tree.xpath("child::node()"):
    print(tag_contents(tree))

    # assert False
    # for el in tree:
    # for el in tag.iterdescendants("*"):
    # res.append(tag_to_text(el))
    # return tag_contents(tree)
