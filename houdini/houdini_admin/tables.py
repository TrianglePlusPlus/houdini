import django_tables2 as tables

from houdini_server.models import Application, User, Permission, Role


class PermissionTable(tables.Table):
    class Meta:
        model = Permission
        fields = ('name', 'slug', 'id')


class RoleTable(tables.Table):
    parents_names = tables.Column(verbose_name='Parents')
    own_permissions_names = tables.Column(verbose_name='Own Permissions')
    parents_permissions_names = tables.Column(verbose_name='Inherited Permissions')

    class Meta:
        model = Role
        fields = ('name', 'slug', 'parents_names', 'own_permissions_names', 'parents_permissions_names', 'id')


class ApplicationTable(tables.Table):
    roles_names = tables.Column(verbose_name='Roles')

    class Meta:
        model = Application
        fields = ('name', 'key', 'secret', 'roles_names', 'id')


class UserTable(tables.Table):
    roles_names = tables.Column(verbose_name='Roles')

    class Meta:
        model = User
        fields = ('name', 'email', 'is_active', 'roles_names', 'date_joined', 'id')
