from django.core.paginator import Paginator
from channels_api.bindings import ResourceBinding
from channels_api.permissions import BasePermission
from .models import Exam
# from .serializers import (OrgSerializer, FacultySerializer, TaskSerializer,
#                           TaskEditSerializer)
from .serializers import ExamSerializer
from channels_api.decorators import list_action, detail_action
from rest_framework.exceptions import NotFound
from core.permissions import AllowCreate


class IsAuthor(BasePermission):
    def has_permission(self, user, action, pk):
        if action == "delete":
            try:
                article = Article.objects.get(pk=pk)
                return article.author == user
            except Exception:
                return False
        else:
            return False
        # if action == "subscribe":
        #     return True
        # return False


class ExamBinding(ResourceBinding):
    model = Exam
    stream = "exams"
    serializer_class = ExamSerializer
    queryset = Exam.objects.filter()
    # permission_classes = (IsAuthor, )

    @list_action()
    def list(self, data, **kwargs):
        if not data:
            data = {}
        queryset = self.get_queryset().filter(published=True)
        p = Paginator(queryset, 10)
        data = p.page(1)
        serializer = self.get_serializer(data, many=True)
        return serializer.data, 200

    @list_action()
    def myexams(self, data, **kwargs):
        if not data:
            data = {}
        queryset = self.get_queryset().filter(
            # published=True
        )
        p = Paginator(queryset, 10)
        data = p.page(1)
        serializer = self.get_serializer(data, many=True)
        return serializer.data, 200

    @list_action()
    def create(self, data, **kwargs):
        d = data
        d['author'] = self.user.pk
        serializer = self.get_serializer(data=d)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data, 201

    @list_action()
    def drafts(self, data=None, **kwargs):
        if self.user is None:
            raise NotFound

        qs = self.get_queryset().filter(
            published=False,
            author=self.user
        )  # .build_report()
        paginator = Paginator(qs, 10)
        data = paginator.page(1)
        serializer = self.get_serializer(data, many=True)
        # ordered_dict =
        # print(paginator.count)
        # ordered_dict['total'] = paginator.count
        return {
            'items': serializer.data,
            'pages': paginator.num_pages,
            'count': paginator.count,
        }, 200
        # return report, 200
