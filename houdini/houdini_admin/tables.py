import django_tables2 as tables

from houdini_server.models import Application, User, Permission, Role


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
        model = Application
        fields = ('name', 'key', 'secret', 'roles_names', 'id')


class UserTable(tables.Table):
    class Meta:
        model = User
        fields = ('name', 'email', 'is_active', 'roles_names', 'date_joined', 'id')
