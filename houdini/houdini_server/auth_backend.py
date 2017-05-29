from django.conf import settings
from django.contrib.auth import get_user_model # TODO: don't need
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password

from datetime import datetime
import jwt

from .models import User

def authenticate_jwt(jwt_string, app_secret):
    # Check to see if the signature is correct
    try:
        data = jwt.decode(jwt_string, app_secret)
        return data
    except jwt.DecodeError:
        return None

def authenticate(email=None, password=None):
    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            if user.is_active:
                return user
            else:
                return False
        else:
            return None
    except User.DoesNotExist:
        return None
