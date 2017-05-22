# http://scottlobdell.me/2015/04/decorators-arguments-python/

from django.shortcuts import redirect
from django.core.urlresolvers import reverse, resolve
from django.conf import settings
from django.contrib import messages
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
        next_url = request.resolver_match.url_name
        response = redirect('login')
        response['Location'] += '?' + urllib.parse.urlencode({'next': next_url})
        return response
    return new_fn

def permission_required(permission):
    def new_fn(fn):
        @login_required
        def wrapper(request, *args, **kwargs):
            # TODO: test that permission can be a list
            if permission in request.session["permissions"]:
                # logged in, and we do have the permission
                return fn(request, *args, **kwargs)
            else:
                # logged in, but we don't have the permission
                return redirect("401")
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
                # logged in, but we don't have the role
                return redirect("401")
            return fn(request, *args, **kwargs)
        return wrapper
    return new_fn
