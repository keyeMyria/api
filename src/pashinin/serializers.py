import datetime
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
from rest_framework import serializers
# from django.http import Http404
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from rest_framework.response import Response
# from rest_framework import status
# from django.utils.timezone import localtime
from django.contrib.auth import get_user_model
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.reverse import reverse
from .models import Course
User = get_user_model()

last_lesson_period = datetime.timedelta(days=8)


class StudentSerializerID(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ('id', 'title', 'code', 'linenos', 'language', 'style')
        fields = ('id', 'first_name')
        depth = 1


class CourseSerializer(serializers.ModelSerializer):
    # schedule = serializers.SerializerMethodField()
    # last_lessons = serializers.SerializerMethodField()
    # schedule = serializers.ReadOnlyField('schedule')

    class Meta:
        model = Course
        fields = ('id', 'name', 'desc')
        # fields = ('id', 'first_name', 'skype', 'phone', 'schedule',
        #           'last_lessons')
        depth = 1

    # def get_schedule(self, user):
    #     return [
    #         {
    #             'day': lesson.start.weekday()+1,
    #             'time': localtime(lesson.start).time(),
    #             'len': lesson.length.total_seconds() // 60,
    #         }
    #         for lesson in user.lessons.filter(
    #                 scheduled=True
    #         )
    #     ]

    # def get_last_lessons(self, user):
    #     return [
    #         {
    #             'id': lesson.pk,
    #             'time': localtime(lesson.start),
    #             'status': lesson.status,
    #             # 'len': lesson.length.total_seconds() // 60,
    #         }
    #         for lesson in user.lessons.filter(

    #         )
    #     ]

    # def validate(self, data):
    #     """
    #     Check that the start is before the stop.
    #     """
    #     if data['start'] > data['finish']:
    #         raise serializers.ValidationError("finish must occur after")
    #     return data


class LessonSerializer(serializers.Serializer):
    # student = serializers.CharField(max_length=200)
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    # uid = serializers.IntegerField()
    student = StudentSerializerID()

    def get_uid(self, user):
        return 123


class ScheduleSerializer(serializers.Serializer):
    day = serializers.SerializerMethodField()
    schedule = LessonSerializer(many=True)
    # last_lessons = serializers.SerializerMethodField()
    # schedule = serializers.ReadOnlyField('schedule')

    def get_day(self, user):
        return "asd"

    def get_last_lessons(self, user):
        return [
            # {
            #     'id': lesson.pk,
            #     'time': localtime(lesson.start),
            #     'status': lesson.status,
            #     # 'len': lesson.length.total_seconds() // 60,
            # }
            # for lesson in user.lessons.filter(

            # )
        ]
