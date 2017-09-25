from django.contrib import admin
from reversion.admin import VersionAdmin
from .models import Article


# admin.site.register(Article)


@admin.register(Article)
class ArticleModelAdmin(VersionAdmin):
    list_display = ('pk', 'title', 'added')
    list_display_links = ('title', )
    raw_id_fields = ('author',)
