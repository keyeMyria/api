import datetime
from core.views import BaseView
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now, localtime
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.reverse import reverse
from rest_framework import viewsets
# from rest_framework.decorators import detail_route, list_route
from pashinin.views import Day
from .serializers import StudentSerializer, ScheduleSerializer
import logging

log = logging.getLogger(__name__)
User = get_user_model()

last_lesson_period = datetime.timedelta(days=8)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['su'] = user.is_superuser
        # ...

        return token


class TokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         'students': reverse('api:students', request=request, format=format),
#        # 'schedule': reverse('api:schedule', request=request, format=format),
#        # 'snippets': reverse('snippet-list', request=request, format=format)
#     })


class Students(APIView):
    """
    List all students, or create a new one.
    """
    permission_classes = (IsAdminUser,)

    def get(self, request, format=None):
        utcnow = localtime(now())
        students = User.objects.filter(
            lessons__start__gt=utcnow-last_lesson_period
        ).distinct()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# viewsets.ModelViewSet
# class StudentViewSet(viewsets.ViewSet):
class StudentViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        utcnow = localtime(now())
        return User.objects.filter(
            lessons__start__gt=utcnow-last_lesson_period
        ).distinct()
        # return self.request.user.accounts.all()

    # def list(self, request):
    #     utcnow = localtime(now())
    #     queryset = User.objects.filter(
    #         lessons__start__gt=utcnow-last_lesson_period
    #     ).distinct()
    #     serializer = StudentSerializer(queryset, many=True)
    #     return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     utcnow = localtime(now())
    #     queryset = User.objects.filter(
    #         lessons__start__gt=utcnow-last_lesson_period
    #     ).distinct()
    #     serializer = StudentSerializer(queryset, many=True)
    #     return Response(serializer.data)


class ScheduleViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser]

    # def get_queryset(self):
    #     utcnow = localtime(now())
    #     return User.objects.filter(
    #         lessons__start__gt=utcnow-last_lesson_period
    #     ).distinct()
    #     # return self.request.user.accounts.all()

    def list(self, request):
        serializer = ScheduleSerializer(Day(localtime(now())))
        return Response(serializer.data)

    # @detail_route(permission_classes=[IsAdminUser])
    def retrieve(self, request, pk=None):
        try:
            date = datetime.datetime.strptime(pk, "%Y-%m-%d").date()
        except Exception:
            return Response("failed to get date object from: {}".format(pk))

        serializer = ScheduleSerializer(Day(date))
        # return Response(serializer.data['schedule'])
        return Response(serializer.data)

        utcnow = localtime(now())
        queryset = User.objects.filter(
            lessons__start__gt=utcnow-last_lesson_period
        ).distinct()
        serializer = StudentSerializer(queryset, many=True)
        # log.debug(serializer.data)
        return Response(serializer.data['lessons'])


class Login2(
        # EnsureCsrfCookieMixin,
        BaseView,
):
    template_name = "core_login.jinja"

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c['menu'] = {}
        # c['form'] = LoginForm
        return c

    def get(self, request, **kwargs):
        c = self.get_context_data(**kwargs)
        if request.user.is_authenticated:  # and not request.user.is_lazy:
            return HttpResponseRedirect(reverse("index", host=c['host'].name))
        else:
            return self.render_to_response(c, status=c['status'])

    def post(self, request, **kwargs):
        c = self.get_context_data(**kwargs)
        f = LoginForm(request.POST)
        record = LoginAttempt(ip=c['ip'])
        if f.is_valid():
            login(request, f.cleaned_data['user'])
            record.user = f.cleaned_data['user']
            record.save()
            return JsonResponse({'code': 0})
        else:
            log.debug(f.errors)
            record.login = f.cleaned_data['username']
            record.password = f.cleaned_data['password']
            record.save()
            return JsonResponse({'errors': f.errors})
