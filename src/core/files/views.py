import json
import os
from core.views import BaseView
from .sendfile import send_file
from .models import BaseFile as File, UploadedFile
from core import now
from .tasks import ensure_fs_ready
from .forms import UploadedFileForm
from django.http import HttpResponse, HttpResponseNotFound
# from django.db.models import Count
from django.conf import settings
# from django.utils.translation import gettext_lazy as _
# from django.core.urlresolvers import reverse
from os.path import isfile, isdir, join
from . import files_used_in_this_repo


class FileView(BaseView):
    def get(self, request, **kwargs):
        download = 'd' in self.request.GET  # Download or display in a browser
        sha1 = kwargs.get('sha1', None)
        try:
            f = File.objects.get(sha1=sha1)
            return send_file(f, attachment=download)
        except File.DoesNotExist:
            #
            # If there is no info in a DB about this file return file
            # anyway (if exists) and then run a task to process file and
            # add to DB.
            #
            filename = os.path.join(
                settings.FILES_ROOT,
                sha1[:3],
                sha1[3:6],
                sha1[6:]
            )
            if os.path.isfile(filename):
                # TODO: run task to add file info to DB
                return send_file(filename, attachment=download)
            else:
                return HttpResponseNotFound(
                    "No such file {}".format(
                        filename if settings.DEBUG else ""))


# c['uploads'] = UploadFile.objects.all().annotate(
#             null_position=Count('date_uploaded')).order_by('-null_position',
#             '-date_uploaded')

class DownloadCore(BaseView):
    def post(self, request, **kwargs):
        if not settings.DEBUG:
            return HttpResponse('[]', content_type='application/json')

        ensure_fs_ready()

        files = files_used_in_this_repo()  # sha1 list
        for f in files:
            url = 'https://pashinin.com/_/files/{}'.format(f)
            File.from_url(url)

        return HttpResponse(json.dumps({
            'dir': settings.REPO_PATH,
            'files': json.dumps(files),
            'len': len(files)
        }), content_type='application/json')


class Upload(BaseView):
    def post(self, request, **kwargs):
        ensure_fs_ready()
        ctx = self.get_context_data(**kwargs)
        user = ctx['user']
        form = UploadedFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = UploadedFile(file=request.FILES['file'])

            # Uploader should have access to his file
            # Save it in a session for Anons
            if user.is_anonymous:
                if 'files' not in request.session:
                    # request.session['files'] = [upload_md5]
                    pass
                else:
                    # request.session['files'] += [upload_md5]
                    pass
            else:
                new_file.uploader = user

            new_file.save()
            from .tasks import move_upload_to_files
            f = move_upload_to_files(new_file)

            # 'BaseFile' object has no attribute 'uploader'
            # if not f.uploader and user is not None and not user.is_anonymous:
            #     f.uploader = user
            #     f.save()

            # TODO: optimize uploaded JPGs
            #
            # jpegtran -copy none -optimize -perfect inputimage.jpg >
            # outputimage.jpg

            # user.avatar = Image.from_file(f)
            return HttpResponse(json.dumps({
                'url': f.get_absolute_url(),
                'id': f.pk,
                'sha1': f.sha1
            }), content_type='application/json')
        else:  # upload form is not valid
            return HttpResponse(json.dumps({'errors': form.errors}),
                                content_type='application/json')

        for key in request.FILES:
            f = request.FILES[key]
            upload = UploadedFile(file=f)
            # upload_md5 = upload.get_md5()
            upload.date_uploaded = now()
            if f.multiple_chunks():  # file is already on disk
                upload.save()
            else:
                # check if this md5 was already uploaded
                prevUpload = upload.uploaded_earlier
                if prevUpload:
                    upload = prevUpload
                else:
                    upload.save()

        # The file is uploaded, it is now for example:
        #
        # /mnt/files/uploads/2016/06/28/dropzone_NaLkPzK.css
        #
        # Upload directory:
        # MEDIA_ROOT = os.path.join(FILES_ROOT, 'uploads/')
        #
        # TODO: process uploaded file
        # upload.process()
        return HttpResponse(json.dumps({'url': upload.url}))


class Files(BaseView):
    template_name = "core_files.jinja"

    def get_context_data(self, **kwargs):
        c = super(Files, self).get_context_data(**kwargs)

        c['files_count'] = File.objects.count()
        c['files'] = File.objects.filter().order_by('-added')[:10]
        c['dropzone'] = True
        c['timeago'] = True

        # Check mountpoint
        import psutil
        c['mounted'] = False
        for p in psutil.disk_partitions(True):
            if p.mountpoint == settings.FILES_ROOT:
                c['mounted'] = True
                break

        return c


class DirView(BaseView):
    template_name = "cms_files_dirview.jinja"
    dir = None

    def get_context_data(self, **kwargs):
        c = super(DirView, self).get_context_data(**kwargs)
        c['files'] = []
        c['dirs'] = []
        path = kwargs.get('path', '')
        if path is None:
            path = ''

        # levels - ['path', 'to', 'dir']
        # paths - ['path', 'path/to', 'path/to/dir']
        c['levels'] = path.strip('/').split('/')
        c['paths'] = list(c['levels'])
        try:
            c['levels'].remove('')
        except ValueError:
            pass
        for ind, el in enumerate(c['levels']):
            sublist = c['levels'][0:ind+1]
            c['paths'][ind] = os.path.join(*sublist)

        j = os.path.join(self.dir, path)
        d = c['dir'] = os.path.realpath(j)

        if self.dir is None or \
           not os.path.isdir(self.dir):
            return c

        if os.path.isdir(d):
            L = os.listdir(d)
            c['dirs'] = sorted([f for f in L if isdir(join(d, f))])
            c['files'] = sorted([f for f in L if isfile(join(d, f))])

            for ind, f in enumerate(c['files']):
                c['files'][ind] = {
                    'name': f,
                    'size': os.path.getsize(join(d, f))
                }
        elif os.path.isfile(d):
            c['f'] = d
        else:
            c['status'] = 404
        return c
