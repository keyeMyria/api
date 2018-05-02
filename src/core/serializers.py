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
# from . import reverse
# from .models import User
User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=200)
    # created = serializers.DateTimeField()

    def validate(self, data):
        """Check that email and password are valid"""
        from django.contrib.auth import authenticate
        # if not (username and password):
        #     raise serializers.ValidationError("Enter email and password")

        user = authenticate(
            username=data['email'],
            password=data['password'],
        )
        if user is None:
            raise serializers.ValidationError("Incorrect email or password")
        else:
            data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    # url = serializers.SerializerMethodField()
    # last_lessons = serializers.SerializerMethodField()
    # schedule = serializers.ReadOnlyField('schedule')

    class Meta:
        model = User
        fields = ('pk', 'email', 'is_superuser', 'timezone_str', 'date_joined')
        # fields = ('id', 'first_name', 'skype', 'phone', 'schedule',
        #           'last_lessons')
        # depth = 1

    # def get_url(self, article):
    #     return reverse("articles:article", kwargs={
    #         'id': article.pk,
    #         'slug': article.slug
    #     }, host='pashinin')
