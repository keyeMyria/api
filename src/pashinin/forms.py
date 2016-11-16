from django import forms


class Enroll(forms.Form):
    name = forms.CharField(label='Имя', max_length=100)
    phone = forms.CharField(label='Телефон', max_length=100)
    message = forms.CharField(label='Question', required=False)

    def __init__(self, *args, **kwargs):
        super(Enroll, self).__init__(*args, **kwargs)
        # self.fields['name'].error_messages = {'required': 'custom required message'}

        # if you want to do it to all of them
        for field in self.fields.values():
            # field.error_messages = {'required':'Обязательное поле'}
            field.error_messages = {
                'required': 'Поле {fieldname} обязательно'.format(
                    fieldname=field.label)}

    def save(self):
        pass
        # # Sets username to email before saving
        # user = super(UserForm, self).save(commit=False)
        # user.username = user.email
        # user.save()
        # return user

    def json(self):
        return {
            "name": self.cleaned_data['name'],
            "phone": self.cleaned_data['phone'],
            "message": self.cleaned_data['message']
        }
