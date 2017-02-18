from django.contrib import admin
from .models import Subject, Exam, Task
from django.utils.translation import ugettext_lazy as _


def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
    make_published.short_description = _("Published")


def unpublish(modeladmin, request, queryset):
    queryset.update(published=False)
    make_published.short_description = _("Hide")+" (published=False)"


# admin.site.register(Task)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'published')
    list_filter = ('published', )
    ordering = ['-published', 'name']
    actions = [unpublish, make_published]


class MembershipInline(admin.TabularInline):
    model = Task
    # show_change_link = True
    extra = 0
    # model = Exam.tasks.through


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)
    # inlines = [
    #     TagInline,
    # ]


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline,
    ]
    exclude = ('tasks',)

    list_filter = ('type', )

    fieldsets = (
        (None, {
           'fields': ('published', 'type', 'subject', 'year')
        }),
        (_('Description'), {
            'fields': ('info', ),
        }),
        # ('Задачи экзамена', {
        #     'fields': ('exam_tasks', ),
        # }),
    )
    # filter_horizontal = ('exam_tasks',)
