from django.contrib import admin
from .models import Task
# from django.utils.translation import ugettext, ugettext_lazy as _


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'added')
