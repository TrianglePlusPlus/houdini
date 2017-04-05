import jwt
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate

from .models import Application, Profile, Role


# Helper functions and classes


class HttpResponseUnauthorized(HttpResponse):
    """Http 401 response"""

    def __init__(self, reason=None):
        if reason is None:
            super().__init__('401 Unauthorized', status=401)
        else:
            super().__init__('401 Unauthorized: ' + reason, status=401)


def authenticate_jwt(jwt_string, app_secret):
    # Check to see if the signature is correct
    try:
        data = jwt.decode(jwt_string, app_secret)
        return data
    except jwt.DecodeError:
        return None


def get_app(app_key):
    app = Application.objects.filter(app_key=app_key)
    if app.count() != 1:
        return None
    else:
        return app[0]


##### Endpoints


# login
# logout
# change password
# reset password


def login_user(request):
    # If they don't POST then throw an error immediately
    if request.method != 'POST':
        return HttpResponse(status=500)
    app_key = request.POST.get('app_key', None)
    app = get_app(app_key)
    if app is None:
        return HttpResponse(status=500)
    jwt_string = request.POST.get('jwt_string', None)
    if jwt_string is None:
        # We'll return a server error if they don't actually send anything
        return HttpResponse(status=500)
    data = authenticate_jwt(jwt_string, app.app_secret)
    if data is None:
        return HttpResponseUnauthorized('App key or web token signature invalid.')
    # App exists and the data is signed correctly
    username = data['username']
    password = data['password']
    user = authenticate(user=username, password=password)
    if user is None:
        return HttpResponseUnauthorized('Invalid user/password combination')
    # Get all of the roles for the profile they are logging in as
    profile = Profile.get_all_profiles()[data['profile']]
    profile_roles = set(profile.roles_set.all())
    # Get all of the roles the user has
    user_roles = set(user.roles_set.all())
    relevant_roles = profile_roles.intersection(user_roles)