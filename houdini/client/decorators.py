# http://scottlobdell.me/2015/04/decorators-arguments-python/

from django.shortcuts import redirect
from django.core.urlresolvers import reverse, resolve
from django.conf import settings
from datetime import datetime
import urllib.parse

def login_required(fn):
    def new_fn(request, *args, **kwargs):
        # check if logged in
        if request.session.get('logged_in_since'):
            if datetime.now() - datetime.strptime(request.session['logged_in_since'], "%Y-%m-%dT%H:%M:%S") < settings.TIME_TO_LIVE:
                # logged in already! return the function unmodified
                return fn(request, *args, **kwargs)

        # TODO: either redirect to the specified login page OR
        # go to the built-in-to-houdini-client login page
        next_url = resolve(request.path_info).url_name
        response = redirect('login')
        response['Location'] += '?' + urllib.parse.urlencode({'next': next_url})
        return response
    return new_fn

def permission_required(permission):
    def new_fn(fn):
        @login_required
        def wrapper(request, *args, **kwargs):
            # TODO: test that permission can be a list
            print(permission)

            if permission in request.session["permissions"]:
                # logged in, and we do have the permission
                return fn(request, *args, **kwargs)
            else:
                pass
                # if they don't, return error page/status re: permissions
                # TODO: django messages
        return wrapper
    return new_fn

def role_required(role):
    def new_fn(fn):
        @login_required
        def wrapper(request, *args, **kwargs):
            # TODO: test that role can be a list
            if role in request.session["roles"]:
                # logged in, and we do have the role
                return fn(request, *args, **kwargs)
            else:
                pass
                # if they don't, return error page/status re: roles
                # TODO: django messages
            return fn(request, *args, **kwargs)
        return wrapper
    return new_fn

# /new_user or /create_user
# POST data: {
#     email,
#     password,
#     ...
# }
