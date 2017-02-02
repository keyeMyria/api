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

from channels.routing import route, route_class
from .consumers import *  # noqa
from channels.generic.websockets import WebsocketDemultiplexer


# WebsocketDemultiplexer doesn't work with class-based consumers
class Demultiplexer(WebsocketDemultiplexer):
    # Mapping
    # stream -> channel
    # Javascript sends data through WS like this:
    # {'stream': 'search', 'payload': {data here}}
    mapping = {
        "0": "websocket",
        # "intval": "binding.intval",
        # "stats": "internal.stats",
    }


channel_routing = [
    # route_class(Demultiplexer),
    route_class(Celery, path=r"^/admin/celery$"),

    # default at the end
    route_class(Default),

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
]
