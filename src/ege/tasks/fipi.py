"""Открытый банк заданий ЕГЭ.

Parsing using Celery tasks.

"""
import time
import re
from celery import shared_task
from celery import chain
import logging
import lxml.html
from lxml.cssselect import CSSSelector as S
from ..models import Subject
from django.template.defaultfilters import slugify
from django.conf import settings
from unidecode import unidecode
from edu import subject_slug
from edu.models import Task
from raven.contrib.django.raven_compat.models import client
from lxml import etree  # noqa
from core.tasks import get
log = logging.getLogger(__name__)


fipi_bank_root_url = "http://www.fipi.ru/content/otkrytyy-bank-zadaniy-ege"


@shared_task
def ege_subjects_and_urls(*args):
    """Scans a root URL http://www.fipi.ru/content/otkrytyy-bank-zadaniy-ege

    Returns a list of pairs [(title.lower().capitalize(), url), ...]

    Example:

    >>> subjects_and_urls()
    >>> [('русский язык', 'http://85.142.162.119/os11/xmodules/...'), ...]

    """
    try:
        html, info = get(fipi_bank_root_url)
        tree = lxml.html.fromstring(html)
        links = S('div.content table a[href^="http://85."]')(tree)
        res = [(" ".join(el.text_content().split()).lower().capitalize(),
                el.get('href'))
               for el in links]

        subjects = (title for title, url in res)
        create_subjects(*subjects)
        # TODO: message if len(res) <> 15  (15 now)
        return res
    except:
        client.captureException()
        return []


@shared_task
def create_subjects(*args):
    try:
        for title in args:
            slug = subject_slug.get(
                title,
                slugify(unidecode(title))
            )
            subject, created = Subject.objects.get_or_create(
                name=title,
                slug=slug
            )
    except:
        client.captureException()


# russian:
# http://85.142.162.119/os11/xmodules/qprint/index.php?proj=AF0ED3F2557F8FFC4C06F80B6803FD26
#
# IT:
# http://85.142.162.119/os11/xmodules/qprint/index.php?proj=B9ACA5BBB2E19E434CD6BEC25284C67F
@shared_task(bind=True)
def get_subject_sections(self, subject_url, *args):
    """Получить разделы по предмету вместе с ссылками

    Для предмета "Информатика":

    [('Информация и информационные процессы',
    'http://85.142.162.119/.../qsearch.php?theme_guid=...&proj_guid=...'),
    ('Информационная деятельность человека',
    'http://85.142.162.119/...'), ...]

    """
    try:
        log.debug("getting sections...")
        html, info = get(subject_url)
        if len(html) < 100:
            raise ValueError("almost no html")
        tree = lxml.html.fromstring(html)
        links = S('td.coursebody a[href^="qsearch.php"]')(tree)
        res = [(" ".join(el.text_content().split()).lower().capitalize(),
                "http://85.142.162.119/os11/xmodules/qprint/"+el.get('href'))
               for el in links]
        for title, url in res:
            log.debug(title)
        return res
    except Exception as e:
        # html, info = get(fipi_bank_root_url)
        # time.sleep(2)
        html, info = get("http://85.142.162.119/os11/xmodules/qprint/" +
                         "openlogin.php?proj=B9ACA5BBB2E19E434CD6BEC25284C67F",
                         force=True)
        time.sleep(2)
        get(subject_url, force=True)
        self.retry(countdown=2, exc=e)
        client.captureException()


@shared_task
def process_sections(sections, *args):
    """Пройтись по всем разделам предмета.

    Parameters
    ----------
    section_title : str
       Заголовок раздела
       ("Информация и информационные процессы")

    url : str
       адрес первой страницы с задачами
    """
    total_pages = 0
    count = 1
    try:
        for section_title, url in sections:
            log.debug('Processing "{}" ({}/{})...'.format(
                section_title,
                count,
                len(args)
            ))
            html, info = get(url)
            tree = lxml.html.fromstring(html)
            pages = S('span.Walk a')(tree)
            pages = [int(p.text_content().strip('[]')) for p in pages]
            pages.append(0)
            total_pages = max(pages)  # noqa
            count += 1

            if not settings.TESTING:
                time.sleep(5)

            chain(
                extract_tasks_from_url.s(url),
                process_tasks.s(),
            )()

            if not settings.TESTING:
                time.sleep(5)

            # for i in range(1, total_pages-1)

            # print(total_pages)
            break
    except:
        client.captureException()


@shared_task(bind=True)
def extract_tasks_from_url(self, url):
    """Извлечение задач со страницы.

    На одной странице расположено 10 форм. В каждой - таблица с
    содержанием задачи. В форме также есть скрытый <input> - GUID
    задачи.

    """
    try:
        html, info = get(url)
        tree = lxml.html.fromstring(html)
        forms = S('form[name="checkform"]')(tree)
        res = []

        # each task is in <form> tag
        for form in forms:
            guid = S('input[name="guid"]')(form)[0].get('value').strip()
            html = ''
            # html = etree.tostring(form, encoding='unicode')
            # html = etree.tostring(S('table')(form)[0], encoding='unicode')
            # print(etree.tostring(S('table td')(form)[0], encoding='unicode'))
            table = S('table')(form)[0]
            # for td in S('tr td')(table):
            for tr in table.xpath("child::node()"):
                if isinstance(tr, lxml.etree._ElementUnicodeResult):
                    continue
                for td in tr.xpath("child::node()"):
                    if isinstance(td, lxml.etree._ElementUnicodeResult):
                        continue
                    for el in td.xpath("child::node()"):
                        if isinstance(el, lxml.etree._ElementUnicodeResult):
                            html += str(el)
                        else:
                            html += etree.tostring(
                                el,
                                encoding='unicode',
                                method="html"
                            )
            res.append((guid, html.strip()))
        return res
    except TypeError as e:
        # TypeError: Type 'lxml.etree._ElementUnicodeResult' cannot be
        # serialized.
        raise e
    except Exception as e:
        raise e
        html, info = get("http://85.142.162.119/os11/xmodules/qprint/" +
                         "openlogin.php?proj=B9ACA5BBB2E19E434CD6BEC25284C67F",
                         force=True)
        time.sleep(2)
        html, info = get(url, force=True)
        time.sleep(2)
        self.retry(countdown=2, exc=e)
        client.captureException()


