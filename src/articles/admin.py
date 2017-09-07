from django.contrib import admin
from reversion.admin import VersionAdmin
from .models import Article


# admin.site.register(Article)


@admin.register(Article)
class ArticleModelAdmin(VersionAdmin):
    pass
