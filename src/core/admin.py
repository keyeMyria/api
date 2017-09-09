from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User, SiteUpdate
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Permission
admin.site.register(Permission)
# admin.site.unregister(Group)


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        required=False,
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput,
        required=False,
    )

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)

        # when password is set
        if self.cleaned_data["password1"]:
            user.set_password(self.cleaned_data["password1"])
        else:
            user.is_active = False
        if commit:
            user.save()

        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password', 'is_active', 'is_superuser',
                  'username', 'groups']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


@admin.register(User)
class UserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('id', 'email', 'date_joined',
                    'is_active', 'browser_on_creation')
    list_display_links = ('id', 'email')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    fieldsets = (
        (None, {'fields': (
            'first_name',
            'username',
            'email',
            'password',
            'city',
            'browser_on_creation',
        )}),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'permissions'
            )
        }),
    )

    # fields used when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'username',
                'password1', 'password2',
                'city'
            )
        }),
    )
    search_fields = ('email',)
    ordering = ('-date_joined',)
    filter_horizontal = ('groups', 'permissions',)


@admin.register(SiteUpdate)
class SiteUpdateAdmin(admin.ModelAdmin):
    list_display = ('commit_message', 'started', 'finished')
    # list_filter = ('public', )


# from django.contrib import admin
# from .models import *
# from .forms import URLForm, URLAddForm


# @admin.register(FullName)
# class FullnameAdmin(admin.ModelAdmin):
#     list_display = ('__str__', 'first', 'last', 'ok')
#     search_fields = ('first__name', 'last__name')
#     # ordering = ('name', )


# @admin.register(Name)
# class NameAdmin(admin.ModelAdmin):
#     list_display = ('name', 'ok')
#     ordering = ('name', 'ok')


# @admin.register(Person)
# class PersonAdmin(admin.ModelAdmin):
#     # search_fields = ('name', )
#     list_display = ('name', )
#     ordering = ('name',)


# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     pass
#     # search_fields = ('name', )
#     # list_display = ('name', )
#     # ordering = ('name',)


# @admin.register(Language)
# class LanguageAdmin(admin.ModelAdmin):
#     list_display = ('name_en', 'name', 'code')
#     ordering = ('name_en',)


# @admin.register(Country)
# class CountryAdmin(admin.ModelAdmin):
#     list_display = ('name_en', 'name_ru', 'code')
#     ordering = ('name_en',)


# @admin.register(ReleaseDate)
# class ReleaseDateAdmin(admin.ModelAdmin):
#     list_display = ('date', 'place')
#     ordering = ('date',)


# # @admin.register(WikiPage)
# # class WikiPageAdmin(admin.ModelAdmin):
# #     list_display = ('url_title', 'lng', 'response_code',)
# #     ordering = ('url_title',)


# class UnitInline(admin.TabularInline):
#     model = Hostname


# @admin.register(Domain)
# class DomainAdmin(admin.ModelAdmin):
#     inlines = [UnitInline]
#     list_display = ('name',)
#     ordering = ('name',)


# @admin.register(Hostname)
# class HostnameAdmin(admin.ModelAdmin):
#     # inlines = [UnitInline]
#     list_display = ('name', 'domain')
#     ordering = ('domain',)


# @admin.register(URL)
# class URLAdmin(admin.ModelAdmin):
#     form = URLForm
#     # exclude
#     list_display = ('__str__', 'redirect', 'scheme', 'host', 'path_str',
#                     'query',
#                     'fragment')
#     # list_display = ('url', 'redirect', 'scheme', 'host', 'image', 'query',
#                      'fragment')
#     # ordering = ('host',)
#     list_filter = ('scheme', )
#     raw_id_fields = ('redirect', 'host')
#     search_fields = ('url', 'scheme__name', 'host__domain__name',
#                       'redirect__url',
#                      'redirect__scheme__name',
#                      'redirect__host__domain__name')
#     # filter_horizontal = ('scheme',)

#     def get_form(self, request, obj=None, **kwargs):
#         if obj is None:
#             return URLAddForm
#         else:
#             return super(URLAdmin, self).get_form(request, obj, **kwargs)


# class URLObjAdmin(admin.ModelAdmin):
#     list_display = ('url', 'obj')
#     raw_id_fields = ('url',)
# admin.site.register(UrlObject, URLObjAdmin)


# @admin.register(IP)
# class IPAdmin(admin.ModelAdmin):
#     pass
