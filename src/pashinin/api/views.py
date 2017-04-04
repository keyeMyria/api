"""
ViewSets have methods:

    def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass

"""


import datetime
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now, localtime
from django.contrib.auth import get_user_model
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


class StudentViewSet2(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = StudentSerializer
    queryset = User.objects.all()


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
        except:
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
