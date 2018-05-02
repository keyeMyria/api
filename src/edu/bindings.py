from django.core.paginator import Paginator
from channels_api.bindings import ResourceBinding
from channels_api.permissions import BasePermission
from .models import Organization, Faculty, Task
from .serializers import (OrgSerializer, FacultySerializer, TaskSerializer,
                          TaskEditSerializer)
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


class UniversityBinding(ResourceBinding):
    model = Organization
    stream = "university"
    serializer_class = OrgSerializer
    queryset = Organization.objects.filter()
    permission_classes = (IsAuthor, )

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


class FacultyBinding(ResourceBinding):
    model = Faculty
    stream = "faculty"
    serializer_class = FacultySerializer
    queryset = Faculty.objects.filter()
    permission_classes = (
        AllowCreate,
        # IsAuthor,
    )

    # @list_action()
    # def list(self, data, **kwargs):
    #     if not data:
    #         data = {}
    #     queryset = self.get_queryset().filter(published=True)
    #     p = Paginator(queryset, 10)
    #     data = p.page(1)
    #     serializer = self.get_serializer(data, many=True)
    #     return serializer.data, 200

    @list_action()
    def create(self, data, **kwargs):
        d, code = super().create(data, **kwargs)
        from core import notify
        notify.superusers('Добавлен факультет '+str(d))
    #     d = data
    #     # d['author'] = self.user.pk
    #     serializer = self.get_serializer(data=d)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     # from channels import Channel
    #     # Channel('send-me-lead').send({
    #     #     'name': 'aaa',
    #     #     'phone': '11111',
    #     #     'message': 'ww',
    #     # })
    #     return serializer.data, 201

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


class TaskBinding(ResourceBinding):
    model = Task
    stream = "tasks"
    serializer_class = TaskSerializer
    queryset = Task.objects.filter()
    permission_classes = (
        AllowCreate,
        # IsAuthor,
    )

    # @list_action()
    # def list(self, data, **kwargs):
    #     if not data:
    #         data = {}
    #     queryset = self.get_queryset().filter(published=True)
    #     p = Paginator(queryset, 10)
    #     data = p.page(1)
    #     serializer = self.get_serializer(data, many=True)
    #     return serializer.data, 200

    @detail_action()
    def edit(self, pk, **kwargs):
        instance = self.get_object_or_404(pk)
        serializer = TaskEditSerializer(instance)
        return serializer.data, 200
        # return {'asd': 123}, 200

    @list_action()
    def create(self, data, **kwargs):
        serializer_data, code = super().create(data, **kwargs)
        from core import notify
        notify.superusers('Добавлен факультет '+str(serializer_data))
    #     d = data
    #     # d['author'] = self.user.pk
    #     serializer = self.get_serializer(data=d)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     # from channels import Channel
    #     # Channel('send-me-lead').send({
    #     #     'name': 'aaa',
    #     #     'phone': '11111',
    #     #     'message': 'ww',
    #     # })
    #     return serializer.data, 201

    @list_action()
    def search(self, data, **kwargs):
        if not data:
            data = {}
        # queryset = self.get_queryset().filter(published=True)
        queryset = self.filter_queryset(self.get_queryset()).filter(
            text__icontains=data.get('query', '')
        )
        # searchCount = queryset.count()
        total = self.filter_queryset(self.get_queryset()).count()

        paginator = Paginator(queryset, 10)
        page = data.get('page', 1)
        data = paginator.page(page)
        serializer = self.get_serializer(data, many=True)
        return {
            'items': serializer.data,
            # 'searchCount': searchCount,
            'searchCount': paginator.count,
            'page': page,
            'pages': paginator.num_pages,
            # 'total': total,
            'total': total,
        }, 200

    @list_action()
    def generate(self, data, **kwargs):
        """TODO: generate 30 objects."""
        if not data:
            data = {}

        # count = data.get('count', 30)
        queryset = self.filter_queryset(self.get_queryset()).filter(
            text__icontains=data.get('query', '')
        )
        # searchCount = queryset.count()
        total = self.filter_queryset(self.get_queryset()).count()

        paginator = Paginator(queryset, 10)
        page = data.get('page', 1)
        data = paginator.page(page)
        serializer = self.get_serializer(data, many=True)
        return {
            'items': serializer.data,
            # 'searchCount': searchCount,
            'searchCount': paginator.count,
            'page': page,
            'pages': paginator.num_pages,
            # 'total': total,
            'total': total,
        }, 200
