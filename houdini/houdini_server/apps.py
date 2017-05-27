from django.apps import AppConfig


class HoudiniServerConfig(AppConfig):
    name = 'houdini_server'
    verbose_name = 'Houdini Server'

    def ready(self):
        """
        Connects up the signal receivers in signals.py
        :return:
        """
        import houdini_server.signals
