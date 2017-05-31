from django.forms import ModelForm, ValidationError

from houdini_server.models import Application, Role, Permission, User


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = ('name', 'roles', 'activate_url', 'password_set_url',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['roles'].widget.attrs.update({'class': 'form-control'})
        self.fields['activate_url'].widget.attrs.update({'class': 'form-control'})
        self.fields['password_set_url'].widget.attrs.update({'class': 'form-control'})


class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = ('name', 'parents', 'permissions',)

    def __init__(self, data=None, *args, **kwargs):
        # We do these tests on the data to catch when the role has no parents or permissions
        # This is necessary in order to allow someone to change a role from having
        # parents/permisions to not having parents/permissions.
        # We do this here to intercept the data before it gets the clean method where it
        # will cause validation errors
        if data is not None:
            data = data.copy()
            if data.get('parents', None) == '':
                del data['parents']
            if data.get('permissions', None) == '':
                del data['permissions']
        super(RoleForm, self).__init__(data=data, *args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['parents'].widget.attrs.update({'class': 'form-control'})
        self.fields['parents'].empty_label = '--- None ---'
        self.fields['permissions'].widget.attrs.update({'class': 'form-control'})
        self.fields['permissions'].empty_label = '--- None ---'


class PermissionForm(ModelForm):
    class Meta:
        model = Permission
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(PermissionForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('roles',)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['roles'].widget.attrs.update({'class': 'form-control'})
        self.fields['roles'].required = False
