import json
from datetime import datetime
from time import mktime
from raven.contrib.django.raven_compat.models import client
import six
from django.db import models


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        # Apps imports should be here (not in header!) or "Apps aren't
        # loaded yet" error apperars:
        # from cms.db.models import URL

        # If object has json() method - just call it
        if callable(getattr(obj, "json", None)):
            return obj.json()


        # If Django model - try primary key
        if issubclass(obj.__class__, models.Model):
            if obj.pk is not None:
                return {
                    '__type__': type(obj).__name__,
                    'pk': obj.pk
                }

        # Datetime
        if isinstance(obj, datetime):
            return {
                '__type__': '__datetime__',
                'epoc': int(mktime(obj.timetuple()))
            }

        # URL model
        # elif isinstance(obj, URL):
        #     return {
        #         '__type__': 'URL',
        #         'url': str(obj)
        #     }

        # TODO: bytes become str forever, thats wrong
        elif isinstance(obj, bytes):
            return {
                '__type__': 'bytes',
                'data': obj.decode("utf-8")
            }

        # Try default if all fails
        else:
            try:
                return json.JSONEncoder.default(self, obj)
            except:
                client.captureException()


def my_decoder(obj):
    models = ("URL", "Article", "WikiPage")
    t = obj.get('__type__', None)
    if t is None:
        return obj
    if t == '__datetime__':
        return datetime.fromtimestamp(obj['epoc'])

    # TODO: bytes become str forever, thats wrong (see encoding)
    if t == 'bytes':
        return obj['data']
    elif t in models:
        return globals()[t].objects.get(pk=obj['pk'])


# Encoder function
def my_dumps(obj):
    return json.dumps(obj, cls=MyEncoder)


# Decoder function
def my_loads(obj):
    try:
        if isinstance(obj, six.binary_type):
            obj = obj.decode('utf-8')
        return json.loads(obj, object_hook=my_decoder)
    except:
        client.captureException()
        return []
