from django.core.management import call_command
from django.core.management.base import BaseCommand


emails_to_deactivate = [
    "test{:02}@thecorp.org".format(n) for n in range(30)
]


class Command(BaseCommand):
    help = 'Deactivate Access test users now that we are in production'

    def handle(self, *args, **options):
        from houdini_server.models import User
        for email in emails_to_deactivate:
            try:
                user = User.objects.get(email=email)
                user.active = False
                user.save()
            except User.DoesNotExist:
                print("User could not be found: " + email)

