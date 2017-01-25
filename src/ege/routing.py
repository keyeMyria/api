from channels.routing import route_class
from .consumers import *  # noqa


channel_routing = [
    route_class(Default),
]
