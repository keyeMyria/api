import logging
import os
from pashinin.views import Base
from django.conf import settings
from .models import *  # noqa
# from django.core.urlresolvers import reverse
log = logging.getLogger(__name__)


class Index(Base):
    template_name = "ege_index.jinja"

    def get_context_data(self, **kwargs):
        c = super(Index, self).get_context_data(**kwargs)
        c['subjects'] = Subject.objects.filter()
        return c


class SubjectView(Base):
    template_name = "ege_subject.jinja"

    def get_context_data(self, **kwargs):
        c = super(SubjectView, self).get_context_data(**kwargs)
        try:
            c['subject'] = Subject.objects.get(slug=kwargs['subj'])
        except Subject.DoesNotExist:
            c['subject'] = None
            c['status'] = 404

        from edu.models import Task
        c['tasks'] = Task.objects.filter()
        return c
