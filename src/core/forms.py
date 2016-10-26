import os
import sys
from django import forms
from django.core.exceptions import ValidationError
from .models import URL


class URLAddForm(forms.ModelForm):
    URL = forms.CharField(label='URL',
                          widget=forms.TextInput(attrs={'placeholder': 'https://www.google.com'}))

    def save(self, commit=True):
        m = super(URLAddForm, self).save(commit=False)
        url = self.cleaned_data.get('URL', None)
        #print(url)
        # ...do something with extra_field here...
        return URL.from_string(url)
        #formset.save(commit=False)
        #formset.save_m2m()
        #return super(URLAddForm, self).save(commit=commit)

    def clean(self):
        url = self.cleaned_data.get('URL', None)
        try:
            URL.from_string(url)
        except Exception as e:
            raise ValidationError('Looks like invalid URL: {}\n{}'.format(url, str(e)),
                                  code='invalid')

    class Meta:
        model = URL
        fields = []


class URLForm(forms.ModelForm):
    # URL = forms.CharField(label='search',
    #                      widget=forms.TextInput(attrs={'placeholder': 'Search'}))

    def save(self, commit=True):
        #extra_field = self.cleaned_data.get('extra_field', None)
        # ...do something with extra_field here...
        return super(URLForm, self).save(commit=commit)

    class Meta:
        model = URL
        fields = '__all__'
