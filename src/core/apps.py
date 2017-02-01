from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
# from django.db.models.signals import post_migrate

# from .management import create_default_site


class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = _("Core")

    # def ready(self):
    #     post_migrate.connect(create_default_site, sender=self)
