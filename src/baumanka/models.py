import os
# from django.utils.translation import gettext_lazy as _
from django.db import models
# from raven.contrib.django.raven_compat.models import client
from core.models import AddedChanged
from dirtyfields import DirtyFieldsMixin
# from django.core.urlresolvers import reverse


class EduMaterial(DirtyFieldsMixin, AddedChanged):
    subject = models.CharField(max_length=200)
    semestr = models.SmallIntegerField()
    files = models.ForeignKey("corefiles.UpToDateFileSet")
    comment = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        default_permissions = ()
