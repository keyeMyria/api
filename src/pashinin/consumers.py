"""This module describes all consumers.

A consumer is actually what does the job. It's a function which is
assigned to a channel later (in routing.py) OR a class-based consumer in
which your write this channel->method mapping.

For example if you have:

    class Consumer1(BaseConsumer):
        method_mapping = {
            "mylongtasks.all": "dothejob",
        }

    def dothejob(self, message, **kwargs):
        pass

then all tasks that go to "mylongtasks.all" channel will be executed
with `dothejob()` method of Consumer1 class.

About methods and functions:

def dothejob(self, message, **kwargs):
    pass


Message
=======

<channels.message.Message object at 0x7fc6b0049dd8>

>>> message.keys()
>>> dict_keys(['server', 'reply_channel', 'query_string', 'client',
'headers', 'method', 'order', 'path'])

"message" is a dict with these keys:

    content: The actual message content, as a dict. See the ASGI spec or
    protocol message definition document for how this is structured.

    channel: A Channel object, representing the channel this message was
    received on. Useful if one consumer handles multiple channels.

    reply_channel: A Channel object, representing the unique reply
    channel for this message, or None if there isn’t one.

    channel_layer: A ChannelLayer object, representing the underlying
    channel layer this was received on. This can be useful in projects
    that have more than one layer to identify where to send messages the
    consumer generates (you can pass it to the constructor of Channel or
    Group)

"""

import json
import datetime
from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels.generic import BaseConsumer
from channels.channel import Group
from channels.generic.websockets import WebsocketConsumer, JsonWebsocketConsumer
import threading
import subprocess
import redis
from django.core.cache import cache
from django.core.mail import send_mail
import logging
log = logging.getLogger(__name__)


def send_lead(f):
    """Send a form from main page

    f - a Django form with 3 params:
    f["name"] - user name
    f["phone"] - user phone
    f["message"] - additional message"""
    body = "{}\nИмя: {}\nТелефон: {}\n\n{}".format(
        datetime.datetime.now(),
        f['name'],
        f['phone'],
        f['message']
    )
    send_mail(
        "Заявка от {}, тел.: {}".format(
            f['name'],
            f['phone']
        ),
        body,
        "{} <ROBOT@pashinin.com>".format(f['name']),
        ["sergey@pashinin.com"]
    )


class Root(BaseConsumer):
    http_user = True

    method_mapping = {
        "root.call": "call",
    }

    def call(self, message, **kwargs):
        import getpass
        # getpass.getuser()
        self.send(getpass.getuser())


# class API(WebsocketConsumer):
class Celery(JsonWebsocketConsumer):
    http_user = True

    def connect(self, message, **kwargs):
        # print(self.method_mapping[message.channel.name])
        self.c = message.content
        for k in message.keys():
            log.debug(k)
        self.user = message.user
        # self.r = redis.StrictRedis(host='10.254.239.1', port=6379, db=0)
        # self.send(r.get(k))
        self.send('{"asd":123}')

    def receive(self, text=None, bytes=None, **kwargs):
        """
        Called with a decoded WebSocket frame.
        """
        if not self.user.is_superuser:
            return

        # self.send(text=text, bytes=bytes)
        self.send(json.dumps({'superuser': self.user.is_superuser}))

        d = {}
        try:
            d = json.loads(text)
            if not isinstance(d, dict):
                raise ValueError("not a dict")
        except ValueError:
            d = {}
            # self.send('unknown: '+text)
        except Exception:
            d = {}

        cmd = d.get('t', None)
        if cmd == 'file':
            from core.files.models import File
            hash = d.get('hash', None)
            comment = d.get('comment', None)
            f = File.objects.get(sha1=hash)
            if comment is not None:
                f.comment = comment
                f.save()
            print(comment)

        for k in d:
            if k == 'ddt':
                v = True if d[k]==b'True' or d[k]=='True' or d[k]==True else False
                self.r.set(k, v)
                self.send('set {} to {}'.format(k, v))
                from cms.adm import channels_run_worker
                channels_run_worker()
                # cache.set('ddt', d[k])

            if k == 'watchcss':
                self.send('css')

            if k == 'restartworker':
                from cms.adm import channels_run_worker
                k = 'worker'
                v = channels_run_worker()
                self.r.set(k, v)
                # self.send(str(p))

    def disconnect(self, message, **kwargs):
        """
        Called when a WebSocket connection is opened.
        """
        pass
