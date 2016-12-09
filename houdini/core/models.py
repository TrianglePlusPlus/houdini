import json
import uuid

from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone


class Application(models.Model):
    name = models.CharField(max_length=64, unique=True)
    app_key = models.CharField(max_length=32)
    app_secret = models.CharField(max_length=32)

    # JSON serialized string of profile names
    profiles = models.TextField()

    def generate_app_key(self):
        self.app_key = uuid.uuid4().hex

    def generate_app_secret(self):
        self.app_secret = uuid.uuid4().hex

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
        super(Permission, self).save(*args, **kwargs)


# TODO: figure out how to sync updates between
# role and permission tables and graph database
class Role(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField()
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    permissions = models.ManyToManyField(Permission)

    @classmethod
    def create(cls, name):
        role = cls(name=name)
        return role

    @classmethod
    def get_json(cls):
        """
        get json for all role objects in database
        """
        roles = Role.objects.all()
        json = {}
        for role in roles:
            json[role.slug] = role.get_json()
        return json

    def get_json(self):
        """
        get json representation of this object for graph
        """
        return {
            'parents': self.get_parents(),
            'permissions': self.get_permissions()
        }

    # this method is super inefficient
    def get_parents(self):
        """
        get a list of slugs of this roles parents
        (traverse up the graph)
        """
        parents = []
        node = self.parent
        while node:
            parents.append(node.slug)
            node = node.parent
        return parents

    def get_permissions(self):
        """
        get a list of slugs of this roles permissions
        """
        return [permission.slug for permission in permissions]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.super(Role, self).save(*args, **kwargs)


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


class Profile(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def get_all_profiles(cls):
        """
        get all available profile subclasses
        """
        return [profile.__name__ for profile in cls.__subclasses__]


class EmployeeProfile(Profile):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    phone = models.CharField(max_length=24)
    dob = models.CharField(max_length=24)
    classyear = models.IntegerField()
    school = models.CharField(max_length=3)
    major = models.CharField(max_length=128)
    race = models.CharField(max_length=64)
    sex = models.CharField(max_length=32)
    is_abroad = models.BooleanField(default=False)
    home_service = models.IntegerField()


class ApplicantProfile(Profile):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    classyear = models.IntegerField()
    school = models.CharField(max_length=3)
    major = models.CharField(max_length=128)
    race = models.CharField(max_length=64)
    sex = models.CharField(max_length=32)

    # add more applicant specific fields


class CustomerProfile(Profile):
    user = models.ForeignKey(User, on_delete=models.PROTECT)


class AlumnusProfile(Profile):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    phone = models.CharField(max_length=24)
    dob = models.CharField(max_length=24)
    classyear = models.IntegerField()
    school = models.CharField(max_length=3)
    major = models.CharField(max_length=128)
    race = models.CharField(max_length=64)
    sex = models.CharField(max_length=32)
