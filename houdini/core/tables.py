import django_tables2 as tables

from .models import Permission

class PermissionTable(tables.Table):
    class Meta:
        model = Permission
        attrs = {'class': 'table table-striped'}
        fields = ('name', 'slug')

    def __init__(self, *args, **kwargs):
        super(PermissionTable, self).__init__(*args, **kwargs)
        self.base_columns['name'].verbose_name = 'Name'
        self.base_columns['slug'].verbose_name = 'Slug'
