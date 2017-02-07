# import logging
# from core.consumers import JsonWebsocketConsumer
# log = logging.getLogger(__name__)


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
