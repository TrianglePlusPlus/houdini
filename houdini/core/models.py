from django.db import models
from django.template.defaultfilters import slugify


class User(models.Model):
    pass


class Employee(models.Model):
    pass


class Applicant(models.Model):
    pass


class Customer(models.Model):
    pass


class Alumnus(models.Model):
    pass


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
