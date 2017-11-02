import os
from os.path import isfile
from .models import BaseFile, UploadedFile
from celery import shared_task
from django.conf import settings
from raven.contrib.django.raven_compat.models import client
# from tempfile import mkstemp, mkdtemp
from . import CT_CHOICES_REVERSED, files_used_in_this_repo
import logging
log = logging.getLogger(__name__)


class FileSystemNotReady(Exception):
    def __init__(self, message, errors):
        super(FileSystemNotReady, self).__init__(message)
        self.errors = errors


def ensure_fs_ready():
    if settings.TESTING:
        if not os.path.isdir(settings.FILES_ROOT):
            os.makedirs(settings.FILES_ROOT, exist_ok=True)
    else:
        if settings.DEBUG:
            if not os.path.isdir(settings.FILES_ROOT):
                raise FileSystemNotReady(settings.FILES_ROOT)
        else:
            if not os.path.ismount(settings.FILES_ROOT):
                raise FileSystemNotReady(settings.FILES_ROOT)


v = 1  # version of algorithm


@shared_task
def process_file(f):
    """Do any stuff with a file in a main archive."""
    # f.update(debug__v=v)
    # File.objects.filter(pk=f.id).update(debug__v=v)
    if f.sha1 is None and f.filename and isfile(f.filename):
        d, fname = os.path.split(f.filename)
        d, d2 = os.path.split(d)
        d, d1 = os.path.split(d)
        f.sha1 = d1+d2+fname

    # Set Content-type for a file
    if f.content_type is None or f.content_subtype is None:
        import magic
        m = magic.from_file(f.filename, mime=True).decode("utf-8")
        if len(m.split('/')) == 2:
            t, subt = m.split('/')
            f.content_type = CT_CHOICES_REVERSED.get(t)
            f.content_subtype = subt

    if f.is_dirty():
        f.save()


@shared_task
def files_process():
    try:
        # for f in BaseFile.objects.exclude(debug__gte={'v': v}):
        for f in BaseFile.objects.filter():
            process_file(f)
    except Exception:
        client.captureException()


@shared_task
def move_all_uploads():
    try:
        for f in UploadedFile.objects.filter():
            move_upload_to_files(f)
    except Exception:
        client.captureException()


@shared_task
def move_upload_to_files(upload):
    if isfile(upload.filename):
        if not upload.in_archive_already:
            BaseFile.copy_to_archive(upload.filename)
        os.remove(upload.filename)
    upload.delete()
    f, c = BaseFile.objects.get_or_create(sha1=upload.get_sha1())

    # Set Content-type for a file
    if f.content_type is None or f.content_subtype is None:
        import magic
        m = magic.from_file(f.filename, mime=True)
        if len(m.split('/')) == 2:
            t, subt = m.split('/')
            f.content_type = CT_CHOICES_REVERSED.get(t)
            f.content_subtype = subt
        f.save()

    # If image move to public files, then check
    # if f.content_type_string in ('image/jpeg', ):
    #     f.publish()
    return f


@shared_task
def download_core_files():
    "Return sha1 hashes iterator of files used in this git repo."
    ensure_fs_ready()

    def files():
        for sha1 in files_used_in_this_repo():
            yield sha1

        try:
            from pashinin.models import Course
            for c in Course.objects.all():
                if c.logo_sha1:
                    yield c.logo_sha1
        except Exception as e:
            log.debug(str(e))

    for sha1 in files():
        url = 'https://pashinin.com/_/files/{}'.format(sha1)
        BaseFile.from_url(url)
