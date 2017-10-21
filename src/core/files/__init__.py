import os
from django.conf import settings

default_app_config = 'core.files.apps.FilesConfig'

#
# Content-types:
#
# http://www.iana.org/assignments/media-types/media-types.xhtml
#

mime_extensions = {
    'image/jpeg': '.jpg'
}

mime_icons = {
    'image/jpeg': 'image-jpeg.png',
    'image/gif': 'image-gif.png',
    'application/pdf': 'application-pdf.png',
    'application/x-bittorrent': 'torrent.png',
    'application/x-debian-package': 'application-x-deb.png',
    'video/quicktime': 'video.png',
}

CT_APPLICATION = 0
CT_AUDIO = 1
CT_EXAMPLE = 2
CT_IMAGE = 3
CT_MESSAGE = 4
CT_MODEL = 5
CT_MULTIPART = 6
CT_TEXT = 7
CT_VIDEO = 8
CT_CHOICES = (
    (CT_APPLICATION, 'application'),
    (CT_AUDIO, 'audio'),
    (CT_EXAMPLE, 'example'),
    (CT_IMAGE, 'image'),
    (CT_MESSAGE, 'message'),
    (CT_MODEL, 'model'),
    (CT_MULTIPART, 'multipart'),
    (CT_TEXT, 'text'),
    (CT_VIDEO, 'video'),
)
CT_CHOICES_REVERSED = {
    'application': CT_APPLICATION,
    'audio': CT_AUDIO,
    'example': CT_EXAMPLE,
    'image': CT_IMAGE,
    'message': CT_MESSAGE,
    'model': CT_MODEL,
    'multipart': CT_MULTIPART,
    'text': CT_TEXT,
    'video': CT_VIDEO
}


def iter_files(path, ending):
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith(ending):
                yield os.path.join(root, name)
        # for name in dirs:
        #     print(os.path.join(root, name))


def files_used_in_this_repo():
    """Return a list of SHA1 hashes of used files.

    Files are used in jinja templates like this:

        {{file("sha1-hash")}}
    """
    import re
    files = []
    for filename in iter_files(settings.REPO_PATH, '.jinja'):
        with open(filename, 'r') as f:
            data = f.read()
            for sha1 in re.findall('[a-z0-9]{40}', data):
                if sha1 not in files:
                    files.append(sha1)
    return files
