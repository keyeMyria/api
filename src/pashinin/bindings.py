from django.core.paginator import Paginator
from channels_api.bindings import ResourceBinding
from .models import Course
from .serializers import CourseSerializer, StudentSerializer
from channels_api.decorators import list_action, detail_action
from django.contrib.auth import get_user_model
User = get_user_model()


class CourseBinding(ResourceBinding):
    model = Course
    stream = "courses"
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class StudentBinding(ResourceBinding):
    model = User
    stream = "students"
    serializer_class = StudentSerializer
    queryset = User.objects.all()

    @list_action()
    def list(self, data, **kwargs):
        """List my students.

        Return only students that I had lessons with in the last 4 weeks

        """
        if not data:
            data = {}
        queryset = self.get_queryset().filter(
            # published=True
        )
        p = Paginator(queryset, 100)
        data = p.page(1)
        serializer = self.get_serializer(data, many=True)
        return serializer.data, 200
