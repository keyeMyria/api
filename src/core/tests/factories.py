import factory
from ..models import User


class UserFactory(factory.django.DjangoModelFactory):
    # name = "Test Product"
    # features = "Awesome feature set brah!"
    pk = factory.Sequence(lambda n: n)
    email = factory.Sequence(lambda n: 'user{}@example.org'.format(n))
    # author = factory.SubFactory(UserFactory)
    # title = 'asd'

    class Meta:
        model = User
        django_get_or_create = ('email',)
