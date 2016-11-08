import json
import os
import redis
from core.views import BaseView
from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.db.models import Count
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.mail import send_mail


class Github(BaseView):
    def post(self, request, **kwargs):
        # c = self.get_context_data(**kwargs)
        send_mail(
            "github hook",
            "body",
            "{Github hook} <ROBOT@pashinin.com>",
            ["sergey@pashinin.com"])
        return HttpResponse("ok")
