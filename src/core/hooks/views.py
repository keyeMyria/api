import json
import urllib
from django.http import HttpResponse
# from django.db.models import Count
from django.conf import settings
# from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView


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
    "Travis web hook"

    def post(self, request, **kwargs):
        # Security check
        # Check not anyone can run update but only Travis
        secret = kwargs.get('secret', None)
        TRAVIS_SECRET = settings.TRAVIS_SECRET
        if not TRAVIS_SECRET or TRAVIS_SECRET != secret:
            return HttpResponse("")

        # We are sure it's Travis now
        # Do the job

        # request.body - bytes
        s = request.body.decode("utf-8")  # string
        d = urllib.parse.parse_qs(s)      # dict with only 1 key - "payload"

        # d["payload"]    is a list with only 1 item - a string
        # This string contains JSON object described here:
        # https://docs.travis-ci.com/user/notifications#Webhooks-Delivery-Format
        payload = json.loads(d["payload"][0])
        SUCCEDED = payload['result'] == 0
        if SUCCEDED:
            commit_sha1 = payload['commit']
            from core.tasks import project_update
            from core.models import SiteUpdate
            from core import now
            upd, created = SiteUpdate.objects.get_or_create(sha1=commit_sha1)
            upd.started = now()
            upd.travis_raw = d["payload"][0]
            upd.commit_message = payload['message']
            upd.save()
            project_update.delay(commit_sha1)
        else:
            # Travis build FAILED
            pass
        return HttpResponse("")


# telepot: https://github.com/nickoala/telepot
class Telegram(APIView):
    def post(self, request, **kwargs):
        token = kwargs.get('token', None)

        # request.body - bytes
        s = request.body.decode("utf-8")  # string
        j = json.loads(s)
        message = j['message']
        text = message['text']

        from telepot import Bot
        bot = Bot(token)
        bot.sendMessage(
            message['chat']['id'],  # chat_id,
            "echo: "+text,  # text,
            # parse_mode=None,
            # disable_web_page_preview=None,
            # disable_notification=None,
            # reply_to_message_id=None,
            # reply_markup=None
        )
        return HttpResponse("ok")
