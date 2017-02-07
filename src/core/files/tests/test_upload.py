import os
import pytest
# import os
# from core.tests import travis
# from django.core.urlresolvers import reverse
# from django.conf import settings
# from unittest import skip

# FILE_UPLOAD_MAX_MEMORY_SIZE = settings.FILE_UPLOAD_MAX_MEMORY_SIZE
# FILE_UPLOAD_TEMP_DIR = settings.FILE_UPLOAD_TEMP_DIR
# MEDIA_URL = settings.MEDIA_URL


# class Upload(CommonTest):
#     # @skip("for now")
#     # def test_upload_create_model(self):
#     #     upload = UploadFile(file="f")
#     #     upload.uploader = self._superuser
#     #     upload.save()

#     @skip("for now")
#     @travis
#     def test_upload_http(self):
#         fname = os.path.join(settings.SITE_PATH,
#                              "static/public/other/torvalds-says-linux.ogg")
#         self.F.url = reverse("files:upload")
#         json = self.F.json

#         def test_upload(user):
#             with open(fname, 'rb') as fp:
#                 r = json({'attachment': fp})  # Upload
#                 url = r['url']
#                 r = self.c.get(url)
#                 self.assertEqual(
#                     r.status_code, 200,
#                     str(user) +
#                     " should have access to the uploaded file %s" % url)
#                 # others must not have access
#                 self.anon()
#                 r = self.c.get(url)
#                 self.assertEqual(
#                     r.status_code, 404,
#                     "Others must NOT have access to the uploaded file %s"
#                     % url)

#                 # remove an uploaded file (we are testing here)
#                 filename = os.path.join(
#                     FILE_UPLOAD_TEMP_DIR,
#                     url[len(MEDIA_URL):]
#                 )
#                 return filename

#         self.anon()
#         test_upload("Anon")
#         self.superuser()
#         os.remove(test_upload("Superuser"))

#         # generate a big enough file, 3Mb
#         fname = "/tmp/123bigfile123"
#         with open(fname, "w") as f:
#             f.truncate(FILE_UPLOAD_MAX_MEMORY_SIZE+1)
#             # TODO: handle big files in upload get_md5

#         self.anon()
#         test_upload("Anon")
#         self.superuser()
#         os.remove(test_upload("Superuser"))
#         os.remove(fname)
cd = os.path.dirname(os.path.abspath(__file__))
assets = os.path.join(cd, 'assets')


@pytest.mark.django_db
def test_upload(client):
    with open(os.path.join(assets, 'text.txt')) as fp:
        r = client.post(
            '/_/files/upload',
            data={
                'name': 'file',
                'file': fp
            },
            # content_type='application/json'
        )
        assert r.status_code == 200
        assert r.json()['sha1'] == 'a8fdc205a9f19cc1c7507a60c4f01b13d11d7fd0'

    # downloading
    r2 = client.get('/_/files/' + r.json()['sha1'])
    assert r2.status_code == 200
