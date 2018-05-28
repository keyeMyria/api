import graphene
# from graphene_django.types import DjangoObjectType
# from cookbook.ingredients.models import Category, Ingredient
import edu.schema


class Query(
        edu.schema.Query,
        graphene.ObjectType
):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutations(
        edu.schema.Mutations,
        graphene.ObjectType
):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


SCHEMA = graphene.Schema(
    query=Query,
    mutation=Mutations
)
