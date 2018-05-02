import os
# from pashinin.views import Base as B
from core.views import BaseView as B
from core.files.views import DirView
from core.menu import Menu
from . import faculties
from .forms import AddFacultyForm
from django.conf import settings
from django.http import JsonResponse
# from core.models import Comment
# from django.http import Http404
from edu.models import Organization, Faculty, Department, Period
from core import reverse
from raven.contrib.django.raven_compat.models import client
# from .models import EduMaterial
# from channels import Channel


if isinstance(settings.FILES_ROOT, str):
    baumanka_dir = os.path.join(settings.FILES_ROOT, 'baumanka')
else:
    baumanka_dir = os.path.join(settings.FILES_ROOT[0], 'baumanka')


class Base(B):
    template_name = "baumanka.jinja"

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)

        c['org'], new = Organization.objects.get_or_create(
            title='МГТУ им. Баумана'
        )
        # if not c['org'].location_str:
        #     c['org'].location_str = 'Россия, Москва'
        #     c['org'].save()

        for code in ['IU', 'RL', 'RK', 'BMT']:
            f, new = Faculty.objects.get_or_create(
                code=faculties[code]['code'],
                title=faculties[code]['title'],
                university=c['org'],
            )
            # add departments
            for K in faculties[code].get('kafs', []):
                # print(
                #     faculties[code]['code']+str(K),
                #     faculties[code][K]['title']
                # )
                dep_code = faculties[code]['code']+str(K)
                name = faculties[code][K]['title']
                d, new = Department.objects.get_or_create(
                    code=dep_code,
                    title=name,
                    university=c['org'],
                    faculty=f,
                )
                if not d.code_slug:
                    d.save()

        c['menu'] = Menu([
            ('faculties', {
                'title': 'Факультеты',
                # 'img': reverse(
                #     'core:files:file',
                #     host=c['host'].name,
                #     kwargs={
                #         'sha1': 'cb5766f0333ebeb9f3cdb0efad36e141566fa67f'
                #     },
                # ),
                'url': reverse('index', host=c['host'].name),
            })
        ])
        c['menu']['iu2'] = {
                'title': 'ИУ-2',
                'url': reverse(
                    'kafedra',
                    host=c['host'].name,
                    # kwargs={'faculty': 'IU', 'kafedra': 2}
                    kwargs={'dpt_code': 'iu2'}
                ),
            }
        c['menu']['bmt1'] = {
            'title': 'БМТ-1',
            'url': reverse(
                'kafedra',
                host=c['host'].name,
                kwargs={'dpt_code': 'bmt1'}
            ),
        }
        c['menu']['iu4'] = {
            'title': 'ИУ-4',
            'url': reverse(
                'kafedra',
                host=c['host'].name,
                kwargs={'dpt_code': 'iu4'}
            ),
        }
        return c


class Baumanka(Base):
    template_name = "baumanka.jinja"

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c["FS"] = faculties
        c['faculties'] = c['org'].faculties.filter(published=True)
        c["menu"].current = 'faculties'
        c['AddFacultyForm'] = AddFacultyForm()
        return c

    def post(self, request, **kwargs):
        from .forms import AddFacultyForm
        f = AddFacultyForm(request.POST)
        if f.is_valid():
            # Channel('send-me-lead').send(f.cleaned_data)
            return JsonResponse({
                'code': 0
            })
        else:
            return JsonResponse({
                'errors': f.errors,
            })
        # content_type='application/json'


class Kafedra(Base):
    """Department (Кафедра)"""
    template_name = "kafedra.jinja"

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        # c["comments"] = Comment.objects.all()

        # if kwargs.get('faculty') != kwargs.get('faculty').upper():
        #     pass

        # faculty = kwargs.get('faculty')
        dpt_code = kwargs.get('dpt_code')
        c['department'] = None

        try:
            c['department'] = Department.objects.get(
                code_slug=dpt_code
            )
            # F = faculties[kwargs.get('faculty')]
            # c["kafname"] = F['code'] + str(kafedra)
            # c["kafurl"] = faculty + str(kafedra)
            # c["kaf"] = F[kafedra]

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
            # try:
            # c['menu'].current = faculty.lower() + str(kafedra)
            c['menu'].current = dpt_code
            # except Exception:
            #     client.captureException()

            # All 12 sems items
            # If there is no such dir - 'have_data' is False
            c["sems"] = []
            for i in range(1, 13):
                have_sem_dir = os.path.isdir(
                    os.path.join(
                        baumanka_dir,
                        dpt_code.upper(),
                        'sem'+str(i)
                    )
                )
                if have_sem_dir:
                    c["sems"].append({
                        'i': i,
                        'have_data': have_sem_dir,
                    })

            for sem in c["sems"]:
                if sem['have_data']:
                    name = 'Семестр '+str(sem['i'])
                    p, new = Period.objects.get_or_create(
                        name=name,
                        department=c['department'],
                    )

            if settings.DEBUG:
                for sem in c["sems"]:
                    sem['semdir'] = os.path.join(
                        baumanka_dir,
                        dpt_code.upper(),
                        'sem'+str(sem['i'])
                    )
        except Exception:
            if settings.DEBUG:
                pass
                # raise
            else:
                client.captureException()
            c['status'] = 404
            # c['kaf'] = {'title': 'no such kaf'}
        return c


class PeriodView(Kafedra, DirView):
    """Period of time for a student.

    Semester

    """
    template_name = "semestr.jinja"
    d = baumanka_dir

    def get_context_data(self, **kwargs):
        # self.dir is a path for DirView
        period_code = kwargs.get('period_code', 'semestr-1')
        self.dir = os.path.join(
            self.d,
            kwargs.get('dpt_code').upper(),
            # 'sem'+kwargs.get('period_code','').split('-')[1]
            period_code,
        )
        try:
            if not os.path.isdir(self.dir):
                self.dir = os.path.join(
                    self.d,
                    kwargs.get('dpt_code').upper(),
                    'sem'+period_code.split('-')[-1],
                )
        except Exception:
            pass

        c = super().get_context_data(**kwargs)

        try:
            c['period'] = Period.objects.get(
                slug=kwargs.get('period_code'),
                department=c['department'],
            )
        except Period.DoesNotExist:
            c['status'] = 404

        c['dropzone'] = True
        c['menu'] = Menu(
            [
                # (c['kafurl'].lower(), {
                (c['dpt_code'], {
                    'title': c["department"].code,
                    'url': reverse(
                        'kafedra',
                        host=c['host'].name,
                        kwargs={
                            # 'faculty': kwargs.get('faculty'),
                            # 'kafedra': kwargs.get('kafedra')
                            'dpt_code': kwargs.get('dpt_code'),
                        }
                    ),
                })
            ] if c["department"] else []
        )
        c['menu'] = Menu([])
        c['menu'] = Menu([
            ('baumanka', {
                'title': c["org"].title,  # МГТУ им. Баумана
                'img': reverse(
                    'files:file',
                    host=c['host'].name,
                    kwargs={
                        'sha1': 'cb5766f0333ebeb9f3cdb0efad36e141566fa67f'
                    },
                ),
                'url': reverse(
                    'kafedra',
                    host=c['host'].name,
                    kwargs={
                        # 'faculty': kwargs.get('faculty'),
                        # 'kafedra': kwargs.get('kafedra'),
                        'dpt_code': kwargs.get('dpt_code'),
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
                        'dpt_code': kwargs.get('dpt_code'),
                        'period_code': 'semestr-'+str(i),
                        # 'sem': i,
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
