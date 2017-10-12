from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create a lot of test users for Access and assign them roles'

    def handle(self, *args, **options):
        # get the users to be created from csv
        import csv
        users = []
        with open('~/django/houdini/houdini/houdini_server/management/commands/access_test_users.csv', mode='r') as infile:
            reader = csv.reader(infile)
            title_row = next(reader)
            for row in reader:
                user = {
                    title_row[0]: row[0], # email
                    title_row[1]: row[1], # password
                    title_row[2]: row[2], # first_name
                    title_row[3]: row[3], # last_name
                    title_row[4]: row[4], # roles
                }
            users.append(user)

        from houdini_server.models import User
        for user in users:
            print("email: ", user.get('email'))
            # new_user = User.objects.create_user(
            #     user.get('email'),
            #     "https://auth.thecorp.org/activate/",
            #     password=user.get('password'),
            #     first_name=user.get('first_name'),
            #     last_name=user.get('last_name'),
            # )
            # TODO: set roles
            # assume it's just one role?
            # Role role = Role.objects.get(slug=user.get('roles'))
            # new_user.roles.add(role)
            # new_user.save()

