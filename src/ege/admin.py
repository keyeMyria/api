from django.contrib import admin
from .models import Subject, EGE
from django.utils.translation import ugettext_lazy as _


def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
    make_published.short_description = _("Published")


def unpublish(modeladmin, request, queryset):
    queryset.update(published=False)
    make_published.short_description = _("Hide")+" (published=False)"


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'published')
    list_filter = ('published', )
    ordering = ['-published', 'name']
    actions = [unpublish, make_published]


@admin.register(EGE)
class EGEAdmin(admin.ModelAdmin):
    list_filter = ('type', )
