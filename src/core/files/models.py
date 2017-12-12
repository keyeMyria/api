import os
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models
from core import now
import hashlib
import re
# from raven.contrib.django.raven_compat.models import client
import shutil
from dirtyfields import DirtyFieldsMixin
from core.models import AddedChanged
from django.urls import reverse
from django.core.files.uploadedfile import (TemporaryUploadedFile,
                                            InMemoryUploadedFile)
from . import CT_CHOICES
import logging
log = logging.getLogger(__name__)


class BaseFile(DirtyFieldsMixin, AddedChanged):
    """A single file and it's properties.

    Can't be changed or updated with a new version

    """
    # basename = models.CharField(max_length=200, blank=True, null=True)
    sha1 = models.CharField(max_length=40, editable=False, unique=True)
    size = models.BigIntegerField(null=True, blank=True, editable=False)
    content_type = models.IntegerField(
        blank=True,
        null=True,
        choices=CT_CHOICES,
        editable=False,
    )
    content_subtype = models.CharField(
        max_length=96,
        blank=True, null=True,
        editable=False,
    )
    # public = models.BooleanField(
    #     default=False,
    #     help_text=_("Anyone can access this file")
    # )
    # uploader = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     default=None,
    #     null=True,
    #     blank=True,
    #     db_column='uploader'
    # )
    # comment = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        default_permissions = ()  # Defaults to ('add', 'change', 'delete')
        verbose_name = _("File")
        verbose_name_plural = _('Files')
        index_together = (("content_type", "content_subtype"), )

    @property
    def content_type_string(self):
        if self.content_type is None:
            return str(None)
        return '{}/{}'.format(
            dict(CT_CHOICES)[self.content_type],
            self.content_subtype
        )

    @classmethod
    def filename_from_hash(cls, **kwargs):
        """Return a full filename string from SHA1.

        Example:

        sha1 = '012319f8340cb23cd9568ada37de023ecfedf138'
        BaseFile.filename_from_hash(sha1=sha1)
        > /mnt/files/012/319/f8340cb23cd9568ada37de023ecfedf138

        Where "/mnt/files/" is FILES_ROOT variable (settings.py)
        """

        # ext = kwargs.get('ext', '')
        if 'sha1' in kwargs:
            sha1 = kwargs['sha1']
            return os.path.join(
                settings.FILES_ROOT,
                sha1[:3],
                sha1[3:6],
                sha1[6:]
            )

    @property
    def filename(self):
        return BaseFile.filename_from_hash(sha1=self.sha1)

    @classmethod
    def get_md5(cls, filename):
        "Return 32 char MD5 hash"
        blocksize = 32768  # multiple of 128
        hasher = hashlib.md5()
        try:
            with open(filename, "rb") as f:
                buf = f.read(blocksize)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = f.read(blocksize)
                return hasher.hexdigest()
        except Exception:
            return None

    @classmethod
    def get_sha1(cls, f):
        "Calculate SHA1 of a file."

        blocksize = 32768  # multiple of 128
        hasher = hashlib.sha1()

        if isinstance(f, str):
            with open(f, "rb") as ff:
                buf = ff.read(blocksize)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = ff.read(blocksize)
        elif isinstance(f, (TemporaryUploadedFile, InMemoryUploadedFile)):
            for chunk in f.chunks():
                hasher.update(chunk)
        else:
            raise ValueError(
                f"Don't know how to get SHA1 from: {type(f)}")

        return hasher.hexdigest()
    # client.captureException()

    @classmethod
    def copy_to_archive(cls, filename):
        """Copy a file to our archive, return a File model"""
        # fname = os.path.abspath(fname)
        sha1 = cls.get_sha1(filename)
        d = os.path.join(settings.FILES_ROOT, sha1[:3], sha1[3:6])
        dst = os.path.join(d, sha1[6:])
        if not os.path.isfile(dst):
            if not os.path.isdir(d):
                os.makedirs(d, exist_ok=True, mode=0o755)
            shutil.copyfile(filename, dst)
        f, created = cls.objects.get_or_create(sha1=sha1)
        # TODO: run "file process" task
        f.size = os.path.getsize(dst)
        if f.is_dirty():
            f.save()
        return f

    @classmethod
    def from_url(cls, url):
        "Add a file to our archive from an URL."

        # check if already have this file
        # https://pashinin.com/_/files/{}
        m = re.fullmatch('https://pashinin.com/_/files/(?P<sha1>.{40})', url)
        try:
            f = cls.objects.get(sha1=m['sha1'])
            log.debug(f'Cached: {m["sha1"]}')
            return f
        except (cls.DoesNotExist, KeyError):
            log.debug(f'Downloading {url}')

        # Have no such file => download it to a temporary file...
        import tempfile
        import urllib
        with tempfile.NamedTemporaryFile() as f:
            with urllib.request.urlopen(url) as response:
                data = response.read()  # a `bytes` object
                f.write(data)
                f.flush()
                # print(len(data))
            # urllib.urlretrieve(url, f.name)
            # print(f.name)
            return BaseFile.copy_to_archive(f.name)

    # @classmethod
    # def from_bytes(cls, b):
    #     d = Data.from_bytes(b)
    #     filename = cls.uploads_md5(d.md5)
    #     f, created = cls.objects.get_or_create(data=d, filename=filename)
    #     if not os.path.isfile(filename):
    #         with open(filename, "wb") as fd:
    #             fd.write(b)
    #     return f

    def readable_by(self, user, request=None):
        if user.is_superuser:
            return True
        if request is not None:
            files = request.session.get('files', [])
            if self.data.md5 in files:
                return True
        # or md5 in session var
        return False

    @classmethod
    def write(cls, sha1, f):
        filename = cls.filename_from_hash(sha1=sha1)
        path = os.path.dirname(filename)
        os.makedirs(path, exist_ok=True)
        if isinstance(f, (TemporaryUploadedFile, InMemoryUploadedFile)):
            if not os.path.isfile(filename):
                with open(filename, "wb") as fd:
                    for chunk in f.chunks():
                        fd.write(chunk)
        else:
            raise ValueError(
                "BaseFile.write(): how to write {}".format(type(f))
            )
        return filename

    @property
    def icon(self):
        '''Return an URL to icon for this file type'''
        p = '/_s/img/icons'
        return os.path.join(
            p,
            # mime_icons.get(self.content_type_string, '01.png')
        )

    def send(self):
        from .sendfile import send_file
        return send_file(self.filename, attachment=True)

    def as_response(self):
        from .sendfile import send_file
        return send_file(self.filename, attachment=True)

    def get_absolute_url(self):
        return reverse("core:files:file", kwargs={
            'sha1': self.sha1,
        })

    def __str__(self):
        return self.sha1


