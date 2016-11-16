import json
import datetime
from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels.auth import channel_session_user_from_http
from channels.generic import BaseConsumer
from channels.channel import Group
from channels.generic.websockets import WebsocketConsumer, JsonWebsocketConsumer
import threading
import subprocess
import redis
from django.core.cache import cache
from django.core.mail import send_mail


# Send form from main page
# Form: name, phone, message
def send_lead(f):
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


def popenAndCall(ws, popenArgs):
    """
    Runs the given args in a subprocess.Popen, and then calls the function
    onExit when the subprocess completes.
    onExit is a callable object, and popenArgs is a list/tuple of args that
    would give to subprocess.Popen.
    """
    def runInThread(ws, popenArgs):
        proc = subprocess.Popen(*popenArgs)
        proc.wait()
        ws.send('asd')
        return
    thread = threading.Thread(target=runInThread, args=(ws, popenArgs))
    thread.start()
    # returns immediately after the thread starts
    return thread


def http_request_consumer(message):
    # print(message.content)
    response = HttpResponse('Hello world! You asked for %s' % message.content['path'])
    for chunk in AsgiHandler.encode_response(response):
        message.reply_channel.send(chunk)


# class AdminAPI(WebsocketConsumer):
class AdminAPI(JsonWebsocketConsumer):
    http_user = True

    # method_mapping = {
    #     "websocket.connect": "method_name",
    # }

    # def raw_receive(self, message, **kwargs):
    #     self.receive(message['text'], **kwargs)

    # def raw_receive(self, message, **kwargs):
    #     if "text" in message:
    #         try:
    #             self.receive(json.loads(message['text']), **kwargs)
    #         except:
    #             self.receive(json.loads(message['bytes'].encode('utf-8')), **kwargs)
    #     else:
    #         self.receive(json.loads(message['bytes'].encode('utf-8')), **kwargs)
    #         # raise ValueError("No text section for incoming WebSocket frame!")

    # def raw_connect(self, message, **kwargs):
    #     """
    #     Called when a WebSocket connection is opened. Base level so you don't
    #     need to call super() all the time.
    #     """
    #     for group in self.connection_groups(**kwargs):
    #         Group(group, channel_layer=message.channel_layer).add(message.reply_channel)
    #     channel_session_user_from_http(self.connect)(message, **kwargs)

    def popen(self, args):
        def runInThread(ws, args):
            proc = subprocess.Popen(*args)
            proc.wait()
            ws.send(str(ws.user))
            return

        thread = threading.Thread(target=runInThread, args=(self, args))
        thread.start()
        return thread


    def connect(self, message, **kwargs):
        # print(self.method_mapping[message.channel.name])
        self.c = message.content
        # print(message.keys())
        self.user = message.user
        self.r = redis.StrictRedis(host='10.254.239.1', port=6379, db=0)
        # self.send(r.get(k))
        # print(message.user)
        # self.popen(["ls"])


    def receive(self, text=None, bytes=None, **kwargs):
        """
        Called with a decoded WebSocket frame.
        """
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
