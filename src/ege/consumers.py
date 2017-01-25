import core.json as json
import datetime
from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels.generic import BaseConsumer
from channels.channel import Group
from channels.generic.websockets import WebsocketConsumer, \
    JsonWebsocketConsumer as JSONC
import threading
import subprocess
import redis
from django.core.cache import cache
from django.core.mail import send_mail
from subprocess import Popen
from core.consumers import JsonWebsocketConsumer, SuperuserConsumer
import logging
log = logging.getLogger(__name__)


class Default(JsonWebsocketConsumer):
    """Default websockets consumer (for anyone)"""

    def receive(self, stream, payload, **kwargs):
        """Called with decoded JSON content."""
        if 'celery' == stream:
            pass

        else:
            # no specific stream
            pass
        self.send({'s': 'def'})
