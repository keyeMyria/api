# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
from rest_framework import serializers
# from django.http import Http404
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from rest_framework.response import Response
# from rest_framework import status
from django.contrib.auth import get_user_model
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.reverse import reverse
from core import reverse
from .models import Organization, Faculty, Task
User = get_user_model()


class OrgSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    url = serializers.SerializerMethodField()
    # last_lessons = serializers.SerializerMethodField()
    # schedule = serializers.ReadOnlyField('schedule')

    class Meta:
        model = Organization
        fields = ('pk', 'title', 'html', 'cut_html', 'slug', 'url',
                  'author', 'published', 'added')
        # depth = 1

    def get_url(self, article):
        return reverse("articles:article", kwargs={
            'id': article.pk,
            'slug': article.slug
        }, host='pashinin')


class FacultySerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    # url = serializers.SerializerMethodField()
    # last_lessons = serializers.SerializerMethodField()
    # schedule = serializers.ReadOnlyField('schedule')

    class Meta:
        model = Faculty
        fields = ('pk', 'code', 'title', 'university')
        # depth = 1

    def get_url(self, article):
        return reverse("articles:article", kwargs={
            'id': article.pk,
            'slug': article.slug
        }, host='pashinin')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('pk', 'as_html')
        # depth = 1


class TaskEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('pk', 'text')
        # depth = 1
