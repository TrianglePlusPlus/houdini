from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.utils import timezone

from datetime import datetime
import jwt
import requests
import urllib.parse

from houdini_server.endpoints import Endpoint
from .forms import LoginForm, RegisterForm
from .auth_backend import FailureType

User = get_user_model()

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        r = {}
        user = authenticate(email=email, password=password, response=r)
        # if we were successfully logged in
        if user:
            messages.success(request, "Successfully logged in")

            auth_login(request, user)

            if r.get('http_response') is not None:
                # decode the JWT received in the HTTP reponse which contains roles/permissions
                data = Endpoint.authenticate_jwt(r['http_response'].text, settings.HOUDINI_SECRET)
                # TODO: check if data == None?
                # TODO: convert roles and permissions to sets?
                # save the roles and permissions in the session
                request.session["roles"] = data["roles"]
                request.session["permissions"] = data["permissions"]
                request.session["logged_in_since"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                # then redirect to the "next" page (which will hit @login_required again)
                return redirect(request.GET.get("next", "index"))
            else:
                # TODO: handle an error
                pass
        # otherwise, response will have been filled in with what went wrong
        else:
            if r.get('failure_type') == FailureType.local_failure:
                # TODO: in this case, i.e. where you authenticate successfully against the auth server
                #       but not locally, we might want to suggest that the user create a local account
                #       that will link up with the existing auth server account and redirect to a view
                # TODO: i also think i need to include houdini_server.http
                return HttpResponseUnauthorized('Invalid user/password combination')
            elif r.get('failure_type') == FailureType.server_failure:
                if r.get('http_response') is not None:
                    messages.error(request, r['http_response'].text)
                else:
                    messages.error(request, "Authentication Server Error")

                response = redirect("login")
                response['Location'] += '?' + urllib.parse.urlencode({'next': request.GET.get("next", "index")})
                return response
            else:
                messages.error(request, "Invalid login.")
    else:
        form = LoginForm()
        return render(request, "houdini_client/login.html", {'form': form})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # make a JWT jwt_string of data signed with app_secret
            jwt_string = jwt.encode({
                "first_name": form.cleaned_data.get("first_name"),
                "middle_name": form.cleaned_data.get("middle_name"),
                "last_name": form.cleaned_data.get("last_name"),
                "email": form.cleaned_data.get("email"),
                "password": form.cleaned_data.get("password")
            }, settings.HOUDINI_SECRET)

            # POST it to the login endpoint
            r = requests.post(settings.HOUDINI_SERVER + "/endpoints/create_user", data={
                "app_key": settings.HOUDINI_KEY,
                "jwt_string": jwt_string
            })

            # if user was successfully created
            if r.status_code == 201:
                # create a local user
                user = User.objects.create_user(
                    form.cleaned_data.get("email"),
                    first_name=form.cleaned_data.get("first_name"),
                    last_name=form.cleaned_data.get("last_name")
                )
                user.save()

                messages.success(request, "User successfully created! Check your email for an activation link.")
                return redirect("index")
            else:
                messages.error(request, r.text)
                return render(request, "houdini_client/register.html", {'form': form})
        else:
            return render(request, "houdini_client/register.html", {'form': form})
    else:
        form = RegisterForm()
        return render(request, "houdini_client/register.html", {'form': form})

def activate(request, key):
    expired = False
    if request.method == "POST":
        # make a JWT jwt_string of the key signed with app_secret
        jwt_string = jwt.encode({
            "activation_key": key
        }, settings.HOUDINI_SECRET)

        # POST it to the activate endpoint
        r = requests.post(settings.HOUDINI_SERVER + "/endpoints/regenerate_activation_key", data={
            "app_key": settings.HOUDINI_KEY,
            "jwt_string": jwt_string
        })

        if r.status_code == 200:
            messages.success(request, r.text)
        else:
            messages.error(request, r.text)
    else:
        # make a JWT jwt_string of the key signed with app_secret
        jwt_string = jwt.encode({
            "activation_key": key
        }, settings.HOUDINI_SECRET)

        # POST it to the activate endpoint
        r = requests.post(settings.HOUDINI_SERVER + "/endpoints/activate_user", data={
            "app_key": settings.HOUDINI_KEY,
            "jwt_string": jwt_string
        })

        if r.status_code == 200:
            messages.success(request, r.text)
        elif r.status_code == 403:
            expired = True
            messages.error(request, r.text)
        else:
            messages.error(request, r.text)

    return render(request, "houdini_client/activation.html", {'expired': expired, 'key': key})

def logout(request):
    messages.success(request, "Successfully logged out")

    auth_logout(request)

    # TODO: ?
    request.session["roles"] = []
    request.session["permissions"] = []
    request.session["logged_in_since"] = (datetime.now() - settings.TIME_TO_LIVE).strftime("%Y-%m-%dT%H:%M:%S")
    # then redirect to the home page
    return redirect('index')
