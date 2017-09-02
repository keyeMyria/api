import os
# import mimetypes   # mimetypes based on filenames
import magic         # mimetypes based on content (better)
from django.http import HttpResponse, HttpResponseNotFound
from django.conf import settings
from core import underDjangoDebugServer
from .models import File


def _convert_file_to_url(filename):
    relpath = os.path.relpath(filename, settings.SENDFILE_ROOT)
    # ['/protected/']  <- Nginx internal location
    compounds = [settings.SENDFILE_URL]
    while relpath:
        relpath, head = os.path.split(relpath)
        compounds.insert(1, head)
    return '/'.join(compounds)


# r['Cache-Control'] = 'no-cache'
def send_file(f, *args, **kwargs):
    '''Send a protected file though Nginx or Django's dev server.
    f - filename (string) or File object (Model)'''
    # To indicate to the browser that the file should be viewed in the browser:
    #   Content-Type: application/pdf
    #   Content-Disposition: inline; "filename.pdf"
    #
    # To have the file downloaded rather than viewed:
    #   Content-Type: application/pdf
    #   Content-Disposition: attachment; "filename.pdf"
    if isinstance(f, File):
        filename = f.filename
    elif isinstance(f, str):
        filename = f
    else:
        raise ValueError("send_file(): how to send {}?".format(type(f)))

    attachment = kwargs.pop('attachment', False)
    outFilename = kwargs.pop('outFilename', os.path.basename(filename))

    if not os.path.isfile(filename):
        if settings.DEBUG:
            return HttpResponseNotFound(
                'File not found\n\nDebug info:\n  Missing file: {}'.format(
                    filename
                ),
                content_type="text/plain")
        else:
            return HttpResponseNotFound(
                'File not found', content_type="text/plain")

    # Create a response
    response = HttpResponse()

    # Set Content-type
    if isinstance(f, File) and f.content_type is not None and f.content_subtype:  # noqa
        response['Content-type'] = f.content_type_string
    else:
        # Always need to set a content type
        # Big binary file can hang up a browser (if try to parse)
        try:
            mime = magic.Magic(mime=True)
            response['Content-type'] = mime.from_file(filename)
        except Exception as e:
            if settings.DEBUG:
                print(e)
            response['Content-type'] = "application/octet-stream"

    if response['Content-type'] in (
            # "text/html",
            "text/plain",
    ):
        response['Content-type'] = response['Content-type'] + "; charset=utf-8"

    if attachment:
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(
            outFilename
        )
    else:
        # 'inline; filename="%s"' % (outFilename)
        # open in browser
        # if response['Content-type'] in (
        #         "application/pdf",
        #         "text/x-python",
        # ):
        #     response['Content-Disposition'] = 'inline'
        response['Content-Disposition'] = 'inline;'

    # Send content
    if underDjangoDebugServer():
        with open(filename, 'rb') as fd:
            response.write(fd.read())
    else:
        # response['X-Accel-Redirect'] = _convert_file_to_url(filename)
        response['X-Accel-Redirect'] = bytes(
            _convert_file_to_url(filename), 'utf-8')

    return response
