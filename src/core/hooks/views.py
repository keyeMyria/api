import json
import os
import redis
import urllib
from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.db.models import Count
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework import renderers


class Github(APIView):
    def post(self, request, **kwargs):
        # c = self.get_context_data(**kwargs)
        # send_mail(
        #     "github hook",
        #     "body",
        #     "{Github hook} <ROBOT@pashinin.com>",
        #     ["sergey@pashinin.com"])
        return HttpResponse("ok")


class Travis(APIView):
    def post(self, request, **kwargs):
        # request.body - bytes
        s = request.body.decode("utf-8")  # string
        d = urllib.parse.parse_qs(s)      # dict

        # d["payload"]    is a list with 1 item - a string
        # This string contains JSON object described here:
        # https://docs.travis-ci.com/user/notifications#Webhooks-Delivery-Format
        payload = json.loads(d["payload"][0])
        if payload['result'] == 0:  # Travis build SUCCEDED
            commit_sha1 = payload['commit']
            send_mail(
                "travis hook",
                commit_sha1,
                "Travis hook <ROBOT@pashinin.com>",
                ["sergey@pashinin.com"])
        else:  # Travis build FAILED
            pass
        return HttpResponse("ok")


class Telegram(APIView):
    def post(self, request, **kwargs):
        # request.body - bytes
        s = request.body.decode("utf-8")  # string
        send_mail(
            "telegram hook",
            s,
            "Telegram hook <ROBOT@pashinin.com>",
            ["sergey@pashinin.com"]
        )
        return HttpResponse("ok")
