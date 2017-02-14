from django import forms
from .models import Task


class TaskChangeForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'published', 'debug']
