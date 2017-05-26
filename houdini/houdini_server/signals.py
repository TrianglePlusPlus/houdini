from django.db.models.signals import post_save, m2m_changed, post_delete
from django.dispatch import receiver
from .models import Role, RolesToPermissions

@receiver(m2m_changed, sender=Role.permissions.through)
def role_m2m_changed(sender, **kwargs):
    RolesToPermissions.refresh_table()

@receiver(post_delete, sender="houdini_server.Role")
def role_post_delete(sender, **kwargs):
    RolesToPermissions.refresh_table()

@receiver(m2m_changed, sender="houdini_server.Permission")
def post_save(sender, **kwargs):
    RolesToPermissions.refresh_table()

@receiver(post_delete, sender="houdini_server.Permission")
def permission_post_delete(sender, **kwargs):
    RolesToPermissions.refresh_table()
