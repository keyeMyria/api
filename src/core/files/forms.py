import os
from django import forms
from .models import UploadedFile, BaseFile


class UploadedFileForm(forms.ModelForm):
    class Meta:
        fields = ('file',)
        model = UploadedFile


class FileAddForm(forms.ModelForm):
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')  # , None
        return super(FileAddForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        m = super(FileAddForm, self).save(commit=False)
        data = self.cleaned_data
        f = data.get('file', None)
        sha1 = File.get_sha1(f)
        m.sha1 = sha1
        m.uploader = self.request.user
        # m.page_len = 10
        # m.comment = 'a'

        fname = File.write(sha1, f)
        m.size = os.path.getsize(fname)
        import magic
        mime = magic.from_file(fname, mime=True).decode("utf-8").split('/')
        m.content_type = File.CT_CHOICES_REVERSED[mime[0]]
        m.content_subtype = mime[1]

        if commit:
            m.save()
        return m

    class Meta:
        model = BaseFile
        # exclude = ['sha1']
        fields = ['file', 'comment', 'public']


class FileForm(forms.ModelForm):
    #
    # comment = forms.CharField(
    #     required=False,
    #     widget=AutosizedTextarea(
    #         attrs={'placeholder': 'Write something', 'class': 'spanX',
    #                'style': 'max-height:550px'}))
    # on_disk = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FileForm, self).__init__(*args, **kwargs)

        obj = kwargs.get('instance')
        if obj:  # if changing
            kwargs['fields'] = ['file', 'uploader']
            kwargs['readonly_fields'] = ('uploader',)
            # self.fields['on_disk'] = forms.BooleanField(required=False)

            #     self.fields['file'].initial = p.content
            # if p.lng is not None:
            #     self.fields['category'].queryset = ArticleCategory \
            #                            .objects.filter(lng=p.lng)

    def save(self, commit=True):
        m = super(FileForm, self).save(commit=False)
        # data = self.cleaned_data
        # uploaded_files = request.session.get('uploaded_files_ids', set())
        # if f.multiple_chunks():  # big enough to be on disk
        #     # Like: path/tmpuj7kjiau.upload
        #     filename = f.temporary_file_path()
        #     print('big', filename)
        # else:
        #     print('small')
        #     # with open(uploadedFilename, 'wb+') as destination:
        #     #     for chunk in f.chunks():
        #     #         destination.write(chunk)

        # m.sha1 = sha1
        # m.uploader = self.request.user
        # m.page_len = 10
        if commit:
            m.save()
        return m

    def clean(self):
        data = super(FileForm, self).clean()
        # title = data.get("title", "").strip()
        # if title:
        #     data["title"] = title
        # else:
        #     raise ValidationError('Enter a title', code='invalid')
        return data

    class Meta:
        model = BaseFile
        # exclude = ['restrictions', 'added_on', 'rev']
        fields = ['comment', 'public']
        # widgets = {'title': TextInput(attrs={'class': 'spanX'})}
