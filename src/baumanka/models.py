import os
from django.utils.translation import gettext_lazy as _
from django.conf import settings
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


class EduMaterial(DirtyFieldsMixin, AddedChanged):
    subject = models.CharField(max_length=200)
    semestr = models.SmallIntegerField()
    files = models.ForeignKey("corefiles.UpToDateFileSet")
    comment = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        default_permissions = ()
