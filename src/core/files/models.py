import os
from django.utils.translation import gettext_lazy as _
from django.conf import settings
MEDIA_ROOT = settings.MEDIA_ROOT
MEDIA_URL = settings.MEDIA_URL
from django.db import models
from core import now
import hashlib
from raven.contrib.django.raven_compat.models import client
import shutil
from dirtyfields import DirtyFieldsMixin
from django.http import HttpResponse
from core.models import AddedChanged
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile


def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

#def mymd5(f, fsize=None, hexdigest=True):
#    """1. file size > 3Mb
#    data = first MB + middle MB + last MB
#    return md5(data)
#
#    2. file size <= 3Mb
#    return md5(whole file)
#"""
#    curpos=None
#    if fsize==None:
#        curpos = fsize = f.tell()
#        f.seek(0,os.SEEK_END) # at end
#        fsize = f.tell()
#        f.seek(curpos,os.SEEK_SET)
#
#    m = hashlib.md5()
#    if fsize>3*MB:
#        f.seek(0)
#        piece = f.read(MB)
#        m.update(piece)
#
#        f.seek(int(fsize/2))
#        piece = f.read(MB)
#        m.update(piece)
#
#        f.seek(-MB, os.SEEK_END)
#        piece = f.read(MB)
#        m.update(piece)
#    else:
#        for piece in read_in_chunks(f):
#            #process_data(piece)
#            m.update(piece)
#
#    #m.update("Nobody inspects")
#    #m.update(" the spammish repetition")
#    return m.hexdigest()
#


# from polymorphic import PolymorphicModel


class Data(models.Model):
    md5 = models.CharField(max_length=32, null=True, blank=True, editable=False)
    size = models.IntegerField(null=True, blank=True, editable=False)

    class Meta:
        # db_table = 'data'
        verbose_name = _("Bin data")
        verbose_name_plural = _("Bin data")
        unique_together = (("md5", "size"),)
        # abstract = True

    @classmethod
    def from_bytes(cls, b):
        hasher = hashlib.md5()
        hasher.update(b)
        o, created = cls.objects.get_or_create(md5=hasher.hexdigest(), size=len(b))
        return o

    @classmethod
    def from_file(cls, f):
        o, created = cls.objects.get_or_create(md5=File.get_md5(f), size=os.path.getsize(f))
        return o

    @property
    def file(self):
        """Return a File model with current md5 and size (if any) or None"""
        return None

    def __str__(self):
        return str(self.md5)


mime_extensions = {
    'image/jpeg': '.jpg'
}

mime_icons = {
    'image/jpeg': 'image-jpeg.png',
    'image/gif': 'image-gif.png',
    'application/pdf': 'application-pdf.png',
    'application/x-bittorrent': 'torrent.png',
    'application/x-debian-package': 'application-x-deb.png',
    'video/quicktime': 'video.png',
}


