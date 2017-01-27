import os
import channels.asgi

app = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = app+'.settings'
channel_layer = channels.asgi.get_channel_layer()
