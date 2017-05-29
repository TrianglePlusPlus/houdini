# http://scottlobdell.me/2015/04/decorators-arguments-python/

from django.shortcuts import redirect
from django.core.urlresolvers import reverse, resolve
from django.conf import settings
from django.contrib import messages
from datetime import datetime
import urllib.parse

from .auth_backend import is_logged_in

def login_required(fn, redirect_login='login'):
    def new_fn(request, *args, **kwargs):
        if is_logged_in(request):
            # logged in already! return the function unmodified
            return fn(request, *args, **kwargs)

        next_url = request.resolver_match.url_name
        response = redirect(redirect_login)
        response['Location'] += '?' + urllib.parse.urlencode({'next': next_url})
        return response
    return new_fn

def permission_required(permission, redirect_401='401'):
    def new_fn(fn):
        @login_required
        def wrapper(request, *args, **kwargs):
            if permission in request.session["permissions"]:
                # logged in, and we do have the permission
                return fn(request, *args, **kwargs)
            else:
                # logged in, but we don't have the permission
                return redirect(redirect_401)
        return wrapper
    return new_fn

def role_required(role, redirect_401='401'):
    def new_fn(fn):
        @login_required
        def wrapper(request, *args, **kwargs):
            if role in request.session["roles"]:
                # logged in, and we do have the role
                return fn(request, *args, **kwargs)
            else:
                # logged in, but we don't have the role
                return redirect(redirect_401)
            return fn(request, *args, **kwargs)
        return wrapper
    return new_fn