task_process_version = 2


@shared_task
def process_tasks(*args):
    """Обработать задачи, полученные с fipi.ru

    Либо переданные (как список), либо из базы данных.

    """
    if len(args) > 0:
        tasks = args[0]  # list of tuples
        for task_info in tasks:
            process_task.delay(*task_info)
        return len(tasks)
    else:
        # process tasks from DB
        tasks = Task.objects.filter(debug__has_key='fipi_guid') \
                            .filter(debug__v__lt=task_process_version)
        for task in tasks:  # Task models
            info = (
                task.debug['fipi_guid'],
                task.debug['html']
            )
            process_task.delay(*info)
        return len(tasks)


@shared_task
def process_task(guid, html):
    try:
        task = Task.objects.get(debug__fipi_guid=guid)
        if not task.published:
            tree = lxml.html.fromstring(html)
            task.text = tag_contents(tree)
            print(html)
            task.debug['v'] = task_process_version
            task.save()
            return 'processed'
        else:
            return 'published'
    except Task.DoesNotExist:
        # There still may be the same task just without Fipi GUID
        task = Task(
            title=html[:20],
            text=html,
            debug={
                'fipi_guid': guid,
                'html': html,
                'v': task_process_version
            }
        )
        task.save()
        return 'created'


def tag_contents(tag):
    if isinstance(tag, lxml.etree._ElementStringResult) or \
       isinstance(tag, lxml.etree._ElementUnicodeResult):
        return str(tag)

    res = []
    for el in tag.xpath("child::node()"):
        # print(el)
        # for el in tag:
        # res.append(str(el)+'\n')
        res.append(tag_to_text(el))

    return "".join(res)


def tag_to_text(tag):
    res = []
    contents = tag_contents(tag)
    # contents = ''
    empty = not bool(contents.strip())

    if isinstance(tag, lxml.etree._ElementStringResult) or \
       isinstance(tag, lxml.etree._ElementUnicodeResult):
        return str(tag)

    # b
    elif tag.tag == "b":
        if not empty:
            # res.append("**{}**".format(contents))
            return "**{}**".format(contents)
        return ''

    elif tag.tag == "br":
        # res.append("<br>")
        return "<br>"

    # i
    elif tag.tag == "i":
        if not empty:
            return "_{}_".format(contents)
        return ''

    elif tag.tag == "input":
        return ''
        # if not empty:
        #     res.append("_{}_".format(contents))

    # p
    elif tag.tag == "p":
        # return "{}\n\n".format(contents.strip())
        # return str(tag)
        if not empty:
            if len(res) > 1 and res[-1].strip() == '':
                # print(res)
                res.pop()
            # res.append(contents.strip() + "\n\n")
            return contents.strip() + "\n\n"
        return ''

    # script
    elif tag.tag == "script":
        s = tag.text.strip()
        if s.startswith("ShowPictureQ"):
            m = re.search('["\'](.*?)["\']', s)
            url = m.group(1)
            url = "http://85.142.162.119/os11/"+url
            # TODO: get file from url
            res.append(url+" ")
            # res.append(element.text.strip()+"\n\n")
        return ''

    # span
    elif tag.tag == "span":
        if not empty:
            return contents
        return ''

    # table
    elif tag.tag == "table":
        # html = etree.tostring(tag, encoding='unicode')
        html = '<table>\n'

        # for el in tag.xpath("child::node()"):
        html += contents

        html += '</table>\n\n'
        return html
        # res.append(html)
        # res.append('<table>: \n\n')

    elif tag.tag == "tbody":
        # html = etree.tostring(tag, encoding='unicode')
        # html = '<tbody>'
        # for el in tag.xpath("child::node()"):
        html = contents

        # html += '</tbody>'
        return html

    elif tag.tag == "tr":
        # res.append(contents.strip() + "\n\n")
        return '  <tr>{}\n  </tr>\n'.format(contents)

    elif tag.tag == "td":
        # res.append(contents.strip() + " ")
        if len(contents) < 80:
            return '    <td>{}</td>'.format(contents.strip())
        else:
            return '    <td>\n{}\n    </td>\n'.format(contents.strip())

    # any other tag
    else:
        return 'Unknown tag: "{}" <-- \n'.format(tag.tag)
        # html = etree.tostring(tag, encoding='unicode')
        # print(html)
        # res.append(html)
        # raise ValueError('Unknown tag: "{}"'.format(tag.tag))
        # try:
        # except:
        #     client.captureException()
        # if tag.text is not None:
        #     res.append(tag.text)

    # return "".join(res)


@shared_task
def get_inf():
    # subject root url
    url = "http://85.142.162.119/os11/xmodules/qprint/index.php" +\
          "?proj=B9ACA5BBB2E19E434CD6BEC25284C67F"
    try:
        chain(
            get_subject_sections.s(url),
            process_sections.s(),
            # process_tasks.s(),
        )()
    except:
        client.captureException()
