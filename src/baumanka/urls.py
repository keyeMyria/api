from django.conf.urls import include, url
from .views import *


urlpatterns = [
    url(r'^$',  Baumanka.as_view(), name="index"),
    url(r'^(?P<F>\w+?)(?P<K>\d+)/$', Kafedra.as_view(), name="kafedra"),
    url(r'^(?P<F>\w+?)(?P<K>\d+)/practice$',
        Practice.as_view(), name="practice"),
    # url(r'^(?P<F>\w+?)(?P<K>\d+)/sem(?P<sem>\d+)/$',  Sem.as_view(), name="sem"),
    url(r'^(?P<F>\w+?)(?P<K>\d+)/sem(?P<sem>\d+)/(?:(?P<path>.*)/?)?$',
        Sem.as_view(), name="sem"),
    # url(r'^(?P<F>.+)(?P<id>\d+)/', include(faculty.urls, namespace='faculty')),
]
