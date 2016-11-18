from django.contrib.auth import hashers
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.template.defaultfilters import slugify


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
        pass

    def add_permission(self, slug):
        pass

    def remove_permission(self, slug):
        pass

    def add_parent(self, slug):
        pass

    def remove_parent(self, slug):
        pass

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Role, self).save(*args, **kwargs)


class Permission(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Permission, self).save(*args, **kwargs)
