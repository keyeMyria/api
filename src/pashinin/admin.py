from django.contrib import admin
from .models import Lesson, Course, CourseLead, QA
# from django.utils.translation import ugettext_lazy as _
from ordered_model.admin import OrderedModelAdmin
from core.models import User
# from adminfilters.models import Species, Breed


class UserAdminInline(admin.TabularInline):
    model = User


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    ordering = ['-start']
    list_filter = ('student', )
    list_display = ('start', 'student')
    save_as = True
    # raw_id_fields = ("student",)
    # inlines = [UserAdminInline]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'published', )
    ordering = ['id']


@admin.register(CourseLead)
class CourseLeadAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'contact',
        'course',
        'status',
        'student',
    )
    list_filter = ('status', )
    ordering = ['status']


@admin.register(QA)
class QAAdmin(OrderedModelAdmin):
    list_display = (
        'order',
        'question',
        'move_up_down_links',
    )
    # list_filter = ('status', )
    list_display_links = ('question', )
    ordering = ['order']
