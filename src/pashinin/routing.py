"""This module describes the pairs of Channel-->Consumer.

A task (request) you create goes to a channel. A consumer gets this task
from a channel and then runs (does the job).

1. Create a Consumer (a function or a class) in consumers.py

If your consumer is a function then create a new channel below (just
pick a name) and assign a consumer (a function) to it like this:

          CHANNEL         CONSUMER

    route('send-me-lead', send_lead),

If your consumer is a class-based consumer then such mapping
(channel->consumer) is described inside your class like this:

    class Consumer1(BaseConsumer):
        method_mapping = {
            "mylongtasks.all": "dothejob",
        }

Then you can send tasks to a channels like this:

    from channels import Channel
    Channel('mylongtasks.all').send({'some': 'data'})


"channel_routing" variable (list defined below) is used settings.py file
when defining CHANNEL_LAYERS:

    'ROUTING': '{{app}}.routing.channel_routing',

"""

# Channels v1
from channels.routing import route, route_class
from channels.generic.websockets import WebsocketDemultiplexer

from django.conf.urls import url
from django.urls import path

# Channels v2
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from channels.generic.websocket import (
#     WebsocketMultiplexer,
#     AsyncWebsocketConsumer
# )
# from channels.generic.websocket.multiplex import \
#     WebsocketMultiplexerApplication


from .consumers import (
    # Default,
    # Celery,
    # AdminConsumer,
    # MyConsumer,
    send_lead,
    send_lead_course
)
from .models import CourseBinding
from .bindings import CourseBinding, StudentBinding
from articles.bindings import ArticleBinding
from edu.bindings import UniversityBinding, FacultyBinding, TaskBinding
from ege.bindings import ExamBinding
from core.bindings import UserBinding


class Demultiplexer(WebsocketDemultiplexer):
    http_user = True

    # Stream name -> Consumer
    consumers = {
        "courses": CourseBinding.consumer,
        "articles": ArticleBinding.consumer,
        "university": UniversityBinding.consumer,
        "faculty": FacultyBinding.consumer,
        "users": UserBinding.consumer,
        "tasks": TaskBinding.consumer,
        "root": TaskBinding.consumer,
        "celery": TaskBinding.consumer,
        "exams": ExamBinding.consumer,
        "students": StudentBinding.consumer,
    }
    groups = ["binding.values"]


# class EchoConsumer(AsyncWebsocketConsumer):
#     """
#     Basic echo consumer for testing.
#     """

#     results = {}

#     async def connect(self):
#         self.results["connected"] = True
#         await self.accept()

#     async def receive(self, text_data=None, bytes_data=None):
#         await self.send(text_data=text_data, bytes_data=bytes_data)

#     async def disconnect(self, code):
#         self.results["disconnected"] = True


# text_multiplexer = WebsocketMultiplexer({
#     "echo": EchoConsumer,
# })


# class RootDemultiplexer(WebsocketDemultiplexer):
#     http_user = True

#     # Stream name -> Consumer
#     consumers = {
#         "courses": CourseBinding.consumer,
#         "root.std": CourseBinding.consumer,
#     }
#     # groups = ["binding.values"]


# Mapping
# =======
# Channel -> Consumer
channel_routing = [
    # route_class(Celery, path=r"^/admin/celery$"),
    # route_class(Demultiplexer, path='^/stream/?$'),

    # route_class(Default),
    route_class(Demultiplexer),  # default at the end

    # route("root.std", AdminConsumer),
    # route("root.std", CourseBinding.consumer),
    #

    # route("websocket.connect", ws_connect),
    # Called when WebSockets get sent a data frame
    # route("websocket.receive", ws_receive),

    # Called when WebSockets disconnect
    # route("websocket.disconnect", ws_disconnect),

    # route('http.request', 'pashinin.consumers.http_request_consumer')
    # Include sub-routing from an app.
    # include("chat.routing.websocket_routing", path=r"^/chat/stream"),

    # Custom handler for message sending (see Room.send_message).

    # Can't go in the include above as it's not got a `path` attribute
    # to match on.

    # include("chat.routing.custom_routing"),

    route('send-me-lead', send_lead),
    route('course-enroll', send_lead_course),
]


# Channels v2
# application = ProtocolTypeRouter({
#     # http->django views is added by default

#     # "websocket": WebsocketMultiplexer({
#     #     "echo": EchoConsumer,
#     # }),

#     # "websocket": URLRouter([
#     #     url("^$", text_multiplexer({
#     #         "type": "websocket",
#     #         "path": '/',
#     #         "query_string": '',
#     #         "headers": [],
#     #         "subprotocols": [],
#     #     })),
#     # ]),
#     "websocket": AuthMiddlewareStack(
#         URLRouter([
#             # url("^front(end)/$", MyConsumer),
#             url("^$", EchoConsumer),
#             # url("^$", text_multiplexer),
#             # path('', MyConsumer),
#             # path('', text_multiplexer),
#         ])
#     ),
#     # "websocket": URLRouter([
#     # url("^chat/admin/$", AdminChatConsumer),
#     # url("^chat/$", PublicChatConsumer),
#     # ]),

# })
# application = WebsocketMultiplexer({
#     "echo": EchoConsumer,
# })
# application = text_multiplexer({
#     "type": "websocket",
#     "path": '/',
#     "query_string": '',
#     "headers": [],
#     "subprotocols": [],
# })
