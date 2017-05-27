from datetime import datetime, timedelta
import json
import uuid
from queue import Queue

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.core.mail import send_mail
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone


class Application(models.Model):
    name = models.CharField(max_length=64, unique=True)
    key = models.CharField(max_length=32, blank=True)
    secret = models.CharField(max_length=32, blank=True)

    roles = models.ManyToManyField("Role")

    @property
    def roles_names(self):
        return ', '.join((role.name for role in self.roles.all()))

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
    def own_permissions_names(self):
        return ', '.join((permission.name for permission in self.permissions.all()))

    @property
    def parents_permissions_names(self):
        return ', '.join((permission.name for permission in self.get_parent_permissions()))

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

    def get_parent_permissions(self):
        parent_permissions = set()
        search_queue = Queue()
        for parent in self.parents.all():
            search_queue.put(parent)
        while not search_queue.empty():
            role = search_queue.get()
            for permission in role.permissions.all():
                parent_permissions.add(permission)
            for parent in role.parents.all():
                search_queue.put(parent)
        return parent_permissions

    def get_all_permissions(self):
        permissions = set(self.permissions.all())
        permissions |= self.get_parent_permissions()
        return permissions

    def __str__(self):
        return self.name


class RolesToPermissions(models.Model):
    role = models.ForeignKey('Role')
    permissions = models.TextField()

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
            mapping = RolesToPermissions(role=role, permissions=permissions_string)
            mapping.save()


class HoudiniUserManager(UserManager):
    def get_by_natural_key(self, email):
        return self.get(email=email)

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.generate_activation_key()
        user.send_activation_email()
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=32)
    middle_name = models.CharField(max_length=32, null=True)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=40)
    activation_key_expires = models.DateTimeField()
    password_reset_key = models.CharField(max_length=40, null=True)
    password_key_expires = models.DateTimeField(null=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'

    objects = HoudiniUserManager()

    roles = models.ManyToManyField("Role")

    @property
    def roles_names(self):
        return ', '.join((role.name for role in self.roles.all()))

    def generate_activation_key(self):
        self.activation_key = uuid.uuid4().hex
        self.activation_key_expires = timezone.now() + settings.ACCOUNT_ACTIVATION_TIME

    def send_activation_email(self, resend=False):
        activation_link = settings.BUILD_ABSOLUTE_URL(reverse("activate", kwargs={'key': self.activation_key}))
        if resend:
            message = "Hello " + str(self) + "! Your old activation key expired so we have generated a new one for you. Go to this link to activate your account: " + activation_link
        else:
            message = "Hello " + str(self) + "! You have successfully registered for an account. Go to this link to activate your account: " + activation_link
        send_mail(
            "Activate your account",
            message,
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=False
        )

    # TODO: should there be a limit to the amount of activation keys you can generate?
    # or maybe a time limit between each regeneration?
    def regenerate_activation_key(self):
        self.generate_activation_key()
        self.send_activation_email(resend=True)

    def generate_password_reset_key(self):
        self.password_reset_key = uuid.uuid4().hex
        self.password_key_expires = timezone.now() + settings.PASSWORD_RESET_TIME

    def send_password_reset_email(self):
        password_reset_link = settings.BUILD_ABSOLUTE_URL(reverse("password_set", kwargs={'key': self.password_reset_key}))
        message = "Hello " + str(self) + "! To reset your password, visit this link: " + password_reset_link
        send_mail(
            "Reset your password",
            message,
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=False
        )

    @property
    def is_authenticated(self):
        return True

    @property
    def name(self):
        return str(self)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

# class Profile(models.Model):
#     class Meta:
#         abstract = True
#
#     @classmethod
#     def get_all_profiles(cls):
#         """
#         Get a dictionary of profile names to their actual classes
#             { 'EmployeeProfile': <class 'houdini_core.models.EmployeeProfile'>, ...}
#         """
#         profiles = {}
#         for profile in cls.__subclasses__():
#             profiles[profile.__name__] = profile
#         return profiles
#
#
# class EmployeeProfile(Profile):
#     user = models.ForeignKey(User, on_delete=models.PROTECT)
#     phone = models.CharField(max_length=24)
#     dob = models.CharField(max_length=24)
#     class_year = models.IntegerField()
#     school = models.CharField(max_length=3)
#     major = models.CharField(max_length=128)
#     race = models.CharField(max_length=64)
#     sex = models.CharField(max_length=32)
#     is_abroad = models.BooleanField(default=False)
#     home_service = models.IntegerField()
#     roles = models.ManyToManyField('Role')
#
#
# class ApplicantProfile(Profile):
#     user = models.ForeignKey(User, on_delete=models.PROTECT)
#     class_year = models.IntegerField()
#     school = models.CharField(max_length=3)
#     major = models.CharField(max_length=128)
#     race = models.CharField(max_length=64)
#     sex = models.CharField(max_length=32)
#     roles = models.ManyToManyField('Role')
#
#     # TODO: add more applicant specific fields
#
#
# class CustomerProfile(Profile):
#     user = models.ForeignKey(User, on_delete=models.PROTECT)
#     roles = models.ManyToManyField('Role')
#
#
# class AlumnusProfile(Profile):
#     user = models.ForeignKey(User, on_delete=models.PROTECT)
#     phone = models.CharField(max_length=24)
#     dob = models.CharField(max_length=24)
#     class_year = models.IntegerField()
#     school = models.CharField(max_length=3)
#     major = models.CharField(max_length=128)
#     race = models.CharField(max_length=64)
#     sex = models.CharField(max_length=32)
#     roles = models.ManyToManyField('Role')
