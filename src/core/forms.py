from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
# from .models import URL


# class URLAddForm(forms.ModelForm):
#     URL = forms.CharField(label='URL',
#                           widget=forms.TextInput(attrs={'placeholder': 'https://www.google.com'}))

#     def save(self, commit=True):
#         m = super(URLAddForm, self).save(commit=False)
#         url = self.cleaned_data.get('URL', None)
#         #print(url)
#         # ...do something with extra_field here...
#         return URL.from_string(url)
#         #formset.save(commit=False)
#         #formset.save_m2m()
#         #return super(URLAddForm, self).save(commit=commit)

#     def clean(self):
#         url = self.cleaned_data.get('URL', None)
#         try:
#             URL.from_string(url)
#         except Exception as e:
#             raise ValidationError('Looks like invalid URL: {}\n{}'.format(url, str(e)),
#                                   code='invalid')

#     class Meta:
#         model = URL
#         fields = []


# class URLForm(forms.ModelForm):
#     # URL = forms.CharField(label='search',
#     #                      widget=forms.TextInput(attrs={'placeholder': 'Search'}))

#     def save(self, commit=True):
#         #extra_field = self.cleaned_data.get('extra_field', None)
#         # ...do something with extra_field here...
#         return super(URLForm, self).save(commit=commit)

#     class Meta:
#         model = URL
#         fields = '__all__'


#
# This form checks a pair (email, password) and adds "user" to
# "cleaned_data" if (email, password) is correct. Else - raise errors.
#
# f = LoginForm(request.POST)
#
class Login(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(
        label='Пароль',
        max_length=100,
        widget=forms.PasswordInput()
    )

    def __init__(self, *args, **kwargs):
        super(Login, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            # field.error_messages = {'required':'Обязательное поле'}
            field.error_messages = {
                'required': 'Поле {fieldname} обязательно'.format(
                    fieldname=field.label)}

    def clean(self):
        cleaned_data = super(Login, self).clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            user = authenticate(username=email,
                                password=password)
            if user is None:
                raise forms.ValidationError("Incorrect email or password")
            else:
                cleaned_data['user'] = user

        return cleaned_data
