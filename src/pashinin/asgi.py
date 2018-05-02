import os
# import django

import channels.asgi  # v1
# from channels.routing import get_default_application  # v2


app = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = app+'.settings'

# v1
channel_layer = channels.asgi.get_channel_layer()  # old

# v2
# django.setup()
# application = get_default_application()
