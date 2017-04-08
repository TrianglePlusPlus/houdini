import json
import uuid
from queue import Queue

from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone


class Application(models.Model):
    name = models.CharField(max_length=64, unique=True)
    key = models.CharField(max_length=32, blank=True)
    secret = models.CharField(max_length=32, blank=True)

    # JSON serialized string of profile names
    profiles = models.TextField()

    @classmethod
    def create(cls, name):
        application = cls(name=name)
        return application

    def save(self, *args, **kwargs):
        if not self.key:
            self.generate_key()
        if not self.secret:
            self.generate_secret()
        super().save(args, kwargs)

    def generate_key(self):
        self.key = uuid.uuid4().hex

    def generate_secret(self):
        self.secret = uuid.uuid4().hex

    def add_profile(self, profile_name):
        """
        add profile to application
        """
        profile_names = json.loads(self.profiles)
        if profile_name not in profile_names:
            profile_names.append(profile_name)
            profile_names.sort()
            self.profiles = json.dumps(profile_names)

    def remove_profile(self, profile_name):
        """
        remove profile from application
        """
        profile_names = json.loads(self.profiles)
        if profile_name in profile_names:
            profile_names.remove(profile_name)
            profile_names.sort()
            self.profiles = json.dumps(profile_names)


class Permission(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(blank=True)

    @classmethod
    def create(cls, name):
        permission = cls(name=name)
        return permission

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# TODO: figure out how to sync updates between
# role and permission tables and graph database
class Role(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField()
    parents = models.ManyToManyField("self", blank=True, symmetrical=False)
    permissions = models.ManyToManyField(Permission, blank=True, symmetrical=False)

    @classmethod
    def create(cls, name):
        role = cls(name=name)
        return role

    @classmethod
    def get_roles_json(cls):
        """
        @:return The json for all role objects in database
        """
        roles = Role.objects.all()
        json = {}
        for role in roles:
            json[role.slug] = role.get_json()
        return json

    def get_json(self):
        """
        @:return The json representation of just the role instance
        """
        return {
            'parents': self.get_parent_slugs_for_role(),
            'permissions': self.get_permission_slugs_for_role()
        }

    # this method is super inefficient
    def get_all_parents(self):
        # TODO: Is this necessary?
        pass

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def permissions_names(self):
        return ', '.join((permission.name for permission in self.permissions.all()))

    def get_permission_slugs_for_role(self):
        """
        @:return A list of the slugs for all of this role's permissions
        """
        return [permission.slug for permission in self.permissions]

    @property
    def parents_names(self):
        return ', '.join((parent.name for parent in self.parents.all()))

    def get_parent_slugs_for_role(self):
        return [parent.slug for parent in self.parents]

    def get_all_permissions(self):
        permissions = set(self.permissions_set.all())
        search_queue = Queue((parent for parent in self.parents_set.all()))
        while not search_queue.empty():
            role = search_queue.get()
            for permission in role.permissions_set.all():
                permissions.add(permission)
            for parent in role.parents_set.all():
                search_queue.put(parent)
        return permissions

    def __str__(self):
        return self.name


class RolesToPermissions(models.Model):
    role = models.ForeignKey('Role')
    permisions = models.TextField()

    @staticmethod
    def refresh_table():
        """
        Clears the entire table and for every role gathers all of its permissions
        :return: void
        """
        # First clear the entire table
        RolesToPermissions.objects.all().delete()
        # Now regenerate all of the mappings
        for role in Role.objects.all():
            permissions = role.get_all_permissions()
            permissions_list = [permission.name for permission in permissions]
            permissions_list += [permission.slug for permission in permissions]
            permissions_string = json.dumps(permissions_list)
            mapping = RolesToPermissions(role, permissions)
            mapping.save()


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=32)
    middle_name = models.CharField(max_length=32, null=True)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(max_length=32, unique=True)
    username = models.CharField(max_length=32, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    address1 = models.CharField(max_length=128, null=True)
    address2 = models.CharField(max_length=128, null=True)
    city = models.CharField(max_length=128, null=True)
    state = models.CharField(max_length=64, null=True)
    zip = models.CharField(max_length=11, null=True)

    roles = models.ManyToManyField(Role)

    USERNAME_FIELD = 'username'


class Profile(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def get_all_profiles(cls):
        """
        Get a dictionary of profile names to their actual classes
            { 'EmployeeProfile': <class 'core.models.EmployeeProfile'>, ...}
        """
        profiles = {}
        for profile in cls.__subclasses__():
            profiles[profile.__name__] = profile
        return profiles


class EmployeeProfile(Profile):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    phone = models.CharField(max_length=24)
    dob = models.CharField(max_length=24)
    class_year = models.IntegerField()
    school = models.CharField(max_length=3)
    major = models.CharField(max_length=128)
    race = models.CharField(max_length=64)
    sex = models.CharField(max_length=32)
    is_abroad = models.BooleanField(default=False)
    home_service = models.IntegerField()
    roles = models.ManyToManyField('Role')


class ApplicantProfile(Profile):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    class_year = models.IntegerField()
    school = models.CharField(max_length=3)
    major = models.CharField(max_length=128)
    race = models.CharField(max_length=64)
    sex = models.CharField(max_length=32)
    roles = models.ManyToManyField('Role')

    # TODO: add more applicant specific fields


class CustomerProfile(Profile):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    roles = models.ManyToManyField('Role')


class AlumnusProfile(Profile):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    phone = models.CharField(max_length=24)
    dob = models.CharField(max_length=24)
    class_year = models.IntegerField()
    school = models.CharField(max_length=3)
    major = models.CharField(max_length=128)
    race = models.CharField(max_length=64)
    sex = models.CharField(max_length=32)
    roles = models.ManyToManyField('Role')
