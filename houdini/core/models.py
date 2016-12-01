from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone


class User(AbstractBaseUser):
    class Meta:
        abstract = True

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


class Employee(User):
    phone = models.CharField(max_length=24)
    dob = models.CharField(max_length=24)
    classyear = models.IntegerField()
    school = models.CharField(max_length=3)
    major = models.CharField(max_length=128)
    race = models.CharField(max_length=64)
    sex = models.CharField(max_length=32)
    is_abroad = models.BooleanField(default=False)
    home_service = models.IntegerField()


class Applicant(User):
    classyear = models.IntegerField()
    school = models.CharField(max_length=3)
    major = models.CharField(max_length=128)
    race = models.CharField(max_length=64)
    sex = models.CharField(max_length=32)

    # add more applicant specific fields


class Customer(User):
    pass


class Alumnus(User):
    phone = models.CharField(max_length=24)
    dob = models.CharField(max_length=24)
    classyear = models.IntegerField()
    school = models.CharField(max_length=3)
    major = models.CharField(max_length=128)
    race = models.CharField(max_length=64)
    sex = models.CharField(max_length=32)


class Role(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField()

    @classmethod
    def create(cls, name):
        role = cls(name=name)
        return role

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.super(Role, self).save(*args, **kwargs)


class Permission(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField()

    @classmethod
    def create(cls, name):
        permission = cls(name=name)
        return permission

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.super(Permission, self).save(*args, **kwargs)
