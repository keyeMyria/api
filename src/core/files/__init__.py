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
