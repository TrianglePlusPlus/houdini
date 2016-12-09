from django.forms import ModelForm, ValidationError

from .models import Permission


class PermissionForm(ModelForm):
    class Meta:
        model = Permission
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PermissionForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['slug'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        super(PermissionForm, self).clean()

        name = self.cleaned_data.get('name')
        if name:
            if Permission.objects.filter(name=name).count() > 0:
                raise ValidationError('Permission already exists.')
