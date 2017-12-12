from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, ScheduleViewSet


router = DefaultRouter(trailing_slash=False)
router.register(r'students', StudentViewSet, 'student')
router.register(r'schedule', ScheduleViewSet, 'schedule')

app_name = 'api'
urlpatterns = (router.urls, 'api')
