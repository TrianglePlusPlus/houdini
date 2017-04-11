from django.apps import AppConfig
from . models import *


class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = 'Houdini Core'

    def ready(self):
        """
        Initializes the RolesToPermissions table
        :return:
        """
        RolesToPermissions.refresh_table()