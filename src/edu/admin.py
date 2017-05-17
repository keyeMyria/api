import mptt
from django.contrib import admin
from .models import Task, Category
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


# admin.site.register(Tag)
# class TaskAdmin(admin.ModelAdmin):


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    form = TaskChangeForm

    list_display = ('title', 'taken_from', 'comment')
    actions = [unpublish, make_published]
    ordering = ['published', '-added']
    list_filter = ('published', 'solution_status', 'added')
    search_fields = ['text', 'comment']

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '60'})},
        # models.TextField: {'widget': Textarea(attrs={'rows': 4,
        # 'cols': 40})},
    }

    fieldsets = (
        (_('Task'), {
           'fields': ('published', 'title', 'text', ('taken_from', 'comment'),
                      'tags')
        }),
        (_('Solution'), {
            'fields': ('solution_status', 'solution'),
        }),
        ('Advanced options', {
            'fields': ('debug', ),
        }),
    )


# mptt.admin.MPTTModelAdmin
@admin.register(Category)
class CategoryAdmin(mptt.admin.DraggableMPTTAdmin):
    # list_display = (
    #     'name',
    #     'parent',
    #     'tree_id',
    #     'level',
    # )
    search_fields = ('name', )
