import json
import hashlib
from django.db import models
from django.db.models import Count, Func
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import gettext_lazy as _
# from social.apps.django_app.default.models import UserSocialAuth
from django.contrib.auth.models import Permission, Group, PermissionsMixin
from django.db import transaction
from random import randint
from django.core.cache import cache
from mptt.models import MPTTModel, TreeForeignKey
from netfields import InetAddressField, NetManager
from django_gravatar.helpers import get_gravatar_url
from . import now
# from lazysignup.utils import is_lazy_user


# Travis payload format:
# https://docs.travis-ci.com/user/notifications#Webhooks-Delivery-Format
class SiteUpdate(models.Model):
    started = models.DateTimeField(
        default=None,
        null=True, blank=True,
        db_index=True
    )
    finished = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        null=True, blank=True
    )
    sha1 = models.CharField(max_length=40, editable=False, unique=True)
    commit_time = models.DateTimeField(
        db_index=True,
        null=True, blank=True
    )
    commit_message = models.CharField(
        max_length=150,
        editable=False,
        null=True, blank=True
    )
    travis_raw = models.TextField(null=True, blank=True)
    log = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = _("Site update")
        verbose_name_plural = _("Site updates")

    @property
    def travis_raw_pretty(self):
        if self.travis_raw:
            parsed = json.loads(self.travis_raw)
            return json.dumps(parsed, indent=4, sort_keys=True)
        else:
            return ""

    @property
    def length(self):
        if self.finished and self.started:
            return self.finished-self.started
        else:
            return None

    def __str__(self):
        return self.sha1


class AddedChanged(models.Model):
    added = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        # default=now,
    )
    changed = models.DateTimeField(
        auto_now=True,
        db_index=True,
        # default=now
    )
    # , editable=False

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            is_staff=False,
            is_active=True,
            is_superuser=False,
            last_login=now(),
            date_joined=now()
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def random(self):
        """TODO"""
        # there can be deleted items
        with transaction.atomic():
            count = self.aggregate(count=Count('id'))['count']
            random_index = randint(0, count - 1)
            return self.all()[random_index]

    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    USERNAME_FIELD = 'email'

    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
        db_index=True,
        blank=True, null=True,
        default=None,
    )
    username = models.CharField(
        max_length=200,
        db_index=True,
        # unique=True,
        default='',
        blank=True, null=True,
        help_text=_("This is an unique identifier, not actual username. Can be a session \
key for temporary users")
    )
    # is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        default=False,
        help_text=_("Designates whether this user can access the admin site.")
    )
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True, db_index=True)
    first_name = models.CharField(
        max_length=200,
        blank=True, null=True,
    )
    last_name = models.CharField(
        max_length=200,
        blank=True, null=True,
    )
    date_last_pass_sent = models.DateTimeField(null=True)
    skype = models.CharField(max_length=200, blank=True, null=True)
    discord = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    browser_on_creation = models.CharField(
        max_length=300,
        db_index=True,
        default=None,
        blank=True, null=True,
        help_text=_("Browser string used when this user was created")
    )
    created_from_ip = models.GenericIPAddressField(blank=True, null=True)
    timezone_str = models.CharField(
        max_length=50,
        db_index=True,
        default='UTC',
    )
    # avatar = models.ForeignKey(
    #     'images.Image',
    #     null=True,
    #     blank=True,
    #     # help_text=_("Avatar image")
    # )
    permissions = models.ManyToManyField(
        Permission,
        related_name="permissions",
        blank=True
    )
    groups = models.ManyToManyField(
        Group,
        related_name="groups",
        blank=True
    )
    telegram_chat_id = models.IntegerField(
        blank=True, null=True,
    )

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def gravatar(self, size_in_px=25):
        """Return authorized social accounts"""
        return get_gravatar_url(self.email, size=size_in_px)

    # @property
    # def social_accounts(self):
    #     """Return authorized social accounts"""
    #     return UserSocialAuth.objects.filter(user=self)

    @property
    def is_lazy(self):
        return True
        # return is_lazy_user(self)

    def get_full_name(self):
        "Used in Admin. Dajngo wants this to be defined."
        return "{} {}".format(self.first_name, self.last_name)

    def get_short_name(self):
        "Used in Admin. Dajngo wants this to be defined."
        return self.email

    def __str__(self):
        # if self.is_lazy:
        #     return "{}".format(_('Anonymous'))

        if self.first_name:
            return self.first_name
        elif self.email:
            return self.email
        else:
            return "User {}".format(self.pk)