# Content-types:
# http://www.iana.org/assignments/media-types/media-types.xhtml
class File(DirtyFieldsMixin, AddedChanged):
    CT_APPLICATION = 0
    CT_AUDIO = 1
    CT_EXAMPLE = 2
    CT_IMAGE = 3
    CT_MESSAGE = 4
    CT_MODEL = 5
    CT_MULTIPART = 6
    CT_TEXT = 7
    CT_VIDEO = 8
    CT_CHOICES = (
        (CT_APPLICATION, 'application'),
        (CT_AUDIO, 'audio'),
        (CT_EXAMPLE, 'example'),
        (CT_IMAGE, 'image'),
        (CT_MESSAGE, 'message'),
        (CT_MODEL, 'model'),
        (CT_MULTIPART, 'multipart'),
        (CT_TEXT, 'text'),
        (CT_VIDEO, 'video'),
    )
    CT_CHOICES_REVERSED = {
        'application': CT_APPLICATION,
        'audio': CT_AUDIO,
        'example': CT_EXAMPLE,
        'image': CT_IMAGE,
        'message': CT_MESSAGE,
        'model': CT_MODEL,
        'multipart': CT_MULTIPART,
        'text': CT_TEXT,
        'video': CT_VIDEO
    }
    # date_uploaded = models.DateTimeField(default=now)
    # md5 = models.CharField(max_length=32, null=True, blank=True, editable=False)
    basename = models.CharField(max_length=200, blank=True, null=True)
    sha1 = models.CharField(
        max_length=40,
        editable=False,
        unique=True,
        primary_key=True
    )
    size = models.BigIntegerField(null=True, blank=True, editable=False)
    content_type = models.IntegerField(
        blank=True,
        null=True,
        choices=CT_CHOICES
    )
    content_subtype = models.CharField(max_length=96, blank=True, null=True)
    public = models.BooleanField(
        default=False,
        help_text=_("Anyone can access this file")
    )
    uploader = models.ForeignKey(
        'core.User',
        default=None,
        null=True,
        blank=True,
        db_column='uploader'
    )
    comment = models.CharField(max_length=200, null=True, blank=True)
    # https://github.com/ahupp/python-magic

    class Meta:
        verbose_name = _("File")
        verbose_name_plural = _('Files')
        index_together = (("content_type", "content_subtype"), )

    def publish(self):
        ext = mime_extensions.get(self.content_type_string, '')
        filename_public = self.filename_from_hash(
            sha1=self.sha1,
            public=True,
            ext=ext
        )
        if not os.path.isfile(filename_public):
            pass
        pass

    @property
    def content_type_string(self):
        if self.content_type is None:
            return str(None)
        return '{}/{}'.format(dict(File.CT_CHOICES)[self.content_type],
                              self.content_subtype)

    @classmethod
    def filename_from_hash(cls, **kwargs):
        """Return a filename string from hash string"""
        ext = kwargs.get('ext', '')
        public = kwargs.get('public', False)
        if 'sha1' in kwargs:
            sha1 = kwargs['sha1']
            if public:
                return os.path.join(
                    settings.FILES_ROOT,
                    'public',
                    sha1[:3],
                    sha1[3:6],
                    sha1[6:] + ext
                )
            else:
                return os.path.join(
                    settings.FILES_ROOT,
                    sha1[:3],
                    sha1[3:6],
                    sha1[6:]
                )

    @property
    def filename(self):
        return File.filename_from_hash(sha1=self.sha1, public=self.public)

    @classmethod
    def get_md5(cls, filename):
        blocksize = 32768  # multiple of 128
        hasher = hashlib.md5()
        try:
            with open(filename, "rb") as f:
                buf = f.read(blocksize)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = f.read(blocksize)
                return hasher.hexdigest()
        except:
            return None

    @classmethod
    def get_sha1(cls, f):
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
                "Unknown variable to get SHA1 from: {}".format(type(f)))

        return hasher.hexdigest()
    # client.captureException()

    @classmethod
    def copy_to_archive(cls, filename):
        """Copy a file to an archive, return a File model"""
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

    # @classmethod
    # def from_url(cls, url):
    #     #assert False, url
    #     # "url" start after /_sp/ ...   (so -5)
    #     filename = os.path.join(MEDIA_ROOT, url[len(MEDIA_URL)-5:])
    #     d, created = Data.objects.get_or_create(md5=cls.get_md5(filename),
    #                                             size=os.path.getsize(filename))
    #     #o, created = cls.objects.get_or_create(data=d)
    #     try:
    #         return cls.objects.filter(data=d)[0]
    #     except:
    #         f = cls(data=d)
    #         f.save()
    #         return f

    @classmethod
    def from_bytes(cls, b):
        d = Data.from_bytes(b)
        filename = cls.uploads_md5(d.md5)
        f, created = cls.objects.get_or_create(data=d, filename=filename)
        if not os.path.isfile(filename):
            with open(filename, "wb") as fd:
                fd.write(b)
        return f

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
            raise ValueError("File.write(): how to write {}".format(type(f)))
        return filename

    @property
    def icon(self):
        '''Return an URL to icon for this file type'''
        p = '/_s/img/icons'
        return os.path.join(p, mime_icons.get(self.content_type_string, '01.png'))
        return self.get_absolute_url()
        f, ext = os.path.splitext(self.name)
        if ext.startswith('.'):
            ext = ext[1:]

        if ext == 'torrent':
            return p+'torrent.png'
        elif ext in ['webm']:
            return p+'video.png'
        elif ext == 'ogg':
            return p+'ogg.png'
        elif ext == 'png':
            return self.url
        else:
            return p+'01.png'

    def send(self):
        from .sendfile import send_file
        return send_file(self.filename, attachment=True)

    def get_absolute_url(self):
        return reverse("files:file", kwargs={
            'sha1': self.sha1,
        })

    def __str__(self):
        return self.sha1


class UploadedFile(models.Model):
    """File uploaded to FILES_ROOT/uploads/<date>/filename"""

    file = models.FileField(upload_to='%Y/%m/%d')
    uploader = models.ForeignKey(
        'core.User',
        default=None,
        null=True,
        blank=True,
        db_column='uploader'
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
        self.sha1 = File.get_sha1(self.filename)
        self.save()
        return self.sha1

    @staticmethod
    def generate_new_filename(instance, filename):
        f, ext = os.path.splitext(filename)
        return '%s%s' % (uuid.uuid4().hex, ext)

    @property
    def in_archive_already(self):
        """Located in private or public folders?"""
        return os.path.isfile(
            File.filename_from_hash(
                sha1=self.get_sha1()
            )
        )

    @property
    def filename(self):
        """Returns a full filename of an UploadedFile"""
        return os.path.join(MEDIA_ROOT, self.file.name)

    def __str__(self):
        return str(self.file)
