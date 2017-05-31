from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.utils import timezone

class AdminUserManager(UserManager):
    def get_by_natural_key(self, email):
        return self.get(email=email)

    def _create_user(self, email, **extra_fields):
        """
        Creates and saves a User with the given email.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, email, **extra_fields):
        return self._create_user(email, **extra_fields)

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(max_length=100, unique=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'

    objects = AdminUserManager()

    def __str__(self):
        return self.first_name + ' ' + self.last_name
