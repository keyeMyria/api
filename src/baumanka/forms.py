from django.forms import ModelForm  # , Textarea, Input
from edu.models import Faculty


class AddFacultyForm(ModelForm):
    class Meta:
        fields = ('code', 'title',)
        model = Faculty
        # widgets = {
        #     'code': Textarea(attrs={'cols': 80, 'rows': 20}),
        # }
        # labels = {
        # 'code': '',
        # 'name': _('Writer'),
        # }
        # help_texts = {
        #     'name': _('Some useful help text.'),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k, field in self.fields.items():
            field.widget.attrs[
                'placeholder'
            ] = f'{field.label}: {field.help_text}'
            field.help_text = None
            field.label = ''