# pip install django-mptt
class Tree(MPTTModel):
    parent = TreeForeignKey(
        'self',
        default=None,
        null=True,
        blank=True,
        db_index=True,
        # related_name="%(app_label)s_%(class)s_parent",
        # related_name="%(app_label)s_%(class)s_children",
        related_name='children',
        verbose_name=_("Parent element"),
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True


class Comment(Tree):
    author = models.ForeignKey(
        'core.User',
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    src = models.TextField()


class LoginAttempt(models.Model):
    '''
    A login attempt record (both successful and not).

    If user field is set then login was successful.

    Instead login and password fields are set.
    '''
    # https://docs.python.org/3/library/ipaddress.html
    # inet = InetAddressField(primary_key=True)
    ip = InetAddressField()
    login = models.CharField(
        max_length=260,
        null=True, blank=True,
    )
    password = models.CharField(
        max_length=260,
        null=True, blank=True,
    )
    user = models.ForeignKey(
        'core.User',
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    time = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        null=True, blank=True,
    )
    # success = models.BooleanField(default=False)

    objects = NetManager()


class Unnest(Func):
    function = 'UNNEST'


class IP(models.Model):
    # https://docs.python.org/3/library/ipaddress.html
    # inet = InetAddressField(primary_key=True)
    inet = InetAddressField()

    open_ports = ArrayField(
        models.IntegerField(),
        blank=True,
        null=True
    )

    objects = NetManager()

    class Meta:
        verbose_name = _('IP')
        verbose_name_plural = _('IP-addresses')

    @classmethod
    def stat(cls):
        """Return Port and how many IPs have it open"""
        return cls.objects \
                  .annotate(port=Unnest('open_ports', distinct=True)) \
                  .values('port') \
                  .annotate(count=Count('port')) \
                  .order_by('-count', '-port')

    @classmethod
    def with_open_ports(cls, ports):
        """Return Port and how many IPs have it open"""
        return cls.objects.filter(open_ports__contains=ports)

    def __str__(self):
        # from django.contrib.postgres.aggregates import ArrayAgg
        # print(IP.objects.aggregate(arrayagg=ArrayAgg('inet')))
        # print(IP.objects.values('open_ports')\
        #       .annotate(number_of_days=Count('open_ports', distinct=True)))
        # print(IP.objects.filter()\
        #       .aggregate(Avg('open_ports')))
        # print(IP.objects.aggregate(All('open_ports')))
        # print(IP.stat())
        #       .group_by('inet'))
        # print(IP.objects.values('inet').annotate(arr_els=Unnest('open_ports')))
        # .values_list('arr_els', flat=True).distinct())
        return str(self.inet)


class Hostname(models.Model):
    name = models.CharField(
        max_length=260,
        help_text="example.org, host.example.org"
    )
    # 2 level domain?
    is_domain = models.BooleanField(default=False)

    class Meta:
        # unique_together = (("name", "domain"),)
        # index_together = [["name", "domain"], ]
        verbose_name = _("Hostname")
        verbose_name_plural = _("Hostnames")

    @property
    def key(self):
        return 'host_{}'.format(
            hashlib.md5(str(self).encode('utf-8')).hexdigest()
        )

    @property
    def last_visited(self):
        key = self.key+'lastvisit'
        return cache.get(key)

    @last_visited.setter
    def last_visited(self, t):
        key = self.key+'lastvisit'
        return cache.set(key, t, 60)

    def last_visit_older(self, s):
        # print(self, self.last_visited)
        if self.last_visited is None:
            return True
        # return now() - self.last_visited > timedelta(seconds=3)

    # @classmethod
    # def from_string(cls, s):
    #     host_arr = s.split('.')
    #     host_part = '.'.join(host_arr[:-2])
    #     domain_part = '.'.join(host_arr[-2:])
    #     # try:
    #     domain, c = Domain.objects.get_or_create(name=domain_part)
    #     # except:
    #     #    client.captureException()
    #     domain.clean()
    #     host, c = Hostname.objects.get_or_create(
    #         name=host_part,
    #         domain=domain
    #     )
    #     return host

    def __eq__(self, other):
        if other is None:
            return False
        if str(self) == str(other):
            # if self.name == other.name and \
            #   self.domain == other.domain:
            return True
        return False

    def __str__(self):
        if self.name:
            return '{}.{}'.format(self.name, str(self.domain))
        else:
            return str(self.domain)

# class Country(models.Model):
#     name_ru = models.CharField(max_length=150)
#     name_en = models.CharField(max_length=150)
#     code = models.CharField(max_length=2)
#     truecountry = models.IntegerField(default=0, null=False)

#     class Meta:
#         db_table = 'countries'
#         ordering = ('name_en',)
#         verbose_name_plural = "Countries"

#     def __str__(self):
#         lng = django.utils.translation.get_language()
#         if 'ru' == lng:
#             return self.name_ru
#         return self.name_en


# class PersonManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset() \
#                                          .select_related('name',

# class URLScheme(models.Model):
#     """http://en.wikipedia.org/wiki/URI_scheme"""
#     name = models.CharField(max_length=260)

#     class Meta:
#         db_table = 'url_scheme'

#     def __eq__(self, other):
#         if other is None or self is None:
#             return False
#         if self.name == str(other):
#             return True
#         return False

#     def __str__(self):
#         return self.name


# class URL(models.Model):
#     """scheme://username:password@example.org:8042/path?query#fragment"""

#     cookies_file = '/var/www/xdev/tmp/url_cookies.txt'

#     scheme = models.ForeignKey(URLScheme, null=True, blank=True)
#     host = models.ForeignKey(Hostname, null=True, blank=True)
#     path_str = models.CharField(max_length=260, help_text="/path/in/url",
#                                 null=True, blank=True, default=None)
#     # image = models.ForeignKey('Image', null=True, blank=True)
#     # query = hstore.DictionaryField(null=True, blank=True)
#     query = models.CharField(max_length=260, null=True, blank=True,
#                              help_text="?query")
#     fragment = models.CharField(max_length=260, null=True, blank=True,
#                                 help_text="#fragment")
#     # objects = hstore.HStoreManager()
#     status_code = models.IntegerField(default=None, null=True, blank=True)
#     redirect = models.ForeignKey('self', null=True, blank=True, default=None,
#                                  db_column='redirect_id', related_name='+')
#     v = models.IntegerField(default=0, help_text="asd")

#     class Meta:
#         db_table = 'url'
#         unique_together = (("scheme", "host", "path_str",
#                             "query", "fragment"), )
#         # index_together = [["name", "domain"], ]
#         verbose_name = "URL"
#         verbose_name_plural = "URLs"

#     @property
#     def sha1(self):
#         s = str(self)
#         if isinstance(s, six.text_type):
#             s = s.encode('utf-8')
#         return hashlib.sha1(s).hexdigest()

#     @property
#     def links_abs(self):
#         """Absolute URLs from the page. Return QuerySet of URL models."""
#         links = self.soup.find_all('a')
#         u = str(self.final_url)
#         s = set([urljoin(u, tag.get('href', None)) for tag in links
#                  if tag.get('href', None) is not None])

#         def id(x):
#             return URL.from_string(x).id

#         ids = list(map(id, s))
#         return URL.objects.filter(pk__in=ids)

#     @property
#     def final_url(self):
#         if self.redirect:
#             return self.redirect
#         return self

#     def get(self):
#         "Returns [Request object] or None. See 'requests' pkg"
#         key = 'url_data_{}_r'.format(self.sha1)
#         r = cache.get(key)
#         if r is not None:
#             return r

#         wait = 4
#         while not self.host.last_visit_older(wait):
#             sleep(wait)

#         headers = {
#             'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:29.0)'
#             ' Gecko/20100101 Firefox/29.0'
#         }

#         try:
#             r = requests.get(str(self), headers=headers)
#         except requests.exceptions.ConnectionError:
#             client.captureException()
#             return None
#         if r.history:
#             u_redirected = URL.from_string(r.url)
#             if settings.DEBUG:
#                 print('got redirect to:', u_redirected)
#             if self.redirect != u_redirected and self.redirect != self:
#                 self.redirect = u_redirected
#                 self.save()
#         cache.set(key, r, 60*60)
#         self.host.last_visited = now()
#         return r

#     @property
#     def key(self):
#         return 'url_data_{}'.format(self.sha1)

#     def download(self, wait=4, **kwargs):
#         return self.get().content

#     @classmethod
#     def download_url(cls, url, filename, **kwargs):
#         "Download URL and save it to FILENAME."
#         # endfile = os.path.basename(url) + '.jpg'
#         headers = {'User-Agent':
#                    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:29.0)
# Gecko/20100101 Firefox/29.0'}
#         import requests
#         r = requests.get(url, headers=headers, stream=True)
#         if r.status_code == 200:
#             with open(filename, 'wb') as f:
#                 for chunk in r.iter_content(chunk_size=1024):
#                     if chunk: # filter out keep-alive new chunks
#                         f.write(chunk)
#         else:
#             return r.status_code
#         return url

#     def data_to_unicode(self, **kwargs):
#         """Extract META tags from HTML.
#
#         and try to convert data to Unicode string"""
#         from article.parser.html import guess_html_encoding
#         # update = kwargs.get('update', False)
#         data = self.download(**kwargs)
#         # print(data.decode("cp1251", 'ignore'))
#         s, enc = guess_html_encoding(data)
#         if enc is not None:
#         #    print(enc)
#         #    print(s)
#             return s
#         try:
#             return data.decode('utf-8')
#         except UnicodeDecodeError as e:
#             try:
#                 return data.decode('cp1251')
#             except UnicodeDecodeError as e:
#                 return str(e)

#     @property
#     def soup(self):
#         key = 'url_soup_{}'.format(self.sha1)
#         soup = cache.get(key)
#         if soup is None:
#             soup = BeautifulSoup(self.data_to_unicode())
#             # cache.set(key, soup)
#         return soup

#     def matches(self, d=None, h=None, path=None, f=None, q=None):
#         if d is not None and not d.lower() == str(self.host.domain).lower():
#             return False
#         if h is not None and not re.match(h, str(self.host)):
#             return False
#         if path is not None and not re.match(path, self.path_str):
#             return False
#         if f is not None and not re.match(f, self.fragment):
#             return False
#         if q is not None and not re.match(q, self.query):
#             return False
#         return True

#     @property
#     def obj(self):
#         return 'todo'

#     @classmethod
#     def from_string(cls, s):
#         if isinstance(s, cls):
#             return s
#         o = urlparse(s)
#         scheme, c = URLScheme.objects.get_or_create(name=o.scheme)
#         host = Hostname.from_string(o.hostname)
#         u, c = cls.objects.get_or_create(scheme=scheme,
#                                          host=host,
#                                          path_str=o.path,
#                                          query=o.query,
#                                          fragment=o.fragment)
#         return u

#     def __eq__(self, other):
#         if other is None or self is None:
#             return False
#         #if self.url == other.url and self.url is not None:
#         #    return True
#         else:
#             if self.scheme == other.scheme and \
#                self.host == other.host and \
#                self.path_str == other.path_str and \
#                self.query == other.query:
#                 return True
#             return False
#         return NotImplemented

#     def __str__(self):
#         s = "{}://{}".format(str(self.scheme), self.host)
#         if self.path_str:
#             s += self.path_str
#         if self.query:
#             s += "?" + self.query
#         if self.fragment:
#             s += "#" + self.fragment
#         if self.scheme and self.host:
#             return s
#         else:
#             return NotImplemented


# class UrlObject(models.Model):
#     # url = models.ForeignKey(URL, primary_key=True)
#     url = models.OneToOneField(URL, primary_key=True)
#     # obj = models.ForeignKey(Hostname, null=True, blank=True, default=None)
#     content_type = models.ForeignKey(ContentType, null=True)
#     object_id = models.PositiveIntegerField(null=True)
#     obj = GenericForeignKey('content_type', 'object_id')
#     v = models.IntegerField(default=0)

#     class Meta:
#         db_table = 'obj_from_url'
#         # ordering = ('name',)

#     def __str__(self):
#         return self.obj

# class Translated(models.Model):
#     translation_of = models.ForeignKey(
#         'self',
#         default=None,
#         null=True,
#         blank=True,
#         related_name="%(app_label)s_%(class)s_translated",
#         verbose_name=_("Translation of")
#     )
#     lng = models.ForeignKey(
#         Language,
#         default=None,
#         null=True,
#         blank=True,
#         related_name="%(app_label)s_%(class)s_lng",
#         verbose_name=_("Language")
#     )

#     def get_translation(self, language):
#         if self.lng == language:
#             return self
#         if self.translation_of is not None:
#             pass
#         return

#     class Meta:
#         abstract = True

# class Language(models.Model):
#     name = models.CharField(
#         max_length=150,
#         help_text="Original language name"
#     )
#     name_en = models.CharField(max_length=150, help_text="Name in English")
#     code = models.CharField(
#         max_length=2,
#         help_text="2 chars",
#         unique=True,
#         primary_key=True,
#         verbose_name=_("Code")
#     )

#     class Meta:
#         db_table = 'languages'
#         ordering = ('name',)
#         verbose_name = _("Language")
#         verbose_name_plural = _("Languages")

#     def __str__(self):
#         return self.name
