from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import gettext_lazy as _
# from social.apps.django_app.default.models import UserSocialAuth
from django.contrib.auth.models import Permission, Group, PermissionsMixin


class AddedChanged(models.Model):
    added = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
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
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
        db_index=True,
    )
    username = models.CharField(
        max_length=200,
        db_index=True
    )
    # is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True, db_index=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    date_last_pass_sent = models.DateTimeField(null=True)
    # avatar = models.ForeignKey(
    #     'images.Image',
    #     null=True,
    #     blank=True,
    #     # help_text=_("Avatar image")
    # )
    # permissions = models.ManyToManyField(Permission)
    # groups = models.ManyToManyField(Group)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    class Meta:
        # db_table = 'auth_user'
        verbose_name = _("User")
        # app_label = 'auth'
        verbose_name_plural = _("Users")

    @property
    def is_authenticated(self):
        return not self.is_anonymous

    @property
    def is_anonymous(self):
        return self.id == 1

    def gravatar(self, size_in_px=25):
        """Return authorized social accounts"""
        from django_gravatar.helpers import get_gravatar_url, has_gravatar, get_gravatar_profile_url, calculate_gravatar_hash
        return get_gravatar_url(self.email, size=size_in_px)

    @property
    def social_accounts(self):
        """Return authorized social accounts"""
        return UserSocialAuth.objects.filter(user=self)

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email
