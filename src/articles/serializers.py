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
from .models import Article
User = get_user_model()


class ArticleSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    url = serializers.SerializerMethodField()
    # last_lessons = serializers.SerializerMethodField()
    # schedule = serializers.ReadOnlyField('schedule')

    class Meta:
        model = Article
        fields = ('pk', 'title', 'html', 'cut_html', 'slug', 'url',
                  'author', 'published', 'added')
        # depth = 1

    def get_url(self, article):
        return reverse("articles:article", kwargs={
            'id': article.pk,
            'slug': article.slug
        }, host='pashinin')