class File(AddedChanged):
    """File that can be used in other places, renamed and updated.

    New File objects are created for every place requesting a file.

    Example: an article requests files like:
    \file{name_of_file}. A File object is created with
    name=name_of_file. Then a file is uploaded or chosen.

    """
    name = models.CharField(
        max_length=200,
        blank=True, null=True
        # not unique since 2 articles may want different files but name
        # them the same.
    )
    basefile = models.ForeignKey(
        BaseFile,
        null=True, blank=True,
        on_delete=models.SET_NULL,
    )
    # groups = models.ManyToManyField(Group)

    class Meta:
        default_permissions = ()  # Defaults to ('add', 'change', 'delete')


class UpToDateFileSet(AddedChanged):
    files = models.ManyToManyField(BaseFile)

    class Meta:
        default_permissions = ()  # Defaults to ('add', 'change', 'delete')


class UploadedFile(models.Model):
    """File uploaded to FILES_ROOT/uploads/<date>/filename"""

    file = models.FileField(upload_to='%Y/%m/%d')
    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=None,
        null=True,
        blank=True,
        db_column='uploader',
        on_delete=models.SET_NULL,
    )
    date_uploaded = models.DateTimeField(default=now)
    sha1 = models.CharField(
        max_length=40,
        editable=False,
        null=True,
        blank=True,
        verbose_name="SHA1"
    )

    class Meta:
        # db_table = 'uploads'
        verbose_name = _("Uploaded file")
        verbose_name_plural = _('Uploaded files')

    def get_sha1(self):
        if self.sha1:
            return self.sha1
        self.sha1 = BaseFile.get_sha1(self.filename)
        self.save()
        return self.sha1

    # @staticmethod
    # def generate_new_filename(instance, filename):
    #     f, ext = os.path.splitext(filename)
    #     return '%s%s' % (uuid.uuid4().hex, ext)

    @property
    def in_archive_already(self):
        """Located in private or public folders?"""
        return os.path.isfile(
            BaseFile.filename_from_hash(
                sha1=self.get_sha1()
            )
        )

    @property
    def filename(self):
        """Returns a full filename of an UploadedFile"""
        return os.path.join(settings.MEDIA_ROOT, self.file.name)

    def __str__(self):
        return str(self.file)
