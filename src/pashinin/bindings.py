
from channels_api.bindings import ResourceBinding

from .models import Course
from .serializers import CourseSerializer


class CourseBinding(ResourceBinding):
    model = Course
    stream = "courses"
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
