from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password

from datetime import datetime

from .models import User

def authenticate(email=None, password=None):
    try:
        user = User.objects.get(email=email)
        if user.check_password(password) and user.is_active:
            return user
        else:
            return None
    except User.DoesNotExist:
        return None
