from channels.routing import route, route_class
from .consumers import AdminAPI


channel_routing = [
    # Called when WebSockets connect
    route_class(AdminAPI)
    # route("websocket.connect", ws_connect),

    # Called when WebSockets get sent a data frame
    # route("websocket.receive", ws_receive),

    # Called when WebSockets disconnect
    # route("websocket.disconnect", ws_disconnect),

    # route('http.request', 'pashinin.consumers.http_request_consumer')
     # Include sub-routing from an app.
    # include("chat.routing.websocket_routing", path=r"^/chat/stream"),

    # Custom handler for message sending (see Room.send_message).
    # Can't go in the include above as it's not got a `path` attribute to match on.
    # include("chat.routing.custom_routing"),
]
