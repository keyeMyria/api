import os
from pashinin.views import Base
from core.files.views import DirView
from . import faculties
from django.conf import settings
# from core.models import Comment
from django.core.urlresolvers import reverse

baumanka_dir = '/mnt/files/baumanka/'


class Baumanka(Base):
    template_name = "baumanka.jinja"

    def get_context_data(self, **kwargs):
        c = super(Baumanka, self).get_context_data(**kwargs)
        c["FS"] = faculties
        c['menu'] = {
            # 'parent': {
            #     'title': c['kafname'],
            #     # 'url': reverse("baumanka:kafedra", F=kwargs.get('F'), K=kwargs.get('K'))
            #     'url': reverse("baumanka:index")
            # },
            'items': [
                {
                    'title': 'Бауманка',
                    'url': reverse("baumanka:index"),
                }
            ]
        }
        return c


class Kafedra(Base):
    template_name = "kafedra.jinja"

    def get_context_data(self, **kwargs):
        c = super(Kafedra, self).get_context_data(**kwargs)
        # c["comments"] = Comment.objects.all()
        c['menu']['items'] = [
            {
                'title': 'Бауманка',
                'url': reverse("baumanka:index"),
            }
        ]
        if kwargs.get('F') != kwargs.get('F').upper():
            pass
        try:
            F = faculties[kwargs.get('F')]
            c["kafname"] = F['code']+kwargs.get('K')
            c["kafurl"] = kwargs.get('F')+kwargs.get('K')
            c["kaf"] = F[int(kwargs.get('K'))]
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
        except:
            c['status'] = 404
            # c['kaf'] = {'title': 'no such kaf'}
        return c


class Sem(Kafedra, DirView):
    template_name = "semestr.jinja"
    d = os.path.join(settings.FILES_ROOT, 'baumanka')

    def get_context_data(self, **kwargs):
        # self.dir is a path for DirView
        self.dir = os.path.join(
            self.d,
            kwargs.get('F')+kwargs.get('K'), 'sem'+kwargs.get('sem'))
        c = super(Sem, self).get_context_data(**kwargs)
        c['menu'] = {
            'cls': 'equal',
            'items': []
        }

        # All sems items in menu
        for sem in c['sems']:
            c['menu']['items'] += [
                {
                    'title': '{}'.format(sem['i']),
                    # 'url': reverse("index"),
                    'url': reverse("baumanka:sem", kwargs={
                        'F': c['F'],
                        'K': c['K'],
                        'sem': sem['i']
                    }),
                }
            ]
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
