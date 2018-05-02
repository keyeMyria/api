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

import datetime
import subprocess
import traceback
from django.core.mail import send_mail
# from channels.generic.websocket import WebsocketConsumer
# from core.consumers import JsonWebsocketConsumer, SuperuserConsumer
from raven.contrib.django.raven_compat.models import client
import logging
log = logging.getLogger(__name__)


# class MyConsumer(WebsocketConsumer):
#     groups = ["broadcast"]

#     def connect(self):
#         # Called on connection. Either call
#         self.accept()
#         # Or to reject the connection, call
#         # self.close()

#     def receive(self, text_data=None, bytes_data=None):
#         # Called with either text_data or bytes_data for each frame
#         # You can call:
#         self.send(text_data='{"asd": "Hello world!"}')
#         # Or, to send a binary frame:
#         # self.send(bytes_data="Hello world!")
#         # Want to force-close the connection? Call:
#         # self.close()
#         # Or add a custom WebSocket error code!
#         # self.close(code=4123)

#     def disconnect(self, close_code):
#         # Called when the socket closes
#         pass


def send_lead_course(f):
    from .models import Course  # CourseLead
    course = Course.objects.get(slug=f['course'])
    # CourseLead.objects.get_or_create(course=course)

    title = "Запись на \"{}\"".format(
        course.name
    )
    body = "{}\nИмя: {}\nТелефон: {}\n\n{}".format(
        datetime.datetime.now(),
        f['name'],
        f['contact'],
        f['comment']
    )
    from_str = "{} <ROBOT@pashinin.com>".format(f['name'])
    recipients = ["sergey@pashinin.com"]
    send_mail(title, body, from_str, recipients)


def send_lead(f):
    """Send a form from main page

    f - a Django form with 3 params:
    f["name"] - user name
    f["phone"] - user phone
    f["message"] - additional message"""
    try:
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
    except Exception:
        log.error("Can't send email to me: {}".format(traceback.format_exc()))
        client.captureException()


def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line

    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


# class Default(JsonWebsocketConsumer):
#     """Default websockets consumer (for anyone)"""

#     def receive(self, stream, payload, **kwargs):
#         """Called with decoded JSON content."""
#         if 'celery' == stream:
#             pass

#         else:
#             # no specific stream
#             pass
#         self.send({'s': 'def'})


# class AdminConsumer(SuperuserConsumer):
#     """Admin consumer"""

#     def receive(self, stream, payload, **kwargs):
#         """Called with decoded JSON content."""
#         if 'celery' == stream:
#             pass
#         elif 'task' == stream:
#             from core.tasks import project_update
#             project_update.delay("0b17e9e91086c6539589202242e362bf9e82c8d9")
#         else:
#             # no specific stream
#             pass

#         # self.send(self.message.user)
#         for line in execute(["ls"]):
#             self.send({'logline': line})
#         self.send({'logline': 'finish'})
