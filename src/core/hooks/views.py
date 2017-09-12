import json
import urllib
import base64
import requests
import logging
from django.http import HttpResponse
# from django.db.models import Count
# from django.conf import settings
# from django.utils.translation import gettext_lazy as _
from OpenSSL.crypto import verify, load_publickey, FILETYPE_PEM, X509
from OpenSSL.crypto import Error as SignatureError
from rest_framework.views import APIView
from django.http import HttpResponseBadRequest  # , JsonResponse
log = logging.getLogger(__name__)


class Github(APIView):
    """Runs when Github sends data to /_/hooks/github.

    Auth?

    """
    def post(self, request, **kwargs):
        # c = self.get_context_data(**kwargs)
        # send_mail(
        #     "github hook",
        #     "body",
        #     "{Github hook} <ROBOT@pashinin.com>",
        #     ["sergey@pashinin.com"])
        return HttpResponse("ok")


class Travis(APIView):
    """Travis CI web hook.

    https://docs.travis-ci.com/user/notifications/#Configuring-webhook-notifications

    Webhooks are delivered with a application/x-www-form-urlencoded
    content type using HTTP POST, with the body including a payload
    parameter that contains the JSON webhook payload in a URL-encoded
    format.

    """

    # Make sure you use the correct config URL, the .org and .com
    # have different keys!
    # https://api.travis-ci.org/config
    # https://api.travis-ci.com/config
    #
    # org for free repos, com for companies?
    TRAVIS_CONFIG_URL = 'https://api.travis-ci.org/config'

    def post(self, request, **kwargs):
        # request.body - bytes
        try:
            s = request.body.decode("utf-8")  # string
            d = urllib.parse.parse_qs(s)      # dict with 1 key - "payload"
            # d["payload"]    is a list with only 1 item - a string
            # This string contains JSON object described here:
            # https://docs.travis-ci.com/user/notifications#Webhooks-Delivery-Format
            payload = json.loads(d["payload"][0])
            # json_payload = parse_qs(request.body)['payload'][0]
        except Exception as e:
            log.error({
                "message": "Bad Travis data",
                'error': str(e)
            })
            return HttpResponseBadRequest({
                'status': 'failed',
                'reason': 'malformed data'
            })

        # Auth
        # ---------
        signature = self._get_signature(request)
        try:
            public_key = self._get_travis_public_key()
        except requests.Timeout:
            log.error({
                "message": "Timed out retrieving Travis CI public key"
            })
            return HttpResponseBadRequest({'status': 'failed'})
        except requests.RequestException as e:
            log.error({
                "message": "Failed to retrieve Travis CI public key",
                'error': e.message
            })
            return HttpResponseBadRequest({'status': 'failed'})

        try:
            self.check_authorized(signature, public_key, d["payload"][0])
        except SignatureError:
            # Log the failure somewhere
            return HttpResponseBadRequest({'status': 'unauthorized'})
        # ---------
        #
        # We are sure it's Travis now
        # Do the job

        SUCCEDED = payload['result'] == 0
        NOTAG = payload['tag'] is None
        if SUCCEDED and not NOTAG:
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

        return HttpResponse("")

    def check_authorized(self, signature, public_key, payload):
        """
        Convert the PEM encoded public key to a format palatable for pyOpenSSL,
        then verify the signature
        """
        pkey_public_key = load_publickey(FILETYPE_PEM, public_key)
        certificate = X509()
        certificate.set_pubkey(pkey_public_key)
        verify(certificate, signature, payload, str('sha1'))

    def _get_signature(self, request):
        """
        Extract the raw bytes of the request signature provided by travis
        """
        signature = request.META['HTTP_SIGNATURE']
        return base64.b64decode(signature)

    def _get_travis_public_key(self):
        """
        Returns the PEM encoded public key from the Travis CI /config endpoint
        """
        r = requests.get(self.TRAVIS_CONFIG_URL, timeout=10.0)
        r.raise_for_status()
        return r.json()['config']['notifications']['webhook']['public_key']


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
