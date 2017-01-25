from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import *  # noqa
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import Group, Permission


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass
