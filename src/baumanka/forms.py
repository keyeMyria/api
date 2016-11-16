import os
from django import forms
from .models import *  # noqa


class EduMaterialForm(forms.ModelForm):
    class Meta:
        fields = ('subject', 'files',)
        model = EduMaterial
