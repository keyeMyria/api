import functools
from unittest import TestCase


def travis(func):
    """Decorator to run tests only on travis build"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        res = None
        if os.getenv('CI', '') == 'true':
            res = func(*args, **kwargs)
        return res
    return wrapper


class CommonTest(TestCase):
    """A template for tests"""
    def setUp(self):
        self.password = User.objects.make_random_password()
        self.c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        self.email = 'root@localhost'
        try:
            self._superuser = User.objects.get(email=self.email)
        except:
            self._superuser = User.objects.create_user(email=self.email,
                                                       password=self.password)
        self._superuser.is_active = True
        self._superuser.is_superuser = True
        self._superuser.save()
        self.F = F(self.c)

    def anon(self):
        self.c.logout()

    def superuser(self):
        self.assertTrue(self.c.login(username=self._superuser.email, password=self.password))
