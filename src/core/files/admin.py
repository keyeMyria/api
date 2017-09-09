# from django.contrib import admin
# from .models import BaseFile
# from .forms import FileForm, FileAddForm


# @admin.register(BaseFile)
# class BaseFileAdmin(admin.ModelAdmin):
#     # list_display_links = ('title', 'year')
#     list_display = ('size', 'content_type', 'content_subtype',
#                     'added', )
#     # list_filter = ('public', )
#     form = FileForm

#     def get_readonly_fields(self, request, obj=None):
#         if obj:
#             return ['sha1', 'uploader', 'size']
#         return []

#     def get_form(self, request, obj=None, **kwargs):
#         if obj is None:
#             class FileFormWithRequest(FileAddForm):
#                 def __new__(cls, *args, **kwargs):
#                     kwargs['request'] = request
#                     return FileAddForm(*args, **kwargs)
#             return FileFormWithRequest
#         return FileForm
