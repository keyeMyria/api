import logging
import os
from pashinin.views import Base as B
from django.conf import settings
from .models import *  # noqa
from edu.models import Task
import pymorphy2
# from django.core.urlresolvers import reverse

morph = pymorphy2.MorphAnalyzer()
log = logging.getLogger(__name__)


class Base(B):
    def get_context_data(self, **kwargs):
        c = super(Base, self).get_context_data(**kwargs)
        c['EGE'] = settings.SITE_ID == 2
        c['OGE'] = settings.SITE_ID == 3
        c['exam_type'] = 0 if c['EGE'] else 1
        c['exam_type_str'] = 'ЕГЭ' if c['EGE'] else 'ОГЭ'
        return c


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
            c['ege'] = EGE.objects.get(
                subject=c['subject'],
                year=c['year'],
                type=0
            )
            # дательный падеж:
            c['po_subject'] = " ".join([
                morph.parse(w)[0].inflect({'datv'}).word
                for w in str(c['subject']).split()
            ]).lower()
        except Subject.DoesNotExist:
            c['subject'] = None
            c['status'] = 404

        c['tasks'] = Task.objects.filter()
        return c
