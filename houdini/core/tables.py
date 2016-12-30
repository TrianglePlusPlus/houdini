import django_tables2 as tables

from .models import Permission, Role


class PermissionTable(tables.Table):
    class Meta:
        model = Permission
        fields = ('name', 'slug', 'id')


class RoleTable(tables.Table):
    class Meta:
        model = Role
        fields = ('name', 'slug', 'parents_names', 'permissions_names', 'id')


class ApplicationTable(tables.Table):
    class Meta:
        model = Role
        fields = ('name', 'app_key', 'app_secret', 'profiles', 'id')
