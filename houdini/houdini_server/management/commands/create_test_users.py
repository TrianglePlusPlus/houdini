from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create a lot of test users for Access and assign them roles'

    def handle(self, *args, **options):
        # get the users to be created from csv
        import csv
        users = []
        with open('access_test_users.csv', mode='r') as infile:
            reader = csv.reader(infile)
            title_row = next(reader)
            for row in reader:
                user = {
                    title_row[0]: row[0], # email
                    title_row[1]: row[1], # password
                    title_row[3]: row[3], # first_name
                    title_row[4]: row[4], # last_name
                    title_row[5]: row[5], # roles
                }
                users.append(user)
        
        from houdini_server.models import User, Role
        for user in users:
            if User.objects.filter(email=user.get('email')).count() == 0:
                new_user = User.objects.create_user(
                    user.get('email'),
                    "https://auth.thecorp.org/activate/",
                    password=user.get('email password'),
                    first_name=user.get('first name'),
                    last_name=user.get('last name'),
                )
                role = Role.objects.get(slug=user.get('roles'))
                new_user.roles.add(role)
                new_user.save()

