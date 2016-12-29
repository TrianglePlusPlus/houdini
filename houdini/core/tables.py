import django_tables2 as tables

from .models import Permission


class PermissionTable(tables.Table):
    class Meta:
        model = Permission
        fields = ('name', 'slug', 'id')
