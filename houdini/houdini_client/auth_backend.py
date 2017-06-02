from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from django.utils import timezone

from datetime import datetime
from enum import Enum
import jwt
import pytz
import requests

User = get_user_model()

def authenticate_jwt(jwt_string, app_secret):
    # Check to see if the signature is correct
    try:
        data = jwt.decode(jwt_string, app_secret)
        return data
    except jwt.DecodeError:
        return None

def is_logged_in(request):
    if request.session.get('logged_in_since'):
        logged_in_since = datetime.strptime(request.session['logged_in_since'], settings.ISO_8601)
        logged_in_since = pytz.utc.localize(logged_in_since)
        return (timezone.now() - logged_in_since) < settings.TIME_TO_LIVE
    else:
        return False

FailureType = Enum('FailureType', 'server_failure local_failure')

class RemoteServerAuthBackend(ModelBackend):
    def authenticate(self, email=None, password=None, response=None):
        if response is None:
            response = {}

        # make a JWT jwt_string of data signed with app_secret
        jwt_string = jwt.encode({
            "email": email,
            "password": password
        }, settings.HOUDINI_SECRET)

        # POST it to the login endpoint
        r = requests.post(
            settings.HOUDINI_SERVER + "/endpoints/login",
            # cert=settings.SSL_DEV_CERT_KEY,
            data={
                "app_key": settings.HOUDINI_KEY,
                "jwt_string": jwt_string
        })

        # if we were successfully logged in
        if r.status_code == 200:
            try:
                user = User.objects.get(email=email)
                response['success'] = True
                response['http_response'] = r
                return user
            except User.DoesNotExist:
                response['failure_type'] = FailureType.local_failure
                response['http_response'] = r
                return None
        else:
            response['failure_type'] = FailureType.server_failure
            response['http_response'] = r
            return None

    def get_user(self, user_id, request=None):
        try:
            user = User.objects.get(pk=user_id)
            if request:
                if not is_logged_in(request):
                    return None
            return user
        except User.DoesNotExist:
            return None
