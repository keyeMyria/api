from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, ScheduleViewSet, TokenObtainPairView
from core.views import UsersViewSet
from rest_framework.schemas import get_schema_view
from django.urls import path
from rest_framework_simplejwt.views import (
    # TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter(trailing_slash=False)
router.register(r'social', StudentViewSet, 'social')
router.register(r'schedule', ScheduleViewSet, 'schedule')
router.register(r'users', UsersViewSet, 'users')

# app_name = 'api'
# urlpatterns = (router.urls, 'api')
urlpatterns = [
    # path('/', get_schema_view()),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
# + router.urls
