from django.contrib.auth import hashers
from django.db import models
from django.template.defaultfilters import slugify

class Permission(models.Model):
	name = models.CharField(max_length=128, unique=True)
	slug = models.SlugField()

	@classmethod
	def create(cls, name):
		permission = cls(name=name)
		return permission

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Permission, self).save(*args, **kwargs)


class Role(models.Model):
	name = models.CharField(max_length=128, unique=True)
	slug = models.SlugField()
	parents = models.ManyToManyField('self')

	@classmethod
	def create(cls, name):
		role = cls(name=name)
		return role

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Role, self).save(*args, **kwargs)

class BaseUser(models.Model):
	first_name = models.CharField(max_length=128)
	last_name = models.CharField(max_length=128)
	email = models.CharField(max_length=128)
	password = models.CharField(max_length=128)

	def set_password(self, password):
		self.password = hashers.make_password(password)

class Employee(BaseUser):
	pass
