from django.contrib.auth import hashers
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.template.defaultfilters import slugify


class UserType(models.Model):
    name = models.CharField(max_length=32, unique=True)
    fields = JSONField()


class User(models.Model):
    pass


class Role(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField()
    permissions = JSONField()
    parents = JSONField()

    @classmethod
    def create(cls, name):
        role = cls(name=name, permissions=[], parents=[])
        return role

    @classmethod
    def get_json(cls):
        data = {}
        roles = Role.objects.all()
        for role in roles:
            data[role.slug] = {
                "permissions": role.permissions,
                "parents": role.parents
            }
        return data

    def add_permission(self, slug):
        if slug not in self.permissions:
            self.permissions.append(slug)

    def remove_permission(self, slug):
        if slug in self.permissions:
            self.permissions.remove(slug)

    def add_parent(self, slug):
        if slug not in self.parents:
            self.parents.append(slug)

    def remove_parent(self, slug):
        if slug in self.parents:
            self.parents.remove(slug)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Role, self).save(*args, **kwargs)


class Permission(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField()

    @classmethod
    def create(cls, name):
        permission = cls(name=name)
        return permission

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Permission, self).save(*args, **kwargs)
