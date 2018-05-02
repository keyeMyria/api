import json
import urllib
import base64
import requests
import logging
import telepot
# from telepot import Bot
from django.http import HttpResponse
# from django.db.models import Count
# from django.conf import settings
# from django.utils.translation import gettext_lazy as _
from OpenSSL.crypto import verify, load_publickey, FILETYPE_PEM, X509
from OpenSSL.crypto import Error as SignatureError
from rest_framework.views import APIView
from django.http import HttpResponseBadRequest  # , JsonResponse
from django.core.cache import cache
from django.utils.crypto import get_random_string
from ..models import User
from raven.contrib.django.raven_compat.models import client
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
    key = 'user-telegram-{}'

    def get(self, request, **kwargs):
        '''Makes possible to associate users's account with Telegram's account.

        This method is invoked when a registered user click "Connect
        Telegram" in his profile page.

        '''
        token = kwargs.get('token', None)
        user = self.request.user
        if user.is_authenticated and not token:
            token = get_random_string(length=32)
            cache.set(
                self.key.format(token),
                user.pk,
                timeout=5*60,
            )
            return HttpResponse(token)
        else:
            return HttpResponse('')

    def post(self, request, **kwargs):
        # Telegram token is defined in URLs
        token = kwargs.get('token', None)
        bot = telepot.Bot(token)

        # request.body is "bytes"
        s = request.body.decode("utf-8")  # string
        msg = json.loads(s)
        update_id = None
        if 'update_id' in msg:
            for key in msg:
                if key == 'update_id':
                    update_id = msg['update_id']
                else:
                    msg = msg[key]
        # Example:
        # {message: {chat: {}, date: 1515851945, from: {}, message_id:
        # 174, text: H}, update_id: 185696256}

        # try:
        #     message = j['message']
        # except Exception:
        #     print(j)
        #     client.captureException()

        try:
            flavor = telepot.flavor(msg)
        except Exception:
            client.captureException()
            return HttpResponse("")

        # chat_id = message['chat']['id']

        if flavor == 'callback_query':
            query_id, from_id, query_data = telepot.flance(msg)[1]
            # query_id == 6479684549687354674     (really big)
            # query_data == "publish" / "skip" / "spam"
            (chat_id, message_id) = telepot.origin_identifier(msg)
            user = None
            try:
                user = User.objects.get(telegram_chat_id=chat_id)
            except Exception:
                pass

            bot.answerCallbackQuery(
                query_id,
                text=str(user)+': '+str(query_id)
            )
            bot.deleteMessage(telepot.origin_identifier(msg))
            # telepot.origin_identifier(msg)
            # bot.sendMessage(
            #     chat_id,
            #     "echo2: "+text,
            # )

        # This part is invoked when a new message is received or when a
        # user starts a chat with my bot.
        elif flavor == 'chat':
            content_type, chat_type, chat_id = telepot.flance(msg)[1]
            text = msg['text']

            # Someone's pressed Telegram's "/start" button:
            if text.startswith('/start '):
                words = text.split()
                token = words[-1]
                user_id = cache.get(self.key.format(token))
                if user_id:
                    try:
                        user = User.objects.get(pk=user_id)
                        user.telegram_chat_id = chat_id
                        user.save()
                        bot.sendMessage(
                            chat_id,
                            "Привет, "+str(user),
                        )
                    except User.DoesNotExist:
                        client.captureException()
                self.key.format(token)

            # Any other message here. Answer the prayer:
            else:
                bot.sendMessage(
                    chat_id,
                    "echo2: "+text,
                    # parse_mode=None,
                    # disable_web_page_preview=None,
                    # disable_notification=None,
                    # reply_to_message_id=None,
                    # reply_markup=None
                )
        else:
            log.error('unknown message: '+str(msg))
        return HttpResponse("")
