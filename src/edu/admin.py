import mptt
from django.contrib import admin
from .models import (
    Task, Category, Organization, Faculty,
    Department, Period
)
from .forms import TaskChangeForm
from django.forms import TextInput
from django.db import models
from django.utils.translation import ugettext_lazy as _


def publish(modeladmin, request, queryset):
    queryset.invalidated_update(published=True)
    publish.short_description = "Publish"


def unpublish(modeladmin, request, queryset):
    queryset.invalidated_update(published=False)
    unpublish.short_description = "Unpublish"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    form = TaskChangeForm

    save_on_top = True
    list_display = ('title', 'taken_from', 'comment')
    actions = [unpublish, publish]
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


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    readonly_fields = ('id', )


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'published', 'university', 'added')
    list_filter = ('university__title', )
    ordering = ['code', '-added', 'university']
    search_fields = ['code', 'title', 'university__title']
    actions = [unpublish, publish]


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'faculty', 'university')
    readonly_fields = ('code_slug', )
    list_filter = (
        'university__title',
        'faculty__code',
    )


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_filter = (
        'department__university__title',
        'department__code',
    )
