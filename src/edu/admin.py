from django.contrib import admin
from .models import Task
from .forms import TaskChangeForm
from django.forms import TextInput
from django.db import models
from django.utils.translation import ugettext_lazy as _


def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
    make_published.short_description = _("Published")


def unpublish(modeladmin, request, queryset):
    queryset.update(published=False)
    make_published.short_description = _("Hide")+" (published=False)"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    form = TaskChangeForm

    list_display = ('title', 'solution_status', 'published', 'added')
    list_filter = ('published', 'solution_status')
    actions = [unpublish, make_published]
    ordering = ['published', '-added']

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '60'})},
        # models.TextField: {'widget': Textarea(attrs={'rows': 4,
        # 'cols': 40})},
    }

    fieldsets = (
        (None, {
           'fields': ('published', 'title', 'text',)
        }),
        (_('Solution'), {
            'fields': ('solution_status', 'solution'),
        }),
        ('Advanced options', {
            'fields': ('debug', ),
        }),
    )
