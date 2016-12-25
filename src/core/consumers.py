import core.json as json
from channels.generic.websockets import WebsocketConsumer, \
    JsonWebsocketConsumer as JSONC


class JsonWebsocketConsumer(JSONC):
    """Modified version os JSON consumer.
    Uses my JSON encoder (core.json)"""
    http_user = True  # always pass user!

    def raw_receive(self, message, **kwargs):
        if "text" in message:
            content = json.loads(message['text'])
            stream = "default"
            payload = content
            if isinstance(content, dict) and \
               "s" in content and "p" in content:
                stream = content['s']
                payload = content['p']
            self.receive(stream, payload, **kwargs)
        else:
            raise ValueError("No text section for incoming WebSocket frame!")

    def send(self, content, stream='', close=False):
        """Encode the given content as JSON and send it to the client."""
        d = {'s': stream, 'p': content}
        super(JSONC, self).send(text=json.dumps(d), close=close)


class SuperuserConsumer(JsonWebsocketConsumer):
    http_user = True

    def connect(self, message, **kwargs):
        if not message.user.is_superuser:
            self.close()

    def raw_receive(self, message, **kwargs):
        """Called when a WebSocket frame is received."""
        if not message.user.is_superuser:
            return
        super(SuperuserConsumer, self).raw_receive(message, **kwargs)
