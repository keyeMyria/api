import os
# from pashinin.views import Base as B
from core.views import BaseView as B
from core.files.views import DirView
from core.menu import Menu
from . import faculties
from django.conf import settings
# from core.models import Comment
# from django.http import Http404
from core import reverse
from raven.contrib.django.raven_compat.models import client
# from .models import EduMaterial


baumanka_dir = os.path.join(settings.FILES_ROOT, 'baumanka')


class Base(B):
    template_name = "baumanka.jinja"

    def get_context_data(self, **kwargs):
        c = super(Base, self).get_context_data(**kwargs)
        c['menu'] = Menu([
            ('baumanka', {
                'title': '',  # МГТУ им. Баумана
                'img': reverse(
                    'core:files:file',
                    host=c['host'].name,
                    kwargs={
                        'sha1': 'cb5766f0333ebeb9f3cdb0efad36e141566fa67f'
                    },
                ),
                'url': reverse('index', host=c['host'].name),
            })
        ])
        c['menu']['iu2'] = {
                'title': 'ИУ-2',
                'url': reverse(
                    'kafedra',
                    host=c['host'].name,
                    kwargs={'faculty': 'IU', 'kafedra': 2}
                ),
            }
        c['menu']['bmt1'] = {
            'title': 'БМТ-1',
            'url': reverse(
                'kafedra',
                host=c['host'].name,
                kwargs={'faculty': 'BMT', 'kafedra': 1}
            ),
        }
        c['menu']['iu4'] = {
            'title': 'ИУ-4',
            'url': reverse(
                'kafedra',
                host=c['host'].name,
                kwargs={'faculty': 'IU', 'kafedra': 4}
            ),
        }
        return c


class Baumanka(Base):
    template_name = "baumanka.jinja"

    def get_context_data(self, **kwargs):
        c = super(Baumanka, self).get_context_data(**kwargs)
        c["FS"] = faculties
        return c


class Kafedra(Base):
    template_name = "kafedra.jinja"

    def get_context_data(self, **kwargs):
        c = super(Kafedra, self).get_context_data(**kwargs)
        # c["comments"] = Comment.objects.all()

        if kwargs.get('faculty') != kwargs.get('faculty').upper():
            pass

        faculty = kwargs.get('faculty')
        kafedra = kwargs.get('kafedra')

        try:
            F = faculties[kwargs.get('faculty')]
            c["kafname"] = F['code'] + str(kafedra)
            c["kafurl"] = faculty + str(kafedra)
            c["kaf"] = F[kafedra]

            # c['menu']['iu2'] = {
            #     'title': 'ИУ-2',
            #     'url': reverse(
            #         'kafedra',
            #         host=c['host'].name,
            #         kwargs={'faculty: 'IU', 'kafedra: 2}
            #     ),
            # }
            # c['menu']['bmt1'] = {
            #     'title': 'БМТ-1',
            #     'url': reverse(
            #         'kafedra',
            #         host=c['host'].name,
            #         kwargs={'faculty: 'BMT', 'kafedra: 1}
            #     ),
            # }
            # c['menu']['iu4'] = {
            #     'title': 'ИУ-4',
            #     'url': reverse(
            #         'kafedra',
            #         host=c['host'].name,
            #         kwargs={'faculty: 'IU', 'kafedra: 4}
            #     ),
            # }
            try:
                c['menu'].current = faculty.lower() + str(kafedra)
            except Exception:
                client.captureException()

            # All 12 sems items
            # If there is no such dir - 'have_data' is False
            c["sems"] = [{
                'i': i,
                'have_data': os.path.isdir(
                    os.path.join(
                        baumanka_dir,
                        c["kafurl"],
                        'sem'+str(i)
                    )
                )
            } for i in range(1, 13)]
            if settings.DEBUG:
                for sem in c["sems"]:
                    sem['semdir'] = os.path.join(
                        baumanka_dir,
                        c["kafurl"],
                        'sem'+str(sem['i'])
                    )
        except Exception:
            if settings.DEBUG:
                raise
            else:
                client.captureException()
            c['status'] = 404
            # c['kaf'] = {'title': 'no such kaf'}
        return c


class Sem(Kafedra, DirView):
    template_name = "semestr.jinja"
    d = baumanka_dir

    def get_context_data(self, **kwargs):
        # self.dir is a path for DirView
        self.dir = os.path.join(
            self.d,
            kwargs.get('faculty')+str(kwargs.get('kafedra')),
            'sem'+str(kwargs.get('sem'))
        )
        c = super(Sem, self).get_context_data(**kwargs)

        c['dropzone'] = True
        c['menu'] = Menu(
            [
                (c['kafurl'].lower(), {
                    'title': c["kafname"],
                    'url': reverse(
                        'kafedra',
                        host=c['host'].name,
                        kwargs={
                            'faculty': kwargs.get('faculty'),
                            'kafedra': kwargs.get('kafedra')
                        }
                    ),
                })
            ]
        )
        c['menu'] = Menu([])
        c['menu'] = Menu([
            ('baumanka', {
                'title': c["kafname"],  # МГТУ им. Баумана
                'img': reverse(
                    'core:files:file',
                    host=c['host'].name,
                    kwargs={
                        'sha1': 'cb5766f0333ebeb9f3cdb0efad36e141566fa67f'
                    },
                ),
                'url': reverse(
                    'kafedra',
                    host=c['host'].name,
                    kwargs={
                        'faculty': kwargs.get('faculty'),
                        'kafedra': kwargs.get('kafedra')
                    }
                ),
            })
        ])
        for i in range(1, 13):
            c["menu"]['sem'+str(i)] = {
                'title': str(i),
                'url': reverse(
                    'sem',
                    host=c['host'].name,
                    kwargs={
                        'faculty': kwargs.get('faculty'),
                        'kafedra': kwargs.get('kafedra'),
                        'sem': i,
                        'path': '/'
                    }
                ),
            }
        c['menu'].current = 'sem'+str(kwargs.get('sem'))
        # c['subjects'] = EduMaterial.objects.all()
        return c

    def get(self, request, **kwargs):
        c = self.get_context_data(**kwargs)

        # 'f' is in context when we requested a file (set in DirView)
        if 'f' in c:
            from core.files.sendfile import send_file
            return send_file(c['f'])
        else:
            if os.path.isdir(c['dir']) and not request.path.endswith('/'):
                from django.shortcuts import redirect
                return redirect(request.path+'/')
            return self.render_to_response(c, status=c['status'])


class Practice(Kafedra):
    template_name = "practice.jinja"
