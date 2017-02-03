from django.apps import AppConfig
# from django.db.models.signals import post_migrate
# from django.utils.translation import ugettext_lazy as _

# from .management import create_default_site


class EgeConfig(AppConfig):
    name = 'ege'
    verbose_name = "Школьные экзамены"

    # def ready(self):
    #     post_migrate.connect(create_default_site, sender=self)
