from django import forms
from .models import EduMaterial


class EduMaterialForm(forms.ModelForm):
    class Meta:
        fields = ('subject', 'files',)
        model = EduMaterial
