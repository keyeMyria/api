import logging
import graphene
import django_filters
from graphene import relay, ObjectType
from django_filters import OrderingFilter
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.rest_framework.mutation import SerializerMutation
from .serializers import FacultySerializer
# from graphene.contrib.django import DjangoNode
# from graphene.contrib.django.filter import (
#     GlobalIDFilter, DjangoFilterConnectionField,
#     GlobalIDMultipleChoiceFilter
# )
from .models import Task, Faculty, Department, Organization, Period
LOG = logging.getLogger(__name__)


# Filters

class FacultyFilter(django_filters.FilterSet):
    class Meta:
        model = Faculty
        fields = ['university', 'code', 'published']
    order_by = OrderingFilter(fields=('code',))


class DepartmentFilter(django_filters.FilterSet):
    class Meta:
        model = Department
        fields = ['university', 'faculty', 'code_slug']
    order_by = OrderingFilter(fields=('code',))


class PeriodFilter(django_filters.FilterSet):
    class Meta:
        model = Period
        fields = ['department', 'slug']
    order_by = OrderingFilter(fields=('name',))


class OrganizationFilter(django_filters.FilterSet):
    class Meta:
        model = Organization
        fields = ['title']
    order_by = OrderingFilter(fields=('title',))


# Nodes

class PeriodNode(DjangoObjectType):
    department = DjangoFilterConnectionField(
        lambda: DepartmentNode,
        filterset_class=DepartmentFilter,
    )
    class Meta:
        model = Period
        interfaces = (relay.Node, )
        filter_fields = ['slug', 'name', 'department']


class DepartmentNode(DjangoObjectType):
    periods = DjangoFilterConnectionField(
        PeriodNode,  # lambda: DepartmentNode (if Node is defined later)
        filterset_class=PeriodFilter,
    )
    class Meta:
        model = Department
        interfaces = (relay.Node, )
        filter_fields = ['university', 'faculty', 'code_slug']


class FacultyNode(DjangoObjectType):
    departments = DjangoFilterConnectionField(
        DepartmentNode,  # lambda: DepartmentNode (if Node is defined later)
        filterset_class=DepartmentFilter,
    )
    # university2 = relay.Node.Field(OrganizationNode)
    university = DjangoFilterConnectionField(
        lambda: OrganizationNode,
        # filterset_class=DepartmentFilter,
    )

    class Meta:
        model = Faculty
        interfaces = (relay.Node, )
        filter_fields = ['university', 'departments']
        # fields = ['departments']

    @classmethod
    def get_node(cls, id, context, info):
        try:
            node = cls._meta.model.objects.get(id=id)
        except cls._meta.model.DoesNotExist:
            return None

        # if node.published or context.user == post.owner:
        if node.published:
            return node
        return None


class OrganizationNode(DjangoObjectType):
    # pgid = graphene.Int()
    faculties = DjangoFilterConnectionField(
        FacultyNode,
        filterset_class=FacultyFilter,
    )

    class Meta:
        model = Organization
        interfaces = (relay.Node, )
        filter_fields = ['title']

    def resolve_pgid(self, *_):
        return self.id

    def resolve_faculties(self, info, **kwargs):
        filters = {
            'published': True,
        }
        return Faculty.objects.filter(**filters)


# Mutations

# class CreateOrg(graphene.Mutation):
#     """Create organization."""
#     class Arguments:
#         name = graphene.String()

#     # Class attributes
#     ok = graphene.Boolean()
#     batch_owner = graphene.Field(lambda: BatchOwner)

#     def mutate(self, info, name):
#         record = {'name': name}
#         api_utils.create('BatchOwner', record)
#         # Custom methods to create records in database
#         batch_owner = BatchOwner(name=name)
#         ok = True
#         return CreateBatchOwner(batch_owner=batch_owner, ok=ok)


class CreateFacultyMutation(SerializerMutation):
    class Meta:
        serializer_class = FacultySerializer
        model_operations = ['create', 'update']
        lookup_field = 'id'


# class Mutations(graphene.ObjectType):
class Mutations(object):
    faculty = CreateFacultyMutation.Field()


# Query
class Query(object):
    """Query endpoint for GraphQL API."""
    organization = relay.Node.Field(OrganizationNode)
    organizations = DjangoFilterConnectionField(
        OrganizationNode,
        filterset_class=OrganizationFilter,
    )
    faculty = relay.Node.Field(FacultyNode)
    faculties = DjangoFilterConnectionField(
        FacultyNode,
        filterset_class=FacultyFilter,
    )
    department = relay.Node.Field(DepartmentNode)
    departments = DjangoFilterConnectionField(
        DepartmentNode,
        filterset_class=DepartmentFilter,
    )
    period = relay.Node.Field(PeriodNode)
    periods = DjangoFilterConnectionField(
        PeriodNode,
        filterset_class=PeriodFilter,
    )

    # all_tasks = graphene.List(TaskType)
    # faculties = DjangoFilterConnectionField(FacultyType)
    # faculties = graphene.List(
    #     FacultyType,
    #     university=graphene.Int(),
    # )
    # all_ingredients = graphene.List(IngredientType)

    # def resolve_all_departments(self, args, info):
    #     return Department.objects.filter(published=True)

    def resolve_all_tasks(self, info, **kwargs):
        return Task.objects.all()

    def resolve_faculties(self, info, **kwargs):
        filters = {
            'published': True,
        }
        # university = kwargs.get('university')
        # print(university)
        # if university is not None:
        #     org = Organization.objects.get(pk=university)
        #     print(org)
        #     filters['university'] = org

        # return Faculty.objects.all()
        return Faculty.objects.filter(**filters)

    # def resolve_department(self, info, **kwargs):
    #     filters = {
    #         # 'published': True,
    #     }
    #     code_slug = kwargs.get('code_slug')
    #     if code_slug is not None:
    #         filters['code_slug'] = code_slug

    #     # return Faculty.objects.all()
    #     return Faculty.objects.get(**filters)
