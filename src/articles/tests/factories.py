import factory
from ..models import Article
from core.tests.factories import UserFactory


class ArticleFactory(factory.django.DjangoModelFactory):
    # name = "Test Product"
    # features = "Awesome feature set brah!"
    pk = factory.Sequence(lambda n: n)
    title = factory.Sequence(lambda n: 'Article {}'.format(n))
    author = factory.SubFactory(UserFactory)
    # title = 'asd'

    class Meta:
        model = Article
        django_get_or_create = ('pk',)
