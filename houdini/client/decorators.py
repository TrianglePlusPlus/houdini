# http://scottlobdell.me/2015/04/decorators-arguments-python/

from django.shortcuts import redirect
from django.core.urlresolvers import reverse, resolve
from datetime import datetime, timedelta
import urllib.parse
time_to_live = timedelta(minutes=1)

def login_required(fn):
    def new_fn(request, *args, **kwargs):
        # check if logged in
        if request.session.get('logged_in_since'):
            if datetime.now() - datetime.strptime(request.session['logged_in_since'], "%Y-%m-%dT%H:%M:%S") < time_to_live:
                # dope! return the function unmodified
                return fn(request, *args, **kwargs)
        # [3]
        # either redirect to the specified login page OR        > both pass the next page in the url
        # go to the built-in-to-houdini-client login page       > ""

        next_url = resolve(request.path_info).url_name
        response = redirect('login')
        response['Location'] += '?' + urllib.parse.urlencode({'next': next_url})
        return response
    return new_fn

def permission_required(permission):
    def new_fn(fn):
        def wrapper(request, *args, **kwargs):
            # TODO: error check permission?
            # can be a list

            print(permission)
            # check if logged in
            # if not
                # call login_required shit and redirect back here (case [3] up top)
            # if yes
                # check if current login session has required permission(s)
                # if they do, return function! you're good to go
                # if they don't, return error page/status re: permissions

            return fn(request, *args, **kwargs)
        return wrapper
    return new_fn

def role_required(role):
    def new_fn(fn):
        def wrapper(request, *args, **kwargs):
            # TODO: error check role?
            # can be a list

            print(role)
            # check if logged in
            # if not
                # call login_required shit and redirect back here (case [3] up top)
            # if yes
                # check if current login session has required role(s)
                # if they do, return function! you're good to go
                # if they don't, return error page/status re: roles

            return fn(request, *args, **kwargs)
        return wrapper
    return new_fn


# /login:
# POST data: {
#     'app_key': __,
#     'jwt_string': {
#         email,
#         password
#     } => signed with app_secret
# }
# response: {
#     roles: [],
#     permissions: []
# }

# /new_user or /create_user
# POST data: {
#     email,
#     password,
#     ...
# }
