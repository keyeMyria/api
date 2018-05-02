# import core
from django.urls import include, path
# from tastypie.api import Api
from django.contrib import admin
from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from graphene_django.views import GraphQLView
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from core.views import UsersViewSet
# from .views import StudentViewSet, ScheduleViewSet
# from tastypie.resources import ModelResource
# from api.models import Note
# from tastypie.authorization import Authorization
# from allauth.socialaccount.models import SocialApp


# class SocialAppResource(ModelResource):
#     class Meta:
#         queryset = SocialApp.objects.all()
#         resource_name = 'socialapp'
#         authorization = Authorization()
#         # fields = ['title', 'body']


# v1_api = Api(api_name='v1')
# v1_api.register(SocialAppResource())


router = DefaultRouter(trailing_slash=False)
# router.register(r'social', StudentViewSet, 'social')
# router.register(r'schedule', ScheduleViewSet, 'schedule')
router.register(r'users', UsersViewSet, 'users')

# app_name = 'api'
# urlpatterns = (router.urls, 'api')
urlpatterns = router.urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('csrf', ensure_csrf_cookie(lambda r: HttpResponse('OK'))),
    path('auth/', include('auth.urls')),
    # path('auth/jwt/', obtain_jwt_token),
    # path('accounts/', include('allauth.urls')),
    # path('accounts/', include('accounts.urls')),

    # *core.urls.urlpatterns,
    # path('', include(v1_api.urls)),

    # path('accounts/', include('allauth.urls')),
    path('graphql', GraphQLView.as_view(graphiql=settings.DEBUG)),
    *router.urls,
]
