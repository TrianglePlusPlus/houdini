from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password

from houdini_server.models import User # TODO: can we say from django.contrib.auth.models import User?

class AuthBackend(ModelBackend):
    def authenticate(self, email=None, password=None):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id, request=None):
        try:
            user = User.objects.get(pk=user_id)
            if request:
                if not user.is_logged_in(request):
                    return None
            return user
        except User.DoesNotExist:
            return None
