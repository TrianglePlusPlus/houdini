from django.apps import AppConfig
from . models import *


class HoudiniCoreConfig(AppConfig):
    name = 'houdini_core'
    verbose_name = 'Houdini Core'

    def ready(self):
        """
        Initializes the RolesToPermissions table
        :return:
        """
        RolesToPermissions.refresh_table()
